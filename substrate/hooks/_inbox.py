"""
Inbox: the inbound half of the two-way protocol (Will 2026-11-01).
=================================================================

Will: "what if it was a 2 way protocol where my messages go through jarvis' own gates and hooks
for me before hitting the llm? ... it can only think or read at any time, not both. so i figured
we optimize that pending time."

Measured the same day: the prompt hooks run the moment he sends (0.2 to 0.8 s), then the message
waits in the queue until the model's next tool boundary (4 min 13 s for one message, 10 s for
another). This module is shared by three hooks that use that wait:

  inbox-capture.py  (UserPromptSubmit) secret gate for him, durable record, start the prep worker
  inbox-prep.py     (background)       deterministic prep: kind, references, what memory holds
  inbox-deliver.py  (PostToolUse)      hand finished prep to the model at the next tool boundary

Everything here fails open except the secret gate, which blocks on purpose.
"""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
INBOX = HOME / ".claude" / "state" / "inbox"
MSG_DIR = INBOX / "msgs"      # one JSON per captured message (input to the prep worker)
PREP_DIR = INBOX / "prep"     # finished prep waiting for delivery: <id>.md + <id>.json
DONE_DIR = PREP_DIR / "done"  # delivered or expired prep, kept as a record
LOG = INBOX / "inbox.jsonl"   # append-only: captured / blocked / prepped / delivered / expired

MEMORY_DIR = HOME / ".claude" / "projects" / "C--Users-Will" / "memory"

# Prep older than this is not delivered: it belonged to a turn that already passed.
DELIVER_MAX_AGE_S = 20 * 60

# ============ Secret gate (Constitution 2.4) ============
# High precision only: a false positive erases one of Will's messages, so each pattern is a
# provider's documented key shape, not a guess at "anything long and random".
SECRET_PATTERNS = [
    ("Anthropic API key", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}")),
    ("OpenRouter API key", re.compile(r"\bsk-or-v1-[A-Fa-f0-9]{48,}")),
    ("OpenAI API key", re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_\-]{40,}")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{60,})")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}(?![0-9A-Za-z_\-])")),
    ("Groq API key", re.compile(r"\bgsk_[A-Za-z0-9]{40,}")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9\-]{10,}")),
    ("Telegram bot token", re.compile(r"\b\d{8,10}:AA[A-Za-z0-9_\-]{33}(?![A-Za-z0-9_\-])")),
    ("Stripe secret key", re.compile(r"\b(?:sk|rk)_live_[A-Za-z0-9]{24,}")),
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY")),
]

# Will can still send one on purpose (a revoked key he is showing, say).
ALLOW_SECRET = "#allow-secret"


def find_secret(text):
    """Name of the first key shape found in text, or None."""
    for name, rx in SECRET_PATTERNS:
        if rx.search(text or ""):
            return name
    return None


def redact_secrets(text):
    out = text or ""
    for name, rx in SECRET_PATTERNS:
        out = rx.sub(f"[redacted {name}]", out)
    return out


# ============ Shared helpers ============

def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def msg_id(session, ts, prompt):
    return hashlib.sha1(f"{session}|{ts}|{prompt[:500]}".encode("utf-8", "replace")).hexdigest()[:12]


def log(event):
    try:
        INBOX.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps({"ts": now_iso(), **event}, ensure_ascii=False) + "\n")
    except Exception:
        pass


def is_machine_prompt(prompt):
    """Prompts the harness or a cron wrote, not Will: slash commands, task notifications, hook feedback."""
    p = (prompt or "").lstrip()
    return (not p) or p.startswith("<") or p.startswith("Stop hook feedback") or p.startswith("[CRON")
