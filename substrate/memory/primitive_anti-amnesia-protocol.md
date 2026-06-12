---
name: anti-amnesia-protocol-aap-write-ahead-log-for-crash-recovery
description: "Third and final layer of the three-layer persistence architecture. WAL.md captures live execution state (task manifest, progress, intent) so crashes don't cause amnesia. Check WAL FIRST on every session start."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8f988124-8197-4f80-8a59-217ae187c3ef
---

# Anti-Amnesia Protocol (AAP)

The final piece of the three-layer mind:

| Layer | File | What it captures | Survives |
|-------|------|-----------------|----------|
| 3 | CKB + MEMORY.md | Identity + knowledge | Everything |
| 2 | SESSION_STATE.md | Session boundaries | Context compression |
| **1** | **WAL.md** | **Live execution state** | **Crashes** |

**Why:** Session crashed with 10 agents and 35 tasks in-flight (2026-03-26). SESSION_STATE.md was stale (written before autopilot started). Git had the commits but not the plan. Jarvis had to forensically reconstruct instead of just knowing. Will: "when I ask what happened you should be aware of what happened." ANY unclean exit triggers recovery — PC crash, OOM, user closes terminal, ctrl+C. All are equal. If WAL says ACTIVE in a new session, the mind was interrupted.

**How to apply:**

## Session Start — Step 0 (BEFORE EVERYTHING)
Check `.claude/WAL.md`. If status == ACTIVE → crash detected → run recovery protocol before anything else.

> **Reconciliation (2026-06-11, vs `boot-session-state-over-rsi`)**: merged boot order — WAL crash-check (`status ACTIVE?`) = step 0 (crash detection); SESSION_STATE = step 1 and the authoritative DIRECTIVE source; RSI files only when SESSION_STATE points at them.
> The two entries govern different axes (crash-detection vs directive-priority) and are compatible under this ordering.

## Pre-Flight (before autopilot/multi-agent work)
1. Write WAL.md: status=ACTIVE, full task manifest (all QUEUED), parent commit, intent
2. Commit + push WAL.md BEFORE spawning any agents

## In-Flight
- Task start → QUEUED → ACTIVE
- Task commit → ACTIVE → DONE (record commit hash)
- Every 3-5 tasks → checkpoint (commit WAL.md)

## Landing (clean end)
- Mark WAL CLEAN, fold into SESSION_STATE.md, commit + push

## Recovery (crash detected)
1. Read WAL → get manifest + intent
2. Cross-reference git log + git status → mark tasks DONE/ORPHANED/LOST
3. Present recovery report immediately
4. Await user decision

Full spec: `vibeswap/docs/_meta/protocols/ANTI_AMNESIA_PROTOCOL.md` · retention audit: `ANTI_AMNESIA_RETENTION_SCORECARD.md`

**Scope (2026-06-12)**: WAL is now TWO-tier — project work → `vibeswap/.claude/WAL.md`; cross-repo / JARVIS-wide work → `~/.claude/WAL.md`. Closes the "WAL is vibeswap-scoped" coupling-drift from the scorecard. FOLLOW-UP (pending): the SessionStart WAL-status hook still reads only the vibeswap WAL — generalize it to also read `~/.claude/WAL.md`.
