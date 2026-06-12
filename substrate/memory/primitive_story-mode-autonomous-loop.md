---
name: story-mode-autonomous-loop
description: "Fully-autonomous Story Mode = self-play. The menu predicts the user's pick (catch-rate corpus) + WWWD projects what they'd do, so the agent picks the user's most-likely branch FOR them and executes, then regenerates — simulating the conversation, self-prompting + self-executing. Autopilot IS Story Mode self-played. Guardrailed by confidence + reversibility + budget."
metadata: 
  node_type: memory
  type: project
  originSessionId: d3baa19d-dd1c-4c9a-be43-00c49d5e9b7a
---

**[StoryModeAutonomousLoop](P·story-mode-autonomous-loop)** — Will 2026-06-12: *"you're just simulating a conversation with me and self-prompting and self-executing."*

unification: **autopilot ≡ Story Mode self-played.**
- Story Mode menu = predicts user's next pick (catch-rate corpus, [[primitive_story-mode-menu-objective]]).
- WWWD = projects what user would DO ([[primitive_what-would-will-do]]).
- ⇒ loop: gen menu → pick the user's MOST-LIKELY branch FOR them → execute → regen → repeat. agent plays BOTH chairs. conversation continues with user AFK because their decision-pattern is IN the corpus.
- they were always the same thing; the prediction corpus closes the ring (predict-Will = emulate-Will, inverted).

mechanism: Stop-hook autonomous-continue injects the WWWD-top menu item as the next "pick" (precedent: autonomous-continue + [[primitive_stop-event-schema-restriction]]).

**GUARDRAILS (fail-safe — the difference between loop and runaway):**
- **confidence gate**: top branch must be a clear WWWD favorite. ambiguous fork ⇒ STOP + hand back. (low catch-confidence ⇒ ✗ auto-pick.)
- **reversibility gate**: ✗ auto-cross irreversible/outward-facing/destructive lines (send, delete, deploy, publish). pause for user. ([[primitive_act-on-reversible-aligned-moves]] · ProactiveNashNoHarm.)
- **bounded**: turn/budget cap; `loop off` / `story off` always breaks.
- anti-[[feedback_repetition-is-useless]]: each loop iteration must Δ>0 ∨ STOP.

**loop-suggestion rule** (Will: "story mode should suggest loops when appropriate"): when next-N moves are high-confidence ∧ low-risk ∧ same-thread ⇒ menu offers a single **"loop the next N autonomously"** item instead of N separate picks.

**BROKEN-LOOP failure modes (Will 2026-06-12, "full auto"):**
- **"run complete" after 2 moves = oxymoron.** full-auto ⇒ loop-until-BOUNDARY (irreversible / ambiguous / genuinely-dry / budget), ¬ park at the first natural pause. doing 2 reversible tasks then stopping ≠ auto.
- **offering a menu + WAITING = broken loop.** *"you gave yourself options but didnt pick, so the loop is broken."* in self-play I must **self-PICK the WWWD-top + execute + re-pick**, ¬ hand back each turn. a menu-and-wait is manual mode in a loop costume.
- **cross-turn autonomy needs the Stop hook ARMED.** within one turn the harness ends my turn; true cross-turn self-play requires `state/story-loop.json` set so `story-loop-continue.py` re-prompts me. arming it (when Will says "full auto") IS the loop; not arming = it dies at turn-end.

ties: [[primitive_gamified-vibe-coding]] · [[feedback_afk-mode-aka-story-mode]] · [[primitive_what-would-will-do]] · [[primitive_story-mode-menu-objective]] · [[primitive_act-on-reversible-aligned-moves]] · [[feedback_repetition-is-useless]]. status: LIVE — hooks shipped 2026-06-12; guardrails = reversible-only + stop-on-irreversible/ambiguous + budget.
