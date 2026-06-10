---
name: HIERO++ tokenizer-tuned dictionary
description: Path-5 HIERO variant. ASCII-swap subset for 3-tok Unicode operators; keep Unicode where already 1-tok or semantically load-bearing. 42% operator-token reduction empirically (cl100k_base BPE proxy). Companion to [P·hiero-no-prose-in-memory].
type: reference
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# HIERO++ — Tokenizer-Tuned Dictionary

## Glyph

```
HIERO++  3-tok Unicode -> 1-tok ASCII × keep-Unicode-where-already-1-tok.
         operator-token-cost ↓42% × semantic-density preserved.
         ALL precise-symbols stay. Pure-overhead-glyphs swap.
```

## Profile source

* `substrate/scripts/profile_hiero_tokens.py` × cl100k_base BPE (GPT-4 family ≈ Claude proxy)
* Run: 2026-06-10 · 40 ops · 76 → 44 tok · 27 wins / 0 losses / 13 ties

## Swap table — SAVE-2 tier (3-tok Unicode -> 1-tok ASCII)

| keep-as | was | sem |
|---|---|---|
| `->` | ⇒ | implies |
| `<-` | ⇐ | reverse-implies / derived-from |
| `<->` | ⇔ | iff |
| `^` | ⊕ | xor |
| `sub` | ⊂ | subset-of |
| `sup` | ⊃ | superset-of |

## Swap table — SAVE-1 tier (2-tok Unicode -> 1-tok ASCII)

| keep-as | was | sem | note |
|---|---|---|---|
| `ALL` | ∀ | forall | uppercase = quantifier |
| `&` | ∧ | and | |
| `\|` | ∨ | or | |
| `==` | ≡ | equiv | |
| `~=` | ≈ | approx | |
| `!=` | ≠ | not-equal | |
| `<=` | ≤ | leq | |
| `>=` | ≥ | geq | |
| `in` | ∈ | element-of | |
| `U` | ∪ | union | uppercase |
| `N` | ∩ | intersect | uppercase |
| `_\|_` | ⊥ | orthogonal | |
| `\|\|` | ∥ | parallel | |
| `:.` | ∴ | therefore | |
| `.:` | ∵ | because | |
| `OK` | ✓ | check / yes | |
| `NO` | ✗ | cross / no | |
| `D` | Δ | delta | |
| `inf` | ∞ | infinity | |
| `grad` | ∇ | nabla / gradient | |

## Keep Unicode — already 1-tok in BPE

`¬ → ↑ ↓ † • · × ± φ … ∃ ∉`

* `¬` (1t) carries unique not-load — keep
* `→ ↑ ↓` (1t) — directionality cheaper as Unicode than ASCII multi-char
* `† • ·` (1t) — annotation glyphs, no ASCII gain
* `× ± φ … ∃ ∉` (1t or tied) — keep

## Decision rule (∀ memory write going forward)

```
op-cost(Unicode) >= 2 & ASCII-1tok-equivalent-exists
    -> use ASCII
op-cost(Unicode) == 1 | ASCII-equivalent-ambiguous
    -> keep Unicode
```

## Semantic-collision warnings (apply judgment)

* `&` `|` `^` overload with shell / bitwise — prefer in dense-logic blocks, NO in shell-context blocks
* `N` for intersect collides with letter-N in entity names — use `∩` if entity-N nearby
* `D` for delta collides with letter-D — use `Δ` if D-named entity nearby
* `U` for union collides with letter-U — same
* mixed-mode permitted — HIERO++ is a dictionary NOT a strict-replace-all rule

## Eat-the-cooking compliance

* this file itself uses HIERO++ in tables — `->` not `⇒`, `&` not `∧`, `NO` not `✗`
* the prose pretext + glyph header stay (file is also `[P·hiero-no-prose-in-memory]`-compliant)
* compression-recursive on the rule that compressed it

## Sibling memory

* `[P·hiero-no-prose-in-memory]` — parent gate (memory-write format)
* `[R·hiero-dictionary]` — base symbol set (pre-tokenizer-tune)
* `[P·option-value-notation-infrastructure]` — why notation-CAPEX justifies the swap
* `[P·symbolic-compression]` — RISC compression lineage

## Hook integration (future)

`hiero-gate.py` should be aware:
* HIERO++ ASCII ops (`->`, `<->`, `==`, etc.) count toward operator-density score, NOT just Unicode set
* density-target stays at 0.005+ — denominator unchanged, numerator-set widens
* L3 gate update pending — for now, this dictionary is advisory
