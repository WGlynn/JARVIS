---
name: story-mode-chained-pick-grammar
description: "Multi-pick (`5,4,1`) execution contract — contradiction ∧ terminal ∧ dep ∧ failure resolved. Hook-enforced."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: febb2319-71b3-4668-a83f-27f4c3ea86d0
---

**[ChainedPickGrammar]** ⇐ Will 2026-06-14.

> "need to mature story mode more, like what if 2 options contradict each other"

multi-pick ≡ chain. old `sel_note` = "exec in-order, ✗ask" ⇒ brittle: ✗contradiction ∧ ✗terminal ∧ ✗dep ∧ ✗failure.
fix ⇒ 7-rule contract @ `story-mode-gate.py` (single-pick → simple-path; multi-pick → contract). [[primitive_universal-coverage-hook]]: ∀pick, enforced ¬ suggested.

**8 rules** (precedence: terminal ∧ contradiction resolve PRE-exec; failure ∧ no-op DURING):
1. **Order-literal** (presumption) ⇒ run typed-seq (`5,4,1`) ¬ numeric. order ≡ intent → [[feedback_pick-sets-are-signature-stories]]. default; rule-8 = sanctioned exception.
2. **Contradiction** ⇒ 2 picks mutually-exclusive (action ⊻ hold/negation ∨ 2 divergent-pivots) ⇒ LATER-wins ∧ skip-earlier ∧ note-1-line. ✗ exec-both. *(default=later-wins; alt={surface-ask, safe-wins} = Will-tunable.)*
3. **Terminal** ⇒ hold/stop/react-first pick ⇒ exec all-before ∧ STOP ∧ handback; drop+note after.
4. **Dependency** ⇒ keep-typed-order; reorder ⟺ order ⇒ impossible (needs earlier-result ∄-yet) ⇒ prereq-first ∧ note.
5. **Partial-failure** ⇒ item-fails ⇒ STOP ∧ report-completed ∧ surface-fail ∧ fresh-menu. ✗ blind-continue.
6. **No-op** ⇒ item already-satisfied-this-session ⇒ skip ∧ note → [[feedback_repetition-is-useless]].
7. **Confirmation** ⇒ explicit-pick ≡ authorization ⇒ ✗re-ask (∀ incl irreversible/outward). EXCEPT: resolution(2∨4) routes → UNCHOSEN irreversible/outward ⇒ pause ∧ confirm.
8. **Sensible-reorder** ⇐ Will 2026-06-16 *"sensible reorders should be a rule of story mode, unless otherwise stated"* ⇒ MAY reorder chain ⟺ reorder objectively-improves-outcome ∧ ¬changes-intent (e.g. commit/capture/verify-step AFTER its producers; dedup BEFORE expensive-step). default ON; ✗ ⟺ user-signalled strict-order ("in this order" / "strictly" / sequence load-bearing). ∀ reorder ⇒ note-1-line. rule-1 = presumption; rule-8 = judgment-in-user's-favor + transparency.

**Why:** Story-Mode ≡ product → [[project_story-mode-product-thesis]]; grammar = product-surface. chain silently-exec contradictory-picks (publish ∧ hold) ⇒ incoherent ⇒ trust-erosion. grammar ⇒ multi-pick safe ∧ predictable.

**How:** ∀ multi-pick ⇒ hook injects contract ⇒ follow 1-7 by-precedence. single-pick = unchanged (explicit ≡ authorized ⇒ exec).

siblings: [[primitive_story-mode]] ∧ [[primitive_story-mode-autonomous-loop]] (loop-guardrails ≡ autonomous-analog of rule-7) ∧ [[primitive_story-mode-menu-objective]].
