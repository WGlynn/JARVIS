---
name: Phantom Array Antipattern
description: Append-only storage arrays that use an `active` flag for membership instead of physical removal cause loops to iterate "phantom" (logically dead) entries — eventually bricking any function that iterates the array. Extracted from C24 (3 instances surfaced in one scan); all 3 closed in C25 via same template.
type: primitive
originSessionId: 3f731476-3cfc-4cea-97e7-84c17cd7bd13
---
# Phantom Array Antipattern

## The Rule

**When a storage array represents a set of active entities, membership must be encoded by POSITION in the array, not by a FLAG on the entity. Every deactivation MUST remove the entity from the array via swap-and-pop.**

```solidity
// Bad — phantom entries accumulate forever
address[] public validatorList;
mapping(address => Validator) _validators;

function deactivate() external {
    _validators[msg.sender].active = false;   // phantom remains in array
    activeCount--;
}

function _iterate() internal {
    for (uint i; i < validatorList.length; i++) {
        if (_validators[validatorList[i]].active) { /* work */ }
        // else skip — but you still paid SLOAD + branch
    }
}
```

```solidity
// Good — swap-and-pop keeps array aligned with active set
mapping(address => uint256) _indexPlusOne;  // 1-indexed; 0 = not in list

function deactivate() external {
    _validators[msg.sender].active = false;
    activeCount--;
    _removeFromList(msg.sender);
}

function _removeFromList(address addr) internal {
    uint256 idxPlus1 = _indexPlusOne[addr];
    if (idxPlus1 == 0) return;
    uint256 idx = idxPlus1 - 1;
    uint256 lastIdx = list.length - 1;
    if (idx != lastIdx) {
        address lastAddr = list[lastIdx];
        list[idx] = lastAddr;
        _indexPlusOne[lastAddr] = idx + 1;
    }
    list.pop();
    _indexPlusOne[addr] = 0;
}
```

## Why

Three instances surfaced in one C24 scan:
1. `NakamotoConsensusInfinity.validatorList` — `advanceEpoch` is permissionless and calls `_checkHeartbeats` which iterates the full array; deactivation only flipped `.active`. An attacker (or just organic growth) can brick consensus by inflating the array. HIGH.
2. `HoneypotDefense.trackedAttackers` — grows forever, `getDefenseStats` iterates; currently view-only but the pattern is a trap if iteration moves to a write path. MED.
3. `VibeAgentOrchestrator._activeWorkflowIds` — identical shape; no current DoS, architectural debt. MED deferred.

All three share the same source-code structure:
- Storage array grows via `push` on a public/permissionless entry point.
- Entries carry an `active` or equivalent flag.
- Deactivation flips the flag, does NOT shrink the array.
- A loop somewhere reads `arr.length`, iterating phantom entries.

Eventually the loop consumes more gas than a block allows. If the loop is called by a critical path (consensus advancement, settlement), the contract bricks.

## When It Applies

All three must hold:
1. **Append-only write path** — entries are added via `push` on a function that users can reach (directly or transitively).
2. **Iteration somewhere** — a function reads the array in a `for` loop, whether as a view or a state-mutator.
3. **Flag-based deactivation** — entries become "inactive" via a boolean mutation, with no physical removal from the array.

If (1) fails, the array is bounded by config — no attacker vector. If (2) fails, array size is pure storage overhead with no DoS surface. If (3) fails, the pattern already matches good practice.

## State Invariants

1. **Index monotone**: `_indexPlusOne[x] > 0` iff `list[_indexPlusOne[x] - 1] == x`.
2. **No duplicates**: membership check at insert via `require(_indexPlusOne[x] == 0)`.
3. **Pop order independence**: code that iterates the list must NOT assume order is stable across calls — swap-and-pop reorders entries.
4. **Defense cap in depth**: a `MAX_ENTRIES` constant is still warranted as a second-layer bound. Swap-and-pop alone doesn't prevent registering attackers from inflating the array while they stay active; the cap does.

