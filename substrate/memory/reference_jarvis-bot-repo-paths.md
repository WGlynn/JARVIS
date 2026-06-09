---
name: jarvis-bot-repo-paths
description: Where the jarvis bot code lives on disk — production bot, upstream repo, substrate harness
type: reference
originSessionId: 8e0b2388-5171-43d5-a501-c272f20c2f6f
---
**Production TG bot (deployed to fly.io):** `C:\Users\Will\vibeswap\jarvis-bot\`
- multi-shard fly configs: `fly-shard-{1,2,ap,eu,sa,archive,ollama,degen}.toml`
- Dockerfile + Dockerfile.local + Dockerfile.ollama
- src/, knowledge/, memory/, scraper/, scripts/, webapp/, voice-bridge.html
- persona.js V1/V2/V5/V6 + intelligence.js editor live in src/
- last bot-deploy commit: `c8f3e4c6` (blocked on fly.io billing as of 2026-04-30)

**Public/marketing repo (jarvis-network):** `C:\Users\Will\jarvis-network\` (renamed from `~/jarvis\` on 2026-05-03)
- ↔ `github.com/WGlynn/jarvis-network` (origin)
- ARCHITECTURE.md / CHANGELOG.md / LAUNCH.md / LICENSE / deck/ / landing/
- separate from production bot — public release of the simpler core, marketing-facing

**Canonical scaffold + papers (JARVIS):** `C:\Users\Will\JARVIS\` (renamed from `~/jarvis-monorepo\` on 2026-05-03)
- ↔ `github.com/WGlynn/JARVIS` (origin)
- 8-layer scaffold (`01-hooks/`, `02-persistence/`, ..., `08-filesystem-as-substrate/`) plus `verify/` and `papers/`
- Hosts the canonical paper triad: `jarvis-is-not-a-wrapper`, `how-jarvis-works`, `substrate-port`

**Substrate comparison harness:** `C:\Users\Will\jarvis-substrate-comparison\`
- DeepSeek substrate eval (incomplete per WAL 2026-04-30)
- `compare.py` is the entry point

**Template scaffolding:** `C:\Users\Will\vibeswap\jarvis-template\`
- empty/template version, not the live bot

**Desktop:** `C:\Users\Will\Desktop\Jarvis_as_a_Service\` (Apr 23) — separate JaaS exploration, not the TG bot.

**When Will says "the bot" or "TG bot" or "jarvis bot":** default to `vibeswap/jarvis-bot/` unless context says otherwise.
