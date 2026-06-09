---
name: Running Total Pattern
description: Replace O(n) aggregation loops with O(1) running totals maintained at mutation points — prevents gas DoS via unbounded iteration
type: feedback
---

Running Total: never iterate an unbounded list to compute an aggregate when you can maintain it incrementally.

**Why:** NCI-007/008 found that `_getTotalActiveWeight()` and `_checkHeartbeats()` iterated the entire `validatorList` on every call. Combined with free registration (NCI-002), an attacker could inflate the list until these functions exceeded the gas limit, permanently bricking consensus.

**How to apply:** When a value is the sum/aggregate of a dynamic set:
1. Store the aggregate as a state variable
2. Increment it when an element is added/activated
3. Decrement it when an element is removed/deactivated
4. Every mutation point must maintain the invariant

This applies to: totalActiveWeight, totalCellsServed, totalStaked, totalWeight — any "total" derived from iterating a list.

The pattern is obvious in retrospect but easy to miss when the list starts small. The audit found 4 unbounded loops across 2 contracts.
