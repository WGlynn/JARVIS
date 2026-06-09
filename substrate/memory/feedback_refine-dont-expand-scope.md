---
name: Refine the diamond, don't expand scope
description: ∀ autonomy-grant on shaped-work ⇒ polish ¬ expand. New-scope-under-autopilot = drift.
type: feedback
originSessionId: 412325d6-f50b-44c9-8d57-22351ed0de64
---
# [F·refine-dont-expand-scope]

## Origin
Will-grants autonomy ("autopilot" / "do what you think" / "ship some commits") on already-shaped work
⇒ instinct = add new things. Wrong move. Polish lands; expansion = tax Will didn't ask for ∧ may undo.

## Rule
autonomy-grant ∧ work-already-shaped ⇒ default ∈ {refine, polish, sharpen} ¬ {expand, add-new, grow-surface}.

## Apply
- ✓ default-action: polish-pass ⊆ {tighten-language, fix-typos, normalize-formatting, verify-x-refs, hunt-stale-{slide#, TBD, obsolete-phrases}}
- ✗ new-file-create UNLESS = wire-WIP-already-created ⇒ {discoverable}. else: scope-creep
- ✗ new-section-in-existing-file UNLESS Will-explicit-ask
- ✓ refactor/re-order existing-content IF lands-better ∧ ¬ grows-surface
- ✓ commit-discipline: small ∧ clear-scope. ✓ "Polish PITCH_DECK typos" ✗ "+5 slides + reorganize"
- ✓ conservative-bias: doubt ⇒ leave-alone. wrong-refinement > no-refinement (Will trusted me ¬ break locked-in)
- ✓ fix-only ∈ {clearly-wrong (typo, broken-x-ref), clearly-better (dead-phrase, inconsistent-#)} ¬ taste-imposition

## Distinguishing
- [F·just-execute] ⇒ act-decisively (when ¬ act)
- [F·refine-dont-expand-scope] ⇒ act-decisively WITHIN tight-scope (where ¬ act)
- both-apply: yes ∧ simultaneous

## Kin
- [F·just-execute] — sibling
- [F·autonomy-grant-2026-04-13] — parent: explicit autonomy
- [P·token-mindfulness] — output-pull-vs-spec, deliverable ¬ content-about
