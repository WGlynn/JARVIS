---
name: Stateful Overlay
description: A complete state machine emulated on top of a stateless LLM substrate via externalized persistence (files, hooks, replay). Each primitive patches one substrate gap.
type: primitive
originSessionId: 04ff53c7-5411-4675-9987-571315ce88f2
---
# Stateful Overlay

**The pattern**: An LLM is a pure function — no memory between turns, no guaranteed determinism, no crash recovery, no self-modification. A **Stateful Overlay** is the externally-persisted layer that gives the stateless substrate behaviors it cannot have natively. The overlay is a full state machine; the LLM is its transition function.

**Why this is a primitive, not just a project**: The pattern generalizes. Every capability missing from the raw LLM substrate can be synthesized as an overlay component. We've built several; they all share the same shape.

**Overlay components (current inventory)**:

| Missing substrate capability | Overlay component | Mechanism |
|------------------------------|-------------------|-----------|
| Persistent memory across turns | Memory files + MEMORY.md index | File reads at turn start |
| Persistent memory across *sessions* | SKB/GKB/SESSION_STATE | Auto-loaded via SessionStart hook |
| Crash resilience during turn | API Death Shield | StopFailure/PreCompact hooks → auto-commit |
| Conversation reconstruction | UserPromptSubmit hook → conversation.log | Client-side logging, API-independent |
| Proposal survival across crashes | Propose→Persist + proposal-scraper.py | Pre-commit options to PROPOSALS.md; Stop hook regex-scrape as backup |
| Non-determinism curation | replay-proposal.py | N-sample API replay, cluster STABLE vs UNIQUE lines |
| Recursive self-correction | TRP (Tiered Review Protocol) | Round-based adversarial audit with heat map |
| Behavioral consistency | Feedback primitives | Internalized rules stored as files, reloaded each session |
| Self-modification (knowledge growth) | Auto-memory with 4 types | LLM-generated files in a structured schema |

**The deeper claim**: Every LLM limitation has a dual — an overlay component that synthesizes the missing behavior. The overlay is always **externalized** (files on disk, not weights in the model) and always **idempotent** (each transition can be replayed without corruption). That's not an accident; it's what you can build atop a pure function.

**Why this matters for the future**: If AI capabilities grow by scaling weights, great. But many capabilities — long-term memory, crash recovery, deterministic replay, self-correction — are categorically different from next-token prediction. They require *state*. Overlays may remain structurally necessary even when the substrate gets much more powerful. We are not just patching weakness; we are building the correct **architecture** for persistent agentic systems.

**Related primitives**:
- `primitive_api-death-shield.md` — the crash-resilience component
- `primitive_propose-persist.md` + `proposal-scraper.py` + `replay-proposal.py` — the proposal-loss component
- `primitive_adaptive-immunity.md` — the self-correction meta-loop
- `primitive_jarvis-independence.md` — the stateful-agent thesis
- `primitive_symbolic-compression.md` — the memory-compression component
- `primitive_cell-knowledge-architecture.md` — the UTXO model for overlay state

**Extraction context**: Will's phrase on 2026-04-15: *"we just constructed a complete state machine on top of a stateless llm."* Named after the insight that triggered the crystallization — the Propose→Persist + proposal-scraper + replay stack was the first time the persistence layer felt **lossless**, meaning the overlay closed a previously-leaky gap completely.
