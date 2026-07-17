# Cognitive Architectures for Jarvis: Research Dossier

**Author**: Research agent (Claude Sonnet 4.6)
**Date**: 2026-07-16
**Context**: Jarvis is a deterministic Python harness wrapping Claude — PreToolUse/PostToolUse hooks as gates, a file-based markdown memory graph, cron jobs, subagents, and a WWWD decision gate. The LLM does the reasoning; Jarvis only orchestrates it. Will wants to move genuine reasoning OUT of transformer weights and INTO explicit engineered structure. This dossier covers cognitive architectures as the historical discipline of engineering intelligence without neural next-token prediction.

---

## Introduction: Why Cognitive Architectures Matter for Jarvis

Cognitive architectures are the branch of AI that tried to solve exactly what Will is asking about — before transformers existed. They were the attempt to build intelligence by engineering it explicitly: production rules, goal stacks, working memory buffers, belief systems with truth values, chunking (automated rule learning), and episodic memory. They produce intelligent-looking behavior via symbolic manipulation rather than statistical correlation across a training corpus.

Jarvis already has the shape of a cognitive architecture in rough form:
- **Hooks** = production rules (IF condition THEN action)
- **Memory graph** (markdown primitives + wikilinks) = semantic/declarative memory
- **WWWD gate** = goal arbitration / decision cycle
- **Cron jobs** = scheduled cognitive cycles
- **Subagents** = parallel problem-space search

The gap is that these components are held together by LLM-generated text. The LLM is doing all the inference — matching conditions, evaluating which rule to fire, assessing goal priority. A cognitive architecture would replace or augment that inference with deterministic, auditable, fast symbolic machinery.

This dossier covers six architectures: SOAR, ACT-R, LIDA, CLARION, Sigma, and NARS/OpenNARS. Each is assessed on: (a) core mechanism, (b) current maturity and tooling, (c) positioning relative to an LLM, and (d) direct mapping to Jarvis components.

---

## 1. SOAR — State, Operator, And Result

### Core Mechanism

SOAR structures all intelligent behavior as search in problem spaces. At any moment, the agent holds a **working memory** (a structured, tagged graph of current facts, goals, and operator preferences) and a **procedural memory** (a set of IF-THEN production rules). Each decision cycle:

1. Productions fire in parallel against working memory (match phase)
2. The decision procedure selects an operator from proposals
3. The selected operator is applied, modifying working memory
4. If no operator can be selected (an **impasse**), a **substate** is created — a new sub-problem is posed in working memory and the decision cycle recurses into it

Impasses are the key learning mechanism. When a substate resolves an impasse and produces a result, SOAR compiles the trace of that reasoning into a new production rule via **chunking**. The new rule fires immediately in future situations that match the same conditions, turning slow deliberative search into fast compiled reaction. This is SOAR's form of procedural learning — knowledge acquired through experience becomes embedded structure.

Beyond procedural memory, SOAR maintains:
- **Semantic memory** (SMem): factual/declarative knowledge, retrieved by cue
- **Episodic memory** (EPM): snapshots of past working memory states, retrieved by cue
- **Reinforcement learning**: adjusts operator preferences based on reward signals

### Maturity and Tooling (2026)

