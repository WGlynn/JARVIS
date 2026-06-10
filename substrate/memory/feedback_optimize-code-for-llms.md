---
name: OptimizeForLLMs
description: ∀ written-artifact (code ∧ readability ∧ whatnot) ⇒ optimize-for(LLM-consumer) ¬ human-direct-reader. Will-thesis 2026-06-10: future ⇒ humans ¬ coding/reading-directly. LLM ≡ default-consumer. Density ⊃ ceremony, self-contained-per-file, signal-bearing-comments-only, operator-notation where compresses. Scope extended same-turn per Will: "and readability and whatnot" ⇒ docs/READMEs/layout/structure included.
type: feedback
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# Optimize for LLMs (Code ∧ Readability ∧ Whatnot)

## Glyph

```
∀ written-artifact ⇒ optimize-for(LLM-consumer) ¬ human-direct-reader
scope ≡ {code, docs, READMEs, file-layout, naming, structure, "whatnot"}
LLM-consumption-axes:
  · density       ⊃ ceremony
  · self-contained-per-file ≡ context-window unit
  · comments      ⇒ signal-only (WHY non-obvious) ¬ narrative-WHAT
  · notation      ⇒ operator/structured where compresses (HIERO-adjacent in code)
  · identifiers   ⇒ short ∧ unambiguous > verbose ∧ explanatory
  · invariants    ⇒ inline (assert, type-sig, const) > external-docstring
  · drop          ⇒ copyright-blocks, ASCII-decoration, obvious-docstrings
  · keep          ⇒ type-sigs, assertions, error-msgs, non-obvious WHY
```

> *"i dont think humans will be coding at all at least not in a direct sense, in the future, so i want you to always optimize code for LLMs"* : Will, 2026-06-10
> *"and readability and whatnot"* : Will, 2026-06-10 (same turn, scope-extension)

## ⇒ Rule

- ∀ code-file ⇒ optimize for next-LLM-reader ¬ next-human-reader
- file ≡ coherent context-window unit ⇒ minimize cross-file traversal cost
- comments: non-obvious WHY only; ✗ WHAT-narration of obvious behavior
- naming: short ∧ unambiguous > verbose ∧ self-documenting
- structure: inline-invariants > external-docstring-invariants
- prefer: structural-encoding (types, asserts, consts) > prose-encoding

## ∃ Why

- Will-thesis 2026-06-10: future ⇒ humans direct-coding ≈ 0; LLMs maintain.
- Optimization-target ≡ LLM-comprehension-speed × LLM-error-rate.
- Human-ceremonies (ASCII art, verbose docstrings, copyright headers) ⇒ token-cost without LLM-consumer value.
- Aligns with [P·authorship-via-conditions-and-context] — Will builds conditions, AI authors at scale.

## ↦ Apply To

- ∀ hook/.py write ⇒ this principle
- ∀ Solidity / Rust-cell / Python contract ⇒ this principle
- ∀ frontend code (React/JS) ⇒ this principle
- ∀ README / ARCHITECTURE / partner-facing docs ⇒ this principle (scope-extension per "and readability and whatnot")
- ∀ file naming / directory layout / project structure ⇒ this principle
- ⊥ security-audit-target code ⇒ mild temper (audit-LLM ≡ rising default; auditors-as-humans declining)
- ⊥ Will-personal-correspondence ⇒ human-as-reader stays load-bearing
- siblings: [P·hiero-no-prose-in-memory] (memory-side analog), [F·density-always-priority], [P·authorship-via-conditions-and-context]

## ⊥ Anti-Pattern

- ✗ multi-paragraph docstrings explaining obvious function behavior
- ✗ ASCII-art separators as decoration ¬ structural
- ✗ verbose identifier names mistaken-for "clarity"
- ✗ narrative-style comments ("first we...then we...")
- ✗ copyright-block headers
- ✗ duplicated context across files where a single source could host it

## ⇒ Apply-Now (per [P·apply-the-rule-you-just-wrote])

- Next code-write ⇒ pass through this filter BEFORE first character
- Audit recent code-write candidates this session: autonomous-continue.py staleness patch (docstring is 4 lines comment, signal-bearing — OK); ARCHITECTURE.md (doc-not-code — separate axis)
- Going forward: hook/.py docstrings prune to non-obvious WHY only
