#!/usr/bin/env python3
"""SessionStart hook: load the latest SESSION_STATE.md pending-next section.

CLAUDE.md declares SESSION_STATE.md "MANDATORY first read" but no hook was
enforcing it — pure memory-layer rule, textbook Verbal->Gate violation.
This script converts the rule to hook-level enforcement.

Reads vibeswap/.claude/SESSION_STATE.md, extracts from the top of the latest
session block up to (but excluding) the first "## Completed" section or the
first "---" separator, and emits as additionalContext.

Fails loud: missing file or unreadable content surfaces as [WARN] to Claude
rather than silently skipping.
"""
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SESSION_STATE_PATH = os.path.expanduser("~/vibeswap/.claude/SESSION_STATE.md")
MAX_LINES = 140


def extract_pending(path: str) -> str:
    if not os.path.exists(path):
        return (
            f"[WARN] SESSION_STATE.md missing at {path}. "
            "CLAUDE.md declares this mandatory-first-read. "
            "Check path or restore from git before proceeding."
        )
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        return f"[WARN] SESSION_STATE.md unreadable: {e}"

    out: list[str] = []
    for i, line in enumerate(lines):
        if line.startswith("## Completed"):
            break
        if line.strip() == "---" and out:
            break
        out.append(line.rstrip())
        if len(out) >= MAX_LINES:
            out.append("... (truncated -- open SESSION_STATE.md for full block)")
            break
    return "\n".join(out).strip()


def main() -> int:
    hook_mode = not sys.stdin.isatty()
    if hook_mode:
        try:
            json.load(sys.stdin)
        except Exception:
            pass

    pending = extract_pending(SESSION_STATE_PATH) or "[WARN] SESSION_STATE empty"

    context = (
        "[SESSION_STATE.md -- mandatory first read per CLAUDE.md protocol chain]\n"
        f"{pending}\n\n"
        "Full file: vibeswap/.claude/SESSION_STATE.md (read it before proposing next steps)."
    )

    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }

    if hook_mode:
        print(json.dumps(out))
    else:
        print(pending)
    return 0


if __name__ == "__main__":
    sys.exit(main())
