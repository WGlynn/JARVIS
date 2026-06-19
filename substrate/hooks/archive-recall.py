#!/usr/bin/env python3
"""
Archive Recall Hook
===================

UserPromptSubmit hook. The half that makes the JARVIS mind archive USEFUL
instead of ceremony: an index nobody consults is dead weight. This fires on
every substantive prompt and surfaces the highest-signal WORK-PRODUCT artifacts
(specs, handoffs, audits, design docs, drafts) that match what's being asked —
so prior work gets REUSED instead of re-derived or contradicted.

Division of labour (no overlap):
  - deep-recall.py   -> memory PRIMITIVES (principles / how-we-work)
  - entity-index     -> exact-name lookup on Write/Edit
  - archive-recall   -> the prose RECORD of what we already built (this hook)
  - git              -> the code itself

Lexical scoring over archive/INDEX.json (tags 5 > title 3 > summary 1 > path .5,
summed across query tokens), recency as tiebreak. Deliberately HIGH threshold:
only genuine multi-signal matches surface, so this stays load-bearing, not noise.
Zero deps, deterministic, ~15ms (882KB JSON parse).

Tuning:
  - MIN_SCORE 6.0   : needs more than one weak tag hit (e.g. tag+title, or
                      tag+summary+path) before it surfaces.
  - TOP_K 4         : work-product artifacts are heavier to read than primitives.
  - MIN_TOKEN_LEN 4 : substring matching on <4-char tokens is too noisy.
"""
import json
import re
import sys
from pathlib import Path

INDEX_PATH = Path.home() / ".claude" / "projects" / "C--Users-Will" / "archive" / "INDEX.json"

_HOOKS_DIR = Path(__file__).parent
sys.path.insert(0, str(_HOOKS_DIR))
try:
    from _telemetry import log_event
except Exception:
    def log_event(*a, **kw):
        pass

MIN_SCORE = 6.0
TOP_K = 4
MIN_QUERY_TOKENS = 4
MIN_TOKEN_LEN = 4
W_TAG, W_TITLE, W_SUMMARY, W_PATH = 5.0, 3.0, 1.0, 0.5

TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_\-]{3,29}")
STOPWORDS = {
    "this", "that", "from", "have", "with", "your", "what", "when", "which",
    "where", "would", "could", "should", "about", "there", "these", "those",
    "some", "such", "also", "only", "just", "still", "even", "ever", "never",
    "make", "made", "want", "need", "consider", "continue", "think", "into",
    "over", "under", "than", "then", "them", "their", "they", "been", "being",
    "does", "done", "doing", "genuinely", "really", "etc", "stuff", "thing",
    "things", "right", "next", "work", "working", "good", "best", "more",
    "most", "like", "look", "looks", "something", "mentioned", "improve",
    "improving", "useful", "full", "auto", "manage", "yourself",
}


def tokenize(text):
    out = set()
    for m in TOKEN_PATTERN.findall(text):
        t = m.lower()
        if len(t) >= MIN_TOKEN_LEN and t not in STOPWORDS:
            out.add(t)
    return out


def score(entry, terms):
    tags = " ".join(entry.get("tags", [])).lower()
    title = entry.get("title", "").lower()
    summary = entry.get("summary", "").lower()
    path = entry.get("path", "").lower()
    s = 0.0
    for t in terms:
        if t in tags:
            s += W_TAG
        if t in title:
            s += W_TITLE
        if t in summary:
            s += W_SUMMARY
        if t in path:
            s += W_PATH
    return s


def main():
    try:
        payload = sys.stdin.read()
        data = json.loads(payload) if payload.strip() else {}
    except Exception:
        return 0

    prompt = data.get("user_prompt") or data.get("prompt") or ""
    if not isinstance(prompt, str):
        return 0

    terms = tokenize(prompt)
    if len(terms) < MIN_QUERY_TOKENS:
        return 0

    if not INDEX_PATH.exists():
        return 0
    try:
        corpus = json.load(INDEX_PATH.open(encoding="utf-8"))
    except Exception:
        return 0

    ranked = []
    for e in corpus:
        sc = score(e, terms)
        if sc >= MIN_SCORE:
            ranked.append((sc, e))

    if not ranked:
        log_event("archive-recall", "noop",
                  meta={"reason": "below_threshold", "query_tokens": len(terms)})
        return 0

    ranked.sort(key=lambda se: (se[0], se[1].get("date", "")), reverse=True)
    top = ranked[:TOP_K]
    log_event("archive-recall", "match",
              matches=[e["path"] for _, e in top],
              meta={"top_score": round(top[0][0], 1),
                    "total_above_threshold": len(ranked),
                    "query_tokens": len(terms)})

    lines = [
        "[ARCHIVE RECALL — prior work-product matching this prompt]",
        "",
        "We may have ALREADY built / decided / drafted something here. These are the",
        "highest-signal artifacts from the mind archive (specs, handoffs, audits, drafts).",
        "Read the relevant path BEFORE re-deriving or you risk redoing/contradicting it.",
        "",
    ]
    for sc, e in top:
        tg = ", ".join(e.get("tags", [])) or "-"
        lines.append(f"- **{e['title']}** ({e['date']}, [{tg}])")
        if e.get("summary"):
            lines.append(f"  - {e['summary']}")
        lines.append(f"  - `{e['path']}`")
    lines.extend([
        "",
        "If none change the right answer, ignore. Don't acknowledge unless it changed something.",
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
