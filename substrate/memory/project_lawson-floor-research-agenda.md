---
name: Lawson Floor Research Agenda
description: Active research thread (2026-04-16) — floor fairness as an objective function is profound but hard to validate. Needs more proofs, more research, more work.
type: project
originSessionId: 86aa75b4-9664-4b47-9d5b-e15a4569c8dd
---
## The Thesis

Floor fairness — "raise the minimum outcome, not the median or mean" — is profound as an objective function for distributions. It maps to Rawlsian max-min / maximin, and translates cleanly to MEV-resistance, reward distribution, and liquidation fairness in DeFi. But turning it into a rigorous objective is hard: most optimizations in market microstructure maximize totals (volume, depth) or averages (spread, slippage), not floors.

## Why "hard to validate"

- **No canonical benchmark** — you can't just compare to Uniswap's "floor" because the concept wasn't part of their design.
- **Floors are fragile** — a single outlier can define the floor. Need distributional guarantees, not point guarantees.
- **Counterfactual reasoning required** — "worst participant WOULD have gotten X under model A, gets Y under model B" needs a shared simulator.
- **Attack surface is asymmetric** — worst-case floor is easier to attack than median.

## Existing artifacts

- `vibeswap/DOCUMENTATION/LAWSON_FLOOR_FAIRNESS.md` — primer doc (Will has iterated on this several times; MIT person engaged favorably on it).
- `vibeswap/DOCUMENTATION/LAWSON_CONSTANT.md` — constant definition.
- MIT consulting thread — offered to help design next year's hackathon reward function around Lawson Floor.
- [REDACTED-NDA] LOI context — workshop-teaching opportunity pairs well with a formalized Lawson Floor paper.

## Work needed (open research agenda)

1. **Mathematical formalization.** Rewrite Lawson Floor as a tight optimization problem. Specify: distribution class, objective, constraint set, solution concept. Compare with Rawlsian maximin, Gini, entropy-constrained welfare.

2. **Simulation proofs.** Build a reference simulator. Demonstrate Lawson-Floor-optimized allocations vs. revenue-maximizing allocations across:
   - MEV extraction scenarios (batch auction vs. PFOF)
   - LP reward distribution (uniform vs. gauge vs. Shapley)
   - Liquidation outcomes (Dutch vs. sealed-bid)

3. **Attack models.** Write down adversarial models where the attacker optimizes to reduce the floor. Bound how much they can move it with budget X. This is the "hard to validate" step — floor fairness needs robustness theorems.

4. **Empirical validation.** Historical on-chain data: for each of {Uniswap, 1inch, Curve, VibeSwap-style mechanism}, reconstruct the realized fairness floor for small traders. Publish methodology + dataset.

5. **Connection to information geometry.** If fairness floor is dual to some entropy regularization, we get clean derivatives and training targets. This is speculative but worth exploring — it'd unify Lawson Floor with the scoring-mechanism thesis (CogCoin = Economitra).

6. **Position paper.** Once the above hardens, write the canonical paper. "Fairness Floor as Mechanism Design Objective" — submittable to FC, AFT, or EC.

## How to apply

- When Will says "Lawson Floor work" / "fairness research" / "floor proofs", pull this memory.
- Do NOT produce proofs off-the-cuff; check the existing DOCUMENTATION docs first to see what's already formalized.
- The MIT thread (Rubin et al.) is the natural external audience. Position synthesis as: "here's the hackathon-reward-design flavor, here's the general theory behind it."
- Pair opportunity with the [REDACTED-NDA] synthesis workshop — a workshop on "how we built Lawson-Floor-optimizing mechanisms with AI-augmented development" would combine Will's two locked-in work threads cleanly.

## Open questions

1. Is Lawson Floor best framed as an objective or as a constraint? (Objective: maximize it subject to feasibility. Constraint: require floor ≥ threshold, maximize something else subject to that.)
2. How does it interact with our Shapley distribution primitive? (Shapley is marginal-contribution, Lawson Floor is rawlsian — they can agree or disagree depending on the coalition structure.)
3. Are there tradeoffs between floor fairness and incentive compatibility? (Usually yes — raising the floor reduces the variance that incentivizes effort.)
