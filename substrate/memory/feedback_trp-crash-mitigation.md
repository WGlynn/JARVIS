---
name: TRP Crash Mitigation — Use Runner Protocol
description: TRP invocation crashes context window. ALWAYS use TRP_RUNNER.md (staggered loads + context guard + minimal boot + subagent sharding) instead of monolithic execution.
type: feedback
---

TRP invocation in the main context window causes crashes. NEVER run TRP monolithically.

**Why:** Loading CKB + MEMORY + SESSION_STATE + WAL + TRP spec + 4 loop docs + target code + recursive operations exceeds context capacity. Observed repeatedly — every TRP invocation crashed.

**How to apply:** When Will says "recursion protocol", "TRP", "run the loops", or "recursive improvement":
1. Read `vibeswap/docs/trp/TRP_RUNNER.md` — the runner protocol
2. Follow its 4 mitigations:
   - **Staggered loading**: coordinator loads only TRP_RUNNER.md + target summary. Loop docs go to subagents only.
   - **Context guard**: if session is already heavy (>10 exchanges or >5 large files read), refuse and suggest reboot
   - **Minimal boot**: skip CKB, skip full MEMORY traversal, skip deep SESSION_STATE read
   - **Ergonomic sharding (Nervos pattern)**: R0 stays local (self-referential), R1/R3 go to subagents (compute), R2 is hybrid (sonnet discovers, coordinator verifies)
3. Score the cycle using the 5-dimension rubric in TRP_RUNNER.md
4. NEVER load TRINITY_RECURSION_PROTOCOL.md into the coordinator — that's reference docs, not runtime

This is the difference between loading a 747 with cargo vs sending 4 drones with 1 package each.
