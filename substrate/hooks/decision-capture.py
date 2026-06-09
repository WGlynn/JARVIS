#!/usr/bin/env python3
"""
Live Decision Capture (L3 Judgment-Trail Tap)
=============================================

Stop hook. Scans the just-completed assistant turn for decision-shaped
language and appends matches to `_system/decisions_live.jsonl`.

Sibling of `_decision_extractor.py`:
  - Extractor: post-hoc, scans static memory files
  - Live capture (this hook): real-time, scans assistant output

Why both: most load-bearing decisions are MADE in conversation, not
written to memory. They evaporate at session close unless captured live.
The extractor catches the memory residue; this catches the decisions
themselves at the moment they're stated.

Each match becomes one JSONL line:
  {
    "ts": ISO-8601,
    "session_id": str | null,
    "label": "explicit-decision" | "verb-decided" | ...,
    "decision": str (the matched text or capture group),
    "context": str (~200 chars of surrounding text),
    "output_chars": int (full output length, for noise-filter calibration)
  }

Passive: this hook does NOT inject additionalContext. It writes silently.
Periodic review tools (decision_extractor, future judgment_review.py)
read the jsonl to surface decisions for grading.

Failsafe:
  - Silent on any error (decision capture is augmentation, not load-bearing)
  - stop_hook_active guard prevents re-entry
  - Pattern set kept tight (forward-looking commitments only) to avoid
    polluting the trail with descriptive narrative

Origin: 2026-05-13 autopilot. Closes the live-judgment gap left open by
the post-hoc decision extractor. Judgment trail now has both memory-side
and conversation-side capture surfaces.
"""
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

MEMORY_DIR = Path.home() / ".claude" / "projects" / "C--Users-Will" / "memory"
LIVE_LOG = MEMORY_DIR / "_system" / "decisions_live.jsonl"

# Telemetry
_HOOKS_DIR = Path(__file__).parent
sys.path.insert(0, str(_HOOKS_DIR))
try:
    from _telemetry import log_event
except Exception:
    def log_event(*a, **kw): pass


# Same pattern set as _decision_extractor (forward-looking commitments only)
DECISION_PATTERNS = [
    (re.compile(r"\*\*Decision\*\*:\s*(.+?)(?:\n|$)", re.IGNORECASE), "explicit-decision"),
    (re.compile(r"\*\*Pick\*\*:\s*(.+?)(?:\n|$)", re.IGNORECASE), "explicit-pick"),
    (re.compile(r"\*\*Chose\*\*:\s*(.+?)(?:\n|$)", re.IGNORECASE), "explicit-chose"),
    (re.compile(r"\*\*Verdict\*\*:\s*(.+?)(?:\n|$)", re.IGNORECASE), "explicit-verdict"),
    (re.compile(r"\*\*Selected\*\*:\s*(.+?)(?:\n|$)", re.IGNORECASE), "explicit-selected"),
    (re.compile(r"\*\*Resolution\*\*:\s*(.+?)(?:\n|$)", re.IGNORECASE), "explicit-resolution"),
    (re.compile(r"\*\*Approach\*\*:\s*(.+?)(?:\n|$)", re.IGNORECASE), "explicit-approach"),
    (re.compile(r"\*\*Recommendation\*\*:\s*(.+?)(?:\n|$)", re.IGNORECASE), "explicit-recommend"),
    (re.compile(r"^#{2,4}\s*Decision\b.*$", re.IGNORECASE | re.MULTILINE), "section-decision"),
    (re.compile(r"\b(?:we|i|we['’]ll|i['’]ll)\s+(?:decided|chose|picked|selected)\s+to\s+([^\.\n]{8,200})", re.IGNORECASE), "verb-decided"),
    (re.compile(r"\b(?:we|i)['’]?(?:ll|re)?\s+(?:going\s+with|moving\s+to|switching\s+to|sticking\s+with)\s+([^\.\n]{4,150})", re.IGNORECASE), "verb-commit"),
    (re.compile(r"\b(?:we|i)['’]?(?:ll|re)?\s+(?:not\s+going\s+to|won['’]t|will\s+not)\s+(?:use|integrate|adopt|pursue|build|do|ship)\s+([^\.\n]{4,150})", re.IGNORECASE), "neg-decision"),
]

MIN_OUTPUT_CHARS = 200


def extract_last_assistant_message(transcript_path: str) -> str | None:
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


def find_decisions(text: str) -> list[dict]:
    findings = []
    for pat, label in DECISION_PATTERNS:
        for m in pat.finditer(text):
            decision_text = m.group(0).strip()
            if m.groups():
                groups = [g for g in m.groups() if g]
                if groups:
                    decision_text = groups[-1].strip()
            if not (5 <= len(decision_text) <= 300):
                continue
            start, end = m.start(), m.end()
            ctx_start = max(0, start - 100)
            ctx_end = min(len(text), end + 100)
            context = text[ctx_start:ctx_end].replace("\n", " ").strip()
            findings.append({
                "label": label,
                "decision": decision_text[:300],
                "context": context[:300],
            })
    # Dedupe within this turn
    seen = set()
    deduped = []
    for f in findings:
        key = (f["decision"][:80],)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(f)
    return deduped


def append_to_log(findings: list[dict], session_id: str | None, output_chars: int):
    if not findings:
        return
    LIVE_LOG.parent.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now().isoformat(timespec="seconds")
    with LIVE_LOG.open("a", encoding="utf-8") as f:
        for finding in findings:
            entry = {
                "ts": now,
                "session_id": session_id,
                "label": finding["label"],
                "decision": finding["decision"],
                "context": finding["context"],
                "output_chars": output_chars,
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


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
    session_id = (data.get("session_id")
                  or data.get("sessionId"))

    output = extract_last_assistant_message(transcript_path)
    if not output or len(output) < MIN_OUTPUT_CHARS:
        return 0

    findings = find_decisions(output)
    if not findings:
        log_event("decision-capture", "noop",
                  meta={"reason": "no_decision_shape", "output_chars": len(output)})
        return 0

    try:
        append_to_log(findings, session_id, len(output))
        log_event("decision-capture", "fire",
                  meta={"captured": len(findings),
                        "output_chars": len(output),
                        "labels": [f["label"] for f in findings]})
    except Exception:
        # Silent on log failure — capture is augmentation, not load-bearing
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
