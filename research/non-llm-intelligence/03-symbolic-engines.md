# 03 — Symbolic Reasoning Engines

**Cluster:** Logic programming · SAT/SMT solvers · Automated theorem provers · Classical planners ·
Constraint solvers · Inductive Logic Programming · Program synthesis

**Written:** 2026-07-16 · **Laptop-test hard constraint:** <16 GB RAM, CPU-only, commodity hardware

---

## Why This Cluster Is Different

Symbolic engines are not research prototypes. They are deployed production infrastructure — Z3 runs
inside Azure and AWS access-control systems; Datalog/ASP underpin database engines and knowledge
graphs at LinkedIn scale; PDDL planners schedule satellites and logistics fleets. The question is not
"is this mature?" (it is, deeply) but "what is the right cut-plane between LLM and solver?"

The answer has a name: **"LLM proposes, solver disposes."** The LLM does what it does well — parsing
natural language, generating candidate formal specs, recovering from syntax errors, explaining outputs.
The solver does what it does well — exhaustive search over a formally-defined space, returning
sound/complete results with certificates of correctness. Neither side does the other's job. The two are
wired together by a thin translation layer and a self-refinement loop.

For Jarvis specifically, the killer application is not general reasoning — it is **turning the existing
prose memory-graph into a queryable inference substrate** without a rewrite. Every primitive, gate,
circuit, and wikilink already encodes logical structure. That structure is currently re-read prose. A
Datalog/ASP compilation layer could make it computable: transitive reachability, conflict detection,
entailment — for free, once the encoding exists.

---

## Section 1 — Logic Programming: Prolog, Datalog, ASP/clingo

### 1.1 Prolog (SWI-Prolog)

**Mechanism.** Prolog is a resolution-based logic programming language: facts and rules define a
knowledge base; queries trigger SLD resolution, depth-first search with backtracking, returning all
unifications that satisfy the query. If a derivation exists, Prolog finds it (completeness depends on
search strategy and the absence of left-recursion). It handles Horn clauses over arbitrary first-order
terms.

**Maturity / tooling.** SWI-Prolog is the production standard — actively maintained, multi-threaded,
JIT-compiled, with bindings to C, Java, Python, and Rust. Python bridge: `pyswip` (`pip install
pyswip`). Exposes `Prolog.consult("kb.pl")` and `Prolog.query("parent(X, Y)")`. Also has a WebAssembly
port (SWISH) for browser use. The TPTP library provides thousands of benchmark problems. Wikidata as of 2025 contains 1.65B item-level statements (the full RDF triple count is 16–20B);
researchers have demonstrated encoding Wikidata subsets as Prolog facts for specific domains, though
full-scale Prolog KB encoding of all of Wikidata is not standard practice. Pi-CoT (2025 arXiv) uses
Prolog KBs as a multi-hop QA scaffold for LLMs.

**LLM integration.** LLM translates NL query to Prolog goal → Prolog KB returns binding set →
LLM re-verbalizes. Self-refinement: Prolog syntax errors returned as feedback prompts; LLM retries.
Pi-CoT (2025) showed structured Prolog init improves multi-hop QA substantially vs. chain-of-thought
alone.

**Jarvis mapping.** Prolog is expressive but operationally awkward for a Python harness: pyswip is a
thin C-bridge with limited error recovery, and Prolog's depth-first left-to-right search misbehaves on
left-recursive rules (which Datalog handles natively). Prolog is best for problems that need full
first-order terms and complex backtracking. For Jarvis's flat-ish memory graph, Datalog is a strictly
better fit (see 1.2). Prolog is useful as a fast prototyping language for encoding game rules, process
logic, or planning sub-problems. **Adoption tier: secondary / backup substrate if Datalog proves
insufficient.**

**Laptop test:** passes easily. SWI-Prolog is CPU-native; pyswip runs fine on 16GB.

---

### 1.2 Datalog

**Mechanism.** Datalog is the *stratified* subset of Prolog restricted to: no function symbols (only
relations), no negation-as-failure beyond stratified negation, and guaranteed termination. The result:
Datalog programs always terminate, support set semantics (no duplicate derivations), and compute the
*minimal fixed point* of the rule set over the given facts. The canonical algorithms (semi-naive
bottom-up evaluation) are polynomial in the size of the input relations.

Core power for Jarvis: **transitive closure in O(n²) worst-case**, which means "all nodes reachable
from node X via wikilinks" is a single Datalog rule. Similarly, "all primitives in conflict with
primitive P" is a rule over a `conflicts_with` relation.

