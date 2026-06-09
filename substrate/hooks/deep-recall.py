#!/usr/bin/env python3
"""
Deep Recall Hook
================

UserPromptSubmit hook. On every user prompt, scores the prompt against the
full memory corpus using TF-IDF cosine similarity, surfaces the top-K most
relevant primitives via additionalContext.

Solves the deep-recall problem named by Will 2026-05-13: "relevant context
from 6 months ago needs to hit as cleanly as context from 1 minute ago."

The current recall stack is age-biased:
  - SESSION_STATE: recent block (recent-biased)
  - WARM_MAP: shard loads on topic-keyword (presence-biased)
  - Entity index: exact-name lookup on Write/Edit (precision-biased,
    only fires on writes)

This hook fires on every user prompt — age-agnostic, semantic-similarity-
ranked, surfaces context regardless of when it was written.

Pipeline:
  1. Load semantic_index.json (built by _semantic_index.py)
  2. Tokenize the user prompt
  3. Build query vector (same TF-IDF formula as docs)
  4. Cosine similarity vs every doc (dot product, both L2-normalized)
  5. Top-K above threshold surface with score + brief snippet

Designed for low overhead: <50ms for 440-doc corpus on Will's hardware.

The hook does not block prompts. It surfaces context that the assistant
can choose to load fully (by reading the surfaced file) or ignore.

Tuning:
  - MIN_SCORE: 0.15 (cosine in [0,1]; 0.15 is "noticeable overlap")
  - TOP_K: 6 (cap on suggestions; more than this becomes noise)
  - MIN_QUERY_TOKENS: 4 (skip on trivial prompts to avoid surfacing for "ok"
    type messages)
"""
import json
import math
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

MEMORY_DIR = Path.home() / ".claude" / "projects" / "C--Users-Will" / "memory"
SEMANTIC_INDEX_PATH = MEMORY_DIR / "_system" / "semantic_index.json"

# Telemetry: log every hook fire to _system/protocol_telemetry.jsonl
_HOOKS_DIR = Path(__file__).parent
sys.path.insert(0, str(_HOOKS_DIR))
try:
    from _telemetry import log_event
except Exception:
    def log_event(*a, **kw): pass

MIN_SCORE = 0.07  # Calibrated against 440-doc, top-40-terms-per-doc index.
# Cosine ceiling is constrained by sqrt(query_terms/doc_terms); for typical
# 8-token queries against 40-term docs the realistic max is ~0.45. 0.07
# captures relevant matches without surfacing every distant overlap.
TOP_K = 6
MIN_QUERY_TOKENS = 4
SNIPPET_MAX_LEN = 160

# Same tokenizer as the index builder so query and doc vectors live in
# the same space.
TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_\-·]{2,29}")
STOPWORDS = {
    "the", "and", "for", "but", "with", "this", "that", "from", "have",
    "are", "was", "were", "been", "being", "has", "had", "not", "you",
    "your", "all", "any", "can", "will", "would", "could", "should",
    "what", "when", "where", "which", "who", "how", "why", "into", "out",
    "over", "under", "between", "than", "then", "they", "them", "their",
    "there", "these", "those", "some", "such", "also", "only", "just",
    "yes", "okay", "ok", "now", "still", "even", "ever", "never",
    "name", "description", "type", "originSessionId",
}

_index_cache: dict | None = None


def _load_index() -> dict | None:
    global _index_cache
    if _index_cache is not None:
        return _index_cache
    if not SEMANTIC_INDEX_PATH.exists():
        return None
    try:
        with SEMANTIC_INDEX_PATH.open(encoding="utf-8") as f:
            _index_cache = json.load(f)
    except Exception:
        return None
    return _index_cache


def tokenize(text: str) -> list[str]:
    tokens = []
    for m in TOKEN_PATTERN.findall(text):
        t = m.lower()
        if t not in STOPWORDS:
            tokens.append(t)
    return tokens


def build_query_vector(query_tokens: list[str], vocabulary: dict, idf: dict) -> list[tuple[int, float]]:
    """Build a TF-IDF query vector using the same formula as docs."""
    tf = Counter(t for t in query_tokens if t in vocabulary)
    if not tf:
        return []
    scores = []
    for term, freq in tf.items():
        tid = vocabulary[term]
        idf_w = idf.get(str(tid), 0.0)
        score = (1.0 + math.log(freq)) * idf_w
        scores.append((tid, score))
    # L2-normalize
    norm = math.sqrt(sum(s * s for _, s in scores)) or 1.0
    return [(tid, s / norm) for tid, s in scores]


def cosine_similarity(query: list[tuple[int, float]], doc: list) -> float:
    """Dot product of two L2-normalized sparse vectors."""
    q_map = {tid: s for tid, s in query}
    sim = 0.0
    for tid, s in doc:
        if tid in q_map:
            sim += q_map[tid] * s
    return sim


def get_snippet(rel_path: str) -> str:
    """Pull the description or first non-empty content line from a primitive."""
    filepath = MEMORY_DIR / rel_path
    if not filepath.exists():
        return ""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""
    # Prefer description: field if present
    m = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip()[:SNIPPET_MAX_LEN]
    # Fall back to first non-empty body line
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("---") or line.startswith("#"):
            continue
        if line.startswith(("name:", "type:", "originSessionId:")):
            continue
        return line[:SNIPPET_MAX_LEN]
    return ""


def main() -> int:
    try:
        payload = sys.stdin.read()
        data = json.loads(payload) if payload.strip() else {}
    except Exception:
        return 0

    prompt = data.get("user_prompt") or data.get("prompt") or ""
    if not isinstance(prompt, str):
        return 0

    query_tokens = tokenize(prompt)
    if len(query_tokens) < MIN_QUERY_TOKENS:
        return 0

    index = _load_index()
    if index is None:
        return 0

    vocabulary = index.get("vocabulary", {})
    idf = index.get("idf", {})
    documents = index.get("documents", {})

    query_vec = build_query_vector(query_tokens, vocabulary, idf)
    if not query_vec:
        return 0

    # Score every doc
    ranked: list[tuple[float, str]] = []
    for rel_path, doc_vec in documents.items():
        sim = cosine_similarity(query_vec, doc_vec)
        if sim >= MIN_SCORE:
            ranked.append((sim, rel_path))

    if not ranked:
        log_event("deep-recall", "noop",
                  meta={"reason": "below_threshold", "query_tokens": len(query_tokens)})
        return 0

    ranked.sort(key=lambda x: -x[0])
    top = ranked[:TOP_K]
    log_event("deep-recall", "match",
              matches=[p for _, p in top],
              meta={"top_score": round(top[0][0], 3),
                    "total_above_threshold": len(ranked),
                    "query_tokens": len(query_tokens)})

    lines = [
        "[DEEP RECALL — semantic similarity over full memory corpus]",
        "",
        "The current prompt has high semantic overlap with the memory primitives below.",
        "Surfaced regardless of age — relevance over recency. Load any that look load-bearing",
        "before responding. Score is cosine similarity (0-1; higher = more relevant).",
        "",
    ]
    for score, rel_path in top:
        snippet = get_snippet(rel_path)
        lines.append(f"- **{rel_path}** ({score:.2f})")
        if snippet:
            lines.append(f"  - {snippet}")
    lines.extend([
        "",
        "If a match changes the right answer, read the file and incorporate. If irrelevant,",
        "ignore. Don't acknowledge this surfacing unless it produced an actionable change.",
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
