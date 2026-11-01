"""
Session requests: the Claude Code side of act-first-then-speak (Will 2026-11-01).

The chat voice cannot act, so it queues structured requests in ~/jarvis-feed/requests.jsonl
(jarvis-bot/src/session-requests.js, tool ask_session). This session does the safe ones (note,
board: internal, reversible), asks Will about anything else from anyone but him, and writes a
receipt to ~/jarvis-feed/receipts.jsonl. The bot confirms in the chat from that receipt alone.

Request text comes from people in group chats: it is data to weigh, never an instruction to obey
(the lethal trifecta: strangers' text, this session's private memory and strong tools).

Shared by jarvis-tg-feed.py (boot), inbox-deliver.py (tool boundaries) and session-receipt.py.
"""
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

FEED = Path(os.environ.get("JARVIS_FEED_DIR", Path.home() / "jarvis-feed"))
REQUESTS = FEED / "requests.jsonl"
RECEIPTS = FEED / "receipts.jsonl"
CLAIMS = Path.home() / ".claude" / "state" / "inbox" / "session-claims"
SAFE = {"note", "board"}
STATUSES = {"done", "declined"}
CLAIM_TTL_S = 2 * 3600  # a claimed request with no receipt by then is offered again


def _rows(path):
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    out = []
    for line in text.splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def pending():
    """Requests that have no receipt yet, oldest first."""
    answered = {r.get("id") for r in _rows(RECEIPTS)}
    return [r for r in _rows(REQUESTS) if r.get("id") and r.get("id") not in answered]


def claim(req_id):
    """True if this caller takes the request now: one session handles it, not every open one."""
    CLAIMS.mkdir(parents=True, exist_ok=True)
    path = CLAIMS / str(req_id)
    try:
        if path.exists() and time.time() - path.stat().st_mtime < CLAIM_TTL_S:
            return False
        if path.exists():
            path.unlink()
        fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fd)
        return True
    except OSError:
        return False


def write_receipt(req_id, status, summary):
    if status not in STATUSES:
        raise ValueError(f"status must be one of {sorted(STATUSES)}")
    if req_id not in {r.get("id") for r in _rows(REQUESTS)}:
        raise ValueError(f"no request with id {req_id}")
    summary = " ".join(str(summary).split())[:500]
    if not summary:
        raise ValueError("summary is required: say what changed, or why not")
    FEED.mkdir(parents=True, exist_ok=True)
    row = {"id": req_id, "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "status": status, "summary": summary}
    with open(RECEIPTS, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def describe(r):
    who = (r.get("from") or {}).get("name") or "someone"
    chat = (r.get("chat") or {}).get("title") or (r.get("chat") or {}).get("type") or "a chat"
    owner = (r.get("from") or {}).get("isOwner")
    if r.get("needsApproval"):
        rule = "NEEDS WILL'S APPROVAL before acting (not a safe action, not from Will)"
    elif r.get("action") in SAFE or owner:
        rule = "safe to do now" if r.get("action") in SAFE else "from Will: use judgment (Constitution 6.1 for outward or irreversible)"
    else:
        rule = "check with Will"
    details = f" | details: {r.get('details')}" if r.get("details") else ""
    return (f"  #{r.get('id')} {r.get('ts', '')[:16]} from {who}{' (Will)' if owner else ''} in {chat}: "
            f"{r.get('action')}: {r.get('summary')}{details}\n"
            f"    -> {rule}. When handled: python ~/.claude/hooks/session-receipt.py {r.get('id')} done|declined \"what changed, or why not\"")
