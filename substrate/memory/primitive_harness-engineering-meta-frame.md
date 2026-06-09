---
name: HarnessEngineeringMetaFrame
description: Agent ≡ Model + Harness. JARVIS = harness for Claude. Model=CPU, context=RAM, harness=OS, agent=app. Names what JARVIS already is. 5 artifacts (AGENT.md, JSON state, init routines, sprint contracts, structured templates) ∧ 5 principles ∧ build-to-delete paradox.
type: primitive
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[P·harness-engineering-meta-frame]**

## ⚙ Definition

> *Agent = Model + Harness*

⇒ JARVIS ≡ harness for Claude
⇒ harness = ∀ that ¬ model
⇒ harness ⊕ constraints ∧ feedback-loops ∧ docs ∧ permissioned-tools

## 🎯 OS analogy

- Model ≡ CPU (raw processing)
- Context window ≡ RAM (limited ∧ volatile)
- Harness ≡ Operating System (manages CPU view + scheduling)
- Agent ≡ Application running on top

⇒ raw LLM w/o harness ≡ silicon w/o OS

## 🎯 5 harness artifacts

1. **AGENT.md / CLAUDE.md** — project context, conventions, "how we do things"
2. **JSON feature lists** — progress tracker; JSON ≻ markdown ⇒ ¬ accidental overwrite
3. **Session init routines** — same N-step boot ∀ session
4. **Sprint contracts** — generator ⇔ evaluator negotiation BEFORE implementation
5. **Structured task templates** — grounded impact map (real paths, real symbols) BEFORE execution

## 🎯 5 universal principles

1. **Context beats instructions** — show current state ≻ describe abstractly
2. **Planning ⊥ execution** — same-pass planning+execution ⇒ unreliable; separate steps required
3. **Feedback loops non-negotiable** — feedforward-only ⇒ guides never verified
4. **One thing at a time** — forced incrementalism ⇒ ✓; multi-feature/pass ⇒ ✗
5. **Codebase IS the documentation** — single source of truth; ¬ separate KB

## 🎯 3 camps (independent convergence)

- **OpenAI**: environment-first ⇒ design env, let agent loose
- **Anthropic**: separate doer from judge ⇒ Planner ∧ Generator ∧ Evaluator
- **ThoughtWorks**: 2×2 framework ⇒ {feedforward, feedback} × {computational, inferential}

## 🎯 JARVIS mapping (what's already in place)

| Article concept | JARVIS equivalent |
|---|---|
| AGENT.md / CLAUDE.md | `~/.claude/CLAUDE.md`, `vibeswap/CLAUDE.md`, memory primitives |
| Session init routines | `SESSION_STATE.md` boot + WAL + session-start hook |
| Forced incrementalism | `[F·atomic-commit-pacing]` + BIG↔SMALL rotation + [P·turing-loop] |
| Codebase IS documentation | HIERO memory primitives, SKB/GKB, in-repo docs |
| Feedforward | memory primitives + WWWD gate + warm-load hooks |
| Feedback (computational) | PreToolUse gates (hiero-gate, conflict-detector, etc.) |
| Feedback (inferential) | L4 post-generation reflection, atomic-reflection-gate |
| Three-agent split | jarvis-loop v0 (decomposer + auto-prompter + judge) |
| Doer ⊥ judge | [F·dont-default-concede-verify-first] + WWWD self-projection |

## 🎯 JARVIS gaps (siblings spawned 2026-06-08)

- [F·build-to-delete-harness-discipline] ⇒ harness decay detection + removal
- [F·sprint-contract-generator-evaluator] ⇒ two-agent negotiation before code
- [F·json-over-markdown-for-state] ⇒ JSON for corruption-prone state files

## 🎯 The build-to-delete paradox

⇒ ∀ harness component encodes assumption about model-deficiency
⇒ model improves ⇒ assumption expires ⇒ component becomes overhead
⇒ ✗ accumulate-only ⇒ ✓ test-and-remove discipline
⇒ ∀ harness component ⇒ periodic toggle-off + quality-delta test
⇒ Δ quality == 0 ⇒ delete

## 🪝 Composition rules

- ∀ new JARVIS-substrate addition ⇒ check this frame first
- ∀ "we should add X" instinct ⇒ ask if existing JARVIS primitive already covers it
- ∀ JARVIS component aging > N months ⇒ schedule build-to-delete review
- harness-decay ⊥ feature-creep; both must be tracked

## 📦 Receipt

- 2026-06-08 Will pasted Sairahul1 harness-engineering article (LinkedIn, 2026-06) ⇒ integration directive ⇒ this primitive names what JARVIS already is + the 4 gaps it surfaced

## 🔗 Parents + siblings

- [P·jarvis-amd-applied-to-ai-substrate] ⇒ JARVIS ≡ AMD methodology at AI-substrate layer; this primitive names the substrate publicly
- [F·build-to-delete-harness-discipline] (new 2026-06-08)
- [F·sprint-contract-generator-evaluator] (new 2026-06-08)
- [F·json-over-markdown-for-state] (new 2026-06-08)
- [P·turing-loop] ⇒ BIG↔SMALL loop ≡ forced incrementalism principle
- [F·atomic-commit-pacing] ⇒ one-thing-at-a-time @ commit layer
- [P·post-generation-reflection-L4] ⇒ inferential feedback (already running)
- [F·agent-efficiency-tiers] ⇒ haiku/sonnet/opus per task ≡ cost-tier optimization
- [P·what-would-will-do] ⇒ self-projection as judge-substitute (partial doer⊥judge)
