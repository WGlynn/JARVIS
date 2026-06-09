#!/usr/bin/env python3
"""
Post-Generation Reflection (L4 of the JARVIS Protocol-LLM Overlay)
==================================================================

Stop hook. After the assistant completes a turn, re-runs deep-recall over
the GENERATED OUTPUT (not just the input prompt). Catches a class of drift
that input-side recall cannot:

  User prompt mentions A. Input deep-recall pre-loads context for A.
  Assistant turn drifts toward B (perhaps a related entity, a tangent, a
  cited mechanism). The assistant's response mentions B prominently. The
  context relevant to B was never loaded because the input prompt did
  not name B.

  Result: a response that ships without the structural correctness check
  the team has discipline for. L4 closes this gap by running the recall
  layer over outputs.

Implements the L4 layer of the JARVIS overlay architecture documented in
JARVIS/05-meta-protocols/jarvis-protocol-llm-overlay.md. The overlay
without L4 is "input-reflected, output-unchecked." With L4, every
generation passes through the same recall + cross-reference machinery
that gates inputs.

Conservative tuning:
  - stop_hook_active guard prevents infinite loops
  - Threshold tighter than input deep-recall (0.12 vs 0.07): the output
    has already been written, so we surface only HIGH-relevance matches
    rather than every cosine overlap
  - TOP_K capped at 3
  - Falls back to no-op if transcript can't be parsed (graceful degradation)

Hook contract:
  - Reads stdin JSON for stop_hook_active + transcript_path
  - If active, return 0 (let stop proceed)
  - Otherwise, parse transcript JSONL, extract last assistant message
  - Run deep-recall over the message content
  - If high-relevance matches surface, return additionalContext via
    hookSpecificOutput; otherwise return 0
"""
import json
import math
import os
import re
import sys
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

# Tighter threshold than input deep-recall — only surface STRONG matches
# at output reflection time
MIN_SCORE = 0.12
TOP_K = 3
MIN_OUTPUT_TOKENS = 50  # skip on trivial outputs ("ok", "done", etc.)

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
    return [m.lower() for m in TOKEN_PATTERN.findall(text)
            if m.lower() not in STOPWORDS]


def build_query_vector(tokens, vocab, idf):
    tf = Counter(t for t in tokens if t in vocab)
    if not tf:
        return []
    scores = []
    for term, freq in tf.items():
        tid = vocab[term]
        idf_w = idf.get(str(tid), 0.0)
        scores.append((tid, (1.0 + math.log(freq)) * idf_w))
    norm = math.sqrt(sum(s * s for _, s in scores)) or 1.0
    return [(tid, s / norm) for tid, s in scores]


def cosine_similarity(query, doc):
    q_map = {tid: s for tid, s in query}
    return sum(q_map[tid] * s for tid, s in doc if tid in q_map)


def extract_last_assistant_message(transcript_path: str) -> str | None:
    """Read a JSONL transcript and return the most recent assistant message
    text. Returns None if the transcript can't be parsed or has no assistant
    messages."""
    p = Path(transcript_path)
    if not p.exists():
        return None
    try:
        last_assistant_text = None
        with p.open(encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except Exception:
                    continue
                # Claude Code transcript entries have various shapes; we look
                # for the assistant text wherever it sits.
                role = (entry.get("role")
                        or entry.get("message", {}).get("role")
                        or "")
                if role != "assistant":
                    continue
                # Text content can be in message.content (list of blocks)
                # or content directly.
                content = (entry.get("content")
                           or entry.get("message", {}).get("content")
                           or "")
                if isinstance(content, list):
                    text_parts = []
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            text_parts.append(block.get("text", ""))
                        elif isinstance(block, str):
                            text_parts.append(block)
                    last_assistant_text = "\n".join(text_parts)
                elif isinstance(content, str):
                    last_assistant_text = content
        return last_assistant_text
    except Exception:
        return None


def get_snippet(rel_path: str) -> str:
    filepath = MEMORY_DIR / rel_path
    if not filepath.exists():
        return ""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""
    m = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip()[:140]
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("---") or line.startswith("#"):
            continue
        if line.startswith(("name:", "type:", "originSessionId:")):
            continue
        return line[:140]
    return ""


def main() -> int:
    try:
        payload = sys.stdin.read()
        data = json.loads(payload) if payload.strip() else {}
    except Exception:
        return 0

    # Prevent infinite reflection loops
    if data.get("stop_hook_active") or data.get("stopHookActive"):
        return 0

    transcript_path = (data.get("transcript_path")
                       or data.get("transcriptPath") or "")
    if not transcript_path:
        return 0

    output = extract_last_assistant_message(transcript_path)
    if not output:
        return 0

    tokens = tokenize(output)
    if len(tokens) < MIN_OUTPUT_TOKENS:
        return 0

    index = _load_index()
    if index is None:
        return 0

    vocabulary = index.get("vocabulary", {})
    idf = index.get("idf", {})
    documents = index.get("documents", {})

    query_vec = build_query_vector(tokens, vocabulary, idf)
    if not query_vec:
        return 0

    ranked = []
    for rel_path, doc_vec in documents.items():
        sim = cosine_similarity(query_vec, doc_vec)
        if sim >= MIN_SCORE:
            ranked.append((sim, rel_path))

    if not ranked:
        log_event("post-generation-reflect", "noop",
                  meta={"reason": "below_threshold", "output_tokens": len(tokens)})
        return 0

    ranked.sort(key=lambda x: -x[0])
    top = ranked[:TOP_K]
    log_event("post-generation-reflect", "match",
              matches=[p for _, p in top],
              meta={"top_score": round(top[0][0], 3),
                    "total_above_threshold": len(ranked),
                    "output_tokens": len(tokens)})

    lines = [
        "[POST-GENERATION REFLECTION — L4 of JARVIS overlay]",
        "",
        "The just-completed turn has high semantic overlap with memory primitives below.",
        "These were not necessarily surfaced by input-side deep-recall (the output may",
        "have drifted toward content the prompt did not predict). Review whether any",
        "would change the right answer before truly ending:",
        "",
    ]
    for score, rel_path in top:
        snippet = get_snippet(rel_path)
        lines.append(f"- **{rel_path}** ({score:.2f})")
        if snippet:
            lines.append(f"  - {snippet}")
    lines.extend([
        "",
        "If a match changes the right answer, load the file and revise. If irrelevant,",
        "ignore. Do not acknowledge this reflection unless it produced a revision.",
    ])

    # BUG FIX 2026-05-14: Stop event does NOT support hookSpecificOutput.additionalContext
    # in the Claude Code hook schema. Emitting it caused 16h of silent JSON-schema-validation
    # rejections. Solution: persist the reflection to a file the UserPromptSubmit-side
    # post-generation-recall hook can read on next prompt + emit nothing on stdout.
    # This preserves the L4 reflection signal across turn boundaries without violating
    # the Stop hook output contract.
    reflection_record = {
        "ts": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
        "top_matches": [{"score": round(s, 3), "path": p} for s, p in top],
        "rendered": "\n".join(lines),
    }
    try:
        REFLECTION_PATH = MEMORY_DIR / "_system" / "post_gen_reflections.jsonl"
        REFLECTION_PATH.parent.mkdir(parents=True, exist_ok=True)
        with REFLECTION_PATH.open("a", encoding="utf-8") as f:
            f.write(__import__("json").dumps(reflection_record, ensure_ascii=False) + "\n")
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
