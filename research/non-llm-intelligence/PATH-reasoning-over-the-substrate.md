# PATH — Reasoning OVER the LLM Substrate

**Written:** 2026-07-26 · **Author:** JARVIS (opus-4-8), commissioned by Will Glynn
**Status of every claim below carries a maturity label:** `[BUILDABLE-NOW]` (mature, CPU-native, pip-installable, AND verified-present on this box or laptop-tested by the source dossier) · `[PLAUSIBLE-UNTESTED]` (components are real and downloadable and the math says it fits, but it has **never been run or memory-measured on this box** — treat as a hypothesis about feasibility, not a fact) · `[RESEARCH-GRADE]` (published, reproducible, but wiring is bespoke and unbuilt) · `[FRONTIER]` (concept or single-paper, unproven at Jarvis scale) · `[OUT]` (needs a GPU or hardware Will does not have). Nothing is rounded up. "Resembles" is never written as "is." A `[unverified-2026-preprint]` tag marks any citation dated 2026 that could not be independently checked at write time.

**Verified-on-this-box audit (run 2026-07-26, do not launder):** installed and importable — `z3` v4.16.0, `clingo` v5.8.0, `networkx` v3.6.1, `ortools` (CP-SAT). **NOT installed** — `torch`, `transformers`, `sae_lens`, `nnsight`, `torchhd`. Therefore **no bf16 forward pass, no SAE decode, and no VSA/hyperdimensional engine has ever been run on this hardware.** Total RAM 17.1GB; **available RAM at audit time was 6.7GB** (OS + Python + a running Claude Code harness already consume the rest). Every white-box-substrate feasibility claim below is `[PLAUSIBLE-UNTESTED]` until a real load is measured. Only the pure-symbolic engines are `[BUILDABLE-NOW]`.

This document is a course correction. The prior research folder (`ARCHITECTURE-SKELETON.md`, `SYNTHESIS.md`, dossiers 01–09) is excellent engineering pointed at a **different goal than the one Will stated**. This document names the divergence precisely, then lays a buildable path back to the stated goal without discarding the good work.

---

## 1. THE GOAL — restated precisely, and how the folder drifted from it

### 1.1 The goal, verbatim and unpacked

> *"a path to a real intelligent reasoning model that uses the LLM as the FORMLESS BASE OF TRAINED DATA to act upon WITH engineered reasoning."*

Unpacked with the load-bearing words kept load-bearing:

- The LLM's **latent trained knowledge IS the substrate** — the marble.
- An **engineered reasoning process** (explicit, inspectable, deterministic where possible) **imposes FORM** on that formless knowledge — the sculptor.
- The knowledge is the thing being **reasoned OVER**, not something to **route around and minimize**.
- The composed system must reason **BETTER / more reliably** than the raw LLM alone.

The single discriminating axis (named in the hardware-fork dossier and adopted here): reasoning **OVER** the formless data versus reasoning **AROUND** it.

- **AROUND** = prompt-in, tokens-out, then post-process the text. The LLM's internal knowledge is a black box you sample from and filter. You never touch the marble; you photograph it.
- **OVER** = the engineered process acts on the substrate's own state — its activations, its features, its internal disagreement, its knowledge-as-evidence — and produces reasoning the single greedy decode cannot.

The goal demands OVER. Most of the folder built AROUND, and called it done.

### 1.2 The drift, quoted from the folder's own words

The folder's thesis, verbatim (`ARCHITECTURE-SKELETON.md` §0, lines 18–20):

> *"The transformer is a rented, fallible **System-1 peripheral**: called sparingly for what cannot yet be structured ... never trusted as the reasoner."*

And its single most important metric (`ARCHITECTURE-SKELETON.md` §2, lines 110–111):

> *"The LLM-call count per cycle trends toward zero as L7 compiles structure. That trend line is the single most important metric of the whole architecture."*

And the L6 spec (lines 90–94): the LLM is a *"SIDE PERIPHERAL, called by L4/L5 only when structure runs out."* And `SYNTHESIS.md` §5 (lines 102–103): *"keep the LLM as a **shrinking** System-1."*

**This is the inverse of Will's goal.** Will's telos: the LLM's knowledge is the substrate you reason **over**, so the LLM stays maximally **in** the loop as the material being sculpted. The folder's telos: the LLM is a cost to be **driven toward zero**. Same tools (solvers, truth-values, memory graphs), opposite purpose.

The drift is not a mistake in the folder's own frame — shrinking an expensive rented dependency is a legitimate engineering goal. It is simply **the safe adjacent question**, not this one. The anti-drift constraint in the commission names exactly this: *do NOT retreat to "build a separate symbolic knowledge base and shrink the LLM's duty cycle toward zero."*

### 1.3 The specific place the good work points the wrong way

Concretely, from the folder's own audit (`SYNTHESIS.md` §2, `LOOP-STATUS.md`): every built module reasons over the **hand-authored markdown memory graph** or over **gate telemetry**. `_asp_extract` compiles the markdown graph into ASP facts with *zero LLM calls*. `_kr_check` runs SPARQL over an RDF schema. None of them treats the **LLM's own latent knowledge** as the substrate being reasoned over. That is the drift made concrete: a separate symbolic KB, reasoned over, LLM minimized. Good code, adjacent goal.

**The correction, stated once:** keep every engine the folder found. Re-point the whole apparatus so its input is the LLM's own knowledge-state, and its success metric is *reasoning quality*, not *LLM-call count*.

---

## 2. The core architecture that ACTUALLY reasons over the substrate

