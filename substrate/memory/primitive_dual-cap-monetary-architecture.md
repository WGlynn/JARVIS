---
name: "Three-Token Economy (evolved from Dual-Cap Architecture)"
description: "VIBE (Ethereum/Base, lifetime cap 21M, burns permanent) for governance/scarcity. JUL (operational token, elastic). CKB-native token (circulating cap, state rent model) for on-chain utility. Three monetary philosophies matched to chain architecture. Holders, users, builders. Originally conceived as dual-cap (Session 067), evolved into three-token economy."
type: project
---

## Three-Token Economy (evolved from Dual-Cap Monetary Architecture)

> **Note**: This primitive was originally "Dual-Cap Monetary Architecture" (Session 067). The concept evolved into a three-token economy: VIBE (governance/scarcity), JUL (operational/elastic), and CKB-native (state rent/utility). The dual-cap insight (lifetime vs circulating) remains the foundation.

### The Insight

Two cap models exist for capped-supply tokens:

**Lifetime Cap**: Once N tokens have been minted across all time, no more can ever exist. Burns are permanent. Supply only goes down. Bitcoin model. Scarcity is absolute.

**Circulating Cap**: At most N tokens can exist at any given time. Burns release capacity for future minting. Supply breathes — tokens flow through the system like matter through an ecosystem. CKB state rent model. Scarcity is relative to usage.

Neither is universally better. They optimize for different things.

### The Tandem Design

Deploy BOTH — each on the chain whose architecture matches its model:

**VIBE on Ethereum/Base — Lifetime Cap (21M ever)**
- Governance + scarcity signal
- Burns are permanent (every burn makes remaining tokens more valuable forever)
- Attracts holders (investors, stakers, governance participants)
- Bitcoin narrative: simple, clean, "21M means 21M"
- Shapley-distributed through contribution, never airdropped
- P-001 enforced: distributions are irreversible, can't burn-and-remint to game Shapley

**CKB-Native Token — Circulating Cap (state rent model)**
- Operational liquidity for the UTXO ecosystem
- Burns = state occupation (locking tokens to use CKB cells for computation/storage)
- Release state = tokens return to circulation (available for re-minting/reuse)
- Attracts users (builders, agents, data providers, compute contributors)
- Mirrors CKB's own economic model (CKBytes occupied for state, released when state freed)
- The ecosystem breathes — tokens flow like energy through a living system

### Why This Works

The two tokens serve different functions in the same protocol:

| Property | VIBE (Lifetime) | CKB-Native (Circulating) |
|----------|----------------|------------------------|
| Scarcity model | Absolute (fixed forever) | Relative (bounded by usage) |
| Burns | Permanent destruction | Temporary occupation |
| Attracts | Holders, investors | Users, builders |
| Chain | Ethereum/Base (account model) | Nervos CKB (UTXO/cell model) |
| Governance | Direct (ERC20Votes) | Indirect (usage = skin in game) |
| Shapley role | Reward distribution | Operational cost/access |
| Analogy | Gold (scarce, stored) | Energy (bounded, flows) |
| Narrative | "Only 21M will ever exist" | "The ecosystem has a carrying capacity" |

### The CKB State Rent Connection

CKB's state model is uniquely suited to circulating cap because state occupation IS the burn mechanism:

- Creating a cell = locking CKBytes (burning from circulation)
- Destroying a cell = releasing CKBytes (returning to circulation)
- Total CKBytes bounded by issuance schedule
- Available CKBytes = total issued - total occupied

A CKB-native VibeSwap token would mirror this exactly:
- Opening a position/pool = locking tokens (burns from circulating supply)
- Closing a position = releasing tokens (available for re-minting)
- Total capacity bounded but usage-elastic
- The protocol's monetary supply tracks its actual utilization

This is biological — cells consume resources when active, release them when they die. The ecosystem has a carrying capacity (max supply) but the atoms cycle through organisms (positions, pools, agents).

### Both Feed the Same Shapley Distribution

The key architectural choice: both tokens participate in the same cooperative game. VIBE contributions and CKB-native contributions are measured by the same Shapley axioms.

A CKB builder who locks tokens to occupy state is contributing to the ecosystem (enabling computation, providing infrastructure). A VIBE holder who stakes for governance is contributing to the ecosystem (directing resources, signaling priorities). Shapley measures both contributions on the same scale.

This means: you can earn VIBE (permanent, scarce) by contributing operational value on CKB (elastic, flowing). The permanent token rewards the elastic work. Scarcity compensates utility.

### Origin

Will Glynn, Session 067, 2026-03-18:
> "The circulating cap idea is closer to Nervos CKB state rent model. I can see it being used in tandem with the OG VibeSwap."

Design decision: VIBE locked to lifetime cap (commit `27bc912`). Circulating cap reserved for CKB-native implementation where the chain architecture matches the monetary philosophy.
