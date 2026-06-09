#!/usr/bin/env python3
"""
Autopilot Allow Hook
====================

PreToolUse hook that auto-approves tool calls when autopilot mode is active.

Toggle:
  Enable:  touch ~/.claude/.autopilot-active
  Disable: rm    ~/.claude/.autopilot-active

When active, emits permissionDecision:"allow" so Claude Code skips the
user-facing approval prompt. Other PreToolUse gates (HIERO, substance gate,
NDA gate, partner-facing additive) still run their integrity checks and can
still block via {"continue": false}. This hook ONLY suppresses the approval
prompt; it does NOT bypass safety gates.

Origin: 2026-05-06 — autonomous run, Will: "we need a hook to bypass these
[permission prompts]. on autopilot they are a nuisance."

Sibling: feedback_diagnose-on-stop.md (Stop-event interrogation during runs).
"""
import json
import os
import sys
from pathlib import Path

FLAG = Path.home() / ".claude" / ".autopilot-active"


def main() -> int:
    # Drain stdin (the hook input). We do not need its contents — autopilot
    # is a session-level flag, not a per-tool decision.
    try:
        sys.stdin.read()
    except Exception:
        pass

    if not FLAG.exists():
        # Autopilot off — no decision; let other gates / default permissions decide.
        return 0

    # Autopilot on — auto-allow this tool call.
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "autopilot mode active (~/.claude/.autopilot-active flag set)",
        },
        "suppressOutput": True,
    }
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