## Applied Instances

| Contract | Array | Status |
|----------|-------|--------|
| NakamotoConsensusInfinity | `validatorList` | ✅ FIXED (C24-F1) — swap-and-pop on `deactivateValidator`, `slashEquivocation`, and `_checkHeartbeats`; `MAX_VALIDATORS = 10_000` cap on `registerValidator`. |
| HoneypotDefense | `trackedAttackers` | ✅ FIXED (C25-F3) — swap-and-pop on `revealTrap` (terminal state); `MAX_TRACKED_ATTACKERS = 10_000` cap on `_escalateThreat`. Closes the view-only DoS surface. |
| VibeAgentOrchestrator | `_activeWorkflowIds` | ✅ FIXED (C25-F4) — swap-and-pop on `executeStep` COMPLETED path and `failStep`; `MAX_ACTIVE_WORKFLOWS = 10_000` cap on `activateWorkflow`. Storage gap shrunk 50→49 for new `_activeWorkflowIndex` mapping. Mechanical fix only — the architectural question (events-vs-onchain indexing) remains open but no longer blocks the phantom-array debt. |

## Candidates for Future Application

- `ShardOperatorRegistry` operator/shard arrays — verify membership-by-position holds.
- Any "pending queue" in governance/bridge/settlement that grows monotonically.
- `UtilizationAccumulator` if it tracks participant history.

## Design Traps to Avoid

- **"The flag is enough, we'll paginate later"**: pagination is a worse fix than removal because it introduces state for the pagination cursor, which can itself desync. Swap-and-pop is one helper function.
- **Forgetting a deactivation site**: in NCI, three separate sites deactivate (`deactivateValidator`, `slashEquivocation`, `_checkHeartbeats`). All three must call the helper. Grep for `.active = false` to find them.
- **1-indexed mapping confusion**: using 0 as "not in list" sentinel requires index stored as `index+1`. Off-by-one on reads/writes will silently corrupt.
- **Iteration concurrent with removal**: if the same function iterates AND removes during the loop, the index cursor must NOT increment after a removal — the slot now holds a new entity. Use `while (i < list.length)` with `continue` on removal.
- **View-only DoS**: even a pure view can brick if off-chain systems depend on it (indexers, frontends, scoring). "Only a view function" is not a full defense.

## Relation to Other Primitives

- **Cleanup-Duty Density** — that primitive flags "named function doesn't move value correctly." Phantom Array is the structural twin — "named array doesn't reflect actual membership."
- **Settlement State Durability** — same philosophy: physical state must match logical state, flags alone are not enough.
- **Discovery Ceiling** — Phantom Array is a class-level finding (one scan, three instances). Class-level bugs reward scans that explicitly look for structural patterns across files, not per-contract audits.

## How to Apply

When reviewing any contract with `address[]` or similar storage arrays:
1. Grep for `push(` on that array — is the push path user-reachable?
2. Grep for `.length` on that array in any `for` loop — is that loop in a write path or a critical view?
3. Grep for `.active = false` or equivalent deactivation patterns — do they call a `_removeFromList` helper?
4. If any of the above is "yes, yes, no" — you have a Phantom Array.

**Meta:** the cheapest way to find these at scale is a cross-file scan: find every pair of `push` + iterate-by-length, check the deactivation path. The C24 scan did this in one pass and found 3 instances. Future pre-deploy audits should include this scan by default.

## Validation (C25 — class closure)

C25 applied the same template (`_removeFrom<List>` helper + index-plus-one mapping + MAX cap constant) across both C24-deferred instances. Template reused verbatim with only three substitutions: (a) struct being tracked, (b) list variable name, (c) MAX constant name. Zero regressions across both suites (HoneypotDefense 14→17 tests, VibeAgentOrchestrator 48→51 tests). Confirms the primitive is a reusable template, not just a post-hoc description of three coincidences. At n=3 closed with identical template, library extraction is now justified — candidate for a PhantomArrayGuard mixin.
