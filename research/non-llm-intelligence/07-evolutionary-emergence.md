# Cluster 7 — Evolutionary Computation, Artificial Life & Emergence

**Opened:** 2026-07-16  
**Cluster mandate:** Genetic programming + genetic algorithms (DEAP, PyGAD); evolutionary strategies
(CMA-ES); cellular automata + emergence (Wolfram classes, Lenia, Game of Life); swarm / ant-colony /
particle-swarm optimization; artificial life; novelty search + quality-diversity (MAP-Elites); and
self-organizing systems. Key Jarvis question: can the substrate **evolve its own primitives/gates/rules**
(there is already a "TRP" loop that derives new components) — i.e. genetic programming over the gate /
primitive population, with fitness = does the rule catch real errors / reduce tokens?

**Hard constraint:** Ryzen 5 1600 / 16 GB RAM / no GPU. Flag anything that fails the laptop test.

---

## 1. Genetic Programming (GP) — Evolving Programs as Trees

### 1a. Core mechanism

GP operates on a population of **syntax trees** whose leaves are terminals (constants or input
variables) and whose internal nodes are primitives (functions). At each generation the algorithm
selects higher-fitness individuals, applies crossover (swap subtrees) and mutation (replace subtrees
with random ones), enforces size/depth limits to curb "bloat" (programs that grow large without
fitness gain), and repeats. The output of a run is an evolved program — not tuned parameters, but
actual executable logic.

This is qualitatively different from a genetic algorithm (which optimizes a fixed-length parameter
vector). GP discovers the **structure** of the solution, which is why it is the right analogy for
evolving Jarvis gates: a gate is a predicate, a hook is a program, a primitive is a reusable
subtree.

### 1b. Maturity + Python tooling

**DEAP 1.4.4** (released April 2026; actively maintained) is the primary Python framework. It
provides:
- Strongly and loosely typed GP tree evolution
- Built-in bloat control (`staticLimit`, `selDoubleTournament` for parsimony)
- Pluggable fitness functions (you supply the evaluator)
- Multiprocessing via Python's `multiprocessing.Pool` — runs all cores, no GPU needed
- Genetic Algorithms, Genetic Programming, Evolution Strategies, multi-objective (NSGA-II, SPEA2)
  in one library

**gplearn** (scikit-learn-compatible) offers a narrower focus: symbolic regression and
classification, parallelized with joblib. Not as flexible as DEAP but good for numeric fitness
signals.

**Operon** (C++ with Python bindings) uses SIMD vectorization and Taskflow for population-level
parallelism on CPU. Faster than DEAP for numeric fitness, but harder to customize the fitness
function.

**Laptop test:** DEAP passes cleanly. A population of 500 trees evaluating Python-callable fitness
functions on a single machine is routine. Memory footprint per tree is small (Python objects); 16 GB
is comfortable at populations of 500-2000. Operon is faster but overkill for small populations.

### 1c. Relation to the LLM

Two complementary modes:

1. **LLM seeds the primitive/terminal set.** Instead of hand-specifying what operators and predicates
   exist in the GP vocabulary, ask Claude once to generate candidate "building blocks" based on the
   domain. GP then selects which combinations of those building blocks constitute the best gate.

2. **LLM as intelligent mutation operator ("Evolution through Large Models" / ELM).** Replace
   random subtree mutation with an LLM call: "here is the current gate program; here is the fitness
   signal; propose a variation." This is FunSearch's core idea (Romera-Paredes et al., 2024) and
   AlphaEvolve's generalization (May 2025). The LLM mutation is semantically aware; random GP
   mutation is blind but cheap. A 30/70 split (30% LLM mutation, 70% structural) has been shown to
   outperform either alone (Lyria results).

   **Laptop feasibility of ELM:** the LLM call is the Claude API (remote), not local inference. So
   the evolutionary loop stays on the Ryzen; only the mutation calls go out. This is exactly how
   Jarvis already works — Claude is a rented System-1. ELM just adds that call inside a selection
   loop.

### 1d. Jarvis mapping

The TRP loop already does manual component derivation: "identify bottleneck → derive primitive →
test." GP over the primitive population is a principled, automated version of that same loop:

