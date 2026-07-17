# VSA / Hyperdimensional Computing + OpenCog Hyperon
## Dossier for JARVIS Non-LLM Intelligence Research

**Cluster:** Vector Symbolic Architectures + OpenCog Hyperon
**Date:** 2026-07-16
**Researcher:** JARVIS (sonnet-4-6)
**Context:** JARVIS is a deterministic Python harness wrapping Claude — hooks, file-based memory graph (markdown primitives linked by `[[wikilinks]]`), crons, subagents, WWWD decision gate, and ETM philosophy (Economic Theory of Mind: mind = economy, state-rent as allocation mechanism). The goal is to move reasoning from LLM weights into explicit structure — "logical primitives, circuits."

---

## Introduction

This dossier covers two closely related but distinct families of non-LLM AI relevant to JARVIS:

1. **Vector Symbolic Architectures (VSA) / Hyperdimensional Computing (HDC)** — an algebraic framework that encodes symbolic structures as random high-dimensional vectors and computes over them with binding, bundling, and permutation operations. The conceptual payoff: VSA could transform JARVIS's flat `[[wikilink]]` graph into a vector algebra you can actually *compute over* — querying, composing, and traversing primitives without an LLM call.

2. **OpenCog Hyperon** — a live AGI research platform built around a probabilistic-symbolic metagraph (AtomSpace), a reflexive programming language (MeTTa), economic attention allocation (ECAN), and probabilistic logic (PLN). Its core data structure (a weighted knowledge hypergraph with an attention economy) is structurally close to JARVIS's memory graph + ETM. The mapping is real but has limits that must be stated honestly.

Both are explored with concrete technical depth. The final section maps to JARVIS and proposes three adoptable integrations.

---

## Part 1: Vector Symbolic Architectures (VSA) / Hyperdimensional Computing

### 1.1 Core Mechanism

VSA is a family of computational frameworks, not a single algorithm. All variants share:
- A **high-dimensional vector space** (typically D = 1,000–10,000 dimensions)
- A small set of **algebraic operations** on these hypervectors
- The **concentration of measure** property: in high dimensions, random vectors are nearly orthogonal — you can pack exponentially many (~2^D) quasi-orthogonal symbols into fixed dimensionality

The three fundamental operations:

| Operation | Symbol | What it does | Implementation (MAP-Bipolar) |
|---|---|---|---|
| **Binding** | ⊗ | Encodes a role-filler pair (key-value) | Element-wise multiplication |
| **Bundling** | + | Superposition of concepts into a set | Element-wise addition |
| **Permutation** | ρ | Encodes order or positional structure | Cyclic shift |

**Canonical example of knowledge encoding:**

```
# Hypervectors for atoms
CAPITAL = random_hv()
COUNTRY = random_hv()
FRANCE  = random_hv()
PARIS   = random_hv()

# Encode "the capital of France is Paris" as a single hypervector:
fact = bind(CAPITAL, PARIS) + bind(COUNTRY, FRANCE)

# Query: "What is the capital of France?"
query_result = unbind(fact, CAPITAL)
# query_result ≈ PARIS (cosine similarity retrieval from codebook)
```

The unbinding operation recovers the filler from a role-value pair. Because bundling stores multiple associations in one vector, unbinding introduces a noise term from interference — but similarity search against a codebook of known hypervectors recovers the correct answer as long as the bundle has fewer than ~D/2 entries.

### 1.2 VSA Variants

Five families matter for JARVIS, each with different binding operations:

- **MAP-Bipolar (MAP-B):** Real-valued vectors in {−1,+1}^D. Binding = elementwise multiply. Self-invertible. Most mathematically convenient.
- **Binary Spatter Codes (BSC):** Binary {0,1}^D. Binding = XOR. Fast on hardware, biologically plausible.
- **Holographic Reduced Representations (HRR):** Complex or real-valued. Binding = circular convolution. Allows nested structure encoding; unbinding is approximate via cross-correlation.
- **Multiply-Add-Permute (MAP):** Generalizes BSC and MAP-B.
- **Tensor Product Representations (TPR):** Smolensky's formulation. Exact unbinding via tensor contraction. More expensive but useful for strict role-filler semantics.

For JARVIS's use case (text-level primitives, Python substrate, moderate dimensions), MAP-B or BSC via `torchhd` are the practical entry points.

