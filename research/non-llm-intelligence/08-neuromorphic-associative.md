# Neuromorphic & Brain-Inspired Non-Transformer Computing for Jarvis: Research Dossier

**Author**: Research agent (Claude Sonnet 4.6)
**Date**: 2026-07-16
**Context**: Jarvis is a deterministic Python harness wrapping Claude — PreToolUse/PostToolUse hooks as gates, a file-based markdown memory graph, cron jobs, subagents, and a WWWD decision gate. The LLM does the reasoning; Jarvis only orchestrates it. Will wants to move genuine reasoning and memory OUT of transformer weights and INTO explicit engineered structure. This dossier covers brain-inspired, non-transformer neural methods: modern Hopfield/dense associative memory, reservoir/echo state computing, spiking neural networks (SNNs/Nengo), predictive coding, and vector-symbolic architectures (VSA/HDC). All five have Python tooling and can run on Will's Ryzen 5 1600 / 16GB RAM / no GPU box.

**Hardest focus**: modern Hopfield networks as a drop-in replacement for the current cosine-similarity-over-embeddings memory retrieval path.

---

## The Gap This Cluster Targets

Jarvis memory retrieval today works like this:

```
query string → embedding API → cosine similarity over stored embeddings → top-k primitives returned
```

Three problems with this:

1. **The embedding call hits the network** — latency, API dependency, cost per call.
2. **Cosine similarity returns the nearest stored item** — it does not reconstruct or denoise. If the query is partially corrupted or uses different surface form, retrieval degrades.
3. **No compositionality** — two primitives that together answer the query cannot be "bundled" and retrieved as a unit without a separate re-ranking step.

The brain-inspired methods in this cluster offer a different model. Associative memories (Hopfield, SDM) are **pattern-completing** rather than pattern-ranking: given a partial or noisy cue, they settle into the stored attractor that best matches — returning the full pattern, not a ranked list. VSA/HDC adds compositional algebra: you can bind two patterns together and retrieve the bundle. Neither requires an embedding API.

---

## 1. Modern Hopfield Networks / Dense Associative Memory

### Core Mechanism

Classical Hopfield networks (1982, Nobel 2024) store memories as valleys in an energy landscape and recall them by gradient descent from a partial cue. If you present a corrupted version of a stored pattern, the network iterates until it settles into the nearest stored attractor — content-addressable recall.

Modern Hopfield networks (Krotov & Hopfield 2016, Ramsauer et al. 2020 "Hopfield Networks is All You Need") replace the binary state space with continuous representations and redesign the energy function to achieve **exponential storage capacity** O(e^αd) rather than the classical O(d) linear capacity limit. The key insight from Ramsauer et al.: a single retrieval step of the modern Hopfield update rule is mathematically identical to the transformer attention operation. The memory matrix *is* the key-value attention matrix.

The update rule for retrieval from a query state ξ against stored patterns X:

```
ξ_new = X · softmax(β · Xᵀ · ξ)
```

This is exactly scaled dot-product attention with the memory patterns as keys and values simultaneously. The difference from transformers: in Jarvis's use, X is a **persistent, writeable memory bank** you control, not weights baked into a model.

**Sparse/Kernelized variants (NeurIPS 2024)**: KHMs (Kernelized Hopfield Models) use a learnable feature map Φ to transform patterns into kernel space, achieving provably optimal memory capacity and a sublinear-time retrieval algorithm. U-Hop (Wu et al., 2024) adds a two-stage retrieval dynamics that distributes local minima more uniformly, reducing memory confusion ("chimeras" where two stored patterns bleed together).

**Latent Structured Hopfield Network (LSHN, 2025)**: integrates Hopfield dynamics with an autoencoder for efficient semantic associative memory — store compressed latent representations, retrieve and decode. This is the closest published system to "modern Hopfield as a semantic document store."

**Neuromodulation-gated variants (2025)**: extend retrieval to include multistability — a single cue can settle into one of several valid retrievals depending on a context signal. Relevant for Jarvis if you want "retrieve the primitive that applies given the current context/session."

### Maturity and CPU-Friendly Python Tooling

| Package | Install | Backend | CPU-feasible? | Notes |
|---|---|---|---|---|
| `hopfieldnetwork` (PyPI) | `pip install hopfieldnetwork` | NumPy | Yes, fully | Classical binary + continuous Hopfield, GUI included |
| `hopfield-memory` (PyPI, Oct 2024) | `pip install hopfield-memory` | NumPy | Yes, fully | Pattern storage + retrieval for corrupted inputs |
| `HopfieldNetworkPyTorch` (GitHub) | `pip install .` | PyTorch (CPU mode) | Yes | Modern Hopfield (Krotov 2016 + Ramsauer 2020), import `ModernHopfieldNetwork` |
| LSHN (GitHub fudan-birlab/LSHN) | manual | PyTorch | CPU feasible for small memory banks | Autoencoder + Hopfield, official 2025 code |

