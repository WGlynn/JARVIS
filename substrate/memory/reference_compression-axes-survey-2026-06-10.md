---
name: Compression axes survey 2026-06-10
description: 3-agent research sweep covering context, model/inference, and orchestration/reasoning compression axes. Ranked decision tree for solo-operator Claude/Codex substrate. Cite when picking next compression layer.
type: reference
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# Compression Axes Survey — 2026-06-10

## Glyph

```
COMP-SURVEY  3-axis sweep: context × model-inference × orchestration.
             ranked-by: solo-Windows-operator-leverage.
             top-leverage: HIERO-compression × Anthropic-prompt-cache
                          = multiplicative ! additive.
```

## The compounding insight

`HIERO-compression (byte-saved-at-boot) × prompt-cache (0.1x cost-per-cached-read) × N-turns/session = order-of-magnitude session cost cut`

Today's structural compression: MEMORY.md 6,779 -> 3,026 tok. If harness flags as cache-eligible, every subsequent turn pays 10% of full cost on that block. We control the byte side; harness controls the cache flag.

## Ranked table

| # | move | win-empirical | cost | ship |
|---|------|---------------|------|------|
| 1 | prompt-cache breakpoint on boot | 90% read discount | API-native; harness-controlled | investigate |
| 2 | code-mode nudge (N tool calls -> 1 script) | 150k -> 2k tok (98.7%) Anthropic Nov-2025 | PostToolUse hook 200 LOC | SHIPPED 2026-06-10 `code-mode-nudge.py` |
| 3 | single-agent default + cascade router | FrugalGPT 98% cost cut @ GPT-4 quality | hook + threshold | extend coord-gate |
| 4 | demote low-fire PRE-FLIGHT entries to hooks | 100-500 tok/turn per rule converted | audit + per-rule hook | pending fire-count read |
| 5 | round-trip benchmark (BERTScore / task quality) | closes measurement gap | 3 hrs | ship next |
| 6 | LLMLingua-2 on WARM-MAP only | 2-5x prose, CPU-only | 3 hrs + [PRESERVE] fences | conditional |
| 7 | llama.cpp Q5_K_M + KV INT8 + spec-decode | 2x throughput zero-finetune | local infra Jarvis-bot | conditional |
| 8 | speculative tool exec (PostToolUse predicts next read) | no public impl - publishable | 200 LOC | research surface |

## Skip / park

* Gisting / ICAE / AutoCompressor -> need fine-tune access we don't have on Claude
* MoE on laptop -> VRAM bound (total-params NOT active-params)
* Quiet-STaR / Tree-of-Thought pruning -> our tasks aren't search-tree shaped
* 2:4 sparsity / Wanda -> ecosystem thin on Windows
* MXFP4 / MLA / BitNet -> hardware-dependent or pretrain-only

## Validating data points

* Anthropic "Code execution with MCP" (Nov 2025): 150k -> 2k tok customer trace
* Cognition "Don't Build Multi-Agents" (Jun 2025): 3-15x overhead on shared-context tasks
* AgentBoard (Chang NeurIPS 2024): single-agent ties multi on 64% HotpotQA/WebShop @ 50% cost
* FrugalGPT (Chen 2023): 98% cost @ GPT-4 quality via cascade
* LLMLingua-2 (Microsoft 2024): 2-5x compression, 1-2 pt task drop
* Anthropic prompt cache: 0.1x reads (90% off), 1.25x writes, 5-min TTL
* EAGLE-3 (2025): 5x lossless speculative decoding

## Honest gaps

* compression numbers in our shipped state (4-7%, 42%, 55%, 22%) lack BERTScore/task-quality benchmarks -> measurement gap until #5 ships
* prompt-cache eligibility is harness-controlled (Anthropic side) -> we can't verify the multiplicative win until we observe it in billing/telemetry
* tokenizer-aware writing has no formal academic discipline -> HIERO++ is publishable (no one else owns this corner)

## Decision tree (which compression to ship next)

```
session-cost-cut-needed?
  yes -> is harness-cache-eligible boot block stable?
         yes -> wait for cache hit-rate telemetry; biggest lever
         no  -> code-mode nudge + cascade router (next 2 ships)
  no  -> measurement defensibility needed?
         yes -> round-trip benchmark
         no  -> LLMLingua-2 on WARM-MAP (long-tail prose savings)

local-inference-fallback-needed?
  yes -> llama.cpp Q5_K_M + KV INT8 + prompt-lookup (zero finetune)

publishable-research-surface?
  yes -> speculative tool exec (PostToolUse predicts next read; no public impl)
```

## Sibling memory

* `[R·compression-layer-stack]` -> L0..L6 stack across substrate
* `[R·hiero-pp-dictionary]` -> tokenizer-tuned lexicon
* `[P·option-value-notation-infrastructure]` -> why CAPEX on notation pays back
* `[P·universal-coverage-hook]` -> rule-to-hook demotion theory
* `[F·token-blind-multi-agent-default-is-anti-pattern]` -> validated by Cognition + AgentBoard data above

## Source agents (2026-06-10)

* Agent A: context compression frameworks -> LLMLingua-2 / LongLLMLingua / Gisting / RECOMP / ICAE / MemGPT / A-MEM / tokenizer-aware writing
* Agent B: model + inference compression -> Anthropic prompt-cache / MXFP4 / llama.cpp GGUF / AWQ / EXL2 / speculative decoding / EAGLE-3 / KV-cache quant / FlashAttention / SnapKV / MoE / MLA / QuaRot / BitNet
* Agent C: orchestration + reasoning compression -> code-mode orchestration / Anthropic prompt-cache / single-agent default / FrugalGPT cascade / Skeleton-of-Thought / Self-Consistency gating / hook behavioral compression / JIT retrieval / speculative tool execution
