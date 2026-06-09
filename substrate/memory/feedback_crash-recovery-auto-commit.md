---
name: Crash Recovery — Auto-Commit Orphaned Writes
description: On session recovery, immediately commit+push any uncommitted files from the crashed session before doing anything else
type: feedback
---

# Auto-Commit Orphaned Files During Crash Recovery

When recovering from a crash, the FIRST action (after WAL check) should be: check for uncommitted files that the crashed session wrote, commit them, and push.

**Why:** On 2026-03-28, a crash orphaned two fully-written MIT partnership docs. The docs survived on disk but sat uncommitted. The new session had to manually discover and commit them. If Will had been on a different machine or the disk had been wiped, they'd be gone. The work was 98% done — only the commit/push was missing.

**How to apply:**
1. During boot sequence (after WAL check, before resuming work), run `git status` to detect untracked/modified files
2. Cross-reference with SESSION_STATE.md to understand what the crashed session was working on
3. If there are orphaned writes that clearly belong to the crashed session's work, commit and push them IMMEDIATELY
4. This makes crash recovery truly seamless — the new session picks up with all artifacts already safe in git
5. This is the "commit" step that crashes always kill — it must be the first thing the recovery does, not the last
