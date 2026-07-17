# Jarvis Reference Architecture — SKELETON (v0.1)

**Status:** DRAFT SKELETON — written 2026-07-16 while the 9-cluster fan-out is still landing.
Clusters 01–05 (cognitive-architectures, neurosymbolic, symbolic-engines, VSA/Hyperon,
active-inference/econ) have landed and are cited. Clusters 06–09 (knowledge-representation,
evolutionary-emergence, neuromorphic-associative-memory, GOFAI-failure-retrospective) have NOT
landed; every decision that depends on them is marked ⬜ OPEN SLOT. `SYNTHESIS.md` fills the slots.

**Labels used honestly:** `[BUILT]` = running today · `[DESIGNED]` = spec exists, no code ·
`[OPEN]` = question, not answer. Nothing is rounded up.

---

## 0. Thesis and constraint

Intelligence lives in engineered deterministic structure — logical primitives, rules, gates,
circuits, graphs, solvers. The transformer is a rented, fallible **System-1 peripheral**: called
sparingly for what cannot yet be structured (NL understanding, candidate generation, formal
translation), never trusted as the reasoner. This inverts today's Jarvis, where the harness is
deterministic but the *inference* still happens in Claude's weights.

**HARD CONSTRAINT (the constraint is the thesis):** everything below L6 runs on a Ryzen 5 1600
(6c/12t), 16GB RAM, no GPU. Every engine named here passed the laptop test in its dossier.
Symbolic engines, Datalog/ASP, SAT/SMT, rule engines, VSA on CPU, and market bookkeeping are
all sub-second and sub-gigabyte at Jarvis scale (~200–2,000 memory primitives). GPU-bound
candidates were excluded at the dossier level.

---

## 1. Dual purpose: the shared Jarvis ↔ Noesis core (ETM made concrete)

**Claim (owner, 2026-07-16):** this architecture is **ETM operationalized** — mind = economy,
state-rent allocates attention — and **Noesis** (`~/noesis/`) is ETM in
blockchain/AI-intersect form. Therefore the substrate primitives are designed ONCE and
instantiated TWICE:

| Shared primitive | Jarvis instantiation (this doc) | Noesis instantiation (per `noesis/ARCHITECTURE.md`) |
|---|---|---|
| **Weighted knowledge hypergraph** | L1 memory: primitives + wikilinks compiled to a typed, queryable graph | Contribution graph / cell-model state; `temporal_novelty → pom_scores → value_v5..v8` pipeline (`node/src/lib.rs`) |
| **Economic attention allocation** | L2: state-rent on primitives decides what occupies context (working memory = funded set) | CKB cell model's literal state rent; capacity = paid-for state |
| **Provenance of contributions** | Which primitive/hook/session *caused* a good outcome; git history + credit assignment | PoM standing (soulbound) — provenance IS the consensus input |
| **Value-scoring of contributions** | L7 loop: primitives earn/lose standing from measured firing outcomes | `value_v5..v8` scoring of demonstrated contribution vectors |
| **Market credit assignment** | L5: sub-agent auction + Shapley pruning (CouncilShapleyRSI already does this by hand) | Contribution-weighted consensus / reward distribution |

This is the [VoluntaryNoesis] canon made structural: Jarvis's mind runs Noesis PoM economics
voluntarily, off-chain, on one box. Designing L1+L2+L7 well is simultaneously protocol R&D for
Noesis. Kill two birds — but keep the discipline below.

**ANTI-ROUNDING DISCIPLINE (load-bearing):** OpenCog Hyperon's AtomSpace + ECAN is
~isomorphic to ETM **in shape** (dossier 04, Part 3: hypergraph topology STRONG match, STI/LTI ↔
state-rent STRONG match). But the dossier is explicit that the resemblance is *structural
topology*, not *implemented mechanism*: AtomSpace has a real query planner and unification;
ECAN's economics auto-update from computation history; Jarvis's ETM is currently a philosophy.
Mechanism transfer is **UNVERIFIED**. "Resembles" is never rounded up to "is." ECAN itself is
not production-stable in Hyperon (the C++ version is deprecated; MeTTa-native port in progress).
Treat Hyperon as a *convergent design target discovered independently*, not a dependency.
Similarly: never assert Noesis protocol numbers from memory — read the cited `file:line`.

---

## 2. The layer stack

