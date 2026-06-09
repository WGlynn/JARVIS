---
name: Path Commitment Protocol
description: Decision-making sequence for the fork that appears after reviewing an AI-delivered artifact with high theater ratio. Name two coherent paths, commit to one, stash the other. The middle path is forbidden.
type: primitive
originSessionId: 58b19964-c316-4603-98a4-1ffe4fe4f29d
---
**Context:** after running the [AI-Delivered Code Review Protocol](protocol_ai-delivered-code-review.md), the artifact has been assessed. It is either shippable (path not forked — ignore this protocol) or it contains enough theater that a path decision is now required.

**Sequence:**

1. **Name both paths explicitly.** Use the framing:
   - **Path A — Showcase.** Keep the aesthetic. Commit to wiring every advertised capability for real. Requires: a concrete plan for each piece of missing functionality, and the time/context to execute.
   - **Path B — Minimal.** Strip to the one thing you can actually ship well. Kill the theater. Keep the aesthetic only where it earns its keep.
   - **Middle — Forbidden.** A mood board that ages poorly because it carries theater without commitment. Do not drift here.

2. **Answer the audience-market question.**
   - Who is the consumer of this artifact?
   - What do they need to see / use it for?
   - If the answer is "a fully-wired product the user can click through and have work" → Path A is only valid if capability is imminent.
   - If the answer is "a primitive to build on" or "a demo of one real thing" → Path B.
   - If the audience is Agile/CSM/non-crypto ([REDACTED-NDA]-class), Brutalist aesthetic may be a wall — strip further on Path B.
   - If the audience is crypto/dev/MIT, the aesthetic carries weight — preserve it on Path B.

3. **Commit verbally AND in writing.**
   - Verbal commitment: state the path in plain language.
   - Written commitment: create the parallel directory / rename the DEFERRED artifact BEFORE writing any new code. File existence is the truth of the decision.

4. **Scope-lock the chosen path.**
   - Path A scope: list every capability to wire + acceptance criteria for each. Nothing gets added mid-build.
   - Path B scope: list the ONE thing + criteria for "done." Nothing gets added mid-build.

5. **Execute.** Full autonomy on the chosen path. No re-asking the user mid-build — the commitment already answered the per-step questions.

6. **Cross-reference at HANDOFF time.**
   - Chosen path's HANDOFF doc points at the stashed path with a "revive when" trigger.
   - Stashed path's README (if any) notes which minimal version replaces it.

**Why:**
- The middle path is seductive because it looks like compromise. It's actually the worst option: you keep the cost of theater (maintenance, review burden, user confusion) without committing to eliminate it or to back it.
- Explicit two-path framing forces the audience-market question to surface, which is the real decision driver — not "how much code do we keep?"
- Stashing the rejected path protects the visual/design R&D that's already been paid for. It's a call option, not waste.

**Applied instances:**
- Lineage IDE plugin (2026-04-18). Gemini delivered a Substrate aesthetic with zero real wiring. Path A required real Gemini + real DAG client — neither available in-session. Path B was chosen: edit-cell + persist-to-Lineage, aesthetic preserved in terminal and palette only. Showcase stashed. Will committed in chat: "2. but save the gemini one for when we can make it NOT theater."

**Anti-patterns:**
- **Middle path.** Keeping some theater "because it looks cool." Kills the discipline.
- **Deleting the rejected path.** Loses sunk R&D.
- **Non-committal paths.** "Kind of a mix" or "we'll see as we go." This is the middle path pretending it isn't.
- **Re-asking for input per step after commitment.** The commitment IS the input; executing with autonomy is the follow-through.

**Related primitives:**
- [AI-Delivered Code Review Protocol](protocol_ai-delivered-code-review.md) — the preceding step.
- [Deferred Showcase Branching](primitive_deferred-showcase-branching.md) — the artifact-level pattern this protocol operationalizes.
- [Why Not Both](feedback_why-not-both.md) — corollary: when both paths are cheap, do both. When they're genuinely exclusive (as with theater vs minimal), commit.
- [Read the Room](feedback_read-the-room-not-the-memory.md) — drives the audience-market answer in step 2.
