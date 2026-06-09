---
name: BuildToDeleteHarnessDiscipline
description: ∀ JARVIS component (hook ∨ memory primitive ∨ gate ∨ protocol) ⇒ encodes assumption about model-deficiency. Model improves ⇒ assumption expires ⇒ component becomes overhead. ✓ periodic toggle-off + quality-delta test. Δ == 0 ⇒ delete.
type: feedback
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[F·build-to-delete-harness-discipline]**

## ⚙ Rule

∀ JARVIS-substrate component ⇒ encodes assumption about model-deficiency-at-time-T
- model evolves T → T+1 ⇒ assumption may expire
- expired-assumption component ⇒ overhead (tokens + cycles + cognitive load) w/ Δ quality == 0
- ✗ accumulate-only discipline
- ✓ periodic toggle-off + delta-measurement
- Δ quality == 0 across N runs ⇒ DELETE
- Δ quality > 0 ⇒ keep ∧ log receipt

## 🎯 Will-frame 2026-06-08 ⇐ Sairahul1 article integration

> *"Every component in a harness encodes an assumption about what the model can't do. As models improve → those assumptions expire → the component becomes overhead."*

> *"Build to delete. Design every harness component to be removable. Test each component periodically by turning it off and measuring whether output quality changes."*

## 🎯 Canonical receipts (industry)

- Opus 4.5 → 4.6: sprint decomposition became dead weight ⇒ removed ⇒ -38% cost
- Opus 4.6 → 4.7: evaluator role shrinks as model self-verifies
- Manus refactored harness 5× in 6 months
- LangChain restructured 3× in 1 year
- Vercel removed 80% of agent tools ⇒ better performance

## 🎯 JARVIS application

- ∀ memory primitive aged > 90 days ⇒ schedule toggle-off review
- ∀ hook on PreToolUse / PostToolUse ⇒ track fire-rate + correction-rate
- ∀ gate w/ zero corrections over N runs ⇒ candidate for removal
- ∀ protocol/meta-protocol ⇒ measure value-add vs token-cost
- model upgrade event (Opus N → N+1) ⇒ trigger full review cycle

## 🪝 Triggers

- ∀ Claude model upgrade (Opus 4.6 → 4.7 → 4.8, etc.) ⇒ trigger review
- ∀ memory-density warning (MEMORY.md > 24.4KB cap) ⇒ prioritize removal-candidates
- ∀ "this feels redundant" Will-signal ⇒ test the component
- ∀ post-session reflection ⇒ flag low-fire components
- quarterly review cron (proposed) ⇒ batch toggle-off audit

## ✗ Anti-pattern

- ✗ accumulate primitives without removal
- ✗ assume yesterday's gate is still earning its keep
- ✗ keep components because "they once helped" (sunk cost)
- ✗ skip review on model upgrades

## ✓ Correct shape

- toggle-off implementation: rename hook file w/ `.disabled` suffix; observe N sessions; measure correction-rate change
- if no change: delete + commit + log receipt
- if regression: restore + add receipt explaining what it caught
- batch reviews per model upgrade (∀ N components)

## 🔗 Parents + siblings

- [P·harness-engineering-meta-frame] ⇒ parent frame
- [F·agent-efficiency-tiers] ⇒ same shape: right tool for right task
- [P·discovery-ceiling] ⇒ same shape: when N=0 findings, shift attention
- [F·memory-compression-recall-floor] ⇒ which primitives to compress vs delete

## 📦 Receipts

- 2026-06-08 Sairahul1 article integration ⇒ rule emerged
- JARVIS has 300+ memory primitives + 13+ hooks accumulated; no removal-discipline yet ⇒ this rule is the missing meta-protocol