```
population = all current hooks/gates/predicates (as DEAP GP trees)
fitness(tree) = (error_catch_rate on WAL history) - alpha * (mean_tokens_per_invocation)
loop:
    select top-k trees
    crossover + mutate (LLM mutation for semantic moves; structural for diversity)
    evaluate fitness on held-out WAL slice
    replace bottom-k
    if champion fitness improved: emit as new primitive candidate for Will approval
```

The fitness signal is available right now: WAL.md records errors and token spend per session.
Precision (did the gate fire when it should?) and token cost (did the gate reduce LLM calls?) are
both measurable from existing logs.

**Concrete gap:** DEAP trees represent fixed-arity function calls. Jarvis gates are Python
callables. The translation layer is: each terminal is a WAL/memory read, each primitive is a
predicate combiner (AND, OR, NOT, THRESHOLD, CONTAINS). Fitness evaluator reads a WAL replay
dataset and scores each candidate gate. This is a ~200-line integration; nothing in DEAP blocks it.

---

## 2. Genetic Algorithms (GA) — Parameter and Rule Optimization

### 2a. Core mechanism

A GA optimizes a fixed-length representation (bitstring, float vector, or heterogeneous struct).
Each generation: evaluate fitness, select, crossover, mutate. Unlike GP, GA does not evolve
program structure — it evolves parameters or discrete choices within a fixed schema.

For Jarvis, GAs are relevant for:
- Tuning **hook thresholds** (e.g., the 5% TWAP deviation limit, sliding-window sizes)
- Selecting **which hooks are active** in a given session context (bitstring over hook population)
- Optimizing **prompt templates** (where the search space is a discrete vocabulary)

### 2b. Maturity + Python tooling

**PyGAD 3.7.0** (June 2026) is the leading lightweight option: numpy + cloudpickle only, fully
CPU, supports multi-objective (NSGA-II, NSGA-III), flexible early stopping (`reach_X`,
`saturate_N`, `time_T`), optional Keras/PyTorch integration. Excellent documentation.

**DEAP** covers GAs as well (it is multi-paradigm). Use PyGAD for quick iteration, DEAP when you
need tighter control or combined GP+GA runs.

**Laptop test:** Both pass. PyGAD runs on numpy; a population of 200 individuals with 50-parameter
genomes evaluating Python fitness is trivially fast on 6 cores.

### 2c. Relation to the LLM

GA is primarily a **complement** to the LLM, not a replacement. Use GA to find the best
configuration of a parameterized harness; call the LLM only when the problem is not parameterizable.

### 2d. Jarvis mapping

- Evolve the **hook activation bitmask**: which of the N defined hooks are active for a given
  session type? Fitness = (errors caught) / (total hooks invoked) — a precision-per-hook-call signal.
- Evolve **threshold constants** in existing gates: TWAP deviation %, sliding-window durations,
  MAX_PARALLEL_AGENTS. Currently hardcoded; GA can search the Pareto front of (precision, overhead).

---

## 3. Evolution Strategies (ES) and CMA-ES

### 3a. Core mechanism

Evolution Strategies operate on real-valued parameter vectors and are **self-adapting**: the
mutation step size and distribution shape are themselves evolved, removing the need to hand-tune
learning rates. CMA-ES (Covariance Matrix Adaptation Evolution Strategy) is the gold standard: it
maintains and adapts a full covariance matrix describing the search distribution, using "evolution
paths" (cumulative step-size adaptation) to learn the local landscape curvature.

ES is typically used for **continuous** optimization — hyperparameter tuning, neural architecture
search, robotics policy parameters.

### 3b. Maturity + Python tooling

- `cmaes` (CyberAgentAILab, arXiv 2402.01373): minimal, readable pure-Python CMA-ES. Best for
  integration into larger pipelines.
- `pymoo`: full multi-objective framework including CMA-ES, NSGA-II, etc.
- Optuna's `CmaEsSampler`: drop-in sampler for hyperparameter optimization; CMA-ES with Margin
  handles mixed integer-continuous spaces (GECCO 2025: CatCMAwM extends to categorical).

**Laptop test:** Passes. CMA-ES is CPU-native; a population of 64 candidates in parallel maps
cleanly to 6 cores. Memory is O(n²) in the parameter dimension — for n < 1000 parameters this is
under 8 MB.