**Maturity / tooling.**

- `pyDatalog` (`pip install pyDatalog`) — pure Python, runs embedded, no native dependency. Ideal for
  prototyping. Support restarted June 2026. Declarative syntax in Python strings.
- **Soufflé** — high-performance C++ Datalog engine, synthesizes parallel C++ from Datalog specs.
  Used at industrial scale for program analysis. Latest release: v2.5 (March 2025). Invocable via
  subprocess (CLI: `souffle program.dl`) or via SWIG-based Python bindings that require building
  from source with `cmake -DSOUFFLE_SWIG_PYTHON=ON` — not a pip install. Subprocess is the practical
  path for Jarvis. For Jarvis's memory graph (hundreds to low thousands of primitives) Soufflé is
  overkill; start with pyDatalog and migrate only if query latency becomes measurable.
- **Vadalog / Warded Datalog±** — extends Datalog with existential quantifiers for knowledge-graph
  completions; used in production finance/compliance pipelines. More complex; not needed for Jarvis
  MVP.

**LLM integration.** LLM translates NL rule description ("all primitives downstream of X") to a
Datalog rule string; pyDatalog or Soufflé evaluates; result returned to LLM or upstream gate. 2024
arXiv paper (Meta LLaMA 3 + clingo) demonstrated LLM→Datalog translation with structured prompt
engineering and domain-specific knowledge injection; adapted to Datalog facts for recipe recommendation
but the pattern is generic.

**The Jarvis Memory-Graph compilation angle (see Section 8 for full sketch).** This is the load-bearing
application. Today's primitives are prose markdown files with wikilinks. If each primitive is compiled
to a Datalog fact `primitive("P·structure-does-the-work", "axis", "meta")`, each wikilink to
`links("P·structure-does-the-work", "P·economic-theory-of-mind")`, and each conflict annotation to
`conflicts("X", "Y")`, then Jarvis can *compute* rather than re-read:
- Transitive closure of dependency graph
- Conflict detection (which primitives mutually contradict?)
- Entailment: given primitive set S is loaded, what else is entailed?
- Reachability: all primitives reachable from a given SessionStart context

**Adoption tier: TOP 1 for immediate Jarvis integration.**

**Laptop test:** passes trivially. pyDatalog is pure Python. Soufflé is CPU-only C++.

---

### 1.3 Answer Set Programming — clingo

**Mechanism.** ASP generalizes Datalog with: (a) default negation (not just stratified negation),
(b) disjunction in rule heads, (c) optimization (`#minimize`, `#maximize`), (d) aggregates, (e)
cardinality constraints. The solver computes *stable models* — minimal sets of true atoms consistent
with the rules. Multiple stable models = multiple valid worlds; the solver enumerates all or finds
optimal ones. This gives ASP the expressive power to handle inconsistency, incomplete knowledge, and
combinatorial choice problems that pure Datalog cannot.

For Jarvis: ASP can express "find the set of primitives that should fire given current state, subject
to the constraint that no two conflicting primitives fire simultaneously" — this is exactly the
constraint optimization that the WWWD gate currently approximates by re-reading prose.

**Maturity / tooling.** `clingo` (Potassco, Potsdam) is the production standard. `pip install clingo`
gives the official Python API. `clorm` provides an ORM-style interface (Python dataclasses ↔ ASP
atoms), making bidirectional marshalling clean. `clyngor` is a simpler wrapper. clingo is deeply
mature: dominant winner of the International ASP Competition (separate from CASC, which is for
first-order theorem provers), used in industrial scheduling, bioinformatics, robotics. Hybrid
extensions: `clingcon` (constraint arithmetic), `clingo[dl]` (difference logic), `clingo[lp]` (linear
programming). Interactive ASP KB shell: `aspic` (Python + clingo) lets you dynamically load/retract
facts and query in a REPL — directly analogous to what Jarvis needs.

**LLM integration.** The 2024 CEUR-WS paper (LLaMA 3 70B + clingo Python API) demonstrated a full
pipeline: user NL input → LLM encodes as Datalog/ASP facts (e.g., ingredient preferences) using
predefined predicates → clingo solves → LLM verbalizes results. The predicate vocabulary is
domain-specific and declared in the prompt; the LLM only fills in instantiations. Error feedback loop:
clingo parse/grounding errors returned to LLM for correction; 5-retry ceiling.

