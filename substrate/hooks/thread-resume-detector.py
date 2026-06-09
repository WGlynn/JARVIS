#!/usr/bin/env python3
"""
Thread-Resume Detector — Continuity-of-Thought at Prompt Time
=============================================================

UserPromptSubmit hook. When a prompt arrives, scores it against the
HIGH-urgency entries in `_system/open_threads.md` and surfaces likely
RESUME candidates as additionalContext.

WHY
---
The open-threads aggregator builds a static index of in-flight work.
Deep-recall surfaces relevant memory primitives. Neither catches the
specific case of "this prompt is resuming a thread we explicitly left
open in SESSION_STATE / WAL / AA candidates."

Example failure mode this catches:
  Prior session: SESSION_STATE "NEXT SESSION: continue USD8 outreach
    rapid-fire, day-2 batch of 10 targets"
  Next session prompt: "let's do another batch"
  Without this hook: assistant tries to interpret "batch" from generic
    context, misses the explicit hand-off
  With this hook: "RESUME CANDIDATE: SESSION_STATE NEXT-SESSION names
    'continue USD8 outreach rapid-fire day-2 batch' — last edited 0d ago"

Approach
--------
1. Parse `_system/open_threads.md` HIGH-urgency section
2. Extract each thread line + source (already structured by aggregator)
3. Tokenize prompt + each thread line
4. Score by token overlap (Jaccard with substantive-token weighting)
5. If top score >= threshold, surface as RESUME CANDIDATE
6. Cap at top 3 matches to avoid clutter

Lightweight scoring (Jaccard with stopwords stripped) rather than TF-IDF,
because:
  - open_threads.md is short (~200-300 lines)
  - prompt-time hook must be fast (<1s budget reasonable)
  - threads are short phrases not full documents, so TF-IDF brings
    little extra signal

Conservative defaults:
  - MIN_PROMPT_TOKENS = 3 (skip on trivial prompts like "yes" / "go")
  - MATCH_THRESHOLD = 0.20 (token-overlap Jaccard)
  - TOP_K = 3

Origin: 2026-05-13 autopilot. Closes the prompt-time continuity gap left
open by deep-recall (which matches semantic, not "this is the thing we
explicitly said to resume").
"""
import json
import os
import re
import sys
from pathlib import Path

MEMORY_DIR = Path.home() / ".claude" / "projects" / "C--Users-Will" / "memory"
OPEN_THREADS_PATH = MEMORY_DIR / "_system" / "open_threads.md"

# Telemetry
_HOOKS_DIR = Path(__file__).parent
sys.path.insert(0, str(_HOOKS_DIR))
try:
    from _telemetry import log_event
except Exception:
    def log_event(*a, **kw): pass


MIN_PROMPT_TOKENS = 3
# Score = |prompt ∩ thread| / |prompt|. Asymmetric coverage: penalizes
# long-thread Jaccard inflation while keeping signal when most of the
# prompt's substantive tokens appear in the thread.
MATCH_THRESHOLD = 0.40
TOP_K = 3

TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_\-]{2,29}")
STOPWORDS = {
    "the", "and", "for", "but", "with", "this", "that", "from", "have",
    "are", "was", "were", "been", "being", "has", "had", "not", "you",
    "your", "all", "any", "can", "will", "would", "could", "should",
    "what", "when", "where", "which", "who", "how", "why", "into", "out",
    "over", "under", "between", "than", "then", "they", "them", "their",
    "there", "these", "those", "some", "such", "also", "only", "just",
    "yes", "okay", "now", "still", "even", "ever", "never",
    "let", "lets", "lemme", "want", "need", "give", "tell", "ask",
    "thread", "threads", "pending", "todo", "next", "session",
    "back", "continue", "keep", "going",
}


def tokenize(text: str) -> set[str]:
    return {m.lower() for m in TOKEN_PATTERN.findall(text)
            if m.lower() not in STOPWORDS}


