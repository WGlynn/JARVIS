#!/usr/bin/env python3
"""
Write a receipt for a chat-voice request (act first, then speak; Will 2026-11-01).

  python ~/.claude/hooks/session-receipt.py <request id> done "Added Project X (launch 2026-12-12) to projects.md"
  python ~/.claude/hooks/session-receipt.py <request id> declined "Not public; kept out of the notes"

The bot sees the receipt within about 30 s and confirms in the chat the request came from, saying
only what the receipt says. Write it only after the work is really done (Constitution 1.2).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _session_requests as sr  # noqa: E402


def main():
    if len(sys.argv) != 4:
        print(__doc__.strip())
        return 2
    try:
        row = sr.write_receipt(sys.argv[1], sys.argv[2], sys.argv[3])
    except ValueError as e:
        print(f"receipt not written: {e}")
        return 1
    print(f"receipt written for #{row['id']} ({row['status']}); the bot confirms in the chat within ~30 s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