**Jarvis mapping.** ASP subsumes Datalog for the memory-graph use case AND adds the ability to detect
inconsistent primitive sets and compute maximally consistent subsets. The gate architecture maps
naturally: each hook invocation asserts new facts into the ASP context; the stable model tells the
hook what the consistent state is. This is more powerful than Datalog-only but carries more complexity
(stable model semantics is non-monotonic, so debugging is harder). Recommended path: start with
Datalog (simpler, monotone, always terminable), escalate to ASP when you need choice rules or
non-monotone reasoning.

**Adoption tier: TOP 2, after Datalog is established.**

**Laptop test:** passes. clingo is CPU-native, runs in seconds on problem instances up to tens of
thousands of atoms.

---

## Section 2 — SAT and SMT Solvers (Z3, cvc5)

### 2.1 Z3 (Microsoft Research)

**Mechanism.** Z3 is a Satisfiability Modulo Theories (SMT) solver. It takes a formula over a mixture
of theories — linear arithmetic, bitvectors, arrays, strings, uninterpreted functions — and returns
either `sat` (with a model: a concrete assignment) or `unsat` (with a proof/counterexample). SMT
extends pure Boolean SAT with domain-specific decision procedures, making it dramatically more
expressive than a SAT solver alone.

The verification pattern: encode the *negation* of the desired property. If the solver returns `unsat`,
no counterexample exists — the property is proven. If it returns `sat`, the model is a concrete
violation.

**Maturity / tooling.** `pip install z3-solver`. Most recent release: Feb 2026. MIT license. The
Python API (`z3.py`) is first-class — Microsoft uses it internally in Azure network analysis and AWS
Zelkova uses it for IAM policy verification. The API lets you build formula trees programmatically:
`z3.Int("x")`, `z3.And(x > 0, x < 10)`, `solver.check()`. Error feedback: the solver returns a
counterexample model when `sat` on a negated property, which can be re-fed to the LLM.

The "SMT-LLM" system (2025, arXiv 2605.11772) solved 83.6% of Python dependency snippets by
combining Z3 constraint solving with LLM imputation, vs. 54.8% for the pure-LLM baseline (PLLM) —
a 29 percentage-point / ~53% relative improvement — with 11x fewer LLM calls per snippet and 6.3x
faster median resolution time.

**LLM integration.** The canonical pattern from 2025 research: LLM generates Z3 Python code
(variable declarations + constraint expressions); Python executes; `check()` returns `sat/unsat/unknown`
plus a model or proof. On error, the error string is fed back; up to 5 retries. The LLM only needs to
generate the *declarative component* (variables, constraints) — the search is the pre-defined
`solver.check()` call. Adaptive routing systems now classify sub-problems to route to Z3 vs. FOL
provers vs. CP solvers dynamically.

**Jarvis mapping.** Three concrete applications:

1. **Gate pre-condition checking.** Before executing a high-stakes tool call, encode pre-conditions
   as Z3 constraints over the current state (tool arguments, memory state). `check()` verifies
   consistency. If `unsat`, the gate blocks with a sound reason.

2. **Decision consistency.** The WWWD gate currently reasons in prose. A Z3 encoding of the
   decision rules (if X and Y, then action Z) makes the reasoning *checkable* — not just plausible.

3. **Constraint-driven config.** Settings conflicts ("allow X but never allow Y") are naturally Z3
   constraints. The solver detects contradictions in settings.json before they cause runtime errors.

**Adoption tier: TOP 3. Easiest to integrate today — one pip install, Python-native API, no external
process.**

**Laptop test:** passes. Z3 is CPU-native, runs on commodity hardware. Problems at Jarvis scale
(dozens to hundreds of constraints) resolve in milliseconds.

---

### 2.2 cvc5

**Mechanism.** cvc5 is the successor to CVC4. Covers the same theory landscape as Z3 with
competitive/sometimes better performance on quantified formulas and string theory. Also returns proofs
in formats consumable by external checkers. Python bindings (`pip install cvc5`) are first-class since
2022.

**Honest assessment for Jarvis.** cvc5 is a strong solver and the proof output is better than Z3's
for formal verification pipelines. However, Z3's Python API is more mature, better documented, and
more widely used in the LLM+solver integration literature. For Jarvis, Z3 is the right default; cvc5
is the fallback if Z3 returns `unknown` on a specific problem class.

---

## Section 3 — Automated Theorem Provers (Lean 4, Vampire, E)

### 3.1 Lean 4

**Mechanism.** Lean 4 is a dependently-typed functional programming language and interactive proof
assistant. Proofs are programs; the type checker is the proof checker. Lean's Mathlib library contains
~60,000 formalized mathematical theorems. The interactive mode provides a proof state at every tactic
step — the current goal, available hypotheses, and what remains to prove.

