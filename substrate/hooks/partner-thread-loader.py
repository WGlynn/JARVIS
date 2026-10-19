#!/usr/bin/env python3
"""
partner-thread-loader.py

UserPromptSubmit hook. When the prompt names a person who has a conversation record in
Desktop/People/<Name>/ (THREAD.md and/or STATE.md), inject STATE.md plus the tail of THREAD.md, so
a reply drafted after a /clear still has the whole conversation behind it. First mention per
session gets the full record; later mentions get a one-line logging reminder.

Source primitive: memory/primitive_per-person-conversation-record.md (Will 2026-10-19: "let's do it
for ALL conversations going forward"). Aliases: an "aliases:" line in STATE.md (comma-separated),
plus the folder name. Fails loud if a record folder has THREAD.md but no STATE.md.
"""
import json
import os
import re
import sys

PEOPLE = os.path.join(os.path.expanduser("~"), "Desktop", "People")
SEEN_DIR = os.path.join(os.path.expanduser("~"), ".claude", "hooks", ".partner-thread")
TAIL_CHARS = 6000

RULES = (
    "Rules: (1) read STATE.md before drafting; do not contradict a concession or re-argue a settled point. "
    "(2) Log their new message VERBATIM in THREAD.md now, before drafting. (3) Save the draft in this "
    "folder (this overrides the Desktop-root path in the formalize gate). (4) Once Will sends, log the SENT "
    "text (ask if he edited) and update STATE.md: claims, concessions, corrections, promises, open questions."
)


def records():
    out = []
    if not os.path.isdir(PEOPLE):
        return out
    for name in sorted(os.listdir(PEOPLE)):
        d = os.path.join(PEOPLE, name)
        thread, state = os.path.join(d, "THREAD.md"), os.path.join(d, "STATE.md")
        if not (os.path.isfile(thread) or os.path.isfile(state)):
            continue
        aliases = {name.lower()}
        if os.path.isfile(state):
            for line in open(state, encoding="utf-8", errors="replace").read().splitlines()[:15]:
                if line.lower().startswith("aliases:"):
                    aliases |= {a.strip().lower() for a in line.split(":", 1)[1].split(",") if a.strip()}
        out.append((name, d, thread, state, aliases))
    return out


PATH_RE = re.compile(r"(?:/c/|[A-Za-z]:[\\/]|~/)[^\n'\"]*?\.(?:md|txt)", re.I)


def pasted_files(prompt):
    """Files the prompt points at (Git Bash /c/..., C:\\..., ~/...), with their lowercased text."""
    out = []
    for m in PATH_RE.findall(prompt):
        p = m.strip()
        if p.startswith("/c/"):
            p = "C:/" + p[3:]
        elif p.startswith("~/"):
            p = os.path.join(os.path.expanduser("~"), p[2:])
        p = os.path.normpath(p)
        if os.path.isfile(p) and os.path.getsize(p) < 1_000_000:
            out.append((p, open(p, encoding="utf-8", errors="replace").read().lower()))
    return out


def copy_in(src, person_dir):
    """Copy a pasted file into <person>/inbox/ (no overwrite; skip if it already lives in the record)."""
    if os.path.normcase(os.path.abspath(src)).startswith(os.path.normcase(os.path.abspath(person_dir))):
        return None
    inbox = os.path.join(person_dir, "inbox")
    os.makedirs(inbox, exist_ok=True)
    base = os.path.basename(src)
    dst = os.path.join(inbox, base)
    data = open(src, "rb").read()
    n = 2
    while os.path.exists(dst):
        if open(dst, "rb").read() == data:
            return None
        stem, ext = os.path.splitext(base)
        dst = os.path.join(inbox, f"{stem}-{n}{ext}")
        n += 1
    open(dst, "wb").write(data)
    return f"{src} -> {dst}"


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        print(json.dumps({}))
        return
    if payload.get("hook_event_name", "") != "UserPromptSubmit":
        print(json.dumps({}))
        return
    low = (payload.get("prompt", "") or "").lower()
    session = re.sub(r"[^A-Za-z0-9_-]", "", str(payload.get("session_id", "nosession")))[:64]
    os.makedirs(SEEN_DIR, exist_ok=True)
    seen_path = os.path.join(SEEN_DIR, f"{session}.json")
    seen = set(json.load(open(seen_path))) if os.path.isfile(seen_path) else set()

    pasted = pasted_files(payload.get("prompt", "") or "")
    parts = []
    for name, d, thread, state, aliases in records():
        hit = lambda text: any(re.search(r"(?<![a-z0-9])" + re.escape(a) + r"(?![a-z0-9])", text) for a in aliases)
        mine = [(p, txt) for p, txt in pasted if hit(txt) or hit(os.path.basename(p).lower())]
        if not (hit(low) or mine):
            continue
        copied = [c for c in (copy_in(p, d) for p, _ in (mine or pasted)) if c]
        if copied:
            parts.append(f"[PARTNER RECORD: {name}] copied into the record so it survives context windows: "
                         + "; ".join(copied))
        if name in seen:
            parts.append(f"[PARTNER RECORD: {name}] already loaded this session ({d}). {RULES}")
            continue
        seen.add(name)
        block = [f"[PARTNER RECORD: {name}] Conversation record at {d}. {RULES}"]
        if os.path.isfile(state):
            block.append("--- STATE.md ---\n" + open(state, encoding="utf-8", errors="replace").read().strip())
        else:
            block.append(f"!! {name} has THREAD.md but NO STATE.md. Write STATE.md before drafting.")
        if os.path.isfile(thread):
            t = open(thread, encoding="utf-8", errors="replace").read()
            cut = t.find("\n## Older threads")
            t = t[:cut] if cut > 0 else t
            block.append(f"--- THREAD.md (last {TAIL_CHARS} chars; full file on disk) ---\n" + t[-TAIL_CHARS:].strip())
        parts.append("\n".join(block))

    json.dump(sorted(seen), open(seen_path, "w"))
    if not parts:
        print(json.dumps({}))
        return
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                             "additionalContext": "\n\n".join(parts)}}))


if __name__ == "__main__":
    main()
