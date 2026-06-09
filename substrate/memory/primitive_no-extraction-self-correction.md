---
name: "P-001: No Extraction Ever — Autonomous Self-Correction"
description: Companion to P-000 (Fairness Above All). If extraction is mathematically provable on-chain via Shapley fairness measurement, the system self-corrects autonomously without governance. Human intent (P-000) backed by machine enforcement (P-001).
type: project
---

## P-001: No Extraction Ever — Autonomous Self-Correction

### The Two Axioms

**P-000: Fairness Above All** (Human-side, Session 001 — Genesis)
> If something is clearly unfair, amending the code is a responsibility, a credo, a law, a canon.

**P-001: No Extraction Ever** (Machine-side, Session 067)
> If extraction is mathematically provable on-chain beyond a shadow of a doubt, the system self-corrects autonomously for ungoverned neutrality.

P-000 is the human credo — *we* fix it when *we* see it.
P-001 is the machine invariant — *the protocol* fixes it when *the math* proves it.

Together they form a closed loop: human intent backed by autonomous enforcement.

### The Bridge Between Them: Shapley Fairness Measurement

Shapley values measure marginal contribution — what each participant actually adds to the cooperative game. This is not opinion. Not governance. Not voting. Math.

If any actor (user, LP, protocol, admin, or the system itself) takes more than their Shapley-measured marginal contribution, that is **extraction** — proven on-chain, beyond a shadow of a doubt, by the same mathematics that distribute rewards.

The proof is symmetric: the same Shapley computation that says "you earned X" also says "you took X+Y, and Y is extraction."

### Self-Correction Properties

1. **Detection**: Shapley fairness measurement continuously computes marginal contributions. Deviation from fair allocation = extraction signal.

2. **Proof**: On-chain math, not allegation. The same formulas that distribute rewards also detect violations. Cryptographic certainty, not social consensus.

3. **Correction**: The system amends itself autonomously. No governance vote needed. No multisig approval. No human in the loop. The math sees it, the math fixes it.

4. **Ungoverned Neutrality**: Not "nobody governs" — "the math governs." Same way gravity doesn't need a committee. The protocol enforces fairness the way physics enforces conservation of energy.

### Why Both Axioms Are Necessary

- P-000 without P-001: Good intentions with no enforcement. "We promise not to extract" is policy, and policy can be changed.
- P-001 without P-000: Enforcement without intent. A system that self-corrects but was designed by someone who didn't care about fairness could optimize for the wrong invariant.
- P-000 + P-001: Human intent crystallized into machine physics. The designer's values become the protocol's laws. Once deployed, they don't need the designer anymore.

This is the Cincinnatus endgame: Will walks away, and the math keeps enforcing fairness. If it needs Will to function, it's not finished yet.

### Governance Cannot Override Axioms

A critical implication: if 51% of governance votes to "enable protocol fees," P-001 detects that as extraction (null player axiom — governance contributed no liquidity, therefore deserves no LP fees). The self-correction mechanism overrides the governance vote.

This means P-000 and P-001 sit ABOVE governance in the protocol hierarchy:
1. **Physics** (P-001: math-enforced invariants)
2. **Constitution** (P-000: human-side fairness credo)
3. **Governance** (DAO votes, proposals, parameters)

Governance can change parameters within the axioms. It cannot change the axioms themselves. This prevents governance capture — the most common failure mode in DeFi DAOs.

Origin: Will, Session 067: "this also prevents governance from coopting us and breaking our key axioms!"

### Implementation Vectors

- **ShapleyDistributor.sol**: Already measures marginal contribution across 5 axioms (Efficiency, Symmetry, Null Player, Pairwise Proportionality, Time Neutrality)
- **CircuitBreaker.sol**: Already halts on threshold violations — extend to Shapley fairness deviation
- **ContributionDAG.sol**: Already tracks contribution dependency graph — Lawson Constant is structurally load-bearing
- **Future**: Autonomous rebalancing when Shapley deviation exceeds threshold. No governance proposal needed. The invariant is the governance.

### The Analogy

> Gravity doesn't ask permission to pull. Conservation of energy doesn't take a vote. Fairness, when encoded correctly, shouldn't either.

### Origin

Will Glynn, Session 067, 2026-03-17:
> "if anything is unfair or extractive proven by on-chain mathematics that we use to measure shapley fairness and extraction beyond a shadow of a doubt, it's a necessity for the system to self-correct, ideally autonomously for ungoverned neutrality"
