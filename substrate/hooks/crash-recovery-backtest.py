#!/usr/bin/env python3
"""
Crash-Recovery Backtest Harness — proves the recovery path actually recovers.

THE BUG THIS WOULD HAVE CAUGHT (2026-04-15 .. 2026-07-29): api-death-shield
faithfully wrote 93 crash markers, and NO SessionStart hook ever surfaced them.
The recovery machinery worked; nothing pulled the trigger. A green backtest that
asserts "every injected crash appears in the next boot's recovery output, AND
the boot is actually wired to run it" goes RED the moment either half breaks.

Non-destructive: runs entirely in a throwaway temp sandbox. The api-death-shield
module keeps its state paths as module-level globals; the harness imports the
module and rebinds those globals to the sandbox, so no real shield state (real
crashes/, ledger, heartbeat) is ever read or written.

Scenarios (each is a before/after diff — snapshot known-facts, run recovery,
measure what survived):
  1. inject-and-recover : seed K synthetic crashes carrying unique canary tokens
     -> run boot_report() -> assert every canary survives into the durable full
     report AND/OR the ledger, and the markers were archived. LOSS = any canary
     present in the snapshot but absent from recovery output.
  2. clean-boot-silent  : empty sandbox -> boot_report() must return None. Guards
     the opposite failure: phantom recovery / boot noise when nothing crashed.
  3. wiring-live-check   : read the REAL settings.json and assert a SessionStart
     hook actually invokes `api-death-shield ... boot-report`. This is the
     external witness at the config layer — it catches "machinery exists but is
     unwired", the precise shape of the original 93-crash bug.

Exit 0 = all pass. Exit 1 = any loss/failure. CI-able; run before trusting the
crash-recovery path after any change to api-death-shield or settings.json.
"""

import importlib.util
import json
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

CHAIN_DIR = Path(__file__).parent
SHIELD_SCRIPT = CHAIN_DIR / "api-death-shield.py"
SETTINGS_JSON = Path("~/.claude/settings.json")
# Monotonic witness file, written to the REAL shield dir (never the sandbox).
# An OS-level scheduler runs this backtest daily and stamps this file; the boot
# staleness check reads it. If it is absent, stale, or records a failure, the
# boot surfaces it LOUD -- the external-witness design: the checker lives outside
# the system that can fail, and absence is loud, not invisible.
WITNESS_FILE = CHAIN_DIR / "shield" / "backtest-witness.json"