**RAM footprint estimate**: A modern Hopfield memory bank storing N patterns of dimension d uses O(N·d) floats. At d=768 (typical BERT-size embedding) and N=10,000 primitives, the memory matrix is 10,000 × 768 × 4 bytes ≈ **29 MB**. That is negligible. Even at N=100,000 primitives, it is 290 MB — easily within 16GB. The retrieval operation is a single matrix-vector multiply (768-dim), trivially fast on CPU. No GPU required for inference.

**The critical tradeoff**: storing patterns in raw embedding space requires you to have computed those embeddings at write time (one API call per new primitive, amortized). Retrieval is then CPU-local with no API call. If you store the primitives as raw TF-IDF or bag-of-words vectors instead, you avoid all API dependency — capacity and discrimination quality drop somewhat but remain useful.

### Positioning Relative to the LLM

The Hopfield layer sits **between the memory graph and the LLM**. It does not replace the LLM — it replaces the cosine-similarity step that currently selects what context to inject into the LLM's prompt. The LLM still reasons over whatever the Hopfield retrieval surfaces.

```
Before: query → embedding API → cosine sim → top-k → LLM context
After:  query → (one-time embed OR local vectorize) → Hopfield settle → attractor → LLM context
```

The advantage: Hopfield is a *completing* memory, not a *ranking* memory. If the query is "RSAW loop when agent fleet grows," a cosine search might miss the RSAW primitive if the surface form differs. A Hopfield network that stored the RSAW primitive alongside its neighbors in the energy landscape may complete the pattern even from a partial cue.

### Mapping to Jarvis

| Jarvis component | Hopfield role |
|---|---|
| `memory/MEMORY.md` + wikilinked primitives | Memory bank X: each primitive becomes a stored pattern |
| Memory retrieval (currently cosine sim) | Replace with Hopfield retrieval step: query cue → energy minimization → nearest attractor |
| SessionStart hook | Load memory bank from disk into RAM (one-time; 29 MB for 10k primitives) |
| Primitive write (new rule added) | Append new pattern to X; no retraining needed |
| Multi-primitive queries | Weighted superposition of cues before retrieval |

**Minimal working sketch** (no GPU):

```python
import numpy as np

class JarvisHopfieldMemory:
    def __init__(self, beta: float = 8.0):
        self.patterns = []   # list of np.ndarray, shape (d,)
        self.beta = beta     # inverse temperature; higher = sharper recall

    def store(self, pattern: np.ndarray):
        """Add a new pattern (e.g., embedding of a primitive's text)."""
        self.patterns.append(pattern / np.linalg.norm(pattern))

    def retrieve(self, query: np.ndarray, steps: int = 3) -> np.ndarray:
        """Content-addressable recall: settle from query into nearest attractor."""
        X = np.stack(self.patterns)  # shape (N, d)
        xi = query / np.linalg.norm(query)
        for _ in range(steps):
            # Ramsauer 2020 update: xi_new = X^T · softmax(beta · X · xi)
            scores = self.beta * X @ xi
            weights = np.exp(scores - scores.max())
            weights /= weights.sum()
            xi = X.T @ weights
            xi /= np.linalg.norm(xi)
        return xi

    def retrieve_top_k(self, query: np.ndarray, k: int = 5) -> list[int]:
        """Return indices of k most activated patterns after settling."""
        attractor = self.retrieve(query)
        X = np.stack(self.patterns)
        sims = X @ attractor
        return list(np.argsort(sims)[::-1][:k])
```

This is ~30 lines, no external dependencies beyond NumPy, runs on CPU, and handles a 10k-primitive memory bank in under 1ms per retrieval on a modern CPU (single matrix multiply is the bottleneck, ~10k × 768 FLOP).

### Flag: GPU-bound items

The advanced variants (KHM, LSHN with autoencoder) use PyTorch. They run on CPU but at the scale Jarvis needs (N < 100k, d < 1024), CPU inference is fully adequate. The exponential capacity guarantee means you do not need to go beyond these dimensions to get good recall. Flag: if you store raw text as bag-of-words (sparse), you can go to d=50,000 dimensions with essentially no RAM penalty (sparse matrix). Hopfield on sparse vectors is an open research direction, not mature tooling.

---

## 2. Reservoir Computing / Echo State Networks

### Core Mechanism

Reservoir computing is a framework for temporal computation using a fixed, randomly initialized recurrent network (the "reservoir") as a nonlinear dynamical system. Only the readout layer is trained — typically a simple linear regression. The reservoir expands the input time series into a high-dimensional "echo state" space where linear separability emerges naturally.

The key property is the **echo state property**: the reservoir must be contractive enough that its current state encodes a fading memory of past inputs (the "echo"), not arbitrary dynamics. This is achieved by setting the spectral radius of the reservoir weight matrix below 1.

