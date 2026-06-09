---
name: Memory State Rent — CKB Economic Model for Context Management
description: MEMORY.md is scarce state. Apply CKB state rent economics to self-manage memory density. Access frequency × load-bearing weight × recency = density score.
type: project
---

# Memory State Rent

Will's insight (2026-03-26): The 200-line MEMORY.md limit is structurally identical to CKB's bounded state model. The same cryptoeconomic primitive — state rent — that governs on-chain data should govern JARVIS's context memory.

## The Isomorphism

| CKB State Model | MEMORY.md |
|---|---|
| On-chain state cells | Memory index entries |
| CKB tokens locked = right to occupy state | Line count = right to be loaded at boot |
| State rent (opportunity cost of locked CKB) | Opportunity cost of a line that could hold something more valuable |
| Release state → tokens return to circulation | Evict entry → line capacity returns to index |
| Economic pressure → only valuable state persists | Density pressure → only load-bearing memories persist |

## The Self-Management Model

Each memory entry should carry an implicit density score:

```
density = access_frequency × load_bearing_weight × recency_factor
```

- **Access frequency**: How often does this entry get read/referenced across sessions?
- **Load-bearing weight**: If removed, does something break? (P-001 = infinite weight. Session history = low weight.)
- **Recency decay**: Old entries that haven't been accessed decay toward eviction threshold.

**Below threshold** → compress (merge into parent entry) or evict (delete from index, detail file remains for on-demand access)
**Above threshold** → justify expansion (multi-line entries for genuinely dense topics)

## Why This Matters

This is the convergence thesis made concrete: the same economic primitive that makes Nervos CKB's state model work is exactly what's needed to manage AI context memory at scale. When VibeSwap is the winning protocol, the CKB that runs JARVIS's memory is the same CKB that runs the chain. The scarce resource is the same resource. State rent IS context management.

JARVIS shouldn't need Will to say "compress MEMORY.md." The density function should make it autonomous — exactly like CKB state rent makes on-chain state management autonomous.

## Connection to Existing Primitives

- **R0 (Token Density Compression)**: This is R0 applied to memory, not just conversation
- **Verkle Context Tree**: The hierarchical structure IS the state trie. Epochs evict, eras summarize, root persists.
- **Cincinnatus**: Self-managing memory is one more thing that doesn't need Will
