# ROADMAP — Jarvis's Intelligence Architecture (the LOOPs)

> **The North Star (Will, 2026-07-16):** *"Jarvis is the first single node where we solve ETM where there
> is no stakes, before we launch the multi-node system where everything is at stake."*

Jarvis is the **zero-stakes laboratory** for the economics that Noesis runs at full stakes. We turn ETM
from a philosophy into a working **mechanism** on one node, prove it against a falsifiable test, and only
then hand the proven mechanism to the staked multi-node chain. Every LOOP below is a piece of that.

This roadmap is the execution contract. It supersedes prose plans; each LOOP has a binary done-condition.

---

## Global rules (bind EVERY loop)

1. **Loop invariant (Will):** every increment must be (a) **internalized** — wired into Jarvis's live
   substrate so it changes how the agent operates, not shelfware; (b) written **generic** (parameterized
   root, no hard-coded personal paths in the copyable core); (c) **committed to the public JARVIS repo** so
   others can freely copy it. Build in the open.
2. **GOFAI guardrails (dossier 09), non-negotiable:** explicit machine-readable coverage boundary per
   module (out-of-scope → graceful refusal); **verify every LLM-extracted fact before it enters the
   symbolic layer** (provenance on every assertion); scope narrow — ten deep verified modules over one
   broad shallow one (a growing scope declaration is a CYC warning light).
3. **Laptop test:** runs on Ryzen 5 1600 / 16GB / no GPU. GPU/cluster-bound → out.
4. **Loop discipline (six-commandment):** self-perpetuate first, drive a state machine, per-increment
   commit + push + doc-stamp, silence beats a bad artifact.
5. **Honest labels:** ✅ built · 🟡 designed · 🔬 open. Never round up. `[[no-false-pattern-matching]]`.

---

## Dependency map

```
LOOP 1 (graph) ──┬─→ LOOP 4 (assoc. recall) ──┐
                 ├─→ LOOP 6 (typed KR) ────────┤
LOOP 2 (critic) ─┤                             ├─→ LOOP 7 ★ (ETM attention economy) ─→ LOOP 10 (Noesis bridge)
LOOP 3 (solvers)─┘   LOOP 5 (truth-values) ────┘        │
                     LOOP 8 (WWWD arbitration) ─────────┤
                     LOOP 9 (self-improve / GP) ────────┘
```

Parallelizable now: **1, 2, 3** (independent, cheap, cross-cutting). LOOP 7 is the crux and the milestone;
everything upstream exists to make its mechanism possible and its exit test measurable.

---

## LOOP 1 — Memory-graph deduction (L1 graph integrity) · **ACTIVE**
- **Goal:** the memory graph deduces over itself on CPU, zero LLM calls. `PLAN-01-asp-memory-graph.md`.
- **Deliverables:** `_asp_extract.py` ✅ · `_asp_rules.lp` ✅ · `_asp_query.py` ✅ (Phase-1 core, verified:
  945 nodes / 1,642 edges, deterministic, <0.5s) → Phase 2 (bracket-tags, `name:`-aliasing to fix the ~40%
  non-resolving links, hierarchy, `_link_enforcer` parity, fixpoint oracle + pytest) → Phase 3
  (conflict-candidates, zombies, load-bearing cones, **conflict-detector hook consult** = the internalize).
- **Exit test:** `pytest` green incl. clingo-vs-fallback differential; parity vs `_link_enforcer` (ASP
  strictly ⊇, disagreements explained); conflict-detector consults the graph on live Writes; report
  regenerates in autopilot; pushed to public repo.
- **Status:** 🟡 Phase-1 core verified; Phases 2–3 open.

## LOOP 2 — Structured critic feedback (System-2 verification wiring)
- **Goal:** hooks stop returning flat errors and return `{violated_constraint, suggested_reformulation}`
  (LLM-Modulo, dossier 02). Zero added inference. Cheapest high-ROI upgrade.
- **Deliverables:** a shared `critic_output` schema; retrofit the top ~5 highest-firing PreToolUse gates.
- **Exit test:** ≥5 gates emit structured critic output; a measured before/after on correction-rate or
  reformulation-accept-rate over ≥1 week of live fires (honest number, not estimate).
- **Status:** 🔬 open. Can start now.

## LOOP 3 — Local solver gates (Z3 + OR-Tools)
- **Goal:** move gate logic from heuristic → sound. Z3 for constraint-checkable PreToolUse rules; OR-Tools
  CP-SAT for the concurrency/OOM scheduler (dossiers 02, 03).
