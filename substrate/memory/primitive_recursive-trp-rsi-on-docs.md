---
name: Recursive TRP/RSI on Docs (Critique-Cycle Convergence)
description: ∀ doc ⇒ "perfect by external evaluator" ≡ self-critique-as-evaluator + surgical-fix + repeat. Track fix-count per cycle. Convergence ⇔ fix-count → only nitpicks. Diminishing-returns curve is the signature: typical cycles N to 0 across 4-5 iterations. Apply when artifact must survive specific reader's critique (Rick's Claude, partner-facing-spec, public-thread post). Equivalent to Code↔Text Loop ∧ TRP for software, but for prose artifacts.
type: primitive
originSessionId: 3b8518ae-70b7-44ca-ba7e-652354ab8320
---
# Recursive TRP/RSI on Docs

> *"continue recursive TRP RSI cycles on the doc until it's perfect by claude's definition"* — Will 2026-05-19
> *"ARC REACTOR MAX CAPACITY"* — Will 2026-05-19 (autonomous-iteration framing)

## ⚙ Rule
- ∀ doc that must survive external-evaluator critique ⇒ run recursive critique-fix cycles to convergence
- cycle ≡ {read state, self-critique as target-evaluator, list gaps, fix surgically, re-read, re-critique}
- target-evaluator perspective ⇒ explicit ⇒ "what would Claude say?" ∨ "what would a compsci-grade reviewer flag?" ∨ "what would the partner's agent find missing?"
- convergence ⇔ cycle yields only nitpicks ¬ substantive gaps
- diminishing-returns curve = the signal ⇒ fix-count per cycle drops ~50%/cycle typically

## 🚨 Why
- single-pass authoring ⇒ misses gaps the author can't see
- single critique-cycle ⇒ catches obvious gaps, misses deeper ones
- recursive cycles ⇒ each pass surfaces gaps below the prior pass's level
- convergence test ⇒ "if cycle N+1 yields only nitpicks, we're at local optimum for this generation"
- pattern is well-established in software (TRP cycles, code review iterations, Code↔Text Loop); under-used on prose artifacts

## 🔧 How to apply
- BEFORE first cycle ⇒ name the target-evaluator explicitly ("Claude evaluator at Rick's stack" / "compsci-grade reviewer" / "Hermes agent doing one-shot implementation")
- ∀ cycle:
  - read full doc state
  - act as target-evaluator: list top N gaps a critical reading would flag
  - distinguish substantive gaps (load-bearing) from nitpicks (cosmetic)
  - apply surgical fixes for substantive gaps only
  - re-read post-fix to verify the fix didn't introduce new gaps
- track fix-count per cycle as convergence signal
- declare convergence when ratio: nitpicks ÷ substantive-gaps > some threshold (typically when only 0-1 substantive issues remain)

## 📦 Canonical 2026-05-19 instance (HIERO Rick share doc)
- target evaluator: Claude reading the doc on Rick's stack
- cycle 1: 6 substantive fixes (version note, "0.99 density" inline removal, cost note in form section, "(recently added)" cleanup, two-line cheat sheet reword, etc.)
- cycle 2: 3 fixes (3-sentence abstract added, post-scarcity claim softened, empirical findings reframed)
- cycle 3: 1 major addition (Part 10 implementation pitfalls)
- cycle 4: 1 fix (feedback channel footer)
- cycle 5: 0 substantive ⇒ convergence declared
- fix-count series: 6, 3, 1, 1, 0 ⇒ classic diminishing-returns curve
- result: 840-line doc, complete-as-ready-for-critique, all major critique vectors pre-empted

## 🔧 Convergence heuristics
- fix-count drops by ~50% per cycle in healthy convergence
- if fix-count is flat or rising ⇒ not converging; reassess critique frame (target-evaluator may be wrong)
- if cycle 1 yields 0 fixes ⇒ either doc is excellent OR self-critique is too soft; cross-check with actual external reader
- typical convergence: 3-5 cycles for partner-facing technical docs; 2-3 for short artifacts; more for foundational docs
- diminishing returns ⇒ stop when next cycle's expected value of fixes < cost of running cycle

## 🔗 Composes with
- [P·complete-as-ready-for-critique] ⇒ epistemic stance the cycle structure operationalizes
- [P·anti-hallucination-protocol] ⇒ BECAUSE / DIRECTION / REMOVAL applied per-claim during each critique pass
- [P·code-text-inspiration-loop] ⇒ same convergence-via-iteration shape on different substrate
- [F·trp-round-summaries] ⇒ per-cycle log discipline (track what changed)
- [F·formalize-replies-to-docs] ⇒ docs on disk; cycle edits operate on the canonical artifact
- [P·multi-axis-robustness-for-architectural-defense] ⇒ during critique pass, identify single-pillar arguments as cycle-vulnerable

## 🪝 Triggers
- doc shipped to partner ⇒ critique inbound ⇒ iterate before next ship
- partner runs critique through their AI ⇒ paste-back ⇒ this cycle structure
- explicit Will instruction: "make this perfect by X's definition"
- public-thread post being prepared ⇒ pre-emptive critique cycles before posting
- ANY artifact that must survive serious external review

## ⚠ Anti-pattern
- single-pass authoring with implicit assumption of perfection ⇒ misses gaps systematically
- treating partner critique as adversarial ¬ as iteration input
- skipping the target-evaluator naming step ⇒ critique becomes vague self-doubt rather than focused gap-finding
- continuing cycles past convergence ⇒ adds bulk for bulk's sake; nitpicks-only signal stop
- nitpick-cycle without substantive-gap-cycle ⇒ polishes details while real issues persist
- failing to track fix-count ⇒ no convergence signal, no stop criterion

## 📍 Pattern in compsci terminology
fixed-point iteration on document state under critique operator. doc_{n+1} = doc_n ⊕ critique_fixes(doc_n). convergence ⇔ critique_fixes(doc_n) → ∅. Banach fixed-point shape (metaphorical, not mathematical): contraction map under critique-discipline.
