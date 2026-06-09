---
name: Wardenclyffe Escalation — Multi-provider inference cascade
description: Start cheap, level up on demand. Qwen 3.6 Plus (free, 0.80 quality) leads Tier 0 for coding/math/moderate. Claude escalation for protocol-specific work. 9 free providers, 22.5M tok/day across 3 shards.
type: feedback
---

Wardenclyffe v3.1 routes inference through 13+ providers across 3 cost tiers. Core principle: start at cheapest adequate tier, escalate on quality failure.

**v3.1 update (2026-04-03):** Qwen 3.6 Plus added as Tier 0 lead. A/B tested: 32/40 vs Claude's 37/40 on DeFi mechanism design. Zero hallucination. Gap is protocol context, not capability.

**Escalation chains (v3.1):**
- `moderate/coding/math` → Qwen[T0] first (0.80 quality, $0)
- `reasoning/complex` → Claude[T2] first, Qwen[T0] as fallback
- `simple` → Groq[T0] (speed > quality for greetings)
- `tooluse` → Claude[T2] (Qwen tool calling untested)

**Capacity:** 22.5M tok/day free across 3 shards (24.3x headroom). Qwen adds 6M tok/day alone.

**Why:** The acute 429 fix (built before TRP bottleneck was diagnosed) proved multi-provider cascade works. Qwen 3.6 Plus elevates the ceiling — a free provider that performs at 80% of premium quality means the escalation chain is now quality-preserving at Tier 0, not just availability-preserving.

**How to apply:** For any task that doesn't require VibeSwap-specific protocol knowledge, try Qwen first. Content drafting, financial analysis, math, research — all route to Qwen at $0. Only escalate to Claude for mechanism design, security review, or tasks requiring the CKB/GKB loaded.
