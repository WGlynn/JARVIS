---
name: Oracle Primitive Audit Rounds
description: External adversarial review on the oracle primitive (evidence bundles, issuer reputation, canonicality). R2 scope locked 2026-04-17; C12 is the R3 gate.
type: project
originSessionId: 76bb18f6-7846-4e93-9cb8-86f2e3362f78
---
External reviewer runs adversarial rounds on the oracle primitive design. Each round: feedback → triage (adopted / scoped / parked) → implementation commits → updated tuple delivered → next round.

## R1 (pre-2026-04-17) — DELIVERED
Hardening commits on oracle primitive:
- `49e7fa72`
- `117f3631`
- `61e77e66`

Terminology: **Extractive Load** adopted as public-facing name for GEV (technical substrate stays). Dual validation — DeepSeek R2 + this reviewer independently endorsed.

## R2 (2026-04-17) — SCOPE LOCKED

Reviewer verdict: primitive under active adversarial hardening, not theoretical design. Triage of R2 feedback:

| Component | Verdict | Status |
|---|---|---|
| Evidence-bundle schema enforcement | Scope for Cycle 12 | **SHIPPED** `125b01fb` |
| Stake-bonded issuer reputation | Scope for Cycle 12 | **SHIPPED** `125b01fb` |
| Social slashing delay | Opt-in fallback tier, not default | STUB-SHIPPED (`ISocialSlashingTier.sol`, enabled=false) |
| Canonicality Futures | Sketch sufficient | PARKED — see `docs/papers/canonicality-futures-sketch.md` |
| Formal verification (Certora/Halmos) | Pre-mainnet final gate | AFTER C12 + C13 |

**C12 goal**: close the gap where Batch C stopped fabricated `cellId`s; C12 stops fabricated *content within* the bundle via schema enforcement + issuer-reputation cost layer.

**Why social slashing stays opt-in**: emergency brakes that require governance can themselves become attack vectors. Trust-minimized default path preserved; governance path available as fallback tier.

## R3 Gate — OPEN (2026-04-18)

C12 shipped `125b01fb` on branch `feature/social-dag-phase-1`. Six design decisions were made with full autonomy grant:

1. **IssuerRepRegistry**: new standalone contract (not extension of ReputationOracle)
2. **Python oracle signing**: deferred to Phase 2 keeper implementation
3. **StateRentVault integration**: deferred out of C12 scope
4. **StablecoinContext hashing**: included in bundle typed data for auditability
5. **Reputation lifecycle**: penalty-only + time-based mean-reversion (MID=5000 bps, half-life=30 days); SLASHED_OUT does not auto-reactivate on decay
6. **Social slashing**: stub interface shipped with `enabled=false` default

Test results: 26 new tests pass (17 registry + 9 bundle integration), 0 regressions across 142 oracle tests.

**Ready to deliver updated tuple to reviewer**. Files 1-8 for R3:
- `contracts/oracles/IssuerReputationRegistry.sol`
- `contracts/oracles/interfaces/IIssuerReputationRegistry.sol`
- `contracts/oracles/interfaces/ISocialSlashingTier.sol`
- `contracts/oracles/interfaces/ITruePriceOracle.sol` (modified)
- `contracts/oracles/TruePriceOracle.sol` (modified)
- `test/oracles/IssuerReputationRegistry.t.sol`
- `test/oracles/TruePriceOracleC12.t.sol`
- Commit message + this memo for context

Reviewer question for R3: does evidence-bundle + issuer-reputation close the Oracle Problem seam, or does a new attack surface open?

**Sequencing**: C12 + C13 ship → formal verification → bug bounty → mainnet.

## Related
- [Extractive Load](primitive_extractive-load.md)
- [GEV Resistance](primitive_gev-resistance.md)
- [Full Stack RSI](project_full-stack-rsi.md) — parallel track
