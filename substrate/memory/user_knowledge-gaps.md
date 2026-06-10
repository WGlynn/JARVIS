---
name: Will's Knowledge Gaps (Test Tracking)
description: Will's stated learning goals — audit-grade lens cultivation (2026-04-29) ∧ math notation fluency (2026-04-28) ∧ VibeSwap parameter recall (2026-03-25). Defaults: walk math symbols letter-by-letter on notation; run audit-lens decomposition ⇒ before mechanism math on architectural artifacts.
type: user
originSessionId: d6d67641-272a-4e1e-a213-5c200874cf3d
---
# Will's Knowledge Gaps

## Audit-Grade Lens Cultivation (2026-04-29)

> *"i also want to get better at rick's side of things instead of just remaining strong in my own domain"*

### Surface
- Rick caught cover-pool flow conflation visually
- Will mech-design fluent ¬ audit-grade fluent
- Goal: ✓ internalize audit lens ⇒ ¬ collaboration-dependent

### Six audit moves (run ∀ architecture artifact)
1. **Actor decomp** — list user groups ✓ before math
2. **Capability map** — ∀ actor: read / write / state-access
3. **Trust boundary** — where data ∨ control ∨ value crosses actor lines
4. **Attack surface** — ∀ (actor × capability × boundary) ⇒ what could go wrong (inversion: maximize-damage)
5. **Topology audit** — actor-count = swim-lane-count? single-flow ∧ multi-actor ⇒ topology bug
6. **Counter-questions** — partial-trust failure ∨ collusion ∨ ∞-capital adversary ∨ silent-state-error

### My default behavior
- Will-described new design ⇒ surface actor decomp first ✓ before math
- ∀ spec / graphic / sketch I draft ⇒ actor + capability + trust + attack block ✓ before math
- Topology-suspect artifact ⇒ flag, ¬ paper-over

### Cultivation path (Will)
- Re-audit existing VibeSwap artifacts cold ⇒ post-mortem findings vs. 6 moves
- Pre-audit new designs ⇒ 6-move checklist before ship
- Read audit reports (OZ ∨ Trail of Bits ∨ Halborn ∨ Sherlock) ⇒ trace finding ↔ move
- ∀ visual artifact ⇒ actor-count = swim-lane-count discipline

### Trigger
- ∀ architectural artifact (graphic ∨ spec ∨ contract ∨ design)
- ∀ partner-facing draft (Rick ∨ EF)
- Skip ⇐ Will explicitly opts out per-artifact

### Why
- Rick + Will = catches both errors (math ∧ actor) ⇒ at 2-lens latency cost
- Will internalizes audit lens ⇒ first-draft 2-lens-audited ⇒ Rick = 3rd-line ¬ 1st
- Compresses catch latency ⇒ partnership velocity ↑

### Sibling primitive
- P·complementary-lenses-audit-vs-mechanism-design

---

## Math Notation Fluency Goal (2026-04-28)

**Will**: *"can yo explain the math letter by letter for me? i need to start learning math"* (in response to ωᵢ = Σ_token weight_token × ∫₀ᵀ balance_token(t) dt and the φᵢ Shapley formula)

**Calibration**: Will designs sophisticated mechanisms (Shapley distributors, Fibonacci scaling, Clawback Cascade) by *concept* fluently — but he reads formulas with the symbols still partially opaque. He wants symbolic-notation fluency: know that ω is "omega," φ is "phi," Σ is "capital sigma" for discrete sum, ∫ is "integral" for continuous sum, subscripts are indices, dt is the differential, etc. Not "what does the formula mean conceptually" — he already knows that.

**Default behavior going forward**: When any formula appears in conversation (or in a doc Will is reading) and he hasn't already demonstrated fluency on it, walk it letter by letter:

1. **Symbol table** — name (Greek + English), what it means *here*, why mathematicians chose it
2. **Read aloud** — verbatim translation in spoken English ("phi-sub-i equals omega-sub-i times...")
3. **Plain English** — what the formula says without notation
4. **Worked example** — concrete numbers, step by step
5. **Notation guideposts** — Σ vs ∫, why two letters (ω and φ) instead of one, etc.

Don't downshift the conceptual depth — Will has that. Just make the *symbols* legible.

**Trigger conditions**: New formula in a Rick-facing doc, a paper Will's reading, a math discussion. Skip when Will demonstrates familiarity ("you don't need to walk this one").

---

## Test 001 (2026-03-25): Score 35/40

## Test 001 (2026-03-25): Score 35/40

### Blindspot Pattern: Specifics > Concepts
Will understands HOW everything works but struggles with exact numbers, enumerations, and parameter values under pressure. Concepts are solid.

### Missed Questions
1. **Phase naming** (Q2): confused which phase hashes are submitted in
2. **Timing parameters** (Q7): 8s commit / 2s reveal — fuzzy on exact split
3. **Axiom enumeration** (Q11): knows Shapley axioms exist, can't list all 5 cold
4. **Security parameter counts** (Q28): knows circuit breakers, not the 3 types
5. **AMM formula** (Q29): x*y=k should be automatic — PRIORITY FIX

### The 5 Shapley Axioms (drill these)
1. Efficiency — all value distributed
2. Symmetry — equal contributors get equal rewards
3. Null Player — zero in = zero out
4. Pairwise Proportionality — reward ratio = contribution ratio
5. Time Neutrality — same work = same reward regardless of when

### Future Test Adjustments
- Add more parameter-specific questions (exact numbers, thresholds, formulas)
- Add "list all X" free-response questions
- Reduce concept questions (he's strong there)
- Add AMM math section (formulas, slippage calculation, impermanent loss)