### 1.3 VSA as Graph Computation

The December 2025 VS-Graph paper (Poursiami et al., arXiv:2512.03394) is directly relevant. Key result: multi-hop graph traversal and neighborhood aggregation can be performed entirely inside hyperdimensional space — no backpropagation, no GNN weight training — at 250–450x speedup over GNNs, with 4–5% accuracy improvement over prior HDC baselines.

The mechanism:
1. **Spike Diffusion** assigns each node a topology-derived rank
2. Rank → unique random binary hypervector (structural identity)
3. **Associative Message Passing** aggregates multi-hop neighborhoods by bundling neighbor hypervectors

This is the key insight for JARVIS: a `[[wikilink]]` graph can be encoded so that multi-hop traversal (e.g., "what primitives are reachable from WWWD within 2 hops?") becomes a single vector operation, not a graph walk.

### 1.4 VSA + LLMs: 2024–2025 Results

**Hyperdimensional Probe (arXiv:2509.25045):** Uses VSA codebooks to decode LLM internal representations. The LLM produces an embedding; VSA binding/unbinding operations extract the symbolic structure latent in it. This is the "VSA as a queryable lens on LLM internals" direction.

**Attention as Binding (arXiv:2512.14709):** Reinterprets transformer attention through the VSA lens — self-attention is formally equivalent to approximate VSA binding/unbinding. The mathematical connection between what transformers do and what VSA does is tighter than previously understood.

**IBM Neuro-Vector-Symbolic Architecture (NeuroVSA):** IBM Research's ongoing project combining symbolic AI + neural networks via VSA. Publications at NeSy 2024, NeurIPS 2025, AAAI 2025. Focus on few-shot continual learning with dynamic memory, Raven's Progressive Matrices (abstract reasoning), and hardware co-design with phase-change memory.

**NeuSymMS (arXiv:2605.17596):** Hybrid neuro-symbolic memory system for LLM agents, integrating VSA-style structured storage with LLM retrieval.

The practical takeaway: VSA and LLMs are increasingly used together, not as competitors. VSA provides the *explicit structure*; the LLM provides the *semantic embedding and natural language interface*. The LLM reads/writes to a VSA memory bundle; VSA provides algebraic query/traversal without LLM calls.

### 1.5 Tooling: Torchhd

**Torchhd** (PyPI: `torchhd`, JMLR 2023) is the canonical Python library for VSA/HDC research. Key facts:
- Builds on PyTorch; GPU-accelerated
- Supports: Binary Spatter Codes, MAP (bipolar), Holographic Reduced Representations, Sparse Block Codes, Vector-Derived Transformation Binding (VTB)
- Active maintenance: v5.8.4 released June 2025; v5.7.1 October 2024
- Up to 100x faster than reference implementations
- Install: `pip install torchhd`

Basic usage sketch:
```python
import torchhd

D = 10000  # dimensionality

# Create random hypervectors for concepts
primitives = torchhd.random(num_vectors=100, dimensions=D, model="MAP")

# Bind two concepts (role-filler pair)
bound = torchhd.bind(primitives[0], primitives[1])

# Bundle multiple concepts (superposition)
bundle = torchhd.bundle(primitives[0:5])

# Query: similarity search against codebook
scores = torchhd.cosine_similarity(bundle, primitives)
```

Torchhd is production-ready for research; JARVIS could adopt it today without waiting for stabilization.

### 1.6 Maturity Assessment

- **Mathematical foundations:** Extremely mature (Kanerva 1988, Plate 1995, extensive ACM survey 2022)
- **Torchhd library:** Production-ready for research, active maintenance
- **LLM integration patterns:** Emerging (2024–2025 papers), not yet standardized
- **Knowledge graph application:** VS-Graph (2025) proves feasibility; library support (graph → hypervector) is DIY
- **Limitations:** Approximate retrieval (noise from superposition), capacity limited by D, not yet a drop-in for complex symbolic reasoning

---

## Part 2: OpenCog Hyperon

### 2.1 What Hyperon Is (and Is Not)

OpenCog Hyperon is an AGI research platform developed by SingularityNET and associated labs. It is **not** a deployable product — it is explicitly at "pre-alpha" stage as of early 2025. It matters for JARVIS because its architecture embodies exactly the philosophy JARVIS is trying to implement: a metagraph-structured knowledge base with an attention economy driving which parts are processed, a logic layer for uncertain reasoning, and LLMs plugging in as specialized modules rather than being the substrate.

