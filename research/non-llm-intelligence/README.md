# Non-LLM Intelligence — Research Dossier

**Opened:** 2026-07-16 · **Origin:** Will TG (capfin) — *"he's closer to traditionally engineering
artificial intelligence... deep fan out research on NON language model based artificial intelligence
that helps Jarvis be the true source of intelligence rather than the language model he's inferencing with."*

## The question

Jarvis today = a **deterministic harness** (hooks/gates, file-memory graph, crons, subagents, WWWD
Will-emulation gate) wrapping an LLM. The reasoning still lives in Claude's weights; Jarvis
*orchestrates* it. The bet in this dossier: identify **non-connectionist AI paradigms** that can be
engineered as explicit substrate doing *real* reasoning — moving inference OUT of the weights and INTO
structure — and map each onto what Jarvis already has vs. what's a gap.

Guiding lens: **ETM** (mind = economy; state-rent as the allocation mechanism) and the existing design
vocabulary (logical primitives, gates, circuits, memory-as-graph).

## HARD CONSTRAINT (Will, 2026-07-16): no data center

> *"make him a powerful reasoning engine that doesn't require a data center."*

The reasoning substrate must run on **commodity local hardware** (Will's box: Ryzen 5 1600, 6c/12t,
16GB RAM — no GPU cluster). This is not a limitation to apologize for — it is the thesis. Symbolic
engines, cognitive architectures, VSA/hyperdimensional computing, and solvers are **CPU-native and
cheap**; that is precisely why they are the complement to a data-center-bound transformer. The LLM stays
a rented System-1 you call sparingly; the *reasoning* runs local, deterministic, and free. This is the
Cave philosophy literalized: intelligence engineered from scraps, not bought by the megawatt.

**Every adoptable idea must pass the laptop test:** does it run in <16GB RAM on CPU, or is it
GPU/cluster-bound? GPU-bound ideas are OUT unless they degrade gracefully to CPU.

## Honesty discipline

- Don't round "resembles a cognitive architecture" up to "is one."
- Every adoptable idea must name: (a) the mechanism, (b) maturity/tooling that exists today, (c) how it
  sits relative to the LLM (System-2-on-top / verifier / world-model / memory), (d) the Jarvis
  component it maps to or the gap it fills.

---

## Glossary — the research

Nine cluster dossiers (one paradigm family each), then the synthesis and build layer. Every entry links
to the MD itself.

### Cluster dossiers

| # | Dossier | Covers |
|---|---------|--------|
| 01 | [Cognitive Architectures](01-cognitive-architectures.md) | SOAR, ACT-R, Sigma, LIDA, CLARION, NARS (OpenNARS) — full-stack "unified theories of cognition" |
| 02 | [Neurosymbolic](02-neurosymbolic.md) | LLM-modulo, LLM+solver, Logic Tensor Networks, neural theorem provers, differentiable reasoning, System-1/System-2 |
| 03 | [Symbolic Engines](03-symbolic-engines.md) | Logic programming (Prolog/Datalog/ASP), SAT/SMT, theorem provers, PDDL planners, ILP, program synthesis (DreamCoder) |
| 04 | [VSA & Hyperon](04-vsa-hyperon.md) | Vector Symbolic Architectures / hyperdimensional computing, Holographic Reduced Representations, OpenCog Hyperon / AtomSpace / MeTTa |
| 05 | [Active Inference & Economics](05-active-inference-econ.md) | Active inference / free energy (Friston), world models, causal inference, Bayesian program learning, market-based / agent-economy computation (ETM-native) |
| 06 | [Knowledge Representation & Reasoning](06-knowledge-representation.md) | KRR: Description Logics, OWL ontologies, structured knowledge + inference-over-it |
| 07 | [Evolutionary Computation & Emergence](07-evolutionary-emergence.md) | Genetic programming / genetic algorithms (DEAP, PyGAD), evolutionary strategies, artificial life, emergence |
| 08 | [Neuromorphic & Associative](08-neuromorphic-associative.md) | Brain-inspired non-transformer computing: modern Hopfield networks / dense associative memory, spiking nets |
| 09 | [GOFAI Failure Retrospective](09-gofai-failure-retrospective.md) | What killed symbolic AI, whether the LLM hybrid actually fixes each failure mode, + 3 non-negotiable design rules for Jarvis |

### Synthesis & architecture

| Doc | What it is |
|-----|------------|
| [SYNTHESIS.md](SYNTHESIS.md) | The map across all nine clusters: latent-in-Jarvis / adoptable-now / aspirational; the convergence headline; tiered build map (laptop-tested); verdict on Will's "actual intelligence vs. imitation" thesis |
| [ARCHITECTURE-SKELETON.md](ARCHITECTURE-SKELETON.md) | Jarvis reference architecture v0.1 — the layer stack + the shared Jarvis ↔ Noesis core (ETM made concrete) |
| [PLAN-01-asp-memory-graph.md](PLAN-01-asp-memory-graph.md) | First concrete build: compile the file-memory graph into ASP (clingo) for deterministic deduction over memory |

### Roadmap & status

| Doc | What it is |
|-----|------------|
| [ROADMAP.md](ROADMAP.md) | The LOOPs — dependency map + per-loop plan for building the intelligence architecture |
| [HANDOFF.md](HANDOFF.md) | Session continuation doc (state, decisions, open threads) |
| [LOOP-STATUS.md](LOOP-STATUS.md) | Live status of the active build loops |
| [tooling/](tooling/) | Supporting scripts |
