---
name: Fly.io deploy verification gate
description: Never trust flyctl deploy exit code alone — always verify bot is actually running via logs
type: feedback
---

After `flyctl deploy` reports "Machine is now in a good state", the bot may still be crash-looping. Fly's deploy check passes when the VM boots, NOT when the app is functional.

**Why:** Session 2026-03-17 — deployed 3 TG bots, reported them as "live" when they were actually crash-looping with a SyntaxError. Fly's 120s health check grace period meant the deploy tool declared success before Node.js even attempted to load index.js.

**How to apply:** After EVERY Fly.io deploy, tail logs and look for the actual success confirmation line (`JARVIS IS ONLINE` for jarvis-vibeswap/jarvis-degen, `Bot running` for chatterbox). Do NOT tell Will bots are "live" or "running" based solely on flyctl output. Deploy success = app-level confirmation in logs, not infrastructure-level "started" state.
