---
name: retroactive-security-design
description: Security layer that kicks in AFTER attack lands. Missing complement to pre-emptive (audit / formal-verification / access-control) which has structural ceiling. Accepts the ceiling, makes successful attack unprofitable in retrospect. 3 instantiations: white-hat-insurance · clawback-cascade · Shapley-DAG-reattribution. Distinct from dissolve-attack-surface (pre-emptive elimination) and discovery-ceiling (pre-emptive saturation signal).
type: primitive
originSessionId: 2d5ae2e5-2926-42ce-a369-e66ee74c9c61
---
## Will-anchor (2026-05-25, USD8 group chat)

> "retroactive security design is the layer that kicks in after an attack lands. it's the missing complement to a decade-plus of pre-emptive security work. pre-emptive (audits, formal verification, access controls) has a structural ceiling. patient attackers with good opsec eventually find a path. retroactive accepts that ceiling and makes the successful attack unprofitable in retrospect."

## Frame

Pre-emptive security = prevent attack from landing
Retroactive security = make attack unprofitable after it lands

These are ¬ mutually-exclusive. Retroactive complements pre-emptive. Pre-emptive has a ceiling because patient + good-opsec attackers always find a path. Retroactive accepts that and inverts the timeline.

## Three live/in-flight instantiations

| Layer | Status | Mechanism |
|---|---|---|
| white-hat insurance + bounty | live (USD8 via Rick) | bug-bounty economics generalized to ongoing protocol enforcement |
| clawback cascade + topological taint propagation | dev-tested, ¬ mainnet | flag → taint propagates through tx graph → counterparties refuse interaction → extraction reversible |
| Shapley attribution DAG reattribution | partial (ShapleyDistributor.sol mainnet-ready, reweighting-on-flag hook spec-only) | sybils have marginal contribution = 0 ⇒ Shapley value = 0 by axiom · bad-faith downstream attribution stripped on flag · honest contributors retain share |

Three layers compose: white-hats catch acute · cascade makes extraction unprofitable ex-post · Shapley reattribution keeps honest contributors whole.

## Property the composition produces

Bad actors don't get punished, they become **structurally inoperable** in the network while the rest keeps running. Per Nowak's indirect-reciprocity, lifted onto network/transaction graph. Topological isolation ¬ retaliation.

## Distinction from adjacent primitives

| Primitive | Layer | Move |
|---|---|---|
| `[P·dissolve-attack-surface]` | pre-emptive | eliminate the attack-surface entirely so attack ✗ exists |
| `[P·discovery-ceiling]` | pre-emptive | recognize saturation signal of adversarial review (≥3 consecutive 0-finding rounds) |
| **retroactive-security-design** | **post-attack** | accept ceiling, make successful attack unprofitable in retrospect |
| `[P·airgap-problem-blockchain-vs-reality]` | meta | the airgap is what retroactive closes structurally |

## Honest scope

¬ inventing the components. Clawback cascade in airgap onepager (May 2026). Shapley null-player axiom = Shapley 1953. Indirect reciprocity = Nowak. The design move is composing them as load-bearing properties of the substrate rather than separate optional features.

Field has been pre-emptive-only as long as smart contracts have existed. Retroactive layer is being shipped right now.

## Public references

- `Desktop/retroactive-security-dm-summary-2026-05-25.md` (MLA-formatted version Will published to USD8 group)
- `vibeswap/docs/research/papers/airgap-problem-onepager.md` (May 2026, where clawback cascade is named)
- `vibeswap/docs/research/papers/from-mev-to-gev.md` (GEV framework, broader frame this fits in)
- `Desktop/meefs-retroactive-security-detection-2026-05-26.md` + tldr variant (technical detection answer to Meefs)

## Connects

- `[P·dissolve-attack-surface]` — sibling at pre-emptive layer
- `[P·discovery-ceiling]` — pre-emptive's saturation signal
- `[P·airgap-problem-blockchain-vs-reality]` — parent meta-frame
- `[P·honesty-as-structural-load-bearing-property]` — why this works (load-bearing honesty emerges when defection becomes structurally unprofitable, ¬ deterred-by-policy)
- `[F·claim-needs-structural-enforcer]` — retroactive enforcement IS structural, ¬ promised
- `[P·airgap-problem-onepager]` — 6-mechanism stack where the components live
- `Nowak (indirect reciprocity)` — game-theoretic substrate
- `Shapley 1953 (null-player axiom)` — Shapley sub-component substrate

## Use when

- Partner asks "but what stops attackers if pre-emptive fails?" ⇒ explain retroactive as the answer
- Designing new mechanism ⇒ check both pre-emptive (eliminate surface) AND retroactive (unprofitable-in-retrospect) angles
- Drafting security writeup ⇒ name this primitive instead of inventing the framing fresh each time

## Origin

2026-05-25 USD8 group chat (Will-pitch in response to DM from Meefs). Re-surfaced 2026-05-26 morning ⇒ capture as named primitive so future drafts inherit the framing.
