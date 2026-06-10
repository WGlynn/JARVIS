---
name: Cross-Port Function-Variable Audit
description: Mechanism port → audit each fn-variable pair independently. Carrier ports ✓, payload doesn't auto-port. Recursive substrate-match at fn-level ¬ just mechanism-level.
type: primitive
originSessionId: 1b63b789-9726-4714-ba12-c4475b71d433
---
# Cross-Port Fn-Variable Audit

## ⚙ Rule
- Mechanism port (A→B) ⇒ carrier ✓ ¬ payload
- Carrier = mechanism shape (cooperative-game math, distribution, fee routing) ⇒ ports ✓
- Payload = function-shapes inside the mechanism (log/linear/sqrt/etc) ⇒ ¬ auto-port
- Each fn operates on a variable ⇒ variable physics determines fn shape
- Re-derive fn from B's variable physics ¬ copy A's

## 🔧 Audit protocol
1. List every fn inside the mechanism (¬ just top-level)
2. ID variable each fn operates on
3. A.variable.physics ≟ B.variable.physics
4. ✓ ⇒ fn ports | ✗ ⇒ re-derive from B's physics

## 🚨 Origin — 2026-04-28 USD8 log→linear miss
- Shapley spec ported 5/6 components VibeSwap → USD8
- Duration component used logarithmic ⇒ copied from VibeSwap unchanged
- VibeSwap LP commitment = attention/memory variable ⇒ Ebbinghaus log-decay ✓
- USD8 cover-pool duration = capital-at-risk-time ⇒ every day = same risk weight ⇒ linear physics
- Log compresses long-vs-short tenure spread ↓ ⇒ under-rewards stickiness
- Cover pool wants spread expanded ↑ ⇒ linear correct
- Rick caught: *"the rationale does not justify using logarithmic value"*

## 📐 Failure mode (named)
- Substrate-Geometry Match applied at mechanism-level ✓
- ¬ recursed to fn-level inside mechanism
- "Carrier ports, payload doesn't"
- Level-of-abstraction error

## 🚨 Why existing taxonomy missed it
- `P·first-available-trap` ⇒ fires on "pick first analog ¬ substrate-check" ⇒ we DID substrate-check (mechanism-level) ⇒ trap deeper than rule-tuning
- `P·pattern-match-drift-on-novelty` ⇒ fires on "novelty resists analog" ⇒ VibeSwap-LP ≈ USD8-LP user-facing ⇒ novelty was in variable physics ¬ user-facing concept
- "5/6 components port" framing ⇒ smoking gun ⇒ high-fidelity-sounding ⇒ ↓ skepticism on cleanly-marked components
- Rewrite framing ⇒ "5/6 carriers port; each fn inside requires independent variable audit"

## 🔬 Common variable-physics mismatches
- Attention/memory (log-decay) ↔ capital-at-risk-time (linear)
- Liquidity-density (continuous, fractional) ↔ deposit-count (discrete, integer)
- Per-batch microbehavior (high-freq, fractal) ↔ per-period commitment (low-freq, sticky)
- Adversarial setting (sybil-game-relevant) ↔ proportional setting (sybil-irrelevant)

## 🔍 Lens-complementarity (Rick's filter)
- Substrate-match: "shape right for substrate?"
- Complexity-justification: "complexity have defensible reason?"
- ⇒ complementary
- Substrate-match @ wrong level ⇒ complexity-filter catches it
- Complexity-without-substrate-justification = substrate-mismatch signal @ deeper level
- ⇒ apply both filters in sequence on cross-port designs

## ✓ Validation tests
- Catches log→linear before shipping ✓
- ¬ over-fires on genuine mechanism-ports ✓
- Surfaces variable-physics deltas early in cross-port convo ✓

## 🪝 Triggers
- Cross-protocol mechanism transfer
- "X% of components port from Y" framing
- Function-shape choice during port (log/linear/sqrt/exp)
- "Why this curve?" question without substrate-anchored answer

## ⚠ Anti-pattern
- Port whole mechanism + functions atomically ⇒ no fn-level audit gate
- "It worked there so it'll work here" ⇒ carrier-payload conflation
- Defending source-substrate fn shape vs destination-substrate evidence

## 🔗 Related
- `P·substrate-geometry-match` — parent ⇒ this is recursive application @ fn-level
- `P·first-available-trap` — sibling ⇒ whole-mechanism analog choice
- `P·pattern-match-drift-on-novelty` — sibling ⇒ user-facing novelty trigger
- `F·rick-keep-it-simple` — Rick's complexity-filter caught it where ours missed

## 📍 First instances of correct application
- USD8 Shapley duration: log→linear (corrected 2026-04-28)
- USD8 history compression: complex IncrementalMerkleTree+Tornado → lazy+signed+optimistic-dispute (corrected 2026-04-28; carrier-shape itself didn't port — different access pattern)
