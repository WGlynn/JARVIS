---
name: Text→Code Loop — Verify First, Ship Second
description: Observation from C40a (2026-04-23, first documented run of Code↔Text Inspiration Loop). When the loop runs text→code on an existing doc pipeline, the FIRST round is likely to surface drift accumulated during pedagogical compression, not produce a clean code ship. Verify doc claims against code BEFORE writing any code.
type: primitive
originSessionId: 2599425c-2d6c-48c6-a7e1-6457f46d33f3
---
# Text→Code Loop — Verify First, Ship Second

## Observation (2026-04-23, C40a)

Run 1 of the Code↔Text Inspiration Loop after the 60+ doc pedagogical-revision pipeline did NOT produce a clean code ship from a doc "future work" item. It produced a **doc reconciliation**.

Sequence:

1. Primitive said: "Pick a doc's future-work item, ship it as code."
2. Picked `ETM_BUILD_ROADMAP.md` Gap #1 — stated as "NCI has linear retention; replace with convex α=1.6; ~50 LOC."
3. Loaded supporting docs (`NCI_WEIGHT_FUNCTION.md`, `COGNITIVE_RENT_ECONOMICS.md`) — both confirmed the "currently linear" claim.
4. **Verified against code** — `NakamotoConsensusInfinity.sol` has NO retention function. Linear or otherwise. `cumulativePoW` is monotone, `mindScore` is refresh-on-demand.
5. The "before state" described in three docs was a hallucinated narrative — compressed during the pedagogical revision pass to make the "linear → convex" story readable.

Shipped:
- Commit 1: doc reconciliation (three docs corrected).
- Commit 2: pre-existing master-compile unbreaks (em-dash in require literal, missing enum member) surfaced while trying to verify.
- Commit 3: pure `calculateRetentionWeight` primitive + 8 tests, correctly scoped.

## The generalization

**When the text→code direction of the loop runs for the first time on an existing doc pipeline, expect doc-vs-code drift before expecting code output.**

Reason: pedagogical revision passes compress for narrative clarity. Compression introduces drift when the "before" state of a mechanism is asserted without re-verification. A doc saying "currently X" is a claim about code-state at the moment of writing, which may not match current code.

The loop's intended mode (doc surfaces question → code answers it → doc updated with shipped pointer) requires that the doc's claim about CURRENT code is accurate. If it isn't, the "future work" item is ill-posed until the current state is reconciled.

## Heuristic for future text→code rounds

Before writing any code from a doc's future-work item:

1. Read the `Gap IS` / `Before` / `Currently` section.
2. Grep or read the actual contract for the mechanism the doc names.
3. If the code matches the doc's "before" claim — proceed to ship.
4. If the code does NOT match — STOP. The first deliverable is a doc reconciliation commit. Then ship the code against reconciled text.

Cost of this check: ~5 minutes per round. Cost of skipping it: shipped code that invents a baseline and fails review.

## Related to

- [Pattern-Match Drift on Novelty](./primitive_pattern-match-drift-on-novelty.md) — same failure mode, different surface. Here the drift was INSIDE our own doc pipeline, not between a novel concept and a familiar analog.
- [Anti-Hallucination Protocol](./primitive_anti-hallucination-protocol.md) — verifying code-state IS the pre-flight check that catches this.
- [Code↔Text Inspiration Loop](./primitive_code-text-inspiration-loop.md) — parent primitive. This is a heuristic for running it correctly.
- [Token Mindfulness](./primitive_token-mindfulness.md) — the discipline that notices "wait, let me actually read the contract" before generating code.

## One-line summary

*First run of text→code loop on existing doc pipeline: expect doc-reconciliation, not code ship. Pedagogical compression drifts the "currently X" claim; verify before writing.*
