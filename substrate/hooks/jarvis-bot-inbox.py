#!/usr/bin/env python3
"""Jarvis TG bot -> Claude Code inbox reader (the second-brain loop, Will 2026-10-28).

The bot appends every exchange it handles to ~/jarvis-feed/YYYY-MM-DD.jsonl (who, which chat,
the inbound text, the bot's reply, message ids). This prints the exchanges that arrived since the
last read and advances a cursor, so the triage cron can act on a partner's reply (for example
someone answering the bot in a group chat) by posting a follow-up through POST /api/say.

Message text IS printed here, by Will's instruction (seamless bot <-> Claude Code). Keep it out of
public repos and partner records unless it belongs there.

Usage: python jarvis-bot-inbox.py [--peek] [--reset]
Exit: 0 = nothing new, 3 = new exchanges printed.
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows console is cp1252; feeds carry emoji

FEED_DIR = os.path.join(os.path.expanduser("~"), "jarvis-feed")
CURSOR = os.path.join(os.path.expanduser("~"), ".claude", "session-chain", ".jarvis-bot-inbox.cursor")


def load_cursor():
    try:
        return json.load(open(CURSOR, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def main() -> int:
    args = set(sys.argv[1:])
    if "--reset" in args:
        if os.path.exists(CURSOR):
            os.remove(CURSOR)
        print("cursor reset")
        return 0
    cur = load_cursor()
    new = []
    files = sorted(glob.glob(os.path.join(FEED_DIR, "20??-??-??.jsonl")))[-3:]  # last three days
    for f in files:
        start = int(cur.get(f, 0))
        size = os.path.getsize(f)
        if size < start:
            start = 0
        with open(f, "rb") as fh:
            fh.seek(start)
            for raw in fh:
                try:
                    row = json.loads(raw.decode("utf-8", "replace"))
                except json.JSONDecodeError:
                    continue
                new.append(row)
            cur[f] = fh.tell()
    if "--peek" not in args:
        with open(CURSOR, "w", encoding="utf-8") as fh:
            json.dump(cur, fh)
    if not new:
        print("[jarvis-bot-inbox] no new exchanges")
        return 0
    print(f"[jarvis-bot-inbox] {len(new)} new exchange(s) since last read")
    for r in new[-30:]:
        chat = r.get("chat") or {}
        frm = r.get("from") or {}
        who = frm.get("username") and f"@{frm['username']}" or frm.get("name") or frm.get("id")
        where = chat.get("title") or chat.get("type") or chat.get("id")
        tag = " [reply to the bot]" if r.get("repliedToBot") else ""
        print(f"\n  {r.get('ts', '?')}  {where} (chat {chat.get('id')})  from {who}  msg {r.get('messageId')}{tag}")
        print(f"    IN : {str(r.get('in', ''))[:1200]}")
        print(f"    OUT: {str(r.get('out', ''))[:600]}   [{r.get('provider')}/{r.get('model')}]")
    print("\n  follow up: POST http://127.0.0.1:8080/api/say {chatId, text, replyToMessageId} with header X-Api-Secret "
          "(value in ~/vibeswap/jarvis-bot/.env as CLAUDE_CODE_API_SECRET; never print it). No disclosure line.")
    return 3


if __name__ == "__main__":
    sys.exit(main())
