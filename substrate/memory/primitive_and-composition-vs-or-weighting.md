---
name: and-composition-vs-or-weighting
description: "Multi-instrument consensus — a weight-split symbolizes power iff it's an OR-weighted vote; under AND-composition the split is reward-only. Capture-resistance = cycle-independence, not weight-symmetry."
metadata: 
  node_type: memory
  type: reference
  originSessionId: d3baa19d-dd1c-4c9a-be43-00c49d5e9b7a
---

**[ANDvsOR](P·and-composition-vs-or-weighting)** — ∀ multi-instrument consensus (N proofs/powers combined): weight-split ⊥ power **IFF AND-composition** (attacker must defeat ∀ independent layers). Under **OR-additive** (Σ weighted-vote, finalize @ threshold T): split **IS** power ⇒ ∃ instrument w/ weight ≥ T → finalizes alone. **Supermajority T > max-single-weight ⇒ restores AND-at-margin** (no single instrument suffices; capture needs a coalition crossing T). One-liner: *"X% of an instrument is only dangerous if it's an X% vote."*

RPS capture-resistance = **cycle-INDEPENDENCE ¬ weight-symmetry** ⇒ uniform-split (1/N each) neither necessary (AND ⇒ split cosmetic) nor sufficient (OR-vote still cycles for liveness + any subset ≥ T colludes). 3 = minimal non-dominated cycle (2→binary capture; 4+→coalitions).

Constitutional analog: US 3-branch sep-of-powers = **non-substitutable** (each branch necessary, none does another's job) = **AND** ⇒ the Constitution is the AND-composition ideal; a naive weighted-sum is OR. Legitimacy differs: branches ← election; proof-systems ← earned stake.

Fix-order: **(a) declare AND @ finalize [structural, preferred] > (b) cap no-single ≥ T [patch, insufficient under correlation]** (any colludable subset ≥ T captures; correlated instruments collapse AND→OR).

AND load-bearing on: per-instrument **independence** (each un-buyable, else correlated walls = one wall) + per-dimension **provisioning-floor** (¬ starved paper-wall: a reward-split is capture-neutral only above each layer's cost-to-break) + **content-independent tie-break** (VRF / commit-reveal seed ¬ weight-proportional = a smuggled vote) + **liveness ≠ safety-AND** (AND over vetoes ¬ production; gating-layer outage = bounded cost, not substitution).

Time-symmetry: decay ∀ instruments' franchise symmetrically ∨ a non-decaying instrument's *effective* share rises under correlated staleness (drift toward the persistent one). Decay franchise/vote-weight ¬ the staked balance. Symmetric-decay must pair w/ threshold-on-effective-weight ∨ it worsens the low-participation liveness halt.

Origin: 2026-06-11 mechanism-design analysis (verifying a deployed OR-additive 3-proof consensus w/ a 2/3 finalization bar). parent: [P·multi-axis-robustness-for-architectural-defense] · [P·structure-does-the-work] · [F·augmented-mechanism-design-paper] · [P·augmented-governance].
