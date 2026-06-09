---
name: Parallel Issues Log + RSI Cycle
description: When parallel agent execution produces issues (errors, conflicts, timeouts), ALWAYS log to WAL.md and trigger an RSI cycle before proceeding. Hook-enforced.
type: feedback
originSessionId: 76bb18f6-7846-4e93-9cb8-86f2e3362f78
---
**Rule**: If parallel agent execution produces any issues — subagent errors, contradictory results between agents on the same artifact, one agent timing out while another completed, partial failures — **ALWAYS**:
1. Log the issue to `vibeswap/.claude/WAL.md` with timestamp, agents involved, nature of issue
2. Trigger an RSI cycle on the parallelism failure before continuing the work
3. Only resume the original task after the RSI cycle produces a fix or documented acceptance

**Why**: Will, 2026-04-17: *"if there's any issues being in parallel ALWAYS log reports and self correct with an RSI cycle."* Parallelism is existential to throughput ("if we cant paralellize maximally we are fucked"). Silent failures in parallel execution compound — one bad agent result poisons downstream work. Log + RSI closes the loop before the bad state propagates.

**How to apply**:
- After any message containing multiple concurrent Agent tool calls, before acting on results: scan for issue signatures (error strings, conflicting claims, missing sections, timeouts).
- If clean: proceed.
- If any issue: halt the main task, write the WAL entry, run the RSI cycle (what failed, why, what gate prevents recurrence), then resume.

**Enforcement**: This is a gate, not memory. Hook installed in settings.json (see [Always = Gate](primitive_always-equals-gate.md)).

**Reference run (2026-04-17)**: Two Explore agents ran in parallel (RSI Cycle 26 scoping + Oracle Cycle 12 scoping). Both returned clean comprehensive scopes. No issues → no RSI cycle triggered. Protocol was in place but did not need to fire.