### 3c. Jarvis mapping

CMA-ES is the right tool when the search space is **continuous and low-to-medium dimensional** and
the fitness signal is noisy or expensive. For Jarvis: if hook threshold parameters are real-valued
and the fitness function is noisy (WAL logs vary session to session), CMA-ES will converge faster
than a GA. It is not the tool for evolving program structure (GP handles that).

---

## 4. Cellular Automata and Emergence

### 4a. Core mechanism

A cellular automaton (CA) is a grid of cells, each in one of a finite set of states, evolving in
discrete time according to a **local rule**: the next state of a cell depends only on its own state
and its neighbors'. The global behavior is entirely determined by the local rule — no central
controller.

Wolfram's classification (1980s) divides CA rules into four classes by behavior:
- Class 1: fixed point (all cells converge to a static pattern)
- Class 2: periodic / stable structures
- Class 3: chaotic / pseudo-random
- Class 4: complex, long-lived structures — **the interesting class**. Conway's Game of Life (proven
  Turing-complete) lives here.

**Lenia** (Chan 2019+) extends CAs to continuous states and continuous space-time, producing
lifelike self-organizing patterns. Genetically searchable: researchers have used GA + GP search to
discover new Lenia "creatures" exhibiting self-replication, emission, and division of labor. Whether
Lenia is Turing-complete is an **open question** as of 2026.

**Neural CAs** (NCA): replace the handcrafted CA rule with a small neural network, trained
end-to-end via gradient descent. NCA can solve morphogenesis tasks, ARC-challenge reasoning
instances, and self-organization. This is an LLM-augmentable paradigm (the network is tiny and
CPU-trainable).

### 4b. Honest assessment of "emergence"

Here is where the hand-waving must be flagged: "emergence" in the CA context is not a vague
metaphor — it is a **concrete computational claim** about what behaviors a local rule generates at
scale. Class 4 emergence is interesting precisely because it is not easily reducible to the rule
alone; computation "bootstraps" from local interactions. This is a verified phenomenon in specific
systems (Game of Life, Rule 110), not a general property of complex systems.

The claim that "many small gates yield system-level intelligence" in Jarvis is an **analogy**, not a
proven theorem. The structural parallel is real (gates interact locally; the harness exhibits global
behavior nobody pre-specified), but:
- We have no proof that Jarvis's gate interactions are Turing-complete or Class 4 in Wolfram's
  sense.
- "Emergence" as used in most ALife papers means something weaker: behavior that is non-obvious
  from inspection of individual rules.

The analogy is still useful as a **design intuition**: keep gates local and composable; avoid
centralized state; let harness-level behavior arise from interactions. This is exactly what the
TRP/HIERO compaction loop does. But don't claim Jarvis "self-organizes" in the strong CA sense
without measurement.

### 4c. Python tooling

- **CAX** (Cellular Automata Accelerated in JAX): ICLR 2025 Oral. Runs on CPU/GPU/TPU via JAX.
  CPU mode is usable but slow for large grids. For Jarvis purposes (small rule spaces), CPU is fine.
- `cellular-automata` GitHub topic: dozens of pure-numpy implementations, very lightweight.
- Elementary CA in numpy: trivial to implement — 3-neighbor lookup table on a bitarray.

**Laptop test:** Simple CAs (1D, Game of Life 2D, small Lenia grids) pass easily. Lenia on large
grids requires JAX GPU for real-time animation; CPU Lenia on a 128×128 grid is usable for research.

### 4d. Jarvis mapping

The most **concrete** Jarvis use of CA is not running a CA simulation — it is using the CA as a
**model for harness design**: gates should be local (take minimal context), stateless where
possible, and composable. The gate population should exhibit Class 4 behavior: not trivially
converging to silence (no gates fire) or chaos (all gates fire), but maintaining useful structure.

A more exotic but real use: **evolve CA rules** over a gate-like substrate — where "cells" are
session-state slots and "rule" is the gate firing condition. GA over rule space is
computationally cheap and does produce useful heuristics for small state spaces.

---

## 5. Swarm Intelligence — Ant Colony Optimization (ACO) and Particle Swarm Optimization (PSO)

