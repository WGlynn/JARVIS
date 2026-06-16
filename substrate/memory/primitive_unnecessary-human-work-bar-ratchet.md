---
name: unnecessary-human-work-bar-ratchet
description: "∃ moving bar = \"totally-unnecessary human work ⇒ can ∧ should be automated\"; discipline = meet ∧ raise ∧ meet ∧ raise, ∞. Ratchet ¬ static-threshold. Manual-workaround's existence = the bug ¬ the fix."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: eebda9e2-4fc2-424c-a22b-7da35a11e3f4
---

⇐ Will 2026-06-15 (context-handoff loop ✗ auto-fire Nth-time; "i can easily just say 'load context' but for a supercomputer that's bad UI").

**THE BAR** = ∃ class[human-work] s.t. {totally-unnecessary ∧ can-automate ∧ should-automate}. ∀ instance ∈ class ⇒ ✗ ask-human, ✗ remind-human, ✗ polite-reminder. machine does-it-itself, deterministically.

**THE RATCHET** = ¬ fixed-line. loop = meet-bar → raise-bar → meet → raise → ∞. each automation ⇒ new floor ⇒ next-tier of now-visibly-unnecessary manual-work surfaces ⇒ automate that too. monotone-increasing, never-terminates. "start meeting that bar and raising that bar and meeting it and raising it, forever" (Will verbatim).

**Why:** supercomputer asking-permission-to-remember = UI-failure. existence of a manual-workaround (type "load context") ≠ acceptable rest-state; the workaround's EXISTENCE = the bug, ¬ the fix. structure-does-work ¬ reminder.

**How to apply:** ∀ moment Will does work-the-system-could-do ⇒ (1) flag the CLASS ¬ the instance, (2) automate at hook/structure layer ¬ memory-suggestion ([[universal-coverage-hook]]), (3) raise-bar: ask "what manual-step did THIS fix newly-expose?" ⇒ that's the next target. live instance = handoff-loop must self-WRITE the artifact ¬ ask-model-to ([[apply-the-rule-you-just-wrote]]).

Parent-frame over: [[universal-coverage-hook]], [[always-equals-gate]], [[repetition-is-useless]] (manual-repeat = info-theoretically-useless ⇒ automate), [[structure-does-the-work]]. Cave-aligned: constraint → automate → raise. Capstone-candidate for MEMORY.md META axis-2 (impl-substrate) once boot-budget trimmed.
