---
name: Off-Circulation Registry Pattern
description: Whitelist-based aggregator that tracks tokens held by external contracts so view functions reflect true off-circulation — avoids invasive cross-contract refactoring
type: feedback
originSessionId: 0101333f-9e7e-4925-8d8b-9a8a834253dd
---
# Off-Circulation Registry Pattern

## The Problem

A token contract has canonical "off-circulation" tracking (e.g., `totalOccupied` on `CKBNativeToken`) that's updated only through specific functions (`lock()`/`unlock()`). Downstream contracts receive tokens via standard `transferFrom()` for staking/collateral/escrow. Those tokens sit in contract balances — out of circulation — but invisible to `totalOccupied`.

Any system metric built on `totalOccupied` (issuance splits, circulating supply, inflation models) under-counts. The more tokens are staked/collateralized, the worse the drift.

**Why:** Discovered on 2026-04-13 in RSI C8 while closing C7-GOV-001. `SecondaryIssuanceController` computed `shardShare = emission * totalOccupied / totalSupply`, but NCI validators staked hundreds of thousands of CKB via `transferFrom()` — none counted, shard emission dropped.

## The Naive Fix (Rejected)

Add parallel `stake()`/`unstake()` functions mirroring `lock()`/`unlock()`. Change every downstream contract (NCI, VibeStable, JCV, DAOShelter) to call them instead of `transferFrom()`.

**Rejected because:**
- Invasive — changes 4+ contracts, each with their own test surface
- Error-prone — any `transferFrom()` path that sneaks in breaks accounting
- Duplicates accounting — external contracts already track their own holdings; now both sides need updates

## The Registry Pattern

Add a whitelist of external holders to the token contract. `balanceOf(holder)` is authoritative — no duplication, no invasive refactoring.

```solidity
mapping(address => bool) public isOffCirculationHolder;
address[] public offCirculationHolders;

function setOffCirculationHolder(address holder, bool enabled) external onlyOwner {
    // Flag + array both updated; swap-and-pop on unregister
}

function offCirculation() public view returns (uint256) {
    uint256 total = canonicalLocked;
    uint256 len = offCirculationHolders.length;
    for (uint256 i = 0; i < len; i++) {
        total += balanceOf(offCirculationHolders[i]);
    }
    return total;
}
```

**How to apply:** Any time you have a canonical tracker that misses tokens held by external contracts.

- Cost is O(n) per call where n is the number of registered holders (bounded — usually 3-10 in practice)
- Gas is only paid when the view is called (issuance distribute, preview, etc.) — not per-transfer
- Zero changes to downstream contracts
- Single source of truth: `balanceOf()` is authoritative

## When NOT to Use

- **High-frequency reads**: If the aggregator is called on every transfer, the O(n) cost compounds. Cache or use event-based sync instead.
- **Overlapping accounting**: If the external contract already exposes its balance separately (e.g., `DAOShelter.totalDeposited()`) and your controller queries that, registering would double-count. Check for existing separate queries first.
- **Untrusted holders**: The holder could donate tokens to itself to inflate `offCirculation()`. In VibeSwap's case, only governance-controlled contracts are registered, so this is acceptable. For trust-minimized systems, use a pull-based stake() mechanism.

## In-Flight Risk

When a user `transferFrom(user, nci, amount)` — between the transfer and NCI's internal bookkeeping, `offCirculation()` already reflects the new balance. This is correct behavior for the emission split but worth noting: there's no atomic "staked vs. in-flight" distinction.

## Upgrade Safety

The pattern is additive — new state variables, new functions, no changes to existing storage layout. Reduce the `__gap` by the number of new slots (mapping + dynamic array = 2 slots).

## Deploy Order

1. Upgrade token contract (additive, gap-safe)
2. Upgrade downstream consumer (switches to new view)
3. Call `setOffCirculationHolder()` for each registered holder

Must happen within one "settlement window" (epoch, block interval) to avoid under-count during transition.

## Reference

- `CKBNativeToken.offCirculation()` — canonical implementation
- `SecondaryIssuanceController.distributeEpoch()` — consumer that uses it
- `script/RegisterOffCirculationHolders.s.sol` — post-upgrade admin task
- `test/monetary/OffCirculation.t.sol` — 17 tests
- `test/consensus/IssuanceWithOffCirculation.t.sol` — 3 integration tests

Closed C7-GOV-001 (HIGH) and C7-GOV-007 (MED) in a single architectural change.
