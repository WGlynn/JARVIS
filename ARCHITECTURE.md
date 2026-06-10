# Architecture

JARVIS is **eight layers**, all live, all producing artifacts in production today. Last refresh: 2026-06-10.

```
┌──────────────────────────────────────────────────────────────┐
│ 8. Filesystem-as-substrate                                   │
│    OSCH: markdown + git as the orchestration layer           │
│    + self-audit (link-rot · orphan-hook · path-integrity)    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ 7. Stateful applications                               │  │
│  │    TG bot suite · signature validator · jarvis-network │  │
│  │    Filesystem CRMs · 125 papers (59 PDF)               │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │ 6. Agent overlay                                 │  │  │
│  │  │    Subagents · skills · MCP · cron (durable)     │  │  │
│  │  │    · RSAW parallel audit · WWWD cognition gate   │  │  │
│  │  │  ┌────────────────────────────────────────────┐  │  │  │
│  │  │  │ 5. Meta-protocols                          │  │  │  │
│  │  │  │    AMD · AGov · SGM · Universal→Hook · ETM │  │  │  │
│  │  │  │    + WWWD · RSAW · JARVIS-OS (V3 capstone) │  │  │  │
│  │  │  │  ┌──────────────────────────────────────┐  │  │  │  │
│  │  │  │  │ 4. Discipline                        │  │  │  │  │
│  │  │  │  │    491 typed memory files            │  │  │  │  │
│  │  │  │  │    (218 prim · 196 fb · 60 proj      │  │  │  │  │
│  │  │  │  │     · 17 ref); 458 verify-pass       │  │  │  │  │
│  │  │  │  │  ┌────────────────────────────────┐  │  │  │  │  │
│  │  │  │  │  │ 3. Anti-hallucination          │  │  │  │  │  │
│  │  │  │  │  │    Substance · HIERO · entity- │  │  │  │  │  │
│  │  │  │  │  │    cross-ref · conflict-detect │  │  │  │  │  │
│  │  │  │  │  │    · time-logic · em-dash      │  │  │  │  │  │
│  │  │  │  │  │    · directive-verb-class      │  │  │  │  │  │
│  │  │  │  │  │  ┌──────────────────────────┐  │  │  │  │  │  │
│  │  │  │  │  │  │ 2. Persistence (6 tiers) │  │  │  │  │  │  │
│  │  │  │  │  │  │  ┌────────────────────┐  │  │  │  │  │  │  │
│  │  │  │  │  │  │  │ 1. Hooks           │  │  │  │  │  │  │  │
│  │  │  │  │  │  │  │    50 (28+22 sc)   │  │  │  │  │  │  │  │
│  │  │  │  │  │  │  │    Deterministic   │  │  │  │  │  │  │  │
│  │  │  │  │  │  │  └────────────────────┘  │  │  │  │  │  │  │
│  │  │  │  │  │  └──────────────────────────┘  │  │  │  │  │  │
│  │  │  │  │  └────────────────────────────────┘  │  │  │  │  │
│  │  │  │  └──────────────────────────────────────┘  │  │  │  │
│  │  │  └────────────────────────────────────────────┘  │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## Layer dependencies

```
1 → ∀         : hooks fire ⊥ context; ∀ layers-above assume gates-work
2 → 3,4,5,6,7 : persistence ⇒ coherence-across-sessions
3 → 4         : anti-hallucination violations ⇒ discipline primitives
4 → 5         : discipline patterns @ multi-level ⇒ meta-protocol promotion
5 → 6,7       : meta-protocols govern overlay ∧ application design
6 → 7         : agent overlay ⇒ stateful applications
7 → 8         : ∀ applications run on filesystem substrate
```

## The kernel framing

```
JARVIS ≡ coordination-layer over LLM-substrates
       ≅ OS ≡ coordination-layer over hardware-substrates
CPU interchangeable · kernel ¬ interchangeable · applications run-on kernel
```

- **Hardware substrate** ≡ providers ∈ {Anthropic, OpenRouter, DeepSeek, Gemini, Cerebras, Groq, Ollama}
- **Router** ≡ layer-7 TG bot, selects-across providers
- **Kernel** ≡ layers 1-4 (hooks · persistence · anti-hallucination · discipline) — fire ⊥ active-substrate
- **User-space** ≡ layers 5-7 (meta-protocols · agent overlay · applications) — consume kernel guarantees

## What survives substrate degradation

| Layer | Survives LLM swap? | Why |
|---|---|---|
| 1 — Hooks | ✓ full | Python, regex, state-machines — substrate-independent |
| 2 — Persistence | ✓ full | markdown + git, substrate-independent |
| 3 — Anti-hallucination | ✓ full | regex + state-machines |
| 4 — Discipline | ✓ full | files |
| 5 — Meta-protocols | ✓ full | ideas ¬ code |
| 6 — Agent overlay | ◐ partial | Claude-specific impl, conceptually portable |
| 7 — Applications | ◐ partial | portable with substrate-specific tuning |
| 8 — Filesystem | ✓ universal | the substrate itself |

**Wrapper test**: substrate swap ⇒ what survives?
- Wrapper: nothing (wrapper ≡ the LLM call)
- JARVIS: layers 1-5 fully · layer 6 conceptually · layers 7-8 with adaptation
