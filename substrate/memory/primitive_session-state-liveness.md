---
name: Session State Liveness Gate
description: SESSION_STATE.md must be write-through (updated during session), not write-back (written only at end). Prevents stale state on crash/compression.
type: feedback
---

# Session State Liveness Gate

## The Failure Mode

SESSION_STATE.md is written at session boundaries (REBOOT/END). If the session crashes, compresses early, or the agent forgets to run the REBOOT protocol, everything between the last write and the crash is lost. The next session boots from stale state and has no idea what happened.

**Root cause**: Write-back architecture. State accumulates in volatile context, then gets flushed to disk at the end. Any interruption between accumulation and flush = data loss.

## The Gate

**Write-through, not write-back.**

SESSION_STATE.md gets updated **during** the session at natural checkpoints, not just at the end. Every meaningful state transition triggers an inline update.

### Trigger Conditions (update SESSION_STATE + WAL when):

1. **A project status changes** — application accepted/rejected, ticket bought/refunded, PR merged, deployment completed
2. **A deliverable is produced** — file written, PDF generated, paper printed, post published
3. **A new primitive or memory is extracted** — captures that the extraction happened, not just the content
4. **A plan is made or changed** — new approach decided, target list created, itinerary drafted
5. **External information is gathered** — research completed, intel collected, person identified
6. **Multi-step work begins** — WAL must go ACTIVE with intent, parent commit, and task list BEFORE starting
7. **Multi-step work ends** — WAL must go CLEAN with final commit and task status BEFORE moving on

### How to Write

Append to "Completed This Session" as you go. Don't wait. One line per item. If the session crashes after that line is written, the next session knows it happened.

### Verification (BOOT)

On session start, after reading SESSION_STATE:

> **Does the "Completed" section match the git log since the last commit timestamp? Are there commits or file changes not reflected in SESSION_STATE?**

If yes → the previous session crashed mid-work. Reconcile before proceeding.

### Verification (MID-SESSION)

Every ~25% context usage (or after any major deliverable):

> **Is SESSION_STATE current? Would a fresh session reading this file know what I've done?**

If no → update now. Don't defer.

## Why This Is a Gate, Not a Guideline

A guideline says "try to keep it updated." A gate says **the session cannot proceed past a checkpoint without SESSION_STATE reflecting reality.** The distinction matters because guidelines degrade under cognitive load. Gates don't.

**Checkpoint sequence:**
```
Work → State transition detected → Update SESSION_STATE → Continue work
```

Not:
```
Work → Work → Work → Work → ... → REBOOT → Try to remember everything → Write SESSION_STATE
```

## Integration with TRP

- **R0 (Compression)**: Write-through is already compressed — one line per transition. No narrative.
- **R1 (Adversarial)**: Stale SESSION_STATE is a testable failure. "Does SESSION_STATE match git log?" is a verification step.
- **R2 (Knowledge)**: SESSION_STATE is the bridge between volatile session context and persistent memory. If the bridge is stale, knowledge doesn't cross.
- **R3 (Capability)**: This gate makes crash recovery trivial. WAL + current SESSION_STATE = full reconstruction.

## Anti-Pattern

Writing SESSION_STATE once at end of session from memory. Memory degrades over long sessions. Context compression deletes details. The end-of-session write is a lossy reconstruction. Write-through is lossless.

**Why:** SESSION_STATE is the only artifact that bridges sessions. If it's stale, session continuity is broken. Every other persistence mechanism (memory files, git, WAL) can compensate, but only if SESSION_STATE tells the next session where to look.

**How to apply:** After every trigger condition above, update SESSION_STATE inline. Add to REBOOT checklist: "SESSION_STATE already current? If not, something went wrong." Add to BOOT checklist: "Cross-reference SESSION_STATE against git log."
