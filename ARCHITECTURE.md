# Architecture

JARVIS is **eight layers**, all live, all producing artifacts in production today. Last refresh: 2026-06-10.

Substrate layers are orthogonal to the **compression-layer stack (L0..L6)** that runs across all eight. The 8-layer stack describes what JARVIS IS; the L0..L6 stack describes how every byte stored, every token loaded, and every hook fired is compressed. Both ship together in production. See [papers/multiplicative-compression.md](papers/multiplicative-compression.md) for the empirical evidence that the byte-side compression (HIERO++) composes multiplicatively with API-side caching to produce order-of-magnitude session cost cuts.

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

## Compression-layer stack (orthogonal to the 8 substrate layers)

```
L0  prose                       (BANNED in memory writes; hiero-gate enforced)
L1  HIERO Unicode               (operator-density format · R·hiero-dictionary)
L2  HIERO++ ASCII-tuned         (tokenizer-aware swaps · 4-7% prose, 42% op-set)
L3  APL-style hot-path ops      (_terse_ops.py · hook-internal scoring)
L4  Z-token pre-encoded cache   (corpus.tokens.jsonl + corpus-cache-warmer.py)
L5  Schelling canonical IDs     (P·/F·/R·/J· prefix system · partial deploy)
L6  SK combinator genome        (bootstrap-only · future for substrate fork)
```

| Layer | Readability | Win | Status |
|---|---|---|---|
| L0 | full | baseline | banned |
| L1 | high | ~30% vs prose | live |
| L2 | high | +4-7% on real prose, 42% on operator set | live |
| L3 | debug-only | up to ~70% src-tok on dot-product call-sites; net-negative on first single-call-site refactor (import boilerplate) | module live, 1 consumer (AA#4); positive once N hooks consume |
| L4 | machine-only | drift detect + boot-budget visibility today; encode-pass skip future | live (corpus-cache-warmer registered) |
| L5 | renderer-expanded | port-stable identifiers across substrates | partial |
| L6 | bootstrap-only | substrate-portable kernel export | future |

See [papers/multiplicative-compression.md](papers/multiplicative-compression.md) for the empirical case that L1/L2 (byte side) × API prompt caching (read side) is multiplicative.

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