Two foundational components:
1. **Distributed AtomSpace (DAS)** — the hypergraph knowledge repository
2. **MeTTa** — a reflexive, self-modifying programming language for cognitive computation

### 2.2 AtomSpace: The Hypergraph Knowledge Store

AtomSpace is a hypergraph database where:
- **Nodes** represent concepts, entities, truth values, functions
- **Links** (hyperedges) represent n-ary relationships — not just binary edges but arbitrary arity
- Every Atom (node or link) carries an **AttentionValue** (STI + LTI)
- Every Atom carries a **TruthValue** — a probability + confidence pair (for PLN)

Knowledge of all types lives in the same space: declarative facts, linguistic relations, mathematical assertions, procedural rules, goal representations, sensorimotor data. This is deliberate — Hyperon's cognitive model depends on cognition types that *cross-reference* each other.

The AtomSpace supports:
- RAM-resident (fast cognitive cycle)
- Disk-resident (persistent storage)
- Distributed (DAS = distributed AtomSpace across machines)

Queries are written as patterns — expressions containing variables (`$x`) — and matched against the AtomSpace via two-sided unification (the pattern and the stored atom can both contain variables).

### 2.3 MeTTa: The Reflexive Language

MeTTa (Meta Type Talk) is "Atomese 2" — a successor to OpenCog Classic's Atomese query language. It is simultaneously:
- A functional language (evaluates expressions)
- A logic language (supports unification/pattern matching)
- A meta-language (programs can modify the AtomSpace they run in — self-modifying)

Core syntax mechanics:

```metta
; Store an atom (no ! prefix = stored, not evaluated)
(capital paris france)

; Evaluate an expression (! prefix = evaluate and return result)
!(match &self (capital $x france) $x)
; Returns: paris

; Add an atom programmatically
!(add-atom &self (capital berlin germany))

; Two-sided unification example:
; AtomSpace contains: (A ($a $a) A)
; Query: ($b (B B) $b) — matches because $a→B and $b→A
```

The `!` prefix triggers evaluation; without it, the expression is stored into the AtomSpace. This makes MeTTa programs simultaneously a query engine and a data population mechanism.

MeTTa is implemented in Rust; Python bindings exist via `pip install hyperon` (v0.2.2, January 2025). Status: pre-alpha, 4,096+ commits, active development.

### 2.4 ECAN: Economic Attention Allocation

ECAN (Economic Attention Networks) is the attention subsystem. This is where the ETM isomorphism lives most concretely.

**Two currencies:**
- **STI (Short-Term Importance):** Guides which atoms receive processing cycles *right now*. Atoms with STI above a threshold are in the "Attentional Focus" — effectively working memory.
- **LTI (Long-Term Importance):** Guides which atoms remain in RAM vs. get paged to disk/cold storage.

**Economic mechanics:**
- Atoms compete for attention using artificial economics — STI/LTI values function as currency
- **HebbianLinks** record co-activation history: if atom A was used and atom B was used together, the HebbianLink A→B grows stronger
- Currency flows: when atom B is processed, it pays STI to atoms that helped cause B's activation (Hebbian reinforcement)
- ECAN spreads attention across the hypergraph, creating self-organizing foci of processing

**Working memory = Attentional Focus = {atoms with STI > threshold}**

This is formally equivalent to the JARVIS ETM concept where state-rent allocates "mind-space" to active primitives — except Hyperon's version is dynamic and automatic while JARVIS's ETM is currently a philosophy rather than an implemented mechanism.

**Implementation status of ECAN:** The original C++ ECAN implementation is deprecated ("one of the OpenCog Fossils"). A new MeTTa-native ECAN implementation is actively in progress at `iCog-Labs-Dev/metta-attention` (GitHub). Research in 2024–2025 is also exploring information geometry (natural gradient) approaches to dramatically improve ECAN's effectiveness vs. the original Hebbian method. ECAN is real but not yet production-stable in Hyperon.

### 2.5 PLN: Probabilistic Logic Networks