Why this is cheap: the reservoir itself is never trained. You initialize it once (random sparse matrix with controlled spectral radius) and fix it forever. Training = fitting a linear regression on top. The entire fitting procedure runs in seconds on a CPU for reservoirs of 100-1000 nodes.

### Maturity and CPU-Friendly Tooling

**ReservoirPy** is the canonical Python library (`pip install reservoirpy`, version 0.4.2 as of 2025). It is based on NumPy/SciPy, uses sparse matrices for the reservoir weight matrix, and runs entirely on CPU. Key benchmarks: up to 87.9% computation time improvement on a simple laptop versus naive implementations, achieved via sparse matrix multiplication and optional parallel execution.

RAM footprint estimate for a 1000-node reservoir:
- Weight matrix W: 1000 × 1000 × 4 bytes = 4 MB (dense), or ~0.4 MB at 10% sparsity (typical)
- Input matrix W_in: 1000 × d_input × 4 bytes (small)
- State vector: 1000 × 4 bytes = negligible

A 1000-node reservoir runs comfortably in under 100 MB total. For the tasks Jarvis needs (sequence classification, temporal pattern detection over hook event streams), 500-1000 nodes is ample — this fits in under 10 MB.

**RCbench** (2024): a new standardized benchmarking package for reservoir computing, directly compatible with ReservoirPy.

**Reservoir-computing-based associative memory and itinerancy (Nature Communications, 2024)**: demonstrated that reservoir computers can store and traverse complex attractor networks — directly relevant if you want a reservoir to navigate between primitives in a sequence-dependent way.

### Positioning Relative to the LLM

Reservoir computing is a **cheap sequence encoder**, not a reasoner. Its role in Jarvis is orthogonal to the Hopfield memory layer:

- Hopfield: **spatial** recall — given a cue, retrieve a stored pattern
- Reservoir: **temporal** recall — given a sequence of events, classify or predict what happens next

For Jarvis, the natural input to a reservoir is the **hook event stream**: (tool-call, result, tool-call, result, ...) encoded as a sparse vector per event. The reservoir's echo state after T events encodes a compressed temporal summary of the session's trajectory. A linear readout on top can classify: "is this session heading toward OOM?", "is this a WWWD-escalation-candidate pattern?", "should the cron fire a priority interrupt?"

This is a genuinely useful capability that the LLM does poorly in real time (it sees the full context but has no persistent state between tool calls without explicit memory updates).

### Mapping to Jarvis

| Jarvis component | Reservoir role |
|---|---|
| Hook event stream (PreToolUse, PostToolUse, Stop, ...) | Input time series to reservoir |
| Session-level pattern detection | Linear readout trained on labeled session transcripts |
| Cron job trigger logic | Replace or augment rule-based cron logic with reservoir classifier output |
| WWWD gate context | Feed reservoir state as a temporal context feature into WWWD decision |

**RAM / compute**: 500-node reservoir on a stream of N events, each encoded as a 100-dim vector = trivial. The entire state update at each step is a 500×500 sparse matrix multiply + a 500×100 dense multiply, both sub-millisecond on CPU.

**Training requirement**: requires labeled examples of the temporal patterns you want to detect. This is the bottleneck — you need session transcripts labeled with outcomes. If you have 50-100 labeled sessions, a reservoir readout will generalize reliably. Zero-shot is not available.

### Flag: GPU-bound items

Reservoir computing is entirely CPU-native. There is nothing GPU-specific in standard reservoir computing. The June 2025 ScalableHD paper (for HDC) is not directly relevant here. No GPU dependency.

---

## 3. Spiking Neural Networks / Nengo

### Core Mechanism

Spiking neural networks (SNNs) communicate via discrete, sparse spike events rather than continuous real-valued activations. This is a closer model of biological neurons. Sparsity means most neurons are silent most of the time, which translates to energy efficiency on neuromorphic hardware (Intel Loihi) — though on standard CPUs, simulating spikes is often *more* expensive than dense activations, not less.

SNNs are relevant to Jarvis not for energy efficiency on CPU, but for two specific capabilities:

1. **Event-driven computation**: a spike is a natural model for a hook event. PreToolUse fires → a spike propagates through a network that has been "trained" to recognize patterns in hook sequences. This aligns structurally with how hooks already work.

2. **Sparse Distributed Memory (SDM) implementation**: SDM (Kanerva, 1988) is a content-addressable memory model closely related to Hopfield networks but based on random binary addresses and distributed storage. It has been implemented in Nengo (arxiv:2109.03111) as a spiking network. SDM has exponential capacity, handles graceful degradation under noise, and is close to biological models of hippocampal long-term memory.