```
        ┌──────────────────────────────────────────────────────────────┐
   L7   │ SELF-IMPROVEMENT LOOP  (TRP operationalized)                  │
        │ bottom-up rule extraction · chunking · market selection ·     │
        │ primitive standing updates                                    │
        └───────▲──────────────────────────────────────────▲───────────┘
                │ crystallized rules / weight updates       │ outcome evidence
        ┌───────┴──────────────────────────────────────────┴───────────┐
   L5   │ DECISION & GOAL ARBITRATION  (WWWD formalized)                │
        │ operator selection · goal truth-values · sub-agent market     │
        └───▲───────────────────────▲──────────────────────▲───────────┘
            │ verified candidates    │ beliefs (f,c)        │ funded context
        ┌───┴───────────┐   ┌───────┴──────────┐   ┌───────┴───────────┐
   L4   │ SYMBOLIC      │L3 │ BELIEF / TRUTH-  │L2 │ ECONOMIC ATTENTION │
        │ REASONING CORE│   │ MAINTENANCE      │   │ ALLOCATOR          │
        │ rules+solvers │   │ (f,c) calculus   │   │ state-rent, STI/LTI│
        └───▲───────────┘   └───────▲──────────┘   └───────▲───────────┘
            │ facts/queries          │ evidence             │ access stats
        ┌───┴────────────────────────┴──────────────────────┴───────────┐
   L1   │ KNOWLEDGE-HYPERGRAPH MEMORY  (shared Jarvis↔Noesis core)      │
        │ typed graph over primitives · deterministic query · VSA index │
        └───────────────────────────▲──────────────────────────────────┘
                                    │ compiled from
        ┌───────────────────────────┴──────────────────────────────────┐
   L0   │ SUBSTRATE: filesystem, markdown, git, hooks runtime, crons    │
        └──────────────────────────────────────────────────────────────┘

   L6 (SIDE PERIPHERAL, called by L4/L5 only when structure runs out):
        ┌──────────────────────────────────────────────────────────────┐
        │ SYSTEM-1 LLM PERIPHERAL (Claude, rented)                      │
        │ NL↔formal translation · candidate generation · impasse oracle │
        └──────────────────────────────────────────────────────────────┘
```

**Canonical data flow (one cognitive cycle):**
1. Event arrives (user prompt, hook trigger, cron fire) → L0.
2. L2 computes the **funded set**: which primitives/beliefs can afford context-rent right now
   (deterministic score — no LLM call to decide what to remember).
3. L4 runs deterministic inference over the funded subgraph (reachability, conflicts,
   constraints, schedules). If the structure fully determines the action → act. **No LLM call.**
4. If structure runs out (novel situation = impasse), L5 formulates a *narrow* query and calls
   L6 (Claude) as oracle. Response is treated as a low-confidence candidate, not truth.
5. L4 verifies the candidate (LLM-Modulo pattern: solver/critic checks, structured feedback,
   bounded retry loop). Only verified output acts.
6. Outcome feeds L3 as evidence (beliefs update), L2 as access/utility signal (rent flows),
   L7 as a crystallization opportunity (can this impasse-resolution become a permanent rule?).

The LLM-call count per cycle trends toward zero as L7 compiles structure. That trend line is
the single most important metric of the whole architecture.

---

## 3. Layer specifications

### L0 — Substrate `[BUILT]`
- **Responsibility:** persistence, event dispatch, scheduling. Files, git, hooks runtime
  (PreToolUse/PostToolUse/SessionStart/Stop), crons, subagent spawn.
- **Jarvis has:** all of it. This is the existing harness — the one layer that is genuinely done.
- **Gap:** none structural. It is the chassis everything else bolts onto.
- **Noesis shared:** git provenance ≈ chain history (weak analogy only — different trust model).

### L1 — Knowledge-Hypergraph Memory `[BUILT as prose / DESIGNED as graph engine]` — SHARED CORE
- **Responsibility:** the mind's declarative memory as a *typed, deterministically queryable*
  hypergraph, not prose the LLM re-reads. Nodes = primitives/facts/entities; edges = wikilinks,
  conflicts, entailments, provenance.
- **Jarvis has:** ~200+ markdown primitives with `[[wikilinks]]`, HIERO-compressed, boot-injected
  by `memory-preprocessor.py`. Topology is already a hypergraph (dossier 04: STRONG isomorphism
  to AtomSpace *in shape*). But traversal today = LLM re-reading — expensive, lossy, unverified.
