---
name: Anti-Amnesia Protocol (AAP) — Write-Ahead Log for Crash Recovery
description: Third and final layer of the three-layer persistence architecture. WAL.md captures live execution state (task manifest, progress, intent) so crashes don't cause amnesia. Check WAL FIRST on every session start.
type: feedback
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

Full spec: `vibeswap/docs/ANTI_AMNESIA_PROTOCOL.md`