**Maturity / tooling.** Lean 4 is production-grade and actively developed. The ecosystem has exploded
in 2024–2025: LeanDojo (proof state retrieval + Mathlib search), Lean Copilot (LLM-assisted tactic
suggestion inline), APOLLO (automated LLM+Lean collaboration), DeepSeek-Prover-V2, BFS-Prover. The
reinforcement-learning proof synthesis paper in *Nature* 2025 is the clearest signal that
LLM+interactive-prover is a real, working architecture.

**LLM integration.** The tactic-generation loop: LLM proposes next Lean 4 tactic → Lean type-checks
it → either returns new proof state (success) or error (retry). BFS/MCTS guides the search tree.
Alternatively, whole-proof generation: LLM emits full Lean proof; Lean validates all at once. Error
messages from Lean are highly structured and informative; they feed well into LLM correction.

**Honest assessment for Jarvis.** Lean 4 is magnificent for formal mathematics and software
verification — but it is *heavy*. The Mathlib compilation takes hours on cold build; the proof
language is complex; and the class of problems Jarvis needs to reason about (memory-graph consistency,
gate pre-conditions, decision logic) is not mathematical in the Lean sense. Lean is the right tool if
Jarvis eventually needs to *certify* that a protocol is correct (e.g., the canonical messaging spec in
VibeSwap). It is the wrong tool for everyday gate logic.

**Adoption tier: aspirational / specialized. Not for this month. Tag for VibeSwap contract
verification.**

**Laptop test:** marginal. Lean 4 itself is CPU-native but Mathlib warm-up is RAM-intensive. On 16GB
you can run Lean 4 on small custom theories without Mathlib. Workable but not comfortable.

---

### 3.2 Vampire and E (Saturation-Based First-Order Provers)

**Mechanism.** Vampire (Manchester) and E (Munich) are saturation-based theorem provers for full
first-order logic (FOL) with equality. They implement the *superposition calculus*: given axioms and
the negation of the goal, they derive logical consequences until they derive a contradiction (proof) or
exhaust the search space (refutation). Vampire has won at least 53 CASC trophies across multiple divisions (FOF, TFA, and others) since
1999 — note these are division trophies per competition year, not 50+ annual overall wins.

**LLM integration.** The LINC framework (2023–2025) uses LLMs as semantic parsers translating NL
premises and conclusions to FOL, then offloads to Vampire/E for entailment checking. SatLM uses LLMs
to generate declarative task specifications fed to theorem provers. The key advantage over Z3: Vampire
and E handle *quantified* first-order logic natively, which Z3 can struggle with.

**Honest assessment for Jarvis.** Vampire/E are extremely powerful but the interface is purely
TPTP-format text files — no native Python API. Subprocess invocation is workable but awkward. For the
problems Jarvis faces, Z3 handles quantifier-free fragments fine, and Datalog/ASP handle the
graph-reasoning problems. Vampire/E are most useful when Jarvis needs to check a *relational/logical*
property that cannot be expressed in Datalog or easily encoded in Z3 — e.g., "does this set of rules
entail a contradiction under all possible inputs?" at full FOL expressiveness.

**Adoption tier: secondary. Useful for specific deep reasoning tasks. Not for month-one integration.**

**Laptop test:** passes. Vampire and E are CPU-native C++ binaries that run on seconds-to-minutes per
problem at Jarvis scales.

---

## Section 4 — Classical Planners (PDDL / Fast Downward)

**Mechanism.** PDDL (Planning Domain Definition Language) separates *domain* (action types with
preconditions and effects) from *problem* (initial state + goal). Classical planners find a sequence
of action applications transforming the initial state to the goal. Fast Downward (C++) is the
state-of-the-art open-source planner, using heuristic search (A*, GBFS) guided by domain-derived
heuristics. Plans are *sound* (each action is applicable at its step) and *complete* (if a plan
exists, the planner finds it, given enough time).

**Maturity / tooling.** Fast Downward is production-quality, runs via Python subprocess, and has been
used to plan satellite operations and logistics. Pyperplan is a pure-Python educational planner —
simpler, slower, but zero native dependencies. LLM+PDDL pipelines are the most active research area
in LLM+classical-AI as of 2025: NL2Plan (LLM generates PDDL from NL → Fast Downward solves → 10/15
tasks), the NeurIPS 2025 LLM-heuristic paper, and a July 2025 benchmark showing classical planners
still outperform LLMs on complex resource-coordination tasks.