def parse_high_urgency_section(content: str) -> list[dict]:
    """Extract HIGH-urgency entries from open_threads.md.

    Format expected (set by _open_threads.py render_bucket):
      ### `<source>`
      - **[kind]** (Nd) LN — <line text>
    """
    threads = []
    in_high = False
    current_source = None
    for raw in content.splitlines():
        line = raw.rstrip()
        if line.startswith("## HIGH urgency"):
            in_high = True
            continue
        if in_high and line.startswith("## ") and "HIGH urgency" not in line:
            break  # exited HIGH section
        if not in_high:
            continue
        # Source header
        m_src = re.match(r"^###\s+`(.+?)`\s*$", line)
        if m_src:
            current_source = m_src.group(1)
            continue
        # Thread entry
        m_entry = re.match(r"^-\s+\*\*\[(.+?)\]\*\*\s*(?:\((\d+d?)\))?\s*(?:L(\d+))?\s*[—-]\s*(.+)$", line)
        if m_entry and current_source:
            kind, age, line_no, text = m_entry.groups()
            threads.append({
                "source": current_source,
                "kind": kind,
                "age": age or "",
                "line_no": line_no or "",
                "text": text.strip(),
            })
    return threads


def prompt_coverage(prompt_tokens: set, thread_tokens: set) -> float:
    """Fraction of prompt tokens that appear in the thread.
    Asymmetric: penalizes neither long threads nor short prompts."""
    if not prompt_tokens or not thread_tokens:
        return 0.0
    inter = len(prompt_tokens & thread_tokens)
    return inter / len(prompt_tokens)


def score_threads(prompt_tokens: set, threads: list[dict]) -> list[tuple[float, dict]]:
    scored = []
    for t in threads:
        thread_tokens = tokenize(t["text"])
        if not thread_tokens:
            continue
        s = prompt_coverage(prompt_tokens, thread_tokens)
        if s >= MATCH_THRESHOLD:
            scored.append((s, t))
    scored.sort(key=lambda x: -x[0])
    return scored


def main() -> int:
    try:
        payload = sys.stdin.read()
        data = json.loads(payload) if payload.strip() else {}
    except Exception:
        return 0

    prompt = (data.get("prompt")
              or data.get("user_prompt")
              or data.get("userPrompt")
              or "")
    if not isinstance(prompt, str) or len(prompt) < 8:
        return 0

    prompt_tokens = tokenize(prompt)
    if len(prompt_tokens) < MIN_PROMPT_TOKENS:
        return 0

    if not OPEN_THREADS_PATH.exists():
        return 0

    try:
        content = OPEN_THREADS_PATH.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return 0

    threads = parse_high_urgency_section(content)
    if not threads:
        return 0

    scored = score_threads(prompt_tokens, threads)
    if not scored:
        log_event("thread-resume", "noop",
                  meta={"reason": "no_match",
                        "prompt_tokens": len(prompt_tokens),
                        "threads_scanned": len(threads)})
        return 0

    top = scored[:TOP_K]
    log_event("thread-resume", "match",
              matches=[t["source"] for _, t in top],
              meta={"top_score": round(top[0][0], 3),
                    "match_count": len(scored),
                    "prompt_tokens": len(prompt_tokens)})

    lines = [
        "[THREAD-RESUME DETECTOR — open-thread match on prompt]",
        "",
        "This prompt has high token overlap with explicitly-open threads",
        "from prior sessions (SESSION_STATE NEXT-SESSION blocks, WAL carry-",
        "forward items, AA candidate drafts). Consider whether the user is",
        "resuming a known thread vs starting fresh.",
        "",
        f"Top {len(top)} match{'es' if len(top) > 1 else ''} (Jaccard token overlap):",
        "",
    ]
    for score, t in top:
        age_part = f" ({t['age']})" if t['age'] else ""
        line_part = f" L{t['line_no']}" if t['line_no'] else ""
        lines.append(f"- **{score:.2f}** — `{t['source']}`{age_part}{line_part}")
        lines.append(f"  - thread: {t['text'][:200]}")

    lines.extend([
        "",
        "If this is a resume: pull the source file for full context before",
        "responding. If unrelated: ignore. Do not mention this detector",
        "unless it changed your interpretation.",
    ])

    out = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": "\n".join(lines),
        }
    }
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
