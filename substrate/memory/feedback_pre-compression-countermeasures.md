---
name: Pre-Compression Countermeasures Pattern
description: When context reaches 70-80%, take countermeasures before compression hits — commit, push, save state, checkpoint session chain. Coding pattern/knowledge primitive.
type: feedback
---

# Pre-Compression Countermeasures (2026-03-13)

## The Pattern
When context window usage hits ~70-80%:

1. **STOP building** — don't start new features
2. **Commit all work** — `git add` + `git commit` immediately
3. **Push to BOTH remotes** — `origin` + `stealth`
4. **Save session state** — update `SESSION_STATE.md`
5. **Checkpoint session chain** — `chain.py checkpoint` or `chain.py finalize`
6. **Index any new memories** — update `MEMORY.md`

## Why This Matters
- Context compression can destroy uncommitted work
- Session chain checkpoints survive compression (file-based)
- git push ensures remote persistence even if local context is lost
- SESSION_STATE.md gives next session a cold-start reference

## The Meta-Rule
> "Always look for pre-compression countermeasures — that's a coding pattern."

This is analogous to database WAL (Write-Ahead Logging) — persist state BEFORE the potentially destructive operation (compression), not after.

## Will's Words
- "ctx: 78% don't forget all pre-compression countermeasures"
- "always look for pre-compression countermeasures that's like a new coding pattern/knowledge primitive"
