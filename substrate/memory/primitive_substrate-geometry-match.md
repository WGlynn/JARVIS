---
name: Substrate-Geometry Match (Ultimate Design Principle)
description: THE parent design principle from which First-Available Trap, mechanism-fit analysis, and most downstream mechanism choices derive. Match the mechanism's scaling to the substrate's natural geometric form (fractal, self-similar, power-law, golden-ratio). Mismatch is the failure mode; the "sophisticated" answer is usually just letting the substrate's own shape through. Will 2026-04-21: "this is the ultimate design principle."
type: primitive
originSessionId: 117e2fd9-3ef3-4610-a5b4-d4280a0b96cb
---
# Substrate-Geometry Match — Ultimate Design Principle
## (canonical name: "As Above, So Below" applied to mechanism design)

**Status**: Parent principle. Will 2026-04-21: *"this is the ultimate design principle"* and *"it's just 'as above so below' applied to mechanism design."* Generator of First-Available Trap and most downstream mechanism-fit decisions. Load-bearing above individual primitives — when other primitives conflict, resolve by asking which form is closer to substrate geometry.

**Canonical form**: The hermetic maxim — *"That which is Below corresponds to that which is Above, and that which is Above corresponds to that which is Below, to accomplish the miracle of the One Thing"* (Emerald Tablet, ~100 BCE-300 CE). In mechanism design: the structure at macro scale (fractal markets, power-law distributions, natural scaling) must be reflected in the micro scale (individual mechanisms). Correspondence between levels is the load-bearing property. Mandelbrot's fractal-market hypothesis is one mathematical formalization of the macro-scale observation; Fibonacci scaling in VibeAMM is one micro-scale instantiation.

**Rule**: When designing a mechanism that operates on a substrate with known geometric or statistical properties (fractal self-similarity, power-law distribution, golden-ratio scaling, heavy-tailed returns), the mechanism's scaling curve should match the substrate's natural form. Mismatches create impedance: the mechanism either over-constrains common-case behavior or under-responds to tail events.

**Why**: Will's framing, 2026-04-21: *"everything travels in fractal form so I just figured money should as well. it's not complicated."* Market prices are fractal (Mandelbrot's thesis, validated for decades — *The Misbehavior of Markets*, 2004). Natural systems from vascular networks to leaf arrangements follow Fibonacci / golden-ratio progressions. Heavy-tailed return distributions are the norm, not the exception, in real markets.

A rate-limiter, fee curve, or capacity allocator applied to this substrate is matched if its own scaling is fractal/self-similar, mismatched if it is linear/binary. The mismatch shows up as: cliffs (binary halts during gradual stress), over-constraint in common regimes (flat caps that throttle healthy activity), under-response in tail regimes (linear bounds that saturate trivially). The match shows up as: graceful degradation, cost that scales with impact, no special-case stress logic.

VibeSwap's Fibonacci throughput scaling (`contracts/libraries/FibonacciScaling.sol`) is a deployed instance: damping along 23.6 / 38.2 / 50 / 61.8 / 78.6% retracement levels, saturation cooldown = window × 1/φ. It was not a "sophisticated engineering choice" per Will; it was the obvious consequence of not jamming market flow through the wrong geometry.

**How to apply**:
1. Before designing a mechanism, name the substrate's known geometric properties. If the substrate is markets: fractal, heavy-tailed, scale-invariant across timeframes.
2. Check your candidate mechanism's scaling curve against the substrate. Linear mechanism on fractal substrate = mismatch.
3. Prefer mechanisms whose mathematical shape matches the substrate's: Fibonacci / golden-ratio / power-law / logarithmic progressions rather than linear bounds or binary cliffs.
4. Corollary: when the substrate's shape is unknown, *measure first*. Don't assume linearity. Most real-world systems are not linear; assuming linear is itself the first-available trap for mechanism geometry.

**Connection to First-Available Trap**: the first-available mechanism shape in software engineering is linear / binary — `if x > threshold: halt`. This is natural because software is deterministic and the linear form is cognitively cheapest. But deterministic software operating on non-linear reality inherits the mismatch. Substrate-Geometry Match is the positive mechanism-fit rule; First-Available Trap is the negative diagnostic (§5 of `vibeswap/DOCUMENTATION/FIRST_AVAILABLE_TRAP.md`).

**Broader applications**:
- **Fee curves**: volatility fees that scale along golden-ratio tiers rather than step-function brackets.
- **Liquidation thresholds**: continuous stress-derivatives rather than binary LTV cutoffs.
- **Token emission**: log-decay / Fibonacci-weighted rather than linear.
- **Governance thresholds**: superlinear-with-controversy rather than fixed quorum.
- **LLM context budgets**: tier-loaded by situation relevance (what we did to MEMORY.md 2026-04-21) rather than flat always-loaded.

**Related primitives**:
- `primitive_fractalized-shapley-games.md` — the same self-similarity intuition applied to contribution attribution (influence is fractal; flat git commits are the wrong geometry)
- `primitive_first-available-trap.md` — the diagnostic: detects when mechanism geometry mismatches substrate
- `primitive_symbolic-compression.md` — dense glyph representations inherit self-similarity from natural language
- `economitra.md`, `ergon-monetary-biology.md` — monetary systems as biological / natural-system analogs

**Watch for**: the phrase "it's not complicated" when the mechanism is non-obvious to outsiders. Will uses this when a design emerged from seeing the substrate's shape plainly. It's a signal that the primitive is load-bearing, not that the idea is shallow.
