---
name: Fibonacci Rate Limit (Scale-Invariant)
description: Per-(user,pool) throughput damping at golden-ratio thresholds (23.6/38.2/50/61.8%) + cooldown = window × 1/φ. Scale-invariant ⇒ ¬ preferred timescale ⇒ attacker can't pace under threshold.
type: primitive
originSessionId: 79044125-45c4-486a-9ac0-ec65bb0d9b76
---
# Fibonacci Rate Limit — Scale-Invariant Throughput Damping

## ⚙ Rule
- Linear rate limit ⇒ tells attacker the timescale to operate under ⇒ attack at sweet spot
- Fibonacci rate limit ⇒ scale-invariant curve ⇒ ¬ sweet spot exists
- Per-(user, pool) scoping over 1-hour rolling window
- Saturation (>61.8%) ⇒ cooldown = window × 1/φ ≈ 37 min

## 📍 Source
- `vibeswap/DOCUMENTATION/FIBONACCI_SCALING.md` (213 lines)
- Implementation: `vibeswap/contracts/libraries/FibonacciScaling.sol`
- Instance of: `P·substrate-geometry-match`

## 📊 4 damping zones
- < 23.6% ⇒ no damping (Alice at 30% → barely noticed)
- 23.6 → 38.2% ⇒ mild (linear ramp, ~4-25%)
- 38.2 → 50% ⇒ moderate (~25-50%)
- 50 → 61.8% ⇒ strong (~50-100%)
- ≥ 61.8% ⇒ saturation ⇒ cooldown trigger

## 🧬 Why golden-ratio thresholds (substrate match)
- Market-reversal probability ⇒ technical analysis uses these levels (empirical)
- Attention-recovery rates ⇒ "getting back to focus" follows these levels (psych)
- Biological response curves ⇒ reaction-time distributions under load
- Cooldown 1/φ ≈ 0.618 ⇒ matches natural attention-recovery decay

## 🎯 Why 1-hour window
- 1-min ⇒ too short, normal burst hits it
- 24-hr ⇒ too long, attackers ramp slowly hidden in daily volume
- 1-hr matches: human attention-session (50-90 min) + off-chain decision loops (oracle, governance)

## ⚖ Linear vs Fibonacci comparison
- **Linear cuts at arbitrary 25/50/75%**: substrate has no such boundaries; moderate users hit cap; attackers stay just under
- **Fibonacci cuts at substrate-matched 23.6/38.2/50/61.8%**: friction at points users naturally pause; attackers can't avoid (continuous curve, no plateau to hide in)

## 🔧 Implementation snippet
```solidity
function damping(uint256 fractionOfCap) pure returns (uint256) {
    if (fractionOfCap < 0.236e18) return 0;
    if (fractionOfCap < 0.382e18) return 0.1e18 * (fractionOfCap - 0.236e18) / (0.382e18 - 0.236e18);
    if (fractionOfCap < 0.500e18) return 0.25e18 + 0.25e18 * (fractionOfCap - 0.382e18) / (0.500e18 - 0.382e18);
    if (fractionOfCap < 0.618e18) return 0.50e18 + 0.25e18 * (fractionOfCap - 0.500e18) / (0.618e18 - 0.500e18);
    return 1.0e18;  // saturation → cooldown
}
```

## 📍 Where it fires
- `VibeSwapCore.commitOrder` — before accepting commitment
- `VibeAMM._executeSwap` — before applying swap
- `CrossChainRouter.sendMessage` — before dispatching cross-chain tx

## 🛡 Per-(user,pool) isolation prevents
- Saturated user blocking other users from same pool
- User saturated across pools when active in one
- Cross-pool throughput aggregation masking single-pool attack

## 💥 Sybil mitigation (since per-wallet is gameable)
- OperatorCellRegistry bonds ⇒ expensive per-wallet
- Per-wallet aggregate throughput caps ⇒ secondary limiter
- SoulboundIdentity ⇒ Sybil-resistant identity

## 🚨 USD8 application
- DIRECT-PORT — substrate-independent
- Apply to: large-redemption smoothing | claims throughput during stress | mint flow during yield-strategy migration
- Same constants (23.6/38.2/50/61.8% + 1/φ + 1hr); USD8-specific saturation cap per use case

## ✓ When applicable
- Per-actor throughput limiting where attacker pattern = high-rate burst
- Anywhere "linear cap" feels naive against adaptive adversary
- Contexts with golden-ratio substrate behavior (markets, attention, bio)

## ✗ When inapplicable
- Throughput limits where attacker IS the substrate behavior (e.g., emergency floods)
- Rate limits on ordering / sequencing (use temporal invariants instead)

## 🪝 Triggers
- Rate-limit design discussions
- "should we cap at N per hour?" questions
- Anti-MEV / anti-griefer mechanism design

## ⚠ Anti-pattern
- Linear caps at round numbers (25/50/75%) ⇒ attacker optimizes against them
- Window too short or too long ⇒ substrate mismatch
- Per-pool aggregation across users ⇒ collateral damage to honest users
- Tuning constants for "user friction relief" ⇒ that friction IS the mechanism
- Making constants governance-tunable ⇒ they're substrate-anchored, not policy

## 🔗 Related
- `P·substrate-geometry-match` — parent: golden-ratio matches power-law substrate
- `P·circuit-breaker-attested-resume` — sibling: system-wide trigger vs per-user-per-pool
- `P·first-available-trap` — anti-pattern: linear rate limiters are first-available
