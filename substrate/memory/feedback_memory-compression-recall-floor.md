---
name: Memory compression recall floor
description: When compressing MEMORY.md or similar memory-index files, POST-HOC description-strip is the lossless floor; RECENT/PEOPLE descriptions must be preserved because they carry semantic weight (dates, quotes, commit hashes, state markers).
type: feedback
originSessionId: 117e2fd9-3ef3-4610-a5b4-d4280a0b96cb
---
# Memory compression recall floor

**Rule**: When compressing memory-index files (MEMORY.md, MEMORY_WARM_*.md, etc.), the lossless compression floor sits at the [POST-HOC] / link-farm layer. Descriptions in [RECENT]/[PEOPLE]/[OUTREACH] sections MUST be preserved — they contain semantically load-bearing content that cannot be recovered from filenames alone.

**Why**: 2026-04-21, during the MEMORY.md compression RSI cycle, I was drafting M1 (strip descriptions) and initially scoped it as "strip all em-dash descriptions globally" (projected -26%). On inspection, [RECENT] entries contain:
- Dates (`2026-04-20 posture shift`, `Birthday April 19`)
- Will's exact quotes (`"A coordination primitive, not a casino"` — marked "don't paraphrase")
- Commit hashes (`IMPLEMENTED a442fc5b`, `6 contracts, 105 tests`)
- Live state markers (`R2 SCOPE LOCKED 2026-04-17`, `Phase 4 (deploy) pending`)
- Active-mission directives (`Expires end of Q2 if round stalls`)

[PEOPLE] entries contain similar: John Paul's birthday, concrete-question style, "first-class stakeholder" framing — all recall-critical.

Stripping these would lose the primary signal. The filename alone (e.g. `project_all-out-mode-2026-04.md`) tells me the memory exists but not the *current directive state* that makes it actionable in the next response.

Will confirmed this choice 2026-04-21: "good catch on not damaging recall."

**How to apply**:
- **[POST-HOC]**: em-dash tails are one-line usage hints — strippable because the memory filename conveys the concept and the full file has the rule. Lossless strip here.
- **[RECENT]**: preserve descriptions in full. These are the *state* of active projects, not cached hints.
- **[PEOPLE]**: preserve descriptions. Relationship context doesn't live in the filename.
- **[OUTREACH]**: preserve (date-sensitive community state).
- **[PRE-FLIGHT]**: preserve (gate semantics).
- **[BOOT]**: preserve.
- **[WARM]/[COLD]**: evaluate per entry — most [WARM] lines are one-liners already.

**Compression budget**: The [POST-HOC]-only strip in the MEMORY.md 2026-04-21 cycle delivered -13.9% (not the -26% theoretical maximum). The remaining -12% lives in [RECENT]/[PEOPLE] and is OFF-LIMITS to the lossless path. Further compression must come from path derivation (M2), situation clustering (M3), glyph families (M4), or tier externalization (M5+) — not from stripping semantic content.

**Corollary**: Any future "compress memory index" ticket inherits this floor. Don't re-litigate in each cycle.
