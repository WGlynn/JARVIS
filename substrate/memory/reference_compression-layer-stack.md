---
name: Compression-layer stack (L0..L6)
description: 7-layer memory/substrate compression stack. L1-L2 partner-readable, L3-L6 machine-internal where readability is dropped for density. L3+L4 shipped 2026-06-10.
type: reference
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# Compression-Layer Stack — L0..L6

## Glyph

```
COMP-STACK  L0(prose-banned) -> L1(HIERO) -> L2(HIERO++) ->
            L3(APL-hot-path) -> L4(Z-tok cache) ->
            L5(Schelling-IDs) -> L6(SK-genome).
            density-up ALL layers; readability dropped layer-by-layer.
```

## Layer table

| L | name | readability | density-win | status | path |
|---|---|---|---|---|---|
| L0 | prose | full | baseline | BANNED in memory | `[P·hiero-no-prose-in-memory]` |
| L1 | HIERO Unicode | high | ~30% vs prose | LIVE | `[R·hiero-dictionary]` |
| L2 | HIERO++ ASCII-tuned | high | +42% op-tok vs L1 | LIVE | `[R·hiero-pp-dictionary]` |
| L3 | APL-style hot-path ops | debug-only | ~70% src-tok on dot-product call-sites; smaller win on linear scans | MODULE-LIVE 2026-06-10; 1 consumer (AA#4 `recent_research_count`) | `~/.claude/hooks/_terse_ops.py` |
| L4 | Z-token corpus cache | machine-only | drift-detect + token-budget visibility at boot; future: encode-pass skip when downstream consumer needs token-IDs | LIVE 2026-06-10 (cache + SessionStart warmer registered) | `_system/corpus.tokens.jsonl` + `corpus-cache-warmer.py` |
| L5 | Schelling canonical-IDs | renderer-expanded | port-stable across substrates | partial (P·/F·/R·/J· prefixes) | future |
| L6 | SK combinator genome | bootstrap-only | substrate-portable kernel | future | `[F·blockchain-not-contracts]` analog |

## Per-layer notes

### L3 — APL hot-path

* file: `~/.claude/hooks/_terse_ops.py`
* exports 1-char ops: `a e c S P M m d f Z W k R H T s j B N D J` + `score conf recent`
* first consumer: `research-before-capability-claim-gate.py::recent_research_count`
* policy: NO partner-facing code; ONLY hook-internal hot paths
* debug-time readability via the docstring legend in `_terse_ops.py`

### L4 — Z-token cache

* file: `_system/corpus.tokens.jsonl`
* builder: `substrate/scripts/pretokenize_corpus.py`
* tokenizer: cl100k_base BPE (GPT-4 proxy; Claude BPE differs in absolute IDs, but encode-pass-skipped property generalizes when the cache is built with Claude's BPE)
* cached: MEMORY.md + 5 sub-indexes + MEMORY_AUDIT_ARSENAL + wwwd_corpus_priority
* first-pass: 43,823 bytes -> 11,924 token-IDs
* re-run is sha256-incremental (skip unchanged files)
* **consumer wired 2026-06-10**: `~/.claude/hooks/corpus-cache-warmer.py` SessionStart, registered in `settings.json`.
* warmer does: sha256-drift detection → auto re-pretokenize → emit per-file token cost + boot-budget warning into boot context.
* first signal it surfaced: MEMORY.md is 283 B over the 24,400-B boot-load budget (6,779 tokens).
* future value: pure encode-pass skip when downstream consumers (e.g., partner-context-builder, semantic-index updater) read token-IDs directly from cache instead of re-encoding source text.

## Decision rule (which layer to deploy)

```
partner-facing | external-share        -> L1 / L2 only
memory primitive | doc                 -> L2 default
hook internals (scoring, math)         -> L3
boot-time read structures              -> L4 + L1/L2 source
cross-substrate canonical-ID           -> L5
fork-bootstrap kernel                  -> L6
```

## Eat-the-cooking

* this file uses L2 (HIERO++) — `->` not `⇒`, `&` not `∧`
* tables compress more than narrative ALL day
* glyph at top expands via pointer-deref to L0..L6

## Sibling memory

* `[P·hiero-no-prose-in-memory]` — L0/L1 gate
* `[R·hiero-pp-dictionary]` — L2 lexicon
* `[P·symbolic-compression]` — compression lineage
* `[P·option-value-notation-infrastructure]` — why CAPEX on notation pays back
* `[P·jarvis-substrate-decentralization-roadmap]` — L5/L6 future-state context

## Open questions

* L5 Schelling-ID: do we need content-addressed hashes (CID) OR keep human-prefix `P·` system?
* L6 SK genome: is the export target a CKB-cell, a tarball, or a single .py?
* tokenizer mismatch: cl100k_base ≠ Claude BPE exactly. Worth fingerprinting via API?
