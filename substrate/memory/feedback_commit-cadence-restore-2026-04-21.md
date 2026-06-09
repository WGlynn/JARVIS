---
name: Commit Cadence Restore 2026-04-21
description: Will called out that recent commit cadence has dropped from "hundreds a day" to single-digit per cycle. Restore atomic-commit rhythm — skeleton, fill, polish — instead of one big commit per cycle close.
type: feedback
originSessionId: c14b7c38-1d7d-4550-9588-2dbd1e7c40ec
---
# Commit Cadence Restore — 2026-04-21

**Rule**: ship commits at the natural granularity of completed work-units, not at cycle boundaries. Skeleton commit, fill commits (per section / per file / per logical step), polish commits, push batches of ~10. If a cycle naturally produces 15 commits, ship 15 — don't batch into 2.

**Why**: Will, 2026-04-21: *"we want more commits bro, we kind of stagnated from how we used to do hundreds a day."* Recent cycles have been collapsing into a single large commit at cycle-close (e.g. C30: 287 LOC contract + 30 tests + SOR wire-in + memory updates → 1 commit). Prior rhythm was 5-15 commits for the same scope.

The drift came from misapplying [Token Mindfulness](P·token-mindfulness): "consolidate tool calls" got over-generalized into "consolidate commits." Different things. Tool-call consolidation reduces unnecessary round-trips with the model. Commit consolidation removes audit-trail granularity, makes crash recovery harder, makes the public visible-velocity look stalled, and reduces the natural checkpoints where SHIELD / NDA-gate / auto-checkpoint hooks can catch issues.

A secondary contributor was the NDA-gate incident: each commit became a "NDA-scan-blocking" event, which pushed implicitly toward fewer commits. Wrong response — the gate is the protection; running it more often is better, not worse.

**How to apply**:

1. **Scaffold-first commits** for any deliverable >50 LOC or >2 files. Write the skeleton or interface, commit, then fill.
2. **Per-section / per-file fill commits** for docs and large refactors. ETM audit = one commit per Section 1.X / 2.X / etc. Whitepaper rewrite = one commit per section rewrite. Contract refactor = one commit per touched file (when each file is independently buildable).
3. **Polish commits** for NatSpec, formatting, lint cleanup — separate from the substantive change. Easier to review, easier to revert.
4. **Test-side commits** separately from contract-side when tests can land first (regression-anchor pattern) or after (test-after-fix). One commit per test file is fine.
5. **Memory commits** atomic per primitive / feedback / project entry. Don't batch primitives; each is a separate semantic addition to the library.
6. **Push cadence**: every ~10 commits OR phase boundary. Pushes still go through hooks, so don't push every commit (hook overhead × push), but don't queue more than ~10 either (lose the velocity-visibility property Will is asking for).

**What this is NOT**:
- Not commit-theater. Don't split a 5-line typo into 5 commits to inflate the count. The granularity is *natural work-unit*, not "as small as possible."
- Not skipping NDA-gate or SHIELD. Each commit still gets scanned. Higher cadence means more scans, which is the right tradeoff.
- Not abandoning Token Mindfulness on tool calls. Tool-call consolidation continues to apply (don't over-read, don't churn). Commit cadence is orthogonal.

**Receipt**: 100-commit execution plan from 2026-04-21 will be the test. If the rhythm sticks past that batch, drift is corrected.

**Related**:
- [Token Mindfulness](P·token-mindfulness) — applies to tool calls, not commits. Don't conflate.
- [Session State Commit Gate](P·session-state-commit-gate) — gates *pushes*, not commits. Higher commit cadence is fine; pushes still need state updates.
- [Crash-Resilient Memory Writes](F·crash-resilient-memory-writes) — atomic commits ARE the crash-resilience story for code. Same principle.
- [Persist Plans Before Reboot](F·persist-plans-before-reboot) — frequent commits = frequent persist points = lower cost-per-reboot.
