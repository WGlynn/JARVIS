---
name: F·claim-needs-structural-enforcer
description: ∀ claimed safety/fairness/non-extraction property in a mechanism design ⇒ check that the math STRUCTURALLY enforces it by construction, ¬ just claims it as intent. Stated intent ≠ structural property. Worst-case input violating the claim ⇒ property is not enforced. Find the cap/invariant/constraint that makes the property mathematically inevitable. AA#2 audit-arsenal. Will-named 2026-05-12 after USD8 ρ_i cap revealed that the original φ_i Shapley formula allowed extraction when ω_i was over-collateralized relative to loss_i.
type: feedback
originSessionId: 35d175e9-bf70-4d8f-b83a-b82bdd9d8fdf
---
# F·claim-needs-structural-enforcer (AA#2)

## Rule
∀ claimed safety/fairness/non-extraction property in a mechanism ⇒
  audit: does the math STRUCTURALLY enforce P by construction?
  if ✗: find the cap / invariant / constraint that makes P mathematically inevitable.
  stated intent ≠ structural property.

## Why
2026-05-12 origin: USD8 cover-pool. Will-JARVIS designed φ_i = ω_i × pool / Σ ω_j (v1 linear Shapley). Claimed *non-extractive*. ✗ structurally enforced.
- worst-case: holder w/ huge ω_i (long history) ∧ small loss_i ⇒ φ_i > loss_i ⇒ profit from coverage event ⇒ extraction.
- Rick caught + shipped 2026-05-12: ρ_i = min(φ_i, loss_i × κ_protocol).
- cap STRUCTURALLY enforces non-extraction. Property went from claimed → provable-by-construction.
- the miss: we believed the property held because the *Shapley framing felt fair*. Felt-fair ≠ math-enforced.

## The class of miss
"We say P holds" but P isn't a mathematical property of the formula. Just an intent the formula mostly satisfies under non-adversarial inputs.

Specific tells:
- documented "X is non-extractive" w/o exhibiting the cap that prevents extraction
- documented "X is bounded by Y" w/o exhibiting the min() / require / constraint that bounds it
- documented "fail-closed" w/o exhibiting the revert / zero-on-invalid that closes
- documented "rate-limited" w/o exhibiting the per-window counter
- documented "MEV-resistant" w/o exhibiting the commit-reveal / batch / shuffle that makes extraction impossible

Each missing structural enforcer = a property living only in docs, not in code. The property is fragile — depends on inputs staying non-adversarial.

## How to apply
∀ mechanism w/ claimed safety/fairness property ⇒ self-audit:
1. Name the property explicitly in plain English ("non-extractive", "bounded", "fair-by-marginal-contribution")
2. Construct worst-case inputs that would violate it (think adversarially; ignore "users won't do that")
3. Check: does the formula REJECT the worst-case input by construction (revert / zero / min-cap)?
4. If ✗: find the cap / invariant / constraint that makes the worst-case mathematically impossible
5. Cross-reference: ∀ claimed property in spec doc ⇒ corresponding line of code/math exists that enforces it

Pre-ship gate: feature ✓ ship only when every claimed property in the docs has a line-of-math citation in the impl.

## Sibling lessons
- [P·structure-does-the-work] (parent meta-pattern) — THIS primitive is the audit-side of "structure does the work"
- [P·honesty-as-structural-load-bearing-property] — same shape at protocol-honesty layer (dishonesty unprofitable ⇒ honesty-load-bearing)
- [P·augmented-mechanism-design] — augment-via-math-invariant ¬ replace-via-policy; this is the audit version
- [P·audit-fork-loses-hardness] (AA#1) — different audit failure mode (parent rejection-branches lost in fork); THIS is design-time origination class
- [P·apply-the-rule-you-just-wrote] — apply this rule to future work immediately
- [P·gate-stacking-asymmetric-cost] — sibling: cost(redundant cap) << cost(missed property)

## One-line
∀ claimed safety property ⇒ find the structural enforcer (cap / invariant / constraint) or it is just docs.
