---
name: Unbonding Slash Completeness
description: Slashing must cover ALL token states (staked + unbonding + pending) not just the currently-staked portion
type: feedback
originSessionId: 7a39bf11-01d1-433e-8d9b-d501620892f6
---
## Unbonding Slash Completeness

When a protocol has multi-phase token states (staked → unbonding → withdrawable), slashing that only touches the "staked" state creates an escape hatch. Validators can move tokens to "unbonding" before misbehaving, reducing effective slash to near-zero.

**Why:** C7-GOV-010 found that NCI's `_slashEquivocator()` only slashed `v.stakedVibe` (50%), ignoring `unbondingAmount`. A validator who requested withdrawal of 90% of their stake BEFORE equivocating would only be slashed on the remaining 10% — reducing the penalty from 50% to ~5%.

**How to apply:** Any slashing function must enumerate ALL token states for the slashed entity:
1. Currently staked (active)
2. In unbonding/cooldown (pending withdrawal)
3. In pending rewards (unclaimed)
4. In any other intermediate state

Apply the slash proportionally to each. The slash percentage should be the same across all states — a token in unbonding represents the same security commitment as a staked token until the unbonding period completes.

Related: [Running Total Pattern](primitive_running-total-pattern.md) — also tracks aggregate state across partitions.
