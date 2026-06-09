---
name: Revenue Architecture Decisions (Session 067)
description: Canonical revenue rules — swap fees 100% to LPs, bridge fees 0%, other ecosystem revenue TBD. Three competing FeeRouter contracts need reconciliation.
type: project
---

## DEX Swap Fees: 100% to LPs. Period.

**Decision (Will, 2026-03-17):** "the dex swap fee revenues definitively go 100%. we will find other revenue sources for everything else. the ecosystem is fucking massive"

**Why:** Zero extraction is a P-000 axiom. LPs are the backbone. Taking from their fees to fund insurance/treasury/staking would make VibeSwap no different from Uniswap.

**How to apply:** Never route any portion of LP swap fees to treasury, insurance, stakers, buyback, or any non-LP destination. `protocolFeeShare` must remain 0.

## Bridge Fees: 0%. Always.

**Decision (Will, 2026-03-17):** "yeah bridge fees 0%. we aren't extracting ever."

**Why:** Same principle. Users only pay LayerZero gas (pass-through, not our revenue).

**How to apply:** VibeBridge, VibeCrossChainSwap, CKB bridge SDK all set to 0 fee. Never show bridge fee revenue on treasury/revenue pages.

## Revenue Sources for Non-LP Things (TBD)

Will is thinking about how to fund: treasury, insurance, staking rewards, buyback, mind contributors.

Current candidates (not yet decided):
- Priority bid revenue (from commit-reveal auction priority mechanism)
- Penalty redistributions (50% slashing of invalid reveals)
- SVC marketplace fees (VibeMarket, VibeGig — separate products, not DEX)
- Compute fees (Wardenclyffe inference, JUL mining)
- Voluntary tip jar

**Three competing FeeRouter contracts exist** with different splits — FeeRouter.sol, VibeFeeRouter.sol, VibeFeeDistributor.sol. Will needs to decide which is canonical. Until then, don't commit to specific split percentages in frontend or docs.

## What This Means for Frontend/Docs

- Revenue pages should show priority bid revenue and penalty redistributions as primary sources
- Don't show specific split percentages until Will decides the canonical split
- Never show "swap fee revenue" or "bridge fee revenue" as protocol income