- **Gap:** no query engine. "All primitives downstream of X," "does the loaded set contain a
  conflict," "orphans" — currently LLM approximations, should be sub-second exact computation.
- **Candidate engines:**
  - **Increment 1 = the parallel ASP-memory-graph plan** (clingo, per dossier 03 §1.3;
    pyDatalog is the zero-dependency fallback, dossier 03 §8 has the complete <1-week build:
    parser → facts → recursive rules → hook integration). ASP adds defaults/negation-as-failure
    over plain Datalog — useful for "apply rule unless overridden" primitive semantics.
  - **Associative side-car:** VSA/hyperdimensional index (torchhd on CPU) for similarity
    retrieval the exact-logic engine can't do — "what primitive resembles this situation."
    Dossier 04 Integration 1 has the sketch. ⬜ OPEN SLOT: confirm/replace after cluster 08
    (neuromorphic-associative-memory) lands — that dossier owns the associative-recall
    engine choice (VSA vs. SDM vs. Hopfield-family vs. skip).
  - **Long-term:** AtomSpace/MeTTa if Hyperon matures (pre-alpha today; do not depend on it).
  - ⬜ OPEN SLOT: node/edge type ontology and schema versioning — cluster 06
    (knowledge-representation) dossier decides (frames vs. description logics vs. plain typed
    Datalog relations; also whether conflicts/exceptions need non-monotonic semantics = ASP
    reinforcement).
- **Noesis shared:** this graph *is* the off-chain twin of Noesis's contribution/state graph.
  Provenance edges (which session/agent/human authored which primitive) = PoM provenance.
  Same schema questions (typed nodes, weighted edges, provenance-carrying) arise on both sides;
  answer once.

