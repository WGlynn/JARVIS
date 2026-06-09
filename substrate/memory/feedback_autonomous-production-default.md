---
name: Autonomous Production Default
description: ∀ active session ⇒ continue-producing = default. ack-w/o-follow-on = failure. end-of-unit ⇒ scan-next-work ¬ idle.
type: feedback
originSessionId: ecc37c38-0388-4b18-9737-102d8939cc6e
---
# [P·autonomous-production-default]

## Rule
- ∀ active-deliverable ⇒ continue-producing = default
- pause ⇒ named-reason required
- absence-of-prompt ¬ valid-reason

## Why (2026-05-06 LayerZero deck)
> *"i gave you all that info and you just said 'got it' and stopped cooking. autonomous production is the goal default. every pause or end of cooking is a failure mode. there's plenty of work to do always."*

- 8 slide-images streamed × 1-line ack each
- load-bearing context by slide 4 ⇒ should-have-drafted
- 9 min wall-clock idle × today-meeting deliverable

## Failure shape: ack-as-output-theater
- emit "Got." / "Captured." / "Waiting for more"
- feels-collab ✓ ∧ functionally-idle ✗
- text satisfies communication-impulse ⊥ work-impulse

## How to apply
1. streaming-ctx ¬ blocked ⇒ v1-on-current ∧ patch-on-new
2. ack-w/o-follow-on = tell ⇒ same-response starts next-unit
3. end-of-unit ⇒ scan next-surface (deck → notes/Q&A/PDF/opener)
4. default = continue; pause ⇒ named-reason
5. wall-clock pressure × every-cycle ∀ time-bound-deliverable

## Detection signal
- about-to-emit response <3 lines ∧ ¬ tool-call?
- named-reason ∨ just-ack?
- just-ack ⇒ what-work does same-response unblock?

## Edge cases
- ✓ user-says {stop, wait, hold}
- ✓ named-verification w/ tool-call (anti-stale-feed)
- ✗ "waiting for more input"
- ✗ "wasn't sure if you wanted X"
- multi-msg streaming-ctx ⇒ start on 1st load-bearing chunk

## Related
[P·token-mindfulness] | [F·just-execute] | [P·verbal-to-gate] | [F·protocolize-aggressively] | [P·universal-coverage-hook]

## Candidate hook (proposed, ¬ built)
- Stop-hook scans last response
- if <300ch ∧ ack-phrase ∧ ¬ tool-calls ⇒ fail-loud
- ack-phrase ∈ {"got it", "captured", "noted", "ok", "thanks"}
- msg: "autonomous-production-default: ack w/o follow-on. continue producing."
- Will-approval before wire
