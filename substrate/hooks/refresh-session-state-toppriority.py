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
    info = {"ctx": "?", "session": "?", "cwd": "?", "directive": "(none captured)"}
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
    return info


def build_block(info):
    ts = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    return (
        f"{START}\n"
        f"## ⚠ NEXT SESSION — TOP PRIORITY (auto-refreshed {ts})\n\n"
        f"> Machine-written every Stop from the mechanical handoff — never stale. "
        f"The curated block below is the quality layer; this is the floor.\n\n"
        f"- context at last stop: {info['ctx']}\n"
        f"- session: {info['session']}  ·  cwd: {info['cwd']}\n"
        f"- latest directive: {info['directive']}\n"
        f"- rich handoff: `~/Desktop/SESSION-HANDOFF-*.md` + "
        f"`memory/project_session-*.md`  ·  mechanical floor: "
        f"`~/.claude/hooks/.ctx-handoff/LATEST.md`\n\n"
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
