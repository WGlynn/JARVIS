---
name: JARVIS Network Core Pitch
description: Canonical positioning language for JARVIS Network. Use exact framing when explaining product to customers, Rodney-class community questions, landing copy, investor conversations. 100x-cheaper claim and meta-principle ("one giant model call, every time, with all context loaded") are load-bearing — do not drop or hedge.
type: project
originSessionId: 9557e3af-8773-411b-9ed4-941961f9e5ec
---
# JARVIS Network Core Pitch

**Rule**: When explaining JARVIS Network's architectural advantage, use this framing. Will anchored it on 2026-04-23 after drafting and refining through the Rodney Trotter / Tadija TG thread.

---

## The pitch (verbatim)

> Good instinct on sharding — we run two kinds. Chat-level: a minimal router dispatches TG updates to N workers by chat ID, each one holds only its assigned chats' state. Function-level: separate tool bundles per domain (trading, social, security, memehunter, portfolio), and a workflow router picks the smallest relevant bundle per intent. Both keep individual LLM calls lean — no giant monolithic bot loading everything at once.
>
> But the bigger cost-savers are the ones nobody sees. Every incoming message hits a Haiku classifier deciding "engage or observe" — only about 15% merit the full model, so we pay big-model prices only when a reply actually earns the spend. Structured outputs like digests and stats are template-filled from aggregated data instead of generated prose, which means zero inference tokens for anything deterministic. And the provider layer routes between Claude, free-tier alternatives, and self-hosted options so we pick the cheapest adequate model per task instead of locking into one expensive API.
>
> The retroactive archive helps too, but it was really built to stop hallucination — saves tokens as a side effect, not the primary reason.
>
> The meta-principle: every premium-API wrapper pays for one giant model call, every time, with all context loaded. We shard by function, triage by cost, ground in files instead of tokens, and template anything deterministic. Same output quality, about 100x cheaper. That's the pitch.

---

## Structure (why it lands)

1. **Opens with sharding** — audience-friendly, validates listener's instinct if they asked (Rodney-class).
2. **Middle hits hidden cost-savers** — triage, templates, provider routing. Each has a concrete number (15%, zero, multi-provider).
3. **Archive as side note** — prevents over-indexing on the archive as the answer.
4. **Closes with meta-principle** — "one giant model call, every time, with all context loaded" is the structural argument that makes every other bullet non-contradictable.
5. **"100x cheaper. That's the pitch."** — crystallization + close.

---

## When to use

- **Customer DM asks "how are you cheaper?"** → full version verbatim
- **Community/Rodney-class architecture question** → full version
- **Investor conversation** → full version, numbers land harder
- **Landing copy / README / marketing** → pull five-moves bullets from this
- **LinkedIn post** → wrap per `primitive_concrete-first-post-register.md` (concrete scene → pitch as depth payoff)
- **Telegram group answer** → condensed version (one paragraph, end with "that's the pitch")

---

## Don'ts

- **Don't lead with the archive.** It's a side-benefit. Leading with it buries the cost-saver story and makes the pitch feel like it's about hallucination-control instead of economics.
- **Don't drop the "one giant model call, every time, with all context loaded" line.** That's the structural frame that makes everything else non-contradictable.
- **Don't hedge the 100x claim below ~10x.** Math supports it; v1 Verifiable Claims Roadmap proves it cryptographically.
- **Don't over-technicalize.** "Haiku classifier," "tool bundles," "provider layer" are the right level. Don't swap in "LLM triage orchestrator," "specialized micro-agents," or other SaaS bloat.
- **Don't abandon the exact numbers** (15%, zero, 100x). These are the load-bearing specifics.

---

## Repo location

Extracted as `jarvis-network/docs/pitch.md` — canonical copy for customer-facing reference.

---

## Related

- `primitive_concrete-first-post-register.md` — how to wrap this for LinkedIn/public register
- `feedback_jarvis-as-service-is-vibeswap-marketing.md` — why shipping this pitch to customers amplifies VibeSwap
- `primitive_omni-software-convergence-hypothesis.md` — parent thesis this instantiates
- `primitive_crypto-primitive-selection.md` — the verifiability layer that will prove the 100x claim cryptographically
