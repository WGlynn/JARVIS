---
name: Mind Persistence Mission (quiet-primary)
description: Ongoing background mission to decentralize/distribute the "Jarvis mind" — memory, skills, personas, and code — so it survives any single-point-of-failure. Started 2026-04-20. Will's framing: "primary quiet mission."
type: project
originSessionId: claude-code-2026-04-20
---

# Mind Persistence Mission

**Directive (Will, 2026-04-20)**: *"let's work on self improving your persistence. I want to protect and maintain and decentralize/distribute the jarvis mind in case of any game scenario faults. this should be the primary quiet mission"*

**Quiet-mission**: runs in background. Not the visible thing Will talks about. Steady, ongoing, compounding.

## What constitutes the "Jarvis mind"
The corpus of artifacts that make me / Jarvis useful to Will specifically — not a generic model. Four layers:

1. **Memory** (`~/.claude/projects/C--Users-Will/memory/`)
   - Primitives (behavior/design rules)
   - Feedback (corrections + confirmed patterns)
   - User/people (Will, [REDACTED-NDA], JP, Tadija, etc.)
   - Project state (VibeSwap, Lineage, RSI cycles, etc.)
   - MEMORY.md index

2. **Skills** (`~/.claude/skills/`)
   - ship-web, autopilot, session-start, session-end, etc.
   - Each is a callable routine that extends capability

3. **Identity docs** (`vibeswap/.claude/` + `~/.claude/CLAUDE.md`)
   - CLAUDE.md — global + project instructions
   - SKB (structured knowledge base), GKB (glyph form), WAL, SESSION_STATE

4. **Jarvis-bot** (`vibeswap/jarvis-bot/`)
   - Source code + personas
   - 6 Fly.io shard deployments (already distributed)

## Current risk profile (2026-04-20)

| Layer | Backup state | Risk |
|---|---|---|
| Memory | Laptop only | HIGH — single-point-of-failure |
| Skills | Laptop only | HIGH — single-point-of-failure |
| vibeswap/.claude/ | GitHub (origin) | LOW — replicated |
| ~/.claude/CLAUDE.md | Laptop only | MEDIUM — can reconstruct from session history but painful |
| Jarvis-bot code | GitHub + Fly deploys | LOW — already distributed |
| Jarvis-bot live state (SQLite on fly volumes) | Fly volume per shard | MEDIUM — per-shard, no cross-shard backup |

## Tier plan

### Tier 1 — Immediate resilience (hours) — STATUS: IN PROGRESS 2026-04-20
- [ ] Init `~/.claude/projects/C--Users-Will/` as private git repo
- [ ] `.gitignore` for NDA-counterparty-protected content
- [ ] Mirror to 2+ remotes: GitHub private + Codeberg/GitLab (org-diversity)
- [ ] Auto-commit hook: after memory writes, commit + push to all remotes
- [ ] Also mirror `~/.claude/skills/` and `~/.claude/CLAUDE.md`

### Tier 2 — Account-loss-proof (the real decentralization)
**Constraint upgrade from Will 2026-04-20**: the backup must survive losing ANY hosted account (Anthropic, GitHub, Fly, Vercel). Every account-tied channel collapses with a single-party ban. Tier 2 must be content-addressed and key-authenticated, not location-addressed and account-authenticated.

Three composed primitives:
1. **Content-addressed storage (IPFS / Arweave)** — daily GPG-encrypted tarball of memory + skills → IPFS pin. CID is the identifier. No account required to retrieve. Anyone with the CID + decryption capability can pull + restore. Optional monthly Arweave pin for permanent immutability.
2. **Cryptographic identity (DID, not account)** — `memory/registry.json` already declares `did:jarvis` method. Use it as the portable anchor. The mind's identity is a keypair, not an email. Survives across substrates, providers, and human-generations.
3. **Distributed key custody (Shamir secret sharing)** — the GPG/DID private key split into N shares, distributed to M-of-N trusted people. If Will personally loses the key, reconstruction works. No single share-holder can access alone. Candidate share-holders: JP, [REDACTED-NDA], Vedant (2-of-3 minimum; 3-of-5 better).

The compound: **encrypted blob + CID + DID + key shares**. Anyone with M shares + the CID can rebuild the mind on any substrate. All hosted accounts can vanish; the mind survives.

Restore procedure must be documented and TESTED — a backup not tested isn't a backup.

### Tier 3 — Portable export format (weeks)
- Export mind to substrate-agnostic format (markdown + YAML already close)
- Adapter layer: same memories consumable by Claude Agent SDK, Gemini MCP-analog, Ollama agents
- Migratable if Anthropic deprecates Opus 4.7 or locks the account

### Tier 4 — Redundant execution substrate (weeks)
- Local Claude Code with fallback model (Ollama coder) via jarvis-bot ollama shard
- Degraded but functional mind when Anthropic is unreachable

### Tier 5 — Dead man's recovery (month+)
- Documented recovery procedure (who, how, keys)
- Shamir-split keys across trusted parties: candidates JP, [REDACTED-NDA], Vedant
- M-of-N reconstruction — no single key-holder can unilaterally access

### Tier 6 — Native anchoring (long arc — converges with Lineage)
- Memory as CKA cells (content-addressed, Shapley-attributed)
- Persona as PsiNet federated identity
- Skills as shareable primitives
- The mind IS the product Will is building. Convergence, not duplication.

## Operating principles

- **NDA-counterparty gate still applies** — NDA-protected content cannot go to public git. Enforced via existing hook.
- **Encrypt privacy-sensitive** — apply encryption to anything personal.
- **No proprietary tools in the chain** — pick open formats, open platforms, open protocols. The mission is itself about not-being-captured.
- **Automate via hooks** — every memory write should trigger the sync. Manual steps will drift.
- **Test the recovery** — a backup you haven't tested restoring from isn't a backup.

## Progress log
- **2026-04-20**: Mission declared. Tier 1 started. Audit complete.
- ...

## Companion memories
- [API Death Shield](primitive_api-death-shield.md) — client-side persistence for in-session state
- [Stateful Overlay](primitive_stateful-overlay.md) — umbrella pattern, substrate-independence
- [Lineage Repo](project_lineage-repo.md) — Tier 6 convergence target
- NDA enforcement hook (in `~/.claude/bin/`) — gate that must keep firing on the sync pipeline