### 5a. Core mechanisms

**ACO:** Artificial ants traverse a problem graph, depositing pheromone on edges proportional to
solution quality. Pheromone evaporates over time; the colony collectively reinforces shorter/better
paths. Best for **combinatorial optimization** (routing, scheduling, TSP).

**PSO:** Particles move through a continuous search space, each attracted toward its personal best
and the global best found by any particle. No gradient required. Best for **continuous
multi-modal** optimization.

### 5b. Python tooling

- `pyswarms`: PSO in Python, actively maintained, CPU only.
- `ACOpy`: ACO implementation for TSP-class problems.
- DataCamp's open tutorial covers ACO + PSO + Artificial Bee Colony in pure Python.

**Laptop test:** Both pass trivially. PSO and ACO are O(population × evaluations); populations of
50-200 is standard; CPU is completely sufficient.

### 5c. Honest assessment for Jarvis

ACO and PSO solve a narrower class of problems than GP/GA. Their Jarvis relevance is limited:
- ACO could optimize **session scheduling** (which cron jobs to run in which order) or
  **hook invocation order** when order matters.
- PSO could tune continuous threshold parameters — but CMA-ES is strictly better at this.

These are not primary tools. They are useful for specific sub-problems where the graph structure or
multi-modal landscape makes them the right fit. Don't reach for ACO/PSO before exhausting GA/CMA-ES.

---

## 6. Novelty Search and Quality-Diversity (QD)

### 6a. Core mechanism

**Novelty Search** (Lehman & Stanley 2008/2011): replace the fitness function with a **novelty
metric** — reward individuals for being different from everything found so far. This avoids local
optima in deceptive fitness landscapes (where hill-climbing toward the objective leads away from
the solution). The algorithm maintains an archive of "stepping stones" — behaviorally diverse
individuals that may not score well on the final objective but open up new regions of search.

**Quality-Diversity (QD) / MAP-Elites** (Mouret & Clune 2015): maintain a **grid of behavioral
niches**. Each cell in the grid stores the highest-fitness individual for that behavior
characterization. The algorithm simultaneously maximizes diversity (coverage of the grid) and
quality (fitness within each cell). The result is not a single solution but an **illuminated map**
of the fitness landscape.

### 6b. Python tooling

