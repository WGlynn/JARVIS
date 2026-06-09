---
name: Cell Knowledge Architecture (CKA)
description: UTXO/cell model for knowledge management — cells are consumed and produced (not mutated), naturally shard across instances, content-addressable, with type validation and context-budget capacity
type: project
---

# Cell Knowledge Architecture (CKA)

Named 2026-04-04. The architecture governing how knowledge cells are created, consumed, sharded, and loaded. CKB = the data. CKA = the architecture. Maps to Nervos CKA/CKB at different scales.

## Core Insight

The GKB codebook is already cells. Each glyph is an independent unit of state. The monolithic file is serialization — the data model was always cellular. CKA makes this explicit and gains UTXO properties.

## Cell Schema

```
Cell {
  id:        hash(content)           // content-addressable
  type:      primitive | protocol | technical | alignment | external
  scope:     public | dyadic(userId) | owner
  tier:      RISC (glyph) | CISC (full) | RAW (uncompressed)
  content:   string
  refs:      [cellId]                // DAG edges to dependencies
  born:      blockHeight             // knowledge-chain epoch
  spent:     blockHeight | null      // null = live cell (UTXO)
  capacity:  charCount               // context budget consumed
}
```

## UTXO Properties

1. **Cells consumed and produced, not mutated.** TRP updates spend old cell, create new with new hash. History = chain of spent cells. No merge conflicts across shards — no shared mutable state.

2. **Natural sharding by topic relevance.** Governance shard loads POM, CINCIN, P-000. Trading shard loads MECH, STACK, LAYERS. No shard needs full set. Cell selection replaces monolithic boot.

3. **Lock scripts = access control.** Dyadic CKB cells locked to user relationship. Public GKB glyphs unlocked. Owner-only cells for security/alpha.

4. **Type scripts = validation.** Primitive type requires: name, falsifiable claim, evidence. Protocol type requires: trigger, steps, exit. Invalid knowledge fails type check.

5. **Capacity = context budget.** Cells pay for space they occupy (Nervos state rent analog). Stale cells evicted. High-value cells persist. Total loaded cells ≤ context window.

## Tier Compression

SKB→GKB is a tier change on the same cell. `MECH` at CISC = full SKB section. `MECH` at RISC = glyph. Same cell, different resolution. Shards load the tier they need.

## CKB-Native Tokenomics (State Rent)

Carbon copy of Nervos CKB economic model applied to the CKA shard network.

**3-token model (unchanged)**:
- VIBE = 21M governance, hard cap, conviction voting weight
- JUL = elastic work token, own PoW puzzle, rebase + PI
- CKB-native = state rent token, own PoW puzzle, inflationary tail emission

**No dual mining.** JUL miners mine JUL. CKB-native miners mine CKB-native. Separate puzzles, separate difficulty, separate emission curves. Dual mining dilutes both.

**Emission model**:
- Base issuance → CKB-native miners (PoW)
- Secondary issuance (tail, fixed annual rate) → 3-way split:
  1. Shard operators (proportional to cells stored/served)
  2. DAO stakers (sheltered from dilution)
  3. Treasury/burn (unoccupied state proportion)

**State rent mechanism**:
- 1 CKB-native = 1 byte of CKA cell state
- Creating a cell locks tokens proportional to cell.capacity
- Locked tokens can't enter DAO → secondary issuance dilutes you
- Cell not worth the rent → destroy it, reclaim tokens, stake in DAO
- State cleans itself through economic pressure

**Shard nodes = protocol nodes with minds and rights.** Users interacting with TG bot shards are interacting with CKA nodes that store cells, serve queries, and participate in BFT consensus. The bot network IS the protocol.

## Naming Convergence

CKB = Cell Knowledge Base (data) — maps to Nervos CKB
CKA = Cell Knowledge Architecture (governance) — maps to Nervos CKA
Not accidental — same pattern at different scales.

## Implementation Status (2026-04-04)

- CKA cells deployed in jarvis-bot: 10 cells, manifest.json, selectCells(), getCellContext()
- Deployed to Fly.io v512
- **3-token NCI implementation PLANNED** — plan at `.claude/plans/imperative-hatching-tide.md`
- Next session: execute the plan (6 new contracts, 2 modified, 6 test files)