# 02 — Neurosymbolic AI

**Cluster:** Combining neural nets (or LLMs) with symbolic reasoning — the live frontier most directly
relevant to Jarvis, which already is a neural core + symbolic scaffold.

**Opened:** 2026-07-16 · **Hard constraint:** all adoptable ideas must pass the laptop test (≤16GB
RAM, CPU-only, Ryzen 5 1600).

---

## 1. Taxonomy: What "Neurosymbolic" Actually Means

The field has no single unified definition, but Henry Kautz's 2020 AAAI presidential address taxonomy
remains the most used classification. It describes six integration levels, arranged by how tightly the
neural and symbolic halves couple:

| Type | Label | Description | Examples |
|------|-------|-------------|---------|
| 1 | Symbolic→Neural→Symbolic | Symbolic tokens in, neural processing, symbolic tokens out. Pure deep learning. | GPT-4, BERT |
| 2 | Symbolic[Neural] | A **symbolic engine orchestrates**; neural components are called as tools when needed. | AlphaGo, AlphaGeometry |
| 3 | Neural→Symbolic | Neural system **generates symbolic structures** that a separate symbolic engine verifies or reasons over. | LINC, Logic-LM, LLM-Modulo |
| 4 | Neural∪Compile(Symbolic) | Domain knowledge compiled into network architecture before training. | Limited; mostly theoretical |
| 5 | Neural_{Symbolic} | Differentiable logic embedded inside the network; end-to-end trainable. | Scallop, DeepProbLog, LTNs |
| 6 | Neural[Symbolic] | Fully native symbolic reasoning inside neural weights. | Theoretical; undemonstrated |

**Practical verdict (2026):** Types 2 and 3 dominate all deployed systems. They have clear component
boundaries, independent debuggability, graceful degradation, and auditability. Types 4–6 are research
frontiers; Types 5's differentiable reasoning remains computationally expensive at any real scale.

A complementary framing: Kahneman's **System-1/System-2** dual-process theory. System-1 = fast,
intuitive, pattern-based. System-2 = slow, deliberate, rule-governed. Standard LLM inference is
System-1. Neurosymbolic architectures aim to add a System-2 layer — either by wrapping the LLM in a
symbolic controller (Type 2), or by having the LLM feed a symbolic solver (Type 3).

**Jarvis already sits at the boundary of Types 2 and 3.** Its PreToolUse/PostToolUse hooks form a
symbolic controller layer; WWWD is a rule-based decision gate; the memory graph is a structured
knowledge base. This is not metaphor — it is the Kautz Type 2 pattern: a deterministic harness
orchestrating an LLM invoked as a tool.

---

## 2. LLM-Modulo Frameworks (Kambhampati et al., ICML 2024)

### 2.1 Core Mechanism

**Paper:** "LLMs Can't Plan, But Can Help Planning in LLM-Modulo Frameworks" (arXiv:2402.01817,
ICML 2024 spotlight).

The central claim: LLMs cannot autonomously plan OR self-verify. Auto-regressive generation is
fundamentally a System-1 operation — pattern completion over training distribution — and cannot
reliably detect its own errors or guarantee constraint satisfaction.

The proposed fix is a **bi-directional feedback loop** between the LLM and a bank of external critics:

```
                  ┌──────────────────────────────────────────┐
Problem spec ──>  │  LLM (idea generator)                    │
                  │  · generates candidate plan               │
                  │  · converts plan to critic-readable form  │
                  │  · incorporates feedback for next attempt │
                  └──────────────────┬───────────────────────┘
                                     │ candidate plan
                                     ▼
                  ┌──────────────────────────────────────────┐
                  │  CRITIC BANK (external verifiers)        │
                  │  · model-based critics (formal, sound)   │
                  │  · LLM-based critics (soft constraints)  │
                  └──────────────────┬───────────────────────┘
                                     │ feedback / rejection
                                     └─────────────────────>  (loops back to LLM)
```

Two types of critics:

- **Model-based critics** — formal domain models (PDDL planners, SMT solvers, constraint checkers).
  These are *sound*: if they accept, the plan is correct with respect to the model. They check hard
  constraints like executability, ordering, resource limits.
- **LLM-based critics** — separate LLM calls assessing soft qualities (style, coherence, user
  preference). These are *heuristic*, not sound.

The LLM also helps acquire and refine the domain models used by the model-based critics — so the
division of labor is asymmetric: the LLM does natural language understanding and reformulation; the
symbolic critics do hard verification.

### 2.2 Division of Labor (Neural vs. Symbolic)

