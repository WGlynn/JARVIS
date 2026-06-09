---
name: jarvis-tg-bot-free-tier-inference-only
description: Jarvis TG bot inference ⇒ free-tier ∀ time; paywall ⇒ workaround ¬ pay
type: project
originSessionId: 8e0b2388-5171-43d5-a501-c272f20c2f6f
---
**Rule:** TG-bot inference ∈ free-tier ∀ providers ∀ time.

> *"the tg bot was always and will always be supported by free models, any paywall requires a new workaround on our end"* — Will, 2026-04-30

**Why:**
- bot = free public utility (TG-distributed, open ingress)
- paywall ⇒ {gate-paying-users (✗ character), per-msg-cost-Will (✗ budget)}
- value = overlay (persona / framing-gate / knowledge-chain) ¬ premium-model
- ∴ any free-model good-enough-for-overlay = good-enough

**How to apply:**
- 402/403/429 on provider ⇒ swap-provider ∨ extend-fallback-chain. ✗ top-up.
- code-shape: provider-abstraction + fallback-list + 429-graceful. ✗ single-source paid-API.
- ✗ propose paid-plan ∀ bot. overrides "$X/mo upgrade" suggestions.
- multi-provider keys ⇒ fly.io secrets ¬ code.

**Free-tier provider rank (2026-04, fast→generous):**
- Groq — Llama-3.3-70B / Qwen / DeepSeek-distill, prod-grade, free-tier real
- Cerebras — fastest tok/s, free-tier
- Google-AI-Studio — Gemini-Flash, generous quota
- Cloudflare-Workers-AI — daily-quota
- OpenRouter — `:free` suffix endpoints
- Novita — free-credits exhaust ⇒ ¬ durable (current failure mode)

**Failure mode (2026-04-30):** Novita 403 NOT_ENOUGH_BALANCE on TG bot. Free credits ran out. Workaround pending: swap to Groq primary + fallback chain.
