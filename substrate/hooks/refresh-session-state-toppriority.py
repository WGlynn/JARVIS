#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Refresh SESSION_STATE TOP PRIORITY from the mechanical handoff — on every Stop.

The problem this kills: SESSION_STATE.md's "NEXT SESSION -- TOP PRIORITY" block is
what the boot-directive check reads, but it was only ever updated as a MANUAL model
step. So it rotted while the deterministic handoff (~/.claude/hooks/.ctx-handoff/
LATEST.md) stayed current. The handoff IS the session state; the boot directive was
reading a stale hand-maintained copy of it.

Fix (Stop hook, deterministic, no model memory): own a sentinel-bounded auto-block
at the TOP of SESSION_STATE.md and rewrite it every Stop from LATEST.md. The boot
reader finds this fresh block first; any curated rich block below is preserved as the
quality layer. Idempotent: the sentinels bound exactly what this hook overwrites.

Per [P.always-equals-gate] + [P.universal-coverage-hook]: "the directive must always
be current" = a hook, not a habit. Stop-hook emit stays schema-safe ({} only) per
[P.stop-event-schema-restriction]. Fail-safe: never block Stop; on any error, exit 0.
"""
import datetime
import json
import os
import re
import sys

SESSION_STATE = os.path.expanduser("~/vibeswap/.claude/SESSION_STATE.md")
LATEST = os.path.expanduser("~/.claude/hooks/.ctx-handoff/LATEST.md")
START = "<!-- AUTO-HANDOFF:START -->"
END = "<!-- AUTO-HANDOFF:END -->"


def parse_latest():
    info = {"ctx": "?", "session": "?", "cwd": "?", "directive": "(none captured)",
            "recent_turns": "", "mtime": None}
    try:
        info["mtime"] = os.path.getmtime(LATEST)
    except Exception:
        pass
    try:
        text = open(LATEST, encoding="utf-8").read()
    except Exception:
        return info
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("- context:"):
            info["ctx"] = s.split(":", 1)[1].strip()
        elif s.startswith("- session:"):
            info["session"] = s.split(":", 1)[1].strip()
        elif s.startswith("- cwd:"):
            info["cwd"] = s.split(":", 1)[1].strip()
    m = re.search(r"## Recent user turns.*?\n\s*\d+\.\s*(.+)", text, re.S)
    if m:
        first = m.group(1).strip().splitlines()[0]
        info["directive"] = first[:200]
    # Capture the whole recent-turns block -- the fresh thread, so a stale rich
    # handoff below can be demoted without losing where the last window actually was.
    rt = re.search(r"(## Recent user turns.*)", text, re.S)
    if rt:
        block = rt.group(1).strip()
        info["recent_turns"] = block[:1600]
    return info


def latest_handoff():
    """Newest ~/Desktop/SESSION-HANDOFF-*.md -> (name, mtime_str, bounded_text), or None.

    Per [F.always-embed-handoff-in-session-state-top-priority] (Will 2026-06-30):
    the top-priority block must EMBED the rich handoff inline, not just point at it.
    """
    try:
        import glob
        desktop = os.path.expanduser("~/Desktop")
        files = glob.glob(os.path.join(desktop, "SESSION-HANDOFF-*.md"))
        if not files:
            return None
        newest = max(files, key=os.path.getmtime)
        raw_mt = os.path.getmtime(newest)
        mtime = datetime.datetime.fromtimestamp(raw_mt).strftime("%Y-%m-%d %H:%M")
        text = open(newest, encoding="utf-8").read().strip()
        if len(text) > 4000:
            text = text[:4000] + "\n\n…(truncated — full file on Desktop)"
        return (os.path.basename(newest), mtime, text, raw_mt)
    except Exception:
        return None


# If the mechanical floor is newer than the newest rich handoff by more than this
# many minutes, the last window wrote no rich handoff -> the embedded rich file is
# stale. Flag it and lead with the fresh mechanical recent-turns instead of lying
# "never stale." (Root-cause fix 2026-08-12, parallel to handoff-first.py.)
FRESH_DELTA_MIN = 20


def build_block(info):
    ts = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    rich = latest_handoff()
    if rich:
        name, mtime, text, rich_mt = rich
        mech_mt = info.get("mtime")
        stale = (mech_mt is not None and (mech_mt - rich_mt) > FRESH_DELTA_MIN * 60)
        if stale:
            stale_h = (mech_mt - rich_mt) / 3600.0
            fresh = ""
            if info.get("recent_turns"):
                fresh = (
                    f"\n**Fresh thread — last window (mechanical floor, {info['cwd']}):**\n\n"
                    f"{info['recent_turns']}\n"
                )
            embedded = (
                f"{fresh}\n"
                f"<details><summary>Prior written rich handoff `{name}` (saved {mtime}, "
                f"STALE by ~{stale_h:.1f}h — may NOT reflect your last window)</summary>\n\n"
                f"{text}\n\n</details>\n"
            )
        else:
            embedded = f"\n**Embedded handoff** (newest `{name}`, saved {mtime}):\n\n{text}\n"
    else:
        embedded = (
            "\n- rich handoff: `~/Desktop/SESSION-HANDOFF-*.md` + "
            "`memory/project_session-*.md`\n"
        )
    return (
        f"{START}\n"
        f"## ⚠ NEXT SESSION — TOP PRIORITY (auto-refreshed {ts})\n\n"
        f"> Machine-written every Stop from the mechanical handoff + newest rich handoff. "
        f"Mechanical floor is never stale; the rich handoff is flagged if it lags the last window.\n\n"
        f"- context at last stop: {info['ctx']}\n"
        f"- session: {info['session']}  ·  cwd: {info['cwd']}\n"
        f"- latest directive: {info['directive']}\n"
        f"- mechanical floor: `~/.claude/hooks/.ctx-handoff/LATEST.md`\n"
        f"{embedded}\n"
        f"{END}"
    )


def main():
    try:
        sys.stdin.read()
    except Exception:
        pass
    try:
        if not os.path.exists(SESSION_STATE):
            print("{}")
            return 0
        doc = open(SESSION_STATE, encoding="utf-8").read()
        block = build_block(parse_latest())
        if START in doc and END in doc:
            doc = re.sub(re.escape(START) + r".*?" + re.escape(END),
                         lambda _m: block, doc, count=1, flags=re.S)
        else:
            lines = doc.splitlines(keepends=True)
            idx = 0
            for i, l in enumerate(lines):
                if l.startswith("# "):
                    idx = i + 1
                    break
            lines.insert(idx, "\n" + block + "\n")
            doc = "".join(lines)
        tmp = SESSION_STATE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(doc)
        os.replace(tmp, SESSION_STATE)
    except Exception:
        pass
    print("{}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
