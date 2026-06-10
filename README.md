# JARVIS

> *Just A Rather Very Intelligent System.*

JARVIS is the agent overlay architecture I run on top of Claude. This repo is the monorepo description of that overlay — a tour of the eight layers, each with concrete artifacts, each cross-linked to where the source-of-truth code lives.

The code is not duplicated here. The code lives in [`vibeswap`](https://github.com/wglynn/vibeswap), in `~/.claude/`, and in the supporting repos linked from each layer. **This repo is the map.** The architecture is the territory.

## The accusation

> *"You forward user input to an LLM, you forward the LLM's response back, and the middle isn't load-bearing. The value is the LLM's, redistributed at a markup."*

The simplest test: would removing the LLM kill the system, or replace one substrate? JARVIS passes that test. Most "AI agents" do not.

The full essay: [`papers/jarvis-is-not-a-wrapper.md`](./papers/jarvis-is-not-a-wrapper.md).

## The eight layers (architecture description)

| # | Layer | What it does |
|---|---|---|
| 1 | [Hooks](./01-hooks/) | Deterministic gates on every tool call, session boot, and commit |
| 2 | [Persistence](./02-persistence/) | Six tiers of state that survive session boundaries |
| 3 | [Anti-hallucination](./03-anti-hallucination/) | Substance gate, HIERO format, time-logic gate, claim-level discipline |
| 4 | [Discipline](./04-discipline/) | Pattern capture into reusable primitives — 216 primitives + 194 feedback rules + 59 projects + 17 references in the live corpus (see [`substrate/memory/`](./substrate/memory/) for the public slice) |
| 5 | [Meta-protocols](./05-meta-protocols/) | How design decisions get made: AMD, AGov, Substrate-Geometry Match, Universal-Coverage → Hook, ETM |
| 6 | [Agent overlay](./06-agent-overlay/) | Subagent spawning, slash commands as skills, MCP connectors, remote scheduled triggers |
| 7 | [Stateful applications](./07-stateful-applications/) | The Telegram bot suite, standalone signature validator, jarvis-network OSS, filesystem-native CRMs, 120+ published papers (see [`papers/`](./papers/)) |
| 8 | [Filesystem-as-substrate](./08-filesystem-as-substrate/) | Why markdown + git is the orchestration layer, not Notion + Salesforce |

## Modules (runnable / installable artifacts)

The eight layers above describe the architecture. The modules below are concrete: each subdirectory is self-contained, has its own README, and can be used independently of the others.

| Module | What it is |
|---|---|
| [`substrate/`](./substrate/) | The live primitive corpus + cron canonicals + hooks + Python wrapper. `pip install -e ./substrate` makes the corpus importable as typed objects with a derivable dependency graph. Formerly hosted at `WGlynn/jarvis-substrate`. |
| [`installer/`](./installer/) | Kernel install scripts. Adopts the JARVIS hook + memory + cron-prompt layout into a fresh `~/.claude/` setup. Formerly hosted at `WGlynn/jarvis-os`. |
| [`papers/`](./papers/) | Essays that specify or justify pieces of the architecture. Mostly Medium-grade write-ups; some have PDF companions. |
| [`verify/`](./verify/) | Reader-runnable checks against the live system. Five verification scripts that test the architecture claims hold. |

## How to read this repo

- **If you want the argument**: read [`papers/jarvis-is-not-a-wrapper.md`](./papers/jarvis-is-not-a-wrapper.md).
- **If you want the architecture**: walk the eight layers in order.
- **If you want to verify**: [`verify/`](./verify/) has five reader-runnable checks against the live system.
- **If you want the kernel framing**: JARVIS is to LLM substrates what an OS is to hardware substrates. The CPU is interchangeable. The kernel is not. The applications run on the kernel.

## What *is* and *isn't* in this repo

**In this repo (as of 2026-06-09 merge):**
- `substrate/` — the live hook + memory + cron-prompt + Python-wrapper substrate, importable as a Python package. Formerly hosted at `WGlynn/jarvis-substrate`.
- `installer/` — kernel install scripts. Formerly hosted at `WGlynn/jarvis-os`.
- `papers/` — 125 markdown papers (59 with PDF companions), including all the augmented-X series, the Shapley + fairness math papers, the VibeSwap mechanism-design specs that were here previously, and the canonical-thinking corpus that used to live only in `vibeswap/docs/research/papers/`.
- `01-08 layer dirs/` — the architecture-description essays per layer.
- `verify/` — reader-runnable verification scripts.

**Not in this repo (and why):**
- **VibeSwap product code** — the Solidity contracts, the React frontend, the Python oracle. Those live in [`vibeswap`](https://github.com/wglynn/vibeswap) because they are a separate product, not a JARVIS substrate concern. JARVIS runs against many substrates; VibeSwap is one of them.
- **The full personal memory store** — the local `~/.claude/projects/.../memory/` has 524 primitive / feedback / project / reference files; 412 are mirrored here via `substrate/memory/` after scrub-list filtering for partner-engagement content, NDA-locked material, personal addresses, and API keys. The 112 filtered files stay local by design.
- **Hooks with hardcoded personal content** — e.g. partner-name regex lists, personal email in docstrings. Sanitized variants are shipped; the originals stay local.
- **Secrets** — no tokens, no keys, no fly.io app names that aren't already public.

## License

MIT. See [`LICENSE`](./LICENSE).
