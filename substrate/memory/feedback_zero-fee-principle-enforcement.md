---
name: Zero Protocol Fee Principle — Absolute Enforcement
description: NEVER generate content implying VibeSwap charges protocol fees. 0% protocol fee is a P-000 level axiom. AI defaults to industry-standard fee models (Uniswap 0.3%, taker/maker tiers) which directly violate this principle.
type: feedback
---

## Rule: VibeSwap charges ZERO protocol fees. 100% of LP trading fees go to liquidity providers. Always. No exceptions.

**Why:** Session 067 discovered 23 direct violations and 9 misleading references across 32+ files — including DeployProduction.s.sol which would have deployed with 10% protocol fees on mainnet. This happened because AI pattern-matches to DeFi industry norms (Uniswap 0.3%, taker/maker fees, protocol revenue shares) when generating pages, docs, deploy scripts, and papers. Will considers this a P-000 (Fairness Above All) violation: "our zero fee principle is so fucking important. you keep accidentally sneaking fees into it it's actually driving me nuts"

**How to apply:**
1. When generating ANY frontend page, doc, paper, grant, deploy script, or bot response:
   - NEVER use "protocol fee" to describe revenue VibeSwap collects from swaps
   - NEVER use "taker fee" / "maker fee" — VibeSwap doesn't have this distinction
   - NEVER show 0.3% as VibeSwap's fee (that's Uniswap's)
   - NEVER claim stakers/treasury/DAO earn from "protocol fees" or "swap fees"
2. DAO treasury revenue sources are ONLY: priority bid revenue, auction proceeds, penalty redistributions (50% slashing)
3. LP fee (default 0.05%) is set per pool by creators — 100% goes to LPs, 0% to protocol
4. `protocolFeeShare` in VibeAMM.sol MUST remain 0 — never set it nonzero in deploy scripts
5. When comparing to competitors, explicitly state "0% protocol fee" as the differentiator
6. The term "protocol fee" should only appear in contexts that say it equals zero

**Pattern to watch for:** Any time content is generated at scale (bulk pages, papers, docs), audit for this violation. The AI's statistical prior WILL default to fee-charging patterns.
