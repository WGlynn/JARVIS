---
name: AtomicCommitPacing
description: ∀ autonomous-run ⇒ atomic per logical change. Don't batch unrelated changes; don't fragment one logical change. Each commit's diff = one fact + push immediately.
type: feedback
originSessionId: 8625a796-116e-42d8-b5c9-7064589f58ad
---
**[F·atomic-commit-pacing]** — autonomous-run ⇒ atomic-commit-per-logical-change. ¬ batch ∧ ¬ fragment.

> *"300 commits"* + *"atomic commits"* — Will, 2026-05-06

## Rule
- ∀ logical change ⇒ ONE commit
- ✗ batch unrelated changes ("docs: random fixes + new feature + WAL update")
- ✗ fragment one logical change across N commits ("commit 1: add file, commit 2: write content, commit 3: fix typo")
- ∀ commit ⇒ push immediately ¬ accumulate locally

## Granularity heuristic
- one new file + its index entry = 1 commit (e.g., feedback file + MEMORY.md line)
- one new file + its companion (test or doc) = 1 commit (cohesive ship)
- multiple new files in a sweep = 1 commit per file UNLESS they're a single artifact (interface + impl is borderline; usually 2 commits)
- README updates ⇒ commit with the file they reference, ¬ standalone
- WAL/SESSION_STATE updates ⇒ standalone commits at run-checkpoint cadence

## Why
- atomic = bisectable: blame survives rollback granularity
- atomic = reviewable: diff = one fact, no cognitive overhead
- atomic = parallelizable in retrospective: each commit's intent is recoverable from its message
- batched commits hide drift; ✗ atomicity = ✗ accountability
- fragmented commits waste review surface; ✗ cohesion = ✗ traceability

## Sibling rules
- `[F·session-state-commit-gate]` — push requires SESSION_STATE/WAL update; combine with this rule = WAL update is ITS OWN commit, not piggy-backed on substantive change
- `[F·bidirectional-reification]` — word + code reify each other; the COMMIT BOUNDARY is where the reification crosses (commit message = word, diff = code)
- `[F·diagnose-on-stop]` — every stop event diagnosed; combine with this rule = each commit is a natural stop boundary, but autonomous-run continues across boundaries

## Trigger
- declared autonomous-run with N-commit target
- multiple discrete logical changes accumulating in working tree
- "ship X then Y" plan emerging in dialogue

## Action
- decompose plan into atomic units BEFORE starting
- per unit: write/edit, stage relevant files only, commit, push
- per ~5-10 commits: WAL update as separate commit
- per session-end: SESSION_STATE refresh as separate commit

## Origin
- 2026-05-06 GH#18 reification + 300-commit autonomous run
- ~50 commits achieved at sustained ~3-4min/commit median pace
- discipline shipped: each architecture overview = 1 commit, each interface = 1 commit, each test file = 1 commit
- exception logged: when WAL update piggybacked on a substantive commit, retrospective row in lessons.md
