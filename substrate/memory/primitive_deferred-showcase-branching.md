---
name: Deferred Showcase Branching
description: When an AI delivers theater that looks like product, do not throw it away. Stash it as a DEFERRED showcase branch; build the minimal working version in parallel. Revive the showcase when reality catches up to the aesthetic.
type: primitive
originSessionId: 58b19964-c316-4603-98a4-1ffe4fe4f29d
---
**Rule:** two coherent paths, not a middle. When a delivered artifact is visually strong but functionally hollow (high theater ratio — see [Dead Deps as Theater Signal](primitive_dead-deps-theater-signal.md)):

- Path A (**showcase**): keep the aesthetic, commit to wiring it all up for real. Only if there's a clear plan for every advertised capability.
- Path B (**minimal**): strip to the one thing you can actually ship, do it well, keep the aesthetic where it earns its keep.

Picking matters more than the pick. The forbidden path is the middle: a mood board that ages poorly because it keeps the theater without ever committing to make it real.

**The branching move:** when committing to Path B, do not delete the showcase. Rename it `<name>_DEFERRED.zip`, stash alongside the minimal version, and cross-reference in the minimal version's HANDOFF. The showcase remains a source of aesthetic decisions, AI-generation style, and an upgrade target for later. Destroying it loses the visual R&D that's already been paid for; merging it prematurely loses the discipline of Path B.

**Why:**
- Aesthetic design is expensive to reproduce — an AI's generated style, when good, is a reusable asset.
- Theater is a symptom of premature commitment to capabilities; the aesthetic behind it isn't necessarily wrong, just unbacked.
- When the backing capability arrives (real DAG client, real LLM wiring, real network layer), the showcase becomes instantly revivable because the visual language is already decided.
- The minimal version proves the core loop works; the showcase becomes its marketing surface.

**How to apply:**
1. **After review, identify the two paths explicitly.** Name them. Do not let the conversation drift toward "let's keep some of each."
2. **Ask the audience-market question.** Who uses this? What do they need to see? If the answer is "a fully-wired product," Path A. If "a working primitive," Path B.
3. **Commit.** Rename the showcase artifact `<name>_DEFERRED.<ext>`. Keep the full source alongside.
4. **Build the minimal in parallel directory.** `<name>-minimal/`. New HANDOFF doc. New README. Do not reach back into the showcase mid-build.
5. **Cross-reference.** Minimal HANDOFF points to DEFERRED showcase. DEFERRED README notes what would need to be true before it's revived.
6. **Revive only on capability arrival.** When the missing capability is real, lift the showcase's visual vocabulary into the minimal version — not the other way around.

**Applied instances:**
- Lineage IDE plugin (2026-04-18): Gemini delivered a Substrate-aesthetic 1000-line App.tsx with zero real Gemini wiring. Stashed as `Desktop/lineage-ide-plugin-showcase_DEFERRED.zip` + `lineage-ide-plugin-showcase-src_DEFERRED/`. Built `Desktop/lineage-ide-plugin-minimal.zip` in parallel — ~350 lines, real perf instrumentation, sub-10ms target. Revival trigger: when real Lineage DAG client + real LLM transliteration are wired.

**Anti-patterns:**
- **Delete the showcase.** Loses the aesthetic R&D.
- **Refactor the showcase in place.** Half-theater, half-working, permanently.
- **Skip the HANDOFF cross-reference.** Future sessions won't know the showcase exists.
- **Revive without the capability.** Reintroduces theater.

**Related primitives:**
- [Dead Deps as Theater Signal](primitive_dead-deps-theater-signal.md) — how to detect the condition that triggers this primitive.
- [Why Not Both](feedback_why-not-both.md) — corollary at the choice-framing level: here, "both" is "both paths, at different timescales."
- [Undersell + Overdeliver](feedback_undersell-overdeliver.md) — Path B is the undersell; the DEFERRED showcase is the overdeliver when capability catches up.

**Standing instruction:** when reviewing AI-delivered theater, name the two paths, commit to one, stash the other. The middle path is forbidden.
