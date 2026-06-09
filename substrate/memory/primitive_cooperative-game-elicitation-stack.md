---
name: Cooperative-game elicitation stack
description: Shapley operates on v, ¬ produce v. Decouple distribution / value / aggregation / elicitation. Substrate-match each layer.
type: primitive
originSessionId: 05f950b5-8ab9-47f5-a2b2-b8336ce1e9ef
---
# Elicitation stack

## The silence problem
- Shapley axioms ⇒ how to distribute v(N)
- Shapley ¬ produces v
- ⇒ deployments conflate the two ⇒ inherit upstream bias
- bias = upstream of math ⇒ math cannot detect it

## 4 layers (top-down = design order; bottom-up = info flow)

| L | layer | what it does | choices |
|---|---|---|---|
| 1 | **distribution** | (N, v) → φ:N→ℝ | Shapley ∨ core ∨ nucleolus ∨ Banzhaf ∨ closed-form linear |
| 2 | **value function** | rep of v: 2^N → ℝ | linear v(S)=Σwᵢ ∨ superadditive ∨ supermodular ∨ parametrized |
| 3 | **aggregation** | inputs → v | weighted-sum ∨ Bradley-Terry ∨ Plackett-Luce ∨ regression |
| 4 | **elicitation** | world → inputs | direct-observation ∨ pairwise ∨ reputational ∨ hybrid |

## Key rule
- each layer: independent choice
- each layer: substrate-match analysis
- choosing L1 ¬ determines L2/L3/L4
- silent conflation ⇒ load-bearing failure

## 4 elicitation classes

| class | substrate-match when | attack surface |
|---|---|---|
| **direct-observation** | contribution intrinsically observable + Sybil-resistant | Goodhart (gameable observable) |
| **pairwise comparison** | ¬ observable + humans ✓ relative judgment | Sybil voting + collusion + vote-buying |
| **reputational oracle** | external trusted process exists | oracle compromise + staleness + Sybil |
| **hybrid composition** | no single class captures + Goodhart defense | inherits per-component weighted by α/β/γ |

## Composition pattern: pairwise-augmented direct observation
- pure direct ⇒ Goodhart vulnerable
- + small β·pairwise ⇒ defense
- attacker must mech-optimize ∧ social-manipulate (uncorrelated cost surfaces)
- β small (0.1-0.3) ⇒ doesn't dominate, just denies cheap mech-optimization
- Goodhart resistance = the principal cross-layer composition pattern

## Application (USD8 ∧ VibeSwap)

| problem | elicitation | aggregation | distribution |
|---|---|---|---|
| USD8 Cover Pool LP rewards | direct | weighted sum | Shapley closed-form |
| USD8 Cover Score | direct | weighted integral | (score, ¬ distribution) |
| USD8 claim adjudication | pairwise | Bradley-Terry | tribunal pro-rate |
| VibeSwap fee distribution | hybrid (direct + reputational) | weighted sum | Shapley closed-form |
| VibeSwap governance | hybrid (direct + pairwise) | Bradley-Terry | quadratic w/ weighted votes |

## Open problem (recursive blending-weights)
- hybrid: w = α·obs + β·pair + γ·rep
- α/β/γ themselves require principled distribution
- Shapley over blending-weights ⇒ requires own elicitation stack
- recursion ¬ terminate
- 3 candidate exits:
  - bounded recursion (stop at fixed depth, founder-fiat thereafter)
  - constitutional fixity (Layer 2 amendment with friction)
  - adaptive blending via outcome-regression (loss-minimization)
- none complete

## Triggers
- Shapley deployment design (any protocol)
- "is this fair?" Q on distribution mechanism
- discussion of pairwise / DeepFunding / quadratic / conviction voting
- before committing to a value function in a cooperative game

## Anti-patterns
- ✗ "we use Shapley therefore fair"
- ✗ choosing all 4 layers in one breath
- ✗ paired-comparison elicitation where direct observation is intrinsically Sybil-resistant (insurance LPs anonymous, transactional)
- ✗ pure direct observation where contribution shape is genuinely unobservable

## Output artifact
- `vibeswap/docs/papers/cooperative-game-elicitation-stack.md` (research paper, ~6500 words)
- PDF on Desktop: `cooperative-game-elicitation-stack.pdf`

## Related
- shapley distribution (the L1 mechanism this primitive contextualizes)
- substrate-geometry-match (per-layer substrate analysis)
- augmented mechanism design (the methodology that motivates structural choices over discretionary ones)
- first-available-trap (KZG/Verkle/etc. as the seductive-default-that-doesn't-fit-here)
