#!/usr/bin/env python3
r"""
Proposal Scraper — Stop hook that persists option/alternative blocks from assistant
responses to PROPOSALS.md. Survives session crashes and API deaths.

Problem: When Claude proposes options (Option A/B/C, numbered alternatives) and the
session crashes before Will decides, the options exist only in the chat transcript.
LLMs are non-deterministic, so a rerun generates different options — the original
"lottery ticket" is lost.

Fix: After each assistant turn, inspect the last message for proposal-shaped content.
If found, append to PROPOSALS.md (project-scoped if cwd is under a project with
.claude/, else global).

Detection heuristics (ANY hit):
  - Markdown bold option headers:   **Option A**, **Option B**, ...
  - Cycle-style option IDs:         **C11-A**, **C11-D**, ...
  - Numbered proposal lists:        2+ lines matching `^\d\.\s+\*\*`
  - Prose-style option markers:     "Option A:", "Option B:", ...

Wired in settings.json as a Stop hook AFTER api-death-shield stop handler.
Non-blocking: errors log to scraper.log and return cleanly.
"""

import sys
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

CHAIN_DIR = Path(__file__).parent
SHIELD_DIR = CHAIN_DIR / "shield"
LOG_FILE = SHIELD_DIR / "proposal-scraper.log"

# Global fallback location if cwd has no .claude project folder
GLOBAL_PROPOSALS = Path("~/.claude/PROPOSALS.md")

# Strong signals — explicit option labels. Any hit → proposal.
STRONG_PROPOSAL_PATTERNS = [
    re.compile(r"\*\*Option [A-Z]\*\*"),
    re.compile(r"\*\*C\d+-[A-Z]\*\*"),
    re.compile(r"\bOption [A-Z]:"),
]

# Weak signal — numbered bold list. Must combine with proximity keyword.
# (A summary or completion report uses numbered bold lists too — structure alone is insufficient.)
NUMBERED_PATTERN = re.compile(r"^\s*\d\.\s+\*\*[^*]+\*\*", re.MULTILINE)

# Proximity keywords that, when present, disambiguate "decision slate" from
# "structured summary" for the weak numbered-list signal.
PROPOSAL_KEYWORDS = re.compile(
    r"\b(?:options?|propos(?:e|ed|al|als)|alternatives?|pick\s+(?:one|from)|"
    r"which\s+(?:of|one|do\s+you)|choose\s+(?:one|from|between)|"
    r"approve\s*/?\s*adjust|which\s+one)\b",
    re.I,
)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def log(msg):
    try:
        SHIELD_DIR.mkdir(exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{now_iso()}] {msg}\n")
    except Exception:
        pass


def read_stdin():
    try:
        raw = sys.stdin.read()
        if raw.strip():
            return json.loads(raw)
    except Exception:
        pass
    return {}


def find_transcript_path(ctx):
    """Locate the JSONL transcript for the current session."""
    # Claude Code Stop hook passes transcript_path in ctx
    tp = ctx.get("transcript_path") or ctx.get("transcriptPath")
    if tp and Path(tp).exists():
        return Path(tp)

    # Fallback: construct from session_id + cwd slug
    sid = ctx.get("session_id") or ctx.get("sessionId")
    if sid:
        cwd = Path(ctx.get("cwd") or os.getcwd())
        slug = str(cwd).replace(":", "").replace("\\", "-").replace("/", "-").lstrip("-")
        candidate = Path(f"~/.claude/projects/{slug}/{sid}.jsonl")
        if candidate.exists():
            return candidate

    return None


def extract_last_assistant_text(transcript_path):
    """Read the JSONL, return the most recent assistant message text."""
    try:
        last_text = None
        with open(transcript_path, encoding="utf-8") as f:
            for line in f:
                try:
                    row = json.loads(line)
                except Exception:
                    continue
                msg = row.get("message", {})
                if msg.get("role") != "assistant":
                    continue
                content = msg.get("content")
                if isinstance(content, list):
                    chunks = [c.get("text", "") for c in content if c.get("type") == "text"]
                    joined = "\n".join(c for c in chunks if c)
                    if joined.strip():
                        last_text = joined
                elif isinstance(content, str) and content.strip():
                    last_text = content
        return last_text
    except Exception as e:
        log(f"Transcript read error: {e}")
        return None


