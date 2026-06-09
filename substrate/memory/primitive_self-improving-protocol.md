---
name: Self-Improving Protocol Pattern (OpenClaw-RL Adapted)
description: 4 concurrent loops that make any AI-integrated protocol improve automatically from usage. Policy serving + rollout collection + reward judging + weight updates. The agent gets smarter every conversation.
type: project
---

# Self-Improving Protocol — 4 Concurrent Loops

Source: Princeton OpenClaw-RL (2026), adapted for VibeSwap/Jarvis.

## Core Insight

> "Every interaction contains an implicit reward signal. Every correction is a gradient.
> Every re-query is a reward signal. The agent didn't get retrained. It got used."

## The 4 Loops

### Loop 1: Policy Serving (llm-provider.js — Wardenclyffe)
- 13-provider cascade across 3 tiers
- Tier -1 (local/Ollama) → Tier 0 (free: Groq/Cerebras) → Tier 1 (budget: DeepSeek) → Tier 2 (premium: Claude)
- Complexity-based routing: simple messages stay cheap, complex ones escalate
- The policy IS the response — whatever the LLM outputs is the "action"

### Loop 2: Rollout Collection (self-improve.js — recordRollout)
- Every interaction is a rollout: user message → bot response → user reaction
- Captures: userId, chatId, message, response, signal, provider, latency
- Tracks provider performance per reward signal (which providers produce better outcomes)
- Feeds into Loop 4 for adaptation

### Loop 3: Reward Judging (reward-signal.js — extractSignal)
- Extracts IMPLICIT signals from user behavior:
  - **Negative:** re-ask (failure), correction (gradient), frustration (emotional), abandonment (total fail)
  - **Positive:** thanks (success), followup (engagement), emoji (emotional), adoption (practical)
  - **Neutral:** acknowledge, continue
- Extracts CORRECTION DIRECTIONS (token-level supervision):
  - "you should have checked the file first" → behavioral rule
  - "no, do X instead" → specific guidance
- Rolling score (0-1) with exponential moving average
- Per-user satisfaction tracking

### Loop 4: Weight Updates (self-improve.js — runAdaptationCycle)
- Since we can't update LLM weights, we update the PROMPT
- The prompt IS the weights in a prompt-engineering paradigm
- Every 10 min: checks accumulated signals → generates prompt overlay
- Prompt overlay contains:
  - Behavioral corrections from user feedback
  - Performance alerts (high re-ask rate, frustration, accuracy)
  - Positive reinforcement when trend is improving
- Provider scoring: which LLMs produce the best user reactions

## Design Principles

1. **Non-blocking:** All loops run concurrently, none waits for another
2. **Graceful degradation:** If any loop fails, others continue
3. **Token-efficient:** Signals extracted via pattern matching, not LLM calls
4. **Privacy-preserving:** Only aggregated scores persist, not raw conversations
5. **Self-correcting:** Negative trends trigger automatic behavioral adaptation

## The Key Distinction

- **Traditional:** collect data → train offline → deploy → hope
- **This pattern:** deploy → extract signal from every interaction → adapt continuously → improve automatically

The protocol gets smarter every time someone talks to it.

## VibeSwap-Specific Adaptations

- Shard memory (shard-memory.js): compressed semantic memory for cross-shard context
- Cross-context (cross-context.js): DM ↔ group awareness per user
- Shard dedup (shard-dedup.js): coordinate responses when multiple shards in same group
- Bidirectional mesh monitor: every node watches every other node

## The Vision

A self-improving DEX that passively, actively, and proactively improves 24/7.
The more users it has, the smarter it gets. Not through retraining — through usage.
