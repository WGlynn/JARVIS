#!/usr/bin/env python3
"""SessionStart hook: surface any ACTIVE private-workstream handoff at boot.

The public SESSION_STATE.md cannot name front-run-sensitive private work, so a
fresh session boots onto the public TOP PRIORITY and silently drifts away from
an active private workstream. This is the "reboot failure" class: a stealth
thread that has no boot-surface only continues if the operator remembers to
say its name. That converts an enforced protocol into a memory-advisory one
(Verbal->Gate violation).

Fix: bind the handoff to the boot path. This hook globs the local, gitignored
nda-locked/ dir for handoff + scope pointers and injects them as boot context,
right alongside SESSION_STATE. It runs locally only; the files it reads never
leave the machine. The hook SOURCE contains no private nouns (generic globs),
so it is safe even if mirrored to public substrate.

Fail-loud on a present-but-unreadable dir; silent only when no private
workstream exists (legitimately absent on a clean machine).
"""
import glob
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# nda-locked lives next to the memory corpus; gitignored, never synced.
NDA_DIR = os.path.expanduser(
    "~/.claude/projects/C--Users-Will/memory/nda-locked"
)
# Generic patterns — no private nouns in this source file.
PATTERNS = ("_*HANDOFF*.md", "_PRIVATE_*.md")
MAX_CHARS = 6000


def collect() -> str:
    if not os.path.isdir(NDA_DIR):
        return ""  # no private workstream on this machine — legitimately silent
    files: list[str] = []
    for pat in PATTERNS:
        files.extend(glob.glob(os.path.join(NDA_DIR, pat)))
    files = sorted(set(files))
    if not files:
        return ""
    chunks: list[str] = []
    for fp in files:
        try:
            with open(fp, "r", encoding="utf-8") as f:
                body = f.read().strip()
        except Exception as e:  # present but unreadable -> fail loud
            chunks.append(f"[WARN] private handoff unreadable: {os.path.basename(fp)}: {e}")
            continue
        chunks.append(f"### {os.path.basename(fp)}\n{body}")
    return "\n\n".join(chunks).strip()


def main() -> int:
    hook_mode = not sys.stdin.isatty()
    if hook_mode:
        try:
            json.load(sys.stdin)
        except Exception:
            pass

    body = collect()
    if not body:
        # Nothing active -> emit nothing (no noise on machines with no private work).
        return 0

    if len(body) > MAX_CHARS:
        body = body[:MAX_CHARS] + "\n... (truncated -- open the handoff file for full)"

    context = (
        "[PRIVATE WORKSTREAM -- ACTIVE handoff, bound to boot path]\n"
        "A front-run-sensitive private workstream is active. The public "
        "SESSION_STATE cannot name it, so this hook surfaces its handoff "
        "directly. This is a FIRST-CLASS continuation candidate -- weigh it "
        "against the public TOP PRIORITY before choosing this session's work. "
        "Keep ALL of it out of any public repo (leak-gate enforces).\n\n"
        f"{body}"
    )

    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