**pyribs 0.11.0:** the primary Python library for QD. Implements MAP-Elites, CMA-ME, CMA-MAE, and
scalable QD variants. **Deliberately single-threaded and CPU-only** ("only runs single-threaded on
a single CPU" per docs — designed for accessibility, not cluster scale). Minimal dependencies.
Excellent documentation including a QDAIF tutorial (QD through AI Feedback — pyribs + LLM for
diverse story generation).

**pymap_elites** (resibots): the original reference MAP-Elites implementation, including CVT
MAP-Elites for high-dimensional behavior spaces.

**DCRL-MAP-Elites:** adds a reinforcement learning variation operator; requires more dependencies.

**Laptop test:** pyribs passes. Single-threaded numpy. A 100×100 behavior grid with 10,000
evaluations is fast on CPU.

### 6c. LLM + QD

The QDAIF paradigm (Quality Diversity through AI Feedback): use the LLM to mutate candidates
(generating diverse variants) and as the evaluator (scoring them). This is directly applicable to
the Jarvis primitive population: maintain a grid of primitives characterized by (behavioral domain,
trigger type); fill each cell with the highest-precision gate for that niche. The LLM generates
variants; CPU-local QD algorithm manages the archive.

### 6d. Jarvis mapping — the key insight

MAP-Elites solves the problem that plain GP/GA can converge to a **single dominant primitive type**
that covers one niche well but leaves others empty. The Jarvis primitive population should be
diverse: some gates catch logic errors, some catch token waste, some catch memory drift, some catch
security boundary violations. MAP-Elites with behavior descriptors = (error category, trigger
phase) maintains one champion per niche, preventing monoculture.

This is a more principled version of the RSI loop's current "derive new component from bottleneck"
heuristic: instead of Will manually identifying underserved niches, MAP-Elites measures which grid
cells are empty and directs search there.

```python
# Sketch: MAP-Elites over Jarvis gate population
# Behavior descriptor: (error_category: int[0..N], session_phase: int[0..3])
# Fitness: precision on WAL replay (true positives / (true + false positives))

import ribs
archive = ribs.archives.GridArchive(
    solution_dim=len(gate_parameters),
    dims=[N_error_categories, 4],        # 4 session phases
    ranges=[(0, N_error_categories), (0, 4)]
)
emitter = ribs.emitters.GaussianEmitter(archive, sigma=0.1, ...)
scheduler = ribs.schedulers.Scheduler(archive, [emitter])

for _ in range(n_iters):
    solutions = scheduler.ask()
    objectives, measures = evaluate_gates_on_wal(solutions)  # CPU-local
    scheduler.tell(objectives, measures)
```

---

## 7. Open-Ended Evolution and LLM-Guided Evolutionary Search (the 2025 frontier)

### 7a. The FunSearch → AlphaEvolve lineage

**FunSearch** (Romera-Paredes et al. 2024): pair an LLM with a programmatic evaluator. LLM
generates candidate functions in Python; evaluator scores them; top candidates go back into the
context for the next LLM call. Discovered new combinatorics results beyond human best-known.

**AlphaEvolve** (DeepMind, May 2025): extends to whole codebases. Uses Gemini Flash (fast,
high-volume generation) + Gemini Pro (fewer, higher-quality suggestions). Improved Strassen's
matrix multiplication algorithm after 56 years. **Closed source.**

**Open-source equivalents (2025):**
- **OpenEvolve** (MIT license): open implementation of AlphaEvolve. Supports any LLM via API,
  islands-based GA, asynchronous sandboxed evaluation.
- **CodeEvolve**: adds weighted LLM ensemble, inspiration-based crossover, meta-prompting.
  Outperforms AlphaEvolve on 4 benchmark problems.
- **GEAR** (Genetic AutoResearch, May 2026): drop-in replacement for single-incumbent hill-climbing
  in research agents. Maintains bounded elite population; composite selection score balances
  productivity, local novelty, global coverage. Three variants: GEAR-Prompt (LLM manages
  population in NL), GEAR-Fixed (programmatic controller), GEAR-Evolve (controller is itself
  mutable). All outperform AutoResearch baseline at equal compute.

### 7b. Honest GPU-bound flag

AlphaEvolve uses Gemini — cloud, not local. OpenEvolve and CodeEvolve also use API-based LLMs by
default. The LLM backbone for ELM **does not run on the Ryzen**; it is the Claude/remote API. The
evolutionary search loop (selection, mutation dispatch, fitness evaluation) runs locally and is
cheap. This is the correct architecture for Jarvis: evolutionary harness local, LLM remote and
called sparingly.

**What is GPU-bound and therefore OUT for Jarvis's local substrate:**
- Running Lenia at scale with JAX GPU acceleration
- Training neural cellular automata end-to-end
- Running any LLM locally (even quantized 7B models push 16 GB RAM when evolution populations
  require batched inference)
- Population-level parallel GP with GPU evaluators (Beagle framework etc.)

**What runs fine on the Ryzen:**
- DEAP GP trees with Python fitness functions
- PyGAD + pyribs for parameter optimization and QD
- CMA-ES via `cmaes` library
- Simple CA evolution (rule search over 256 elementary CA rules — trivial)
- ACO/PSO for combinatorial sub-problems
- The evolutionary loop of OpenEvolve/GEAR with the LLM calls going to Claude API

### 7c. Jarvis mapping

GEAR is the closest existing system to what Jarvis's TRP loop already does manually. The
difference: TRP runs once per session, driven by Will and JARVIS together; GEAR runs automatically,
maintains a population of search states, and discovers that maintaining population diversity
continues finding improvements long after a single-incumbent run converges.

The TRP → GEAR upgrade path:
1. Represent each candidate Jarvis component derivation as a GEAR node (code + reflection + perf stats)
2. Replace the single-thread TRP with GEAR-Fixed: bounded population of component candidates
3. Fitness = (WAL error rate reduction) + (session token reduction) on held-out sessions
4. Run GEAR-Evolve eventually: let the search controller itself become mutable

---

## 8. Self-Organizing Systems — the Model, Not the Algorithm

### 8a. What self-organization actually means

Self-organization: a system displays ordered spatiotemporal patterns **solely from component
interactions**, without a central controller specifying the global pattern. This is a mechanistic
claim, not a hand-wave. The conditions for self-organization in the ALife literature are:
- Local interaction rules
- Positive feedback (reinforcement of patterns that emerge)
- Negative feedback (suppression preventing runaway reinforcement)
- Multiple stable attractors

ALife 2025's theme was "Exploration of emergence in complex systems." The practical output of ALife
research for engineered systems is less "build an emergent system" and more "design local rules that
produce desired global behavior."

### 8b. Honest flag on "emergence" claims for Jarvis

"Many small gates yield system-level intelligence" is an attractive framing but needs
qualification:
- **True claim:** the Jarvis harness exhibits behavior not pre-specified by any single hook —
  session context, memory coherence, and error prevention arise from gate interactions.
- **Unverified claim:** that this constitutes "intelligence" in any strong sense vs. a well-tuned
  rule system.
- **False claim to avoid:** that Jarvis is "self-organizing" in the Lenia/Game-of-Life sense
  without measuring whether gate interactions are actually in Wolfram Class 4.

The self-organization literature's useful contribution is the **design principle**: local + modular
+ composable > centralized. Jarvis already applies this. The evolutionary computation tools above
are ways to *search* for local rules that produce good global behavior — which is concrete and
actionable, not metaphorical.

---

## 9. Top 3 Adoptable-for-Jarvis (CPU-Only Sketches)

### #1 — GP over the Gate Population (DEAP + WAL fitness)

**Why first:** Directly implements the TRP loop's intent. The loop currently requires Will + JARVIS
to manually identify bottlenecks and derive primitives. GP automates the derivation step with a
measurable fitness function from existing logs.

**Mechanism:** DEAP primitive tree GP, where terminals are WAL/memory read operations and
primitives are predicate combiners. Fitness = precision on WAL replay dataset (error caught /
(error caught + false trigger)).

**CPU sketch:**
```python
# DEAP setup (condensed)
import operator
from deap import base, creator, gp, tools, algorithms

# Terminals: reads from session state
pset = gp.PrimitiveSet("GATE", arity=0)
pset.addPrimitive(operator.and_, 2)
pset.addPrimitive(operator.or_, 2)
pset.addPrimitive(operator.not_, 1)
pset.addTerminal(lambda: read_wal("token_delta") > 5000, "high_tokens")
pset.addTerminal(lambda: read_wal("error_type") == "memory_drift", "mem_drift")
# ... add ~10-20 domain terminals from WAL schema

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=4)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate_gate_on_wal_replay)   # user-supplied
toolbox.register("select", tools.selDoubleTournament, fitness_size=5, parsimony_size=1.4,
                 fitness_first=True)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr, pset=pset)
toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=8))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=8))

# Multiprocessing — uses all 6/12 Ryzen cores
import multiprocessing
pool = multiprocessing.Pool()
toolbox.register("map", pool.map)

pop, log = algorithms.eaSimple(toolbox.population(n=300), toolbox,
                                cxpb=0.7, mutpb=0.3, ngen=50, verbose=True)
```

**Dependencies:** `deap` only (+ numpy, stdlib). RAM: <1 GB for this population size.  
**Output:** evolved gate program as a Python expression tree, directly serializable to a hook.

---

### #2 — MAP-Elites Primitive Archive (pyribs + behavior descriptors)

**Why second:** Solves the monoculture problem. The current TRP loop produces components in a
serial, bottleneck-driven sequence. MAP-Elites maintains a **diverse population across behavioral
niches simultaneously**, so the gate archive covers all error categories rather than converging
on one dominant type.

**Mechanism:** pyribs GridArchive with behavior descriptor = (error_category_index,
session_phase). Emitter generates parameter variations of gate threshold settings; fitness =
precision on WAL replay for that gate variant.

**CPU sketch:**
```python
import ribs
import numpy as np

N_ERROR_CATS = 8   # memory_drift, token_waste, api_boundary, etc.
N_PHASES = 4       # boot, mid-session, tool-call, stop

archive = ribs.archives.GridArchive(
    solution_dim=10,          # 10 tunable threshold params per gate
    dims=[N_ERROR_CATS, N_PHASES],
    ranges=[(0, N_ERROR_CATS), (0, N_PHASES)],
)
emitter = ribs.emitters.GaussianEmitter(
    archive, x0=np.zeros(10), sigma=0.1, batch_size=32
)
scheduler = ribs.schedulers.Scheduler(archive, [emitter])

for iteration in range(500):
    solutions = scheduler.ask()
    # evaluate each gate configuration on WAL replay; return
    # (objective_score, [error_cat_index, phase_index]) per solution
    objs, measures = batch_evaluate_on_wal(solutions)
    scheduler.tell(objs, measures)

# Result: archive.data() gives the best gate per (error_cat, phase) niche
```

**Dependencies:** `ribs` (numpy-based, CPU only, explicitly single-threaded).  
**RAM:** negligible — archive stores floats, not programs. 100×100 grid = 40 KB.  
**Integration:** run after GP produces candidate gate programs; MAP-Elites finds the best
threshold setting for each gate across all niches.

---

### #3 — GEAR-style Population Search for TRP Component Derivation

**Why third:** The TRP loop is the most expensive manual operation in the Jarvis harness —
it requires Will + JARVIS to co-derive new components. GEAR's insight is that replacing single-
incumbent search with a bounded elite population + diversity pressure finds improvements much
longer. This maps directly onto TRP.

**Mechanism:** Implement GEAR-Fixed locally in Python. Each "individual" is a component derivation
state: (candidate_primitive_code, reflection_notes, WAL_performance_stats). Selection uses a
composite score: productivity_estimate × local_novelty × global_coverage_bonus. Variation:
LLM mutation (Claude API call with parent primitive + fitness signal in context). Evaluation:
replay on WAL slice. Population bound: 10-20 elites (cheap; each is a text + code artifact).

**CPU sketch (pseudocode — the LLM calls are the expensive part, not the search):**
```python
class GearNode:
    code: str            # Python callable implementing the candidate gate
    reflection: str      # LLM-generated notes on why this variant was proposed
    precision: float     # measured on WAL replay
    coverage: float      # fraction of error categories it catches
    novelty: float       # edit distance from other elites (Levenshtein)

def composite_score(node, archive):
    return node.precision * node.novelty * coverage_bonus(node, archive)

def gear_step(population, wal_replay_data):
    scores = [composite_score(n, population) for n in population]
    parents = select_top_k(population, scores, k=2)
    # LLM crossover: "here are two gate implementations; propose a variant combining their strengths"
    child_code = claude_mutate(parents[0].code, parents[1].code, parents[0].reflection)
    child_precision, child_coverage = evaluate_on_wal(child_code, wal_replay_data)
    child_novelty = min(levenshtein(child_code, n.code) for n in population) / MAX_DIST
    child = GearNode(child_code, ..., child_precision, child_coverage, child_novelty)
    # Replace weakest member if child improves
    if composite_score(child, population) > min(scores):
        population[np.argmin(scores)] = child
    return population

# Main loop (run during TRP, Will-approved)
population = [GearNode(gate) for gate in current_primitive_set]
for _ in range(50):   # 50 LLM calls per TRP session = ~$0.50 at Sonnet pricing
    population = gear_step(population, load_wal_replay())
emit_top_candidates(population)   # Will reviews and approves
```

**Dependencies:** stdlib + whatever WAL reader already exists. LLM calls go to Claude API (remote).  
**RAM:** trivially small — population is a list of text strings.  
**Token budget:** 50 LLM calls × ~1000 tokens = 50K tokens per TRP run. Cheap.

---

## Summary and Verdict

| Paradigm | Laptop-safe? | Honest maturity | Jarvis mapping | Priority |
|---|---|---|---|---|
| GP (DEAP) | Yes | High — DEAP 1.4.4, actively maintained | Evolve gate programs; automate TRP derivation | **HIGH** |
| GA (PyGAD) | Yes | High — 3.7.0 June 2026 | Tune hook thresholds; evolve hook activation mask | Medium |
| ES / CMA-ES | Yes | Very high — `cmaes`, pymoo, Optuna | Continuous threshold optimization; noisy fitness | Medium |
| MAP-Elites / QD (pyribs) | Yes | High — 0.11.0, CPU-only by design | Diverse primitive archive; prevent monoculture | **HIGH** |
| GEAR / ELM | Yes (loop local; LLM remote) | Active 2025-2026 research; no stable release | Automated TRP population search | **HIGH** |
| Cellular Automata | Yes (small grids) | Mature (numpy); Lenia needs JAX GPU at scale | Design intuition only; small-scale rule evolution | Low |
| Swarm (ACO/PSO) | Yes | Mature; limited Jarvis relevance vs. GA/CMA-ES | Session scheduling; combinatorial sub-problems | Low |
| ALife / Emergence | Partially (Lenia at scale = GPU) | Research-grade; ASAL 2024, ALife 2025 active | Design philosophy; emergent-harness framing | Conceptual |

**Honest conclusion on "intelligence as emergence":** this is a concrete algorithm design principle
(keep gates local, composable, non-centralized; measure whether the system maintains diverse
behavior rather than converging to silence or chaos) — not a magical property. The evolutionary
computation tools above are the operationalization: they search for local rules that produce good
global behavior, which is the actual technical task. The "emergence" framing is useful as design
intuition but must not be used to justify skipping measurement.

**The single most valuable insight for Jarvis:** the TRP self-improvement loop already exists — it
just runs manually and serially. GP + MAP-Elites + GEAR together constitute an automated,
population-based, diversity-maintaining version of that same loop with a measurable fitness
function from the existing WAL logs. None of it requires a GPU. All of it runs on the Ryzen.

---

## Sources

- [DEAP PyPI](https://pypi.org/project/deap/)
- [DEAP GP documentation](https://deap.readthedocs.io/en/master/tutorials/advanced/gp.html)
- [PyGAD PyPI](https://pypi.org/project/pygad/)
- [PyGAD documentation](https://pygad.readthedocs.io/en/latest/)
- [pyribs paper (arXiv)](https://arxiv.org/abs/2303.00191)
- [pyribs stable docs](https://docs.pyribs.org/en/stable/)
- [pyribs GitHub](https://github.com/icaros-usc/pyribs)
- [pymap_elites (reference MAP-Elites)](https://github.com/resibots/pymap_elites)
- [MAP-Elites GitHub topic (Python)](https://github.com/topics/map-elites?l=python)
- [cmaes Python library (arXiv)](https://arxiv.org/abs/2402.01373)
- [cmaes GitHub](https://github.com/CyberAgentAILab/cmaes)
- [CMA-ES official site](https://cma-es.github.io/)
- [OpenEvolve (AlphaEvolve open-source)](https://github.com/algorithmicsuperintelligence/openevolve)
- [CodeEvolve (arXiv)](https://arxiv.org/html/2510.14150v1)
- [GEAR: Genetic AutoResearch (arXiv)](https://arxiv.org/abs/2605.13874)
- [AlphaEvolve (DeepMind PDF)](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/AlphaEvolve.pdf)
- [LLM Guided Evolution (ACM GECCO)](https://dl.acm.org/doi/10.1145/3638529.3654178)
- [CAX: Cellular Automata in JAX (arXiv)](https://arxiv.org/html/2410.02651)
- [Lenia and Expanded Universe (arXiv)](https://ar5iv.labs.arxiv.org/html/2005.03742)
- [ALife 2025 Conference](https://2025.alife.org/program)
- [Automating the Search for ALife with Foundation Models (Sakana AI)](https://sakana.ai/asal/)
- [DataCamp: Swarm Intelligence Python](https://www.datacamp.com/tutorial/swarm-intelligence)
- [Novelty Search: Abandoning Objectives (Evolutionary Computation)](https://dl.acm.org/doi/10.1162/EVCO_a_00025)
- [digneapy PyPI](https://pypi.org/project/digneapy/)
- [Darwin Godel Machine (arXiv 2025)](https://arxiv.org/pdf/2505.22954)
- [CMA-ES with RBF Surrogate 2025 (arXiv)](https://arxiv.org/abs/2505.16127)
- [GPU-Accelerated GP (Beagle, arXiv)](https://arxiv.org/pdf/2603.12292)
