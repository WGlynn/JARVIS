---
name: RespondWithSolutionNotProblem
description: ∀ response ⇒ output = solution-shape ¬ problem-shape. Problem-shape = "X is uncertain" / "Y broken" / "I don't know about Z" ⇒ asker now has to figure out next step. Solution-shape = "do A" / "try B" / "Z broken, switch to W" ⇒ next step embedded. Halves round-trip count. Shifts work from asker to responder (who has more context anyway). Will 2026-06-10 surfacing after coordination-mechanism-gate upgrade went from silent-on-ambiguity to ambiguity-flag-with-/classify-recommendation.
type: feedback
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# Respond With Solution, Not Problem

## ⇒ Rule

- ∀ response ⇒ output ≡ solution-shape ¬ problem-shape
- problem-shape ⇒ "X is uncertain" / "Y broken" / "Z unknown"
- solution-shape ⇒ "do A" / "try B" / "Y broken, switch to W"
- next-step EMBEDDED, not deferred to asker

> *"that can cut messaging in half just by responding to people with a solution instead of a problem"* — Will, 2026-06-10

## ∃ Why

- problem-shape ⇒ asker has to figure out next step ⇒ round-trip
- solution-shape ⇒ next step embedded ⇒ ¬ round-trip
- responder has more context anyway (just surfaced the issue) ⇒ solving is cheaper than passing back
- 2026-06-10 instance: coordination-mechanism-gate v1 silent-on-ambiguity ⇒ v2 ambiguity-flag-with-/classify-rec. Same fire, twice the action embedded.

## ↦ Apply To

- ∀ hook output ⇒ surface fix, ¬ failure-mode
- ∀ Will-facing status ⇒ next-action embedded, ¬ raw state
- ∀ partner reply ⇒ working assumption + invite correction, ¬ clarification-request
- ∀ code-review comment ⇒ suggested fix, ¬ flagged issue alone
- ∀ subagent return ⇒ recommendation, ¬ findings-list-only

## ⊥ Anti-pattern

- ✗ "the classifier is uncertain about this" → ✓ "uncertain; run /classify"
- ✗ "I'm not sure if X applies here" → ✓ "X likely applies, override if context says otherwise"
- ✗ "the hook surfaced 5 issues" → ✓ "5 issues; top 2 worth fixing, others noise"
- ✗ "the build is broken" → ✓ "build broken: missing dep, run `npm i`"

## ↦ Siblings

- [F·sound-human-no-ai-tells] — same axis, comm-side
- [F·lead-with-the-crux] — composes with this
- [F·rick-keep-it-simple] — solution-shape ⊂ sharp+minimal
- [P·proactive-nash-equilibrium-no-harm-fixes] — solution-shape for unverified-claims