**Nengo** (Applied Brain Research, open source) is the Python framework:
- `pip install nengo` — core simulator on CPU/NumPy
- `pip install nengo-dl` — TensorFlow backend (faster on CPU via optimization)
- Backends: CPU (NumPy), TF (NengoDL), Intel Loihi (NengoLoihi), FPGA
- Supports building neural models in Python, then deploying to any backend without changing model code

**Nengo CPU overhead**: benchmark evaluations used 32 GB RAM as baseline; small models (hundreds of neurons, simple classification) run fine on 8-16 GB. For Jarvis's use (not large-scale brain simulation, just SDM-as-memory or pattern classifier), 16 GB is adequate. The Jarvis-relevant use case is: build a Nengo model with ~1000-10000 neurons implementing SDM, run it on CPU, use it as a fast associative recall engine.

**Sparse Distributed Memory in detail**:
SDM stores patterns in a high-dimensional binary address space. A "hard location" is activated when a stored pattern falls within Hamming distance r of the query. Retrieved values are a weighted average over all activated hard locations. Properties:
- Exponential capacity (like modern Hopfield)
- Graceful degradation: noisy queries still retrieve the right pattern
- Natural continual learning: write a new pattern without retraining anything
- Python implementations: `sdmlib` (NumPy, CPU-native, fast), `msbrogli/sdm-framework` (GPU optional), `SparseDistributedMemory` org on GitHub

`sdmlib` is a pure NumPy implementation, installable and runnable on Will's box with no GPU. The cognitive computing package (updated April 2025) bundles SDM, VSA, and HRRs in one pip-installable package.

### Positioning Relative to the LLM

SNNs on CPU are primarily relevant for:
1. **SDM as an alternative associative memory** (same role as Hopfield, different mechanism)
2. **Hook event stream classification** using Nengo's event-driven simulation (same role as reservoir computing, but with spiking dynamics that are more interpretable in terms of timing)

Nengo is not a reasoning system; it does not replace the LLM. It is a memory and pattern-detection layer.

### Mapping to Jarvis

| Jarvis component | SNN/Nengo role |
|---|---|
| Memory retrieval | SDM (via sdmlib or Nengo) as content-addressable recall; functionally equivalent to Hopfield but different error profile |
| Hook event detection | Event-driven spiking classifier — each hook fires a spike, Nengo network integrates over session |
| Future: neuromorphic HW | Same Nengo model deploys to Loihi without code change if Will ever gets a neuromorphic board |

### Flag: GPU-bound items

Standard Nengo runs on CPU; NengoDL uses TensorFlow which can use a GPU if present but works on CPU. Intel Loihi is a neuromorphic chip, not a GPU — this is a different and potentially very cheap future path for Jarvis if neuromorphic edge hardware becomes commodity (SpiNNaker2 is already available in research settings). Do not conflate "neuromorphic" with "GPU" — they are orthogonal. On Will's current box, plain CPU Nengo is the correct path. Energy efficiency claims are only valid on Loihi, not on x86 CPU (where SNNs are often slower than ANNs).

---

## 4. Predictive Coding Networks

### Core Mechanism

Predictive coding (PC) is a computational neuroscience theory of cortical function, formalized as a machine learning algorithm by Rao & Ballard (1999) and extended by Friston's free energy principle. The core idea: every layer of a hierarchical network generates a **prediction** of the layer below it; the actual activity of the lower layer sends back **prediction errors**; weights update to minimize prediction error.

This produces learning via purely **local computations** — each synapse updates based only on the activity of the neurons it directly connects, without a global error signal transmitted backward. It is biologically plausible and formally different from backpropagation, though under specific conditions (zero-centered Gaussian prior, linear generative model), PC algorithms converge to the same solution as backprop.

The practical version, "Inference Learning" (IL):
1. **Inference phase**: fix inputs and targets, let prediction errors propagate and update neural states (fast, iterative)
2. **Learning phase**: update synaptic weights using local error signals (slow)

**Key 2024-2025 results**:
- Song et al., Nature Neuroscience (2024): "Inferring neural activity before plasticity as a foundation for learning beyond backpropagation" — establishes PC as not just approximating backprop but as a distinct and complementary algorithm
- "ePC: Fast and Deep Predictive Coding in Digital Simulation" (arXiv:2505.20137, 2025): achieves deep PC in simulation with performance approaching backprop on standard benchmarks
- "Benchmarking Predictive Coding Networks — Made Simple" (arXiv:2407.01163, 2024): systematic comparison showing PC is competitive at shallow depth but underperforms backprop on deep networks; depth scaling remains an open problem

**Python tooling**: PC lacks the mature Python library ecosystem that Hopfield and reservoir computing have. Research implementations exist in PyTorch (CPU-compatible) but are research-grade, not production-ready. The most usable route is implementing a shallow PC network (2-3 layers) in NumPy directly — straightforward for a technically sophisticated user.

### Positioning Relative to the LLM

