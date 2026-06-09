---
name: Session State Commit Gate
description: Every git push MUST be preceded by SESSION_STATE + WAL update — no push without state sync
type: feedback
originSessionId: cb50ef68-bd3e-49a2-b0f8-a82c32fa5716
---
## Session State Commit Gate

**Rule:** No `git push` without updating SESSION_STATE.md and WAL.md first.

### The Problem (Self-Audit: 2026-04-12)

2,420 commits. 10 session-state tracking commits. Persistence score: ~15/100.

SESSION_STATE and WAL capture structured RSI/TRP sessions but miss organic work entirely — hackathons, feature builds, doc writing, cross-ref audits. The result: 85% of session history exists only in git log, with no context about WHY the work happened, what was learned, or what's pending.

### The Gate

Before every `git push`, verify:

1. **SESSION_STATE.md "Completed" section** includes what was just committed
2. **SESSION_STATE.md "Pending" section** reflects actual next steps (not stale from 4 days ago)
3. **SESSION_STATE.md Block Header** has current commit hash, date, and branch
4. **WAL.md** reflects current epoch (ACTIVE if mid-work, CLEAN if done)

If any of these are stale, update them BEFORE pushing.

### Why This Was Failing

- SESSION_STATE updates were a protocol step, not a gate
- During organic sessions, the protocol chain isn't explicitly invoked
- The BOOT sequence reads SESSION_STATE but the WORK/COMMIT sequence doesn't write to it
- Write-through was aspirational, not enforced

### The Fix

Wire SESSION_STATE into the commit flow, not the session flow. Commits happen in every session. If SESSION_STATE updates are gated on commits, coverage approaches 100%.

### Minimum Viable Update

If context is tight and a full SESSION_STATE rewrite is too expensive, the minimum update is:

```markdown
## Block Header
- **Session**: [one-line description]
- **Commit**: `[hash]`
- **Status**: [CLEAN/ACTIVE]

## Completed This Session
- [one bullet per commit since last update]

## Pending / Next Session
- [what's actually next, not stale content]
```

This takes ~30 seconds and prevents the 85% data loss.

### Scoring

Persistence Score = (commits with SESSION_STATE coverage) / (total commits) * 100

Target: >80%. Current: ~15%. Every session that pushes without updating SESSION_STATE degrades the score.