- **Deliverables:** `_solver_gate.py` (Z3-backed check for ≥1 real invariant); `_scheduler.py` (CP-SAT
  bin-packing the "max N concurrent forge/agent" limit, replacing the hope-it-doesn't-OOM heuristic).
- **Exit test:** one invariant proven sound/complete via Z3 with a passing adversarial fixture; scheduler
  produces an optimal assignment matching or beating the hand rule on a replay of real session load.
- **Status:** 🔬 open. Can start now.

## LOOP 4 — Associative recall (L1 memory retrieval)
- **Goal:** content-addressable recall that does pattern-completion (partial/noisy cue → right primitive),
  which cosine search can't. Modern Hopfield (~35-LOC NumPy, ~30MB) + VSA/Torchhd for compositional
  wikilink queries (dossiers 04, 08).
- **Deliverables:** `_hopfield_recall.py` drop-in beside the current embedding recall; VSA encoder for the
  wikilink graph.
- **Exit test:** on a held-out set of "cue → correct primitive" pairs, Hopfield recall ≥ current cosine
  recall on top-k accuracy AND succeeds on ≥1 partial-cue case cosine fails. If it doesn't beat the
  baseline, it doesn't ship (keep cosine).
- **Status:** 🔬 open. Depends on LOOP 1 (graph as substrate).

## LOOP 5 — Belief layer / truth-values (L3)
- **Goal:** explicit uncertainty as `(strength, confidence)` (PLN-lite / NARS, dossiers 01, 04). Gates and
  primitives accumulate self-calibrating truth-values from WAL outcomes; routine applicability-scoring
  moves off the LLM, LLM reserved for genuine novelty.
- **Deliverables:** `_truthvalue.py` (revision math); a per-gate reliability ledger fed by WAL fire/outcome.
- **Exit test:** gate `(f,c)` values converge from real fire history; a routine scoring decision that
  currently calls the LLM is served by the truth-value layer with equal-or-better accuracy on a labeled
  sample.
- **Status:** 🔬 open. Depends on WAL outcome data; feeds LOOP 7.

## LOOP 6 — Typed knowledge + sound inference (L1 KR)
- **Goal:** a 5–10 class OWL-EL type schema over primitives (Primitive/Gate/Pattern/Feedback/…); RDFS
  deductive closure + SPARQL consistency checks, pure Python (rdflib + owlrl, dossier 06).
- **Deliverables:** `_kr_schema.ttl` + `_kr_check.py` (e.g. "every Gate must have a registered hook").
- **Exit test:** ≥3 deterministic consistency checks that currently need an LLM read or manual audit run as
  SPARQL and catch ≥1 real inconsistency in the live corpus.
- **Status:** 🔬 open. Depends on LOOP 1 (nodes/types).

## LOOP 7 ★ — The Economic Attention Allocator (L2) — **THE SINGLE-NODE ETM SOLVE**
- **Goal:** turn ETM from philosophy into **mechanism**. An attention economy over the memory graph decides
  what loads into context: candidates are two-currency STI/LTI (ECAN-style), ACT-R activation, or
  market/Hayek pricing (dossiers 04, 05; skeleton L2). This is the milestone — the zero-stakes ETM solution.
- **Deliverables:** `_attention_economy.py` — an allocator that replaces the hand-tiered MEMORY.md boot
  budget with a computed one, using LOOP 1 graph structure + LOOP 5 truth-values + usage history as the
  "wealth/rent" signal.
- **Exit test (falsifiable, hard):** automated allocation **beats the hand-tiered MEMORY.md** on
  *context-tokens × task-success* over a real workload replay. If it can't beat Will's hand-tuning, it does
  **not** ship — no elegant-mechanism-that-loses-to-the-baseline.
- **Status:** 🔬 open. **Crux.** Depends on LOOPs 1, 5 (and benefits from 4, 6). This is the loop that
  earns the sentence "we solved ETM on one node."

## LOOP 8 — Decision arbitration (L5, WWWD formalized)
- **Goal:** WWWD becomes a generative model of Will that minimizes prediction error — active inference
  (pymdp) and/or a Hayek-machine market over subagents (dossier 05). Preferences = goal prior;
  predicted-Will vs actual-Will = the error that updates the model. Escalate-to-Will preserved.
- **Deliverables:** `_wwwd_infer.py` scoring decisions against the existing WWWD corpus + corrections.
- **Exit test:** on the held-out correction history, the formal model predicts Will's actual call ≥ the
  current heuristic gate, and its epistemic-uncertainty signal correctly flags the cases that need escalation.
- **Status:** 🔬 open. Depends on WWWD corpus (exists) + LOOP 5.

## LOOP 9 — Self-improvement mechanized (L7, TRP as evolution)
- **Goal:** TRP stops being manual. Genetic programming over the gate/primitive population (DEAP) + MAP-
  Elites (pyribs) to keep the harness diverse across failure niches, not monocultured on the last failure
  (dossier 07). Fitness = WAL catch-rate × token-delta.
- **Deliverables:** `_gate_evolve.py` (WAL→candidate→shadow-mode→confidence-gated promotion) + a niche
  archive keyed on (error-category, session-phase).
- **Exit test:** ≥1 auto-derived gate promoted through shadow mode that catches a real error class the
  hand-written gates missed, with a measured catch-rate — and the archive demonstrably holds ≥N distinct
  niches (no monoculture).
- **Status:** 🔬 open. Depends on WAL fitness signal + LOOP 1.

## LOOP 10 — The Noesis bridge (single-node → multi-node)
- **Goal:** extract the proven shared core (L1 hypergraph-with-provenance + L2 attention-economy + L5
  credit/value + L7 evolution) and validate that the ETM **mechanism** that beat MEMORY.md on one
  zero-stakes node is the same one securing Noesis PoM across staked nodes. `[[voluntary-noesis]]` cashed.
- **Deliverables:** a documented mechanism-isomorphism (no longer "resembles" — now a shared implementation
  or a proven-equivalent spec), and the port of the attention/credit primitives into Noesis's form.
- **Exit test:** the single-node ETM allocator's core rule is expressed in Noesis's PoM/attention terms and
  passes Noesis's own tests; the isomorphism is code-grounded, not asserted. **This is the launch gate for
  "everything is at stake."**
- **Status:** 🔬 open. Capstone. Depends on LOOP 7 succeeding.

---

## Execution order
1. **Now (parallel):** finish **LOOP 1** (Phases 2–3) · start **LOOP 2** and **LOOP 3** (independent, cheap).
2. **Next:** **LOOP 5** (truth-values) and **LOOP 6** (typed KR); **LOOP 4** (recall) as capacity allows.
3. **The milestone:** **LOOP 7** — the single-node ETM solve, gated by its falsifiable test.
4. **Then:** **LOOP 8, 9** harden the agent around the proven economy.
5. **Launch gate:** **LOOP 10** — bridge to Noesis, where the stakes turn on.

Each loop closes only when its exit test passes, it's wired live, and it's committed to the public repo.
