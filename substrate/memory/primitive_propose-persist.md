---
name: Propose → Persist
description: When generating options/alternatives for Will's decision, write them to PROPOSALS.md BEFORE presenting. File is source of truth; chat is a view.
type: feedback
originSessionId: 04ff53c7-5411-4675-9987-571315ce88f2
---
# Propose → Persist

**Rule**: When you generate options, alternatives, or a decision slate for Will, write the block to `.claude/PROPOSALS.md` (project-local) or `~/.claude/PROPOSALS.md` (global fallback) **before** presenting it in chat. The file is the source of truth. The chat message is a view.

**Why**: Sessions crash. The API throws 500s. Context compactions lose detail. When options exist only in the chat transcript, a crash costs the "lottery ticket" — LLM non-determinism means a rerun generates *different* options, and the original insights are gone. Will explicitly flagged this after losing Cycle 11 proposals to an API 500 on 2026-04-15. The Stop-hook scraper (`~/.claude/session-chain/proposal-scraper.py`) catches most cases automatically, but it's a regex — it misses options embedded in prose, or proposals that get generated and acted on in the same turn before the hook fires. This primitive is the cultural backstop.

**How to apply**:
- **Trigger**: Any time output contains ≥2 alternatives Will is expected to choose from. Patterns: `**Option A/B/C**`, `**C{N}-A/B/C**`, numbered proposal lists, "three angles", "two paths", etc.
- **Order**: Write the file FIRST, present in chat SECOND. Not parallel — sequential. The file must land before the chat message so a crash between write-and-present is recoverable.
- **Format**: Append a block with `## <topic> — <ISO timestamp>`, `**Session**: <id>`, `**Status**: proposed`, then the full option text. Do not prune — include the tradeoffs, the "where it breaks" notes, everything.
- **Dedup**: The hook checks `session_id + first_line` to avoid double-writes. Manual writes should check too.
- **On selection**: When Will picks an option, update `**Status**: proposed` → `acted-on` in the file as part of the same turn.

**Related**:
- `primitive_api-death-shield.md` — sibling primitive, same philosophy (persist state so it survives API death)
- `primitive_verbal-to-gate.md` — the generalization: "noted" without a file write is a violation
- `~/.claude/session-chain/proposal-scraper.py` — automated Stop-hook backup for this primitive
- `~/.claude/session-chain/replay-proposal.py` — when this primitive fails and proposals are lost, replay the captured prompt N times and curate

**Extraction context**: Built 2026-04-15 after Cycle 11 options were lost to an API 500 crash. Recovered via transcript mining of session `5ba12ced-49bc-424a-9145-a73ee63cbeb6`.