**LLM integration.** Two modes: (a) LLM generates PDDL domain/problem files from NL task description
→ planner executes; (b) LLM generates heuristic functions in Python → planner uses them. Mode (a) is
the reliable one — PDDL is declarative enough that LLMs generate it accurately with few-shot examples.
The plan is validated by VAL (the PDDL plan validator) for guaranteed executability before execution.
One study (arXiv 2305.14909) reports solving 48 challenging planning tasks across three domains using
LLM-generated PDDL + Fast Downward, after iterative LLM+validator correction loops; the paper does
not state a percentage of a larger task set, so "95%" figures cited in summaries of this work cannot
be confirmed from the abstract and should not be relied on.

**Jarvis mapping.** The most natural application: **multi-step autopilot planning.** When Jarvis
enters autopilot mode and must execute a 10-step protocol, encoding the protocol actions as PDDL
operators and the current session state as the initial state would let Fast Downward generate an
*optimal ordered plan* — rather than hoping the LLM sequences the steps correctly. Gates become PDDL
preconditions; actions become PDDL operators with defined effects on the state. The LLM's role: NL
goal → PDDL problem file.

**Honest assessment.** PDDL is powerful but the modeling cost is real. Writing a PDDL domain for
Jarvis's protocols requires upfront encoding effort (2–4 days of careful work). Once encoded, the
planner handles all future protocol executions soundly. This is a medium-term investment, not a
week-one task.

**Adoption tier: medium-term. Not month-one. Tag for autopilot and multi-step protocol encoding.**

**Laptop test:** passes solidly. Fast Downward is CPU-native; runs in seconds to low minutes on
problems at Jarvis scale (tens of actions, hundreds of state variables).

---

## Section 5 — Constraint Programming (OR-Tools / MiniZinc)

**Mechanism.** Constraint Programming (CP) models a problem as a set of decision variables, each with
a domain, and a set of constraints over those variables. The solver searches for assignments satisfying
all constraints, using constraint propagation to prune the search space, often combined with
backtracking. OR-Tools (Google) CP-SAT is a hybrid CP/SAT solver that outperforms pure CP systems on
many scheduling and assignment problems. MiniZinc is a solver-agnostic modeling language that compiles
to OR-Tools, Chuffed, and others.

**Maturity / tooling.** `pip install ortools` — production-grade, used in Google's internal vehicle
routing and fleet optimization (it is Google's in-house solver; the specific "Google Flights" branding
is not confirmed in OR-Tools documentation — that claim appears in summaries but not in Google's own
OR-Tools writeups), and in industrial scheduling broadly. Python API is first-class. MiniZinc Python wrapper available. OR-Tools
CP-SAT won the yearly MiniZinc challenge multiple years. PyCSP3 provides XCSP3-format CP modeling in
Python with OR-Tools backend. The ConstraintLLM paper (2025) demonstrated a neuro-symbolic framework
for industrial-level CP using LLMs to generate constraint models.

**LLM integration.** LLM generates MiniZinc model or OR-Tools constraint code from NL specification
→ solver returns optimal assignment or `INFEASIBLE`. LLMs handle the model generation step; OR-Tools
handles the combinatorial search. The Gala system (2025) demonstrated global LLM agents for
text-to-model translation for CP problems.

**Jarvis mapping.** CP is most valuable for **resource allocation and scheduling**: which subagents to
run in parallel given a RAM budget; how to schedule forge test runs under the 3-concurrent-process
limit; which primitives to load given a token-budget constraint. These are exactly the problems that
currently require manual configuration or LLM guessing. OR-Tools makes them solvable in <1ms.

**Adoption tier: solid second-tier.** Less urgent than Datalog/Z3 but high-value for the scheduling
problems Jarvis already has. OR-Tools is the easiest pick — pure pip install, no subprocess.

**Laptop test:** passes. OR-Tools is CPU-native, designed for production scheduling on commodity
hardware.

---

## Section 6 — Inductive Logic Programming (Popper, Metagol)

**Mechanism.** ILP learns logic programs (rules) from examples + background knowledge. Given positive
examples (what the rule should explain), negative examples (what it should not), and a background
knowledge base of facts, ILP systems find the shortest logic program that is consistent with all
examples and entails all positives. The hypothesis space is the space of logic programs; search is
guided by the language bias (what predicate/arity combinations are allowed).

Popper (Cropper, 2021+) encodes the search as an ASP problem — the outer loop uses clingo to
enumerate candidate programs and prune based on coverage. Metagol uses higher-order metarules to
drastically prune the search space, enabling learning of recursive programs from very few examples.

