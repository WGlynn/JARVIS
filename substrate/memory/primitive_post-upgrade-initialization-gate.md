---
name: Post-Upgrade Initialization Gate
description: When adding storage to an upgradeable contract, require an explicit reinitializer(N) for any new slot whose semantic default is NOT the zero-value. Unguarded zero-state is a security hazard, not a safe default.
type: primitive
originSessionId: 5ba12ced-49bc-424a-9145-a73ee63cbeb6
---
# Post-Upgrade Initialization Gate

## The Rule

**When adding a new storage variable to an upgradeable contract, ask: "what does the zero value of this slot *mean*?" If it doesn't mean what the rest of the contract assumes — add a `reinitializer(N)` function, package it into the `upgradeToAndCall` payload, and gate the affected code paths on a completion flag.**

Do NOT rely on:
- Code comments warning the admin to "remember to call setX after upgrade"
- Separate post-upgrade scripts run by humans
- The absence of test coverage for the "admin forgot" scenario

These are all human-error vectors. The upgrade transaction must itself bring the new slot into a valid state.

## Why

When a proxy is upgraded, the new implementation's `initialize()` does NOT re-run (OpenZeppelin's `initializer` modifier reserves version 1 permanently after first use). Newly-added storage slots inherit the EVM default (zero). For a freshly-deployed proxy, `initialize()` sets them. For an upgrade, nothing sets them.

If the zero value happens to match the semantic default (e.g., a new `uint256 public totalFoo` counter — zero is correct pre-use), no action is needed. But many additions don't have this property:

| Added field | Zero value means | What the contract assumes |
|-------------|------------------|---------------------------|
| `totalActiveInternalJul` (backing counter) | 0 active backing | Every active receipt's backing is tracked here |
| `maxInternalPerEpoch` (rate limit) | 0 = deny all | Bridge operates normally |
| `kycApproved[user]` (allowlist) | all users blocked | Pre-existing users remain approved |
| `paused` (new flag) | not paused | Undefined — depends on circuit-breaker intent |

In each case, the post-upgrade zero state is a footgun: either a rug opportunity (legacy obligations unseeded → owner drains), a DoS (all calls revert), or an invariant violation.

## The Pattern

### 1. Add a completion flag

```solidity
/// @notice Set to true by either initialize() (fresh deploy) or
///         migrateX() (upgrade path). Used to gate affected code.
bool public xMigrationComplete;
```

### 2. Initialize set the flag for fresh deploys

```solidity
function initialize(...) external initializer {
    // ...
    xMigrationComplete = true; // fresh deploys are already "migrated" (no legacy state)
}
```

### 3. Add a reinitializer for upgrades

```solidity
function migrateX(/* params needed to seed new storage */) external reinitializer(2) onlyOwner {
    require(/* input validity */);
    if (xMigrationComplete) return; // fresh deploy called into it, no-op

    // ... seed new storage from legacy state ...

    xMigrationComplete = true;
}
```

Use `reinitializer(2)` (OZ >= 4.8) so the function can be called exactly once per proxy, in sequence after `initializer` (version 1).

### 4. Gate affected code paths on the flag

```solidity
function withdrawJul(uint256 amount) external onlyOwner nonReentrant {
    require(xMigrationComplete, "Legacy migration pending");
    // ... rest ...
}
```

Gate the MINIMAL set of functions affected by the new storage — don't gate everything. Unrelated read-only views should remain available.

### 5. Package reinitializer with upgrade

Governance calls:
```solidity
proxy.upgradeToAndCall(newImpl, abi.encodeCall(NewImpl.migrateX, (arg1, arg2)));
```

Not:
```solidity
proxy.upgradeTo(newImpl);         // DANGER: window where migration is unrun
proxy.call(migrateX.selector, ...); // Human sequencing error possible
```

The `upgradeToAndCall` puts the upgrade and migration in ONE transaction. If the migration reverts, the upgrade reverts.

## Applied Instances

| Finding | Contract | New Storage | Zero-State Hazard | Fix |
|---------|----------|-------------|-------------------|-----|
| C9-AUDIT-1 (CRIT) | JarvisComputeVault | `totalActiveInternalJul` | Backing check `>= 0` always passes → owner drains legacy depositors | `backingMigrationComplete` + `migrateToInternalBacking(receiptIds, scalar)` |
| C9-AUDIT-3 (MED) | JULBridge | `maxInternalPerEpoch` | Every bridge() reverts → DoS until owner calls setter | `initializeV2(initialInternalLimit)` |

Both fixes follow the same shape: completion flag / reinitializer / upgradeToAndCall packaging.

## Detection Rule

For every PR that adds storage to an upgradeable contract:

1. **List the new slots**. What does each store?
2. **Map each slot's zero value to its semantic meaning**. Does that meaning match the contract's expectations immediately after upgrade?
3. **If not**, the PR must add:
   - A completion flag (or an equivalent invariant check)
   - A `reinitializer(N)` function that seeds the slot correctly
   - A gate on affected code paths
   - A note in the upgrade runbook: "This upgrade MUST be packaged as `upgradeToAndCall(newImpl, abi.encodeCall(migrateX, ...))`."

If the PR doesn't address these, the review is blocked.

## Anti-Patterns

**"Admin will remember"**: NatSpec that says "Owner MUST call `setX` after upgrade" is not enforcement. It's documentation. A transaction that doesn't run is not a bug in documentation — it's a vulnerability.

**"Default is safe"**: Treating EVM zero as a "safe default" because "nothing happens" is wrong. Zero-state often means "no liability tracked" which is exactly the attacker's preferred state (no obligation to honor → free withdrawal).

**"We'll deploy fresh each time"**: Mainnet proxies ARE upgraded. Assuming fresh deploys is fine for testnets; production systems must handle the upgrade path or explicitly refuse it.

**Why:** Upgradeable contracts rarely get one shot. The window between "new implementation is live" and "admin runs migration script" is a vulnerability window if anything consequential can happen in that window.

**How to apply:** Every storage addition needs the four checks above. If you can't answer the zero-state-semantics question, don't merge the PR — design is incomplete.