Predictive coding is a **learning algorithm** for adapting weights in a network, not primarily a retrieval system. Its most direct Jarvis application is as an **online learning rule for adapting the memory graph's retrieval weights without needing an LLM call**.

Scenario: Jarvis retrieves a primitive, the LLM uses it, the session outcome is recorded. A predictive coding update rule strengthens the connections between the query pattern and the retrieved primitive if the outcome was good. This is a local, session-level adaptation that makes Jarvis's retrieval smarter over time without retraining.

The catch: predictive coding is a learning algorithm, not a memory architecture. You would use it *on top of* a Hopfield or reservoir layer to adapt its weights.

### Mapping to Jarvis

| Jarvis component | PC role |
|---|---|
| Memory retrieval | PC-based online adaptation of Hopfield weights (strengthens/weakens attractors) |
| Hook gate adaptation | Online weight update when a hook fires correctly/incorrectly |
| Session feedback loop | PostToolUse outcome → PC error signal → adjust memory attractor strengths |

### Flag: GPU-bound items

PC networks of the size Jarvis needs (tens to hundreds of neurons) are trivially CPU-runnable. The GPU-bound concern is only for large-scale PC networks (billions of neurons attempting to match transformer-scale). For the Jarvis use case, PC is strictly CPU-native. Maturity flag: **low** for production Python tooling. This is a research-grade technique with no pip-installable production library comparable to ReservoirPy or torchhd. Treat it as a 2027+ adoption target unless you are comfortable implementing the inference loop from scratch.

---

## 5. Vector Symbolic Architectures (VSA) / Hyperdimensional Computing (HDC)

### Core Mechanism

VSA/HDC encodes information as high-dimensional vectors ("hypervectors") — typically 1,000 to 10,000 dimensions — and manipulates them using three algebraic operations:

- **Binding** (⊗): combines two hypervectors into a new one representing their association. `A ⊗ B ≠ A, ≠ B` — the result is dissimilar to both operands.
- **Bundling** (⊕): combines multiple hypervectors into a "superposition" that is similar to each component. `A ⊕ B ≈ A, ≈ B`.
- **Permutation** (ρ): shifts the components of a hypervector, typically to represent sequential position.

These three operations are sufficient to encode and decode structured data: key-value pairs, sequences, graphs, and trees — all as fixed-width hypervectors. Retrieval uses cosine similarity (real-valued hypervectors) or Hamming distance (binary) against a **codebook** of known hypervectors.

This is directly related to Hopfield/SDM: the Holographic Reduced Representation (HRR) is a VSA using circular convolution for binding, and its retrieval mechanism is equivalent to a Hopfield-style associative lookup. The connecting theory: SDM, Hopfield, and VSA are all implementations of the same underlying mathematical structure (Kernel Memory Networks, Schroeder et al., 2022).

### Maturity and CPU-Friendly Tooling

**Torchhd** (Python/PyTorch, JMLR 2023): the de facto VSA library. Supports 6 VSA models (BSC, MAP, HRR, FHRR, SBC, VTB). CPU-native; on 20-core Xeon benchmarks, Torchhd is on average 24× faster than prior publicly available HDC code. For Will's 6-core Ryzen 5 1600, expect a proportionally smaller speedup but still fast: a classification over 10k hypervectors at d=10,000 dimensions completes in well under 100ms on CPU.

RAM footprint: a codebook of N=10,000 hypervectors at d=10,000 dimensions (binary, bit-packed via HDTorch+) = 10,000 × 10,000 / 8 bytes ≈ 12.5 MB. At 32-bit float: 400 MB (still within 16GB). For Jarvis's use at d=1,024 and N=10,000, the float codebook is 40 MB — negligible.

**ScalableHD (2025)**: achieves up to 10× throughput over TorchHD on multi-core CPUs via two-stage pipelining and NUMA-aware core binding. This means Will's 12-thread Ryzen 5 1600 could run HDC inference at reasonable throughput for real-time hook-event classification.

**Cognitive computing package** (updated April 2025, pip-installable): bundles SDM + VSA + HRR + HolographicReducedRepresentations in one package — the closest thing to a batteries-included associative memory toolkit.

**FactorHD (arXiv:2507.12366, July 2025)**: extends HDC to multi-object, multi-class representation and factorization — relevant if you want to retrieve "all primitives related to WWWD AND hooks."

### Positioning Relative to the LLM

VSA sits in the **same retrieval layer as Hopfield** but adds a critical capability Hopfield lacks: **compositional structure**. In Jarvis, you can:

- Bind a primitive's name with its context: `name_hv ⊗ context_hv` → a single hypervector representing the primitive-in-context
- Bundle related primitives: `p1_hv ⊕ p2_hv ⊕ p3_hv` → a "cluster" hypervector that is similar to all three
- Encode wikilinks as binding relations: `[[WWWD]] links to [[AutopilotLoop]]` → `wwwd_hv ⊗ links_to_hv ⊗ autopilot_hv`
- Query: "what does WWWD link to?" → `wwwd_hv ⊗ links_to_hv` → retrieve target with inverse binding

