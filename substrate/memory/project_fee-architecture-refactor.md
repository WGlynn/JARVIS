---
name: Fee Architecture Refactor (2026-04-02)
description: FeeRouter stripped to 100% LP passthrough. FeeController added — PID auto-tuning fees from measured IL. VIBE never touches the fee pipeline. Fee agnostic.
type: project
---

## Fee Architecture Refactor

**FeeRouter**: Stripped from 4-bucket split (40% treasury, 20% insurance, 30% revShare, 10% buyback) to single-destination passthrough. 100% of swap fees go to LPs via ShapleyDistributor. Fee agnostic — fees stay in whatever token the trade generated them in.

**Buyback-and-burn removed**: Protocol-level buyback is value redistribution, not value creation. Individuals can buy/burn voluntarily. The protocol has no opinion about VIBE's price.

**FeeController (NEW)**: PID-tuned fee auto-adjustment based on measured impermanent loss.
- ILMeasurement library: computeIL, computeILFromReserves, EWMA smoothing
- PID controller: P (tracks current IL), I (corrects accumulated error), D (anticipates volatility)
- Per-pool state, floor at 1 BPS, ceiling at 50 BPS
- Wired into VibeAMM via _getBaseFee() — reads from controller on every swap/batch/PoW path
- Stable pairs converge toward gas cost. Volatile pairs adjust upward. No governance vote.

**The principle**: The fee is a measurement, not a parameter. It equals what LPs actually sacrifice, nothing more.

**Why:** Will's directive from day 1 was 100% fees to LPs. The old FeeRouter contradicted this. FeeController emerged from first-principles reasoning: if VibeSwap's batch auction reduces IL, the fair fee is lower than other DEXs — but how much lower? Measure it.

**How to apply:** All fee-related work should respect these constraints. VIBE never enters the fee pipeline. No protocol extraction. Fee auto-tunes from reality.
