---
name: Rebase-Invariant Accounting
description: Any quantitative gate or backing check against a rebasing token must anchor in pre-rebase (internal) units; external amounts drift with monetary policy and silently weaken or strengthen the invariant.
type: primitive
originSessionId: 5ba12ced-49bc-424a-9145-a73ee63cbeb6
---
# Rebase-Invariant Accounting

## The Rule

**When a contract enforces a quantity-based invariant over a rebasing token, the invariant must be denominated in rebase-invariant (pre-rebase / internal) units — never in external display amounts.**

Applies to:
- Backing / collateralization checks ("does the vault still hold ≥ N JUL worth of deposits?")
- Rate limits ("max K JUL per epoch")
- Reserve ratios, insolvency guards, liquidity thresholds
- Any accounting where "the same amount, later" must mean the same economic quantity

## Why

A rebasing token like Joule has a global `rebaseScalar` that multiplies internal (raw) balances to produce external (display) balances:

```
externalBalance(account) = internalBalance(account) * rebaseScalar / 1e18
```

The scalar changes whenever the monetary policy fires (demand shock absorption, PI controller adjustment, Moore's Law decay, etc.). External balances change without any token movement.

**Every external-unit measurement is time-sensitive.** Two snapshots of `balanceOf(X)` taken at different times may compare apples to oranges.

If an invariant is expressed in external units:
- **Positive rebase** (scalar ↑): existing balances grow. Backing checks pass that shouldn't (the *gain* belongs proportionally to depositors, not the contract). Rate limits admit *less* real quantity than intended.
- **Negative rebase** (scalar ↓): existing balances shrink. Backing checks fail that shouldn't. Rate limits admit *more* real quantity than intended (up to 2x in observed cases).

Internal balances are rebase-invariant: no rebase changes them. They track the raw token state and the economic reality of "how much work-equivalent token is actually here."

## The Pattern

Joule exposes both views:
```solidity
interface IJoule {
    function balanceOf(address) external view returns (uint256);           // external, rebased
    function internalBalanceOf(address) external view returns (uint256);   // rebase-invariant
}
```

For any accounting:

```solidity
// WRONG — drifts with rebase scalar
uint256 backing = token.balanceOf(address(this));
require(backing >= required, "undercollateralized");

// RIGHT — rebase-invariant
uint256 internalBacking = IJouleInternal(token).internalBalanceOf(address(this));
require(internalBacking >= internalRequired, "undercollateralized");
```

For measuring a transfer's effect:

```solidity
uint256 internalBefore = IJouleInternal(token).internalBalanceOf(address(this));
token.transferFrom(from, address(this), externalAmount);  // user pays in display units
uint256 internalAfter = IJouleInternal(token).internalBalanceOf(address(this));
uint256 internalDelta = internalAfter - internalBefore;   // rebase-invariant credit

// Gate, account, and store in internal units
internalConverted += internalDelta;
require(internalConverted <= internalLimit, "rate limited");
```

## Applied Instances

| Finding | Contract | Invariant | Pre-Fix (broken) | Post-Fix |
|---------|----------|-----------|------------------|----------|
| C7-GOV-006 (HIGH) | JarvisComputeVault | Backing ≥ active credits | `balanceOf(vault) >= creditsIssued / CREDITS_PER_JUL` (external, drifts) | `internalBalanceOf(vault) >= totalActiveInternalJul` |
| C7-GOV-005 (MED) | JULBridge | Max bridge volume per epoch | `convertedThisEpoch + julAmount <= maxPerEpoch` (external, drifts) | `internalConvertedThisEpoch + internalDelta <= maxInternalPerEpoch` |

Both fixes used the same shape: measure `internalBalanceOf` before/after the transfer, gate on the delta.

## Upgrade Safety

When adding rebase-invariant tracking to an upgradeable contract:

1. **Add new storage slots** for internal counters (`*Internal` suffix). Don't reuse old slots with shifted semantics — semantic mutation of live storage is a migration hazard.
2. **Reduce the `__gap` accordingly**, append-only.
3. **Keep old external-unit state** as deprecated trackers for view consumers. Mark with a `@dev DEPRECATED` NatSpec comment pointing to the new active gate.
4. **Default new caps to 0** or require owner initialization post-upgrade. "Deny by default until owner calibrates" is safer than inheriting stale values with new semantics.
5. **Emit a parallel `*Internal` event** carrying both internal and external amounts so off-chain indexers can migrate gradually without losing context.

## Detection Rule

For any contract that holds or transfers a rebasing token, grep for:
- `balanceOf(` on the rebasing token where the result feeds a comparison, division, or stored accumulator
- `amount` fields stored across time that came from external `transfer`/`transferFrom` parameters

Each hit is a candidate for rebase-induced drift. Replace with `internalBalanceOf` / measured internal delta.

**Why:** External-unit accounting on a rebasing token is a silent invariant break — it doesn't revert, it just drifts. Tests at default scalar pass. Real mainnet with an active rebase controller silently violates the intent.

**How to apply:** Any time you see a rebasing token in a contract's state, trace every quantity-based invariant. If the invariant references external units (`balanceOf`, raw `amount` stored across time), rewrite in internal units. If the invariant references a *fresh* snapshot used only within a single transaction (no cross-time comparison), external units are safe — just don't persist them for later comparison.
