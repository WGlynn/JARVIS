#!/usr/bin/env python3
"""SessionStart hook: HANDOFF-FIRST.

Will's directive (2026-08-12): "an auto fire for read handoff, nothing should
ever come before it in a window ... more than a session start because windows
and sessions are different -- i could clear the window and still be in the same
session."

Windows != sessions. The window boundaries are ALL four SessionStart sources:
  startup | resume | clear | compact
`clear` and `compact` are same-session, new-window events. SessionStart with an
empty matcher fires on all four, so this ONE hook -- pinned to index 0 of the
SessionStart array -- guarantees the handoff is the FIRST block of every window,
with nothing before it.

It reads the TRUE newest SESSION-HANDOFF-*.md by mtime (across both Desktop and
Desktop/Session-Handoffs), because the AUTO-HANDOFF block embedded in
SESSION_STATE.md can lag a revision behind the freshest handoff on disk.

Bounded head only (config HEAD_LINES) -- the top of a handoff is the priority
block by convention; the pointer lets the model open the full file on demand.
"""
import glob
import json
import os
import sys

HANDOFF_GLOBS = [
    os.path.expanduser("~/Desktop/SESSION-HANDOFF-*.md"),
    os.path.expanduser("~/Desktop/Session-Handoffs/SESSION-HANDOFF-*.md"),
]
MECH_FLOOR = os.path.expanduser("~/.claude/hooks/.ctx-handoff/LATEST.md")
HEAD_LINES = 90
MECH_HEAD_LINES = 40
# If the mechanical floor is newer than the newest rich handoff by more than
# this many minutes, the last window closed WITHOUT writing a rich handoff --
# so the rich file is stale and the floor is the true current state. Headline
# the floor instead of the laggy rich file. (Root-cause fix 2026-08-12: after a
# /clear of a session that wrote no SESSION-HANDOFF, the auto-fire was surfacing
# a days-old handoff as "THE current handoff for this window.")
FRESH_DELTA_MIN = 20


def newest_handoff():
    cands = []
    for g in HANDOFF_GLOBS:
        cands.extend(glob.glob(g))
    if not cands:
        return None
    # newest by mtime -- the true freshest, independent of SESSION_STATE lag
    return max(cands, key=lambda p: os.path.getmtime(p))


def read_head(path, n):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.read().splitlines()
    except Exception as e:
        return None, f"[WARN] handoff unreadable: {e}"
    body = "\n".join(lines[:n])
    truncated = len(lines) > n
    return body, truncated


def mtime_or_none(path):
    try:
        return os.path.getmtime(path)
    except Exception:
        return None


def mech_age_hours():
    try:
        import time  # noqa -- time module is fine; wall-clock via os.stat only
        mt = os.path.getmtime(MECH_FLOOR)
        return (time.time() - mt) / 3600.0
    except Exception:
        return None


def build():
    rich_path = newest_handoff()
    rich_mt = mtime_or_none(rich_path) if rich_path else None
    mech_mt = mtime_or_none(MECH_FLOOR)

    # Freshness reconciliation: if the mechanical floor is materially newer than
    # the newest rich handoff, the last window wrote no rich handoff -> the floor
    # is the true current state. Headline it; demote the rich file to "prior".
    mech_wins = (
        mech_mt is not None
        and (rich_mt is None or (mech_mt - rich_mt) > FRESH_DELTA_MIN * 60)
    )

    if mech_wins:
        mech_body, mech_trunc = read_head(MECH_FLOOR, MECH_HEAD_LINES)
        if mech_body is None:
            mech_body = "[WARN] mechanical floor unreadable"
            mech_trunc = False
        banner = (
            "================================================================\n"
            "  READ HANDOFF FIRST -- this is THE current handoff for this window\n"
            "  (auto-fired on every window boundary: startup|resume|clear|compact)\n"
            "  source: MECHANICAL FLOOR (last window wrote no rich handoff)\n"
            "================================================================\n"
        )
        out = f"{banner}\n{mech_body}"
        if mech_trunc:
            out += "\n\n... (head only -- open ~/.claude/hooks/.ctx-handoff/LATEST.md for the rest)"
        # Demoted pointer to the newest WRITTEN rich handoff, flagged stale.
        if rich_path and rich_mt is not None:
            stale_h = (mech_mt - rich_mt) / 3600.0
            out += (
                f"\n\n--- prior written rich handoff (STALE by ~{stale_h:.1f}h -- "
                f"may NOT reflect your last window) ---\n"
                f"  {os.path.basename(rich_path)}\n"
                f"  open it only if the mechanical floor above lacks the thread you want.\n"
            )
        return out

    # Normal path: the newest rich handoff is current (window wrote one).
    if not rich_path:
        return ""
    body, truncated = read_head(rich_path, HEAD_LINES)
    if body is None:
        return truncated  # the warn string
    name = os.path.basename(rich_path)
    tail = "\n\n... (head only -- open the full file for the rest)" if truncated else ""
    age = mech_age_hours()
    age_note = f" | mechanical floor age ~{age:.1f}h" if age is not None else ""
    banner = (
        "================================================================\n"
        "  READ HANDOFF FIRST -- this is THE current handoff for this window\n"
        "  (auto-fired on every window boundary: startup|resume|clear|compact)\n"
        f"  source: {name}{age_note}\n"
        "================================================================\n"
    )
    return f"{banner}\n{body}{tail}\n"


def main():
    hook_mode = not sys.stdin.isatty()
    source = None
    if hook_mode:
        try:
            payload = json.load(sys.stdin)
            source = payload.get("source")
        except Exception:
            pass

    ctx = build()
    if not ctx:
        return 0

    if source:
        ctx = f"[window boundary: SessionStart source={source}]\n" + ctx

    if hook_mode:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": ctx,
            }
        }))
    else:
        print(ctx)
    return 0


if __name__ == "__main__":
    sys.exit(main())