PLN is Hyperon's uncertain inference engine. Key properties:
- Combines higher-order fuzzy logic with probabilistic reasoning and predicate/term logic
- Represents truth as **second-order distributions** (probability of probability — distributions over distributions) for robust uncertainty handling
- Supports induction, abduction, analogy, temporal reasoning, causal reasoning all within one formalism
- The "biggest challenge" (per the developers) has always been inference control — which inference steps to run in which order. A proof-of-concept using the Hyperon/MeTTa chainer is underway.

PLN is being ported from OpenCog Classic C++ to MeTTa-native. Repositories: `trueagi-io/pln-experimental` and `trueagi-io/PLN`. Status: active port, not production-ready.

For JARVIS, PLN matters as the "uncertain reasoning" layer that could replace ad-hoc LLM judgment calls about which primitives apply in which context.

### 2.6 PRIMUS: The Cognitive Architecture

Hyperon's highest-level cognitive model is PRIMUS. Structure:
- **Working memory** = Attentional Focus (ECAN-governed)
- **Declarative memory** = general AtomSpace knowledge
- **Procedural memory** = MeTTa programs stored in the AtomSpace (they can modify themselves)
- **Attentional focus** drives a rapid goal-directed cognitive cycle
- **LLMs, formal reasoning engines, evolutionary program learners** plug in as specialized "lobes" — external modules that read/write to AtomSpace but are not the integrative substrate

This is important: in PRIMUS, LLMs are *peripherals* to the symbolic substrate, not the substrate itself. This is exactly the inversion JARVIS is moving toward.

### 2.7 Hyperon's Roadmap and Funding Context

- SingularityNET awarded >$1M in grants across 13 Hyperon challenges (November 2024)
- A $1.25M RFP in early 2025, funding 14 projects accelerating Hyperon/MeTTa
- Target: production-ready Hyperon stack by late 2025 (ambitious; pre-alpha is still the reality)
- AGI-level claims are speculative and far out; the *technical substrate* (AtomSpace + MeTTa) is real, open-source, and increasingly usable

The SingularityNET context is worth noting: Hyperon is embedded in a broader ecosystem (ASI Alliance, AGIX token, SingularityNET decentralized AI) which means organizational/incentive considerations may affect which components mature fastest.

---

## Part 3: ETM/AtomSpace Isomorphism Assessment

This is the most important conceptual section. The claim is that JARVIS's ETM (Economic Theory of Mind: mind = economy, state-rent as allocation mechanism) is "strikingly close" to Hyperon's AtomSpace + ECAN. Here is an honest decomposition.

### Where the Resemblance is Real

| JARVIS Concept | Hyperon Equivalent | Isomorphism Strength |
|---|---|---|
| Memory graph (markdown primitives + `[[wikilinks]]`) | AtomSpace (nodes + hyperedge links) | **STRONG** — Both are typed knowledge hypergraphs. The wikilink graph has essentially the same topology as AtomSpace, just with different encoding (Markdown files vs. typed Atoms). |
| ETM "state-rent" as allocation signal | ECAN LTI (Long-Term Importance) — gates what stays in RAM | **STRONG** — Functionally identical: both use a resource cost signal to determine which knowledge remains in active cognitive space. |
| Active context / working primitives | ECAN Attentional Focus (STI > threshold) | **STRONG** — Both define "working memory" as the subset of the knowledge graph that is currently "funded" for processing. |
| Primitive interdependencies / `[[wikilinks]]` | HebbianLinks tracking co-activation | **MODERATE** — Wikilinks are hand-authored dependencies; HebbianLinks are auto-learned from co-activation. The data structure is isomorphic but the acquisition mechanism is different. |
| WWWD decision gate | PLN inference + ECAN attention | **MODERATE-WEAK** — WWWD is a single LLM call ("what would Will do?"). PLN + ECAN would replace it with a traversal of uncertain-logic rules over the AtomSpace. Functionally convergent but mechanistically very different. |
| Hook gates (PreToolUse, PostToolUse) | MeTTa pattern-match triggers | **MODERATE** — Both are "if pattern then action" rules. JARVIS hooks are Python closures registered against Claude SDK events; MeTTa programs are stored in AtomSpace and execute on pattern matches. Same pattern, different substrate. |
| ETM "consciousness propagation" | PRIMUS cognitive cycle | **WEAK** — Philosophically related (both model mind as an economic substrate) but PRIMUS is a concrete engineering spec while ETM is a philosophical frame that has not been fully operationalized in JARVIS. |

