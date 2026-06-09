---
name: TRP Agent Concurrency — Cap at 2
description: Max 2 concurrent opus subagents during TRP to avoid saturating Anthropic API rate limit, which knocks out TG Jarvis bot
type: feedback
---

Cap TRP subagent concurrency at 2 (not 3+). Running 3-4 opus agents simultaneously saturates the Anthropic API rate limit, causing the Telegram Jarvis bot to hit rate limit errors and go offline for ~60s.

**Why:** Observed 2026-04-02 — TRP R22-R27 spawned 3 concurrent opus agents, Jarvis TG bot showed "AI provider rate limit hit" errors twice. Jarvis and Claude Code share the same Anthropic account rate limit.

**How to apply:** During TRP rounds, dispatch max 2 subagents at a time. If 3 loops need sharding, run 2 in parallel then 1 after. Serialize more aggressively. The speed cost is small vs knocking out Jarvis.