**Maturity / tooling.** Popper is actively maintained (last GitHub update Sept 2025), pip-installable,
and written in Python with clingo as backend. Metagol requires SWI-Prolog. Both are research-grade but
functional. Applied to ARC-AGI benchmark in 2025. Combined with DreamCoder for visual concept
learning.

**LLM integration.** ILP + LLM is an emerging combination: LLM generates the background knowledge and
metarule vocabulary; ILP searches for the program. The LLM proposes candidate predicate structures;
ILP validates and generalizes from examples.

**Honest assessment for Jarvis.** ILP is the right tool when Jarvis needs to *learn* rules from
observed behavior rather than have them written by hand. Example: if Jarvis has observed 50 cases of
"Will escalated to input-needed" and 50 cases of "Jarvis proceeded autonomously," ILP could induce a
rule predicting when escalation is appropriate. This is a powerful future capability but requires
accumulating labeled examples first. ILP also struggles with noisy real-world data.

**Adoption tier: future / aspirational. Valuable once there is a labeled behavioral dataset.
Not month-one.**

**Laptop test:** passes. Popper runs on CPU with clingo as backend.

---

## Section 7 — Program Synthesis (DreamCoder, Sketch)

**Mechanism.** Program synthesis generates a program satisfying a specification (input-output
examples, logical constraints, or natural language). DreamCoder (MIT, 2021) is the canonical
neuro-symbolic system: it alternates between "wake" (synthesize programs for current tasks via guided
search) and "sleep" (abstract common sub-programs into a growing library of primitives). The library
bootstraps future synthesis — concepts learned early become the vocabulary for harder concepts.

Sketch (Armando Solar-Lezama) is a syntax-directed synthesis system: you write a program with "holes"
and Sketch fills in the holes using SAT solving. More constrained than DreamCoder but more
controllable and faster.

**Maturity / tooling.** DreamCoder is research code (Python), not production-ready. Sketch is
available as an open-source tool. The 2025 program-synthesis-via-test-time-transduction paper extends
the approach to ARC-AGI. LILO (2023) adds LLM-guided library learning on top of DreamCoder's
wake-sleep loop.

**Honest assessment for Jarvis.** Program synthesis is the long-game play: Jarvis accumulates
primitive usage patterns; synthesis induces new primitives. This is deeply aligned with the Cave
philosophy and TRP (deriving new substrate components from real bottlenecks). But DreamCoder needs a
well-defined domain language and many training examples to bootstrap. It is not a drop-in.

**Adoption tier: aspirational / long-term. Watch LILO+DreamCoder for LLM-guided library learning.
Not this year.**

**Laptop test:** marginal. DreamCoder's search can be GPU-accelerated but runs on CPU. Slow for
complex domains.

---

## Section 8 — The Killer Application: Compiling Jarvis's Memory-Graph to Datalog

This is the most concrete and immediately buildable integration. Here is a complete sketch.

### Current state

Jarvis's memory graph is ~200+ markdown files, each a "primitive" with wikilinks to other primitives.
Every session, the preprocessor hook reads a subset of these and injects prose into context. Inference
over the graph (e.g., "all primitives downstream of P·structure-does-the-work") requires the LLM to
re-read and re-reason — expensive, lossy, slow.

### The Datalog layer (buildable in <1 week)

**Step 1: Parser (1 day).** Write a Python script that reads all `.md` files in
`vibeswap/.claude/memory/`, extracts:
- Primitive ID from filename: `primitive_structure-does-the-work.md` → `"P·structure-does-the-work"`
- Tags/axes from HIERO header (regex over the first few lines)
- Wikilinks: `[[P·economic-theory-of-mind]]` → outbound edge
- Explicit conflict annotations: `✗` adjacent to another primitive ID

Emits:
```prolog
primitive("P·structure-does-the-work", "axis2-implementation").
links("P·structure-does-the-work", "P·economic-theory-of-mind").
links("P·structure-does-the-work", "P·bottleneck-dissolution").
conflicts("P·always-equals-gate", "P·memory-suggestion-for-always").
```

**Step 2: Rules (0.5 days).**
```prolog
% Transitive reachability (what does loading X pull in?)
reachable(X, Y) :- links(X, Y).
reachable(X, Z) :- links(X, Y), reachable(Y, Z).

% Conflict propagation (if X conflicts with Y and Z entails X...)
indirect_conflict(A, B) :- reachable(A, X), conflicts(X, B).

% Context budget: given a set of loaded primitives, what is implicitly entailed?
entailed(X) :- loaded(Y), reachable(Y, X).

% Orphan detection: primitives with no inbound links (review candidates)
orphan(X) :- primitive(X, _), \+ links(_, X).
```

