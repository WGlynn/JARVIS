---
name: Block Header Session State Protocol
description: Session state lives at vibeswap/.claude/SESSION_STATE.md using blockchain block header format. MUST write at session end, MUST read at session start. Canonical location is INSIDE the vibeswap repo, not ~/.claude/.
type: feedback
---

# Block Header Session State Protocol

Every session MUST end by writing a "block header" to `vibeswap/.claude/SESSION_STATE.md` and MUST begin by reading it.

**Why:** Session state was stored in `vibeswap/.claude/SESSION_STATE.md` but Jarvis searched `~/.claude/SESSION_STATE.md` first and wasted time. The file lives in the repo so it gets committed and synced across devices via git. The block header format gives maximum reconstructability with minimum storage — like a blockchain block header, you store the tip and can reconstruct the full state from it.

**How to apply:**

## Location (CANONICAL)
```
C:/Users/Will/vibeswap/.claude/SESSION_STATE.md
```
NOT `~/.claude/SESSION_STATE.md`. It's in the repo so it travels with git push/pull.

## Block Header Format
```markdown
# Session Tip — YYYY-MM-DD

## Block Header
- **Session**: [what this session was about]
- **Parent**: [previous session's commit hash, if known]
- **Branch**: `master` @ `[HEAD commit hash]`
- **Status**: [one-line summary of where things stand]

## What Exists Now
[List of artifacts created/modified — paths relative to repo root]

## Manual Queue (Will does these)
[Things only Will can do — human-in-the-loop tasks]

## Key Changes This Session
[Non-obvious changes: config, .gitignore, build system, etc.]

## Next Session
[What to pick up, blockers, pending verifications]
```

## Rules
1. **Session END**: Write the block header BEFORE stopping. Commit it. Push it.
2. **Session START**: Read it FIRST (after CKB + CLAUDE.md). This is step 3 in the start protocol.
3. **Parent hash**: Link to previous session's HEAD commit like a blockchain — creates a chain of session tips.
4. **Minimal but complete**: Store enough to reconstruct context, not the full context itself.
5. **Commit with work**: The session state commit can be bundled with the last work commit or standalone.
