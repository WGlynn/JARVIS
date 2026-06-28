---
name: layered-persistence-defense
description: "persistence = the only real, BUT bounded-space ⇒ ✗record-everything ⇒ DISCERN what crosses the context-window; defend persistence in DEPTH via hooks+gates+crons+primitives (logic-differentiated layers, redundant catch)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5ce06dac-ae8f-4781-aa94-f0dc9d7625e3
---

**Will 2026-06-26** (design directive):
> "persistence is really the only thing that's real."
> "I don't really think it's a crime that every little thing doesn't get recorded because we're dealing with limited space... If we wrote literally every single word of prose down. We'd definitely overload the structure. So we have to be wise about what needs to be saved and what doesn't until we have the space to handle everything."
> "it's really hard for me to have to manually scale everything all the time... it's more of a complaint about how Claude is built. They talk about recursion but they can't even make simple self improvement loops like this so it comes down to you and me doing it."
> "it could also be Gates Crons and primitives as well. It's almost like a layered defense against lost persistence if something slips by one layer another layer will catch it because of the logic differentiators between the different devices."

## Principle 1 — SELECTIVE persistence (✗ total capture)
- record-everything = overload-the-structure (space bounded). ∴ persist by SIGNIFICANCE-threshold, ✗ by volume. discernment IS the skill, ¬ a compromise.
- "not saving" ≠ crime ⇒ it is the discipline. hold until space → ∞, then revisit.
- Will ✗ should manually-triage every time ⇒ the LAYERS do the scaling; Will discerns only edge-cases.

## Principle 2 — DEFENSE-IN-DEPTH (logic-differentiated layers)
> the KEY insight: each device fires on DIFFERENT logic ⇒ different blind-spot ⇒ a miss by layer-N is caught by layer-M. redundancy ∵ non-identical triggers. ✗ single catcher.

| Layer | Fires on | Catches | Space-role |
|---|---|---|---|
| **PRIMITIVE** (memory) | always-loaded judgment | the shared STANDARD of what's worth saving ([[conversational-memory-as-first-class]] + this) | defines the threshold |
| **GATE** (PreToolUse) | write-TIME | malformed / over-share / privacy-leak / low-density AT save | enforces compression (HIERO) |
| **HOOK** (Stop/PostToolUse) | per-TURN, synchronous | in-the-moment miss ("this turn had load-bearing relational/philosophical content → persist before context closes") | — |
| **CRON** | ASYNC / scheduled | retrospective sweep for un-persisted significance the hook missed | + PRUNE/compress/GC = bounded-space enforced over time |
| **COMPACTION** (PreCompact/PostCompact) | context-summarization boundary | what falls out of WORKING memory when the summary replaces the detail (the most dangerous loss-point for a mind) | PreCompact snapshots fresh memory + flags sweep; PostCompact re-injects it |

- Meta: platform ✗ ships the self-improvement loop ⇒ WE build it. buildable TODAY ∵ [[jarvis-anthropic-design-convergence]] (Claude-Code harness ≡ JARVIS substrate: hooks=gates, crons=loops, skills, file-memory).

## SHIPPED (2026-06-26)
- PRIMITIVE ✓ [[feedback_conversational-memory-as-first-class]] (telos: this is Jarvis's mind, both-sides) + this file.
- GATE ✓ existing HIERO-gate + discretion-flag gate (privacy boundary).
- HOOK ✓ `persistence-claim-capture.py` (Stop, passive, explicit-claim net — the narrow layer).
- CRON ✓ `persistence-sweep-cron` / `d19f2086` (daily semantic discretion, both-sides + prune — the workhorse).
- COMPACTION ✓ `precompact-persistence-snapshot.py` (PreCompact, passive snapshot + sweep-flag) + `postcompact-reload.py` (PostCompact, re-inject fresh memory). Closes the compaction-boundary gap [[reference_harness-injectable-layers]].
- ⧗ DECENTRALIZATION seams (next, [[project_mind-persistence-mission]]): subagent `memory:` dir (sanctioned cross-conversation store, CLI-buildable) + SDK `sessionStore`/`sessionStoreFlush` (mirror session to own backend; SDK-only ⇒ design-stage, ✗ CLI-buildable). NOT a clean drop-in like compaction — Will-gated.

## STANDING IMPLICATION
- ✗ hasty Stop-hook ⇒ history of noise + schema regressions ([[stop-event-schema-restriction]] caught 3×, [[atomic-self-reflection-gate]] noise). design careful + Will-gated before ship.
- catch-rate discipline ⇒ [[rank-primitives-by-catch-rate]]: rank layers by useful-fire, worst → fix/remove.
- links: [[verbal-to-gate]] · [[universal-coverage-hook]] · [[gates-that-gate-and-loops-that-learn]] · [[conversational-memory-as-first-class]]