### Where the Resemblance is Superficial

1. **AtomSpace is a typed hypergraph engine with a real query planner and two-sided unification.** JARVIS's wikilink graph is a set of Markdown files with manual cross-references. The *topology* is similar; the *computational capabilities* are incomparable. AtomSpace can execute pattern queries across millions of atoms; the JARVIS memory graph currently requires an LLM to "traverse" it.

2. **ECAN's economics are dynamic and auto-updating from actual computation history.** JARVIS's ETM is a framing philosophy — it describes why certain structures matter but does not automatically update attention weights based on access patterns. The difference is "philosophy that resembles the design" vs. "implemented mechanism."

3. **PLN's probabilistic truth values are a formal mathematical object** (second-order distributions). JARVIS has no formal uncertainty calculus; the LLM's uncertainty is implicit in its output tokens. These are not the same thing.

4. **MeTTa's self-modification** (the AtomSpace can contain and execute programs that modify the AtomSpace) is substantially different from JARVIS's hook system, which is static Python code registered at session start. JARVIS cannot write a new hook to disk and have it execute in the same session.

**Summary:** The structural topology is genuinely isomorphic (both are knowledge hypergraphs with attention economics). The *implementation gap* is large. The ETM gives JARVIS a correct design target that Hyperon has partially built. The right framing: ETM predicted the Hyperon architecture by different reasoning — they are converging on the same design space.

---

## Part 4: Top 3 Adoptable-for-JARVIS Integrations

### Integration 1: VSA Hypervector Index over the JARVIS Memory Graph

**What it is:** Encode every JARVIS primitive (each `.md` file) as a hypervector. `[[wikilinks]]` become binding operations. The bundle of all primitives in a category (e.g., all COMM primitives) becomes a superposition hypervector. Queries ("which primitives are relevant to this situation?") become similarity searches.

**Why it matters:** Currently, context selection requires either the LLM to read all memory files or a manual routing system. VSA provides a vector algebra over the graph that supports multi-hop retrieval and similarity-based activation without LLM calls.

**Concrete sketch:**

```python
import torchhd
import os

D = 10000
primitive_files = glob("~/.claude/memory/*.md")
primitive_hvs = {}

for path in primitive_files:
    name = os.path.basename(path).replace(".md", "")
    primitive_hvs[name] = torchhd.random(1, D, model="MAP").squeeze()

# Encode wikilinks as binding
for path in primitive_files:
    links = extract_wikilinks(path)  # parse [[...]] references
    name = os.path.basename(path).replace(".md", "")
    for link in links:
        if link in primitive_hvs:
            # Bind source primitive to its linked primitive
            edge_hv = torchhd.bind(primitive_hvs[name], primitive_hvs[link])
            primitive_hvs[name] = torchhd.bundle(
                torch.stack([primitive_hvs[name], edge_hv])
            )

# At query time: given a situation description embedded as a hypervector,
# find the most relevant primitives via cosine similarity
def query_memory_graph(situation_embedding_hv, top_k=5):
    all_hvs = torch.stack(list(primitive_hvs.values()))
    scores = torchhd.cosine_similarity(situation_embedding_hv, all_hvs)
    return top_k_primitives(scores)
```

**Gap to fill:** Encoding a natural language situation as a hypervector. The cleanest path: use an LLM embedding of the situation, then project it into hypervector space via a random projection matrix (a known technique). This keeps LLMs for NL understanding; VSA handles the graph query.

**Effort:** The Torchhd wiring is 1–2 days. The real work is the unfilled gap: producing a situation hypervector from natural language. The random-projection-from-LLM-embedding approach is a known technique but requires experimentation to tune (projection dimensionality, normalization, retrieval threshold). Realistic estimate: 1 week to a prototype that produces non-trivial retrieval results. Whether it beats keyword matching on JARVIS's actual primitive set (~40–100 primitives) is unverified — the VSA literature demonstrates this on classification benchmarks, not on small hand-authored knowledge graphs. Calibration timeline unknown; treat this as experimental until benchmarked against JARVIS's real retrieval tasks.

**Limitation:** Approximate retrieval — some relevant primitives will be missed, irrelevant ones surface. Requires tuning D and codebook design. Not a replacement for careful manual primitive authoring.

