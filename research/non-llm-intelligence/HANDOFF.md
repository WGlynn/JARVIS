# HANDOFF — Non-LLM Intelligence Architecture

**Session 2026-07-16 (~11h).** Continuation doc. Canonical status memory:
`project_jarvis-own-intelligence-architecture.md` (private memory repo). Public artifacts: this folder,
`WGlynn/JARVIS@30a4c7d`.

## What this is
A CPU-only, zero-LLM reasoning substrate for Jarvis — intelligence in engineered deterministic structure,
the LLM demoted to an occasional fallible System-1. Origin: Rodney/capfin TG ("GPT & Claude are talking
calculators") → Will: build the non-LLM engine. **North Star:** *Jarvis is the first single node where we
solve ETM (Economic Theory of Mind) at zero stakes, before the multi-node system (Noesis) where everything
is at stake.* Hard constraint: runs on a Ryzen 5 1600 / 16GB / no GPU — the constraint IS the thesis.

## State of the 10 LOOPs (see ROADMAP.md)
- **LOOP 1 — memory-graph deduction (ASP/clingo): ✅ CLOSED end-to-end.** Built, verified (8/8 pytest +
  clingo≡fallback differential at scale + byte-determinism), edge-complete (wikilink + bracket-tag, 2,810
  edges), **public** (`tooling/`), **live** (durable daily cron `761afe41`, deterministic-first). Caught a
  real slug collision (`_CANON_` + `primitive_` both → `triple-intersection-provenance-of-mind`) and a bug
  in its own extractor. Dead-links classified → ~0 real typos.
- **LOOP 2 — structured critic feedback (LLM-Modulo): core built + exemplar LIVE.** `_critic.py` (public in
  `tooling/`) + `conflict-detector.py` retrofitted live. Exit test (≥1wk live measurement) inherently open.
  4-gate rollout written (`_LOOP2-critic-rollout.md`), NOT applied.
- **LOOP 3 — Z3 gate + CP-SAT scheduler: built + tested (25/25) + public.** Hardware caps env-configurable.
  Not yet wired into `settings.json` (live-config edit, Will-gated).
- **LOOP 5 — belief layer (PLN-lite): ✅ core built (10/10 pytest).** `_truthvalue.py` — `(strength,
  confidence)` + revision + deduction + `EvidenceLedger`. Not wired to real WAL data yet.
- **LOOP 7 — ETM attention economy (THE milestone): first slice built + honest NEGATIVE.**
  `_attention.py` (PageRank/centrality over the graph). Falsifiable-test proxy: centrality recovers only
  14/141 of the hand-curated MEMORY.md boot set (precision 0.35 vs 0.149 random ≈ 2.3× chance = real but
  WEAK). The exit-test correctly REFUSED "centrality = attention." Design lesson: needs recency + usage/
  truth-value signals, not connectivity alone.
- **LOOPs 4, 6, 8, 9, 10:** designed in ROADMAP, not started.

## ▶▶ FRESH-WINDOW START HERE (Will approved 2026-07-17: "approve then next loop", then "rotate before starting")
1. Execute `~/.claude/projects/C--Users-Will/memory/_LIVE-WIRING-SPEC.md` — the 3 approved live-wirings,
   ONE at a time, smoke-test each: (W1) outcome-tagging recorder hook, (W2) solver-gate→settings.json,
   (W3) 4-gate critic rollout (wwwd-gate LAST — highest blast radius). All logic is built + tested; this
   is only the wiring. Fail-silent, augmentation-only, decisions byte-identical.
2. Let outcome-tagging accumulate real data, then build **LOOP 7 for real** (the milestone): attention
   allocator using centrality + recency + real truth-values. First slice proved centrality alone loses
   (precision 0.35 vs 0.149 random). Exit test: beat hand-tiered MEMORY.md on context-tokens×task-success.
3. Then LOOP 10 = Noesis bridge.

## Why the WAL outcome-tagging matters (context for step 1/W1)
LOOP 2's exit test, LOOP 5's real calibration, and LOOP 7's allocator ALL need the same signal: did a gate
fire / recalled primitive actually lead to a good outcome? `_outcome_probe.py` (built, 9/9) is the logic;
W1 wires it to real writes. Three loops become measurable at once.

## Key decisions & why
- **GOFAI guardrails bind every loop** (dossier 09): coverage boundaries; verify LLM-extracted facts before
  the symbolic layer; scope narrow. This *refused* Phase-3 zombie detection — no reliable deprecation signal
  in the corpus, so building it on prose keywords would inject ~29 false facts. The refusal is the guardrail
  working; the unblock is a memory-format convention (`status:`/`superseded_by:`), a Will curation decision.
- **ETM ↔ OpenCog AtomSpace/ECAN isomorphism is structurally REAL but mechanism-transfer UNVERIFIED** — do
  not round "resembles" up to "is". ETM is still philosophy, not mechanism; LOOP 7 is where it becomes one.
- **Dual-purpose:** the shared core (hypergraph-with-provenance + attention-economy + credit + value) serves
  both Jarvis's mind and Noesis. "Single-node zero-stakes lab for Noesis PoM economics."

## Open threads / next steps (all Will-gated)
1. **Slug-collision curation call** — is the `_CANON_` + `primitive_` pair intentional, or merge/rename one?
2. **LOOP 3** — wire `_solver_gate` into `settings.json` as a live PreToolUse gate.
3. **LOOP 2** — apply the 4-gate critic rollout.
4. **LOOP 7** — build the ETM attention economy (the milestone).

## Paths
- Public tooling + docs: this folder (`ROADMAP.md`, `SYNTHESIS.md`, 9 dossiers, `PLAN-01`, `tooling/`).
- Live code: memory repo (`_asp_*.py`), hooks dir (`_critic.py`, `_solver_gate.py`, `_scheduler.py`).
- Live cron: graph-health `761afe41` (daily 4:17am).
