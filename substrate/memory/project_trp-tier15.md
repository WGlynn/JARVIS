---
name: TRP Tier 27
description: 12-round TRP across 2 sessions. Tier 15→27. 104 findings total, 40 fixed. Core architecture gaps identified.
type: project
---

## TRP Status: TIER 27

### Session 2 (2026-04-02): Tier 15→21
- R16-18: Settlement pipeline — 17 findings, 13 fixed
- R19-20: ShapleyDistributor — 20 findings, 8 fixed. CRITICAL multi-token accounting.
- R21: CrossChainRouter — 26 findings, 3 fixed. eid/chainid mismatch.

### Session 3 (2026-04-02): Tier 21→27
- R22: CrossChainRouter cure — 6 fixed (emergency withdraw, deposit/fee separation)
- R23: ShapleyDistributor cure — 2 fixed (Lawson Floor cap, quality weight validation)
- R24: CircuitBreaker + CrossChainRouter — 26 new, 6 fixed (breaker auto-reset, commitId)
- R25: VibeAMM — 2 fixed (addLiquidity breaker, dead import)
- R26: CommitRevealAuction — verification round, 0 new fixes
- R27: Integration pass — systemic UUPS finding

**Cumulative**: ~104 findings, ~40 fixed across 12 rounds.

### Critical Open Items
1. NEW-01 CRITICAL: Phantom bridged deposits (CrossChainRouter)
2. NEW-03 HIGH: fundBridgedDeposit depositor mismatch
3. CB-02 HIGH: VibeSwapCore needs CircuitBreaker
4. INT-01 HIGH: UUPS missing on 3 core contracts
5. N03 HIGH: Quality weight front-running
6. Collateral underpricing (CommitRevealAuction, Tier 15)

**Why:** Tracks progression. **How to apply:** Next session starts from TIER 27. Summaries: `docs/trp/round-summaries/round-{16..27}.md`
