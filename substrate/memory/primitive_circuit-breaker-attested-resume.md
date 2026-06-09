---
name: Circuit breaker with attested resume
description: Multi-level emergency pause; cooldown = floor ¬ guarantee; resume requires explicit safety attestation.
type: primitive
originSessionId: 05f950b5-8ab9-47f5-a2b2-b8336ce1e9ef
---
# CircuitBreaker (attested-resume)

## Rule
- emergency pause ⇒ multi-level (per-breaker-type)
- cooldown ⇒ floor ¬ trigger
- resume ⇒ requires attestation, ¬ automatic
- ⇒ closes auto-resume-during-stress failure mode

## Source
- `vibeswap/contracts/core/CircuitBreaker.sol` (478 LOC)
- C43 attested-resume cycle; lines 52-59 flag the pattern
- VibeSwap production primitive

## Breaker types (multi-level)
- VOLUME (anomaly detection)
- PRICE (manipulation detection)
- WITHDRAWAL (bank-run detection)
- LOSS (insolvency detection)
- TRUE_PRICE (oracle deviation)
- + Shapley fairness deviation (extension)

## Auto-resume failure mode (what attestation prevents)
- breaker trips ⇒ cooldown elapses ⇒ ¬ check underlying ⇒ auto-resume
- ⇒ underlying condition may persist
- ⇒ resume mid-stress = catastrophic
- ⇒ historical incident-response failures map here

## Attested-resume mechanism
- breaker tripped ⇒ STOPPED state
- cooldown timer = required-but-insufficient
- explicit attestation from configured set required to re-enable
- attestor evaluates underlying condition resolved
- ⇒ resume only when condition genuinely cleared

## Port-class
- DIRECT-PORT (rename breaker types per substrate; configure attestor set)
- USD8 mapping:
  - LOSS → COVER_INSOLVENCY
  - TRUE_PRICE → COVER_ADEQUACY
  - VOLUME → CLAIM_RATE
  - WITHDRAWAL → POOL_WITHDRAWAL

## Effort
- 1-2 days (rename + tests + audit checkpoint)

## Triggers
- emergency-pause discussion (any protocol)
- "what happens during stress event?"
- depeg detection / Cover Pool insolvency / mass-claim flow
- pre-deployment readiness review

## Anti-pattern
- ✗ pure cooldown auto-resume
- ✗ admin-only resume w/ no attestation framework
- ✗ single-breaker monolith (vs multi-level per-trigger)

## Related
- TWAP-depeg-detector (feeds the TRUE_PRICE breaker)
- settlement-state-durability (what the attestor protects against)
- augmented-mechanism-design (Type 3 Temporal invariant)

## VibeSwap audit observation 2026-04-27
- event asymmetry: manual reset emits `BreakerDisabled`, attested resume emits `BreakerResumedByAttestation`
- ⇒ off-chain monitoring sees one but not the other
- ⇒ recommended: align via single `BreakerStateChanged(type, active, reason)` OR emit both
- minor finding, not load-bearing