| Role | Component |
|------|-----------|
| Idea generation from NL spec | LLM (neural) |
| Format translation (NL → critic-readable) | LLM (neural) |
| Constraint verification (hard) | Symbolic critic (formal, CPU-cheap) |
| Soft-quality assessment | LLM critic (neural, separate call) |
| Domain model acquisition | LLM (neural) + human |
| Iteration control / acceptance | Symbolic logic in the harness |

### 2.3 Maturity and Tooling

- Paper: ICML 2024, well-cited.
- No single open-source "LLM-Modulo framework" package exists; the architecture is a design pattern,
  not a library.
- The closest implementations are custom Python harnesses in research codebases.
- Follow-on systems: ALCM (Khatibi et al., 2024), CMA (Maruyama et al., 2025) instantiate the
  pattern with multiple asynchronous LLM modules and a shared state.
- **Concrete results:** In Blocks World planning, LLM accuracy improved from a low baseline to 82%
  within 15 feedback rounds from a model-based verifier. Travel planning: 6x better than baseline.

### 2.4 Laptop Test

Model-based critics (PDDL planners, Z3, Python constraint checkers) are CPU-native and trivially
small. The LLM calls are the only expensive part, and the framework is designed to reduce total LLM
calls by front-loading symbolic rejection. **Passes laptop test.**

### 2.5 Jarvis Mapping

