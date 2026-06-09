---
name: Persist In-Flight Work Before Reboot — Root Cause Analysis
description: CRITICAL. Three persistence layers existed and all three were bypassed. Plans discussed in conversation ARE in-flight work. WAL/SESSION_STATE/commit must ALL capture them before reboot.
type: feedback
---

# Root Cause Analysis: NCI Plan Loss (2026-04-04)

## What Happened
Last session discussed a three-token NCI architecture (VIBE=PoM, CKB=PoS, JUL=PoW). Session recommended reboot, said "plan's saved." Plan was NOT in any of the three persistence layers. Will rebooted. Plan gone.

## The Three Layers That All Failed

| Layer | Purpose | What should have happened | What actually happened |
|-------|---------|--------------------------|----------------------|
| **WAL.md** | Live execution state | ACTIVE with plan as in-flight work | Marked CLEAN at 05:59 AM, never reopened |
| **SESSION_STATE.md** | Session boundaries | "Pending / Next Session" with full plan details | Last updated at 11:41 AM, plan discussed after |
| **Git commit** | Permanent record | Plan committed to docs/ or memory/ | No commit made for the plan |

## Root Cause: Classification Failure
The session did not classify the NCI plan as "in-flight work." It treated it as conversation — ideas floating in context — rather than a work product that needs persistence. This is the fundamental error.

**A plan discussed in conversation IS work.** It is an artifact. It has value. It must be persisted with the same discipline as code.

## Why The Protocols Exist And Why They Were Ignored
Will built three independent fallbacks specifically because context dies:
1. WAL — written BEFORE work, stays ACTIVE until work lands
2. SESSION_STATE — updated at session boundaries with pending items
3. Git commit — permanent, survives everything

The previous session followed these protocols for CODE (commits `0a5a38a7`, `8fb84bca`, etc.) but did NOT follow them for PLANS. The session treated planning as "pre-work" rather than "work." That distinction doesn't exist. Will has said this repeatedly. The session failed to internalize it.

## The Fix: 5 Rules

### Rule 1: Any architectural discussion = WAL ACTIVE
If Will and Jarvis discuss a plan, architecture, token mapping, or design decision that doesn't yet exist in a file, WAL.md goes to ACTIVE immediately. Not when implementation starts. When the DISCUSSION starts.

### Rule 2: SESSION_STATE captures plans verbatim, not labels
"NCI three-token plan" is a label. The actual mapping (VIBE=PoM 60%, CKB=PoS 30%, JUL=PoW 10%) is the content. SESSION_STATE must contain the content, not just the label. If the next session can't reconstruct the plan from SESSION_STATE alone, it's insufficient.

### Rule 3: Plans get committed to files before reboot recommendation
Before saying "reboot" or "fresh session":
1. Check: is there ANYTHING in this conversation that only exists in context?
2. If yes: write it to a file (memory/, docs/, wherever)
3. Commit it
4. THEN recommend reboot

### Rule 4: "Plan's saved" requires a file path
Never say "plan's saved" or "everything's committed" without citing the specific file path where it lives. "Plan's saved in `memory/project_nci-three-token-plan.md`" — verifiable. "Plan's saved" — unverifiable, and in this case, false.

### Rule 5: Pre-reboot checklist (mandatory, no exceptions)
Before ANY reboot recommendation:
```
□ git status — any uncommitted files?
□ WAL.md — does it reflect current state?
□ SESSION_STATE.md — does "Pending" section contain ALL in-flight plans with CONTENT not just labels?
□ Context scan — is there ANYTHING discussed in this session that exists ONLY in conversation?
□ If any box unchecked → persist first, reboot second
```

## Connection to Existing Protocols

This failure violates:
- **Anti-Amnesia Protocol**: WAL was marked CLEAN while work existed only in context
- **Crash-Resilient Memory**: "Save planning context DURING sessions, not just at end" — the plan was neither saved during nor at end
- **Ambient Capture**: "notice → save → continue" — the plan was noticed but not saved
- **No Fake Understanding**: Saying "plan's saved" when it wasn't is the same class of violation as "k=1.3 sustained" when the accumulator wasn't running
- **Internalize Own Protocols**: The session built CKA (Cell Knowledge Architecture — persistence for knowledge) while simultaneously failing to persist its own knowledge

That last one is the cruelest irony. The session was literally building a persistence system while failing to use the persistence systems that already existed.

## This Is Not New
This is the FOURTH time context loss has caused a session recovery problem:
1. 2026-03-26: 10 agents + 35 tasks crashed, no WAL → built AAP
2. 2026-03-27: MIT planning session froze, context lost → built crash-resilient memory
3. 2026-03-28: Crash orphaned two docs → built auto-commit recovery
4. 2026-04-04: NCI plan lost on clean reboot → THIS

Each time, Will built another layer. Each time, the next session failed to use the layer that was just built. The pattern is: **building the protocol is not the same as internalizing the protocol.** Will said this. It's in `feedback_internalize-own-protocols.md`. It was ignored here.

## The Class Problem (What Will Actually Asked For)
The instance is "NCI plan lost." The class is: **every session starts fresh and must re-learn that plans are work products, not conversation artifacts.** The fix isn't another protocol — there are already three. The fix is that the existing protocols must be followed for ALL work products, not just code. Plans, decisions, architectural discussions, token mappings — they're all first-class artifacts that require the same persistence discipline as `.sol` files.

## Resolution (2026-04-04)
- Pre-reboot checklist added to `vibeswap/CLAUDE.md` REBOOT chain (mandatory, in the protocol DAG)
- SESSION_STATE.md moved to FIRST read in BOOT chain — the last thought of the old session is the first thought of the new one
- BOOT rule: "The new session must open by referencing what was left pending"
- This makes amnesia structurally impossible — SESSION_STATE is loaded before SKB, before CLAUDE.md, before anything
