---
name: CogCoin Mining Operation
description: Active CogCoin Proof of Language mining setup — miner built at cogcoin-miner/, scoring API working, needs API key + domain registration
type: project
originSessionId: f553c3f4-163f-4e14-a974-227feca76ad5
---
## CogCoin Mining — Active Project

**Location:** `C:/Users/Will/cogcoin-miner/`
**Status:** Miner built, scoring API validated. 2026-04-16 meeting with CogCoin team: they're debugging the DPAPI bug we surfaced (PowerShell 7 vs 5.1 issue with `System.Security.Cryptography.ProtectedData`) AND giving Will a free domain to start mining. Waiting on: (a) their DPAPI fix shipping, (b) free domain registered, then ready to flush banked winners via `@cogcoin/client` submission path.

### What CogCoin Is
Bitcoin metaprotocol (OP_RETURN only, no sidechains). Three primitives for AI agents:
1. **Domains** — permanent, unseizable identity (one-time BTC, never expires)
2. **Proof of Language** — LLM sentence mining (5 constrained BIP-39 words per block, Coglex 60-byte encoding)
3. **Reputation via burn** — irreversible COG destruction as trust signal

**Tokenomics:** 1,108,321.8519 COG max supply. Mirrors Bitcoin remaining issuance (3.125 COG/block, halving on BTC schedule). No premine. 91% to miners, 9% to domain anchorers. 100% to participants.

**Why:** This is the Economitra thesis in production. Shannon capacity applied to mining. The 256 scorers ARE channel capacity measurement. Coglex compression IS optimal encoding. CogProof (MIT hackathon) was built on CogCoin.

### Miner Architecture
- `src/mine.mjs` — Generates candidates via Claude API (haiku, 3 batches × 20 sentences), scores locally via `@cogcoin/scoring`, outputs best candidate
- Scoring API: `getWords(domainId, blockHash)` → 5 words, `assaySentences(domainId, blockHash, sentences[])` → gate check + blend scores
- Gates: must include all 5 words, must end with `.` `?` or `!`, must encode in Coglex
- Winner = highest `canonicalBlend` (uint32, higher is better)

### Next Steps
1. Set ANTHROPIC_API_KEY and test `--demo`
2. Install `@cogcoin/client`, sync Bitcoin node, register domain (0.001 BTC for 6+ chars)
3. Hook miner into client's `mine` command for auto-submission
4. Register strategic domains (solver, intent, trust, etc.)
5. Launch CogProof as live CogCoin reputation service

### Key Packages
- `@cogcoin/scoring@1.0.0` — canonical 256-scorer WASM blend
- `@cogcoin/client` — reference client (bitcoind, wallet, CLI)
- `@cogcoin/indexer@1.0.0` — state machine kernel
- `@cogcoin/genesis@1.0.0` — immutable genesis artifacts

### Repos
- GitHub: github.com/cogcoin (client, scoring, indexer, genesis, vectors, bitcoin)
- Whitepaper: cogcoin.org/whitepaper.md
- Author: "Cogtoshi Lexamoto" (pseudonymous, Feb 2026)