Jarvis's PreToolUse hooks ARE the critic bank in embryonic form. Every gate that blocks a tool call
based on a rule is a model-based critic. The WWWD gate is a domain-specific critic (does this action
align with Will's patterns?). The gap: Jarvis's critics are currently hand-coded, binary (block/allow),
and opaque — they emit no structured feedback that the LLM can iterate against. Implementing the
feedback loop — having rejected tool calls return structured reasoning that the LLM incorporates into
its next attempt — is the immediate upgrade path.

---

## 3. LLM+Solver Pipelines (NL→Formal Language→Solver)

### 3.1 Core Mechanism

The most mature and practically deployed neurosymbolic pattern. The LLM acts as a **translator**: it
reads natural language, maps it to a formal language (FOL, SMT-LIB, PDDL, MiniZinc, Python + Z3,
Datalog), and hands off to an off-the-shelf solver. The solver does the actual reasoning; the LLM
touches none of it.

Key instances:

- **LINC** (Olausson et al., EMNLP 2023): LLM → First-Order Logic → Prover9. On ProofWriter:
  outperforms GPT-3.5 CoT by +38% and GPT-4 CoT by +26% when paired with even a mid-size model.
- **Logic-LM** (Pan et al., EMNLP 2023): LLM → multiple symbolic backends (SAT, FOL, constraint).
- **SatLM** (Ye et al., 2023): NL → SAT/UNSAT.
- **LLM+P** (Liu et al., 2023): LLM → PDDL → fast-downward planner.
- **OptiMUS** (2024): NL → MILP (optimization).
- **MCP-Solver** (Szeider et al., 2025): Wraps Z3, MiniZinc, PySAT, Clingo as MCP tools; LLM
  builds solver encoding through conversational tool calls.
- **VeriTrans** (2025): Fine-tuned compact model for NL→PL translation; solver as deterministic
  post-processing. Low latency, reproducible.

The reliability issue is real: LLM translation is not always correct. All serious systems add a
**revision-by-error module** — if the solver returns an error or unsatisfiable, that signal goes back
to the LLM to regenerate (typically capped at 3–5 retries).

### 3.2 Division of Labor

| Role | Component |
|------|-----------|
| Natural language understanding | LLM (neural) |
| Translation to formal language | LLM (neural) |
| Actual logical/combinatorial reasoning | Solver (symbolic, sound, complete) |
| Error feedback (parse errors, UNSAT) | Solver → LLM loop |
| Result interpretation into NL | LLM (optional, neural) |

### 3.3 Maturity and Tooling

Mature. All solvers (Z3, Prolog, fast-downward, Clingo, MiniZinc) are open source, actively
maintained, and CPU-native. The LLM-to-solver pipeline is a 50–200 line Python script in any of
these systems. MCP-Solver demonstrates the pattern is now trivially composable with modern LLM
tool-use interfaces.

The main friction: **translation quality.** Benchmark results vary widely depending on how well the
LLM can formalize the domain. Fine-tuning the translator (VeriTrans approach) is a significant
quality improvement but requires data.

### 3.4 Laptop Test

All CPU-native. A Z3 or Clingo solve on a Ryzen 5 1600 is milliseconds for problems that take an
LLM minutes of token generation. **Strongly passes laptop test.**

### 3.5 Jarvis Mapping

The clearest near-term adoption path: any time Jarvis needs logical reasoning over structured state
(scheduling, constraint satisfaction, planning sequences of actions), have the LLM translate the
problem into Z3 or Clingo, run the solver locally, return the verified plan. This offloads the
reasoning from expensive LLM tokens onto free local CPU cycles. The WWWD gate, currently a soft
heuristic emulation, could be partially formalized as a constraint satisfaction problem: "given the
current task state and Will's known decision patterns (encoded as constraints), which action set is
consistent?"

---

## 4. Verifier-Guided Decoding and Grammar-Constrained Generation

### 4.1 Core Mechanism

A different integration point: rather than using the symbolic verifier *after* LLM generation, these
approaches inject symbolic constraints *into* the decoding process itself — shaping what tokens the
LLM can emit at each step.

The spectrum:

- **Grammar-constrained decoding** (Willard & Louf 2023, DOMINO ICML 2024, XGrammar 2024): Mask
  invalid tokens during sampling based on a formal grammar or regex. Guarantees outputs conform to a
  schema. XGrammar 2 (2026) makes this nearly zero overhead.
- **NeuroLogic Decoding** (NAACL 2021, NAACL 2022 with lookahead): Predicate logic constraints over
  what tokens can appear, with lookahead heuristics to avoid constraint violations.
- **IterGen / CRANE (2025)**: Backtracking and resampling when semantic constraints are violated during
  generation. Goes beyond syntactic grammar to semantic predicates.
- **BEAVER (2025)**: Deterministic LLM verifier — soundly quantifies total probability of constraint
  satisfaction; characterizes model properties rigorously.
- **NSVIF (2025)**: Extracts constraints from prompts, synthesizes type and format checkers, interfaces
  with DSPy, PDL, LMQL.

### 4.2 Division of Labor

| Role | Component |
|------|-----------|
| Token probability distribution | LLM (neural) |
| Valid-token mask per grammar/logic | Symbolic automaton/constraint (CPU) |
| Backtracking when violated | Search algorithm (symbolic) |
| Probability-distribution preservation | Grammar-Aligned Decoding (addresses distortion) |

### 4.3 Maturity and Tooling

Grammar-constrained decoding: **production-ready**. XGrammar is a standalone library; Outlines
(dottxt-ai/outlines) is a widely used Python library for structured generation. JSON schema
enforcement is now standard in Ollama, llama.cpp, vLLM.

Semantic constraint decoding (CRANE, IterGen): research stage, not yet packaged as standalone
libraries.

### 4.4 Laptop Test

Grammar masks are computed from finite automata over the tokenizer vocabulary — pure CPU, microsecond
per step. **Passes laptop test.** CRANE-style backtracking is heavier but still CPU-native.

### 4.5 Jarvis Mapping

Jarvis today calls the LLM and then validates output in PostToolUse hooks. Grammar-constrained
decoding inverts this: the constraint fires *before* the token is committed. For structured outputs
(tool call arguments, JSON schemas, decision classifications), this eliminates a whole class of parse
errors and retry loops. Outlines or XGrammar can be dropped into any local model inference call
(Ollama, llama.cpp) with near-zero overhead. The NSVIF pattern — extracting constraints from natural
language prompts and synthesizing checkers — is a direct analog of how Jarvis extracts task
requirements and then gates on them.

---

## 5. LINC and Neural Logic Pipelines (LLM→FOL→Prover)

### 5.1 Core Mechanism

Elaborating on the solver pipeline specifically for **logical deduction** tasks (as opposed to
constraint satisfaction or planning). LINC is the clearest concrete example:

1. LLM receives NL premises and a conclusion to evaluate.
2. LLM translates each premise and the conclusion into First-Order Logic statements in Prover9 syntax.
3. Prover9 (an automated theorem prover) determines entailment.
4. If Prover9 raises a parse error, the LLM is re-prompted (up to 10 times). Majority voting across
   valid completions determines the final label.

Results: on ProofWriter, a StarCoder+ (15.5B) + LINC beats both GPT-3.5 CoT and GPT-4 CoT. Key
insight: the LLM and the symbolic prover have **complementary failure modes** on FOLIO — they fail on
different types of problems, making their combination more robust than either alone.

Follow-ons extend to Lean/Isabelle for formal mathematics (Lean Copilot, LeanDojo), and to temporal
logic for robot specifications (ConformalNL2LTL).

### 5.2 Maturity and Tooling

Prover9: old, stable, CPU-native, small. Lean/Isabelle: active, but heavy proof assistants with
steep learning curves. Vampire, E, Z3 (as theorem prover): lighter options.

For propositional logic use cases: Z3 as a prover is probably the most practical. For FOL at
ProofWriter/FOLIO difficulty: Prover9 or Vampire.

### 5.3 Laptop Test

Prover9, Vampire, Z3 as theorem provers: all CPU-native, routinely run on laptops. **Passes laptop
test.** Lean/Isabelle servers: heavier but still manageable on 16GB RAM without GPU.

### 5.4 Jarvis Mapping

If Jarvis needs to check logical consistency of its own memory primitives (e.g., "does adding this new
rule contradict an existing rule?"), a LINC-style pipeline applies: have the LLM formalize the rules
as FOL, run Prover9/Z3, surface any contradiction. This is a step toward the "self-auditing
substrate" implied by the RSAW protocol — making logical consistency checking automatic and sound
rather than dependent on LLM pattern-matching.

---

## 6. Neural Theorem Proving (NTP) — Lean/Isabelle + LLMs

### 6.1 Core Mechanism

Neural Theorem Proving couples a fine-tuned LLM (generating proof tactics or whole proofs) with a
formal proof assistant (Lean, Isabelle, Coq) that acts as the ground-truth verifier. The proof
assistant rejects invalid proofs with no false positives — it is sound by construction.

Key paradigms:

- **Whole-proof generation**: LLM outputs an entire Lean proof script; the proof assistant
  checks it. HybridProver, MA-LoT.
- **Tactic-step generation**: LLM generates one tactic at a time; proof assistant validates each
  step; search (MCTS, beam search) explores the tactic tree. LeanDojo, LeanCopilot.
- **Autoformalization + RL**: LLM translates NL statements to formal ones; RL loop generates and
  proves variants, with proof assistant as the reward signal. AlphaProof (DeepMind, 2024): 80M
  auto-formalized statements, Gemini + AlphaZero RL, solved 4/6 IMO 2024 problems at silver-medal
  level.

AlphaGeometry 2: LLM alternates with a symbolic deduction engine for Olympiad geometry. 84% of IMO
geometry 2000–2024 solved correctly.

### 6.2 Maturity and Tooling

LeanDojo (open source): mature Python interface to Lean 4 proof states, retrieval over Mathlib.
Lean Copilot (COLM/ICML 2025): runs LLM inference natively in Lean. DeepSeek-Prover-V2 (2025):
open weights model purpose-trained for Lean proving.

These tools work but have a steep on-ramp: you must write or generate formal Lean/Isabelle code,
and the libraries are large (Mathlib4 is gigabytes).

### 6.3 Laptop Test

Lean 4 + Mathlib: runs on CPU, but Mathlib compilation is memory-hungry (~6GB). For Jarvis-scale
use cases (checking small logical arguments, not formalizing all of mathematics), a stripped-down
Lean setup is feasible. **Marginally passes laptop test** for limited use; full Mathlib requires care.

### 6.4 Jarvis Mapping

NTP is architecturally interesting for Jarvis but practically overkill for most tasks. The exception:
if Jarvis ever needs to formally verify protocol invariants (e.g., "this sequence of hook firings
cannot deadlock"), a Lean-based formalization would be uniquely trustworthy. Near-term this is
aspirational, not adoptable. The more practical extraction: the *pattern* of using a proof assistant as
a sound verifier in an RL loop — even if the "proof assistant" for Jarvis is a lightweight Python
invariant checker rather than Lean.

---

## 7. Differentiable Neurosymbolic Frameworks (Scallop, DeepProbLog, Logic Tensor Networks)

### 7.1 Core Mechanism

These frameworks attempt something more radical: making symbolic reasoning itself differentiable, so
the neural and symbolic components can be trained end-to-end with gradient descent. This is
Kautz Type 5.

- **DeepProbLog** (Manhaeve et al., 2018/2021): Probabilistic logic programming (ProbLog) with neural
  predicates. Neural networks parameterize the probabilities of facts; the probabilistic logic engine
  does the reasoning. Gradients flow back through the logic.
- **Scallop** (PLDI 2023): Differentiable Datalog with provenance semirings. Recursion, aggregation,
  negation. PyTorch bindings. 45K lines of Rust; Docker image + summer school 2024 materials. The most
  practically packaged of the three.
- **Logic Tensor Networks (LTNs)** (Badreddine et al., 2022): First-order logic with fuzzy semantics.
  Logical formulas as tensor operations; violations penalized in the loss function.
- **DeepSoftLog** (Maene & Raedt, 2024): Superset of ProbLog with embedded terms; probabilistic rather
  than fuzzy semantics.
- **CTSketch** (NeurIPS 2025): Compositional Tensor Sketching for scalable neurosymbolic learning;
  addresses the computational cost that has limited Scallop/DeepProbLog at scale.

### 7.2 Division of Labor

| Role | Component |
|------|-----------|
| Perception / feature extraction | Neural network |
| Probabilistic fact generation | Neural predicates |
| Logical inference | Differentiable symbolic engine |
| End-to-end training | Gradient through both components |

### 7.3 Maturity and Tooling

Scallop: most accessible. Open source (github.com/scallop-lang), Python bindings, summer school
materials, published textbook (FnTPL 2024). Active research group (Penn). AAAI 2024 paper on
combining Scallop with foundation models like GPT.

DeepProbLog: working but less actively developed, steeper learning curve.

LTNs: open source (ltnreasoner Python library), but integration with LLMs is not packaged.

**Important limitation:** The end-to-end differentiable appeal disappears when the neural component is
a frozen LLM. You cannot backpropagate through GPT-4. These frameworks are most natural when the
neural component is a small task-specific network trained from scratch, not a large pre-trained model.

### 7.4 Laptop Test

Scallop inference: CPU-native, fast for small programs. Training with PyTorch: no GPU required for
small models, but will be slow on 16GB RAM for anything substantial. **Passes for inference / small
programs; borderline for training.**

### 7.5 Jarvis Mapping

Limited direct fit. The differentiable training angle doesn't apply because Jarvis's LLM is frozen.
However, Scallop's **inference mode** (running a Datalog program with probabilistic inputs) is
interesting: Jarvis's memory graph is effectively a Datalog database; Scallop could run reasoning
queries over it with uncertain (LLM-generated) inputs. Example: "given these probabilistic entity
relations extracted from conversation, what tasks are likely entailed?" This is a research path, not
a near-term adoption.

---

## 8. Knowledge Graph Integration (GraphRAG, KG+LLM Reasoning)

### 8.1 Core Mechanism

A large body of 2024–2025 work combines LLMs with structured knowledge graphs:

- **GraphRAG** (Microsoft, open-sourced July 2024): Builds a community-detected knowledge graph from
  documents; queries traverse the graph before prompting the LLM. Solves multi-hop reasoning that
  flat vector RAG cannot.
- **KG-CoT** (2024): Traverses a KG to generate a chain-of-thought reasoning path, provided to the
  LLM as context.
- **Think-on-Graph 2.0** (2024): Deep iterative KG traversal + LLM reasoning loop.
- **GraphToken** injection (2025): Structured KG information injected into frozen LLMs without
  fine-tuning.
- **Graph RAG-Tool Fusion** (2025): Combines KG retrieval with tool-augmented agents.

### 8.2 Division of Labor

| Role | Component |
|------|-----------|
| Entity/relation extraction from text | LLM (neural) |
| Structured storage and traversal | Knowledge graph (symbolic) |
| Multi-hop reasoning paths | Graph traversal algorithm (symbolic) |
| Natural language answer generation | LLM (neural) |
| Hallucination grounding | KG fact lookup (symbolic) |

### 8.3 Maturity and Tooling

Microsoft GraphRAG: production-ready, open source, Python, actively maintained. Neo4j + LangChain
integration: mature. NetworkX for lightweight graphs: trivially runs on any hardware.

For local deployments without a graph database: NetworkX + custom traversal is sufficient for
Jarvis-scale graphs (thousands of nodes).

### 8.4 Laptop Test

NetworkX, SQLite-based graph stores, local Neo4j: all run on 16GB RAM. GraphRAG's LLM extraction
phase is the expensive part (external API calls), but the graph itself and traversal are CPU-native.
**Passes laptop test** for the reasoning/retrieval side.

### 8.5 Jarvis Mapping

Jarvis's file-based memory graph (wikilink-linked markdown primitives) is a manually maintained
knowledge graph. The gap: traversal is currently done by grep and LLM context injection — no
structured graph query. A KG layer over the existing primitives would enable:

- Formal contradiction detection between primitives.
- Automatic entailment queries ("which primitives are violated by this proposed action?").
- Shortest-path reasoning across the dependency graph.

The Jarvis memory graph is already the data source; adding a lightweight graph index (NetworkX
populated from parsed wikilinks) and running KG traversal before LLM context injection is a
near-zero-cost adoption.

---

## 9. System-1/System-2 Architecture in Practice

### 9.1 The Framing

Kahneman's dual-process theory maps cleanly onto the neurosymbolic dichotomy:

- **System-1** (fast, intuitive, automatic): LLM inference. Pattern completion over massive training
  data. No guaranteed correctness. Milliseconds to seconds.
- **System-2** (slow, deliberate, rule-governed): Symbolic reasoning. Guaranteed correct with respect
  to the model. Seconds to minutes depending on problem.

Current LLMs are primarily System-1, even when they "do reasoning" via chain-of-thought — CoT is
still token generation, not symbolic computation.

The neurosymbolic research consensus: **hybrid architectures outperform either alone.** SwiftSage
(2024): T5 as System-1 for simple steps, GPT-4 as System-2 for complex steps. DyVe (2025): merges
PRMs and GenRMs using dual-process theory to balance verification speed and depth. AlphaGeometry 2:
neural LM (System-1, generates candidates) + symbolic deduction engine (System-2, verifies).

### 9.2 Process Reward Models (PRMs) as Symbolic-Neural Hybrids

PRMs (2024–2025 frontier) evaluate each reasoning step rather than only the final answer. This adds
a System-2-like supervisory signal to the System-1 token generation process:

- **ORM** (Outcome Reward Model): Checks only the final answer. Misses step-level errors.
- **PRM** (Process Reward Model): Scores each reasoning step. Better credit assignment.
  OpenAI PRM800K, Setlur et al. 2024 scaling results.
- **GenRM** (Generative Verifier): LLM that reasons about whether each step is correct.
  High quality but expensive.
- **Rule-based verifiers**: Domain-specific checkers (math answer parsers, code execution, formal
  proof checkers). Cheapest and most reliable where applicable.

For Jarvis: rule-based step verification (hooks checking each tool call in a chain) is already the
natural implementation of PRM. The question is whether the verification logic is rich enough to catch
reasoning errors, not just format violations.

### 9.3 Jarvis Mapping

Jarvis's hook architecture is literally a System-2 layer: it runs after each LLM-generated action
(System-1 output) and decides whether to allow, block, or modify it. The current System-2 is thin
(mostly format checks and permission gates). The mature version runs richer symbolic verification:
logical consistency against memory graph, constraint satisfaction against task goals, adversarial
red-teaming via a separate critic call.

---

## 10. Tool Use as Symbolic Offloading (Agentic / ReAct Paradigm)

### 10.1 Core Mechanism

The tool-use paradigm (ReAct, Yao et al. 2023; Anthropic tool use; OpenAI function calling) is the
most widely deployed form of neurosymbolic integration in 2024–2026. The LLM generates an *intent*
to use a tool; the tool executes deterministically; the result returns to the LLM context.

This is Kautz Type 3: the LLM generates a symbolic action (tool call with arguments), the symbolic
system (tool) executes it, results feed back.

The "externalization" literature (arXiv:2604.08224) formalizes what gets offloaded:

- **Memory externalization**: knowledge graphs, vector stores, file systems — the LLM's context
  window is too small and ephemeral; structured stores are persistent and queryable.
- **Skill externalization**: calculators, code interpreters, SQL engines, symbolic solvers — tasks
  where the LLM would be unreliable; dedicated tools are exact.
- **Protocol externalization**: the harness's orchestration logic, gate predicates, control flow —
  decisions that must be deterministic and auditable.

The recurring finding: reliability problems are increasingly solved by **changing the environment**
(the harness / the tool set), not by improving the prompt.

An important 2026 paper (arXiv:2606.26924) — "A Deterministic Control Plane for LLM Coding Agents"
— proposes exactly the Jarvis architecture from first principles: bounded recursion (3-iteration cap),
mandatory delegation receipts, hard-coded gate predicates as a governance overlay. This is an
independent derivation of what Jarvis has been building.

### 10.2 Maturity and Tooling

Completely mature. Anthropic tool use, OpenAI function calling, MCP: production-grade. ToolLLM
demonstrated 16,000+ real-world API integrations. Every major agent framework (LangChain, AutoGen,
CrewAI, DSPy, Haystack) supports tool use as a first-class primitive.

### 10.3 Jarvis Mapping

This is Jarvis's *current primary neurosymbolic integration mechanism*. Every hook that blocks or
routes a tool call is symbolic logic governing neural output. The gap relative to mature neurosymbolic
systems: the hooks lack feedback articulation (they block but don't explain to the LLM in a
structured way that enables self-correction) and lack symbolic planning of tool call sequences (the
LLM decides tool ordering; no constraint solver validates the sequence against goals before execution).

---

## 11. Top 3 Adoptable Patterns for Jarvis (Concrete Integration Sketches)

### 11.1 Priority 1: Structured Critic Feedback (LLM-Modulo Pattern)

**The gap:** Jarvis hooks block tool calls but return no structured reasoning that the LLM can learn
from within a session.

**The upgrade:**

```python
# Current: hook blocks silently or with a flat error string
def pre_tool_use_hook(tool_call):
    if violates_constraint(tool_call):
        return {"decision": "block", "reason": "constraint violated"}

# Upgraded: hook returns structured critic output
def pre_tool_use_hook(tool_call):
    violations = run_constraint_checks(tool_call)
    if violations:
        return {
            "decision": "block",
            "critic_output": {
                "violated_constraints": [v.to_dict() for v in violations],
                "suggested_reformulation": suggest_fix(tool_call, violations),
                "iteration_count": get_iteration_count(tool_call.task_id),
            }
        }
```

The LLM receives this structured critic output in its next prompt and can reformulate the action.
The harness tracks iteration count and escalates (human-in-the-loop) after N attempts.

**Concreteness:** This is a Python dict change to existing hooks. No new libraries. Zero additional
inference cost. Kambhampati's 82%-in-15-rounds result suggests even crude structured feedback
dramatically improves LLM reasoning convergence.

**Hardware:** CPU-only. Passes laptop test trivially.

### 11.2 Priority 2: Local Solver Integration for Reasoning Tasks (LLM+Solver Pipeline)

**The gap:** WWWD and planning decisions are currently made by the LLM via pattern-matching over
memory context. These could be solved exactly by a constraint solver, freeing LLM tokens for tasks
that genuinely require language understanding.

**The upgrade:** A thin Python module that:
1. Accepts a task description and the current Jarvis state (active goals, constraints from CLAUDE.md
   and memory primitives, available tools).
2. Calls the LLM once to translate this into Z3 constraints.
3. Runs Z3 locally (milliseconds).
4. Returns the verified action set to the orchestrator.

```python
import z3

def jarvis_plan_via_solver(task_state: dict, constraints: list[str]) -> dict:
    """
    LLM translates task_state + constraints to Z3 assertions.
    Z3 solves. Returns verified action set or UNSAT (escalate to human).
    """
    z3_code = llm_translate_to_z3(task_state, constraints)  # one LLM call
    solver = z3.Solver()
    exec(z3_code, {"solver": solver, "z3": z3})  # sandboxed execution
    result = solver.check()
    if result == z3.sat:
        return {"plan": extract_model(solver.model()), "verified": True}
    else:
        return {"plan": None, "verified": False, "reason": "constraints unsatisfiable"}
```

**Concreteness:** Z3 Python bindings (`pip install z3-solver`), one LLM translation call, local
solve. Z3 uses ~50MB RAM and is single-threaded (fits inside 16GB easily). The LLM translation is the
weak point — translation errors cause Z3 parse failures which loop back for reformulation.

**Hardware:** Passes laptop test. Z3 is CPU-native.

### 11.3 Priority 3: Graph-Indexed Memory Traversal (KG Pattern)

**The gap:** The memory graph (wikilink-linked primitives) is traversed by grep + LLM attention. No
formal graph traversal; no automated contradiction detection; no entailment queries.

**The upgrade:**

```python
import networkx as nx
import re
from pathlib import Path

def build_primitive_graph(memory_dir: Path) -> nx.DiGraph:
    """Parse wikilinks from all .md files; build directed graph."""
    G = nx.DiGraph()
    for md in memory_dir.rglob("*.md"):
        node = md.stem
        G.add_node(node, path=str(md))
        for link in re.findall(r'\[\[([^\]]+)\]\]', md.read_text()):
            G.add_edge(node, link)
    return G

def primitives_entailed_by(G: nx.DiGraph, primitive_id: str) -> list[str]:
    """Return all primitives reachable from this one (transitive closure)."""
    return list(nx.descendants(G, primitive_id))

def detect_contradictions(G: nx.DiGraph, llm_formalize) -> list[tuple]:
    """
    For each node pair connected by a path, have LLM formalize both as FOL,
    run Z3 to check consistency. Flag contradictions.
    """
    contradictions = []
    for u, v in G.edges():
        if llm_formalize_and_z3_check_contradiction(u, v):
            contradictions.append((u, v))
    return contradictions
```

This graph is built in <1 second, runs in RAM on NetworkX, and enables:
- "Which primitives must fire before this one?" (topological ordering)
- "Does adding this new primitive create a contradiction?" (Z3 consistency check)
- "What is the full dependency chain of WWWD?" (reachability)

**Concreteness:** `pip install networkx`. Runs on the existing markdown files with no file format
changes. The graph builder is ~30 lines. The contradiction checker requires the LLM+Z3 pipeline from
Priority 2 — natural composition.

**Hardware:** NetworkX on 5,000 nodes uses ~10MB RAM. Trivially passes laptop test.

---

## 12. Honesty Assessment: Maturity Map

| Approach | Research Maturity | Tooling Readiness | Jarvis Fit | Laptop Test |
|----------|-------------------|-------------------|------------|-------------|
| LLM-Modulo critic feedback loop | High (ICML 2024) | Pattern only, no library | Direct, immediate | Pass |
| LLM+Z3/Clingo solver | High (many systems) | Excellent (Z3, Clingo pip-installable) | Direct, immediate | Pass |
| Grammar-constrained decoding | Very High | Production (Outlines, XGrammar) | Moderate (structured output) | Pass |
| KG traversal over memory graph | High (GraphRAG) | Excellent (NetworkX) | Direct, immediate | Pass |
| LINC-style FOL proving | Moderate (2023) | Good (Prover9, Z3) | Useful for logic checks | Pass |
| Neural Theorem Proving (Lean) | High (research) | Moderate (LeanDojo) | Aspirational | Marginal |
| Scallop/DeepProbLog differentiable | Moderate | Good (Scallop pip) | Limited (frozen LLM) | Marginal |
| Logic Tensor Networks | Moderate | Good (ltnreasoner) | Limited (frozen LLM) | Pass (inference) |
| Process Reward Models | High (2024-2025) | Research stage | Indirect (hook pattern) | Pass |
| AlphaGeometry-style domain loops | High (DeepMind) | Custom per domain | Inspirational only | Pass (small domain) |

The honest summary: the research frontier has produced dozens of architectures. For Jarvis specifically
— a Python harness wrapping a frozen LLM, CPU-only, no GPU — the immediately adoptable cluster is
**Types 2/3 (LLM-Modulo + LLM+Solver) and KG traversal**. Differentiable frameworks (Types 4/5)
are not applicable to frozen LLM wrappers; they require trainable neural components.

---

## 13. The Mature Version of Jarvis (Synthesis)

Jarvis today: ~2% neural (one LLM call per task), ~98% deterministic Python harness. The
neurosymbolic literature converges on this being the *right direction* — not the primitive version to
be discarded.

The mature version looks like this:

```
                    ┌────────────────────────────────────────────────┐
User input ──>      │  SYMBOLIC CONTROLLER (the harness)             │
                    │  · Task parser (KG lookup against memory graph) │
                    │  · Constraint extractor (Z3 formalization)      │
                    │  · Pre-call verifier (critic bank / gate rules) │
                    │  · Iteration controller (max N, escalation)     │
                    └──────────────────┬─────────────────────────────┘
                                       │ structured prompt + constraints
                                       ▼
                    ┌─────────────────────────────────────────────────┐
                    │  LLM (System-1: pattern completion / NL→format) │
                    │  · called sparingly, for what it does well:     │
                    │    understanding NL, generating candidates,      │
                    │    translating to formal languages               │
                    └──────────────────┬──────────────────────────────┘
                                       │ candidate action / formal translation
                                       ▼
                    ┌─────────────────────────────────────────────────┐
                    │  SYMBOLIC VERIFIERS (System-2: deterministic)   │
                    │  · Z3/Clingo: constraint satisfaction            │
                    │  · NetworkX: memory graph consistency            │
                    │  · Grammar masks: output schema enforcement      │
                    │  · Domain rules: Python invariant checkers       │
                    └──────────────────┬──────────────────────────────┘
                                       │ verified output OR structured feedback
                                       └─────────────> back to controller
```

The LLM gets *smaller* over time as more reasoning is encoded into explicit verifiers. The System-1
call becomes a fast, cheap, narrow translator — not the reasoning engine. This is the Cave philosophy
applied to neurosymbolic design: build the intelligence into the structure, use the rented neural
component only for what cannot yet be structured.

---

## References and Sources

- Kambhampati et al., "LLMs Can't Plan, But Can Help Planning in LLM-Modulo Frameworks," ICML 2024.
  https://arxiv.org/abs/2402.01817
- Olausson et al., "LINC: A Neurosymbolic Approach for Logical Reasoning," EMNLP 2023.
  https://arxiv.org/abs/2310.15164
- Pan et al., "Logic-LM: Empowering Large Language Models with Symbolic Solvers," EMNLP 2023.
- Li et al., "Scallop: A Language for Neurosymbolic Programming," PLDI 2023.
  https://arxiv.org/pdf/2304.04812
- Scallop book (FnTPL 2024): https://www.cis.upenn.edu/~mhnaik/papers/fntpl24.pdf
- "Neuro-Symbolic AI in 2024: A Systematic Review," arXiv:2501.05435
- AlphaGeometry 2 / AlphaProof, Google DeepMind, 2024. Nature 2025.
  https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/
- Kautz Taxonomy: "The Third AI Summer," AAAI 2020 presidential address.
  https://medium.com/@billaram/the-kautz-taxonomy-a-field-guide-to-neuro-symbolic-ai-0627e4832c5b
- Szeider et al., "Bridging Language Models and Symbolic Solvers via MCP," SAT 2025.
  https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SAT.2025.30
- "Externalization in LLM Agents," arXiv:2604.08224
- "A Deterministic Control Plane for LLM Coding Agents," arXiv:2606.26924
- XGrammar: https://arxiv.org/pdf/2601.04426
- CRANE, arXiv:2502.09061
- BEAVER, arXiv:2512.05439
- GraphRAG: https://github.com/microsoft/graphrag
- Survey on PRMs: arXiv:2510.08049
- LAMDA-NeSy awesome list: https://github.com/LAMDA-NeSy/Awesome-LLM-Reasoning-with-NeSy
