---
name: Fractalized Shapley Games
description: Git commits are flat attribution. Real contribution is a fractal DAG of influence. Shapley values must decompose recursively to capture inspiration chains.
type: user
---

# Fractalized Shapley Games (2026-03-27)

> "Our github commits don't carry the full context because I was inspired by alice or bob when making it."

## The Problem
Git is a flat attribution model. `Author: Will` tells you who typed the code. It says nothing about:
- The conversation that sparked the idea
- The paper that reframed the problem
- The teammate whose failed approach revealed the right one
- The community member whose question forced a clearer design

Real intellectual contribution is not a list. It's a **Directed Acyclic Graph** — a fractal tree of influence where every node has parents, and those parents have parents.

## The Insight: Shapley Goes Fractal
Standard Shapley values distribute rewards across a coalition based on marginal contribution. But if the coalition is flat (just committers), you miss the influence chain entirely. **Fractalized Shapley** means:

1. **Every contribution decomposes** — a commit has sub-contributions (inspiration, review, challenge, refinement)
2. **Influence is recursive** — Alice inspired Bob who inspired the algorithm. Alice's Shapley value propagates through Bob's.
3. **The DAG is the truth** — not the commit log. The ContributionDAG captures edges that git cannot.
4. **Attribution decays but never zeroes** — the further back in the chain, the smaller the share, but it's never zero. Shannon entropy of the influence channel determines the weight.

## Why This Matters for VibeSwap
- `ShapleyDistributor.sol` currently distributes based on direct participation
- `ContributionDAG` exists but doesn't yet capture the fractal depth
- The mechanism needs to let contributors DECLARE their influences — "this commit was inspired by [Alice's idea in TG]"
- Self-reporting + peer validation = the influence DAG emerges organically
- Sybil resistance: you can't fake influence that others don't corroborate

## Connection to Economítra
This is Section 4 of the paper made concrete. Information-theoretic value attribution. The mutual information between Alice's idea and Bob's commit IS Alice's Shapley contribution. The channel capacity of the influence link determines how much value flows back.

## Hypercerts: The Leaf Layer (Research 2026-03-27)
Hypercerts (hypercerts.org) are ERC-1155 impact claim tokens. Protocol Labs / Funding the Commons origin. Live on Optimism, Base, Celo. Six-dimensional metadata: contributors, work scope, timeframe, impact scope, impact timeframe, rights.

**What they solve**: Standardized "this work happened" claims. Retroactive funding markets. Non-overlapping impact space.

**What they don't solve** (and we do):
- Flat contributor list — no weighting, no Shapley
- No parent-child relationships between certs
- No inspiration chains or "derivative of" concept
- No recursive credit propagation
- No game-theoretic attribution at any level

**Shapleycerts = the synthesis**:
- Hypercerts as the atomic claim primitive (leaf nodes)
- ContributionDAG as the graph structure linking claims to parent claims
- ShapleyDistributor as the credit-propagation engine running over the DAG
- Every commit/contribution mints or references a hypercert
- Every hypercert DECLARES its parents: "inspired by [Alice's idea]", "builds on [Bob's module]"
- Self-reporting + peer validation = the influence DAG emerges organically
- Shapley runs over the full DAG. Credit flows backward through inspiration chains.
- Shannon mutual information between parent and child = edge weight (how much of Alice's signal survived into Bob's commit)

**Architecture**:
```
[Hypercert layer]     — atomic claims: "this work happened"
        ↓
[ContributionDAG]     — edges: "this work was inspired by / builds on"
        ↓
[ShapleyDistributor]  — credit propagation: "therefore Alice gets X% of Bob's reward"
```

Hypercerts team is migrating to ATProto (Bluesky's protocol) for off-chain data. This could actually make the DAG layer easier — ATProto's lexicon system is built for linked social data.

## MIT Pitch Angle
This is not a DeFi pitch. This is a **research contribution to cooperative game theory**.

**The claim**: Git commits are the dominant attribution model in open-source, and they systematically misattribute value by flattening a recursive influence graph into a list of authors. Shapley values over contribution DAGs solve this, but no existing protocol implements recursive attribution with credit propagation. Hypercerts come closest (standardized claims) but stop at leaf nodes.

**What Will presents**:
1. The theory — Economítra paper. Information theory + mechanism design. Shannon, Shapley, Nash, Axelrod.
2. The gap — Hypercerts solve claims, not attribution graphs. Git solves authorship, not influence.
3. The primitive — Fractalized Shapley: recursive decomposition of contribution with credit propagation through the DAG.
4. The code — ShapleyDistributor.sol + ContributionDAG. Deployed. Tested.

**Why MIT cares**:
- CSAIL: Formalizing recursive attribution is algorithmic game theory. Publishable.
- Media Lab: Computation meets social systems. Their exact mandate.
- Sloan: Mechanism design faculty. Shannon mutual information as edge weights is their language.
- Expo theme "Freedom for All": Making invisible contributions visible IS a freedom technology.
- Every CS researcher has felt "git is a lie of omission." Nobody has formalized a fix with working code.

**The one-liner for judges/faculty**: "We built the protocol that gives Alice credit when Bob's commit was inspired by her idea. Shapley values over a contribution DAG, with working Solidity."

## The Primitive
**Every flat ledger is a lie of omission. Real attribution is fractal. Build the DAG or lose the signal.**
