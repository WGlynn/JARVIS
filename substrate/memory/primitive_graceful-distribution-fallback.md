---
name: Graceful Distribution Fallback
description: Multi-recipient distribution pipelines must not block entirely when one recipient reverts — redirect to fallback
type: feedback
originSessionId: 7a39bf11-01d1-433e-8d9b-d501620892f6
---
## Graceful Distribution Fallback

When a distribution function sends to N recipients in one transaction (e.g., SecondaryIssuanceController splits emission 3 ways), a revert in ANY recipient blocks ALL recipients. This is the "weakest link" pattern — the least available downstream contract controls liveness for the entire system.

**Why:** C7-ISS-001 found that ShardOperatorRegistry reverts when `totalWeight == 0` (no active shards), which blocks the entire epoch distribution including DAO yield and insurance. The system went from "no shards registered" (minor) to "no secondary issuance at all" (critical).

**How to apply:** When distributing to multiple external contracts in one tx:
1. Use try/catch for each recipient
2. On catch, redirect the failed share to a designated fallback (insurance pool, treasury, etc.)
3. Never let one recipient's revert cascade to others
4. Log the fallback event for monitoring

This is the distribution equivalent of the circuit breaker pattern — degrade gracefully, don't fail totally.