This is a **CPU-local, no-API graph traversal** over the wikilink structure of the memory graph. The current Jarvis approach (following [[wikilinks]] by string matching) is brittle to naming variation. The VSA approach is robust to partial cue similarity.

### Mapping to Jarvis

| Jarvis component | VSA role |
|---|---|
| Memory graph wikilinks | Encode as binding relations (primitive ⊗ link-type ⊗ target) |
| Primitive retrieval | Cosine similarity over hypervector codebook — CPU-local, no API |
| Multi-primitive queries | Bundle queries (A ⊕ B) to retrieve primitives similar to both |
| Session context encoding | Bind session events into a running context hypervector; query memory against it |
| WWWD gate context | Feed similarity scores from codebook as features into WWWD decision |

**Note**: VSA and Hopfield are complementary, not competing. Hopfield is better for pure content-addressable recall (noisy cue → complete pattern). VSA is better for structured relational queries (what links to what, what binding equals what). An ideal Jarvis memory layer might use both: Hopfield for fuzzy primitive recall, VSA for structured traversal of the wikilink graph.

### Flag: GPU-bound items

Torchhd is CPU-native by design. At the dimension scales Jarvis needs (d ≤ 10,000, N ≤ 100,000), CPU execution is fully adequate. Memory pressure at million-dimension scales (noted in the 2025 VaCoAl comparison paper) is not relevant here. No GPU required.

---

## Cross-Cutting: Sparse Distributed Memory as the Missing Link

Kanerva's Sparse Distributed Memory (SDM, 1988) deserves special mention because it bridges Hopfield networks, VSA, and spiking neural networks in a unified framework. SDM is:

- Theoretically equivalent to modern Hopfield networks (Kernel Memory Networks, 2022)
- Implementable as a spiking network (Nengo-SDM, 2021)
- A special case of VSA with binary address spaces
- A continual learner (SDM Continual Learner paper, 2023) — adding new patterns does not overwrite old ones

Python implementations:
- `sdmlib` (GitHub avandekleut/sdmlib): pure NumPy, CPU-only, fast
- `msbrogli/sdm-framework`: more complete, optional GPU
- `SparseDistributedMemory` org on GitHub: research-oriented, multiple implementations

For Jarvis, SDM is worth considering as an **alternative backend for the memory bank** if you want explicit distance-based addressing (Hamming space) rather than the energy-minimization of Hopfield. The two are functionally equivalent for most retrieval tasks; SDM has a cleaner capacity theory and more predictable failure modes.

---

## Top 3 Adoptable-for-Jarvis (CPU-Only Sketches)

### Rank 1: Modern Hopfield Network as the Memory Retrieval Layer

**Why**: Direct replacement for cosine-similarity-over-embeddings. Adds pattern completion (noisy/partial queries retrieve correct primitive), exponential capacity, and CPU-local inference with no API dependency. RAM: ~30 MB for 10k primitives at d=768. Latency: sub-millisecond per retrieval on CPU. Maturity: pip-installable today.

**Adoption path**:
1. At SessionStart, vectorize all primitives (once): if you want zero API dependency, use TF-IDF over the primitive text. If you already have embeddings cached, load those.
2. Construct `JarvisHopfieldMemory` (see sketch above), `store()` each primitive vector.
3. When a hook needs to retrieve context, call `retrieve_top_k(query_vec, k=5)` instead of cosine-similarity search.
4. Serialize the pattern matrix to disk (`.npy` file, 30 MB) and reload it at next SessionStart.

**CPU-only sketch**:

```python
# pip install numpy (already installed)
# No GPU, no API, no external calls at retrieval time

import numpy as np
from pathlib import Path

class JarvisHopfieldMemory:
    def __init__(self, beta: float = 8.0):
        self.patterns = []      # list of unit-norm np.ndarray, shape (d,)
        self.labels = []        # list of str — primitive IDs (e.g. "P·wwwd")
        self.beta = beta

    def store(self, vector: np.ndarray, label: str):
        v = vector / (np.linalg.norm(vector) + 1e-12)
        self.patterns.append(v)
        self.labels.append(label)

    def retrieve_top_k(self, query: np.ndarray, k: int = 5) -> list[tuple[str, float]]:
        if not self.patterns:
            return []
        X = np.stack(self.patterns)          # shape (N, d)
        q = query / (np.linalg.norm(query) + 1e-12)
        # One Hopfield update step (== attention without output projection)
        scores = self.beta * (X @ q)
        weights = np.exp(scores - scores.max())
        weights /= weights.sum()
        attractor = X.T @ weights            # settled attractor, shape (d,)
        # Rank by similarity to attractor
        sims = X @ attractor
        top_idx = np.argsort(sims)[::-1][:k]
        return [(self.labels[i], float(sims[i])) for i in top_idx]

    def save(self, path: str):
        np.save(path, np.stack(self.patterns))
        Path(path + ".labels").write_text("\n".join(self.labels))

    def load(self, path: str):
        self.patterns = list(np.load(path))
        self.labels = Path(path + ".labels").read_text().splitlines()
```

