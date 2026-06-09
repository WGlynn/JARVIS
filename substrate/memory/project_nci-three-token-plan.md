---
name: NCI Three-Token Implementation
description: Nakamoto Consensus Infinite 3-token architecture — VIBE=PoM(60%), CKBn=PoS(30%), JUL=PoW(10%). IMPLEMENTED in commit a442fc5b.
type: project
---

# NCI Three-Token Consensus Architecture — COMPLETE

**Commit**: `a442fc5b` (2026-04-04)
**Plan file**: `.claude/plans/imperative-hatching-tide.md`

## The Mapping

| Dimension | Weight | Token | Role |
|-----------|--------|-------|------|
| Proof of Mind (PoM) | 60% | **VIBE** | Non-purchasable governance. Earned through Shapley-verified contribution. 21M cap. |
| Proof of Stake (PoS) | 30% | **CKBn** | State rent collateral. Inflationary with DAO shelter. No hard cap. |
| Proof of Work (PoW) | 10% | **JUL** | Energy-pegged. SHA-256 mining. Elastic rebase. Burns into CKBn via one-way bridge. |

## Why Three (Tinbergen's Rule)
3 independent security targets (resist capital capture, resist compute capture, resist governance capture) require 3 independent instruments. Fewer tokens force dimensions to share properties that contradict each other. This is separation of powers — the constitutional architecture of consensus.

## Implementation Status: ALL PHASES COMPLETE
- Phase 1: CKBNativeToken + JULBridge + tests ✓
- Phase 2: StateRentVault + DAOShelter + SecondaryIssuanceController + tests ✓
- Phase 3: ShardOperatorRegistry + NCI wiring + integration test ✓
- Paper: Section 9 (necessity proof) + Section 10 (implementation list) ✓
- Remaining: Phase 4 (deploy script, FOUNDRY_PROFILE=full, invariant tests)
