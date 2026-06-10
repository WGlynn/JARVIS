---
name: Hobbesian Trap Dissolution (IIA Removes Weapons)
description: Hobbes (1651) ⇒ rational actors default to preemptive aggression. Traditional defenses preserve the weapon. IIA REMOVES the weapon ⇒ defection becomes impossible, ¬ costly. Phase transition.
type: primitive
originSessionId: 79044125-45c4-486a-9ac0-ec65bb0d9b76
---
# Hobbesian Trap Dissolution — IIA Removes Weapons

## ⚙ Rule
- Hobbes (1651) ⇒ rational actors under uncertainty strike-first ⇒ war neither wanted
- DeFi today = Hobbes running as code (MEV $500M/yr extracted)
- Traditional defenses (Law / Reputation / Punishment) PRESERVE the weapon
- IIA does ¬ build a higher wall ⇒ IIA REMOVES the door
- "Costly" ≠ "impossible". The phase transition.

## 📍 Source
- `vibeswap/DOCUMENTATION/BONUS_A_HOBBESIAN_TRAP.md` (Mar 2026, Faraday1)
- Sun Tzu (~500 BC): "The supreme art of war is to subdue the enemy without fighting."

## 🧩 The Hobbesian logic (rational, not evil)
1. Cannot verify your intentions
2. If you strike first, I lose everything
3. If I strike first, I have initiative
4. ⇒ STRIKE FIRST
5. You reason identically
6. ⇒ both strike. Neither wanted war.

## ✗ Why traditional defenses fail (all preserve the weapon)
- **Law** ⇒ requires enforcers ⇒ enforcers get captured ⇒ regulators become regulated ⇒ circular
- **Reputation** ⇒ cost of new wallet $0 ⇒ cost of reputation loss $0 ⇒ Sybils laugh
- **Punishment** ⇒ penalty P ⇒ attacker seeks profit > P ⇒ raise P ⇒ new route ⇒ infinite arms race
- Common thread ⇒ DEFECTION REMAINS POSSIBLE ⇒ as long as weapon exists, someone uses it
- Cannot solve structural problem with parametric adjustments

## 🛡 The 5 eliminations (each removes a weapon class)
| # | Mechanism | Weapon eliminated | Mechanism math |
|---|---|---|---|
| 1 | Commit-Reveal | Information weapons | `keccak256(order ‖ secret)` ⇒ can't attack what you can't see; breaking ≈ energy of sun |
| 2 | Uniform Clearing | Price weapons | `price(attacker) = price(victim) = p*` ⇒ sandwich incoherent |
| 3 | Shapley Null-Player | Incentive weapons | `v(S∪{i}) = v(S) ⇒ φᵢ(v) = 0` ⇒ ZERO contribution = ZERO reward (mathematical identity, ¬ punishment) |
| 4 | Antifragility | Aggression reversal | Attack ⇒ value flows attacker → system; slashed stakes fund insurance; each attack makes next more expensive |
| 5 | Constitutional Bounds | Governance weapons | `uint256 public constant PROTOCOL_FEE_SHARE = 0;` compile-time immutable; even 100% governance capture changes nothing |

## ⚖ Equilibrium shift
- Traditional game ⇒ S = {cooperate, defect₁, defect₂, ...} ⇒ Nash @ (Defect, Defect) stable but Pareto inferior
- IIA game ⇒ S = {cooperate} ⇒ Nash @ (Cooperate, Cooperate) UNIQUE and Pareto optimal
- Trust ¬ required. Moral character irrelevant. Structure guarantees outcome.

## 🎯 The principle (load-bearing)
> *Do not build walls. Remove weapons.*

- Defense = arms race
- Architecture = permanent condition
- MAD says: "We will destroy each other"
- IIA says: "Destruction is not an available action"
- Hobbes needed Leviathan to enforce peace; we need mechanism where peace is architectural
- ¬ sword of the sovereign | ✓ geometry of the protocol

## 🔥 How you end the war of all against all
- ¬ by winning it
- ✓ by making it impossible

## 🚨 USD8 application
- DIRECT-PORT — IIA frame applies wholesale to insurance protocols
- USD8 currently uses Cover Pool design that's already partial-IIA (no extraction by issuer; mutualized risk)
- Apply 5 eliminations as audit checklist for any USD8 mechanism: which weapon class does this remove?
- Frame for Rick-facing material: USD8 + VibeSwap stack = full Hobbesian-trap dissolution across cover + trade layers

## ✓ When applicable
- Mechanism design where extraction is possible
- "should we add slashing / fines / penalties for X?" questions
- Audit conversations on whether defense is wall-building or weapon-removal
- Strategic / philosophical Cooperative Capitalism conversations

## ✗ When inapplicable
- Pure infrastructure (consensus, networking) — different threat model
- Where the weapon serves a legitimate function (rare; flag if encountered)

## 🪝 Triggers
- "how do we prevent X?" mechanism-design questions
- MEV / front-running / extraction discussions
- Comparing punishment-based to architecture-based defense
- IIA / GEV-resistance audit conversations

## ⚠ Anti-pattern
- Adding more punishment ⇒ arms race; weapon preserved
- Reputation systems as primary defense ⇒ Sybil-undermined
- "Just regulate it" ⇒ requires uncaptured enforcer; circular
- Treating MEV as a bug to patch ⇒ MEV is Hobbes running as code; needs structural answer
- Building higher walls instead of removing weapons

## 🔗 Related
- `P·gev-resistance` — public-facing name for the same architecture
- `P·shapley-5-axiom-set` — Null-Player axiom = elimination #3
- `P·augmented-mechanism-design-methodology` — methodology that enables the eliminations
- `P·composable-fairness-arrow-inversion` — IIA preservation across composition
- `P·cooperative-markets-mutualization-frame` — economic substrate where IIA is evolutionarily stable