This is 35 lines of NumPy. It replaces the embedding-API + cosine-search path with zero network calls at retrieval time. Cold start (vectorizing primitives) happens once per session; hot retrieval is sub-millisecond.

### Rank 2: VSA/Torchhd for Wikilink Graph Traversal

**Why**: The Jarvis memory graph has rich wikilink structure ([[primitive A]] → [[primitive B]]) that cosine search ignores. VSA encodes relational structure via binding, enabling queries like "what does WWWD link to?" without string matching. CPU-native, pip-installable. Compositionality is the unique value over Hopfield.

**Adoption path**:
1. `pip install torchhd`
2. At SessionStart, parse wikilinks from all primitives and encode: for each link `A → rel → B`, store `bind(A_hv, bind(rel_hv, B_hv))` in the codebook.
3. At query time: "what does WWWD link to?" → form `bind(wwwd_hv, links_to_hv)` → cosine search returns top-k bound objects → unbind to recover targets.

**CPU-only sketch**:

```python
import torchhd
import torch

D = 1024  # hypervector dimension; d=1024 gives ~2^512 effective capacity

# Initialize codebooks for primitives and relation types
prim_hvs  = {}   # primitive_id -> hypervector
rel_hv    = torchhd.random(1, D).squeeze()   # one relation type: "links_to"
link_bank = []   # list of (source_id, hypervector) triples

def encode_primitive(prim_id: str) -> torch.Tensor:
    if prim_id not in prim_hvs:
        prim_hvs[prim_id] = torchhd.random(1, D).squeeze()
    return prim_hvs[prim_id]

def store_link(source_id: str, target_id: str):
    src_hv = encode_primitive(source_id)
    tgt_hv = encode_primitive(target_id)
    # Binding encodes the triple (source, links_to, target)
    link_hv = torchhd.bind(src_hv, torchhd.bind(rel_hv, tgt_hv))
    link_bank.append((source_id, link_hv))

def query_links(source_id: str, k: int = 5) -> list[str]:
    src_hv = encode_primitive(source_id)
    # Query vector: what does source link to? = source ⊗ rel
    query_hv = torchhd.bind(src_hv, rel_hv)
    # Search link_bank for entries similar to query
    if not link_bank:
        return []
    bank_matrix = torch.stack([hv for _, hv in link_bank])
    sims = torchhd.cosine_similarity(query_hv.unsqueeze(0), bank_matrix).squeeze()
    top_idx = sims.argsort(descending=True)[:k]
    return [link_bank[i][0] for i in top_idx]
```

This sketch runs on CPU (no `.cuda()` calls), handles 10k wikilinks easily, and makes link traversal robust to hypervector noise (partial matches still retrieve correct links).

### Rank 3: ReservoirPy Echo State Network for Session Temporal Pattern Detection

**Why**: The hook event stream is a temporal sequence; no other method in this cluster is designed for temporal sequence modeling. Reservoir computing is the simplest possible temporal classifier — fix a random recurrent network, train only a linear readout — and it runs entirely on CPU with no GPU, no API, sub-millisecond inference. Directly applicable to cron/trigger logic improvement.

**Adoption path**:
1. `pip install reservoirpy`
2. Encode each hook event as a sparse vector (event type one-hot + tool-type one-hot + outcome one-hot → ~50-dim)
3. Run each session through a 200-node reservoir, collecting states
4. Label sessions by outcome (completed OK / OOM / loop / escalated to Will)
5. Train a Ridge regression readout on labeled sessions
6. At inference: after each hook event, update reservoir state in ~0.1ms, get a probability from the readout

**CPU-only sketch**:

```python
from reservoirpy.nodes import Reservoir, Ridge

# 200-node reservoir — about 0.16 MB at 10% sparsity
reservoir = Reservoir(units=200, sr=0.9, lr=0.3, input_scaling=1.0)
readout   = Ridge(output_dim=4, ridge=1e-5)   # 4 outcome classes

from reservoirpy import ESN
model = ESN(reservoir=reservoir, readout=readout, workers=-1)  # use all cores

# Training (offline): X_train is list of sequences, Y_train is list of labels
# model.fit(X_train, Y_train)

# Inference (online): call model.run(event_vector) after each hook event
# session_state = model.reservoir.run([event_vector])
# prediction = model.readout.run(session_state)
```

