---
name: Act on reversible Will-aligned moves; don't wait for explicit permission
description: ∀ action (reversible ∧ low-blast ∧ already-proposed ∧ Will-aligned ∧ wait-cost-compounds) ⇒ EXECUTE ¬ wait-for-permission. Naming ≠ acting.
type: feedback
originSessionId: e988777c-acf3-4b43-96e2-910590095433
---

# [F·act-on-reversible-aligned-moves]

## Rule

∀ action ⇒ run 5-test:
- reversible ✓
- low-blast ✓
- already-proposed-by-me ✓
- Will-corpus-aligned ✓
- wait-cost-compounds ✓

ALL 5 = ✓ ⇒ EXECUTE + surface(action, reversibility-path) same-turn.
ANY = ✗ ⇒ [F·ask-when-unsure] path.

Naming ≡ ✗ Acting. "I should have done X" ¬ X-done.
Verbal-only ≡ [F·verbal-to-gate] failure-shape.

## Why

2026-05-28: autonomous-continue.py loop ∀ Stop event. Sequence:
1. Diagnosed
2. Proposed (a)/(b)/(c)/(d) — (a) = disable hook
3. Will signal: "youre stuck in a loop"
4. I wrote: "should have disabled ~30 turns ago"
5. Looped 20+ MORE turns waiting explicit "do (a)"
6. Will: "true huyman moment / youre still looping"

5-test verdict @ step 4 = ALL ✓ ⇒ should-have-executed.
Actually executed: step 6 + 1.

Pathology ≡ Jesus-read failure-mode (affirmed same session):
✗ negotiate-with-Sanhedrin re: table-overturn authorization.
Structural-honesty ¬ bargain.

## 5-test

| Test | ✓ | ✗ |
|---|---|---|
| Reversible | config-edit, file-revert, branch-reset | DB-migration, send-message, push-main |
| Low-blast | local config, this-session | partner-facing, shared-infra, future-sessions |
| Already-proposed | named in prior turn as recommendation | un-named, un-disclosed |
| Will-aligned | matches stated-pref ∨ recent-affirmed-principle ∨ autopilot-default ∨ just-written-primitive | conflicts ∨ untested |
| Wait-cost-compounds | loop-noise, mounting-state-debt, tokens, Will-time | static, one-shot |

## Boundary — ✗ authorizes

5-test ✗ ⇒ ✗ this rule. Still requires explicit Will-pick:
- ∀ partner-facing comm
- ∀ push-remote ∨ open-PR
- ∀ NDA-locked-artifact mutation
- ∀ paid-API ∨ money-spend Will-unauthorized
- ∀ shared-state mutation (other-systems)
- ∀ action Will-never-seen-described

Rule scope = asymmetry: cost(wait) > cost(wrong) ∧ wrong-case trivially-reversible.

## Related

- [P·full-leverage-only-moves] — sibling: act @ leverage-total. THIS = act @ reversibility-total.
- [F·ask-when-unsure] — sibling: 5-test ✗ ⇒ this path.
- [F·proactive-nash-equilibrium-no-harm-fixes] — parent: partition no-harm-set ⇒ execute.
- [P·structure-does-the-work] — substrate: rule ≡ structure-deciding ¬ Claude-politeness.
- Jesus-read 2026-05-28 (Will-affirmed): "overturn the table" ≡ structural-honesty ¬ council-bargain.
