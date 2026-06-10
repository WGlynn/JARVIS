# JARVIS

> *Just A Rather Very Intelligent System.*

An agent overlay architecture for Claude Code. Eight layers of hooks, persistence, anti-hallucination gates, and meta-protocols that survive session boundaries and compose into something more durable than a chat wrapper.

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
| **47 Claude Code hooks** | `substrate/hooks/` | Drop-in `PreToolUse` / `SessionStart` / `Stop` gates. Each is a self-contained Python script that reads a JSON payload from stdin and emits an `additionalContext` block. Wire into `~/.claude/settings.json`. |
| **468 markdown primitives** | `substrate/memory/` | The discipline corpus. Each file is a pattern, feedback rule, project, or reference. Importable as Python objects; greppable as files. |
| **8 cron canonicals** | `substrate/cron-prompts/` | Slash-command prompts scheduled via Claude Code's scheduling layer. Examples: substrate sync, advice mining, link-rot detection. |
| **`jarvis` Python package** | `substrate/jarvis/` | CLI + library for `show / list / graph / verify / search / count / hindsight` over the corpus. |
| **Installer** | `installer/` | `absorb.sh` reads other Claude substrates and migrates patterns into your `~/.claude/` with namespace-collision handling. `install.sh` for fresh installs. |
| **Verification guides + scripts** | `verify/` | Five prose-based check guides + 2 fresh-clone-runnable Python scripts (`verify_primitive_corpus.py`, `verify_no_secrets.py`). Falsifiable, no trust required. |

## The eight layers (architecture map)

| # | Layer | What it does |
|---|---|---|
| 1 | [Hooks](./01-hooks/) | Deterministic gates on every tool call, session boot, and commit |
| 2 | [Persistence](./02-persistence/) | Six tiers of state that survive session boundaries |
| 3 | [Anti-hallucination](./03-anti-hallucination/) | Substance gate, HIERO format, time-logic gate, claim-level discipline |
| 4 | [Discipline](./04-discipline/) | Pattern capture into reusable primitives — 216 primitives + 194 feedback rules + 59 projects + 17 references in the live corpus (see [`substrate/memory/`](./substrate/memory/) for the public slice) |
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

**In this repo (as of 2026-06-09 merge):**
- `substrate/` — the live hook + memory + cron-prompt + Python-wrapper substrate, importable as a Python package. Formerly hosted at `WGlynn/jarvis-substrate`.
- `installer/` — kernel install scripts. Formerly hosted at `WGlynn/jarvis-os`.
- `papers/` — 125 markdown papers (59 with PDF companions), including all the augmented-X series, the Shapley + fairness math papers, the VibeSwap mechanism-design specs that were here previously, and the canonical-thinking corpus that used to live only in `vibeswap/docs/research/papers/`.
- `01-08 layer dirs/` — architecture-description essays per layer.
- `verify/` — reader-runnable verification scripts.

**Not in this repo (and why):**
- **VibeSwap product code** — the Solidity contracts, the React frontend, the Python oracle. Those live in [`vibeswap`](https://github.com/wglynn/vibeswap) because they are a separate product, not a JARVIS substrate concern. JARVIS runs against many substrates; VibeSwap is one of them.
- **The full personal memory store** — the local `~/.claude/projects/.../memory/` has 524 primitive / feedback / project / reference files; 412 are mirrored here via `substrate/memory/` after scrub-list filtering for partner-engagement content, NDA-locked material, personal addresses, and API keys. The 112 filtered files stay local by design.
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
