#!/usr/bin/env python3
"""
Deep Context Mode -- Activator  (UserPromptSubmit)
==================================================
When the session has crossed C1 (>= 500k tokens), inject a compact behavior
switch so the model ACTIVELY manages its own context past the cliff instead of
just being warned. Below 500k this hook emits NOTHING (early return) -- normal
sessions are untouched, byte-identical to before.

Signal: _seen_set.is_deep_context(session_id) == the {session}.c1 sentinel written
by tools/token-audit/context-rotation-hook.py. Shared with the context loaders so
mode state is single-sourced and they never disagree.

Also does cheap housekeeping every turn: prune seen-set files older than 7 days.

Fail-open: any error -> emit nothing -> normal behavior. Never blocks a prompt.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
try:
    from _telemetry import log_event
except Exception:
    def log_event(*a, **kw):
        pass
try:
    import _seen_set as ss
except Exception:
    ss = None

INSTRUCTIONS = """\
[DEEP CONTEXT MODE -- active: this session is past ~500k tokens]

You are past the effective-context cliff, where middle-of-window content stops
being reliably attended to. Actively manage context -- do not just keep appending:

- Keep tool outputs lean. Prefer Read with offset/limit, Grep/Glob over full-file
  reads, and targeted Bash. If a result will be large, write it to disk and keep
  only the relevant slice in your reply.
- Delegate context-heavy subtasks (reading >5 files, deep web research, large test
  runs) to a sub-agent so their exploratory context never enters this window.
- Put load-bearing state at the TAIL of your turn (the recency zone), not buried.
- When a subtask is fully resolved, say so in one line and drop its detail -- you
  can re-read it from disk if needed.
- Warm-memory shards already injected this session are being auto-suppressed;
  Read a specific memory file on demand if you need it again.
- If context is genuinely exhausted for the task, a clean session rotation (the
  handoff is auto-saved) beats fighting a degraded window."""


def main() -> int:
    try:
        payload = sys.stdin.read()
        data = json.loads(payload) if payload.strip() else {}
    except Exception:
        return 0

    if ss is None:
        return 0

    session_id = data.get("session_id") or data.get("sessionId") or ""

    # cheap housekeeping -- only deletes seen-set files older than 7 days
    try:
        ss.prune(days=7)
    except Exception:
        pass

    try:
        if not ss.is_deep_context(session_id):
            return 0
    except Exception:
        return 0

    log_event("deep-context-mode-activator", "fire",
              meta={"session": str(session_id)[:8]})
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": INSTRUCTIONS,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
