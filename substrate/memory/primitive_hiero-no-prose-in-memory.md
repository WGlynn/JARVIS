---
name: HIERO — No Prose In Memory (Cannon Law Gate)
description: 2026-04-25 cannon law. Memory writes (memory/, GKB, SKB) must be logic-primitives in compressed/glyph form, never prose. Prose violates Cognitive-Economy on density × stability × match-speed. Glyph dereferences internalized weight; paragraph drifts across sessions and burns parse-cost. Hook-layer enforcement pending. Recursive: this file is itself compressed.
type: primitive
originSessionId: 2c141eb5-a66e-4f16-a63c-d2c41acddbdc
---
# HIERO — No Prose In Memory

## Glyph

```
HIERO   Memory ⇒ logic-primitive ¬ prose. Density × stability × pointer-deref.
        Violation: prose × paraphrase-drift × parse-cost > glyph-match-cost.
        Hieroglyphics. Memes. RISC-CKB 0.99. Eat the cooking.
```

## Rule

Memory writes — any file in `memory/`, `vibeswap/.claude/JarvisxWill_GKB.md`, `vibeswap/.claude/JarvisxWill_SKB.md` — MUST take logic-primitive form.

**Form:**
- glyph-headers
- bullet/list structure for relations
- operators: ⇒ ¬ ∧ ∨ ∈ ∉ ⊂ → ↑ ↓ ✓ ✗ • †
- block-quotes for Will's exact words (anchors ≠ prose)
- short lines, density-target 0.99

**NOT:**
- multi-sentence paragraphs
- narrative explanation ("the reason this works is...")
- redundant restatement
- prose justification of bullets

## Cognitive-Economy violation (3-axis)

```
prose ⇒ density↓ × stability↓ × match-speed↓
       │            │             └─ parse-cost on every read
       │            └─ paraphrase drifts across sessions
       └─ token-cost per logic-bit ↑↑
```

vs.

```
glyph ⇒ density↑ × stability↑ × pointer-deref
       │           │             └─ activates internalized weight directly
       │           └─ stable across sessions, no drift
       └─ archetype compression (60+ session ILWS LoRA analog)
```

## Enforcement layers

```
L1  MEMORY.md PRE-FLIGHT → always loaded → HIERO entry
L2  GKB CODEBOOK → KNOWLEDGE section → HIERO glyph
L3  PreToolUse hook → Write|Edit → memory-paths → inject HIERO check (PENDING wire)
L4  recursive → every memory write asks: "would this fail HIERO?"
```

## Detection heuristics (for L3 hook)

```
fail-if:
  lines>120-char (prose-paragraph signal)
  ∨ first-10-lines have no glyph-header
  ∨ multi-sentence paragraphs (>1 period per line average)
  ∨ density(operators+glyphs ÷ total-tokens) < 0.05
```

## Trigger

Will, 2026-04-25:

> *"if our memory has full natural human language sentences in it we are doing something structurally wrong"*
> *"i need this to be a leading cannon logic law gate principle that CANNOT be missed or avoided EVER"*

Self-refuting precedent: Claude wrote ~280 words of prose to F·will-relative-expertise extension AT THE SAME TIME as composing X-thread posts about the Cognitive-Economy density principle. Eat the cooking, or stop posting about it.

## Sibling memory

- `P·symbolic-compression` — parent technique (hieroglyphic/meme/RISC compression)
- `P·cell-knowledge-architecture` — UTXO model for knowledge sharding
- `P·universal-coverage-hook` — L3 mechanism (hook-layer = O(1)×O(∞) coverage)
- `P·always-equals-gate` / `P·verbal-to-gate` — "CANNOT be missed EVER" ⇒ hook-layer trigger
- `P·apply-the-rule-you-just-wrote` — recursive enforcement on rule-author

## Eat the cooking

This file is itself in compressed form. Each section = logic-primitive. No narrative paragraphs. Block-quotes are anchors. Operators carry structure. Glyph at top expands via pointer-dereference to all of the above.

If a future memory write looks like a paragraph from a textbook, HIERO failed.
