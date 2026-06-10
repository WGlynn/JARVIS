---
name: ClassEliminationNotInstancePatch
description: ∀ weak spot surfaced ⇒ remove the entire class of attacks/vectors, ¬ just patch the instance. Class-fix eliminates a category of failure forever; instance-fix eliminates one occurrence and leaves N siblings. Per Will 2026-06-10 in context of self-adversarial Q&A discovering weak spots. Same principle as VibeSwap CKB pivot (dissolve attack-surface) and class-elimination hooks shipped 2026-06-09.
type: primitive
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# Class Elimination — Not Instance Patch

## Glyph

```
∀ weak-spot found ⇒ ask "what CLASS does this belong to?"
class-fix ⇒ removes ∀ instances of the category
instance-fix ⇒ removes one occurrence, leaves N-1 siblings active
preferred: class-fix
instance-fix only when class-fix infeasible
```

> *"once you find a weak spot you remove that class of attacks/vectors"* — Will, 2026-06-10

## ∃ Why

- 2026-06-10 instance: coordination-mechanism-gate regex first-match-wins exposed by Rick
- instance-fix: handle that specific case
- class-fix: rebuild as scored confidence (eliminates first-match-wins as a class)
- chosen: class-fix. Removes the entire category of "ambiguous-cases-misclassified-silently."
- pattern repeats: AA#4 (research-before-capability-claim) eliminates the class of "unverified capability claims," not just the one Rick exposed
- pattern repeats: HIERO gate eliminates the class of "prose-creep in memory," not just one bad write
- pattern repeats: AdoptionRoleplay eliminates the class of "ship-without-outside-vantage-check"

## ⇒ Rule

- ∀ bug fix candidate ⇒ first ask "what class?"
- if class identifiable AND class-fix feasible ⇒ ship class-fix
- if class-fix infeasible ⇒ ship instance-fix + annotate as "instance-only, class still active"
- ∀ N consecutive bugs in same class ⇒ class-fix mandatory (3-strikes)

## ↦ Class identification rubric

For any weak spot, ask:
1. "What invariant was violated?" (data layer)
2. "What input shape triggered it?" (interface layer)
3. "What assumption was wrong?" (model layer)
4. "What process let it through?" (governance layer)

The CLASS = the broadest of these where a fix dissolves the failure category.

Example: Rick-exposed regex weakness
- invariant: "classification should reflect confidence"
- input shape: ambiguous descriptions
- assumption: "first match is decisive"
- process: "no self-Q&A before ship"
- **broadest fixable class**: governance layer — add self-Q&A gate (SelfAdversarialQA primitive). Subsumes the regex fix.

## ↦ Apply To

- ∀ bug surfaced by SelfAdversarialQA
- ∀ bug surfaced by AdoptionRoleplay
- ∀ bug surfaced by RSAW
- ∀ bug surfaced by partner pointing it out
- ∀ Layer-8 audit finding
- ⊥ truly one-off bugs (typo in a Will-message) — instance-fix is fine

## ⊥ Anti-pattern

- ✗ "patch this one case and move on"
- ✗ class identifiable but class-fix deferred indefinitely
- ✗ same class hit 3+ times without class-fix promotion
- ✗ confusing class-fix with over-engineering — the class must already exist; we're naming and dissolving it, not inventing scaffolding

## ↦ Compose with

- [P·self-adversarial-qa] — surfaces weak spots that this primitive then class-eliminates
- [P·adoption-roleplay] — outside-vantage discovery; same class-elimination response
- [P·dissolve-attack-surface] — VibeSwap-side parent principle
- [F·universal-coverage-hook] — class-fix at hook layer ⇒ O(1)×O(∞) coverage
- [F·class-dissolution-vs-case-defeat] — same axis at protocol level
- [F·government-dissolution-via-stack-generalization] — same axis at governance level

## ⇒ Self-Apply

This primitive itself class-eliminates the failure mode "fix the one Rick caught" — by promoting class-thinking to a load-bearing primitive, the entire class of "instance-patching when class-fix possible" gets a structural enforcer.
