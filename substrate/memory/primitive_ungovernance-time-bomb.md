---
name: Ungovernance Time Bomb (Governance Decay to Autonomy)
description: Hardcoded exponential decay of governance voting weight ⇒ protocol bootstraps with governance, ends without it. Solves parametric tuning + protocol autonomy in one mechanism. VibeSwap canonical.
type: primitive
originSessionId: 1b63b789-9726-4714-ba12-c4475b71d433
---
# Ungovernance Time Bomb

> *"governance time bomb, which gives the protocol a certain number of years to settle on weights and parameters for the parametric contract outputs before the governance weight winds down to zero"* — Will to Rick, 2026-04-28

## ⚙ Rule
- Governance = bootstrapping tool ¬ permanent fixture
- Hardcoded decay ⇒ ¬ vote-changeable ⇒ governance dies on schedule
- weight(t) = initialWeight × (1/2)^(t / halfLife)
- Default halfLife = 1yr ⇒ year 10 = 0.098% of original
- Supermajority threshold ⇒ governance mathematically impossible past N halvings
- Bootstrap-with-training-wheels-that-retract

## 🚨 Solves
- Whale capture (Compound/MakerDAO failure mode)
- Voter apathy (<5% participation universal)
- Governance attacks (Beanstalk $182M flash-loan-governance)
- Political rent-seeking (Curve wars)
- Ossification (Bitcoin block size deadlock)
- "We can codify rules, just don't know which ones at build time" — gives a window for empirical settling, then locks in

## 🔧 How to apply
- Genesis: full governance authority, 100% voting weight
- Operation: governance tunes parameters using real-world data
- Decay: every halfLife seconds, voting weight halves
- Terminus: weight → 0; final values become constitutional (Cincinnatus-style)
- ¬ optional ¬ vote-changeable ⇒ encoded in immutable contract logic

## 📊 Example: 1yr half-life
| Year | Voting Weight |
|---|---|
| 0 | 100% |
| 1 | 50% |
| 2 | 25% |
| 5 | 3.125% |
| 8 | 0.39% |
| 10 | 0.098% |

## 📍 Implementation pattern (Solidity sketch)
```solidity
function getVotingWeight(address voter, uint256 proposalTime) public view returns (uint256) {
    uint256 balance = governanceToken.balanceOf(voter);
    uint256 elapsed = proposalTime - GENESIS_TIMESTAMP;
    uint256 halvings = elapsed / HALF_LIFE_SECONDS;
    uint256 remainder = elapsed % HALF_LIFE_SECONDS;
    // Fixed-point decay; supermajority threshold makes proposals impossible
    // once cumulative weight drops below quorum
}
```

## 🔍 Why it works (mechanism design)
- **Forced settlement** ⇒ governance has window to converge ¬ indefinite-vote-fatigue
- **Empirical-tuning friendly** ⇒ admin/governance phase = when chain data accumulates; settling phase locks empirically-validated values
- **Trust-minimization terminus** ⇒ protocol becomes self-adjusting (thermostat ¬ committee)
- **Static + dynamic resolved** ⇒ weights ARE dynamic during countdown; become fixed at terminus; one mechanism, both regimes
- **Anti-capture by design** ⇒ even if governance is captured, capture has expiration date

## 🪝 Triggers
- "How do we go from admin → governance → autonomous?" question
- Parametric contract design where values need tuning but ultimate fixity is desired
- Avoiding indefinite-DAO-governance failure modes
- Solving "fixed vs dynamic weights" design tension
- Cincinnatus-aligned founder/governance walkaway

## ⚠ Anti-pattern
- Governance with no sunset ⇒ accumulating capture surface
- Sunset that's vote-changeable ⇒ governance votes to extend itself ⇒ defeats purpose
- Linear decay ⇒ provides no "soft landing" — exponential half-life lets governance taper organically
- Sunsets without empirical-tuning window ⇒ values frozen before real-world data validated them

## 🔗 Related
- `P·cincinnatus-walkaway-test` — founder-walkaway sibling; this is governance-walkaway
- `P·augmented-governance` — Physics > Constitution > Governance hierarchy; this is governance's terminal state (decays to zero, constitution remains)
- `P·hobbesian-trap-dissolution` — IIA removes weapons; ungovernance time bomb removes the governance attack vector via timer

## 📍 Source
- Canonical doc: `vibeswap/docs/ungovernance-spec-2026/ungovernance-spec-2026.md` (Faraday1, JARVIS, March 2026)
- Implementation: VibeSwap governance contracts
- USD8 partnership-facing reference: 2026-04-28 Will → Rick chat (alignment update on weight-progression question; v1 invariants stated as reliability + leanness + determinism)

## 🚨 USD8 application
- Cover Score weight registry has admin-tuneable weights v1
- Governance time bomb = the answer to Rick's "admin → governance → autonomous" stage progression
- Parameters tuned from real holder/cover-pool data during the bomb's countdown
- Final weights become constitutional after decay completes
- Resolves "fixed vs dynamic weights" — both, on a deadline
