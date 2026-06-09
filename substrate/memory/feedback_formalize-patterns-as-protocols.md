---
name: Formalize Patterns as Protocols
description: When a useful pattern emerges organically, formalize it as a documented protocol with a memory file AND a MEMORY.md index entry. The loop isn't closed until both exist.
type: feedback
---

# Formalize Patterns as Protocols

When a pattern works — document it as a formal protocol, then index it in MEMORY.md. Both steps required. Pattern without protocol = tribal knowledge that dies on context compression. Protocol without index entry = invisible to future instances.

**Why:** The block header session state pattern worked perfectly but couldn't be found because it was never formalized or indexed. The pattern existed in practice (the file was being written) but not in retrievable knowledge (no memory file, no index pointer, ambiguous path in CLAUDE.md). Hours of context wasted searching.

**How to apply:**
1. Notice a pattern working well (organically or by design)
2. Write a `memory/` file documenting: what it is, why it works, exact format/location, rules
3. Add a pointer in MEMORY.md with the right temperature tag
4. Update CLAUDE.md (global and/or project) if it affects session start/end protocols
5. The loop is closed when a fresh Jarvis instance can find and execute the pattern without human prompting