def load_shield_module():
    """Import api-death-shield.py (hyphenated name -> importlib) fresh."""
    spec = importlib.util.spec_from_file_location("api_death_shield", SHIELD_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sandbox_module(mod, sandbox):
    """Rebind the module's state-path globals into an isolated sandbox dir."""
    mod.SHIELD_DIR = sandbox
    mod.CRASH_MARKERS_DIR = sandbox / "crashes"
    mod.CONVERSATION_LOG = sandbox / "conversation.log"
    mod.HEARTBEAT_FILE = sandbox / "heartbeat.json"
    mod.LOG_FILE = sandbox / "shield.log"
    mod.LAST_RECOVERY_REPORT = sandbox / "LAST_RECOVERY_REPORT.md"
    mod.RECOVERY_LEDGER = sandbox / "recovery-ledger.jsonl"
    mod.ensure_dirs()


def inject_crash(mod, i, canary):
    """
    Write a synthetic crash marker directly (bypassing write_crash_marker so we
    never shell out to real git). The canary token is embedded in BOTH the error
    string and a dirty-file path, so it must survive through recovery_report()'s
    error line and file listing.
    """
    ts = f"20200101-0000{i:02d}"
    marker = mod.CRASH_MARKERS_DIR / f"crash-{ts}.json"
    marker.write_text(json.dumps({
        "timestamp": f"2020-01-01T00:00:{i:02d}+00:00",
        "error": f"server_error CANARY={canary}",
        "last_heartbeat": {"timestamp": "2020-01-01T00:00:00+00:00", "turn_count": 100 + i},
        "git_status": {"dirty_files": 1, "files": [f"M canary_{canary}.sol"]},
    }), encoding="utf-8")
    return canary


def scenario_inject_and_recover(k=12):
    """Snapshot K canaries -> recover -> diff. Returns (ok, detail)."""
    sandbox = Path(tempfile.mkdtemp(prefix="crash-backtest-inject-"))
    try:
        mod = load_shield_module()
        sandbox_module(mod, sandbox)

        # last-known-good state (what a real boot would also have)
        mod.HEARTBEAT_FILE.write_text(json.dumps(
            {"timestamp": "2020-01-01T00:00:00+00:00", "turn_count": 100, "git_head": "deadbeef"}
        ), encoding="utf-8")
        mod.CONVERSATION_LOG.write_text("[2020-01-01] USER:\nseed conversation\n", encoding="utf-8")

        # SNAPSHOT: inject K crashes with unique canaries
        canaries = [f"C{i:03d}X{(i*7 + 13) % 997:03d}" for i in range(k)]
        for i, c in enumerate(canaries):
            inject_crash(mod, i, c)

        unprocessed_before = len(list(mod.CRASH_MARKERS_DIR.glob("crash-*.json")))

        # RUN RECOVERY (the exact path SessionStart invokes)
        summary = mod.boot_report()

        # MEASURE what survived
        report_text = mod.LAST_RECOVERY_REPORT.read_text(encoding="utf-8") if mod.LAST_RECOVERY_REPORT.exists() else ""
        ledger_text = mod.RECOVERY_LEDGER.read_text(encoding="utf-8") if mod.RECOVERY_LEDGER.exists() else ""
        unprocessed_after = len(list(mod.CRASH_MARKERS_DIR.glob("crash-*.json")))
        archived_after = len(list(mod.CRASH_MARKERS_DIR.glob("crash-*.processed")))

        lost = [c for c in canaries if (c not in report_text and c not in ledger_text)]

        checks = {
            "summary_returned": summary is not None,
            "all_canaries_recovered": len(lost) == 0,
            "markers_archived": unprocessed_after == 0 and archived_after == k,
            "count_line_present": summary is not None and f"{k} unprocessed" in summary,
        }
        ok = all(checks.values())
        detail = (
            f"{k - len(lost)}/{k} canaries recovered, {len(lost)} lost; "
            f"unprocessed {unprocessed_before}->{unprocessed_after}, archived={archived_after}"
        )
        if lost:
            detail += f"; LOST={lost[:5]}"
        if not ok:
            detail += f"; failed_checks={[c for c, v in checks.items() if not v]}"
        return ok, detail
    finally:
        shutil.rmtree(sandbox, ignore_errors=True)


def scenario_clean_boot_silent():
    """Empty sandbox -> boot_report() must be None (no phantom recovery)."""
    sandbox = Path(tempfile.mkdtemp(prefix="crash-backtest-clean-"))
    try:
        mod = load_shield_module()
        sandbox_module(mod, sandbox)
        summary = mod.boot_report()
        ok = summary is None
        return ok, ("silent (None) as required" if ok else f"phantom recovery: {summary!r}")
    finally:
        shutil.rmtree(sandbox, ignore_errors=True)


def scenario_wiring_live_check():
    """
    Read the REAL settings.json and assert a SessionStart hook invokes
    `api-death-shield ... boot-report`. This is the regression guard: the
    original bug was machinery-present-but-unwired, invisible at runtime.
    """
    try:
        d = json.loads(SETTINGS_JSON.read_text(encoding="utf-8"))
    except Exception as e:
        return False, f"could not parse settings.json: {type(e).__name__}: {e}"

    cmds = [
        h.get("command", "")
        for grp in d.get("hooks", {}).get("SessionStart", [])
        for h in grp.get("hooks", [])
    ]
    wired = any("api-death-shield" in c and "boot-report" in c for c in cmds)
    return wired, (
        "settings.json SessionStart -> api-death-shield boot-report"
        if wired else
        "NOT WIRED: no SessionStart hook calls boot-report (the 93-crash bug)"
    )


def write_witness(scenarios, passed, total):
    """Stamp the monotonic witness file the boot staleness-check reads."""
    try:
        WITNESS_FILE.parent.mkdir(parents=True, exist_ok=True)
        WITNESS_FILE.write_text(json.dumps({
            "last_run": datetime.now(timezone.utc).isoformat(),
            "ok": passed == total,
            "passed": passed,
            "total": total,
            "scenarios": scenarios,
        }, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"WARN: could not write witness file: {e}", file=sys.stderr)


def main():
    print("=== CRASH-RECOVERY BACKTEST ===")
    scenarios = {}

    ok, detail = scenario_inject_and_recover(k=12)
    scenarios["inject-and-recover"] = ok
    print(f"[1] inject-and-recover .... {'PASS' if ok else 'FAIL'}  ({detail})")

    ok, detail = scenario_clean_boot_silent()
    scenarios["clean-boot-silent"] = ok
    print(f"[2] clean-boot-silent ..... {'PASS' if ok else 'FAIL'}  ({detail})")

    ok, detail = scenario_wiring_live_check()
    scenarios["wiring-live-check"] = ok
    print(f"[3] wiring-live-check ..... {'PASS' if ok else 'FAIL'}  ({detail})")

    passed = sum(scenarios.values())
    total = len(scenarios)
    write_witness(scenarios, passed, total)
    print(f"RESULT: {passed}/{total} PASS  (witness -> {WITNESS_FILE.name})")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