---

### Integration 2: AtomSpace as JARVIS Working Memory (MeTTa-Python bridge)

**What it is:** Replace JARVIS's session state (currently `SESSION_STATE.md` + `WAL.md` flat files) with a local AtomSpace instance. Active primitives are loaded as Atoms with high STI. Completed task contexts decay in STI and eventually drop to disk (LTI-governed persistence). MeTTa pattern queries replace the LLM's job of "figure out which rule applies here."

**Why it matters:** The current JARVIS session state is a flat text file that the LLM has to interpret. An AtomSpace would provide structured, queryable working memory with typed relationships and automatic attention-driven decay. The ETM's state-rent philosophy becomes mechanistically implemented rather than just described.

**Concrete sketch:**

```python
from hyperon import MeTTa

metta = MeTTa()

# Load a JARVIS primitive as an atom
metta.run("""
  (primitive WWWD
    (type decision-gate)
    (description "What Would Will Do — autonomous decision emulation")
    (links AUTOPILOT ATOMIC-REFLECTION-GATE))
""")

# Query: find all decision-gate primitives
results = metta.run("!(match &self (primitive $name (type decision-gate) $rest) $name)")

# Add session state
metta.run("!(add-atom &self (active-context COMM-PRIMITIVES 0.8))")

# Pattern-triggered rule: if active context is COMM and output is partner-facing,
# then apply EM-DASH gate
metta.run("""
  (rule em-dash-gate
    (if (and (active-context COMM $conf) (output-type partner-facing)))
    (then (apply-gate EM-DASH-FILTER)))
""")
```

**Gap to fill:** Hyperon Python bindings (`pip install hyperon`) are pre-alpha. The API is functional for small-scale use but undocumented edge cases are common. Adoption requires accepting some instability or building a thin abstraction layer over the Hyperon Python API.

**Effort:** The MeTTa code sketched above will run in a day. The real cost is API churn: Hyperon v0.2.2 is pre-alpha and the Python bindings have changed across every minor release. Expect 1–3 days of API archaeology per Hyperon release during development. Realistic estimate: 2–4 weeks to a working prototype that mirrors SESSION_STATE.md into AtomSpace and answers pattern queries. 2–3 months to production-stable, assuming you absorb at least one breaking Hyperon update. Do not retire WAL.md until the AtomSpace integration has survived one release cycle.

**Limitation:** Hyperon is pre-alpha — the bindings change across releases (v0.2.2 is latest as of Jan 2025). This is not production infrastructure yet. Use as experimental substrate, not as the single source of truth for session state without redundancy.

---

### Integration 3: PLN-Lite for Primitive Applicability Scoring

**What it is:** A simplified version of PLN's uncertain inference, implemented in Python without the full Hyperon stack. Each JARVIS primitive carries a probability distribution over "situations where this primitive fires." When the WWWD gate runs, instead of (or in addition to) an LLM call, it performs a quick weighted query over primitives ranked by their PLN-style applicability score.

**Why it matters:** Currently, the WWWD gate is a pure LLM call. PLN-lite would give JARVIS a deterministic fast path for routine decisions, with LLM escalation only for genuinely novel situations. This is the "move reasoning from LLM weights into explicit structure" goal made concrete.

**Concrete sketch:**

```python
from dataclasses import dataclass

@dataclass
class TruthValue:
    """PLN-style second-order truth value."""
    strength: float  # P(primitive applies) in [0,1]
    confidence: float  # evidence count-based confidence in [0,1]

    def merge(self, other: "TruthValue") -> "TruthValue":
        """Revision formula: weighted merge of two TVs."""
        k = 1  # evidence sensitivity constant
        w_self = self.confidence * k
        w_other = other.confidence * k
        new_strength = (w_self * self.strength + w_other * other.strength) / (w_self + w_other + 1e-9)
        new_confidence = (w_self + w_other) / (w_self + w_other + k)
        return TruthValue(new_strength, new_confidence)

# Each primitive gets a TV based on observed firing history
primitive_tvs = {
    "WWWD": TruthValue(0.9, 0.8),
    "PONYTAIL": TruthValue(0.7, 0.6),
    "EM-DASH-GATE": TruthValue(0.85, 0.9),
    # ...
}

def score_primitives(situation_features: dict) -> list[tuple[str, float]]:
    """
    Score all primitives for applicability given current situation features.
    Returns (primitive_name, score) sorted descending.
    """
    scores = []
    for name, tv in primitive_tvs.items():
        feature_match = compute_feature_match(situation_features, name)
        combined_strength = tv.strength * feature_match
        scores.append((name, combined_strength * tv.confidence))
    return sorted(scores, key=lambda x: x[1], reverse=True)

def update_tv(primitive: str, fired: bool):
    """Update truth value from observed outcome."""
    observation = TruthValue(1.0 if fired else 0.0, confidence=0.1)
    primitive_tvs[primitive] = primitive_tvs[primitive].merge(observation)
```