There is no single mechanism. There is a **fork**, forced by physics, into two real families — and both genuinely satisfy the goal, at different depths. The honest architecture uses both.

### 2.1 The physics that forces the fork

Mechanisms that act on the *formless data directly* — activations, hidden states, logits, SAE features — require **white-box / open weights**. Claude (and Fable) is a **hard black box**: the Anthropic API exposes no logprobs, no top-token probabilities, no hidden states, no logit_bias to the client (verified: Anthropic is the strictest black box among major vendors, no logprobs as of Feb 2026; the one server-side exception is schema-compiled Structured Outputs, which give you grammar-conformance without logit *access*).

Therefore:

> **You cannot reason OVER Claude's formless data. It is structurally impossible.** To reason over the substrate in the literal sense, the substrate must be a model you can open — a **local open-weights model**. Claude can only be reasoned *around* (prompt/tokens), or used as a heavy black-box oracle *beside* the openable substrate.

This is the strategic fork the prior folder never confronted. It assumed Claude stays the reasoner. The goal forbids that assumption for the deepest form of the goal.

### 2.2 The two families that satisfy the goal — and their depth

**FAMILY A — WHITE-BOX LATENT (the literal marble/sculptor).** Run a small open-weights model locally, hook its residual stream, decode its activations into interpretable **SAE features** (a pre-trained sparse autoencoder), reason with deterministic/symbolic logic **over those feature-facts**, and optionally **steer** generation by editing the residual stream. This is the *only* family where "engineered reasoning acts upon the formless trained data" is literally true rather than metaphorical. `[RESEARCH-GRADE]` — the components are real and downloadable; the composition (symbolic rules over SAE-feature facts) is unbuilt anywhere in the folder and is the actual frontier.

**FAMILY B — BLACK-BOX ENGINEERED SEARCH (form on knowledge via an external controller).** An explicit, seedable, inspectable search/decision engine (MCTS, do-calculus, expected-free-energy, MDL program-search) treats the LLM as a **queried oracle** — a transition function ("given state s and action a, what is s'?") or a hypothesis generator ("propose a causal DAG") — while the **engine owns the objective, the search, and the decision**. The reasoning trace is an artifact of the *search acting upon the LLM's latent knowledge*, not of a greedy decode. This works black-box, so it works on Claude **today**. `[BUILDABLE-NOW]` for the harness; `[RESEARCH-GRADE]` for the wiring quality. **Read `[BUILDABLE-NOW]` here as "the harness is trivial to write," NOT "broadly applicable" — §7.3 argues the region where a domain supplies BOTH a natural state space AND an engineered scorer may be narrow. Buildable ≠ broadly-useful.**

### 2.3 The knife-edge that separates "reasoning over" from "LLM-with-extra-steps"

Family B collapses back into clever prompting the instant the **LLM also does the scoring**. Canonical WebDreamer (arXiv:2411.06559) uses the LLM as "both world model AND value function" — then the engine is a one-line argmax and the whole thing is Tree-of-Thoughts with a UCB decoration. The same trap is RAP's (arXiv:2305.14992): its reward is *action-likelihood + state-confidence + LLM-self-evaluation* — all three are LLM-internal signals, so the value oracle is the marble grading its own carving. This is the identical self-verification weakness that (correctly, per ICML 2024 Smit et al.) condemns self-consistency and multi-agent debate.

**The discipline that makes Family B real (non-negotiable):**

> The value / scoring / decision must be **engineered** — a deterministic goal-test, a sound external critic (Z3 / PDDL-validator / pytest), an expected-free-energy functional, or do-calculus — **never a second LLM call.** Where you can hold that line, the engine genuinely imposes form the LLM lacks (look-ahead, calibrated exploration, intervention-correctness). Where you cannot, you are back to prompting.

This discipline has a sharp, honest tension: *where you have a clean deterministic scorer, you often did not need the LLM's world-knowledge; where you need the LLM's knowledge, you often lack a clean scorer.* The viable region is real but **narrow and domain-gated**, and must be proven per-domain by a falsifiable exit test (§5), never assumed.

### 2.4 The composed architecture

```
   ┌───────────────────────────────────────────────────────────────────────┐
   │  ENGINEERED REASONING (the sculptor) — deterministic, inspectable       │
   │  ─────────────────────────────────────────────────────────────────────  │
   │  Family A controller:  probe-read → branch → intervene → continue        │
   │  Family B controller:  MCTS / do-calculus / EFE / MDL-search             │
   │  Shared soundness rail: NARS (f,c) belief revision · sound critics ·      │
   │                         conformal abstention (the honesty line)          │
   └───────▲──────────────────────────────────────────────▲──────────────────┘
           │ reads feature-facts / activations             │ queries as oracle
           │ (WHITE-BOX, local open-weights only)          │ (BLACK-BOX, any LLM)
   ┌───────┴───────────────────────────┐        ┌──────────┴───────────────────┐
   │  LOCAL OPEN-WEIGHTS SUBSTRATE      │        │  CLAUDE — heavy black-box     │
   │  gemma-2-2b + Gemma Scope SAEs     │        │  oracle for knowledge the     │
   │  = the marble you can OPEN         │        │  2B model lacks (untrusted    │
   │                                    │        │  candidate, cross-checked)    │
   └────────────────────────────────────┘        └───────────────────────────────┘
```

