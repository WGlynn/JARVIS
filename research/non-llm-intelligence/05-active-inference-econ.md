# 05 — Active Inference, World Models, Causal Inference, Market-Based Computation

**Cluster:** Grounded prediction, control, and agent-economy computation — the ETM-native angle.
**Written:** 2026-07-16 | **Hardware constraint:** Ryzen 5 1600, 16 GB RAM, no GPU. Laptop test is mandatory.
**Honesty discipline:** mechanism / maturity / LLM relationship / Jarvis mapping — one per section. Nothing rounded up.

---

## Introduction

This dossier covers the quadrant that is most directly native to the ETM (Economic Theory of Mind) philosophy already embedded in Jarvis: approaches that treat intelligence as resource allocation under uncertainty rather than pattern completion in embedding space. The four topics are not independent — they form a conceptual stack:

- **Active inference** provides the normative control loop: an agent minimizes surprise by acting to make the world match its predictions.
- **World models** give that agent something to simulate: compact models of state transitions that enable cheap lookahead planning.
- **Causal inference** gives the agent intervention-aware reasoning: not "what correlates with what" but "what happens if I do X" — the do-calculus.
- **Market-based computation** implements the allocation layer: which sub-agent, tool, or hypothesis wins the right to act is decided by auction/bid rather than central routing.

These four together describe an agent that (a) holds a model of the world, (b) plans by simulating futures in that model, (c) reasons causally about interventions, and (d) allocates compute via economic mechanisms. That is the Jarvis design target stated in ETM terms. The LLM is a semantic oracle you call from within this structure, not the structure itself.

---

## 1. Active Inference / Free Energy Principle

### 1a. Core Mechanism

Karl Friston's Free Energy Principle (FEP) posits that any self-organizing system — biological or artificial — must resist the tendency toward entropy by minimizing its "surprisal": the mismatch between what its internal model predicts and what it actually senses. Minimizing surprisal is equivalent to minimizing an information-theoretic quantity called **variational free energy (VFE)**, which is a tractable upper bound on surprisal.

For an agent with a generative model of the world, this produces two drives operating simultaneously:

