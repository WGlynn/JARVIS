#!/usr/bin/env python3
"""
Inbox delivery: PostToolUse hook, the last step of the two-way protocol's inbound side (2026-11-01).

Queued messages reach the model at a tool boundary; so does this hook. It hands over any prep
inbox-prep.py finished for this session, then moves it to prep/done/ so it is delivered once.
Claiming is an atomic rename, so two hooks running at once never deliver the same prep twice.
Prep for a message sent more than 20 minutes ago is expired, not delivered.

Runs after every tool call, so the common case (nothing waiting) is one directory listing.
"""
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _inbox  # noqa: E402


def done(path):
    """Move path into prep/done/. False if another hook already took it."""
    try:
        _inbox.DONE_DIR.mkdir(parents=True, exist_ok=True)
        os.replace(path, _inbox.DONE_DIR / path.name)
        return True
    except OSError:
        return False


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    session = data.get("session_id") or ""
    try:
        metas = sorted(_inbox.PREP_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime)  # in the order sent
    except Exception:
        metas = []
    blocks = []
    now = time.time()
    for mp in metas:
        try:
            meta = json.loads(mp.read_text(encoding="utf-8"))
        except Exception:
            continue
        md = mp.with_suffix(".md")
        stale = now - float(meta.get("sent_epoch") or 0) > _inbox.DELIVER_MAX_AGE_S
        if meta.get("session") != session and not stale:
            continue  # another live session's message
        if not done(mp):
            continue
        if stale or meta.get("session") != session or not md.exists():
            done(md)
            _inbox.log({"event": "expired", "id": meta.get("id")})
            continue
        try:
            blocks.append(md.read_text(encoding="utf-8"))
        except Exception:
            pass
        done(md)
        _inbox.log({"event": "delivered", "id": meta.get("id"), "waited_s": round(now - float(meta.get("sent_epoch") or now), 1)})
    if not blocks:
        print("{}")
        return 0
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "\n\n".join(blocks)}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
