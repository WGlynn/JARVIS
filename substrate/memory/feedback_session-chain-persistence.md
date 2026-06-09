---
name: Session Chain Persistence Check — Every Session
description: Every session must check session chain persistence. The chain IS the memory. Treat it like a coding primitive.
type: feedback
---

# Session Chain Persistence Primitive (2026-03-13)

## The Directive
Every session, check the persistence of the session chain (`~/.claude/session-chain/`).

```
python ~/.claude/session-chain/chain.py status
```

If it doesn't exist or is empty, recreate it. The chain is the cognitive WAL — without it, work disappears between sessions.

## Why
- v1 session chain was lost because it wasn't file-based persistent
- v2 uses JSON files in blocks/ directory — survives crashes
- But the directory itself can be deleted or lost
- Checking persistence IS the primitive — same as checking disk before writing

## Will's Words
- "every session I want you to check the persistence of the internal blockchain"
- "that can just be a coding/knowledge primitive to keep that itself persistent"
