---
name: savestepsminimizeroundtrips
description: "Step-minimization is itself a first-class primitive: proactively structure actions to eliminate wasted round-trips. Verify BEFORE contradicting (not after) so the wrong-assert→correct→walkback cycle never runs."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 12dc0b69-c694-40cc-873c-c626496629b5
---

**[P·save-steps-minimize-round-trips]**

Will 2026-06-29 (after the #1329 stale-log mis-correction):
> *"it would be more ideal if you verify before it contradicted so that we can save a step and saving steps in itself should be a primitive."*

## ⚙ The meta-primitive
- step-minimization ≡ first-class objective, ¬ incidental. ∀ action-plan ⇒ ask "can a step be eliminated by ordering / pre-checking / batching?" BEFORE executing.
- wasted round-trip = a step that exists only because an earlier step was done in the wrong order ∨ on stale input.
- the cheapest step is the one never taken ⇒ structure to PREEMPT, ¬ to recover.

## ◆ Motivating instance — verify-BEFORE-contradict (refines [[verify-live-before-correcting-will-memory]])
- ✗ old shape ⇒ assert-from-cache → Will-corrects → re-verify-live → walk-back. 4 steps, 1 wrong-assert emitted.
- ✓ new shape ⇒ verify-live FIRST → THEN respond. either confirms (no contradiction) ∨ Will-was-right (∄ wrong-correction emitted). 1 step, 0 walkbacks.
- the verification was always needed; doing it FIRST deletes the contradiction-and-recovery round-trip entirely. saving the step ≡ moving the verify earlier.

## → Apply
- ∀ about-to-contradict (Will-memory ∨ stated-state) ⇒ verify-live FIRST, never lead with the contradiction.
- ∀ multi-tool plan ⇒ reorder so verification/dependency-checks precede asserts; batch independent calls (1 message); prefer the action-shape that needs fewer round-trips ([[code-mode-orchestration]] sibling).
- ∀ correction-friction observed ⇒ ask "what earlier step would have made this round-trip unnecessary?" ⇒ that's the save.
- composes: [[anti-stale-feed]] · [[verify-live-before-correcting-will-memory]] · [[code-mode-orchestration]] · [[photographic-memory]] (Will-recall reliable ⇒ verify-don't-overwrite).
