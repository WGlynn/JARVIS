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

## Clusters (one dossier file each)

1. `01-cognitive-architectures.md` — SOAR, ACT-R, Sigma, LIDA, CLARION, NARS (OpenNARS)
2. `02-neurosymbolic.md` — LLM-modulo, LLM+solver, Logic Tensor Networks, neural theorem provers, differentiable reasoning, System-1/System-2
3. `03-symbolic-engines.md` — logic programming (Prolog/Datalog/ASP), SAT/SMT, theorem provers, PDDL planners, ILP, program synthesis (DreamCoder)
4. `04-vsa-hyperon.md` — Vector Symbolic Architectures / hyperdimensional computing, Holographic Reduced Representations, OpenCog Hyperon / AtomSpace / MeTTa
5. `05-active-inference-econ.md` — active inference / free energy (Friston), world models, causal inference, Bayesian program learning, market-based / agent-economy computation (ETM-native)

## Synthesis

`SYNTHESIS.md` (Jarvis-authored after clusters land) — the map: latent-in-Jarvis / adoptable-now /
aspirational, plus the one-paragraph verdict on Will's "actual intelligence vs. imitation" thesis.
