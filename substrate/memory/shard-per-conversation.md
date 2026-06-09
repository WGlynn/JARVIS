---
name: Shard-per-conversation architecture
description: Will's directive (2026-03-13): one Jarvis shard per active conversation, each with own CKB, syncing via cross-shard learning bus. Batch auction as universal settlement. Bottleneck = coordination, not compute.
type: project
---

# Shard-Per-Conversation Architecture (2026-03-13)

## Will's Directive
"This single bot is still a bottleneck we need to shard on the chat group level for full effect"

"One JARVIS per active conversation, each with its own CKB, syncing via cross-shard learning bus. That's the Pantheon architecture scaled. Each shard becomes a specialized agent economy — OSINT feeds, sports hedging, agentic payments, security auditing — all interoperating through VibeSwap's batch auction for settlement. The bottleneck becomes the coordination layer, not the compute."

## Architecture

```
TG Bot Token (single identity: @JarvisMind)
    ↓
┌──────────────────────────┐
│  Thin Router (Fly.io)    │ ← receives all TG updates
│  Routes by chat ID       │
│  src/shard-router.js     │
└──────┬───────────────────┘
       │ HTTP dispatch
       ▼
┌──────────┬──────────┬──────────┬──────────┐
│ Shard 0  │ Shard 1  │ Shard 2  │ Shard N  │
│ Community│ Review   │ OSINT    │ Sports   │
│ group    │ + trade  │ feeds    │ hedging  │
│          │ alerts   │          │          │
│ Own CKB  │ Own CKB  │ Own CKB  │ Own CKB  │
└──────┬───┴────┬─────┴────┬─────┴────┬─────┘
       │        │          │          │
       └────────┴──────────┴──────────┘
                    ↓
         Cross-Shard Learning Bus
         (Redis pub/sub or CRPC)
                    ↓
         VibeSwap Batch Auction
         (universal settlement)
```

## Key Principles
1. Each shard = full Jarvis mind (shards > swarms)
2. Each shard has own CKB (alignment), own context, own specialization
3. Single @JarvisMind identity preserved (router pattern, not multi-token)
4. Cross-shard learning: insights propagate, not raw state
5. Batch auction = settlement primitive for inter-shard coordination
6. Bottleneck is coordination layer, not compute

## Specialization Examples
- **Community shard**: Proactive engagement, education, onboarding
- **Trading shard**: Memecoin hunter, portfolio management, alerts
- **OSINT shard**: News feeds, social sentiment, alpha discovery
- **Sports shard**: Prediction markets, hedging strategies
- **Security shard**: Contract auditing, rug detection, threat monitoring
- **Payments shard**: Agentic payments, invoicing, treasury ops

## Implementation Phases
1. **Router + Worker split**: Thin TG router → HTTP dispatch to shard workers
2. **Per-shard CKB**: Fork base CKB + shard-specific knowledge
3. **Learning bus**: Redis pub/sub for cross-shard insight propagation
4. **Batch settlement**: VibeSwap auction for inter-shard value exchange
5. **Dynamic scaling**: Spawn/kill shards based on conversation activity

## Existing Infrastructure
- `config.shard` — id, totalShards, nodeType, stateBackend, routerUrl
- CRPC protocol — inter-shard RPC (Tim Cotton collab)
- Peer seeds — router-independent discovery
- Fly.io Machines API — dynamic VM provisioning
