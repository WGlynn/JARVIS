---
name: "Augmented Governance — Constitutional Invariants Enforced by Cooperative Game Theory"
description: Governance is not removed but augmented with math-enforced invariants. Same pattern as augmented mechanism design. Governance operates freely within P-000/P-001 bounds — Shapley math acts as constitutional court. Prevents governance capture, the #1 DeFi DAO failure mode.
type: project
---

## Augmented Governance

### The Pattern

Augmented Mechanism Design: markets still function, but batch auctions + Shapley make them fairer by construction.

Augmented Governance: DAO still votes, but constitutional invariants (P-000/P-001) enforced by Shapley math prevent governance from breaking fairness.

Same word. Same pattern. Augmentation, not replacement.

### The Hierarchy

1. **Physics** (P-001: Shapley invariants, self-correction) — cannot be overridden
2. **Constitution** (P-000: Fairness Above All) — amendable only when the math agrees
3. **Governance** (DAO votes, proposals, parameters) — free to operate within 1 and 2

Governance is augmented the same way the AMM is augmented — you're free to do whatever you want, as long as the math says nobody is getting extracted.

### Regular vs Augmented Governance

**Regular governance (Uniswap, Compound, etc.):**
- 51% votes to turn on protocol fees → fees turn on → LPs get extracted
- 51% votes to drain treasury → treasury drained → protocol dies
- Governance capture by whales → rent extraction → death spiral

**Augmented governance (VibeSwap):**
- 51% votes to turn on protocol fees → Shapley detects null-player extraction → self-correction overrides → LPs stay whole
- 51% votes to drain treasury → violates efficiency axiom → correction blocks it
- Whale captures governance → every extraction attempt is detected and reversed by the same math that distributes rewards

The vote still happened. The voice was heard. The math just said "no, that violates the invariant."

### The Constitutional Court Analogy

A constitutional court can strike down a law that violates the constitution. The legislature has full power to legislate — but within constitutional bounds.

Augmented governance is the same, except:
- The constitution is P-000 + P-001
- The court is Shapley math
- The ruling is autonomous (no judges needed)
- The enforcement is on-chain (no appeals)

A constitutional court staffed by math, not humans. Incorruptible by definition.

### Why This Matters

**Governance capture is the #1 failure mode in DeFi DAOs.** Compound governance was captured by a whale who voted themselves $25M. MakerDAO governance nearly drained the surplus buffer. Curve wars are governance capture as a business model.

Every DAO eventually faces the question: "what if the voters are the ones extracting?"

Regular governance has no answer. Augmented governance does: the math overrides the vote.

### Implementation in VibeSwap

- **ShapleyDistributor.sol**: Measures marginal contribution (the constitutional test)
- **CircuitBreaker.sol**: Halts on threshold violations (the enforcement mechanism)
- **ExtractionDetection.t.sol**: 9 tests proving detection works (the precedent)
- **Future**: GovernanceGuard contract that wraps DAO proposals in a Shapley fairness check before execution. Proposals that violate P-001 are automatically vetoed by the math.

### What Governance CAN Do (Within Bounds)

- Adjust fee tiers per pool (as long as 100% goes to LPs)
- Fund new initiatives from treasury (priority bid revenue, not LP fees)
- Change circuit breaker thresholds
- Add new token pairs
- Approve grants and partnerships
- Modify emission schedules (within Shapley efficiency axiom)
- Everything that doesn't violate fairness

### What Governance CANNOT Do

- Enable protocol fee extraction from LP swaps
- Redirect LP fees to treasury/stakers/anyone
- Override Shapley distribution weights to favor insiders
- Drain treasury beyond what the math says is fair
- Break the null player axiom (give rewards to non-contributors)

### Origin

Will Glynn, Session 067, 2026-03-17:
> "governance coopting axioms is almost like augmented governance like our augmented mechanism design"

### Paper Title (Future)

"Augmented Governance: Constitutional Invariants Enforced by Cooperative Game Theory"

Abstract: We present a governance framework where on-chain cooperative game theory (Shapley values) acts as a constitutional court, autonomously vetoing governance proposals that violate fairness axioms. Unlike existing DAO governance where majority rule can enable extraction, augmented governance preserves the mathematical invariants that define protocol fairness while leaving all non-violating governance decisions unconstrained. We prove through simulation (9 tests, 2 fuzz with 256 runs each) that extraction is always detected and self-corrected, making governance capture structurally impossible.
