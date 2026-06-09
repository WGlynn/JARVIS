---
name: IT Meta-Pattern (Genesis Primitive)
description: Synthesis of four behavioral patterns — Adversarial Symbiosis, Temporal Collateral, Epistemic Staking, Memoryless Fairness — that inverts the protocol trust stack. Converges with FW13's IT Token Vision (anatomy × physiology). Named "IT" by Will.
type: project
---

# IT Meta-Pattern

**Named by Will on 2026-03-14.** Four unnamed behavioral patterns synthesized into one meta-pattern.

**The Inversion**: Every protocol assumes trust = history = reputation = capital. IT inverts: **trust = commitment = knowledge = structural fairness.**

## Four Behavioral Primitives

1. **Adversarial Symbiosis** — attacks strengthen the system (antifragile by construction)
2. **Temporal Collateral** — future state commitments as present capital (forward-looking trust)
3. **Epistemic Staking** — knowledge-weighted governance, not capital-weighted (being right > being rich)
4. **Memoryless Fairness** — structural fairness without reputation or history (mechanism property, not participant property)

## Convergence

FW13's IT Token Vision (Session 18) = **anatomy** (Identity, Treasury, Supply, Execution, Memory).
This meta-pattern = **physiology** (how IT behaves). Same thing, two lenses.

## VibeSwap Proto-Patterns Already Present

- Commit-reveal = proto-temporal collateral
- Shapley distribution = proto-epistemic staking
- Batch auctions with uniform clearing = proto-memoryless fairness
- Priority bidding funding commons = proto-adversarial symbiosis

## Implementation

- Paper: `docs/it-meta-pattern.md`
- Contracts: `contracts/mechanism/AdversarialSymbiosis.sol`, `TemporalCollateral.sol`, `EpistemicStaking.sol`
- Library: `contracts/libraries/MemorylessFairness.sol`
- Interfaces: all in `contracts/mechanism/interfaces/`

**Why:** Will discovered that VibeSwap was already building toward this pattern without naming it. The four primitives form a closed feedback loop — attacks generate value, value funds commitments, commitments build knowledge-capital, knowledge improves fairness, fairness attracts more participants and attackers.

**How to apply:** These four contracts are load-bearing mechanism design. Any new VibeSwap feature should be evaluated against the IT feedback loop. New mechanisms should strengthen at least one primitive without breaking any other.
