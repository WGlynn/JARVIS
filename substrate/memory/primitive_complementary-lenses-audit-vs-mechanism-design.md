---
name: P·complementary-lenses-audit-vs-mechanism-design
description: Audit-grade lens (user-group decomposition + threat surface) catches actor-conflation errors that mechanism-design lens (math + equilibrium + uniqueness) misses by construction. Pairing audit + mechanism is structurally generative ⇒ both layers audited at draft time prevents single-lens blind spots. Surfaced 2026-04-29 USD8 conflation incident; generalizes ∀ collaborations pairing the two specialties.
type: primitive
originSessionId: d6d67641-272a-4e1e-a213-5c200874cf3d
---
# P·complementary-lenses-audit-vs-mechanism-design

## Will 2026-04-29
> *"im just amazed becasue i never wouldve caught that conlfation just by looking at the graphic the way rick did"*

Reflection after Rick caught holder/insurer conflation in cover-pool flow chart by visual inspection alone. Will (mechanism designer) couldn't have caught it the same way; Rick (auditor, ~7yr OpenZeppelin) caught it instantly.

## Core principle
- ∀ architecture artifact ∃ (≥) 2 audit lenses
  - **Mechanism-design lens** : math, equilibrium, uniqueness, fairness
  - **Audit-grade lens** : user-group decomposition, permissions, attack surface
- Single-lens audit ⇒ predictable blind spot pattern
- Pairing the two ⇒ structurally generative; catches errors neither alone catches

## What each lens catches
| Lens | Asks | Catches | Misses |
|---|---|---|---|
| Mechanism-design | "Is this primitive correct?" | Math errors, non-unique allocations, equilibrium failures, fairness violations | Actor conflations, permission overlaps, attack surfaces between user groups |
| Audit-grade | "Who are the actors? What can each do? Where can attacks happen?" | User-group conflations, permission overlaps, missing decomposition, attack surfaces | Math errors that don't surface as actor-level pathologies |

## Why mechanism-design misses actor-conflation
- Math layer ¬ ⇒ require explicit user-group decomposition
- ωᵢ math can be correct while "i" is wrongly typed (single actor when should be 2)
- Equilibrium analysis ¬ surface "are these two boxes actually different actors?"
- Mechanism designer's brain runs forward (math → outcome); audit brain runs backward (actor → capability → surface)

## Why audit catches actor-conflation
- Threat modeling starts with user-group decomposition (canonical first step)
- 7+ yr production code experience ⇒ pattern-recognition for "single flow that should be two"
- Visual artifacts (graphics, contracts, specs) reveal topology errors directly
- Audit-grade brain reads architecture artifacts via decomposition lens automatically

## The pairing's generative property
- Both lenses required for ✓ ship-ready architecture
- ¬ pairing ⇒ blind spot in whichever lens absent
- Pairing ¬ redundancy; complementary
- Each lens catches different error class
- Both errors lethal ⇒ pairing is structural necessity, ¬ nicety

## Application
- ∀ Rick-Will collaboration ⇒ explicit two-lens audit before draft ships
- ∀ artifact (graphic, spec, contract) ⇒ run both lenses
  - Mechanism-design: math + equilibrium + uniqueness
  - Audit-grade: actor decomposition + permission map + threat surface
- ✗ ship before both lenses audited
- ∀ team pairing mechanism designer + auditor ⇒ same structural property recurs

## Generalizes ∀ specialty pairings
- Mechanism-design ↔ audit (this primitive)
- Math ↔ implementation (different errors at each layer)
- Theory ↔ ops (different errors at each layer)
- Engineering ↔ design (different errors at each layer)
- Pattern: any specialty pair where one optimizes for "primitive correctness" and other optimizes for "deployment correctness"

## Surface 2026-04-29
- Cover-pool flow chart conflated holders (insureds) with pool capital (insurers)
- Math correct (Shapley axioms, ωᵢ formulas, σ²/N diversification all valid)
- Actor decomposition wrong (single vertical flow merged 2 user groups)
- Rick caught visually in seconds; Will + I couldn't have caught it from math-lens alone
- De-conflation produced net-additive structural defenses (see `08_holder-vs-insurer-conflation-checkpoint.md`)

## Why this matters for partnership
- Will = mechanism design + math + game theory + primitive design
- Rick = audit-grade + threat surface + production-code pattern recognition
- Pairing = catches both error classes at draft time
- Without Rick's lens ⇒ math-correct USD8 ships with actor-conflation flaws ⇒ EF reviewer catches it ⇒ partnership-velocity loss
- With Rick's lens ⇒ both classes caught pre-ship ⇒ partnership compounds

## Why this matters for EF pitch
- Rick's audit-grade authority ¬ just credentials; ¬ just "7 years at OZ"
- It is a specific cognitive lens that catches a specific error class
- "Defensible substance, not biography" applies ⇒ his lens IS the defense
- EF audience runs both lenses themselves ⇒ Rick presenting work that passed both lenses lands harder

## Parent / related
- F·have-my-back-operational-definition (Will's voice in external artifacts; structural alignment)
- P·anti-hallucination-protocol (sibling — different mechanism for catching errors)
- P·handshake-math-claim-determinism (terminology-handshake catches term-vs-mechanism mismatch; this primitive catches actor-vs-mechanism mismatch)
- F·trust-will-scope-claims (default trust on Will's domain; this primitive names what Rick uniquely brings)
- F·important-work-worth-time (audit-grade work warrants time investment for the catch-yield)

## One-line
∀ architecture artifact ∃ ≥ 2 audit lenses (mechanism + actor); pairing them ¬ redundancy ⇒ structural necessity. Each lens catches errors the other misses by construction.