CODE_SPAN_PATTERN = re.compile(r"```.*?```|`[^`\n]+`", re.DOTALL)


def _strip_code_spans(text):
    """Remove fenced and inline code spans so documentation examples don't self-trigger."""
    return CODE_SPAN_PATTERN.sub(" ", text)


def looks_like_proposal(text):
    """
    Detect whether `text` contains a decision-slate proposal block.

    Strong signal: any explicit option label (Option A/B/C, cycle IDs like C11-A)
                   appearing OUTSIDE code spans.
    Weak signal:   >=2 numbered bold items AND a proximity keyword, both outside code spans.

    False-positive guards (added 2026-04-15 after successive scraper self-triggers):
      - Bare numbered bold lists without keyword are rejected.
      - Matches inside backtick code spans are ignored (documentation of trigger
        patterns should not fire the trigger).
    """
    if not text:
        return False
    stripped = _strip_code_spans(text)
    for p in STRONG_PROPOSAL_PATTERNS:
        if p.search(stripped):
            return True
    if len(NUMBERED_PATTERN.findall(stripped)) >= 2 and PROPOSAL_KEYWORDS.search(stripped):
        return True
    return False


def choose_proposals_file(ctx):
    """Prefer project-local PROPOSALS.md; fall back to global."""
    cwd = Path(ctx.get("cwd") or os.getcwd())
    # Walk up looking for .claude/
    for candidate in [cwd] + list(cwd.parents):
        if (candidate / ".claude").is_dir():
            return candidate / ".claude" / "PROPOSALS.md"
    return GLOBAL_PROPOSALS


def ensure_header(path):
    if path.exists() and path.stat().st_size > 0:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# Proposals Ledger\n\n"
        "Canonical store for options/alternatives proposed for decision. "
        "Survives session crashes.\n"
        "Auto-appended by `~/.claude/session-chain/proposal-scraper.py`.\n\n---\n",
        encoding="utf-8",
    )


def already_persisted(path, text, sid):
    """Dedupe: skip if the same first-line + session_id already exists."""
    if not path.exists():
        return False
    try:
        existing = path.read_text(encoding="utf-8")
        first_line = text.strip().split("\n", 1)[0][:100]
        return (sid in existing) and (first_line in existing)
    except Exception:
        return False


def append_proposal(path, text, ctx):
    sid = ctx.get("session_id") or ctx.get("sessionId") or "unknown"
    ts = now_iso()
    # Try to derive a topic from the first header or first sentence
    topic_match = re.search(r"^#+\s+(.+)$|^\*\*([^*]+)\*\*", text, re.MULTILINE)
    topic = (topic_match.group(1) or topic_match.group(2) or "Proposal") if topic_match else "Proposal"
    topic = topic.strip()[:80]

    if already_persisted(path, text, sid):
        log(f"Skip (already persisted): {topic}")
        return

    ensure_header(path)
    entry = (
        f"\n## {topic} — {ts}\n"
        f"**Session**: `{sid}`\n"
        f"**Status**: proposed\n\n"
        f"{text.strip()}\n\n---\n"
    )
    with open(path, "a", encoding="utf-8") as f:
        f.write(entry)
    log(f"Appended proposal to {path}: {topic}")


def main():
    ctx = read_stdin()
    transcript = find_transcript_path(ctx)
    if not transcript:
        return

    text = extract_last_assistant_text(transcript)
    if not looks_like_proposal(text):
        return

    path = choose_proposals_file(ctx)
    try:
        append_proposal(path, text, ctx)
    except Exception as e:
        log(f"Append error: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"FATAL: {type(e).__name__}: {e}")
