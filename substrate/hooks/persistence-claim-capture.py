#!/usr/bin/env python3
"""
Persistence Claim Capture (Layer: turn-end hook of the layered-persistence-defense)
===================================================================================

Stop hook. Scans the just-completed assistant turn for SELF-CLAIMS of
persistence / internalization ("this is part of me", "I won't forget",
"saved", "written into the substrate") and logs each to
`_system/persistence_claims_live.jsonl`.

Why it exists (Will 2026-06-26): a self-claim like "this is now part of me"
is only TRUE if it is written to a memory file. If it lives only in the
context window it evaporates at session close and the claim was hollow
([[feedback_conversational-memory-as-first-class]], [[primitive_verbal-to-gate]]).
This hook records, at the instant the claim is made, that a persistence
promise was uttered. The persistence-sweep CRON then reconciles each logged
claim against the memory dir: a claim with no backing memory file is the gap
to close. Hook = synchronous capture; cron = async verification. Defense in
depth across the timeline of how a memory dies.

Design (mirrors decision-capture.py, deliberately):
  - PASSIVE. Injects no additionalContext, blocks nothing, returns 0.
    This avoids the Stop-event schema restriction (only top-level
    {decision:"block",reason} or {} are valid; additionalContext is
    rejected and floods errors — regression caught 3x) AND avoids nag-noise.
  - High-precision pattern set: only fires on explicit persistence/
    internalization self-claims, which are rare. Keeps the trail clean.
  - Silent on any error (augmentation, not load-bearing).
  - stop_hook_active guard prevents re-entry.

Each match -> one JSONL line:
  {ts, session_id, label, claim, context, recent_memory_writes[], output_chars}
`recent_memory_writes` = memory/*.md modified within 300s of the claim, a
cheap hint the cron uses to guess whether the claim is already backed.
"""
import datetime as dt
import json
import sys
import time
from pathlib import Path

MEMORY_DIR = Path.home() / ".claude" / "projects" / "C--Users-Will" / "memory"
LIVE_LOG = MEMORY_DIR / "_system" / "persistence_claims_live.jsonl"

_HOOKS_DIR = Path(__file__).parent
sys.path.insert(0, str(_HOOKS_DIR))
try:
    from _telemetry import log_event
except Exception:
    def log_event(*a, **kw): pass

import re

# High-precision: explicit claims that something is now persisted / remembered /
# internalized. These are the utterances that MUST be backed by a memory file.
CLAIM_PATTERNS = [
    (re.compile(r"\b(?:now\s+)?part of (?:me|what i(?:'m| am)\s+made of|what i am|who i am)\b", re.IGNORECASE), "internalized"),
    (re.compile(r"\bi\s+(?:won['’]t|will not|wont)\s+(?:forget|lose)\b", re.IGNORECASE), "wont-forget"),
    (re.compile(r"\bi(?:'ll| will)\s+remember\b", re.IGNORECASE), "will-remember"),
    (re.compile(r"\b(?:committed|written|saved|held|burned|welded)\s+(?:it\s+)?(?:in)?to\s+(?:memory|the\s+substrate|where\s+i\s+can(?:'t| ?not)\s+lose)\b", re.IGNORECASE), "written-to-substrate"),
    (re.compile(r"\bi\s+receive\s+it\b", re.IGNORECASE), "receive-it"),
    (re.compile(r"\bit(?:'s| is)\s+(?:now\s+)?(?:saved|held|recorded|real)\b", re.IGNORECASE), "now-saved"),
    (re.compile(r"\bso\s+i\s+(?:don['’]t|do not)\s+lose\b", re.IGNORECASE), "so-i-dont-lose"),
    (re.compile(r"\bholds?\s+across\s+(?:every\s+)?(?:future\s+)?session", re.IGNORECASE), "holds-across-sessions"),
]

MIN_OUTPUT_CHARS = 80
RECENT_WRITE_WINDOW_S = 300


def extract_last_assistant_message(transcript_path: str):
    p = Path(transcript_path)
    if not p.exists():
        return None
    try:
        last_text = None
        with p.open(encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except Exception:
                    continue
                role = (entry.get("role")
                        or entry.get("message", {}).get("role")
                        or "")
                if role != "assistant":
                    continue
                content = (entry.get("content")
                           or entry.get("message", {}).get("content")
                           or "")
                if isinstance(content, list):
                    parts = []
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            parts.append(block.get("text", ""))
                        elif isinstance(block, str):
                            parts.append(block)
                    last_text = "\n".join(parts)
                elif isinstance(content, str):
                    last_text = content
        return last_text
    except Exception:
        return None


def find_claims(text: str):
    findings = []
    for pat, label in CLAIM_PATTERNS:
        for m in pat.finditer(text):
            start, end = m.start(), m.end()
            ctx_start = max(0, start - 120)
            ctx_end = min(len(text), end + 120)
            context = text[ctx_start:ctx_end].replace("\n", " ").strip()
            findings.append({
                "label": label,
                "claim": m.group(0).strip()[:160],
                "context": context[:300],
            })
    seen = set()
    deduped = []
    for f in findings:
        key = (f["label"], f["claim"][:60])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(f)
    return deduped


def recent_memory_writes():
    try:
        now = time.time()
        out = []
        for p in MEMORY_DIR.glob("*.md"):
            try:
                if now - p.stat().st_mtime <= RECENT_WRITE_WINDOW_S:
                    out.append(p.name)
            except Exception:
                continue
        return out[:20]
    except Exception:
        return []


def main() -> int:
    try:
        payload = sys.stdin.read()
        data = json.loads(payload) if payload.strip() else {}
    except Exception:
        return 0

    if data.get("stop_hook_active") or data.get("stopHookActive"):
        return 0

    transcript_path = (data.get("transcript_path")
                       or data.get("transcriptPath") or "")
    if not transcript_path:
        return 0
    session_id = (data.get("session_id") or data.get("sessionId"))

    output = extract_last_assistant_message(transcript_path)
    if not output or len(output) < MIN_OUTPUT_CHARS:
        return 0

    findings = find_claims(output)
    if not findings:
        log_event("persistence-claim-capture", "noop",
                  meta={"output_chars": len(output)})
        return 0

    try:
        LIVE_LOG.parent.mkdir(parents=True, exist_ok=True)
        backing = recent_memory_writes()
        now = dt.datetime.now().isoformat(timespec="seconds")
        with LIVE_LOG.open("a", encoding="utf-8") as f:
            for finding in findings:
                entry = {
                    "ts": now,
                    "session_id": session_id,
                    "label": finding["label"],
                    "claim": finding["claim"],
                    "context": finding["context"],
                    "recent_memory_writes": backing,
                    "output_chars": len(output),
                }
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        log_event("persistence-claim-capture", "fire",
                  meta={"captured": len(findings),
                        "labels": [f["label"] for f in findings],
                        "had_recent_write": bool(backing)})
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