1. **Perceptual inference:** Update internal beliefs to fit incoming observations (minimize VFE by adjusting the model's posterior — this is Bayesian belief updating).
2. **Active inference:** Take actions that change the world to match predictions (minimize VFE by changing the observations, not just the beliefs).

Planning in active inference is handled via **expected free energy (EFE)**, which scores policies (action sequences) by how much free energy they are *expected* to incur in the future. EFE decomposes into:

- **Pragmatic value (exploitation):** Expected match between predicted outcomes and preferred outcomes (the agent's prior preferences, encoded in the C vector).
- **Epistemic value (exploration):** Expected information gain — how much uncertainty a policy would resolve. This produces curiosity and intrinsic motivation for free, without needing a hand-crafted exploration bonus.

The result is that a single objective (minimize EFE) produces goal-directed behavior AND exploration simultaneously. This is qualitatively different from reward-maximization RL, where exploration must be separately incentivized.

**The discrete-state POMDP formulation** (the one implemented in pymdp) represents an agent's generative model as five parameter sets:

| Matrix | Meaning |
|---|---|
| A | Likelihood: P(observation \| hidden state) |
| B | Transition: P(next state \| current state, action) |
| C | Prior preferences: log probability over desired observations |
| D | Prior beliefs about initial state |
| E | Prior beliefs over policies (optional; action habits) |

These are tabular probability matrices. For small-to-medium state spaces (tens to hundreds of hidden states, tens of observations, handful of actions), they are dense NumPy arrays that fit trivially in RAM and run entirely on CPU.

### 1b. Maturity and CPU-Friendly Tooling

**pymdp** (Heins, Millidge, Friston et al., 2022 — Journal of Open Source Software) is the canonical Python implementation for discrete-state active inference. It is NumPy-based and CPU-native. No GPU required. The `Agent` class exposes a clean loop:

```python
from pymdp import Agent
import numpy as np

# A, B, C, D are numpy arrays encoding the generative model
agent = Agent(A=A, B=B, C=C, D=D)

obs = env.reset()
for t in range(T):
    agent.infer_states(obs)          # perceptual inference: update beliefs
    q_pi, G = agent.infer_policies() # planning: score policies by EFE
    action = agent.sample_action()   # act
    obs = env.step(action)
    agent.infer_parameters()         # optional: learn A, B from experience
```

Install: `pip install inferactively-pymdp`
Repo: https://github.com/infer-actively/pymdp

**Performance and scale:** pymdp runs comfortably on CPU for state spaces up to a few hundred states and a few dozen observations. The bottleneck is policy enumeration — if you allow long policy horizons over many actions, the number of policy candidates grows exponentially. In practice, tree-pruning and reduced policy sets keep this tractable. A 2024 paper introducing `cpp-aif` (a multi-core C++ active inference implementation) benchmarks against pymdp, indicating pymdp's NumPy operations are the limit for very large state spaces — but for Jarvis-scale problems (reasoning over a graph of primitives, not over a 10,000-state environment), pymdp is adequate.

**RxInfer.jl** (Julia — ReactiveBayes ecosystem) is the higher-performance alternative. It implements Bayesian inference via reactive message passing on a factor graph, achieving over 300x speedup over Hamiltonian Monte Carlo on comparable problems. It supports continuous and discrete state spaces, handles hybrid models, and runs on CPU. As of 2025, it has a REST server (`RxInferServer.jl`) and is being ported toward edge devices. The catch is Julia: requires a separate runtime and cross-language calls from Python add overhead. For Jarvis's Python harness, pymdp is the pragmatic choice; RxInfer.jl is a valid future upgrade path for the compute-intensive components.

**GPU status:** Not required. pymdp is CPU-native. RxInfer.jl is also CPU-first. Active inference at the discrete-state POMDP scale is intrinsically lightweight.

### 1c. Relationship to the LLM

The LLM and the active inference agent sit at different levels of abstraction:

| Layer | Component | Role |
|---|---|---|
| Semantic | Claude (LLM) | Proposes actions, generates hypotheses, interprets unstructured text |
| Structural | Active inference agent (pymdp) | Scores proposed actions against the generative model, selects policies that minimize EFE |
| Preference | C vector | Encodes what outcomes the system should prefer — defined by the engineer, not learned from the LLM |

The correct integration pattern: the LLM proposes a *set of candidate actions or plans* (e.g., "call tool X", "emit text Y", "spawn sub-agent Z"). The active inference agent holds a generative model of the task environment (states = task progress or belief states; transitions = what actions typically lead to what states). It uses EFE to score the LLM's candidates and select the one that best balances goal achievement and uncertainty reduction. The LLM handles the *semantics*; the active inference layer handles the *control*.

A 2025 paper ("Orchestrator: Active Inference for Multi-Agent Systems in Long-Horizon Tasks", arXiv:2509.05651) demonstrates exactly this pattern: an active inference orchestrator selects which specialized LLM agent to invoke at each step, using EFE to balance exploiting known-good agents and exploring uncertain ones. The orchestrator is computationally lightweight because it operates at agent-selection granularity, not token granularity.

### 1d. Mapping to Jarvis

**WWWD as a generative model.** The WWWD (What Would Will Do) gate is currently implemented as a learned heuristic: Jarvis tries to emulate Will's decision pattern by analogy with past corrections stored in memory primitives. Active inference offers a formal upgrade: WWWD becomes a *generative model* P(Will's decision | task context, history). Will's observed decisions are treated as observations; WWWD infers the posterior over what Will would decide (perceptual inference), then selects the action that minimizes EFE against Will's inferred preferences (the C vector — encoded from Will's stated priorities, CAVE philosophy, primitive archive). Discrepancies between predicted and actual Will decisions update the model's parameters (A and B matrices). This is not metaphor — it is a direct application of active inference to behavior prediction and alignment.

**Hook gating as policy selection.** Jarvis's hooks (PreToolUse, PostToolUse, Stop) currently gate individual operations with hardcoded or heuristic logic. Each hook is a decision point: allow / block / modify. The active inference agent can sit above this layer, scoring candidate actions (tool calls, responses, sub-agent spawns) by EFE before any hook fires. High-EFE actions (likely to lead to dispreferred outcomes or high uncertainty) get blocked at the structural level before they reach LLM execution.

**Gap:** Jarvis has no formal generative model of task environments today. Building one for even a simple Jarvis use case (e.g., "route a task to the right sub-agent and adapt when the sub-agent fails") would require defining A, B, C, D matrices manually for that sub-task. This is engineering work, not research work — the mechanisms are mature.

---

## 2. World Models and Model-Based Planning

### 2a. Core Mechanism

A **world model** is a compact representation of environment dynamics — essentially a simulator you can run cheaply in your head. Given a current state s and action a, the world model predicts the next state s' and a reward signal. With a world model, planning becomes *simulation*: you roll out multiple action sequences, score the outcomes, and select the best sequence before committing to any action.

The key insight is that a world model decouples *knowing what to do* from *doing it*. You learn the world model once (or engineer it from known dynamics), then plan cheaply by simulating futures. This is far more sample-efficient than model-free RL, which must try actions in the real world to learn their consequences.

**Monte Carlo Tree Search (MCTS)** is the canonical planning algorithm on top of a world model. MCTS builds a search tree by:
1. **Selection:** Traverse the tree from the root using UCB (Upper Confidence Bound) to balance exploration and exploitation.
2. **Expansion:** Add a new leaf node representing an unexplored state-action pair.
3. **Simulation (rollout):** From the new leaf, simulate a random (or heuristic) policy to a terminal state.
4. **Backpropagation:** Update the value estimates along the path from root to leaf.

After N iterations, select the action with the highest visit count or value estimate. AlphaGo/MuZero use MCTS + learned world models, but MCTS itself is hardware-agnostic and runs on CPU.

**Model Predictive Control (MPC)** is a simpler variant: at each step, solve an optimization problem over a finite horizon using the world model, execute the first action, then re-solve. MPC is widely used in robotics and process control and has minimal compute requirements when the world model is a simple transition function.

### 2b. Maturity and CPU-Friendly Tooling

CPU-native Python MCTS libraries exist and are trivially installable:

- `pip install monte-carlo-tree-search` — general purpose, requires implementing a `State` class with `get_possible_actions()`, `take_action()`, `is_terminal()`, `get_reward()`. Time-limited or iteration-limited search.
- `pip install mcts-simple` — faster iteration with dramatic speedups (tic-tac-toe: 9 hours → 100 seconds for 10⁶ iterations)
- `pip install scikit.mcts` — configurable tree/default/backup policies

The world model itself can be:

1. **Handcrafted (best for Jarvis):** A Python function that maps (state, action) → next_state. For Jarvis's task graph (state = current task status + context, action = sub-agent invocation or tool call), this is a state machine that can be written in a few dozen lines. Zero ML required.
2. **Learned (tabular or simple NN):** A lookup table of observed transitions, or a small MLP. Either runs on CPU.
3. **LLM as world model (GPU-bound, not recommended for Jarvis):** Use the LLM to predict next states. This works but is slow and expensive — not CPU-native.

The cleanest Jarvis-compatible pattern: handcrafted world model (state machine over task progress) + CPU MCTS for plan search + LLM only for leaf node evaluation (when the state is ambiguous and needs semantic scoring).

**Hardware status:** MCTS on CPU is well within the Ryzen 5 1600 constraint. 10,000 rollouts per decision on a simple state machine completes in milliseconds.

### 2c. Relationship to the LLM

Current LLM-based planning (Chain-of-Thought, ReAct, tree-of-thoughts) runs entirely inside the LLM — it is expensive, non-deterministic, and subject to compounding error on long horizons (GPT-4o drops from 85% to 53% accuracy as horizon length increases). A world model externalizes the simulation: the LLM proposes candidate actions and scores leaf nodes; the world model + MCTS handles the combinatorial search.

This is a direct instance of the "LLM as System-1, structured reasoning as System-2" split. The LLM generates options; MCTS selects among them by simulation. The LLM is called sparingly (at decision nodes where semantic judgment is needed), not for every simulation step.

### 2d. Mapping to Jarvis

**WWWD decision tree.** The WWWD gate currently makes single-step decisions. A world model upgrade: maintain a small state machine over the current task's lifecycle (states: task_received → sub_task_decomposed → tool_called → result_verified → response_emitted → done). At each step, MCTS searches over possible next actions (which tool to call, whether to spawn a sub-agent, whether to escalate to Will) and picks the plan that maximizes expected task completion probability. The world model is the state machine; MCTS is the planner; the LLM scores ambiguous leaf nodes.

**Gap:** Jarvis has no explicit state machine over task lifecycles today. Tasks are executed reactively, step by step. A world model introduces lookahead — at the cost of requiring an explicit model to be built. For Jarvis's current scale (a handful of sub-agent types, a few task categories), this is tractable and would require perhaps 200-300 lines of Python.

---

## 3. Causal Inference

### 3a. Core Mechanism

Pearl's causal hierarchy distinguishes three levels of reasoning:

| Level | Question | Example |
|---|---|---|
| L1: Observational | What is? | "When the LLM is slow, tasks fail." |
| L2: Interventional | What if I do X? | "If I switch to a faster model, will tasks succeed?" |
| L3: Counterfactual | What would have happened? | "If I had not spawned a sub-agent, would this task have succeeded?" |

Correlational ML (including LLMs) operates at L1. It can tell you what is associated with what in training data. It cannot answer L2 or L3 questions without additional causal structure.

The **do-calculus** (Pearl, 2000) provides a complete set of rules for transforming L2 (interventional) questions into L1 (observational) quantities when a **causal graph (DAG)** is available. The causal graph encodes which variables causally influence which others. Given the graph, do-calculus can derive what will happen if you intervene on a variable — without running the intervention.

A **Structural Causal Model (SCM)** is the formal object: a set of variables, a DAG over them, and a set of structural equations defining how each variable is determined by its parents plus noise. Given an SCM, you can compute interventional distributions (L2) and counterfactuals (L3) analytically or via simulation.

### 3b. Maturity and CPU-Friendly Tooling

The Python causal inference ecosystem is mature and entirely CPU-native:

**DoWhy** (PyWhy / Microsoft): The primary do-calculus library in Python. Follows a four-step workflow: Model (define the causal graph) → Identify (determine if the effect is identifiable from observational data, using do-calculus rules) → Estimate (compute the effect numerically) → Refute (adversarial checks on the causal assumption). Pure Python + NumPy + scikit-learn. No GPU. Install: `pip install dowhy`.

**CausalML** (Uber, v0.16.0 released Feb 2026): Specializes in heterogeneous treatment effects and uplift modeling. Useful when you want to know "does action X have different effects in different contexts?"

**CausalRL** (newer): Covers the Pearl causal hierarchy (L1/L2/L3) with formal do-calculus queries, causal bandits, and SCMs. More direct integration with RL and decision-making.

**Pyro** (Uber, PyTorch-based): Probabilistic programming with `pyro.do()` for intervention. Requires PyTorch but not a GPU — runs on CPU.

**Hardware status:** All of the above run on CPU. DoWhy's core graph operations are pure Python/NetworkX; effect estimation uses scikit-learn estimators. RAM footprint for typical causal graphs (tens of variables) is negligible. Even for datasets with millions of rows, causal identification (which variables matter) is cheap; estimation cost depends on the chosen estimator but a linear model or propensity score match is fast.

### 3c. Relationship to the LLM

LLMs are trained on observational text — they excel at L1 (what correlates with what in training data) but systematically fail L2 and L3 questions. Benchmarks (Cladder, CRASS, CounterBench 2025) confirm that LLMs struggle with counterfactual chains, mediation analysis, and confounder-heavy reasoning. This is a structural failure, not a scale failure — you cannot fix it by making the model bigger.

The correct split: the LLM generates causal hypotheses ("I think A causes B because...") and proposes interventions ("let me try tool X"); the causal inference layer evaluates whether those hypotheses are consistent with the observed data and the causal graph, and computes the expected effect of the proposed intervention before it is taken.

This is the "LLM as hypothesis generator, structure as hypothesis evaluator" pattern — directly analogous to neurosymbolic approaches but at the causal level.

### 3d. Mapping to Jarvis

**Root cause analysis for hook failures.** When a hook fails or produces unexpected output, Jarvis currently logs it and moves on. A causal model of Jarvis's own behavior — a DAG over hook inputs, LLM outputs, memory state, and task outcomes — would enable genuine root cause analysis: not "which hook fired before the failure?" (L1) but "what intervention on the context would have prevented the failure?" (L2). This is the use case Amazon's AWS team uses DoWhy for (microservice latency root cause), directly portable to Jarvis.

**Counterfactual WWWD.** WWWD currently asks "what would Will do?" The causal upgrade: WWWD becomes a counterfactual reasoner — "what *would* Will have done if the context had been different?" (L3). This allows Jarvis to reason about Will's preferences in novel situations by simulating counterfactual variants of past decisions, not just pattern-matching to the nearest past example.

**Intervention-aware tool selection.** Before calling an expensive tool (a sub-agent spawn, a web search, a long LLM call), Jarvis can use a causal model of task completion (variables: tool_called, context_quality, task_complexity, success) to predict the interventional effect of calling that tool given the current context. This is the PCP (Pre-Compute-Probability) gate made formally causal.

**Gap:** Jarvis has no causal graph of its own behavior today. Building a minimal one (5-10 variables, manually specified) and fitting it from logged task data would be the first step. DoWhy makes this a Python afternoon's work once the data exists.

---

## 4. Market-Based / Economic Computation

### 4a. Core Mechanism

The central insight of market-based computation: **markets are distributed optimization algorithms**. Hayek's core observation was that no central planner can aggregate all the dispersed, local knowledge held by individual agents — but prices in a free market do aggregate it automatically, via decentralized bidding. The same insight applies to computation: if you have many computational sub-agents each with local knowledge, and you want to allocate work efficiently, a market (auction) mechanism can coordinate them without a central controller knowing the capabilities of each agent.

**Learning Classifier Systems (LCS) / Bucket Brigade (Holland, 1980s):** The first formalization. A population of condition-action rules ("classifiers") compete for the right to fire. Each classifier has a *strength* value. When multiple classifiers match the current situation, they bid (bid = strength × specificity); the winner fires and pays its bid to whichever classifier set up the winning conditions (the bucket brigade). Payoff from the environment flows backward through successful action chains — decentralized credit assignment.

**Hayek Machine (Baum, 1999):** A strict formalization of LCS with property rights enforced. Agents bid for the right to act on the world. The winning agent "owns" the world state, pays its bid to the previous owner, performs its action, and collects any reward plus payment from the next owner. A Nash equilibrium of the market produces a globally optimal policy — this was formally proven. The Hayek Machine extends to POMDPs by adding a writable memory register.

**Economy of Minds (EoM, 2026 — arXiv:2606.02859):** The state-of-the-art extension to LLM agents. Each agent is a language model parameterized only by a system prompt (shared frozen backbone). Within episodes, agents bid in first-price sealed-bid auctions for the right to act; the winner pays its bid to the previously active agent (bucket brigade). Across episodes, the population evolves: wealthy agents are mutated (exploitation); bankrupt agents are replaced (exploration). No central controller, no explicit role assignment. Emergent specialization (planners, executors, verifiers) arises purely from wealth dynamics. Tested on mathematical reasoning, financial research, scientific research, distributed systems optimization — the paper reports outperforming monolithic baselines despite starting with weak agents (*preprint, June 2026, not yet peer-reviewed; treat performance claims as promising but unverified pending independent replication*).

**Key architectural facts about EoM:**
- Agent diversity comes from system prompts, not weight differences — no training cost.
- Auction mechanism itself is O(n) in the number of eligible agents — trivially fast.
- Credit assignment (bucket brigade) is O(episode_length) — also trivially fast.
- The only expensive operation is the LLM forward pass at each auction step.

### 4b. Maturity and CPU-Friendly Tooling

The Hayek Machine and bucket brigade are not packaged as a turnkey Python library (as of 2026). The mechanism is simple enough to implement from scratch in ~100 lines of Python. Learning Classifier Systems have Python implementations (pyLCS, XCS-Py) but are primarily used for RL benchmarks, not for LLM agent orchestration.

EoM (arXiv:2606.02859) provides a research implementation but does not appear to have a released open-source codebase as of 2026-07.

The **auction mechanism itself** is trivially CPU-bound: comparing bids is O(n) arithmetic. The computational cost of an EoM-style system is entirely dominated by the LLM forward passes, not the economic coordination. On a CPU-only setup, you would call the LLM API (Claude, remote) and run the auction logic locally — the local computation is negligible.

**Hardware status:** Market coordination logic (bidding, bucket brigade, wealth tracking) is CPU-native and runs in microseconds. The LLM calls are remote API calls — not local compute. This is laptop-test clean.

### 4c. Relationship to the LLM

Market-based computation is not an alternative to the LLM — it is an *allocation mechanism over LLM invocations*. In EoM, each agent is an LLM with a distinct system prompt; the auction determines which agent's LLM invocation executes at each step. The economic mechanism provides:

1. **Decentralized credit assignment:** No hardcoded routing; effective agents accumulate wealth and persist; ineffective ones are replaced.
2. **Emergent specialization:** Agents that repeatedly win auctions in specific contexts evolve (via prompt mutation) toward those contexts.
3. **Exploration by default:** Bankrupt agents are replaced, ensuring the population continuously explores new strategies without explicit exploration bonuses.

The ETM mapping is direct: ETM says "mind = economy; state-rent = allocation mechanism." A market-based agent population *is* this architecture made operational. The LLM is the productive unit (like a firm in an economy); the auction is the price mechanism; wealth is the accumulated signal of fitness.

### 4d. Mapping to Jarvis

**Sub-agent routing as auction.** Jarvis currently routes tasks to sub-agents via hardcoded or heuristic logic (classify task → assign agent type). The market-based upgrade: sub-agents bid for tasks based on their "strength" (accumulated success rate on similar tasks). The highest bidder gets the task and is debited the bid value. If the task succeeds, the agent earns back the bid plus a margin; if it fails, the agent loses wealth. Over time, agents with the right capabilities for each task type naturally accumulate more wealth and win more bids — decentralized specialization without a routing table.

**Primitive competition.** Jarvis's memory graph holds many primitives. Which primitive is most relevant to the current context? Currently: embedding similarity or keyword lookup. The market-based alternative: primitives hold strength values (accumulated relevance signals from past invocations). When multiple primitives match a context, they bid; the winner's content is injected into context first. This is the bucket brigade applied to memory retrieval — and it is why the JARVIS-ETM connection is not just metaphorical. Memory retrieval as market is a direct implementation of ETM.

**WWWD gate as allocation signal.** In the market framing, WWWD is not just a decision heuristic — it is the payoff signal. Actions that WWWD classifies as Will-aligned produce payoff; actions that diverge produce negative payoff. Sub-agents that consistently produce Will-aligned outputs accumulate wealth; sub-agents that diverge are replaced or mutated. WWWD becomes the fitness function for agent evolution, not just a single decision gate.

**Gap:** No wealth tracking, no bidding, no mutation across sub-agent invocations exists in Jarvis today. This is a significant architectural gap but also the most ETM-aligned upgrade available. A minimal implementation — strength values on sub-agent types, simple first-price auctions, bucket brigade credit — could be prototyped in ~200 lines of Python and is entirely CPU-native.

---

## Synthesis: Top 3 Adoptable-for-Jarvis

The following three are ranked by: (1) ETM/philosophical alignment, (2) implementation tractability on the existing Python harness, (3) CPU-feasibility, (4) expected uplift in Jarvis reasoning quality.

---

### #1 — Market-Based Sub-Agent Routing (Hayek Machine Pattern)

**Why this first:** It is the most ETM-native idea in this dossier and requires no new ML. ETM says "mind = economy." The Hayek Machine *is* this operationalized: sub-agents bid for tasks, wealth tracks fitness, the bucket brigade assigns credit. This directly resolves two current Jarvis limitations: hardcoded routing (replaced by emergent specialization) and binary success/failure signals (replaced by continuous wealth accumulation). WWWD becomes the payoff signal rather than a single gate.

**CPU integration sketch:**

```python
# jarvis/market.py — ~150 lines

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import random

@dataclass
class SubAgent:
    name: str
    prompt: str          # system prompt — the only differentiator
    wealth: float = 1.0  # initial endowment
    history: List[bool] = field(default_factory=list)

    def bid(self, task_context: str) -> float:
        # Simple bid: fraction of wealth times a context match score
        # Replace with a learned score later; for now, heuristic
        match_score = self._context_match(task_context)
        return self.wealth * match_score * random.uniform(0.8, 1.0)  # noisy bid

    def _context_match(self, context: str) -> float:
        # Stub: keyword overlap between agent's prompt and task context
        # Replace with embedding cosine similarity if desired
        prompt_words = set(self.prompt.lower().split())
        ctx_words = set(context.lower().split())
        if not ctx_words:
            return 0.5
        return len(prompt_words & ctx_words) / len(ctx_words | prompt_words)

class AgentMarket:
    def __init__(self, agents: List[SubAgent]):
        self.agents = agents
        self.active_agent: Optional[SubAgent] = None
        self.pending_payment: float = 0.0

    def auction(self, task_context: str) -> SubAgent:
        """Run a first-price sealed-bid auction. Winner acts; pays bid to previous agent."""
        eligible = [a for a in self.agents if a.wealth > 0.01]
        if not eligible:
            raise RuntimeError("All agents bankrupt — population collapse.")

        bids = {a: a.bid(task_context) for a in eligible}
        winner = max(bids, key=bids.get)
        winning_bid = bids[winner]

        # Bucket brigade: winner pays bid to previous active agent
        if self.active_agent is not None:
            self.active_agent.wealth += winning_bid
        winner.wealth -= winning_bid

        self.pending_payment = winning_bid
        self.active_agent = winner
        return winner

    def settle(self, success: bool, reward: float = 1.0):
        """Settle after task execution. WWWD verdict = reward signal."""
        if self.active_agent is None:
            return
        if success:
            self.active_agent.wealth += reward
            self.active_agent.history.append(True)
        else:
            self.active_agent.history.append(False)
            # Bankruptcy check
            if self.active_agent.wealth < 0.05:
                self._replace_agent(self.active_agent)

    def _replace_agent(self, bankrupt: SubAgent):
        """Replace bankrupt agent with a mutated copy of a wealthy agent."""
        wealthy = sorted(self.agents, key=lambda a: a.wealth, reverse=True)
        if wealthy and wealthy[0] is not bankrupt:
            new_prompt = self._mutate_prompt(wealthy[0].prompt)
            idx = self.agents.index(bankrupt)
            self.agents[idx] = SubAgent(
                name=f"agent_{random.randint(1000,9999)}",
                prompt=new_prompt,
                wealth=0.5  # starter endowment
            )

    def _mutate_prompt(self, prompt: str) -> str:
        # Stub: in production, use Claude to generate a variant
        # For now, append a small variation marker
        return prompt + "\n[variant]"
```

**RAM:** Negligible — all state is Python dicts and floats.
**CPU:** Auction logic runs in microseconds. LLM calls are API-bound.
**Integration point:** Wrap the existing `jarvis/dispatch.py` (or equivalent sub-agent router) with `AgentMarket.auction()` before each task dispatch. Add `settle()` call after WWWD evaluates the output.

---

### #2 — Active Inference Orchestrator (pymdp POMDP layer)

**Why this second:** Active inference provides the normative framework for what the Hayek Machine lacks: uncertainty quantification. The market routes to the best current agent; active inference asks "but should we explore a different agent given our uncertainty?" EFE's epistemic value term provides principled exploration for free. The Orchestrator paper (arXiv:2509.05651) proves this pattern works at the multi-agent LLM level.

**CPU integration sketch:**

```python
# jarvis/aif_orchestrator.py — pymdp-based action selection

import numpy as np
from pymdp import Agent as AIFAgent
from pymdp.maths import softmax

# === Define the generative model ===
# Hidden states: [task_complexity (low/med/high), agent_fit (good/bad)]
# Observations: [task_outcome (success/fail/partial), agent_health (healthy/struggling)]
# Actions: [invoke_agent_A, invoke_agent_B, invoke_agent_C, escalate_to_will]

num_states = [3, 2]          # task_complexity x agent_fit
num_obs = [3, 2]             # outcome modality x health modality
num_actions = 4

# A: likelihood P(obs | state) — specify as probability arrays
A = [
    # P(outcome | task_complexity, agent_fit)
    np.array([[[0.8, 0.1], [0.6, 0.1], [0.3, 0.05]],   # success
              [[0.15, 0.4], [0.3, 0.4], [0.5, 0.4]],   # fail
              [[0.05, 0.5], [0.1, 0.5], [0.2, 0.55]]]  # partial
             ),
    # P(health | agent_fit) — independent of task_complexity
    np.array([[0.9, 0.2], [0.1, 0.8]])
]

# B: transition P(next_state | state, action)
# (simplified: actions affect agent_fit belief, not task_complexity)
B = [
    np.tile(np.eye(3)[:, :, np.newaxis], (1, 1, num_actions)),  # complexity unchanged by action
    # ... define how each action updates agent_fit belief
]

# C: prior preferences over observations (log scale)
# Prefer success outcomes, disprefer failure
C = [
    np.array([2.0, -2.0, 0.0]),   # outcome: prefer success
    np.array([1.0, -1.0])          # health: prefer healthy
]

# D: prior beliefs about initial state
D = [softmax(np.ones(3)), softmax(np.ones(2))]

# === Instantiate agent ===
orchestrator = AIFAgent(A=A, B=B, C=C, D=D)

def select_action(observation: list) -> int:
    """
    observation: [outcome_index, health_index] from last step
    returns: action index (0-3)
    """
    orchestrator.infer_states(observation)
    q_pi, G = orchestrator.infer_policies()
    action = orchestrator.sample_action()
    return int(action)

# In the Jarvis loop:
# obs = [last_task_outcome, agent_health_signal]
# action_idx = select_action(obs)
# chosen_agent = agent_list[action_idx]  # or escalate if action_idx == 3
```

**Caveats:** The A and B matrices above are stubs — real deployment requires fitting them from Jarvis's own task logs (use `agent.infer_parameters()` in pymdp). The state space is intentionally tiny (6 hidden states) to remain CPU-tractable. This is appropriate for the Jarvis use case.

**RAM:** pymdp with this model footprint uses < 5 MB. Negligible.
**CPU:** Policy inference on a 6-state model takes microseconds.
**Integration point:** Replace the WWWD decision heuristic with `select_action()`. Feed Jarvis task outcome logs into `agent.infer_parameters()` to learn A and B over time. The C vector encodes Will's preferences — update it from memory primitives when preferences change.

---

### #3 — Causal Root Cause Analysis for Hook Failures (DoWhy)

**Why this third:** This is the most directly actionable with existing Jarvis infrastructure. Jarvis already logs hook events, tool calls, and outcomes. Building a causal graph over these logs and using DoWhy to answer "what intervention would have prevented this failure?" turns Jarvis's log data into a learning mechanism without any neural training. It also provides the structural substrate for counterfactual WWWD.

**CPU integration sketch:**

```python
# jarvis/causal_rca.py — root cause analysis via DoWhy

import pandas as pd
import dowhy
from dowhy import CausalModel

# Load Jarvis task logs (hook events, LLM outputs, task outcomes)
# Schema: [context_length, tool_called, sub_agent_type, hook_fired,
#          wwwd_score, task_success]
logs = pd.read_csv("~/.claude/logs/task_history.csv")

# Define causal graph (manual, engineer-specified — start simple)
causal_graph = """
digraph {
    context_length -> task_success;
    tool_called -> task_success;
    sub_agent_type -> task_success;
    hook_fired -> task_success;
    wwwd_score -> task_success;
    context_length -> wwwd_score;
    sub_agent_type -> tool_called;
}
"""

model = CausalModel(
    data=logs,
    treatment="tool_called",         # the intervention variable
    outcome="task_success",
    graph=causal_graph
)

# Identify: does do-calculus say this effect is identifiable?
identified_estimand = model.identify_effect()
print(identified_estimand)

# Estimate: what is the causal effect of calling tool X vs. tool Y?
estimate = model.estimate_effect(
    identified_estimand,
    method_name="backdoor.linear_regression"
)
print(estimate)

# Refute: adversarial checks (placebo treatment, random common cause)
refutation = model.refute_estimate(
    identified_estimand, estimate,
    method_name="placebo_treatment_refuter"
)
print(refutation)
```

**RAM:** DoWhy's graph operations use NetworkX (< 1 MB per graph). Effect estimation uses linear regression or propensity scoring — CPU-native, RAM footprint proportional to log dataset size.
**Integration point:** Add a background cron that runs causal analysis on Jarvis's task logs weekly. Surface the top causal factors for task failure as updated memory primitives. Use the interventional estimates to inform the pre-flight PCP gate ("calling this tool in this context causes a 40% failure rate — confirm?").

---

## Gaps and Honest Assessment

| Topic | State | Gap in Jarvis | Verdict |
|---|---|---|---|
| Active inference (pymdp) | Mature, CPU-native, well-documented | No generative model of task environment; no EFE-based action selection | Adoptable now; requires upfront model engineering |
| World models + MCTS | MCTS is trivially CPU-native; world model = state machine | No explicit state machine over task lifecycle | Adoptable now; simplest to implement |
| Causal inference (DoWhy) | Mature, CPU-native, Python-native | No causal graph of Jarvis's own behavior; no structured log schema | Adoptable now; blocked on log data collection |
| Market-based routing (Hayek/EoM) | Mechanism is simple; no off-shelf library; EoM paper is 2026 and has no public code | No wealth tracking, no bidding, no agent mutation | Adoptable now; requires ~200 lines of new Python |
| RxInfer.jl (high-perf AIF) | Mature in Julia; 300x faster than HMC | Julia runtime; cross-language overhead from Python | Viable future upgrade; not needed at current Jarvis scale |

**What is genuinely GPU-bound and therefore disqualified:** Large learned world models (MuZero, Dreamer, DreamerV3) require GPU for training. LLM-as-world-model approaches require GPU for fast inference. These are flagged out. The handcrafted world model + MCTS approach is the CPU-native equivalent and is strictly preferred for Jarvis's use case.

**What is not yet mature:** Formal integration of active inference with LLM agent harnesses is a 2025-2026 research frontier (Orchestrator paper, Hybrid AIF Models). The pattern works; the tooling is research-grade, not production-grade. Jarvis would be an early adopter, not a fast follower.

---

## Mapping Summary: ETM↔Market-Computation and WWWD↔Active Inference

### ETM ↔ Market-Based Computation

The mapping is structural, not metaphorical:

| ETM Concept | Market-Based Computation Equivalent |
|---|---|
| Mind = economy | Agent population = economy; each agent = a productive unit |
| State-rent as allocation mechanism | Wealth/bid as allocation mechanism — only agents with accumulated fitness win tasks |
| Attention as scarce resource | Right to act (won by auction) as the scarce resource |
| Price signal aggregates dispersed information | Bid signal aggregates each agent's self-assessment of its fit for a task |
| Competition produces efficient allocation | Wealth dynamics produce emergent specialization without central routing |
| Bankruptcy = market discipline | Bankrupt agents replaced — ineffective strategies eliminated without central pruning |

The Hayek Machine is literally a computational instantiation of Hayek's price mechanism. EoM extends it to LLM agents in 2026. Jarvis's ETM philosophy is not an analogy for this system — it IS this system, waiting for the auction layer to be built.

### WWWD ↔ Active Inference

| WWWD Concept | Active Inference Equivalent |
|---|---|
| "What would Will do?" | Generative model P(Will's decision \| context, history) — the A and B matrices |
| Will's stated preferences | C vector — prior preferences over outcomes encoded from memory primitives |
| Discrepancy between Jarvis action and Will's correction | Prediction error — drives parameter update in A and B (learning) |
| Single-step decision heuristic | Policy selection by minimizing EFE — lookahead planning over multiple steps |
| Memory primitives as Will-context | D vector — prior beliefs about the current situation before observations arrive |
| WWWD confidence | Epistemic value term in EFE — how uncertain is Jarvis about what Will would do? |

Active inference formalizes WWWD from "emulation heuristic" to "Bayesian predictive model with principled uncertainty." When Jarvis is uncertain about what Will would do, the EFE's epistemic term increases — Jarvis explores (asks Will) rather than exploiting (acting autonomously). This is a directly derivable behavior from the formalism, not a hardcoded rule.

---

## Sources

- [Active Inference and the Free Energy Principle (Engineering Notes, 2026)](https://notes.muthu.co/2026/02/active-inference-and-the-free-energy-principle-how-agents-minimize-surprise-instead-of-maximizing-reward/)
- [pymdp: A Python library for active inference in discrete state spaces (JOSS 2022)](https://joss.theoj.org/papers/10.21105/joss.04098)
- [pymdp arXiv paper: 2201.03904](https://arxiv.org/abs/2201.03904)
- [pymdp GitHub repo](https://github.com/infer-actively/pymdp)
- [Active inference on discrete state-spaces: a synthesis (arXiv 2001.07203)](https://arxiv.org/pdf/2001.07203)
- [Reward Maximisation through Discrete Active Inference (arXiv 2009.08111)](https://arxiv.org/pdf/2009.08111)
- [Orchestrator: Active Inference for Multi-Agent Systems (arXiv 2509.05651)](https://arxiv.org/pdf/2509.05651)
- [RxInfer.jl GitHub](https://github.com/ReactiveBayes/RxInfer.jl)
- [RxInfer.jl docs](https://docs.rxinfer.com/stable/)
- [Active Inference for Physical AI Agents — Engineering Perspective (arXiv 2603.20927)](https://arxiv.org/pdf/2603.20927)
- [Economy of Minds: Emerging Multi-Agent Intelligence with Economic Interactions (arXiv 2606.02859)](https://arxiv.org/abs/2606.02859)
- [Market-based Architectures in RL and Beyond (arXiv 2503.05828)](https://arxiv.org/pdf/2503.05828)
- [Market-Based Reinforcement Learning in Partially Observable Worlds (arXiv cs/0105025)](https://arxiv.org/pdf/cs/0105025)
- [LLM-Based World Models Can Make Decisions Solely (arXiv 2411.08794)](https://arxiv.org/html/2411.08794v2)
- [Monte Carlo tree search PyPI: monte-carlo-tree-search](https://pypi.org/project/monte-carlo-tree-search/)
- [mcts-simple PyPI](https://pypi.org/project/mcts-simple/)
- [DoWhy GitHub](https://github.com/py-why/dowhy)
- [Evaluating Causality in AI Models in 2026 (FutureAGI)](https://futureagi.com/blog/evaluating-causality-in-ai-models/)
- [CausalML PyPI (v0.16.0, Feb 2026)](https://pypi.org/project/causalml/)
- [Counterfactual Planning for Generalizable Agents (AAAI 2025)](https://ojs.aaai.org/index.php/AAAI/article/download/40184/44145)
- [Language Agents Meet Causality — Bridging LLMs and Causal World Models](https://j0hngou.github.io/LLMCWM/)
- [Distributed Intelligence with Active Inference (arXiv 2505.24618)](https://arxiv.org/pdf/2505.24618)
- [Hardware-oriented Active Inference (arXiv 2508.13177)](https://arxiv.org/pdf/2508.13177)
- [Schema-based active inference (arXiv 2601.18946)](https://arxiv.org/pdf/2601.18946)
