---
name: Verified compute with bonded dispute window
description: Off-chain compute submits result + bond; dispute window opens; un-disputed ⇒ finalize; disputed ⇒ slash.
type: primitive
originSessionId: 05f950b5-8ab9-47f5-a2b2-b8336ce1e9ef
---
# VerifiedCompute (bonded dispute)

## Rule
- off-chain compute ⇒ submit result + bond
- dispute window opens ⇒ any observer can challenge w/ counter-proof
- ¬ challenge ⇒ finalize after window
- ✓ challenge ⇒ slash bond, reject result

## Source
- `vibeswap/contracts/settlement/VerifiedCompute.sol` (195 LOC)
- abstract base contract; substrate-agnostic
- pattern: same as Tornado Cash proof finalization, modern ZK rollup settlement

## State machine
- None → Pending (on submission)
- Pending → Finalized (window elapsed, no dispute)
- Pending → Disputed (challenge submitted)
- Disputed → resolved (counter-proof verified ⇒ slash; ¬ verified ⇒ finalize)

## Bond mechanics
- submitter posts stake against result correctness
- SLASH_RATE = 50% (configurable)
- successful challenger receives portion of slashed bond
- ⇒ economic invariant: false submission costs more than expected gain

## USD8 application: Brevis-integrated Cover Score flow
- Brevis circuit computes Cover Score off-chain
- submitter (claimant or keeper) bonds stake against the proof
- 24-hour dispute window
- ¬ disputed ⇒ score finalized ⇒ claim settles
- ✓ disputed (counter-proof of computation error) ⇒ slash submitter ⇒ reject score

## Port-class
- WRAPPER-NEEDED
- abstract base ports as-is
- USD8-specific subclass: `CoverScoreVerifiedCompute`
- wrapper defines: Brevis proof verification, role gating, dispute mechanic specifics
- effort: 3-5 days for wrapper + tests + Brevis integration

## Why this beats trust-the-prover
- pure trust ⇒ prover lies ⇒ undetected
- trust + dispute ⇒ prover lies ⇒ challenger profits ⇒ ¬ profitable to lie
- bond economics enforce honesty without requiring trusted-prover whitelist

## When ✓ this pattern
- off-chain compute with on-chain settlement
- result is publicly verifiable (anyone can re-run to challenge)
- claim cadence allows dispute window (≥hours)

## When ✗
- sub-second finality required (no dispute window possible)
- result only verifiable by trusted parties (no challenger pool)
- bond economics ¬ work (e.g., result gain >> any feasible bond)

## Triggers
- "off-chain compute integration"
- "ZK coprocessor pattern"
- Brevis / RISC Zero / SP1 / Axiom integration discussion
- Cover Score settlement flow design

## Anti-pattern
- ✗ off-chain compute with no dispute mechanism (trust-the-prover)
- ✗ centralized whitelist of approved provers (capture surface)
- ✗ no slashing (no economic deterrent to lying)

## Related
- IssuerReputationRegistry (reputation layer pairs with bond layer)
- merkle-commit-dispute-finalize (parent pattern)
- off-chain-storage-onchain-commitment (architectural sibling)
