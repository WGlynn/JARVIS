---
name: NCI L1 Trajectory — contract-now, native-eventually
description: NCI ships first as a smart contract on an existing EVM chain (validation + augmentation). Eventual move to a native VibeSwap chain is a substrate necessity, not a graduation, driven by PoM requiring first-class protocol state.
type: project
originSessionId: a1e0e274-6aeb-4b28-9156-b6c7479e2cd3
---
# NCI L1 Trajectory

**Status:** contract-based NCI live on existing EVM chain (LayerZero omnichain). Native-chain port is a when-not-if, scoped per substrate-necessity below.

## Two frames — both true

1. **Contract-based abstraction consensus is a paradigm worth publishing.** Running a novel consensus weighting layer inside smart contracts on top of an existing chain's ordering substrate is itself an idea. Other protocols with economic-security-at-a-layer-above requirements could pattern-match on what we've shipped. Will's own words 2026-04-21: *"who knows contract based abstraction consensus could become a thing based on this."* That paper/artifact is independent of our L1 arc.

2. **The eventual L1 move is substrate-forced, not prestige-driven.** Will, same turn: *"we will eventually move to our own network obviously because our security structure is fundamentally different from any other chain."* Proof of Mind is the pivot — it's a time-accumulated, unbuyable weighting primitive whose dependencies (SoulboundIdentity, ContributionDAG, VibeCode, AgentReputation) are first-class protocol state, not oracle reads. EVM chains track balances and contract storage; they don't track PoM state at the base layer. Running PoM as a contract primitive means every consensus weighting operation is a contract call that reads external mocks or oracles — fine for validation, structurally wrong for permanence. On a native chain the block header commits to the identity/reputation/contribution ledger and consensus reads it directly. PoM becomes a protocol invariant, not a contract invariant.

## How to apply
- Don't frame contract-NCI as a "stepping stone." It's a first-class shipped artifact with its own publishable value.
- Don't frame the L1 move as aspirational or long-term-only. It's the natural home for the security structure; the timing is a resourcing question.
- When designing new primitives, ask: is this a contract-invariant that can live at the weighting layer, or is it a protocol-invariant that needs block-header commitment? The answer shapes whether it can ship now or only post-L1.
- Documentation of NCI should credit both frames — paper/whitepaper language should acknowledge the contract form as a publishable paradigm AND set the expectation that native-chain deployment is the permanent home.

## Chainlink positioning
Will 2026-04-21: *"we should acknowledge that we're kind of doing what chain-link does but not really."* Fair. Chainlink pioneered contract-layer stake-backed operator networks — off-chain compute, on-chain collateral, aggregator contracts enforcing economic penalties, a service surface callable by other protocols. They proved the paradigm works at production scale.

What we share: contract-layer staking + slashing + operator registration + event-observable admin surface. The scaffolding is recognizably Chainlink-adjacent.

What we add: we use the primitive for *consensus weighting* rather than *data-feed aggregation*, and we add Proof of Mind — a time-accumulated unbuyable cognitive dimension. Chainlink's trust model is honest-majority-of-operators (with a reputation-scoring heuristic layered on top); ours is 3D weighting (PoW + PoS + PoM) where the third dimension can't be bought. No Chainlink analogue for PoM.

Shorthand for outreach / papers: *"Chainlink showed that you can run stake-backed services at the contract layer. NCI explores how far that primitive stretches when you push it into the consensus-weighting role and add a third security dimension."*

## Related memory
- [Augmented Mechanism Design](F·augmented-mechanism-design-paper) — the "augment don't replace" principle. Contract-NCI augments; native-NCI still augments (the broader crypto ecosystem), but is the permanent substrate for VibeSwap's specific security structure.
- [Substrate-Geometry Match](P·substrate-geometry-match) — PoM's geometry (time-accumulated, non-linear, identity-bound) requires a substrate that can host that geometry natively. EVM's geometry is account-balance + contract-storage; it hosts PoM only by indirection.
- [The Cave Philosophy](`~/.claude/CLAUDE.md` top) — contract form is the cave. The native chain is what the cave patterns make possible.
