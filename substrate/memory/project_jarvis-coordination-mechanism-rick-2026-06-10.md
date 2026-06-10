---
name: JarvisCoordinationMechanism
description: Rick TG 2026-06-10 ⇒ JARVIS feature request — analysis-prompt × auto-assign to different models for cost control. *"Budget management — analysis prompt and auto assign to different models to keep cost low. We don't need fable to answer weather questions."* Will-reframe: "coordination mechanism." Rick: "If u have that, would be awesome" ⇒ adoption-signal from a Hermes daily user. Status: captured, design-sketch inline, awaiting Will-call on priority/implementation tier.
type: project
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# JARVIS Coordination Mechanism (Rick-suggested 2026-06-10)

## Origin

TG thread 2026-06-10 morning, after Will sent Rick the hermes-vs-jarvis line ("hermes is basically jarvis without a predestined personality"):

> Rick: "I have a good suggestions for u"
> Rick: "Add a extra fn to that others do not have"
> Rick: "Budget management — analysis prompt and auto assign to different models to keep cost low"
> Rick: "I think this is a great one"
> Rick: "We don't need fable to answer weather questions"
> Will: "coordination mechanism"
> Rick: "If u have that, would be awesome"

## ⇒ Pattern

```
PreDispatch:
  prompt → classifier → {complexity-class, domain-class, urgency}
  class  → router     → model-tier ∈ {haiku, sonnet, opus, off-mesh}
  route  → execute    → (with telemetry on cost vs class)
```

Two axes Rick is pointing at:
1. **Cost-aware tier-select** — cheap model for cheap task
2. **Coordination across substrate** — single dispatch surface for many model-providers (the Hermes-style multi-provider gateway)

## ∃ Why it's load-bearing

- Hermes has this (multi-provider via OpenRouter + cost-aware routing)
- JARVIS currently does NOT — every turn uses whatever Claude Code session has loaded
- Rick uses Hermes daily for non-coding agent tasks specifically because of this
- Rick explicitly said "would be awesome" if JARVIS had it ⇒ first concrete external adoption-signal for JARVIS-OS feature parity

## ↦ Existing JARVIS surfaces this would compose with

- **Agent spawns** already select tier (haiku/sonnet/opus) per autopilot subagent-launch pattern — the spawn-time tier-select exists but is heuristic-by-prompter, not classifier-driven
- **L6 agent overlay** is where this would naturally live (between cognition gate and tool execution)
- **L7 TG bot** already routes across providers for the bot side; this would generalize the pattern to main JARVIS substrate

## ↦ Implementation tiers (sketch — Will-pick)

**Tier 1 (smallest, in-Claude-Code):**
- PreToolUse hook on `Agent` matcher
- Classifies subagent prompt-description → recommends `subagent_type` (haiku-eligible vs sonnet vs opus)
- Augmentation, not block — main agent can override
- Cost: ~50 LoC Python, single hook, reversible

**Tier 2 (skill-based):**
- `/classify` or `/route` skill that takes a task description, returns recommended tier + rationale
- Useful when Will is dispatching subagents manually and wants a sanity check before paying for opus
- Cost: skill manifest + small classifier prompt

**Tier 3 (multi-provider gateway, real coordination layer):**
- Generalizes beyond Claude tier-select to cross-provider routing
- Requires OpenRouter / direct provider keys / API abstraction layer
- Closest to what Hermes ships
- Cost: substantial — touches substrate boundary, ¬ pure-Claude-Code anymore

## ↦ What this is NOT

- ✗ a replacement for WWWD (WWWD = cognition gate, this = dispatch coordination)
- ✗ a Hermes port (this is JARVIS-native, not a wrapper around Hermes)
- ✗ partner-facing commitment (USD8 framing rule: this is a JARVIS feature, ¬ USD8 commitment; if Rick adopts JARVIS later, that's separate)

## ↦ Adoption-roleplay pass (per [P·adoption-roleplay])

**R1 — Rick reading this primitive cold (he won't, but the test):** "Did Will hear me? Yes, captured verbatim. Does Will distinguish tiers I might want? Yes, Tier 1-3 progression matches my cost-axis ask. Adopt-level: would check back in if Will ships Tier 1."

**R2 — Skeptical reader looking at JARVIS substrate cold:** "Reasonable feature request, real adoption-signal, design sketch is appropriately staged. The Tier 3 (multi-provider) is the only one that closes the Hermes gap fully; Tier 1 is JARVIS-internal cost optimization. Both are real wins."

## ↦ Sibling primitives

- [P·adoption-roleplay] — outside-vantage critique that surfaced this as worth capturing
- [F·optimize-code-for-llms] — code optimization rule applies to the classifier itself
- [F·rick-keep-it-simple] — implementation should ship minimal Tier 1 first, ¬ Tier 3 ambitious
- [J·vibeswap-ckb-sovereign-pivot] (orthogonal) — this is JARVIS, ¬ VibeSwap
- Hermes architecture reference: side-by-side at `Desktop/jarvis-vs-hermes-side-by-side-2026-06-10.md`

## Status

- Captured: 2026-06-10
- Rick adoption-signal: ✓ explicit
- Implementation: pending Will-call on tier (Tier 1 is autonomous-eligible if Will approves)
- Priority: HIGH for partnership-deepening with Rick; MEDIUM for cost-optimization