### L2 — Economic Attention Allocator `[DESIGNED — this is ETM's cash-out]` — SHARED CORE
- **Responsibility:** decide, deterministically and cheaply, what occupies scarce cognitive
  space: context-window tokens (Jarvis's literal state-rent), hook salience, agent time,
  RAM. Working memory := the funded subset of L1.
- **Jarvis has:** the philosophy (ETM), a hand-tiered approximation (PRE-FLIGHT / HOT / WARM-map
  memory tiers = manual rent bands), and boot-budget discipline. No automatic mechanism: weights
  don't update from access patterns.
- **Gap:** the mechanism. Candidates, in ascending ambition:
  1. **ACT-R activation as deterministic baseline** (dossier 01 §2): score each primitive by
     base-level activation `B = ln(n/t) + β` (frequency/recency) + spreading activation from
     current task terms; top-k within token budget get injected. Auditable, ~zero CPU,
     psychologically validated. Buildable now; PyACT-Up exists if we don't hand-roll.
  2. **Two-currency STI/LTI split** (ECAN shape, dossier 04 §2.4): STI = in-context-now,
     LTI = stays-in-hot-tier vs. archived. Plus Hebbian co-activation edges learned from
     "these primitives were funded together in a successful session."
  3. ⬜ OPEN SLOT: rent *pricing* — flat decay vs. auction vs. utility-backpropagation
     (bucket-brigade from L5 market). Mechanism-transfer from ECAN is UNVERIFIED (see §1);
     cluster 05's market patterns and cluster 07 (evolutionary-emergence) both bear on this.
     Decide in SYNTHESIS with a measurable criterion: does automated allocation beat the
     hand-tiered MEMORY.md on (context tokens spent) × (task success)?
- **Noesis shared:** THE core shared component. Jarvis L2 is a single-node laboratory for
  Noesis state-rent economics: same question ("what does scarce state cost, and who pays?"),
  same failure modes (squatting, starvation, rent-seeking), testable here at zero stakes
  before it's consensus-critical there.

### L3 — Belief & Truth-Maintenance `[OPEN — no current equivalent]`
- **Responsibility:** calibrated uncertainty over the system's own knowledge and machinery.
  Every gate, primitive, and learned rule carries evidence-based confidence, not binary trust.
- **Jarvis has:** nothing formal. Anti-Stale-Feed and Anti-Hallucination protocols are
  *procedural* honesty disciplines executed by the LLM; there is no uncertainty calculus.
- **Candidate engines:**
  - **NARS/ONA** (dossier 01 Rank 1): (frequency, confidence) truth values; revision rule merges
    evidence; designed exactly for insufficient-knowledge-and-resources — Jarvis's operating
    condition. C binary, Python shell, active (v0.9.3, 2025). Start NAL 1–4 only.
  - **clipspyx certainty factors** — cruder, but free if L4 adopts CLIPS anyway.
  - **PLN-lite** (dossier 04 Integration 3) — Hyperon-native shape, but PLN port is not
    production-ready; concept only.
  - ⬜ OPEN SLOT: NARS vs. certainty-factors vs. minimal Bayesian counters. Also ⬜: whether
    L3 truth values and L2 attention values should be one number or must stay orthogonal
    (NARS couples them via priority; ETM suggests rent ≠ truth — a well-funded belief can be
    wrong). Cluster 06 + GOFAI retrospective (09: truth-maintenance systems, why TMS/ATMS
    died or didn't) inform this.
- **Noesis shared:** (f,c) over contribution value ≈ confidence-weighted `pom_scores`;
  Noesis's status discipline (built/designed/open, never round up) is L3 practiced by humans.

### L4 — Symbolic Reasoning Core `[DESIGNED — engines chosen, wiring not built]`
- **Responsibility:** all inference that can be exact: graph queries, constraint checks,
  scheduling, rule firing with conflict resolution, plan validation. The System-2 that is
  *actually deterministic* rather than an LLM told to think step-by-step.
- **Jarvis has:** 54 Python hook scripts (`~/.claude/hooks/`, counted 2026-07-16) = hand-rolled
  production rules with fixed ordering; no
  agenda, no conflict resolution, no fact base. Deterministic but not a *reasoner*.
- **Candidate engines (all pip-installable, all pass laptop test):**
  - **Datalog/ASP (clingo / pyDatalog)** — graph inference over L1 (increment 1, see L1).
  - **CLIPS (clipspy/clipspyx)** — production-rule engine with salience, agenda, retraction;
    upgrade path for hook dispatch (dossier 01 Rank 2; NeuSymMS blueprint exists).
  - **Z3** — gate precondition checker: permission rules and Foundry-performance rules as
    constraints; a gate that blocks does so with an unsat proof, not a regex (dossier 03 Rank 2).
  - **OR-Tools CP-SAT** — subagent/test scheduler under the 3-process/16GB constraint
    (dossier 03 Rank 3).
  - **LLM-Modulo controller** (dossier 02 §2, §11.1): the *pattern* binding L4 to L6 —
    LLM generates, symbolic critics verify, structured feedback loops back, bounded retries.
    Hooks upgraded from "block with error string" to "return machine-usable critique."
  - ⬜ OPEN SLOT: PDDL planning — does Jarvis need explicit plan synthesis (Fast Downward)
    or is goal-arbitration + rules enough? Defer until L5 experience says plans are the
    bottleneck. GOFAI retrospective (09) should report why planning brittleness killed prior
    attempts, and what changed.
- **Noesis shared:** modest — verification-before-trust is the same posture as consensus
  validation, but engines differ (Z3 here, RISC-V determinism there). Shared *discipline*,
  not shared code.

### L5 — Decision & Goal Arbitration (WWWD formalized) `[BUILT as LLM gate / OPEN as mechanism]`
- **Responsibility:** which goal, which operator, which agent, act-or-escalate. Today's WWWD.
- **Jarvis has:** WWWD `[BUILT]` — but as an LLM emulation of Will, i.e., System-1 wearing a
  System-2 costume. Also CouncilShapleyRSI: *manual* market-based seat pruning by exact Shapley.
- **Candidate mechanisms:**
  - **Market-based sub-agent routing / Hayek-machine** (dossier 05 #1): agents bid from wealth,
    bucket-brigade credit assignment, WWWD verdict = settlement signal, bankruptcy = pruning.
    ~150 lines, no ML, the most ETM-native option. Automates what CouncilShapleyRSI does by hand.
  - **SOAR-style impasse discipline** (dossier 01): no-rule-matches → substate → oracle (L6) →
    chunk the resolution into a permanent rule (feeds L7). Adopt the *pattern* now; adopt SOAR
    itself only if the rule base outgrows CLIPS (6–12 month decision, not now).
  - **NARS goals** as first-class objects with truth values → principled multi-goal arbitration.
  - **Active-inference EFE** (pymdp, dossier 05 #2): adds principled explore-vs-exploit the
    market lacks. ⬜ OPEN SLOT: market-only vs. market+EFE vs. NARS-goals — SYNTHESIS decides;
    do not build two arbitration mechanisms simultaneously.
- **Gap:** everything except the escalation path. WWWD's *escalate-to-Will* branch is load-
  bearing and survives every candidate: the human stays the final arbiter.
- **Noesis shared:** STRONG — auction + credit-assignment + prune-by-marginal-contribution is
  the same mechanism family as contribution-weighted consensus and Shapley-style reward
  splitting. L5 telemetry = empirical data for Noesis mechanism design.

### L6 — System-1 LLM Peripheral `[BUILT — currently overweight]`
- **Responsibility (target state):** NL↔formal translation, candidate generation under
  constraint, impasse oracle, prose rendering. Called *by* L4/L5 with narrow, structured
  queries; output always verified before it acts. PRIMUS says it exactly: LLMs are lobes,
  not the substrate.
- **Jarvis has:** Claude as ~98% of current inference. The whole migration is the controlled
  shrinkage of this layer's duty cycle.
- **Gap:** inversion of control. Today the LLM calls tools; target is structure calls the LLM.
  Concretely: grammar-constrained/structured outputs at the boundary (Outlines-class tooling,
  dossier 02 §4) so L6 returns parseable candidates, never free prose into the control path.
- **Noesis shared:** none directly (Noesis consensus must not depend on an LLM). The shared
  item is the *boundary discipline*: unverified generation never touches state.

### L7 — Self-Improvement Loop (TRP operationalized) `[BUILT as protocol / DESIGNED as mechanism]`
- **Responsibility:** the CLARION dynamic, which dossier 01 identifies as the philosophically
  correct frame for the whole system: LLM = implicit bottom level, structure = explicit top
  level, and this loop is **bottom-up extraction** — watch the bottom level solve impasses,
  crystallize recurring solutions into permanent rules/gates/primitives. Plus the economic
  selection loop: rules that earn (L2 rent inflow, L5 wealth) persist; rules that don't are
  pruned. SOAR calls the first half chunking; TRP/trp2 already does it by hand.
- **Jarvis has:** TRP/trp2 `[BUILT]` (human-in-loop derivation of new gates/hooks/primitives),
  RSAW self-audits, CouncilShapleyRSI. All LLM-executed protocols, not mechanisms.
- **Gap:** closing the loop mechanically — impasse log → candidate rule → shadow-mode trial
  (rule predicts, doesn't act) → L3 confidence accumulates → promotion to live gate. Note
  Jarvis today *cannot* hot-load a hook mid-session (dossier 04 §3 point 4); promotion is a
  between-sessions step, which is acceptable and safer.
  - ⬜ OPEN SLOT: variation mechanism — LLM-mutated rules vs. ILP (Popper, dossier 03 §6) vs.
    evolutionary search. Cluster 07 (evolutionary-emergence) owns this decision.
  - ⬜ OPEN SLOT: safety rails for self-modification — which layers may L7 touch (proposal:
    L1 content and L2 weights yes; L0 substrate and the escalation path never). GOFAI
    retrospective (09) should report how EURISKO-style self-modification failed.
- **Noesis shared:** STRONG — "value-scored contributions accumulate standing; standing gates
  influence" is literally the PoM loop. L7 is Jarvis earning PoM standing from itself.

---

## 4. Consolidated map: have / gap / Noesis-share

| Layer | Jarvis already has | Gap | Noesis shared component | Share strength |
|---|---|---|---|---|
| L0 Substrate | hooks, crons, git, files [BUILT] | — | provenance-by-history | weak |
| L1 Hypergraph | markdown graph + wikilinks [BUILT as prose] | query engine (ASP/Datalog), VSA index, typed schema | contribution/state graph, provenance | **STRONG** |
| L2 Attention | ETM philosophy + manual tiers | activation scoring → two-currency rent, auto-update | **state-rent economics** | **STRONG (core)** |
| L3 Belief | honesty protocols (procedural) | (f,c) calculus (NARS/ONA ⬜) | confidence-weighted value scores | moderate |
| L4 Reasoning | Python hooks (fixed-order) | CLIPS agenda, Z3 gates, CP-SAT scheduling, LLM-Modulo wiring | verification-before-trust posture | weak (discipline only) |
| L5 Arbitration | WWWD (LLM), manual Shapley pruning | agent market, impasse discipline, ⬜ EFE | auction/credit/prune mechanisms | **STRONG** |
| L6 LLM | Claude at ~98% duty cycle | inversion of control, structured boundary | none (by design) | none |
| L7 Self-improve | TRP/trp2, RSAW (protocols) | mechanical crystallize→shadow→promote loop | **PoM standing loop** | **STRONG** |

The STRONG column (L1, L2, L5, L7) *is* the shared Jarvis↔Noesis core: hypergraph + rent +
market-credit + value-standing. Design decisions there should be written once, with both
instantiations in view.

---

## 5. Migration path (increments, each independently shippable)

Sequenced by: current-bottleneck-first, dependency order, and ship-ready-units discipline.
Each increment leaves the system better even if the next one never happens.

- **Increment 1 — L1 graph compiler** `[coordinate: this IS the parallel ASP-memory-graph
  plan]`. Parse primitives → facts; reachability/conflict/orphan/entailment queries; wire into
  `memory-preprocessor.py` so boot injection = computed entailed set, not tier dump.
  Engine per that plan (clingo ASP; pyDatalog fallback). ~1 week per dossier 03 §8.
  *Exit test:* boot context tokens ↓ with zero missed-primitive regressions.
- **Increment 2 — L2 v0 activation scoring.** ACT-R base-level activation over Increment 1's
  graph + access log; deterministic top-k-within-budget injection. First measurable ETM
  mechanism. *Exit test:* beats hand-tiered MEMORY.md on tokens × task-success.
- **Increment 3 — L4 gate hardening.** Z3 precondition gate (permissions, Foundry rules) +
  structured-critic hook outputs (LLM-Modulo feedback shape) + CP-SAT scheduler for
  subagent/forge concurrency. Three small independent units.
- **Increment 4 — L3 belief layer.** ⬜ engine per SYNTHESIS (default candidate: ONA, NAL 1–4).
  Every gate firing logs evidence; gates acquire (f,c); WWWD context shows calibrated
  confidence instead of nothing.
- **Increment 5 — L5 agent market.** Hayek-machine routing over existing subagent types;
  WWWD verdict as settlement; Shapley pruning automated. Telemetry doubles as Noesis
  mechanism-design data. ⬜ EFE add-on decided later.
- **Increment 6 — L7 closed loop.** Impasse log → candidate rule → shadow mode → L3
  confidence threshold → between-session promotion. Only attempt after 3+4 exist (needs
  structured critiques as input and (f,c) as promotion gate).
- **Increment 7 — L2 v1 full rent economy.** Two-currency STI/LTI + credit backpropagation
  from L5 settlements, replacing v0's fixed formula — the full ETM mechanism, informed by
  live data from increments 2/5 and by the ⬜ pricing-slot decision. This is the increment
  with direct Noesis read-across; document it bilingually (Jarvis mechanism + Noesis note).

L6 shrinkage is not an increment — it is the metric. Track LLM-calls-per-task and
percent-of-decisions-made-by-structure from Increment 1 onward.

---

## 6. Open-slot register (for SYNTHESIS.md)

| # | Slot | Layer | Deciding input |
|---|---|---|---|
| 1 | Associative-recall engine (VSA/torchhd vs. alternatives vs. skip) | L1 | cluster 08 dossier |
| 2 | Node/edge ontology; non-monotonic semantics need | L1 | cluster 06 dossier |
| 3 | Rent pricing mechanism (decay vs. auction vs. utility-backprop); ECAN transfer verdict | L2 | clusters 04+05+07; empirical exit-test of Increment 2 |
| 4 | Truth-value engine (NARS vs. certainty factors vs. Bayesian counters); rent⊥truth orthogonality | L3 | clusters 01+06+09 |
| 5 | PDDL planning: needed at all? | L4 | cluster 09 + L5 experience |
| 6 | Arbitration mechanism (market-only vs. +EFE vs. NARS-goals) | L5 | clusters 01+05; pick ONE |
| 7 | Rule-variation mechanism (LLM-mutate vs. ILP vs. evolutionary) | L7 | cluster 07 dossier |
| 8 | Self-modification safety rails (which layers L7 may touch) | L7 | cluster 09 (EURISKO et al.) |

---

## 7. What this skeleton is not

Not a claim that any of this is intelligence yet. Clusters 01–05 establish that every layer has
a mature, CPU-native engine candidate and that the composition is the pattern the neurosymbolic
literature independently converged on (dossier 02 §13's diagram is this stack, compressed).
Whether the composed system *reasons* better than the LLM it wraps is an empirical question,
answered per-increment by the exit tests — never by vibes. GOFAI died partly of unfalsifiable
architecture diagrams; every box above therefore carries a measurable exit condition or an ⬜.