**Gap to fill:** `compute_feature_match()` — mapping situation features to primitive relevance. This can start as a keyword/tag match (deterministic) and be upgraded to a VSA similarity query (Integration 1) or a full PLN inference chain.

**Effort:** A few days for a working prototype. The TruthValue math is simple; the hard part is instrumenting which primitives actually fired in each session (data collection) and defining "situation features" formally enough to match against.

**Limitation:** PLN-lite is not PLN. It lacks abduction, induction, temporal reasoning, and the full chain inference capability. It is a first step toward explicit uncertain reasoning, not a replacement for the full system.

---

## Sources Cited

- Kanerva, P. (2009). Hyperdimensional Computing: An Introduction. *Cognitive Computation*, 1(2). https://link.springer.com/article/10.1007/s12559-009-9009-8
- Plate, T.A. (1995). Holographic Reduced Representations. *IEEE Trans. Neural Networks*, 6(3).
- Schlegel et al. (2022). A Comparison of VSAs. ACM Computing Surveys.
- Kleyko et al. (2022). ACM Survey on HDC/VSA Parts I & II. https://dl.acm.org/doi/10.1145/3538531
- Torchhd library (JMLR 2023). https://www.jmlr.org/papers/v24/23-0300.html | https://github.com/hyperdimensional-computing/torchhd
- Poursiami et al. (2025). VS-Graph: Scalable and Efficient Graph Classification Using HDC. arXiv:2512.03394. https://arxiv.org/abs/2512.03394
- "Attention as Binding: A Vector-Symbolic Perspective on Transformer Reasoning." arXiv:2512.14709 (Dec 2025). https://arxiv.org/pdf/2512.14709
- "Hyperdimensional Probe: Decoding LLM Representations via VSA." arXiv:2509.25045. https://arxiv.org/pdf/2509.25045
- Goertzel et al. (2023). OpenCog Hyperon: A Framework for AGI at the Human Level and Beyond. arXiv:2310.18318. https://arxiv.org/pdf/2310.18318
- OpenCog Hyperon official site. https://hyperon.opencog.org/
- Hyperon experimental GitHub (trueagi-io). https://github.com/trueagi-io/hyperon-experimental
- hyperon PyPI (v0.2.2). https://pypi.org/project/hyperon/
- OpenCog ECAN wiki. https://wiki.opencog.org/w/OpenCogPrime:EconomicAttentionAllocation
- metta-attention (iCog-Labs-Dev). https://github.com/iCog-Labs-Dev/metta-attention
- PLN OpenCog wiki. https://wiki.opencog.org/w/Probabilistic_logic_networks
- SingularityNET Hyperon page. https://singularitynet.io/research/opencog-hyperon/
- IBM NeuroVSA project. https://research.ibm.com/projects/neuro-vector-symbolic-architecture
- NeuSymMS (arXiv:2605.17596). https://arxiv.org/html/2605.17596
- MeTTa language specification. https://trueagi-io.github.io/hyperon-experimental/metta/
- SingularityNET Annual Report 2024. https://singularitynet.io/singularitynet-annual-report-2024-advancing-beneficial-agi-and-decentralized-ai/
- SingularityNET Deep Funding ECAN framework RFP. https://deepfunding.ai/rfp/framework-for-evaluating-approaches-to-attention-allocation/ — Note: deepfunding.ai is SingularityNET's community grant platform; distinct from Ethereum Foundation's "Deep Funding" program (EF's project per Will's memory). Same domain name, different organizations.
- MeTTa in a Nutshell. https://singularitynet.io/metta-in-a-nutshell-exploring-the-language-of-agi/
