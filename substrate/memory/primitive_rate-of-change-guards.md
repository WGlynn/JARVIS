---
name: Rate-of-Change Guards
description: Any state variable observable by external actors must have bounded rate-of-change to prevent single-transaction manipulation. Absolute bounds aren't enough — velocity matters.
type: feedback
---

# Rate-of-Change Guards

Limiting HOW MUCH a value can change is necessary but insufficient. You must also limit HOW FAST it can change.

**Why:** TRP found three distinct instances where absolute bounds existed but rate-of-change was unbounded:
- R48 (NEW-05): Liquidity state could be spoofed by a compromised peer in a single message — fixed with 50% rate-of-change limit per sync
- R41 (AMM-05): TWAP could drift without bound within a single window — fixed with per-window drift cap (200 bps) and golden-ratio damping
- R24 (CB-05): Circuit breaker window value was stale after cooldown, causing immediate re-trip — fixed with auto-reset after cooldown

**How to apply:**
1. For every state variable that external actors can observe or influence, define a maximum delta per time unit
2. TWAP oracles: cap per-update price movement AND per-window cumulative drift
3. Liquidity sync: cap percentage change per message/block
4. Circuit breakers: reset accumulation windows after cooldown periods
5. Rate limits: use fixed windows with explicit reset, not sliding windows (simpler, cheaper, harder to game)

**Generalization:** Rate-of-change guards are the derivative of value guards. If you only check `|x| < MAX`, an attacker can move x from -MAX to +MAX in one step. If you also check `|dx/dt| < RATE`, manipulation requires sustained effort over time — which is observable and stoppable. This applies to: oracle prices, governance parameters, token supplies, pool ratios.
