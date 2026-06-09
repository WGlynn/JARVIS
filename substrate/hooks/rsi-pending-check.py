#!/usr/bin/env python3
"""SessionStart hook: scan the Full Stack RSI project file for pending loops.

Replaces the prior `cat memory/project_full-stack-rsi.md 2>/dev/null | python -c ...`
one-liner in settings.json. That one-liner was broken:

  - It cat'd a file path that no longer exists (the RSI file was moved to
    memory/nda-locked/ during the NDA gate rollout).
  - 2>/dev/null silently swallowed the cat failure.
  - The downstream python -c received empty stdin and emitted '0 loops pending'.
  - Result: boot hook lied about state, Claude proposed already-closed cycles.

Fix: probe both candidate paths. Fail loud if neither exists. Count PENDING
markers in the file that does exist.
"""
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CANDIDATE_PATHS = [
    os.path.expanduser(
        "~/.claude/projects/C--Users-Will/memory/nda-locked/project_full-stack-rsi.md"
    ),
    os.path.expanduser(
        "~/.claude/projects/C--Users-Will/memory/project_full-stack-rsi.md"
    ),
]


def locate_rsi_file() -> tuple[str | None, list[str]]:
    tried: list[str] = []
    for p in CANDIDATE_PATHS:
        tried.append(p)
        if os.path.exists(p):
            return p, tried
    return None, tried


def scan_pending(path: str) -> list[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return []
    return [line for line in content.splitlines() if "PENDING" in line]


def build_context(pending: list[str], rsi_path: str | None, tried: list[str]) -> str:
    if rsi_path is None:
        tried_str = "\n  - ".join(tried)
        return (
            "[WARN] project_full-stack-rsi.md not found at any candidate path:\n"
            f"  - {tried_str}\n"
            "Boot-time RSI-pending check disabled. File may have moved again; "
            "update rsi-pending-check.py CANDIDATE_PATHS."
        )
    count = len(pending)
    header = (
        f"FULL STACK RSI CHECK: {count} loops pending "
        f"({os.path.basename(os.path.dirname(rsi_path))}/{os.path.basename(rsi_path)}). "
        "Read SESSION_STATE.md first (now wired as separate SessionStart hook), "
        "then project_full-stack-rsi.md and propose next loop."
    )
    if pending:
        return header + " Loops: " + " | ".join(pending)
    return header


def main() -> int:
    hook_mode = not sys.stdin.isatty()
    if hook_mode:
        try:
            json.load(sys.stdin)
        except Exception:
            pass

    rsi_path, tried = locate_rsi_file()
    pending = scan_pending(rsi_path) if rsi_path else []
    context = build_context(pending, rsi_path, tried)

    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }

    if hook_mode:
        print(json.dumps(out))
    else:
        print(context)
    return 0


if __name__ == "__main__":
    sys.exit(main())