- Open source, actively maintained: https://github.com/SoarGroup/Soar
- Python bindings via SWIG (part of the Soar Suite distribution)
- Official Soar IDE (VisualSoar) for authoring rules
- Active research group at University of Michigan (John Laird's group)
- 2025 publication: Wray, Kirk, Laird — "Eliciting problem specifications for LLM-Modulo cognitive systems" (*Cognitive Systems Research*, Dec 2025)
- NL2GenSym (Oct 2025, arXiv 2510.09355): first end-to-end framework translating natural language to SOAR production rules via LLM, with Execution-Grounded Generator-Critic mechanism
- Human-robot collaboration work (arXiv 2508.11759, 2025): Soar agent as orchestrator with LLM as language translator
- Minimum Python working example: https://github.com/KRaizer/Soar-Python-Minimum-Working-Example

Maturity verdict: **high**. SOAR is 40 years old, used in military simulations, games (thousands of agents in StarCraft-style environments), and robotics. Python bindings are stable. The main cost is rule authoring — Soar rules must be written in a specialized declarative language, and there are a lot of them for non-trivial tasks. NL2GenSym partially addresses this.

### Positioning Relative to LLM

The dominant 2024-2025 research pattern for Soar+LLM is:
- **LLM as fallback oracle when SOAR hits an impasse**: When SOAR lacks a production rule to fire, it queries the LLM for a suggested action AND a corresponding rule; the rule gets added to procedural memory. The LLM trains SOAR in real time.
- **LLM as language translator**: SOAR handles orchestration, goal management, and operator selection; LLM translates between natural language and SOAR's symbolic representation.
- **LLM generating production rules from NL specs** (NL2GenSym): reduces the cold-start knowledge-engineering problem.

SOAR is a natural System 2 controller: slow, deliberate, rule-governed. LLMs provide the System 1 pattern-matching intuition and language interface.

### Jarvis Mapping

| Jarvis Component | SOAR Equivalent |
|---|---|
| PreToolUse/PostToolUse hooks | Production rules (IF wm-conditions THEN action) |
| WWWD gate | Decision procedure + operator selection cycle |
| Memory graph (markdown primitives) | Semantic memory (SMem) |
| Session state files | Episodic memory (EPM snapshots) |
| Subagents | Substates (parallel problem-space search) |
| Chunking opportunity | When Claude solves a novel impasse, codify that reasoning into a new hook/gate |

The closest gap SOAR fills: **explicit operator selection and impasse handling**. Currently when Jarvis (via Claude) faces an ambiguous situation, the LLM makes the call implicitly in weights. SOAR would make that call via an auditable production-rule match that can be inspected, versioned, and improved.

---

## 2. ACT-R — Adaptive Control of Thought-Rational

### Core Mechanism

ACT-R (John Anderson, Carnegie Mellon) is primarily a theory of human cognition expressed as a computational model. Its core architectural distinction: **declarative memory** and **procedural memory** are strictly separated modules communicating through **buffers**.

At any moment, each module (vision, motor, declarative, goal, imaginal) has a **buffer** — a small, fixed-capacity slot holding one chunk of information. Productions fire when their conditions match the current buffer contents simultaneously. This strict serialization constraint is a deliberate cognitive fidelity choice: humans can only attend to one thing at a time.

Declarative memory works on **activation-based retrieval**: facts (chunks) have a base-level activation that decays with time and increases with use frequency, plus spreading activation from the current goal buffer. The chunk with highest activation above a threshold is retrieved. This produces human-like forgetting and priming effects.

Goal buffer holds the current goal; procedural memory fires productions that update goal buffer state. ACT-R has a tight, empirically-validated cycle time (~50ms per production cycle) that matches human reaction times.

Key departures from SOAR: ACT-R does NOT have SOAR's impasse mechanism or chunking in quite the same sense. It is oriented toward cognitive modeling fidelity over maximal problem-solving power.

### Maturity and Tooling (2026)

- Primary implementation: ACT-R Lisp environment (actr.psy.cmu.edu) — mature, not Python-native
- **pyactr**: Python 3 implementation (Petra Lewandowski), published alongside *Computational Cognitive Modeling and Linguistic Theory*
- **python_actr**: CCM Lab (Carleton University), pip-installable as `actr`
- **PyACT-Up**: models ACT-R's declarative memory module in Python with minimal other commitments — useful for the forgetting curve / activation-based retrieval pattern alone
- **LLM-ACTR** (2024): neuro-symbolic hybrid extracting ACT-R's internal decision-making as latent neural representations injected into LLM adapter layers
- Human-like memory for LLM agents (ACM HAI 2025): ACT-R-inspired autonomous recall/forget based on time, frequency, context
- **ACT-Up context event memory** (arXiv 2606.28045, 2026): rapid prototyping of event-driven contextual memory in an ACT-R variant

Maturity verdict: **high for cognitive modeling, medium for engineering use**. ACT-R's Lisp heritage and human-fidelity orientation make it harder to repurpose as an engineering substrate vs. SOAR. The Python wrappers are functional but narrower. PyACT-Up is the cleanest engineering-facing component.

### Positioning Relative to LLM

ACT-R's most exportable concept for LLM agents is its **declarative memory model**: activation-based retrieval with time decay and frequency-of-use boosts. This is a proven, psychologically-validated algorithm for "what should the agent remember right now?" that doesn't require training data or a neural network — just a recency/frequency accounting system with spreading activation from current context.

The ACT-R buffer architecture is also exportable: enforce the rule that each module exposes exactly one chunk at a time to the production system. This prevents the LLM from attending to too many things simultaneously and losing track.

### Jarvis Mapping

| Jarvis Component | ACT-R Equivalent |
|---|---|
| Memory graph retrieval | Declarative memory with base-level activation + spreading activation |
| Hook context passed to Claude | Buffer contents (what's "in focus" this cycle) |
| Task/goal state | Goal buffer |
| Session forgetting | Base-level decay (ACT-R's forgetting law: `B = ln(n/t) + β`) |
| Hook firing | Production rule match on buffer contents |

The closest gap ACT-R fills: **principled memory retrieval**. Currently Jarvis uses the LLM to judge what context to inject. ACT-R's activation formula would make that a deterministic, auditable calculation: each primitive gets a score, top-k get injected. No LLM needed for memory selection.

---

## 3. LIDA — Learning Intelligent Decision Agent

### Core Mechanism

LIDA is grounded in **Global Workspace Theory (GWT)**, the cognitive science theory (Bernard Baars) that consciousness arises from a "global workspace" — a broadcast mechanism by which one coalition of specialized processors wins an attention competition and broadcasts its content to all other processors.

LIDA's cognitive cycle (100-300ms):
1. **Understanding phase**: sensory inputs processed by parallel specialist processes into percepts; current situation model (the "workspace") is updated
2. **Attention phase**: competing "codelets" (specialized processors) form coalitions around perceptual content; one coalition wins the attention competition via activation strength
3. **Action selection phase**: winning coalition's content is broadcast globally; action schemes in procedural memory are activated; behavioral stream selects and executes an action

Learning modes: perceptual learning (new percepts), episodic learning (snapshots), procedural learning (new action schemes), and attentional learning (codelets that compete more effectively).

LIDA's key insight: intelligence emerges from *competition among many small specialists*. No central reasoner, no single rule engine. The "intelligent" behavior is a market outcome.

### Maturity and Tooling (2026)

- LIDA Framework: Java-based API from University of Memphis — functional but not actively maintained post-Stan Franklin's retirement
- No mature Python implementation
- Most of the "LIDA" work in 2024-2026 is theoretical or educational; the codebase has not kept pace with the research
- Medical diagnosis and robotics applications exist but are research artifacts

Maturity verdict: **low for engineering use**. The architecture is intellectually rich but the available tooling is a Java framework that requires significant investment. Not recommended as a primary engineering dependency for Jarvis.

### Positioning Relative to LLM

LIDA's most useful concept is the **codelets-as-specialists** pattern: small, focused, fast processes that each detect one kind of situation and advocate for attention. This maps well to specialized hooks — each hook is a codelet. The attention competition mechanism (which coalition of hooks fires?) is currently implicit in Jarvis (hooks run in order, first match wins or all run). LIDA suggests: weight coalitions by activation strength and let the most urgent/relevant win.

### Jarvis Mapping

| Jarvis Component | LIDA Equivalent |
|---|---|
| PreToolUse hooks | Codelets (specialists detecting specific conditions) |
| WWWD gate | Global workspace competition / attention selection |
| Hook activation threshold | Codelet activation strength |
| Multi-hook coalitions | Coalition formation around a situation |

Concept is valuable; tooling is not ready. Extract the pattern, not the library.

---

## 4. CLARION — Connectionist Learning with Adaptive Rule Induction On-line

### Core Mechanism

CLARION (Ron Sun, RPI) is distinguished by its **explicit dual-level architecture**: every subsystem has a top level (explicit, conscious, rule-based) and a bottom level (implicit, unconscious, connectionist/associative). The two levels interact bidirectionally.

Four subsystems:
- **ACS (Action-Centered Subsystem)**: procedural knowledge, action selection; top = explicit rules, bottom = neural associations
- **NACS (Non-Action-Centered Subsystem)**: declarative knowledge, reasoning; top = symbolic facts/rules, bottom = associative memory
- **MS (Motivational Subsystem)**: drives and goals
- **MCS (Metacognitive Subsystem)**: monitors and regulates the other three

The learning dynamic:
- **Bottom-up learning**: implicit associations in the bottom level get extracted and crystallized as explicit rules in the top level (making tacit knowledge explicit)
- **Top-down learning**: explicit rules guide the development of implicit associations (deliberate practice building intuition)

This explicit-implicit interplay was CLARION's claim to fame in cognitive science — it accounts for human data on skill acquisition, verbalization effects, and transfer learning better than purely symbolic or purely connectionist models.

**pyClarion** (2025/2026): a new lightweight open-source Python implementation derived from a 2026 paper analyzing CLARION's essential implementation principles. This is the most engineering-accessible version of CLARION to date.

### Maturity and Tooling (2026)

- pyClarion: Python, open source, 2025-2026 (paper: "Building Intelligent Agents Based on the Clarion Cognitive Architecture: Some Essential Principles," SCITEPRESS 2026)
- Original CLARION: Java/C++ simulation environment (older)
- Active research: Ron Sun's lab at RPI continues publishing
- Limited adoption outside cognitive science research

Maturity verdict: **medium**. pyClarion is new and Python-native, which is promising. The conceptual framework is sound. But the double-level mechanism requires both a symbolic rule engine AND a neural/associative bottom level, which means you need two substrates. For Jarvis, this is either a good fit (the LLM IS the bottom level; CLARION's top level would be the gate layer) or an over-engineering trap.

### Positioning Relative to LLM

CLARION's dual-level architecture maps onto the LLM+rules hybrid naturally:
- **Bottom level** = LLM (implicit, associative, pattern-matching, opaque)
- **Top level** = explicit production rules / gates (transparent, auditable, deterministic)
- **Bottom-up extraction**: when the LLM repeatedly makes the same decision in similar situations, crystallize that into an explicit rule (a new hook). This is bottom-up learning.
- **Top-down refinement**: new explicit rules then shape which contexts the LLM is prompted with, biasing its implicit processing.

This framing is the most philosophically coherent description of what Jarvis is trying to build.

### Jarvis Mapping

| Jarvis Component | CLARION Equivalent |
|---|---|
| Claude LLM | Bottom level (implicit, associative) |
| PreToolUse/PostToolUse hooks | Top level explicit rules (ACS) |
| TRP loop (deriving new primitives) | Bottom-up rule extraction |
| Memory injection shaping Claude output | Top-down learning |
| WWWD decision | MCS (metacognitive regulation) |

CLARION provides the clearest philosophical frame for what Jarvis is doing and where it is going. The bottom-up extraction concept — watching LLM behavior and crystallizing patterns into explicit hooks — is exactly TRP operationalized.

---

## 5. Sigma — Graphical Cognitive Architecture

### Core Mechanism

Sigma (Paul Rosenbloom, USC Institute for Creative Technologies) is the newest major cognitive architecture (2010s-present). Its core claim: cognition can be unified under a single computational substrate — **probabilistic graphical models (factor graphs)** — rather than having separate symbolic and neural components.

Factor graphs provide a uniform representation for:
- Beliefs (as probability distributions over variables)
- Preferences and utilities
- Memories (semantic, episodic, procedural — all encoded as factors)
- Learning (message passing = Bayesian belief propagation)

The **graphical architecture hypothesis**: the long-separate traditions of cognitive architectures and probabilistic graphical models can be merged. The result handles symbols, probabilities, and signals in one representation. Memory retrieval, decision making, perception, and learning are all belief propagation in the same graph.

Sigma targets: grand unification (one mechanism for all cognition), functional elegance (minimal distinct components), generic cognition (not human-modeling fidelity), and sufficient efficiency (≤50ms per cognitive cycle for real-time virtual humans).

### Maturity and Tooling (2026)

- BSD 2-clause open source release available (cogarch.ict.usc.edu)
- Rosenbloom remains active: 2025 publication "In search of insight: My life as an architectural explorer" (*Journal of Artificial General Intelligence*, 15, 3-61)
- The implementation language is not Python-native (Lisp-based kernel)
- Small team; less community than SOAR or ACT-R
- Primary use: virtual human agents for US Army training simulations

Maturity verdict: **low-to-medium for external use**. Sigma is intellectually at the frontier — the graphical unification idea is genuinely elegant and theoretically sound. But it is a research system developed by a small team for a specific institutional context. The tooling investment for non-USC groups is significant.

### Positioning Relative to LLM

Sigma's probabilistic graphical model foundation makes it the most natural architecture for hybrid uncertainty quantification. Where SOAR says "fire the matching rule" and ACT-R says "retrieve the highest-activation chunk," Sigma says "perform belief propagation and output a probability distribution over actions."

For LLM integration, Sigma would let the system maintain explicit uncertainty over its beliefs, goals, and plans — not just a point estimate. This matters when Jarvis is reasoning about things like "how confident am I that this gate should fire?" or "what is the probability this tool call will fail?"

### Jarvis Mapping

Sigma's concepts are most useful as inspiration rather than direct adoption:
- Gates as factor nodes (each gate contributes a factor to the posterior over "what should happen")
- Memory retrieval as belief propagation (the most relevant primitive is the one with highest posterior given the current context)
- Goal selection as utility maximization in the factor graph

---

## 6. NARS / OpenNARS — Non-Axiomatic Reasoning System

### Core Mechanism

NARS (Pei Wang, Temple University) is the architecture whose design assumptions most directly match Jarvis's operating conditions. Its founding premise:

> **"Intelligence is the ability to adapt to the environment while working with insufficient knowledge and insufficient resources."**

Classical logic assumes complete knowledge. Bayesian probability assumes a prior. NARS assumes neither. Every statement has a **truth value as a (frequency, confidence) pair**:
- **frequency** `f ∈ [0,1]`: proportion of positive evidence among total evidence
- **confidence** `c ∈ [0,1)`: how stable the frequency is (approaches 1 as evidence accumulates, never reaches it — no absolute truth)

Truth value `<1, 1>` (perfect frequency, perfect confidence) is a limit that can be asymptotically approached but never claimed. This is epistemically honest: NARS can never assert certainty.

The inference engine implements **Non-Axiomatic Logic (NAL)**, structured in nine layers:
- NAL 1-6: propositional and predicate logic with inheritance relations, compound terms, higher-order statements
- NAL 7: temporal reasoning (sequences, intervals between events)
- NAL 8: procedural knowledge (goals, operations, sensorimotor coupling)
- NAL 9: self-reference (the system reasoning about its own reasoning)

Inference types: deduction, abduction, induction, revision, analogy, comparison, conjunction, disjunction, negation. Each has a truth-value formula that propagates uncertainty from premises to conclusions.

**Revision rule**: when two beliefs with the same content but different (f, c) pairs are encountered, they are merged using a formula that increases confidence as evidence accumulates. New evidence can raise or lower frequency.

**Working memory / attention**: NARS has a bounded memory. Concepts are retained by priority (a combination of short-term urgency and long-term utility). When resources are constrained, lower-priority concepts are forgotten. This is not a bug — it is the design for operating under resource constraint.

**Goals**: first-class objects in the same representation as beliefs. A goal `G` with truth value `(f, c)` means "I expect/desire state G with frequency f and confidence c." Goals drive backward chaining to find operators that achieve them.

**Three data types**: Beliefs (past experience), Questions (information requests), Goals (desired states). All processed by the same inference machinery.

### Maturity and Tooling (2026)

Multiple active implementations:

**OpenNARS for Applications (ONA)**
- GitHub: https://github.com/opennars/OpenNARS-for-Applications
- Written in C (fast, lean, embeddable)
- Python interface for interactive use + English NL input via NLTK
- Latest release: v0.9.3, April 22, 2025 (119 stars, 1,753 commits — genuinely active)
- Designed for real-time application embedding, not just research demos
- Supports sensorimotor coupling: dozens of events per second

**NARS-GPT**
- GitHub: https://github.com/opennars/NARS-GPT
- GPT (any OpenAI-compatible LLM) as language channel → ONA as reasoning engine
- LLM translates natural language to Narsese; ONA does the inference
- No context window limitation: beliefs stored in ONA's bounded memory, not LLM context
- Last updated January 2025; April 2025 ONA release includes NARS-GPT compatibility overhaul
- Supports long-term learning: new beliefs persist across sessions in ONA memory

**OpenNARS for Research (3.0+)**
- GitHub: https://github.com/opennars/opennars
- Java, more feature-complete but slower
- Research-oriented; includes all nine NAL layers

**Neuro-Symbolic Benchmark (arXiv 2604.18873, 2025)**
- Pipeline: NL → FOL → Narsese → ONA execution
- NARS-Reasoning-v0.1: 1,000 instances (easy/medium/hard), three-label (True/False/Uncertain)
- Phi-2 LoRA fine-tuned on the pipeline achieves competitive results
- Key finding: "strong language generation should not be confused with reliable reasoning" — LLMs hallucinate reasoning; ONA executes it correctly

**Revised foundational textbook** (*Non-Axiomatic Logic: A Model of Intelligent Reasoning*) planned for 2025 publication.

Maturity verdict: **high for ONA specifically**. ONA is a production-ready C binary with Python scripting, an active maintainer (Patrick Hammer), and real-world deployments in robotics and surveillance. The NARS-GPT pattern is working code, not a research prototype. The theoretical foundation is unusually coherent and well-documented.

### Why NARS Fits Jarvis Best (Detailed Analysis)

Jarvis's fundamental operating condition: **insufficient knowledge and insufficient resources**. Claude does not know what Will would do in every situation. The hook system cannot anticipate every tool call pattern. The memory graph cannot hold everything. This is exactly the NARS design assumption.

Specific matches:

**1. Gates as belief revision**
Currently Jarvis hooks fire or don't — binary. NARS would let each hook maintain a belief with (frequency, confidence) about whether the gate should fire. A new hook starts with `(0.5, 0.1)` — uncertain, low confidence. Over time, as it fires correctly or incorrectly, the confidence rises and the frequency converges to the true base rate. The hook system becomes self-calibrating.

**2. WWWD as goal arbitration**
NARS goals have truth values. When multiple goals compete (complete the task fast vs. don't OOM the machine vs. maintain context coherence), NARS has a principled way to arbitrate: goals with higher desirability × confidence win. Currently WWWD is an LLM judgment call. NARS would make it an inference.

**3. Memory graph as NARS concepts**
Each markdown primitive could be a NARS concept — a term with associated beliefs, questions, and goals. Retrieval would be by attention budget (how much priority does this concept have given the current task?) rather than LLM context injection. NARS's attention mechanism is built for bounded memory.

**4. Procedural knowledge (NAL 8)**
NAL 8 handles operations (tool calls, hook firings) as goals with procedural preconditions. This is exactly Jarvis's hook execution model, formalized.

**5. No axioms = no brittleness**
SOAR requires correct production rules or it impasses. NARS will always produce an answer under uncertainty — it just has lower confidence. This is more robust for a harness that runs continuously without human oversight.

**Integration sketch (buildable now)**:
```
Claude output → NARS-GPT (ONA) → parse LLM assertions into Narsese beliefs
ONA reasoning cycle → update belief/goal graph
ONA goal activations → inform which hooks to emphasize next turn
Hooks that fire → feed back as confirmatory/disconfirmatory evidence to ONA
ONA memory → persisted between sessions (replacing/augmenting markdown graph)
```

---

## Cross-Cutting Observation: CLIPS as a Production-Rules Bridge

Before the top-3 ranking, one honorable mention deserves attention because it is immediately installable today with no research investment:

**CLIPS** (C Language Integrated Production System, NASA/Johnson Space Center, 1985-1996, still maintained):
- Python bindings: `clipspy` 1.0.6 (Oct 2025, pip-installable, CLIPS 6.4x)
- Extended fork: `clipspyx` (Mar 2026, CLIPS 7.0 support, async, certainty factors, backward chaining)
- NeuSymMS (2025, arXiv 2605.17596): production-ready system using CLIPSPy as the memory management engine for LLM agents — facts as RDF-style triples, CLIPS rules for conflict resolution, PostgreSQL for persistence
- CLIPS is essentially the production-rule engine from cognitive architectures, extracted and packaged

CLIPS is not a full cognitive architecture but it gives you the most immediately engineerable piece — production rules with forward chaining — without the overhead of adopting a whole cognitive architecture. If Jarvis's hooks are currently Python functions, CLIPS would replace them with a formal rule engine that has conflict resolution, agenda management, and fact retraction built in. `clipspyx`'s certainty factors are essentially a CLIPS-native approximation of NARS truth values.

---

## Top 3 Adoptable-for-Jarvis: Ranked

### Rank 1: NARS / OpenNARS for Applications (ONA)

**Why**: Best philosophical fit. ONA is the only architecture explicitly designed for insufficient knowledge and resources. Its (frequency, confidence) truth values let gates and beliefs self-calibrate without training. It has a working LLM integration pattern (NARS-GPT) with open-source code. The C binary is fast and embeddable.

**What it fills**: The gap between "LLM said X" and "we have evidence X is right." NARS lets Jarvis maintain calibrated beliefs about the reliability of its own gates, memories, and decisions. Over time the system becomes epistemically self-aware.

**Buildable now**: Yes. ONA is on PyPI-accessible via GitHub, the Python shell is functional, and NARS-GPT shows exactly how to wire GPT-class LLMs as the language channel. The integration would be:
1. Install ONA (build from C source or use provided binary)
2. After each Claude output, run it through a Narsese parser (similar to NARS-GPT's NL→Narsese step, adapted to Jarvis's structured outputs)
3. Feed parsed beliefs/goals into ONA
4. Read ONA's current goal activations at the start of each WWWD cycle to inform Claude's context
5. Hook fire/no-fire results feed back as evidence to ONA

**Honest caveats**: Learning Narsese has a curve. ONA's Python interface is functional but not polished. For NAL 7-9 (temporal, procedural, self-referential), the documentation is thinner. Start with NAL 1-4 only.

---

### Rank 2: CLIPS / CLIPSPy (Production Rules Engine)

**Why**: Most immediately buildable. CLIPS is a production-rule engine with 40 years of refinement, `pip install clipspy`, and a 2025-2026 paper (NeuSymMS) showing exactly how to use it as the gate/memory layer over an LLM. Not a full cognitive architecture, but it gives you the most valuable piece — deterministic, auditable, conflict-resolving rule firing — with near-zero adoption cost.

**What it fills**: Replaces or augments Jarvis's Python hooks with a proper rule engine. Instead of Python functions that run in sequence, you get CLIPS rules that pattern-match on a fact base, have explicit priority (salience), and are managed by an agenda. `clipspyx` adds certainty factors (rudimentary truth values) and backward chaining.

**Buildable now**: Yes, today. `pip install clipspy` or `pip install clipspyx`. The NeuSymMS architecture is a direct blueprint: extract facts from LLM output → CLIPS rules classify/resolve/update fact base → persist to storage → inject as context into next LLM call.

**Integration sketch**:
```python
import clips  # clipspy

env = clips.Environment()
env.load("jarvis_rules.clp")  # load production rules

# After LLM output:
env.assert_string(f'(tool-call (name "{tool_name}") (args "{args}"))')
env.run()  # fire all applicable rules

# Read agenda decisions:
for fact in env.facts():
    if fact.template.name == "gate-decision":
        decision = fact["action"]  # block, allow, warn
```

**Honest caveats**: CLIPS is not a full cognitive architecture. It lacks: goal stacks (you build these), episodic memory (you build this), learning (rules don't update themselves — you need to add that). `clipspyx`'s certainty factors help but are not as theoretically grounded as NARS. Think of CLIPS as the production-rule skeleton onto which you graft other components.

---

### Rank 3: SOAR (Long-term substrate target)

**Why**: SOAR is the most complete working cognitive architecture with Python bindings, active research, and a proven pattern for LLM integration (impasse-driven LLM queries). The chunking mechanism — automatically compiling deliberate problem-solving into production rules — is exactly the process Will wants to make explicit: Claude solves something novel, that solution gets encoded as a permanent gate.

**What it fills**: A genuine cognitive cycle with goal tracking, operator selection, memory systems (procedural + semantic + episodic), and learning. If Jarvis is going to become a real cognitive architecture over time rather than just an orchestration harness, SOAR is the most mature and best-documented path.

**Buildable now**: Partially. The Python SML bindings work. The cost is authoring SOAR rules (Soar rule language, not Python). NL2GenSym (2025) partially automates this via LLM. A realistic path: use SOAR for the goal/subgoal management layer only, with Claude handling the "body" of each operator application.

**Integration sketch (impasse-LLM pattern)**:
1. SOAR agent manages the task hierarchy (what is the current goal? what operator should apply?)
2. When SOAR impasses (no production rule matches the current situation), call Claude as the oracle
3. Claude's response + suggested rule → add to SOAR's procedural memory
4. SOAR then handles future similar situations without Claude

Over time, SOAR's procedural memory grows richer; Claude's involvement shrinks for known problem types.

**Honest caveats**: SOAR has a steep onboarding curve. The rule language is not Python. VisualSoar (the IDE) is aging. For Jarvis at current scale, the engineering investment is high relative to immediate return. This is a 6-12 month investment to get real leverage, not a weekend project. Start with CLIPS/NARS first; graduate to SOAR if the rule base grows large enough to need SOAR's infrastructure.

---

## Aspirational vs. Buildable: Honest Assessment

| Architecture | Concept Value | Buildable Today | Time to First Value |
|---|---|---|---|
| NARS / ONA | Very high | Yes (ONA + NARS-GPT) | 1-2 weeks |
| CLIPS / CLIPSPy | High (scoped) | Yes (pip install) | 1-3 days |
| SOAR | Very high | Medium (rule authoring overhead) | 4-8 weeks |
| CLARION | High (frame) | Low (pyClarion new/thin) | 8+ weeks |
| ACT-R / PyACT-Up | Medium | Medium (PyACT-Up scoped) | 2-4 weeks (memory only) |
| LIDA | Medium (concept) | Low (Java, unmaintained) | Not recommended |
| Sigma | High (theory) | Low (research system) | Not recommended |

**Key principle**: the CLARION dual-level frame (LLM = implicit bottom level, hooks = explicit top level, TRP = bottom-up extraction) is the philosophically correct description of what Jarvis is building — even if pyClarion itself is not the right tooling. You can adopt CLARION's conceptual frame without adopting its implementation.

---

## Summary Recommendation

The path forward is layered:

**Layer 1 (now)**: Install `clipspyx`, convert Jarvis's hook dispatch into a CLIPS fact base with an agenda. This gives you production-rule semantics, conflict resolution, and salience ordering without any research investment.

**Layer 2 (1-2 weeks)**: Wire ONA (NARS) as the belief layer. Each hook fire/no-fire becomes evidence that updates an ONA belief. WWWD goal arbitration reads ONA's current goal activations. Jarvis starts accumulating calibrated beliefs about its own behavior.

**Layer 3 (months)**: As the rule base grows complex enough, migrate goal/subgoal management to SOAR. Use the NL2GenSym pattern to have Claude generate SOAR rules from observed behavior.

The conceptual frame throughout is CLARION: Claude is the implicit bottom level, the hook/gate system is the explicit top level, and TRP is the ongoing bottom-up extraction of tacit LLM knowledge into explicit rules.

---

*Sources consulted*:
- https://soar.eecs.umich.edu/
- https://github.com/SoarGroup/Soar
- https://github.com/opennars/OpenNARS-for-Applications
- https://github.com/opennars/NARS-GPT
- https://cis.temple.edu/~pwang/NARS-Intro.html
- https://arxiv.org/abs/2510.09355 (NL2GenSym)
- https://arxiv.org/abs/2403.00810 (Bootstrapping Soar with LLM)
- https://arxiv.org/html/2604.18873v1 (NL→Narsese pipeline)
- https://arxiv.org/abs/2309.02427 (CoALA: Cognitive Architectures for Language Agents)
- https://arxiv.org/html/2605.17596v1 (NeuSymMS: CLIPSPy + LLM)
- https://clipspy.readthedocs.io/
- https://pypi.org/project/clipspyx/
- https://ict.usc.edu/research/labs-groups/cognitive-architecture/ (Sigma)
- https://cogarch.ict.usc.edu/
- https://cis.temple.edu/tagit/publications/TAGIT-TR-21.pdf (NARS in MeTTa, 2024)
- pmc.ncbi.nlm.nih.gov/articles/PMC7805877/ (Self in NARS)
- https://www.scitepress.org/Papers/2026/144968/144968.pdf (pyClarion, 2026)
- https://github.com/KRaizer/Soar-Python-Minimum-Working-Example
- Wikipedia articles on Soar, ACT-R, LIDA, CLARION, Sigma
