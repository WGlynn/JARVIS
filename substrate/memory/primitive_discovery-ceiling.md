---
name: Discovery Ceiling
description: When adversarial review produces 0 new findings across 3+ consecutive rounds on the same target, that target has reached its discovery ceiling. Shift attention elsewhere.
type: feedback
---

# Discovery Ceiling

Every codebase under adversarial review has a discovery ceiling — the point where additional review rounds produce diminishing returns. Recognizing this point prevents wasted effort and signals readiness.

**Why:** TRP R39, R40, R42, R44, R47 were all verification-only rounds (0 new findings). Each confirmed that the target contract had reached saturation. R50-R53 shifted entirely to test infrastructure — no new contract logic findings. This is the empirical signal that 53 rounds of adversarial review have exhausted the discoverable surface.

**How to apply:**
1. Track new findings per round per contract
2. When a contract produces 0 new findings across 3 consecutive rounds, mark it as "ceiling reached"
3. Shift adversarial effort to: (a) cross-contract integration flows, (b) new code, (c) different attack models
4. Verification rounds on ceiling'd contracts should be periodic (every 10 rounds), not continuous
5. When the ONLY remaining work is test infrastructure (not contract logic), the entire system has reached discovery ceiling

**Generalization:** Discovery ceilings exist in all search problems — security audits, bug bounties, code review, testing. The marginal value of additional review declines exponentially after saturation. The skill is recognizing saturation and reallocating effort, not grinding past it. This is the stopping criterion for any recursive improvement loop.

**Meta-application to RSI:** TRP R1 (adversarial code review) hit discovery ceiling at R53. This is what triggered the full-stack RSI invocation — the loop converged, so the recursion moves to the next target (R0 density, R2 knowledge, R3 capability).
