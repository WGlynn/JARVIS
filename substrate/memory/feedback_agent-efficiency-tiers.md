---
name: Agent efficiency — model tiers + shared context + terse outputs
description: Use haiku/sonnet/opus tiers for agents based on task complexity. Shared context in .claude/AGENT_CONTEXT.md. Keep status updates and WAL checkpoints minimal.
type: feedback
---

# Agent Efficiency Protocol

**Why:** Session hit rate limit with 5 agents still in-flight (2026-03-26). Money is a constraint. Most test-writing agents ran on opus unnecessarily — 5x the cost of sonnet for equivalent output.

**How to apply:**

## Model Tiers
```
haiku:   Commit orphaned files, NatSpec, cleanup, simple grep-and-fix, rename ops
sonnet:  Writing tests, deploy scripts, documentation, code review, coverage audits
opus:    Mechanism design, security review, ethresear.ch posts, gas optimization, architecture
qwen:    Financial analysis, math, content drafting, non-protocol-specific reasoning (via OpenRouter, $0)
```
Use `model` parameter on Agent tool: `"model": "haiku"` or `"model": "sonnet"`.
For Qwen tasks, use `scripts/llm-compare.sh` or direct OpenRouter API calls.

**Qwen 3.6 Plus (added v3.1):** 0.80 quality score, 1M context, zero hallucination on A/B test vs Claude. Use for tasks that don't require VibeSwap protocol-specific knowledge. The gap is context, not capability — load the protocol docs and it performs near-Claude level. Free tier = infinite budget for content generation, financial analysis, and research.

## Shared Context
`.claude/AGENT_CONTEXT.md` contains: repo location, Solidity conventions, commit format, push instructions. Agent prompts should say "Read .claude/AGENT_CONTEXT.md for conventions" instead of repeating boilerplate. Saves ~200 tokens per agent prompt.

## Terse Outputs
- Status updates: one line per completed agent, not a paragraph
- WAL checkpoints: every 5-7 completions, not every 3
- Agent prompts: one paragraph task description max. Context file handles the rest.

## Mitosis Tuning
- k=1.3 for mixed-priority work (default)
- k=1.0 for homogeneous waves (e.g., all test-writing)
- k=0.7 for wind-down / end of session