**Step 3: Python query interface (0.5 days).**
```python
from pyDatalog import pyDatalog

def load_memory_graph(memory_dir: str):
    """Parse all primitives and assert facts into pyDatalog."""
    # ... parse loop ...
    pyDatalog.assert_fact("primitive", prim_id, axis)
    pyDatalog.assert_fact("links", src, dst)

def reachable_from(prim_id: str) -> list[str]:
    X = pyDatalog.Variable()
    return [x for x in pyDatalog.ask(f"reachable('{prim_id}', X)")]

def find_conflicts(loaded_set: list[str]) -> list[tuple]:
    # assert loaded/1 facts, query indirect_conflict
    ...
```

**Step 4: Hook integration (0.5 days).** The `memory-preprocessor.py` SessionStart hook currently
reads files and builds prose context. After Datalog layer is built:
1. On boot, call `load_memory_graph()` — takes <1s for 200 primitives.
2. Compute `reachable_from("P·wwwd")` to determine which primitives the session needs.
3. Check `find_conflicts(session_loaded_set)` — if any conflicts, emit a warning primitive.
4. Only read prose for the computed reachable set, not all 200 files.

This reduces context injection from "dump all hot primitives as prose" to "inject only what the
dependency graph says is needed, with conflict-free guarantee."

### What this is NOT

This is not a replacement for the LLM. The LLM still reads the prose primitives it needs. The Datalog
layer handles the *structural* reasoning over the graph — reachability, conflicts, entailment —
that the LLM currently approximates by re-reading. The LLM remains the semantic reasoner; Datalog is
the graph engine.

### Scaling path

Start with pyDatalog (pure Python, zero dependencies, adequate for 200-2000 primitives). If the
memory graph grows to 10,000+ nodes or query latency becomes perceptible, migrate to Soufflé (compile
the same Datalog program, get native parallel C++ evaluation at microsecond latency).

---

## Section 9 — Top 3 Adoptable-for-Jarvis, Ranked

### Rank 1: Datalog (pyDatalog) — Memory-Graph Compiler

**Why now.** One pip install, pure Python, no subprocess, no native build. The problem it solves
(structural reasoning over the wikilink graph) is a *current bottleneck* — the SessionStart hook
re-reads prose in a linear scan. The implementation sketch above is complete enough to ship in 3 days.
Guarantees: termination, completeness, no hallucination in the graph traversal. Payoff: context budget
cuts (inject only entailed primitives), conflict detection before they cause reasoning errors, orphan
detection for memory hygiene.

**Integration point:** `memory-preprocessor.py` SessionStart hook.

**Risk:** Low. Monotone semantics, pure Python, easily swapped out if something better emerges.

---

### Rank 2: Z3 (z3-solver) — Gate Pre-condition Checker

**Why now.** One pip install, Python-native API, no external process. The problem it solves (verifying
that a proposed tool call or decision is consistent with declared constraints) is immediately valuable
for any gate where "is this action consistent with the current session state?" is the question.

Concrete first target: encode the settings.json permission rules as Z3 constraints. Before any
PreToolUse hook fires, assert the tool call as a Z3 formula and check() — if unsat, the gate has a
provably sound reason to block, not just a heuristic one. This is the formal backbone the WWWD gate
currently lacks.

