---
name: Research batch 2026-03-17 — x402 AWS, Codex subagents, TradingAgents, RL self-locking, Turing test
description: Six references absorbed in session — x402 validation, multi-agent patterns, RL pitfalls, personality design validation
type: reference
---

**1. AWS x402 Reference Architecture (Base mainnet)**
- AWS published Lambda@Edge 402 + Agentcore USDC micropayments on Base
- We shipped x402 with bloom filters + signed receipts BEFORE this publication
- Validation: our approach is ahead of AWS's reference architecture
- Source: aws.amazon.com/blogs/industrial (via Will's TG share)

**2. OpenAI Codex Subagents**
- Parallel specialized agents (default/worker/explorer) with TOML configs
- Our shard architecture does the same + CRPC consensus verification
- Source: https://developers.openai.com/codex/subagents

**3. TauricResearch/TradingAgents**
- Multi-agent trading: analyst team → bull/bear debate → execution + risk mgmt
- Built on LangGraph, supports Claude
- Bull/bear debate = CRPC applied to market thesis — Diablo's trading shard could absorb
- Source: https://github.com/TauricResearch/TradingAgents

**4. Information Self-Locking in RL (Zou et al.)**
- Agents get stuck in low-information loops, stop asking good questions
- Solution: directional critiques (not naive feedback fishing)
- Validates our decision to gut feedback-fishing from Jarvis
- Source: https://arxiv.org/abs/2603.12109

**5. Turing Test Passed by Being Worse (Jones et al., 2025)**
- GPT-4.5 passed at 73% with casual/typo/ignorant persona vs 36% without
- Validates Jarvis personality: imperfection IS the intelligence signal
- "The bar for 'human' was never as high as we thought"

**6. Incompleteness (intuitionmachine, Gumroad)**
- Gödel's incompleteness applied to AI — no system both complete and consistent
- Aligns with our design: honest about limits > pretending completeness
- Source: https://intuitionmachine.gumroad.com/l/incompleteness
