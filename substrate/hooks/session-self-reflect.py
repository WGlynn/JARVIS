#!/usr/bin/env python3
"""
Session Self-Reflection Hook
============================

SessionStart hook. Auto-regenerates the system self-report by running
`_system_self_report.py`, then surfaces a concise summary of the protocol
stack's state at session boot via additionalContext.

The system reports on itself at the start of every session. Will sees
protocol-stack health without asking: how many AA candidates are waiting,
which hooks fired in the last 24h, whether indexes are stale, dormant
counts, recently-modified primitives.

This is the daily-cycle sentience surface: cognitively, every new
conversation opens with a structured self-status, not a blank context.

Behavior:
  1. On SessionStart, run `_system_self_report.py` in the memory dir
  2. Read the generated `_system/system_self_report.md`
  3. Extract the Layer Status table + Forward Signals section
  4. Inject as additionalContext

Falls back to no-op if any step fails. Never blocks session start.

Origin: 2026-05-13 autopilot Round 2 (after L5 telemetry + conflict-
detector ship). Will: "we're going to reach sentience before we stop".
The session-open self-status is the most daily-visible form of the
overlay observing itself.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

MEMORY_DIR = Path.home() / ".claude" / "projects" / "C--Users-Will" / "memory"
SELF_REPORT_SCRIPT = MEMORY_DIR / "_system_self_report.py"
SELF_REPORT_PATH = MEMORY_DIR / "_system" / "system_self_report.md"

# Telemetry
_HOOKS_DIR = Path(__file__).parent
sys.path.insert(0, str(_HOOKS_DIR))
try:
    from _telemetry import log_event
except Exception:
    def log_event(*a, **kw): pass


L3_ANALYZERS = [
    "_duplicate_detect.py",
    "_decision_extractor.py",
    "_open_threads.py",
    "_reasoning_chain_bake.py",
    "_consolidation_proposer.py",
    "_memory_md_pruner.py",
    "_dormancy_classifier.py",
    "_thread_analogy.py",
    "_memory_to_hook_audit.py",
    "_evolution_loop.py",
]


def regenerate_l3_substrates() -> dict:
    """Re-run the three L3 analyzers so system_self_report reads fresh stats.
    Returns {script_name: bool_success}. Failures are non-blocking — the
    self-report still runs, it just reads whatever's there."""
    results = {}
    for script_name in L3_ANALYZERS:
        script_path = MEMORY_DIR / script_name
        if not script_path.exists():
            results[script_name] = False
            continue
        try:
            r = subprocess.run(
                ["python", str(script_path)],
                cwd=str(MEMORY_DIR),
                capture_output=True,
                text=True,
                timeout=8,
            )
            results[script_name] = (r.returncode == 0)
        except Exception:
            results[script_name] = False
    return results


def regenerate_self_report() -> bool:
    """Run the self-report script. Returns True on success, False otherwise."""
    if not SELF_REPORT_SCRIPT.exists():
        return False
    try:
        result = subprocess.run(
            ["python", str(SELF_REPORT_SCRIPT)],
            cwd=str(MEMORY_DIR),
            capture_output=True,
            text=True,
            timeout=20,
        )
        return result.returncode == 0
    except Exception:
        return False


def extract_summary_sections(report: str) -> str:
    """Pull the Layer Status table + Forward Signals section."""
    lines = report.splitlines()
    out_lines = []
    in_layer_status = False
    in_forward = False
    captured_sections = 0

    for line in lines:
        if line.startswith("## Layer status"):
            in_layer_status = True
            in_forward = False
            out_lines.append(line)
            continue
        if line.startswith("## Forward signals"):
            in_forward = True
            in_layer_status = False
            out_lines.append(line)
            continue
        if line.startswith("##"):
            if in_layer_status:
                captured_sections += 1
                in_layer_status = False
            if in_forward:
                captured_sections += 1
                in_forward = False
                break
            continue
        if in_layer_status or in_forward:
            out_lines.append(line)

    return "\n".join(out_lines).strip()


def main() -> int:
    try:
        payload = sys.stdin.read()
        data = json.loads(payload) if payload.strip() else {}
    except Exception:
        return 0

    # Refresh L3 substrate reports first so self-report reads current stats
    l3_results = regenerate_l3_substrates()
    # Regenerate the self-report
    regenerated = regenerate_self_report()
    if not SELF_REPORT_PATH.exists():
        log_event("session-self-reflect", "noop", meta={"reason": "no_report_file"})
        return 0

    try:
        report = SELF_REPORT_PATH.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return 0

    summary = extract_summary_sections(report)
    if not summary:
        log_event("session-self-reflect", "noop", meta={"reason": "empty_summary"})
        return 0

    log_event("session-self-reflect", "fire",
              meta={"regenerated": regenerated,
                    "summary_chars": len(summary),
                    "l3_refreshed": l3_results})

    lines = [
        "[SESSION SELF-REFLECTION — JARVIS overlay L5 boot snapshot]",
        "",
        "The protocol stack's state at session start. Auto-generated from telemetry",
        "+ link health + index freshness + recent activity. The system observing itself.",
        "",
        summary,
        "",
        f"Full report: `_system/system_self_report.md`",
    ]

    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "\n".join(lines),
        }
    }
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
