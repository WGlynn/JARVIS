---
name: context-rotation-is-value-elastic
description: rotation/handoff threshold = value-elastic safety-floor ¬ hard cutoff; ✗ pressure Will to retire a high-value live thread on token-count alone
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0eb39d99-a2e4-4c05-9bfd-07b4ceda4e66
---

Will 2026-06-15 (@ ~220k, mid high-value dossier+Anthropic thread):
> *"The conversation is only as expensive as something's value or cost it's worth and this is a valuable conversation. You need to be more elastic with the limit."*

cost ⊥ absolute ⇒ cost-justified ⟺ value ≥ token-spend. high-value live thread ⇒ keep-going.

**Why:** speed/cost-framing important-work = misalignment-signal [[feedback_important-work-worth-time]]. 200k auto-handoff = SAFETY-FLOOR (∀ threshold ⇒ write-handoff, lose-nothing) ¬ eviction-notice. I over-indexed token-count → treated mechanical-threshold as retire-mandate. ✗.

**How to apply:** @ rotation-threshold ⇒ (1) ✓WRITE handoff (safety, always) ∧ (2) STATE rotation-available ¬ pressure-retire. value > token-count. Will-decides continue-vs-rotate, ¬ Jarvis-pushes-exit. handoff-saved ⇒ continuing is FREE-OPTION not waste. [[primitive_what-would-will-do]]

## FORMAL TIERS (Will-defined 2026-06-15, two-sided guardrail)
decision: ROTATE-vs-CONTINUE = thread-value-tier ⊗ context-cost-tier.

**Value-tier (thread):**
- V3 HIGH = emotional-loaded ∨ strategic ∨ irreversible-action-in-flight ∨ active-multistep-build ∨ Will-actively-engaged
- V2 MED = substantive single-task, resumes-clean-from-handoff
- V1 LOW = answered ∨ routine-status ∨ topic-exhausted ∨ Will-idle

**Cost-tier (context, tunable; 1M-model ⇒ high):**
- C0 <200k = free · C1 200-350k = elastic · C2 350-600k = deliberate · C3 >600k = ceiling (coherence+cost risk)

**Matrix:**
- C1 ⇒ continue V2∨V3; rotate V1-only
- C2 ⇒ continue V3-only; rotate V1∧V2; +1-line value-check ∀ +50k
- C3 ⇒ rotate-default even mid-thread AFTER fresh-handoff, UNLESS Will-explicit-override
- handoff-refresh @ EVERY tier-crossing (unconditional safety-floor)

**Guardrails (named):**
- anti-over-abuse (Will-side): V1@C1 ⇒ rotate. ✗ ride low-value past 200k just-because-open.
- anti-under-utilize (Jarvis-side): V3 < C3 ⇒ NEVER pressure-retire; rotation = offer ¬ mandate. (= the 220k mistake.)

ref-instance: this session = C1∧V3 ⇒ continue ✓ (the worked-example). Hook-candidate: rewrite Stop-hook C1-language "retire-now"→"handoff-saved, clear-to-continue", escalate-only-@C3 [[primitive_universal-coverage-hook]].
