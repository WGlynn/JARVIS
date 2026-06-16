#!/usr/bin/env python3
"""SessionStart hook: auto-load the deterministic context handoff.

Pairs with tools/token-audit/context-rotation-hook.py, which writes a mechanical
handoff to ~/.claude/hooks/.ctx-handoff/LATEST.md on every +50k of context. This
loader surfaces it at boot so the human NEVER has to type "load context" --
that manual workaround is the bug, not the fix
(memory: unnecessary-human-work-bar-ratchet).

Only surfaces if the handoff is FRESH (mtime within FRESH_HOURS) so a stale
floor from a long-dead session doesn't masquerade as live state. The rich
curated SESSION_STATE.md remains the primary; this is the always-current
mechanical backstop that fires even when the model-written handoff was starved.
"""
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

LATEST = os.path.expanduser("~/.claude/hooks/.ctx-handoff/LATEST.md")
FRESH_HOURS = 18


def load() -> str:
    if not os.path.exists(LATEST):
        return ""
    try:
        import time

        age_h = (time.time() - os.path.getmtime(LATEST)) / 3600.0
    except Exception:
        age_h = 0.0
    if age_h > FRESH_HOURS:
        return ""
    try:
        with open(LATEST, "r", encoding="utf-8") as f:
            body = f.read().strip()
    except Exception as e:
        return f"[WARN] ctx-handoff LATEST.md unreadable: {e}"
    if not body:
        return ""
    return (
        "[CTX-HANDOFF -- deterministic auto-resume (no 'load context' needed)]\n"
        f"(age ~{age_h:.1f}h; mechanical floor, written by context-rotation-hook)\n\n"
        f"{body}"
    )


def main() -> int:
    hook_mode = not sys.stdin.isatty()
    if hook_mode:
        try:
            json.load(sys.stdin)
        except Exception:
            pass

    ctx = load()
    if not ctx:
        # silent: nothing fresh to resume (clean boot)
        return 0

    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": ctx,
        }
    }
    if hook_mode:
        print(json.dumps(out))
    else:
        print(ctx)
    return 0


if __name__ == "__main__":
    sys.exit(main())
