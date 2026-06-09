---
name: TWAP depeg detector
description: Time-weighted average price ring buffer; spot vs TWAP deviation triggers circuit breaker. Robust to single-block manipulation, responsive to real depeg.
type: primitive
originSessionId: 05f950b5-8ab9-47f5-a2b2-b8336ce1e9ef
---
# TWAP-depeg-detector

## Rule
- TWAP > spot ⇒ smoothed view of price
- spot vs TWAP deviation > threshold ⇒ depeg signal
- ⇒ trigger circuit breaker
- single-block manipulation ✗ moves TWAP enough to false-signal

## Source
- `vibeswap/contracts/libraries/TWAPOracle.sol` (272 LOC)
- ring-buffer w/ configurable window (5m → 24h)
- auto-cardinality growth (line 56: prevents infinite overwrite)
- pure library; protocol-agnostic

## Mechanism
- ingest price observation per block (or sample interval)
- store in ring buffer of size N
- TWAP = Σ(price × duration) / Σ(duration) over window
- query: current TWAP vs current spot ⇒ deviation BPS
- threshold breach ⇒ trigger downstream action (e.g., circuit breaker)

## Why ring buffer (not unbounded array)
- O(1) insert (overwrites oldest)
- O(N) query but N bounded by window
- ¬ unbounded growth ⇒ ¬ DoS surface
- auto-cardinality growth ⇒ window can extend without redeployment

## USD8 application: depeg detection on USDC reserve
- sample USDC/USD price (Chainlink, Pyth, etc.) per block
- compute TWAP over 1-hour window
- spot vs TWAP > 50bps ⇒ trip COVER_ADEQUACY breaker (per circuit-breaker primitive)
- ⇒ Cover Pool pauses pending attested-resume
- protects USD8 from accepting depegged collateral

## Port-class
- DIRECT-PORT (pure library; supply price source + initial seed)
- effort: hours
- audit posture: pattern same as Uniswap v3 TWAP, well-vetted

## When ✓ TWAP (vs spot)
- need robustness to single-block manipulation
- adversary can move spot but ¬ move TWAP cheaply
- depeg = sustained deviation, ¬ instant spike
- ⇒ TWAP is the right measure

## When ✗ TWAP (use spot)
- need sub-block latency (rare for stablecoin protocols)
- legitimate sudden price moves (e.g., flash announcements)
- spot is the only source available

## Triggers
- "how do we detect depeg?"
- "what's the price oracle?"
- USDC / underlying-collateral risk discussion
- Cover Pool circuit-breaker design

## Anti-pattern
- ✗ spot-only price gate (single-block manipulation)
- ✗ unbounded observation array (DoS)
- ✗ TWAP without configurable window (one-size-fits-all)

## Related
- circuit-breaker-attested-resume (downstream consumer)
- substrate-geometry-match (smoothing curve matches the depeg substrate)
- off-chain-storage-onchain-commitment (TWAPOracle is small enough to live on-chain; not all oracles need this)