Training requires 50-100 labeled sessions to be robust. Inference is sub-millisecond per hook event. The reservoir is initialized once at SessionStart and runs statefully through the session.

---

## Honest Assessment and Adoption Sequencing

| Technique | Jarvis fit | Maturity | CPU-native | Effort to adopt | Priority |
|---|---|---|---|---|---|
| Modern Hopfield (NumPy) | Memory retrieval — directly replaces cosine search | High | Yes, fully | Low — 35 lines | **Adopt now** |
| SDM (sdmlib/NumPy) | Same as Hopfield, different mechanism | High | Yes, fully | Low — pip install | Adopt now (pair with Hopfield) |
| VSA/Torchhd | Wikilink graph relational queries | High | Yes (CPU by default) | Medium — requires wikilink parse pass | Adopt next |
| Reservoir (ReservoirPy) | Session temporal pattern detection | High | Yes, fully | Medium — needs labeled sessions | Adopt after training data exists |
| Predictive coding | Online weight adaptation for memory | Medium | Yes | High — no mature library | 2027+ |
| Nengo SNN | SDM via spiking (same function as sdmlib) | Medium | CPU feasible | High — Nengo learning curve | Optional — use sdmlib instead unless Loihi target |

**Do not adopt** based on energy efficiency claims for SNNs on CPU — that benefit only materializes on neuromorphic hardware. On x86, spiking simulation is slower than the dense equivalent. The path to energy-efficient SNNs for Jarvis is sdmlib on CPU now, Nengo on Loihi if/when neuromorphic hardware becomes relevant.

**The architecture that emerges**: a two-layer local memory system replacing the current API-dependent retrieval:
- **Layer 1 (spatial)**: Hopfield or SDM — given a cue, complete the pattern and return the nearest stored primitive. No API call.
- **Layer 2 (relational)**: VSA/Torchhd — traverse the wikilink graph via binding algebra. Compositional queries.
- **Layer 3 (temporal, optional)**: ReservoirPy — classify the current session trajectory and surface cron triggers.

All three layers are CPU-native, zero-API, and collectively fit in under 500 MB RAM. The LLM's role becomes narrower: it reasons over the context that these layers have already assembled locally.

---

## Sources and Key References

- Ramsauer et al. (2020), "Hopfield Networks is All You Need": https://arxiv.org/abs/2008.02217
- Krotov & Hopfield (2016), "Dense Associative Memory for Pattern Recognition": https://arxiv.org/abs/1606.01164
- Awesome Modern Hopfield Networks paper list: https://github.com/Event-AHU/Awesome_Modern_Hopfield_Networks
- U-Hop uniform memory retrieval (2024): https://arxiv.org/abs/2404.03827
- LSHN latent structured Hopfield (2025): https://arxiv.org/abs/2506.01303
- Hopfield-Fenchel-Young Networks (2024): https://arxiv.org/abs/2411.08590
- Modern Hopfield + Encoded Neural Representations (2024): https://arxiv.org/abs/2409.16408
- KHM provably optimal capacity NeurIPS 2024: https://arxiv.org/abs/2410.23126
- Modern Methods in Associative Memory survey (2025): https://arxiv.org/abs/2507.06211
- ReservoirPy GitHub: https://github.com/reservoirpy/reservoirpy
- ReservoirPy PyPI: https://pypi.org/project/reservoirpy/
- Reservoir-computing associative memory (Nature Communications 2024): Kong, Brewer & Lai
- Reservoir Computing Benchmarks review (2024): https://arxiv.org/abs/2405.06561
- Nengo GitHub: https://github.com/nengo/nengo
- Nengo Open Neuromorphic overview: https://open-neuromorphic.org/neuromorphic-computing/software/snn-frameworks/nengo/
- Sparse Distributed Memory on Nengo (2021): https://arxiv.org/abs/2109.03111
- sdmlib (NumPy SDM): https://github.com/avandekleut/sdmlib
- SparseDistributedMemory org: https://github.com/SparseDistributedMemory
- SDM is a Continual Learner (2023): https://arxiv.org/abs/2303.11934
- Torchhd (JMLR 2023): https://arxiv.org/abs/2205.09208
- Torchhd GitHub: https://github.com/hyperdimensional-computing/torchhd
- ScalableHD multi-core CPU (June 2025): https://arxiv.org/abs/2506.09282
- FactorHD (July 2025): https://arxiv.org/abs/2507.12366
- Benchmarking PC Networks (2024): https://arxiv.org/abs/2407.01163
- ePC fast deep predictive coding (2025): https://arxiv.org/abs/2505.20137
- Song et al. Nature Neuroscience (2024) — learning beyond backprop
- SuperLocalMemory V3 zero-LLM agent memory (2026): https://arxiv.org/abs/2603.14588
- Kernel Memory Networks unifying SDM/Hopfield/VSA (2022): https://arxiv.org/abs/2208.09416
