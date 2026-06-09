#!/usr/bin/env python3
"""
Post-Generation Recall — L4 of JARVIS overlay (recovery 2026-05-14)
====================================================================

UserPromptSubmit hook. Reads the most recent post-generation reflection
written by `post-generation-reflect.py` (Stop hook) and injects it as
additionalContext for the next assistant turn.

History
-------
The original L4 design was a Stop hook that injected `additionalContext`
directly. That output is rejected by Claude Code's schema validator
(Stop event does not support `hookSpecificOutput.additionalContext`).
The hook had been firing for 16+ hours producing invalid JSON; the
reflection content was being computed and silently discarded.

This hook recovers the L4 signal across turn boundaries:
  1. Stop hook (`post-generation-reflect.py`) persists reflection to
     `_system/post_gen_reflections.jsonl`
  2. This hook (UserPromptSubmit) reads the latest unprocessed entry
     and injects it as additionalContext
  3. Marker file `_system/post_gen_reflections.cursor` tracks which
     reflections have been delivered so we don't re-inject

Conservative behaviour:
  - Only injects if the reflection is fresh (within last 30 min of wall
    time) so stale reflections from old sessions don't surface
  - Drops if rendered content is empty
  - Silent no-op on any error (matches the rest of the hook chain's
    fail-safe contract)
"""
import datetime as dt
import json
import os
import sys
from pathlib import Path

MEMORY_DIR = Path.home() / ".claude" / "projects" / "C--Users-Will" / "memory"
REFLECTION_LOG = MEMORY_DIR / "_system" / "post_gen_reflections.jsonl"
CURSOR_PATH = MEMORY_DIR / "_system" / "post_gen_reflections.cursor"

FRESHNESS_WINDOW_SECONDS = 30 * 60  # 30 min

# Telemetry
_HOOKS_DIR = Path(__file__).parent
sys.path.insert(0, str(_HOOKS_DIR))
try:
    from _telemetry import log_event
except Exception:
    def log_event(*a, **kw): pass


def read_cursor() -> int:
    """Return the byte-offset of the last delivered reflection (0 if first
    run or cursor missing)."""
    if not CURSOR_PATH.exists():
        return 0
    try:
        return int(CURSOR_PATH.read_text(encoding="utf-8").strip())
    except Exception:
        return 0


def write_cursor(offset: int):
    try:
        CURSOR_PATH.parent.mkdir(parents=True, exist_ok=True)
        CURSOR_PATH.write_text(str(offset), encoding="utf-8")
    except Exception:
        pass


def fetch_undelivered_reflections() -> tuple[list[dict], int]:
    """Read reflections newer than the cursor offset. Return (entries, new_offset)."""
    if not REFLECTION_LOG.exists():
        return [], 0
    cursor = read_cursor()
    try:
        with REFLECTION_LOG.open("rb") as f:
            f.seek(cursor)
            data = f.read()
            new_offset = f.tell()
    except Exception:
        return [], cursor
    entries = []
    for line in data.decode("utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except Exception:
            continue
    return entries, new_offset


def is_fresh(entry: dict) -> bool:
    ts = entry.get("ts", "")
    try:
        recorded = dt.datetime.fromisoformat(ts[:19])
        return (dt.datetime.now() - recorded).total_seconds() <= FRESHNESS_WINDOW_SECONDS
    except Exception:
        return False


def main() -> int:
    try:
        payload = sys.stdin.read()
        _ = json.loads(payload) if payload.strip() else {}
    except Exception:
        return 0

    entries, new_offset = fetch_undelivered_reflections()
    if not entries:
        return 0

    # Take only the most recent fresh entry; older reflections are stale
    # relative to the current turn. Advance the cursor past everything we
    # saw so we don't re-deliver later.
    fresh = [e for e in entries if is_fresh(e)]
    write_cursor(new_offset)

    if not fresh:
        log_event("post-generation-recall", "noop",
                  meta={"reason": "no_fresh_entries", "total_undelivered": len(entries)})
        return 0

    latest = fresh[-1]
    rendered = latest.get("rendered", "")
    if not rendered.strip():
        return 0

    log_event("post-generation-recall", "fire",
              matches=[m.get("path") for m in latest.get("top_matches", [])],
              meta={"entries_seen": len(entries), "fresh_count": len(fresh)})

    out = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": rendered,
        }
    }
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
