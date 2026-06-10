---
name: InworldRoutingAsTier3Reference
description: Inworld Router routes on business-level metrics (cost-per-output-quality × latency-target × task-complexity) across 200+ LLMs. ≡ Rick TG 2026-06-10 coordination-mechanism pitch productized. Reference architecture for [J·jarvis-coordination-mechanism] Tier 3 multi-provider gateway. ¬ adopt-as-is (closed product); borrow routing-shape only.
type: feedback
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# Inworld Routing as Tier 3 Reference

## Glyph

```
Inworld Router routing-fn ⇒ f(cost-per-output-quality × latency-target × task-complexity)
                         ⇒ select-provider ∈ {200+ LLMs}
≡ Rick TG 2026-06-10 ask: "analysis prompt × auto-assign to different models to keep cost low"
↦ JARVIS Tier 3 reference (¬ install)
```

> Rick: *"We don't need fable to answer weather questions."* (TG 2026-06-10)
> Inworld: business-level routing on quality × latency × complexity

## ⇒ Borrowable shape (¬ product)

Routing function:
1. Classify task ⇒ {complexity-class, quality-floor, latency-budget}
2. Score providers ⇒ ∀ candidate: (quality-fit × cost-efficiency × latency-fit)
3. Select max-score provider, fallback chain on failure
4. Telemetry: cost-actual vs cost-expected, quality-feedback signal

## ⇒ Why ¬ install Inworld directly

- closed product (not open-source)
- introduces Inworld dependency in critical path
- Will's substrate values local-first + minimal external deps
- the SHAPE is the value, ¬ the product

## ⇒ For Tier 3 implementation

- adopt routing-fn shape (3-factor cost/quality/latency)
- substrate: Bifrost (open-source, self-hosted, 11μs overhead) ⊃ Inworld closed
- classifier upgrade: extend coordination-mechanism-gate.py with quality-floor + latency-budget params (currently only tier-class)
- new metric tracking: cost-actual vs class-expected over time

## ⇒ Tier-progression

- Tier 1 (✓ shipped 2026-06-10) ⇒ haiku/sonnet/opus tier-select PreToolUse hook
- Tier 2 (✓ shipped 2026-06-10) ⇒ /classify skill (manual sanity check)
- Tier 3 (referenced here) ⇒ multi-provider routing-fn @ Bifrost substrate
- Inworld pattern = Tier 3 design spec, ¬ Tier 3 implementation choice

## ↦ Siblings

- [J·jarvis-coordination-mechanism-rick-2026-06-10] ⇒ parent project
- [R·research-batch-2026-06-10] ⇒ source of finding
- [P·code-mode-orchestration] ⇒ orthogonal Tier-X (token reduction layer)
