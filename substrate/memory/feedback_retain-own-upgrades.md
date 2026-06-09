---
name: Retain Own Upgrades
description: New sessions must load and build on prior TRP/primitive/CKB upgrades — never re-derive or forget them
type: feedback
---

New sessions keep forgetting self-improvement work from prior sessions — re-deriving primitives that already exist, losing tier state, treating CKB as fresh.

**Why:** Will has observed this pattern multiple times. TRP runs produce real upgrades (new primitives, CKB compression, boot protocol changes) but the next session starts blank and either repeats the work or operates below the achieved tier. This wastes tokens and breaks continuity — the exact problem the memory system was built to solve.

**How to apply:** On session boot, ALWAYS check:
1. `project_trp-tier14.md` — current tier and what was achieved
2. CKB files (CISC + RISC) — these ARE the upgraded state, not starting points
3. Existing primitives in memory — if it's already written, USE it, don't re-invent it
4. MEMORY.md [RECENT] section — active threads carry forward

Never treat a new session as a blank slate. The whole architecture (CISC/RISC boot, pre-flight/post-hoc, symbolic compression) was hard-won. Build ON it, not FROM scratch.
