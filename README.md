# JARVIS

> *Just A Rather Very Intelligent System.*

An agent overlay architecture for Claude Code. Eight layers of hooks, persistence, anti-hallucination gates, and meta-protocols that survive session boundaries and compose into something more durable than a chat wrapper.

> **Full feature surface + the moat:** [`FEATURES.md`](./FEATURES.md) — the honest inventory. The running system has **64 enforcement scripts**, a **23,462-block session hash-chain**, and a **1,263-proposal self-improvement loop**. This README documents a fraction of it.

## Official links

- **JARVIS vs OpenClaw — an honest comparison:** https://vibeswap-app.vercel.app/jarvis-vs-openclaw.html — why JARVIS is a governance + persistence *layer*, not a harness; concedes every axis OpenClaw wins, and leads with the underrated artifact: a **23,462-block tamper-evident session hash-chain** (downloadable commitment).
- **JARVIS ∩ OpenClaw — Venn:** https://vibeswap-app.vercel.app/jarvis-openclaw-venn.html — where the two genuinely overlap, where they don't, and where the integration boundary forces a fork.

## Current design (2026-06)

Three things define the system as it runs today, on top of the eight-layer map below:

- **Session hash-chain — 23,462 blocks.** Every checkpoint is a block linked to its parent by hash (`{id, parent, timestamp, prompt, response, hash}`) — the agent's tamper-evident long-term memory of its own history. Blocks stay local (raw content); the **head hash is published** as a commitment, so the chain is verifiable without leaking a word.
- **Merkle self-attestation over 624 governed files.** A Merkle root over every hook, primitive, and session-chain script is committed at session boot; an unsanctioned change to a governed file flags drift on the next boot. "Provably just files" — inspectable by design, kernel rejected on purpose.
- **One persistence framework: local authority → public commitment → shard replication.** Substrate content syncs in full (scrubbed); chain content stays local with only its head committed; both are designed to become nodes in a future shard network.

On top of these sit the operator-cognition gates: **WWWD** (a Will-emulation gate on consequential actions), **AFK mode** (predicted-reply menus for single-keystroke steering), and **RSAW** (recursive self-audit).

## Quickstart

```bash
# 1. Clone
git clone https://github.com/wglynn/JARVIS.git && cd JARVIS

# 2. Install the substrate Python package (corpus + graph + CLI)
pip install -e ./substrate

# 3. Smoke-test: parse the primitive corpus and print a summary
python -m jarvis verify

# 4. Look around
python -m jarvis list --type primitive | head -20
python -m jarvis show what-would-will-do        # one primitive
python -m jarvis graph --root jarvis-os         # dep graph from a root
python -m jarvis hindsight                       # find contradicting primitives
```

If `verify` prints `0 errors` you're set. The CLI reads the markdown corpus at `substrate/memory/` as typed objects with a derivable dependency graph — no database, no daemon, just files.

## What you get

| Artifact | Where | What it does |
|---|---|---|
| **62 hook + session-chain scripts** | `substrate/hooks/` | Drop-in `PreToolUse` / `SessionStart` / `Stop` gates (42 hooks) plus the session-chain persistence scripts. Each is a self-contained Python script that reads a JSON payload from stdin and emits an `additionalContext` block. Wire into `~/.claude/settings.json`. |
| **500 markdown files** | `substrate/memory/` | The discipline corpus: 213 primitives + 185 feedback rules + 57 projects + 17 references (+ indexes). Each file is one pattern. Importable as Python objects; greppable as files. |
| **12 cron canonicals** | `substrate/cron-prompts/` | Slash-command prompts scheduled via Claude Code's scheduling layer. Examples: substrate sync (+ chain commitment), advice mining, skill mining, link-rot detection. |
| **`jarvis` Python package** | `substrate/jarvis/` | CLI + library for `show / list / graph / verify / search / count / hindsight` over the corpus. |
| **Installer** | `installer/` | `absorb.sh` reads other Claude substrates and migrates patterns into your `~/.claude/` with namespace-collision handling. `install.sh` for fresh installs. |
| **Verification guides + scripts** | `verify/` | Five prose-based check guides + 2 fresh-clone-runnable Python scripts (`verify_primitive_corpus.py`, `verify_no_secrets.py`). Falsifiable, no trust required. |

## The eight layers (architecture map)

> Canonical layer description lives in [`ARCHITECTURE.md`](./ARCHITECTURE.md). The summary below is a pointer; when the two drift, fix `ARCHITECTURE.md` first then re-sync this section. CI does not enforce sync between them — discipline does.

