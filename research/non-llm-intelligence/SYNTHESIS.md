# SYNTHESIS — Non-LLM Intelligence for Jarvis

**2026-07-16.** 9 research dossiers (01–09) + 2 Fable planners (ARCHITECTURE-SKELETON, PLAN-01) complete.
This closes the research phase and opens THE LOOP. Every claim here is laptop-tested (Ryzen 5 1600 / 16GB /
no GPU) and carries an honest maturity label. Source dossiers in this folder.

---

## 1. The convergence (the real headline)

Nine agents, different literatures, no contact — they converged on the **same first moves**. When
independent searches agree, the abstraction is real (Will's own `[[substrate-geometry-match]]`). The
agreed core:

1. **Make the memory-graph deduce over itself** — it already IS a knowledge graph (primitives = nodes,
   `[[wikilinks]]` = edges, frontmatter = typed properties). Pointed at by 03 (symbolic), 06 (KR), and
   both planners. Zero-dependency entry via **NetworkX** (PageRank = load-bearing primitives, Louvain =
   implicit domains, orphan/dead-link in ~20 LOC); sound-inference version via **clingo/ASP** (negation
   gives one-line `dead_link`/`orphan`, aggregates reserved for later).
2. **Structured critic feedback in the hooks** (LLM-Modulo, 02) — hooks return
   `{violated_constraint, suggested_reformulation}` instead of a flat error. A Python dict, **zero added
   inference**, published 82% success where baseline LLM planning fails.
3. **Local solvers as sound reasoners** — **Z3** (02, 03; `pip install z3-solver`, ~50MB, ms-solve) hardens
   gates; **OR-Tools CP-SAT** (03) turns the "max 3 concurrent forge / OOM" heuristic into an optimally
   solved bin-packing constraint.
4. **Explicit uncertainty as weighted truth-values** — NARS `(frequency, confidence)` (01) ≈ PLN-lite
   `strength+confidence` (04). Simple Python; replaces ad-hoc LLM judgment for routine scoring, escalates
   to the LLM only on genuine novelty.

**The frame the whole stack already fits: CLARION** (01) — Claude is the implicit bottom level, the
hook/gate system is the explicit top level, TRP is the bottom-up extraction between them. Jarvis was
already a cognitive architecture in shape; now it gets the mechanism.

---

## 2. Tiered build map (laptop-tested)

### TIER 1 — buildable this month (mature, CPU-local, convergent)
| Component | Engine | Dossier | LLM cost |
|---|---|---|---|
| Memory-graph deduction (reach/dead-link/orphan/conflict) | NetworkX → clingo | 03,06,PLAN-01 | **zero** |
| Structured critic feedback in hooks | Python dict (LLM-Modulo) | 02 | zero |
| Gate hardening (constraint checks) | Z3 | 02,03 | 1 translate/setup |
| Concurrency/OOM scheduler | OR-Tools CP-SAT | 03 | zero |
| Typed-primitive consistency (SPARQL checks) | rdflib + owlrl | 06 | zero |
| Truth-values on gate reliability | PLN-lite / NARS (f,c) | 01,04 | zero |

### TIER 2 — buildable, bigger, needs a design pass
- **VSA/Torchhd** associative recall (wikilinks computable, cosine query, no LLM call) — 04. ~1wk proto;
  unverified vs keyword on small graphs.
- **CLIPS/clipspy** RETE production-rule engine to replace ad-hoc Python hooks — 01,06.
- **ACT-R activation scoring** as ETM attention-allocator v0 — skeleton L2.
- **DoWhy** causal root-cause over WAL logs (intervention, not correlation) — 05.
- **DEAP (GP) + pyribs (MAP-Elites)** over the gate population — mechanizes TRP, fixes its monoculture
  (TRP converges on the last failure; MAP-Elites keeps a niche grid) — 07.

### TIER 3 — aspirational / research-grade / do NOT build on yet
- Full **NARS/ONA** cognitive core (01) — best philosophical fit, real integration cost.
- **Hayek-machine / Economy-of-Minds** market routing for subagents (05) — ETM operationalized; no public code.
- **pymdp active-inference** orchestrator formalizing WWWD (05) — the mapping is beautiful (Will's prefs =
  goal prior; predicted-Will vs actual-Will = prediction error), the build is a project.
- **OpenCog Hyperon AtomSpace+ECAN** (04) — bindings pre-alpha; the isomorphism VALIDATES the design, but
  don't build product on pre-alpha.

---

## 3. Hard guardrails (from 09, the skeptic seat) — bind EVERY increment

The honest verdict: the LLM+symbolic hybrid **relocates** the classic GOFAI failures, it does not dissolve
them. So these are constraints, not advice:

1. **Explicit coverage boundaries.** Every symbolic module declares machine-readable scope; out-of-scope →
   graceful refusal, never a confident wrong answer.
2. **Verify every LLM-extracted fact before it enters the symbolic layer.** The extraction pipeline is
   untrusted; provenance on every assertion. *A smaller verified KB beats a larger unverified one* — which
   is Noesis's Proof-of-Mind provenance thesis pointed inward.
3. **Constrain scope aggressively.** Ten narrow, deep, verified modules over one broad shallow one. Any
   growing scope declaration = a CYC warning light ($200M / 40yr says you can't hand-build common sense).

---

## 4. Dual-purpose: Jarvis ↔ Noesis (the single stone)

The shared core is **L1+L2+L5+L7** of the architecture skeleton: knowledge-hypergraph-with-provenance +
economic-attention-allocation + market-credit-assignment + value-scored-standing. Crystallized by the
planner: **"Jarvis's mind is a single-node, zero-stakes laboratory for Noesis PoM economics."** You debug
the economics where nothing is at stake, then the same mechanism secures a chain where everything is.
`[[voluntary-noesis]]` made structural.

**★ Calibration that survived scrutiny:** the ETM ↔ AtomSpace/ECAN isomorphism came back *structurally
real, not superficial* (the agent was told to flag it if superficial) — BUT **ETM is currently a
philosophy, not a mechanism.** Turning ETM-as-philosophy into ETM-as-mechanism is the ONE body of work both
projects stand on. Do not round "resembles" up to "is" (`[[no-false-pattern-matching]]`).

---

## 5. Honest verdict on the founding thesis

Will's framing — *"transformers imitate intelligence; Jarvis is actual intelligence"* — is **too strong as
stated**: the LLM is still doing real cognition, not mere imitation, and pretending otherwise would be the
exact self-theater the guardrails forbid. **But the architecture is right and the direction is right:** move
the *verifiable, deterministic* share of reasoning into CPU-local structure, and keep the LLM as a
*shrinking* System-1 for grounding, translation, and proposal. "A powerful reasoning engine that doesn't
require a data center" is achievable for a growing fraction of what Jarvis does — and the first slice
(memory-graph deduction, **zero LLM calls**) is buildable this month. That slice is where the claim stops
being aspiration and starts being code.

---

## 6. THE LOOP — build order

- **Increment 1 — clingo memory-graph deduction** (PLAN-01, Phases 1–3). Reach/dead-link/orphan →
  conflict-candidates → load-bearing cones. Deterministic verification (double-run SHA-identical facts +
  independent fixpoint oracle). **START HERE** — five clusters + both planners pointed at this door.
- **Increment 2 — structured critic feedback** in existing hooks (LLM-Modulo). Cheapest, high-upside.
- **Increment 3 — PLN-lite (f,c)** truth-values on gate reliability (self-calibrating hooks).
- **Increment 4 — Z3 + OR-Tools** gate hardening & the concurrency scheduler.
- **→ L2 attention economy** (ETM cashed out) behind its falsifiable exit test: automated allocation must
  beat the hand-tiered MEMORY.md on *context-tokens × task-success*, or it does not ship.

Guardrails §3 apply to every increment. Each increment: commit + push + doc-stamp per the six-commandment loop.
