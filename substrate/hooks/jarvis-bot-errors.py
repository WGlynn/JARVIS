#!/usr/bin/env python3
"""Jarvis TG bot -> Claude Code error feed reader.

The bot appends one JSON line per user-facing failure to ~/jarvis-feed/health.jsonl
(kind=reply_error; never message text). This prints the lines that arrived since the last
read and advances a cursor, so a cron fire or a SessionStart hook can hand them to Claude
Code for debugging while Will is AFK (Will 2026-10-28).

Usage:
  python jarvis-bot-errors.py            # print new reply_error lines, advance the cursor
  python jarvis-bot-errors.py --peek     # print without advancing
  python jarvis-bot-errors.py --reset    # forget the cursor
Exit code: 0 = nothing new, 3 = new errors printed (so a cron can branch on it).
"""
import json
import os
import sys

FEED = os.path.join(os.path.expanduser("~"), "jarvis-feed", "health.jsonl")
CURSOR = os.path.join(os.path.expanduser("~"), ".claude", "session-chain", ".jarvis-bot-errors.cursor")
KINDS = {"reply_error", "unclean_shutdown", "polling_restart_failed", "keeper_restart", "keeper_restart_failed"}


def main() -> int:
    args = set(sys.argv[1:])
    if "--reset" in args:
        if os.path.exists(CURSOR):
            os.remove(CURSOR)
        print("cursor reset")
        return 0
    if not os.path.exists(FEED):
        print("[jarvis-bot-errors] no feed file yet:", FEED)
        return 0
    start = 0
    if os.path.exists(CURSOR):
        try:
            start = int(open(CURSOR, encoding="utf-8").read().strip() or 0)
        except ValueError:
            start = 0
    size = os.path.getsize(FEED)
    if size < start:  # rotated or truncated
        start = 0
    new = []
    with open(FEED, "rb") as fh:
        fh.seek(start)
        for raw in fh:
            try:
                row = json.loads(raw.decode("utf-8", "replace"))
            except json.JSONDecodeError:
                continue
            if row.get("kind") in KINDS:
                new.append(row)
        end = fh.tell()
    if "--peek" not in args:
        with open(CURSOR, "w", encoding="utf-8") as fh:
            fh.write(str(end))
    if not new:
        print("[jarvis-bot-errors] no new bot errors")
        return 0
    print(f"[jarvis-bot-errors] {len(new)} new bot error(s) since last read (feed: {FEED})")
    for row in new[-20:]:
        print(f"  {row.get('ts', '?')}  {row.get('kind')}  {row.get('where', '')}  "
              f"{row.get('chatType', '')}  {str(row.get('error', ''))[:200]}")
        if row.get("stack"):
            print(f"      {str(row['stack'])[:240]}")
    print("  logs: ~/jarvis-bot-logs/bot.err.log, bot.log; meter: ~/jarvis-bot-logs/llm-calls.jsonl; "
          "code: ~/vibeswap/jarvis-bot/src; restart: scripts/restart-local.ps1 (test-gated)")
    return 3


if __name__ == "__main__":
    sys.exit(main())