| # | Layer | What it does |
|---|---|---|
| 1 | [Hooks](./01-hooks/) | Deterministic gates on every tool call, session boot, and commit |
| 2 | [Persistence](./02-persistence/) | Six tiers of state that survive session boundaries |
| 3 | [Anti-hallucination](./03-anti-hallucination/) | Substance gate, HIERO format, time-logic gate, claim-level discipline |
| 4 | [Discipline](./04-discipline/) | Pattern capture into reusable primitives — 213 primitives + 185 feedback rules + 57 projects + 17 references in the public slice (561 files in the full local corpus; see [`substrate/memory/`](./substrate/memory/)) |
| 5 | [Meta-protocols](./05-meta-protocols/) | How design decisions get made: AMD, AGov, Substrate-Geometry Match, Universal-Coverage → Hook, ETM |
| 6 | [Agent overlay](./06-agent-overlay/) | Subagent spawning, slash commands as skills, MCP connectors, remote scheduled triggers |
| 7 | [Stateful applications](./07-stateful-applications/) | Telegram bot suite, standalone signature validator, jarvis-network OSS, filesystem-native CRMs, 120+ published papers (see [`papers/`](./papers/)) |
| 8 | [Filesystem-as-substrate](./08-filesystem-as-substrate/) | Why markdown + git is the orchestration layer, not Notion + Salesforce |

Each layer directory has its own README with the concrete artifacts that implement it.

## Modules (runnable / installable)

The eight layers above describe the architecture. The modules below are concrete: each subdirectory is self-contained, has its own README, and can be used independently.

| Module | What it is |
|---|---|
| [`substrate/`](./substrate/) | The live primitive corpus + cron canonicals + hooks + Python wrapper. `pip install -e ./substrate`. Formerly hosted at `WGlynn/jarvis-substrate`. |
| [`installer/`](./installer/) | Kernel install scripts. Adopts the JARVIS hook + memory + cron-prompt layout into a fresh `~/.claude/` setup. Formerly hosted at `WGlynn/jarvis-os`. |
| [`papers/`](./papers/) | Essays that specify or justify pieces of the architecture. Mostly Medium-grade write-ups; some have PDF companions. Skip on first read; come back if a layer essay points you here. |
| [`verify/`](./verify/) | Reader-runnable checks against the live system. Five verification scripts that test the architecture claims hold. |

## What *is* and *isn't* in this repo

**In this repo (as of 2026-06-11):**
- `substrate/` — the live hook + memory + cron-prompt + Python-wrapper substrate, importable as a Python package. Formerly hosted at `WGlynn/jarvis-substrate`.
- `installer/` — kernel install scripts. Formerly hosted at `WGlynn/jarvis-os`.
- `papers/` — 126 markdown papers (with PDF companions for many), including all the augmented-X series, the Shapley + fairness math papers, the VibeSwap mechanism-design specs that were here previously, and the canonical-thinking corpus that used to live only in `vibeswap/docs/research/papers/`.
- `01-08 layer dirs/` — architecture-description essays per layer.
- `verify/` — reader-runnable verification scripts.

**Not in this repo (and why):**
- **VibeSwap product code** — the Solidity contracts, the React frontend, the Python oracle. Those live in [`vibeswap`](https://github.com/wglynn/vibeswap) because they are a separate product, not a JARVIS substrate concern. JARVIS runs against many substrates; VibeSwap is one of them.
- **The full personal memory store** — the local `~/.claude/projects/.../memory/` has 561 primitive / feedback / project / reference files; 500 are mirrored here via `substrate/memory/` after scrub-list filtering for partner-engagement content, NDA-locked material, personal addresses, and API keys. The ~61 filtered files stay local by design.
- **The session-chain blocks** — the 23,462-block hash-chain stays local (the blocks hold raw prompt/response content); only its head-hash commitment is published, at [`substrate/_chain/commitment.json`](./substrate/_chain/commitment.json).
- **Hooks with hardcoded personal content** — e.g. partner-name regex lists, personal email in docstrings. Sanitized variants are shipped; the originals stay local.
- **Secrets** — no tokens, no keys, no fly.io app names that aren't already public.

## Contributing

PRs welcome on hooks, primitives, verify scripts, and layer essays. See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for the contribution surface (it's narrower than "anything goes" but wider than "core only"). Issue templates are at [`.github/ISSUE_TEMPLATE/`](./.github/ISSUE_TEMPLATE/).

This is a personal substrate first — the author runs it as their daily Claude Code overlay. Don't expect a community framework; do expect a reference implementation you can crib from aggressively.

## Common objections

> *"You forward user input to an LLM, you forward the LLM's response back, and the middle isn't load-bearing. The value is the LLM's, redistributed at a markup."*

The simplest test: would removing the LLM kill the system, or replace one substrate? JARVIS passes that test — the hooks, persistence, and discipline layers are LLM-agnostic infrastructure, and the LLM is one swappable substrate among them.

The full essay is at [`papers/jarvis-is-not-a-wrapper.md`](./papers/jarvis-is-not-a-wrapper.md) if you want the long-form argument. Otherwise: run the quickstart and judge for yourself.

## License

MIT. See [`LICENSE`](./LICENSE).

## Story Mode

**Gamified vibe coding** — the original game-AI loop, on an LLM. Operate the agent by picking numbered branches like a pick-your-own-adventure, except the branches are generated live and the choices do real work. See [STORY-MODE.md](STORY-MODE.md). For the web app (no hooks), there's a hookless drop-in: [STORY-MODE-LITE.md](STORY-MODE-LITE.md). On ChatGPT: [STORY-MODE-CHATGPT.md](STORY-MODE-CHATGPT.md).
