---
name: Admin Event Observability
description: Every admin setter on a deployed contract MUST emit an event with old→new values. Zero-event setters are a systemic observability bug class that breaks off-chain indexers, audit-trail reconstruction, and incident response.
type: primitive
originSessionId: a1e0e274-6aeb-4b28-9156-b6c7479e2cd3
---
# Admin Event Observability

**Rule:** every function that mutates protocol state under a privileged guard (`onlyOwner`, `onlyRole`, `onlyOperator`, etc.) MUST emit an event of the shape `<Thing>Updated(<oldValue>, <newValue>)` before returning. Address parameters use `indexed` on both old and new. Numeric parameters can emit non-indexed.

## Why

Three failure modes that silent setters enable:

1. **Off-chain blindness.** Subgraphs, explorers, Dune, and internal dashboards depend on events to materialize contract state. A silent setter means the observable state diverges from the actual state — the subgraph keeps the old value forever, explorers show stale "admin address" fields, dashboards don't trigger alerts.

2. **Incident response gap.** When something breaks — "why is this operator reward zero?" — the first signal is usually event history. No events = no timeline = no root cause without archive-node forensics.

3. **Governance accountability.** Multi-sig DAO actions are ratified by vote; the onchain emit is the receipt. Without events the action is as-if invisible after the tx receipt is forgotten.

## Discovery

Extracted from C36 access-control density scan (2026-04-21). Three instances in the recently-shipped consensus contracts:

- `ShardOperatorRegistry`: `setIssuanceController`, `setStateRentVault`, `setCellRegistry` — no events.
- `NakamotoConsensusInfinity`: `setSoulboundIdentity`, `setContributionDAG`, `setVibeCode`, `setAgentReputation`, `setCKBNativeToken`, `setJouleToken` — 6 external-contract-reference setters, no events.
- `SecondaryIssuanceController`: `setMinDistribution`, `setInsurancePool` — no events.

Total: 11 silent setters across 3 contracts. Strong n-of-3 justification per the Taxonomize rule. The pattern is clearly systemic rather than incidental.

## Enforcement

### Code-review (soft)
On any diff that introduces or modifies a function under an admin guard, check: does it emit? If not, flag and push back. Rewriters and RSI density scans should grep `^\s*function\s+(set|update)\w+.*onlyOwner` and cross-reference against `emit \w+Updated` in the body.

### Static rule (hard)
Slither detector `events-access` catches this class. Add to CI as a blocking rule once the existing surface is cleaned up.

### Template

```solidity
event XUpdated(address indexed oldX, address indexed newX);

/// @dev C36-F2: emits XUpdated for admin-action observability.
function setX(address newX) external onlyOwner {
    address old = x;
    x = newX;
    emit XUpdated(old, newX);
}
```

For numeric values:
```solidity
event MinYUpdated(uint256 oldMin, uint256 newMin);

function setMinY(uint256 newMin) external onlyOwner {
    uint256 old = minY;
    minY = newMin;
    emit MinYUpdated(old, newMin);
}
```

## Related

- **Silent setter ↔ Phantom Array class.** Both are "invisible onchain state" bugs — one hides state-change timing, the other hides unbounded growth. Different mechanisms, same observability failure mode.
- **Pairs with** `feedback_ship-time-verification-surface.md` — events are the ship-verification primitive for admin actions.
- **Not a substitute for** access-control correctness. Events observe; they don't enforce. `onlyOwner` is the guard, the event is the receipt.
