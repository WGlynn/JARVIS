#!/usr/bin/env python3
"""
Boot staleness check for the crash-recovery backtest witness (in-system alarm).

Pairs with crash-recovery-backtest.py (external checker, run by an OS-level
scheduler that fires even when Claude is closed). That backtest stamps
shield/backtest-witness.json on every run. This hook, wired into SessionStart,
reads that witness and surfaces LOUD when the recovery path's health is in doubt:

  - witness MISSING   -> recovery-path health was NEVER verified
  - witness UNREADABLE -> corrupted; treat as unverified
  - last run FAILED    -> the recovery path is broken right now
  - witness STALE      -> the external scheduler is likely dead (its own liveness
                          failing silently is exactly the class of bug we hunt)

Healthy + fresh + passing -> SILENT (a clean boot adds zero noise).

This is the "absence is loud" half of the external-witness design: a monotonic
marker written outside the boot path, checked at boot, so a missing recovery
verification is a visible alarm instead of an invisible non-event.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

WITNESS = Path(__file__).parent / "shield" / "backtest-witness.json"
STALE_DAYS = 2.0
RUN_HINT = "python ~/.claude/session-chain/crash-recovery-backtest.py"


def main():
    if not WITNESS.exists():
        print("=== RECOVERY-PATH WITNESS: MISSING ===")
        print("The crash-recovery backtest has NEVER stamped a witness.")
        print("Recovery-path health is UNVERIFIED. This is the alarm working, not a false one.")
        print(f"run: {RUN_HINT}")
        return

    try:
        d = json.loads(WITNESS.read_text(encoding="utf-8"))
    except Exception as e:
        print("=== RECOVERY-PATH WITNESS: UNREADABLE ===")
        print(f"{type(e).__name__}: {e} -- treat recovery-path health as unverified.")
        print(f"run: {RUN_HINT}")
        return

    last = d.get("last_run", "?")
    ok = bool(d.get("ok"))

    # Compute staleness against the last stamped run.
    stale = False
    age_txt = "unknown"
    try:
        dt = datetime.fromisoformat(last)
        age_days = (datetime.now(timezone.utc) - dt).total_seconds() / 86400.0
        age_txt = f"{age_days:.1f}d"
        stale = age_days > STALE_DAYS
    except Exception:
        stale = True  # unparseable timestamp -> treat as stale

    if not ok:
        print("=== RECOVERY-PATH WITNESS: LAST RUN FAILED ===")
        print(f"backtest {d.get('passed')}/{d.get('total')} at {last}; scenarios={d.get('scenarios')}")
        print("The crash-recovery path is BROKEN. Investigate before trusting recovery.")
        print(f"re-run: {RUN_HINT}")
    elif stale:
        print("=== RECOVERY-PATH WITNESS: STALE ===")
        print(f"Last backtest pass was {age_txt} ago ({last}); threshold is {STALE_DAYS}d.")
        print("The external scheduler (Task Scheduler: JARVIS-CrashRecoveryBacktest) may be dead.")
        print(f"run: {RUN_HINT}  and verify: schtasks /Query /TN JARVIS-CrashRecoveryBacktest")
    # healthy + fresh + passing -> silent by design


if __name__ == "__main__":
    main()
