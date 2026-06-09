# jarvis-os (public substrate)

This is a public slice of the JARVIS agent stack referenced in [pewdiepie-archdaemon/odysseus#NNNN](https://github.com/pewdiepie-archdaemon/odysseus/discussions) (the announcement Discussion that points here).

JARVIS is a personal coding-agent built on top of Claude. It has been running against the author's own workflow for about a year. This repo is the substrate the agent uses, not the agent itself: cron prompts, memory primitives, hooks, the advice-mining queues.

Everything in here is what gets read at boot or fires on tool events. Personal entries (engagement notes, partner-specific receipts, private channel content) stay local.

## What is in here

### `cron-prompts/`
The canonical bodies for the cron-driven Odysseus loops.

- `odysseus-discovery.md` — discovery loop canonical. C1 self-perpetuation, C2 dispatch, C2.5 advice mining (the part this announcement is about), C3 primitives extraction.
- `odysseus-daily-cadence.md` — daily-cadence loop canonical. Same 1/2/2.5/3 structure, different cap rules.
- `_advice-actionable-vibeswap.md` — advice surfaced by C2.5 that applies to the VibeSwap codebase (React+Vite+Tailwind frontend, Solidity contracts, Python oracle).
- `_advice-actionable-jarvis.md` — advice surfaced by C2.5 that applies to JARVIS itself (this repo).
- `_advice-mined-log.md` — rolling log of generic-good-design advice that did not directly map to either substrate.
- `_primitives-pending.md` — candidates for promotion to memory primitives, awaiting triage.

### `memory/`
The discrete memory primitives bundled here are the ones load-bearing for the public posture and the Odysseus mission loop.

- `feedback_odysseus-as-advisory-substrate.md` — the rule that frames Odysseus threads as a public audit of our shared AI-cosplay substrate.
- `feedback_odysseus-daily-discussion-campaign.md` — campaign rules for the daily-cadence loop.
- `feedback_code-comment-why-only.md` — origin: a style nit @vdmkenny left after merging PR #3363 in the Odysseus repo. Folded into the substrate the same week.
- `feedback_spec-vs-deployed-severity-calibration.md` — separates "spec-only" from "deployed" when classifying a finding's severity. Cross-cuts a lot of partner-review work.
- `primitive_time-logic-anti-hallucination-gate.md` — verify-then-assert for any temporal claim. Sibling of an entity-cross-reference primitive not bundled here.
- `primitive_authorship-via-conditions-and-context.md` — when conditions and context are authored by a human and execution is by an agent, attribution flows back through the conditions.
- `project_odysseus-mission-loop.md` — the 5-step mission loop. Inbound advice-mining, outbound public substrate, embedded principles, contribution-graph attribution, guided entry over time.

### `hooks/`
Selected hooks. They run from a Claude Code (Anthropic CLI) configuration that fires on tool-use events.

- `em-dash-augmentation-gate.py` — scans partner-facing drafts for em-dashes and surfaces a scrub-warning. Generic partner patterns shipped; fork users plug in their own handles.
- `hiero-gate.py` — enforces operator-dense, short-line format for memory primitives. Blocks writes that read as prose.
- `atomic-reflection-gate.py` — fires on tool errors and timeouts; surfaces a pause-and-extract reminder so the agent does not paper over root causes.
- `memory-preprocessor.py` — at SessionStart, expands a hierarchical memory index by loading sub-indexes relevant to the active task. Keeps the always-loaded core small while making situation-matched memory available.

### `scripts/`
- `odysseus_discovery.py` — scores recent Odysseus repo activity for mechanism-design / coordination / governance fit. Cron-fired Claude session reads the JSON, picks the top candidate above threshold, runs a convergence-proof gate, drafts and dispatches.

## How the pieces compose

Each memory primitive ends with a `composes-with` section that names parent and sibling primitives. Each hook references the primitives it enforces. Each cron-prompt references both. The dependency graph is mechanical to derive once an extractor is wired up; that is v2 of this repo.

## Lineage

This is downstream of work in two other repos:

- [WGlynn/VibeSwap](https://github.com/wglynn/vibeswap) — the omnichain DEX and mechanism-design substrate. Specifically: `contracts/incentives/FractalShapley.sol`, `contracts/incentives/MicroGameFactory.sol`, `cogproof/src/shapley-dag/shapley.js`, `docs/architecture/patterns-existing/fractalized-shapley-attribution.md`. The contribution-graph shape used by JARVIS for advice-attribution is the same shape proven on the VibeSwap side.
- [Usd8-fi/Usd8-fi-usd8-cover-score](https://github.com/Usd8-fi/Usd8-fi-usd8-cover-score) — USD8's cover-score algorithm, where I contributed the Shapley-value mathematical foundation (PRs #2, #3, #4, spring 2026).

## License

MIT.