The **single most goal-realizing loop** (Family A, the literal reading of Will's phrase):

1. Run a forward pass of the local model on a claim/task.
2. A pre-trained SAE decodes the residual stream into active **feature-facts** (the model's own latent concepts, made inspectable). Note: Gemma Scope publishes SAEs, not a curated catalogue of "hallucination features"; features that *downstream work claims* correspond to uncertainty/confabulation are found by separate analysis (the HalluSAE-class papers, themselves `[unverified-2026-preprint]`) and each such label inherits GOFAI Rule 2 (verify-before-trust).
3. Feed those **feature-facts** (not parsed text) into a clingo/Z3 rule base — deterministic, auditable symbolic reasoning **over the model's internal state**.
4. Branch on the result: accept, verify, abstain, or **steer** via `z' = z + α·d_k` (add a scaled SAE decoder vector to the residual stream) and re-decode.
5. Claude enters only when the local model's features show it is out of depth; its answer is an untrusted candidate, cross-checked against the local model's activated concepts before it is trusted.

Here the engineered structure acts UPON the formless data (activations), imposes form (symbolic rules over features), and yields reasoning the raw model does not do alone. That is give-form-to-the-formless, made literal, on this box.

---

## 3. RESOLVING the white-box/black-box + hardware fork — the concrete buildable stack

Hard constraint: Ryzen 5 1600 (6c/12t), **17.1GB RAM total but only ~6.7GB free under normal load (OS + Python + Claude Code harness)**, **no GPU**. Brutally honest, per-tier. The free-RAM number, not the nameplate 16–17GB, is what a bf16 model must fit inside.

### 3.1 The hidden fork the prior laptop-test missed

White-box feature work needs the model in **PyTorch bf16/fp32** so you can hook activations and run the SAE — **NOT** a quantized GGUF. Two traps (documented upstream, but note `torch`/`transformers` are **not installed on this box**, so neither trap has been hit here yet — these are library facts, not on-box measurements):
- `fp16 on CPU crashes` (`addmm_impl_cpu_ not implemented for Half`, HF transformers issue #27769). Use **bf16 or fp32**, not fp16, not GGUF.
- Activation hooks require **eager mode**; `torch.compile` bypasses them.

So the plausible substrate is a ~2B model in bf16 eager mode. That is the ceiling for feature work on 16GB/no-GPU — **if it fits at all** (see the honest RAM verdict in §3.2, which is `[PLAUSIBLE-UNTESTED]`, possibly false).

### 3.2 The named stack

**WHITE-BOX SUBSTRATE (Family A) — `[PLAUSIBLE-UNTESTED]` at the 2B tier (nothing here is installed; nothing here has been run on this box):**
- **Model:** `google/gemma-2-2b` in **bf16** (~4.7GB weights). Alternative: Qwen3-1.7B. For fast iteration: GPT-2-small / Pythia-70M (trivial RAM — these small ones probably genuinely fit, but that is still untested here).
- **SAE suite:** **Gemma Scope** (arXiv:2408.05147; 400+ pre-trained JumpReLU SAEs on every layer of gemma-2-2b/9b; a 16k-width SAE ~0.3GB). Use pre-trained only — **training your own SAE is `[OUT]`** (GPU-bound).
- **Hooking / decode:** `SAELens` + `nnsight` + `TransformerLens` (all pip, all CPU, framework-agnostic PyTorch) — **none currently installed**; first `pip install` + first forward pass is unrun.
- **Budget — `[PLAUSIBLE-UNTESTED]`, and the margin is worse than the doc originally claimed.** Total RAM on this box is **17.1GB** (not 16). But **available RAM at audit time was only 6.7GB** — the OS, Python, and the Claude Code harness already hold the rest. A commonly cited figure (via `accelerate estimate-memory` / the HF model-memory calculator — cite the tool, not a bare number) puts gemma-2-2b bf16 CPU inference near **~12.7GB system RAM for weights + activations alone**, before SAE + OS + Python working set. **On measured current headroom (6.7GB) this does not fit and will swap;** it might fit only after freeing the box to near-idle, and even then the margin is thin. **Honest possibility to state plainly: Family A local may not fit on this box at all, which would collapse the "literal goal is buildable NOW, on THIS box" thesis to "buildable only on a bigger box."** The one-line fix that resolves this: install `torch`/`transformers`/`sae_lens`, run ONE gemma-2-2b bf16 forward pass + ONE Gemma Scope SAE decode near-idle, measure peak RSS and tok/s, then re-tier this row against the real number. Until then: `[PLAUSIBLE-UNTESTED]`. Speed: expected a few tok/s eager-mode CPU (also unmeasured) — if usable, fine because feature extraction is not interactive chat, but it means k-sampling loops (semantic entropy) are wall-clock-brutal on the local model.

**SYMBOLIC LAYER OVER FEATURES (both families) — `[BUILDABLE-NOW]`, and this tier is genuinely verified on this box:**
- **clingo / ASP** (rules over feature-facts; negation-as-failure) — **verified installed, v5.8.0**. **Z3** (`z3-solver`, ~50MB, ms-solve) — **verified installed, v4.16.0**. **NetworkX** — **verified installed, v3.6.1**. **OR-Tools CP-SAT** — **verified installed**. **ONA** (NARS, lean C binary) for the (f,c) belief layer — separate binary, not audited here. All pip/CPU, sub-second, sub-gigabyte at Jarvis scale. This row — the *engineered sculptor* itself — is the part that is real, present, and cheap today; the untested risk is entirely in the white-box *marble* it would read from.

**BLACK-BOX ENGINE (Family B) — `[BUILDABLE-NOW]`:**
- **Search harness:** pure Python MCTS/ToT/GoT (~200–500 LOC; only dependency is token I/O). **pymdp** (`inferactively-pymdp`, active-inference EFE, <5MB, µs policy inference). **DoWhy/PyWhy** (causal do-calculus over an LLM-proposed DAG; NetworkX + sklearn, negligible RAM). **LILO + Stitch** (MDL program-induction; Stitch runs in seconds on one CPU).
- These are the engines that own the objective. The LLM is the oracle they query.

**LOCAL BLACK-BOX GENERATION (optional second oracle) — `[BUILDABLE-NOW]`:**
- **llama.cpp** with a 7–8B **Q4_K_M GGUF** (~4–5GB, 5–15 tok/s). Gives tokens-out only, no openable internals — a cheap local oracle, not a white-box substrate. Note: `llama.cpp` natively supports **control vectors** (`llama_adapter_cvec`, residual-stream bias-add, zero inference cost) — this is the *one* white-box-flavored edit reachable from GGUF, and it runs on this box today `[BUILDABLE-NOW]`.

**WHERE CLAUDE FITS:**
- **Heavy black-box oracle.** Called when the 2B substrate's features show it is out of depth, or as the Family-B transition/hypothesis oracle. Its output is an **untrusted candidate**, verified by a sound critic and, where possible, cross-checked against the local model's activated concepts before it is trusted. Claude is vastly smarter than any 2B model — so for **hard knowledge**, black-box Claude + search/verify is the realistic near-term path. It is permanently "reasoning around," but it is the pragmatic capability path while Family A is proven on narrow slices.
- **Claude Structured Outputs** (server-side schema→grammar→constrained decoding) `[BUILDABLE-NOW]`: use it to make oracle outputs machine-parseable (successor states, DAGs, candidate rules). This is form on the *channel*, not the *reasoning* — necessary plumbing for both families, not itself reasoning-over.

**`[OUT]` — needs a GPU or 32–64GB RAM (state plainly, do not launder):**
- White-box feature work on **8B+ models** (Llama Scope, Goodfire SAEs on Llama-3.1-8B): ~16–18GB bf16 weights alone before KV cache + a ~3.75GB 131k-wide SAE. Does not fit.
- **Circuit tracing / attribution graphs** (`circuit-tracer`, Anthropic 2025): ~15GB VRAM; CPU-offload exists but is impractically slow on 6c/12t. The richest form of "reason over internals" — genuinely out of reach on this box.
- **Training your own SAE**; **differentiable neurosymbolic training** (LTN/Scallop *training* — you cannot backpropagate through a frozen or rented LLM anyway); any **real-time white-box chat loop**.

### 3.3 The honest verdict on the fork

- The **engineered layer is trivially in budget and verified present** for both families (KBs of RAM, sub-second solvers; z3/clingo/networkx/ortools all confirmed importable on this box).
- **Family A (white-box, the literal goal)** is `[PLAUSIBLE-UNTESTED]` on this box: its stack is **not installed**, no forward pass has ever run, and on measured current headroom (6.7GB available of 17.1GB total) a gemma-2-2b bf16 + SAE load **would swap or not fit**. It *may* fit at the 2B tier near-idle — that is a hypothesis to test with one measured run, not a fact. If it does fit, it is thin-fit, slow-but-usable for non-interactive feature extraction, and the 2B substrate is far dumber than Claude — the standing cost of choosing the openable marble. **If it does not fit, the literal-goal path needs a bigger box, and that must be said, not laundered.**
- **Family B (black-box search)** runs on this box for the engine; the LLM oracle is either a **cloud Claude call** (fast, costs money, black-box) or a **local CPU model** (free, private, but tree-search's call-count makes MCTS minutes-to-hours per plan). **Cost, not RAM, is the real constraint** — engineered search multiplies API calls 10–100× per problem, and the folder's own `[FanOutCostMeasureNotEstimate]` warns this spend is currently invisible/ungoverned. A hard call-budget governor is required or it silently burns money. **DoWhy and program-induction have far lower call counts** (one DAG proposal; a handful of program proposals) and are laptop-comfortable even with a local oracle.

---

## 4. Reachable-now vs research-frontier — honest maturity per mechanism

| Mechanism | Family | White/Black-box | Maturity | Reasons OVER substrate? |
|---|---|---|---|---|
| Control vectors via `llama_adapter_cvec` (add engineered concept-direction to residual stream) | A | white-box (GGUF-reachable) | **`[PLAUSIBLE-UNTESTED]` on this box** — production feature in llama.cpp upstream, but llama.cpp is not built/run here; ICLR 2025 arXiv:2504.19483 shows residual control vectors lift IOI/bAbI/GSM8K on Mistral/Pythia with no retraining (exact point-gain uncited in what could be reached) | **YES** — edits the formless activations; the literal chisel. But the *read/detect* half is solid; the *steer/mitigate* half is **fragile** (see §7). |
| Linear probes over cached activations (detect model's internal state, then branch) | A | white-box | **`[PLAUSIBLE-UNTESTED]` on this box** — the classifier is trivial logistic regression in scikit-learn, but it needs cached activations from a model that is not installed here; SAPLMA/semantic-entropy-probe literature reports strong detection (specific accuracy figures vary by task and are **uncited here** — do not treat "~80%" as a measured number) | **YES** for the read; it forms an engineered doubt-signal from the substrate's own state — detection, note, is **not itself the goal-claim** ("reason over" and "reason better" are proven only by §5.1). |
| SAE feature-facts → clingo/Z3 rule base → gate/steer (the core loop, §2.4) | A | white-box | **`[RESEARCH-GRADE]`** — Gemma Scope real & downloadable; HalluSAE (arXiv:2604.16430 `[unverified-2026-preprint]`) and refusal-audit-via-SAE (arXiv:2605.30162 `[unverified-2026-preprint]`) are published instances of the *shape*; **the symbolic-rules-over-feature-facts composition is UNBUILT anywhere in the folder** | **YES** — this is the strongest literal realization of the goal, *architecturally*; unproven until built and passed through §5.1. |
| Circuit tracing / attribution-graph surgery (localize a fault feature, edit it) | A | white-box | **`[OUT]`** on this box (~15GB VRAM); `[FRONTIER]` in general (interpretation still largely manual) | YES, and the richest — but not on 16GB/no-GPU. |
| MCTS/ToT/GoT over LLM transition-oracle **with engineered scorer** (RAP done right) | B | black-box | **`[BUILDABLE-NOW]`** harness / **`[RESEARCH-GRADE]`** wiring; RAP (arXiv:2305.14992): LLaMA-33B+RAP > GPT-4 CoT by ~33% relative on plan generation (verified) | **YES**, *only* if the value/score is engineered, not a 2nd LLM call. |
| Causal: LLM proposes DAG, **DoWhy/PyWhy runs do-calculus** | B | black-box | **`[BUILDABLE-NOW]`** harness — DoWhy mature, pure-CPU. **Soundness qualifier:** do-calculus is *sound GIVEN a correct DAG* (Pearl); that soundness does **not** transfer to the answer, because the DAG-proposal step is the untrusted LLM link (garbage DAG in → rigorous-nonsense out) and inherits GOFAI Rule 2. The "must live outside the LLM" obstruction (arXiv:2605.27567) is `[CITATION-UNVERIFIED]` (2026 preprint, not read) — do not cite it as a theorem. | **YES** for the *procedure*; the *answer* is only as sound as the LLM-proposed DAG. Least hand-tuned-objective of the black-box cases, but still scaffold-dependent on the variable set. |
| Active inference / EFE over LLM-predicted rollouts (**pymdp**) | B | black-box | **`[RESEARCH-GRADE]`** — pymdp mature & CPU-native; LLM-glue is research-grade; **needs hand-built A/B/C matrices & tiny state space (LLM confabulates calibrated probabilities)** | **YES** for the explore/exploit decision the LLM lacks, within a hand-authored state space. |
| Bayesian program-induction (**LILO + Stitch**), LLM as proposal prior | B | black-box | **`[RESEARCH-GRADE]`** — Stitch is CPU-cheap; output is auditable code under an MDL objective the LLM never sees | **YES** but domain-narrow (task-as-programs), fits the L7 crystallization slot, not a general reasoner. |
| LLM-Modulo: generate → **sound critic** (Z3/PDDL/pytest) → structured feedback → bounded retry | B | black-box | **`[BUILDABLE-NOW]`** pattern (Kambhampati ICML 2024, arXiv:2402.01817: 82% Blocksworld / 15 rounds); critic shape already built (`_critic.py`) | **PARTIAL** — imposes *sound external form*, but the sound answer lives in the critic; the LLM is deliberately kept OUT of the inference path (this is form-on-output, closer to the adjacent question — useful, honestly labeled). |
| NARS **(f,c) belief revision** as a per-claim epistemic wrapper | shared rail | black-box | **`[RESEARCH-GRADE]`** — ONA is a production C binary (v0.9.3); (f,c) merge is ~40 LOC; fills the skeleton's verified-`[OPEN]` L3 slot | **YES** — treats LLM outputs *as evidence*, revises a belief graph across corroboration/contradiction the LLM alone cannot produce. Neither prompting nor a hand-authored KB. |
| Semantic-entropy self-consistency; conformal abstention | shared rail | black-box | **`[BUILDABLE-NOW]`** (Farquhar Nature 2024; Mohri & Hashimoto 2024) | **NO** — a doubt *thermometer* and a *gate*; reads the substrate's variance, does not reason over its knowledge. Valuable (a certificate), honestly not reasoning-over. |
| Self-consistency majority-vote; multi-agent debate | — | black-box | **`[BUILDABLE-NOW]`**, trivial | **NO** — LLM both proposes and judges; ensemble average over its own distribution. Ruled out (ICML 2024: debate ≈ consistency). |

**The two beachheads that are *architecturally positioned* to reason over the substrate — pending the §5.1/§5.2 exit tests (do not read "positioned" as "proven"):**
1. **White-box read + control-vector steer** on gemma-2-2b (`[PLAUSIBLE-UNTESTED]` on this box — stack not installed, fit unmeasured), extended toward **SAE-feature-facts → symbolic rules** (`[RESEARCH-GRADE]`, the frontier worth building).
2. **Black-box engineered search with a sound/engineered scorer**, strongest as **LLM-proposes-DAG → DoWhy do-calculus** (`[BUILDABLE-NOW]` harness; sound *given* a correct DAG, with the DAG-proposal step untrusted — not a theorem that the answer is correct).

---

## 5. Falsifiable exit tests — what proves it reasons BETTER than the LLM alone

No mechanism ships on vibes. Each carries a pre-registered pass bar. GOFAI died partly of unfalsifiable architecture diagrams (`09` retrospective); every claim here is measurable or it is cut.

### 5.1 Family A (white-box) exit test — feature-gating beats black-box-oracle+verify

Build a labeled eval set of N claims/tasks in Jarvis's real domains (memory-primitive consistency, gate-should-fire decisions, tool-plan validity), with ground-truth correct/incorrect. Compare:
- **(A)** raw local model.
- **(B)** local model + SAE-feature-gate + symbolic-rule branch (the §2.4 loop).
- **(C)** black-box Claude + text-verify (the adjacent-question baseline).

**Pass bar (pre-register):** at matched coverage, (B) has strictly lower **selective risk** than (A), measured by **AURC** and **E-AURC** (excess over oracle ranking), AND lower **ECE** and **Brier**. The load-bearing bar: on an **out-of-distribution slice** (paraphrase-stress + harder-than-seen instances), (B)'s calibration gap does **not** collapse the way (A)'s does. Concrete: composed **AURC ≤ 0.7× raw AURC** and composed **ECE ≤ 0.5× raw ECE** on the OOD slice, abstention rate reported. **And the goal-specific bar:** (B) must beat (C) on task-success at fixed cost — otherwise the white-box machinery is ceremony and the honest move is to use Claude black-box.

### 5.2 Family B (black-box search) exit test — engine beats greedy decode, per domain

For each candidate domain, compare **(A)** greedy LLM decode / single CoT vs **(B)** the engine (MCTS-with-engineered-scorer / DoWhy / pymdp) over the same LLM as oracle.

**Pass bar:** (B) strictly beats (A) on task success **on the axis the engine owns** — horizon (bounded-depth planning), uncertainty (calibrated explore/exploit), or causality (L2/L3 interventional/counterfactual queries). Existence proofs the bar is clearable: RAP (LLaMA-33B+RAP > GPT-4 CoT by ~33% relative, plan generation); LLM+external-SAT-solver → ~100% across the 3-SAT hardness range where the LLM alone collapses (arXiv:2408.07215 / 2504.03930); causal do-calculus computes L2/L3 answers the LLM is near-random on (CORR2CAUSE; CausalGraph2LLM NAACL 2025: 60% answer swings under mere graph re-encoding).

**Kill condition (both families):** if the composed system cannot beat raw-LLM-with-verbalized-confidence on these numbers, the structure is ceremony and must be cut. State the abstention rate always — a system that abstains 80% of the time (the ConfLVLM over-abstention limit) "knows when it doesn't know" while reasoning over almost nothing; calibration is *necessary, not sufficient* for "reasons better."

### 5.3 The metric that must NOT be used

**LLM-call-count-per-cycle is retired as a success metric for this goal.** For the white-box path it is *actively backwards* — the whole point is to run the local model constantly and read its guts. The success metric is **reasoning quality at fixed cost** (§5.1/§5.2), full stop.

---

## 6. How this corrects the prior synthesis's drift — explicitly

| Prior folder | This path |
|---|---|
| *"transformer is a rented System-1 peripheral ... called sparingly"* (`SKELETON` §0) | The LLM's knowledge **is the substrate reasoned over**; it stays maximally in the loop as the material being sculpted. |
| *"LLM-call count per cycle trends toward zero ... the single most important metric"* (`SKELETON` L110–111) | **Metric retired.** Success = reasoning quality at fixed cost. For the white-box path the local model would run **constantly** — *if* it fits on this box, which is `[PLAUSIBLE-UNTESTED]` (§3.2). |
| L6 = *"SIDE PERIPHERAL, called only when structure runs out"* | L6 is **promoted from peripheral to substrate** for the local open-weights model. Claude stays a heavy black-box oracle, but is no longer the thing whose duty-cycle is minimized. |
| Every built module reasons over the **hand-authored markdown graph** / gate telemetry (`LOOP-STATUS.md`) | The new input is the **LLM's own knowledge-state** — activations, SAE features, knowledge-as-evidence. The markdown-KB modules are re-scoped as the L1 memory layer, not the reasoning substrate. |
| *"keep the LLM as a shrinking System-1"* (`SYNTHESIS` §5) | The LLM is a **growing, opened System-1** (local) whose internals are the reasoning material, plus a **stable heavy oracle** (Claude). |
| Solvers/truth-values pointed at drafts & gates | **Same engines, re-pointed** at the LLM's knowledge: clingo/Z3 over SAE-feature-facts; NARS (f,c) over LLM-outputs-as-evidence; do-calculus over LLM-proposed DAGs. |

**What is preserved (the good work is not discarded):** the L1 hypergraph memory, the clingo/Z3/CP-SAT/NARS engine roster, the LLM-Modulo critic shape (`_critic.py`), the three GOFAI guardrails, the ETM attention economy, the falsifiable-exit-test discipline. All of it stays. Only the **telos and the input** change: from *route-around-and-minimize a hand-KB* to *impose-form-on-and-reason-over the LLM's own latent knowledge*.

**One honest concession about a partial-drift trap in Family B.** The LLM-Modulo / solver-gate mechanisms (82% Blocksworld; 3-SAT → 100%) are the folder's Tier-1, and they are genuinely useful — but they are the **adjacent question wearing a soundness badge**: the sound answer lives entirely in the external checker, and the LLM's knowledge is deliberately kept *out* of the inference path. They impose *sound external form on one output at a time*; they do not reason *over* the knowledge. Keep them as the **verification rail**, label them honestly, and do not let "3-SAT hits 100%" be cited as evidence for THE GOAL — it is evidence for the adjacent one.

---

## 7. Honest boundaries — what stays genuinely hard, what needs a GPU, what could fail

### 7.1 Genuinely hard / open (no clean answer today)

- **The capability gap is unproven-in-our-favor.** The openable substrate is ~2B, far dumber than Claude. It is **not demonstrated** that feature-level reasoning over a small model beats black-box Claude+solver on real Jarvis tasks. The §5.1 exit test exists precisely because this could fail. A weak marble sculpted better can still lose to a strong marble left alone.
- **Steering is fragile — detection ≠ mitigation.** Probes *detect* internal state well (specific accuracies vary by task; treat any single percentage as illustrative, not measured), but linear **steering to fix** it is *reported to fail* when the model reconstructs the suppressed signal downstream (attractor-dynamics, arXiv:2604.15400 `[unverified-2026-preprint]` — the precise "within 2–3 layers" mechanism is single-preprint and not corroborated here, so do not state it as measured fact), and control vectors are reported to fail when the linear-representation approximation breaks (arXiv:2602.17881 `[unverified-2026-preprint]`). The *direction* of this concession is well-established (RepE/CAA show steering is real but brittle); the specific 2026 mechanisms are not verified here. The *read* half of Family A is solid; the *write* half — the load-bearing "reasons better by editing activations" half — is materially weaker.
- **SAE features are noisy, polysemantic, dataset-dependent.** A "confabulation feature" may not generalize; monosemanticity is imperfect; clamping one feature causes model-dependent collateral damage (arXiv:2606.08365 `[unverified-2026-preprint]`). And GOFAI **Rule 2 binds hard**: "this is the deception feature" is a human/LLM-assigned *interpretation* that can be wrong — an unverified feature-label becomes a silent-error control input exactly like an unverified extracted rule. Verify-before-trust applies to interpretability labels.
- **The Family-B state space is hand-authored — and this is the commissioned drift wearing a Family-B costume, not a footnote.** pymdp needs hand-built A/B/C matrices and a tiny state space; MCTS needs a hand-coded goal-test and action set; DoWhy needs the variable set and refutation battery. That scaffold does real reasoning work. For the majority of Jarvis-relevant tasks there is **no clean state space AND no clean scorer** (§7.3-#2), which means Family B — for most real tasks — degrades to either (a) prompting or (b) the analyst hand-building the very symbolic scaffold the goal said not to retreat into. That is not a "milder cousin" of the build-your-own-KB drift; it is the *same* drift, relocated. Causal do-calculus is the cleanest partial escape (fixed universal procedure over a supplied variable set); MCTS/pymdp are more scaffold-dependent. **Do not let the §2.2/§4 `[BUILDABLE-NOW]` harness-labels read as "broadly applicable" — §7.3 argues the applicable region is narrow.**
- **Family B inherits cluster-09's combinatorial-explosion (Failure Mode 4) UNCHANGED — as a soundness problem, not just a cost problem.** `09` is unequivocal: the exponential wall is *not fixed*; the LLM can help navigate it heuristically only *at the cost of soundness guarantees*. Family B *is* LLM-guided search (MCTS/ToT/GoT). The §2.3 knife-edge disciplines the **scorer** (value must be engineered, never a 2nd LLM call) — but it does **not** discipline the **search-space pruning**. The moment the LLM prunes the tree, soundness is traded for tractability: **a sound scorer on the *accepted* node does not restore soundness over the *rejected* subtree, so Family B can silently prune the correct plan.** This is load-bearing and is *not* solved by the knife-edge; it is a hard limit inherited from GOFAI Mode 4.
- **Grounding a free-text successor state back into an engine-legible state** for the next query is unsolved in general (Text World Models survey, arXiv:2606.09032). Structured decoding helps parseability but needs local open weights.
- **The three GOFAI failures are relocated, not dissolved** (`09`): verification bottleneck (now on feature-interpretation), combinatorial explosion (**untouched** — per `09` the exponential wall is not fixed; LLM-guided pruning navigates it only by *trading away* the soundness that justified reaching for a symbolic engine; solver gates help only where the *check* is cheaper than the *search* and only on the *accepted* branch), symbol grounding (statistically circumvented, non-auditable). This path **embraces** the relocation (verify-every-fact, sound critics, provenance) but does not pretend to dissolve it.
- **Determinism is only partial.** The controller is seedable; the LLM oracle is not (Claude gives no bitwise determinism even at temperature 0). Full-trace reproducibility is not achievable black-box.

### 7.2 Needs a GPU (or 32–64GB RAM) — honest ceiling

- White-box feature work on **8B+ models** (Llama Scope, Goodfire) — the most interesting open SAE suites are out of reach on 16GB.
- **Circuit tracing / attribution graphs** — the richest "reason over internals," ~15GB VRAM.
- **Training SAEs / control vectors from scratch at scale; any real-time white-box chat loop.**

### 7.3 What could fail (the ways this path dies)

1. **§5.1 fails:** 2B-white-box never beats Claude-black-box on real tasks → Family A is a research toy, and the honest architecture is Family B (black-box search) with Claude, accepting "reasoning around" as the ceiling. This is a real possible outcome; state it up front.
2. **The scorer wall:** for most Jarvis-relevant tasks there is no cheap deterministic goal-test (that is *why* you reached for the LLM's knowledge), so Family B's non-negotiable discipline (engineered scorer) has no clean instantiation and it degrades to prompting. The viable region may be too narrow to matter.
3. **Cost governor absent:** black-box search silently burns money (10–100× call multiplier, invisible spend). Without a hard call-budget governor this fails operationally regardless of whether it works technically.
4. **SAE-feature composition never built:** the strongest literal-goal loop (§2.4) is `[RESEARCH-GRADE]` and **unbuilt anywhere**. If execution falls back to clingo-over-text-facts because features are too noisy, it silently becomes the drift again.

### 7.4 The one-line honest summary

**The goal is reachable — but split, and one half is unproven-on-this-box.** The *literal* satisfaction (Family A, reason over activations/features) is `[PLAUSIBLE-UNTESTED]` at a ~2B tier: the stack is **not installed**, the fit is **unmeasured and may not hold on 6.7GB of current headroom**, the substrate is far weaker than Claude, and the steer-half is fragile; its strongest form (SAE-features → symbolic rules) is a real but `[RESEARCH-GRADE]`, unbuilt frontier. **The boldest promise — "the literal goal is buildable NOW on THIS box" — is therefore currently unproven and possibly false; the one measurement that settles it is one gemma-2-2b bf16 forward pass + one SAE decode with peak-RSS reported.** The *pragmatic* satisfaction (Family B, engineered search over Claude-as-oracle with a sound/engineered scorer) is `[BUILDABLE-NOW]` as a harness today, strongest in the causal sub-case (sound *given* a correct DAG, not theorem-backed as to the answer), but is narrow, domain-gated, cost-bound, inherits GOFAI Mode 4 (LLM pruning trades soundness for tractability), and — in its LLM-Modulo variant — shades into the adjacent question. Build both, prove both by the §5 exit tests, and refuse to let either be described as more than it is.

---

## Appendix: primary citations (names, not gestures)

**Verification note:** four load-bearing citations were independently spot-checked at write time and verified accurate with nuances intact — Gemma Scope (2408.05147), RAP (2305.14992), WebDreamer (2411.06559, including its "world model AND value function" dual role), and RepE control-vectors (2504.19483). Those checks earn some trust in the rest. **However, every citation with a 2026 arXiv id (26xx.xxxxx) below could NOT be independently verified at write time and is tagged `[unverified-2026-preprint]`; do not cite any of them as settled fact.**

**White-box latent (Family A):**
- Gemma Scope: Lieberum et al., arXiv:2408.05147 (400+ open JumpReLU SAEs on gemma-2-2b/9b); ai.google.dev/gemma/docs/gemma_scope
- Llama Scope arXiv:2410.20526; Goodfire open SAEs (Llama-3.1-8B/3.3-70B) — both `[OUT]` on this box
- Representation Engineering (RepE), Zou et al. 2023; Contrastive Activation Addition, Rimsky et al. arXiv:2312.06681
- Improving Reasoning via Representation Engineering, ICLR 2025, arXiv:2504.19483 (residual control vectors, no retraining)
- llama.cpp `llama_adapter_cvec` (PR #5970, vgel); vgel/repeng vector generation
- HalluSAE arXiv:2604.16430 `[unverified-2026-preprint]`; refusal-audit-via-SAE arXiv:2605.30162 `[unverified-2026-preprint]` (claimed instances of the feature→logic shape)
- Steering unreliability: arXiv:2602.17881 `[unverified-2026-preprint]`; attractor-dynamics (detection≠mitigation) arXiv:2604.15400 `[unverified-2026-preprint]`; SAE side-effects arXiv:2606.08365 `[unverified-2026-preprint]`
- Tooling: SAELens, nnsight, TransformerLens, Neuronpedia; CPU fp16 crash HF transformers #27769
- Anthropic is a hard black box (no logprobs/logits/hidden states) — verified in hardware-fork dossier

**Black-box engineered search (Family B):**
- RAP: Hao et al., EMNLP 2023, arXiv:2305.14992 (LLaMA-33B+RAP > GPT-4 CoT ~33% rel.)
- ToT arXiv:2305.10601; GoT arXiv:2308.09687; WebDreamer arXiv:2411.06559 (the "LLM as world-model AND value fn" drift to avoid)
- Kambhampati et al. LLM-Modulo, ICML 2024, arXiv:2402.01817 (82%/15-rounds); LINC arXiv:2310.15164; Logic-LM (EMNLP 2023); LLM+P (Liu 2023)
- Causal kernel-obstruction: arXiv:2605.27567 `[CITATION-UNVERIFIED / unverified-2026-preprint]` — a single unread 2026 preprint; **not** to be cited as a theorem. Do-calculus soundness itself is Pearl (established), but sound-procedure ≠ sound-answer once an LLM proposes the DAG. CausalGraph2LLM NAACL 2025 (60% answer-swings under graph re-encoding); DoWhy/PyWhy; pymdp (Heins et al. JOSS 2022, arXiv:2201.03904)
- LILO ICLR 2024 arXiv:2310.19791 + Stitch; DreamCoder PLDI 2021
- 3-SAT existence proof: arXiv:2408.07215, arXiv:2504.03930
- Self-consistency (Wang 2022); multi-agent debate (Du 2023); debate≈consistency (Smit et al. ICML 2024)

**Soundness / calibration rail:**
- NARS/ONA (v0.9.3, Patrick Hammer); NARS-GPT; (f,c) revision (dossier 04 TruthValue.merge)
- Semantic entropy: Farquhar et al. Nature 2024; semantic-entropy probes arXiv:2406.15927 (OATML)
- Conformal factuality: Mohri & Hashimoto 2024; Conformal Linguistic Calibration NeurIPS 2025 arXiv:2502.19110; ConfLVLM over-abstention (Li et al. 2025)
- Metrics: AURC/E-AURC/ECE/Brier; "Entropy Alone is Insufficient" arXiv:2603.21172 `[unverified-2026-preprint]`; "LLM Knowledge is Brittle" arXiv:2510.11905 `[unverified-2026-preprint]`

**Folder drift points (the corrected sources):**
- `ARCHITECTURE-SKELETON.md` §0 lines 18–20 (System-1 peripheral), §2 lines 110–111 (call-count→zero metric), L6 lines 90–94 (side peripheral)
- `SYNTHESIS.md` §5 lines 102–103 (shrinking System-1)
- `09-gofai-failure-retrospective.md` Rules 1–3 (coverage boundaries, verify-before-trust, constrain scope) — bind every mechanism here
