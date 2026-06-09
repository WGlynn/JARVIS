---
name: Issuer reputation with mean-reversion
description: Stake-bonded issuer registry; reputation in BPS [0, 10000]; mean-reverts to MID=5000 over 30-day half-life. Slash subtracts BPS + burns stake. ¬ positive-reward loop.
type: primitive
originSessionId: 05f950b5-8ab9-47f5-a2b2-b8336ce1e9ef
---
# IssuerReputationRegistry

## Rule
- issuer registers ⇒ bonds stake
- reputation [0, 10000] BPS, init=MID
- slash ⇒ subtract reputation BPS + burn proportional stake
- mean-revert toward MID over half-life=30 days
- ⇒ temp slashing ¬ permanent destruction
- ¬ positive-reward loop (reputation = penalty counter, ¬ reward counter)

## Source
- `vibeswap/contracts/oracles/IssuerReputationRegistry.sol` (316 LOC)
- C12 isolation pattern (standalone, ¬ extension of ReputationOracle)
- permissioned slashing locked
- social slashing stub disabled by default

## Why penalty-only (¬ reward loop)
- positive reward loop ⇒ reputation compounds
- ⇒ founder/early-issuer dominance
- ⇒ structural barrier to new issuers
- penalty-only ⇒ everyone starts at MID, falls on misbehavior, recovers via clean operation
- ⇒ no compounding founder advantage

## Why mean-reversion
- pure penalty ⇒ slash permanent ⇒ over time, reputation pool depletes
- temp issue (e.g., short downtime) ⇒ permanent damage
- mean-reversion ⇒ recovery possible via 30 days of clean issuance
- operationally reasonable; expensive enough to deter repeat bad behavior

## Anti-slash-dodge
- 7-day UNBOND_DELAY
- ⇒ ¬ withdraw stake immediately before known-bad action
- ⇒ slash window covers unbonding

## USD8 application: Brevis attestor reputation
- each Brevis attestor bonds collateral on registration
- proof shown fraudulent (via VerifiedCompute dispute window) ⇒ slash reputation + seize collateral
- mean-reversion ⇒ temp issue ¬ ban
- ⇒ attestor pool stays healthy long-term

## Port-class
- REFINE-WITH-INPUT-REDEFINITION
- structure ✓ as-is
- substitute: stakeToken (CKB → USDC/USD8/ETH), authorized slashers (VibeSwap → Brevis verifier + Cover Score tribunal)
- effort: 2-3 days

## Constants (paper-derived)
- MID_REPUTATION = 5000 BPS (mean-reversion target)
- REPUTATION_HALF_LIFE = 30 days
- UNBOND_DELAY = 7 days
- slash_BPS configurable per offense severity

## Triggers
- "attestor reputation system"
- "oracle reputation"
- "how do we deter false attestations?"
- decentralized-attestor-set design

## Anti-pattern
- ✗ binary good/bad (¬ recovery path)
- ✗ permanent slash (no mean-reversion)
- ✗ positive-reward loop (compounding founder advantage)
- ✗ no unbond delay (slash-dodge surface)

## Related
- VerifiedCompute (the slashing trigger)
- augmented-mechanism-design (Type 2 Economic invariant)
- mechanism-design-paper (UNBOND_DELAY, REPUTATION_HALF_LIFE per §6.1)
