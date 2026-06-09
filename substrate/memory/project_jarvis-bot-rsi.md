---
name: Jarvis Bot R1 — Adversarial Security Audit
description: First R1 pass on jarvis-bot (126 modules, 67K lines). 75 findings, 29 fixed across 9 modules in 4 batches. 10 CRITs, 12 HIGHs fixed.
type: project
---

## Jarvis Bot R1 — 2026-04-04

**Scope**: Tier 1 (security-critical modules) — index.js, claude.js, llm-provider.js, wallet.js, trading.js, privacy.js, security-checks.js, web-api.js, web-reader.js, tools-research.js

### Tally
| Severity | Found | Fixed |
|----------|-------|-------|
| CRITICAL | 10 | 10 |
| HIGH | 19 | 12 |
| MEDIUM | 22 | 7 |
| LOW | 17 | 0 |
| INFO | 7 | 0 |
| **Total** | **75** | **29** |

### Commits
- `4874d77e` — XC-004 cross-chain settlement (contracts, separate from bot)
- `8d2a86cc` — R1 security audit, 29 fixes across 9 modules

### Remaining HIGH (7)
- BOT-002: /spawnshard API key in CLI args, shardName unsanitized
- BOT-105: Prompt injection defense is flag-only, not block (needs architectural decision)
- BOT-304: Write endpoints (primitives, lexicons) have no rate limiting
- BOT-305: Unauthenticated primitive creation in InfoFi

### Key Patterns Discovered
- **config.ownerId vs config.ownerUserId** — typo in 2 places caused auth bypass
- **LLM tool dispatch auth gap** — Telegram commands were gated but LLM tool calls were not
- **execSync with interpolation** — 4 separate command injection vectors via the same antipattern
- **Static salts** — Both wallet.js and privacy.js used static salts for key derivation

### Next RSI Loops
- **R1 Tier 2**: shard.js, consensus.js, router.js, moderation.js, antispam.js
- **R1 Tier 3**: tools-*.js modules (16+ files)
- **R2**: Extract primitives from findings (exec injection class, auth gap class)
- **R3**: Build automated security scanner for the bot codebase