Second target: the Foundry performance rules ("max 3 concurrent forge processes, never full suite
without --match-path") are naturally Z3 integer constraints over process counts and argument flags.
A gate that checks these before `forge test` invocations would be sound rather than pattern-matched.

**Integration point:** New `z3-gate.py` PreToolUse hook, called before Bash and forge commands.

**Risk:** Low. Z3's Python API is among the most mature in the symbolic AI ecosystem.

---

### Rank 3: OR-Tools (CP-SAT) — Subagent Scheduler

**Why now.** One pip install, Python-native, sub-millisecond on Jarvis-scale problems. The problem it
solves (how many subagents to run in parallel, how to schedule forge test runs under the 3-process RAM
constraint) is a current operational pain point that causes OOM failures and lost context.

Concrete first target: encode the Foundry performance rules as an OR-Tools CP-SAT problem:
```python
model = cp_model.CpModel()
# Variables: one per possible test run
runs = [model.NewBoolVar(f"run_{i}") for i in range(len(test_files))]
# Constraint: max 3 concurrent
model.Add(sum(runs) <= 3)
# Constraint: if via_ir, only 1 concurrent
model.Add(sum(via_ir_runs) <= 1)
# Objective: maximize coverage
model.Maximize(sum(runs))
solver.Solve(model)
```
This replaces the "at most 3, try not to OOM" heuristic with an optimal solution computed in
microseconds.

**Integration point:** Cron or autopilot scheduler; could also integrate into the forge test dispatch
logic.

**Risk:** Low. OR-Tools is Google's production scheduling library.

---

## Section 10 — What This Cluster Does NOT Do

Honest boundaries, to avoid overclaiming:

- **Symbolic engines do not understand meaning.** Datalog and ASP reason over *symbols*; the
  semantics of those symbols (what "P·structure-does-the-work" *means*) is not in the engine —
  it is in the prose that the LLM reads. The compiler sketch above only captures *structure*
  (graph topology, declared conflicts), not semantics. This is a feature: it is precisely the
  structural layer that the LLM handles badly (re-reading, approximating transitive closure),
  and symbolic engines handle well.

- **Classical planners do not replace deliberation.** Fast Downward finds optimal plans for formally
  specified problems but cannot specify the problem itself — that requires a human or LLM to write
  the PDDL. The modeling cost is real.

- **SMT solvers do not handle natural language.** Z3 can check that a formally stated constraint is
  consistent, but translating prose constraints into Z3 formulas requires LLM or manual encoding.
  The LLM-to-Z3 translation step introduces a new failure mode (malformed formulas) that the
  self-refinement loop must handle.

- **ILP and program synthesis are not drop-ins.** They need labeled example datasets that Jarvis
  does not yet have at scale. These are month-twelve tools, not month-one.

---

## References and Sources

- Potassco clingo: https://github.com/potassco/clingo | https://potassco.org/
- clorm ORM interface: https://github.com/potassco/clorm
- ASP + LLM paper (LLaMA 3 + clingo): https://ceur-ws.org/Vol-3876/paper3.pdf
- Hybrid ASP tutorial: https://www.cs.uni-potsdam.de/~torsten/hybris.pdf
- pyDatalog: https://pypi.org/project/pyDatalog/
- Vadalog / Datalog for knowledge graphs: https://arxiv.org/pdf/1807.08709
- Transitive relations efficiency (2025): https://arxiv.org/pdf/2504.21291
- z3-solver PyPI: https://pypi.org/project/z3-solver/
- Z3 RBAC analysis (Teleport): https://goteleport.com/blog/z3-rbac/
- FregeLogic hybrid neuro-symbolic (SemEval 2026): https://arxiv.org/pdf/2604.18328
- Reality check LLMs as formalizers: https://arxiv.org/pdf/2505.13252
- LLM proposes / solver disposes (emergentmind): https://www.emergentmind.com/topics/llms-with-symbolic-solvers
- Intermediate languages matter (2025): https://arxiv.org/pdf/2502.17216
- Novel architecture: symbolic reasoning + LLM agents (Aug 2025): https://arxiv.org/abs/2508.05311
- PDDL + Fast Downward vs LLMs benchmark (July 2025): https://arxiv.org/html/2507.23589v1
- NL2Plan: https://arxiv.org/pdf/2405.04215
- LLM-generated heuristics for classical planning (NeurIPS 2025): https://arxiv.org/html/2503.18809v2
- LLM world models → Fast Downward (48 tasks across 3 domains): https://arxiv.org/pdf/2305.14909
- Popper ILP (ARC-AGI 2025): https://journals.sagepub.com/doi/10.1177/17248035251363178
- DreamCoder: https://dl.acm.org/doi/10.1145/3453483.3454080
- LILO (LLM-guided library learning): https://arxiv.org/pdf/2310.19791
- TheoremLlama (LLM → Lean 4): https://arxiv.org/pdf/2407.03203
- APOLLO (LLM + Lean collaboration): https://arxiv.org/pdf/2505.05758
- Vampire 2025 (CAV): https://arxiv.org/html/2506.03030v3
- ConstraintLLM (neuro-symbolic CP): https://arxiv.org/pdf/2510.05774
- OR-Tools + MiniZinc: https://spin.atomicobject.com/optimization-minizinc-google-or/
- Pi-CoT (Prolog + LLM chain-of-thought): https://arxiv.org/pdf/2506.20642
- PySwip Python-Prolog bridge: https://github.com/yuce/pyswip
- SMT-LLM dependency resolution (83.6%): https://arxiv.org/pdf/2605.11772
- Rule-based inconsistent KB querying (ASP+Python, 2025): https://arxiv.org/pdf/2508.07742
