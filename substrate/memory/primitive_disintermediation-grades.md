---
name: "Disintermediation Grades — The Cincinnatus Roadmap"
description: Six-grade scale (0-5) measuring how peer-to-peer each protocol interaction is. Every onlyOwner function is a middleman. Every off-chain component is a middleman. The endgame is Grade 5 everywhere — Will walks away and the protocol runs itself. This IS the roadmap.
type: project
---

## Disintermediation Grades

### The Principle

If you figuratively imagine middlemen as satan getting in between people, they must be identified and eradicated from reality. Every intermediary — including the founder — is a structural compromise that must be graded, tracked, and eliminated.

### The Scale

**Grade 0 — Fully Intermediated**: Every interaction requires a trusted third party. You cannot transact without them. They have full control and can censor, extract, or deny service.

**Grade 1 — Transparent Intermediary**: The middleman exists but their extraction is visible. You can see the fees, the MEV, the admin actions. Transparency without elimination.

**Grade 2 — Optional Intermediary**: Peer-to-peer path exists alongside the intermediated path. Users CAN go direct but the middleman is still available (and most default to it).

**Grade 3 — Economically Unviable Intermediary**: Shapley fairness proves the middleman adds zero marginal value. P-001 detects their extraction. The protocol doesn't pay them (null player axiom). They can exist but they starve.

**Grade 4 — Structurally Impossible Intermediary**: The protocol architecture eliminates the surface for intermediation. No position for a middleman to occupy. Like commit-reveal — you can't front-run what you can't see.

**Grade 5 — Pure Peer-to-Peer**: No intermediation point exists. The protocol is the medium, not the middleman. Like language between two people — it facilitates but doesn't intermediate.

### Current State of VibeSwap

| Interaction | Current Grade | Middleman | Target | How to Get There |
|-------------|--------------|-----------|--------|-----------------|
| Swap execution | **4** | None (commit-reveal) | 5 | Already near-peer-to-peer. Grade 5 = direct atomic swap without batch settlement |
| LP fee distribution | **2** | Authorized creator picks participants/weights | 4 | On-chain contribution tracking → auto-game creation → no human picks participants |
| Token minting | **1** | Owner can mint directly, bypassing emission schedule | 4 | Remove owner from mint path. Only EmissionController mints. Enforce in contract. |
| Governance | **0** | 50+ onlyOwner functions, unilateral pause/blacklist/upgrade | 4 | Cincinnatus Protocol: timelock → multisig → governance → renounce. GovernanceGuard with Shapley veto. |
| Trust scoring | **1** | Owner-only recalculateTrustScores() | 3 | Permissionless recalculation with rate limiting. Anyone can trigger, BFS is deterministic. |
| Price oracle | **1** | Off-chain Python operator signs attestations | 3 | Multi-source oracle with Shapley-weighted consensus. On-chain TWAP as fallback. Operator becomes optional. |
| Cross-chain | **1** | LayerZero relayers | 2 | Already using LZ which has permissionless relaying. But still depends on LZ infrastructure. |
| Bot deployment | **0** | Will runs Fly.io servers | 3 | Shard-per-conversation on user devices. WebRTC peer-to-peer. Users run their own Jarvis. |
| Contract upgrades | **0** | Owner calls upgradeToAndCall | 4 | Timelock + governance vote + Shapley fairness gate. Eventually renounce upgrade authority. |
| Fee routing | **1** | FeeRouter controlled by owner | 4 | Governance-adjustable parameters, Shapley-gated changes, eventually immutable. |
| Insurance claims | **1** | Manual claim validation | 3 | On-chain proof of loss (oracle-attested), automatic payout, no human review. |
| Contributor registration | **2** | Authorized bridges can vouch on behalf | 4 | Self-sovereign vouching only. Remove addVouchOnBehalf. Trust is peer-to-peer or it's not trust. |

### The Disintermediation Roadmap (Priority Order)

**Phase 1: Remove Will as Single Point of Failure (Grade 0→2)**
1. Transfer ownership to multisig (Rodney, Freedom, Will = 2-of-3)
2. Add timelock on all admin functions (48hr minimum)
3. Remove owner from VIBEToken.mint() path
4. Make trust score recalculation permissionless
5. Deploy GovernanceGuard (Shapley veto on proposals)

**Phase 2: Make Intermediaries Optional (Grade 1→3)**
6. On-chain contribution tracking → auto-game creation in ShapleyDistributor
7. Multi-source oracle consensus (not single operator)
8. Self-sovereign vouching only in ContributionDAG
9. Insurance auto-payout via oracle proof
10. Fee router parameters governance-adjustable

**Phase 3: Make Intermediaries Structurally Impossible (Grade 2→4)**
11. Renounce upgrade authority on core contracts (VibeSwapCore, VibeAMM)
12. Immutable fee routing (or governance-only with Shapley veto)
13. Fully on-chain oracle (TWAP + multi-source, no off-chain operator needed)
14. Permissionless settlement (already done — anyone can call settleBatch)
15. Permissionless emission (EmissionController.drip() already permissionless)

**Phase 4: Pure Peer-to-Peer Where Possible (Grade 4→5)**
16. Direct atomic swaps for willing counterparties (skip batch auction)
17. Peer-to-peer Jarvis instances (user runs own shard)
18. Client-side oracle validation (don't trust server, verify yourself)
19. Local-first frontend (IPFS/Arweave hosted, no Vercel dependency)

### The Cincinnatus Test

For each interaction, ask: "If Will disappeared tomorrow, does this still work?"

- Grade 0-1: No. Will is required.
- Grade 2: Awkwardly. Someone has to step in.
- Grade 3: Yes, but suboptimally. Some functions degrade.
- Grade 4: Yes, fully. The protocol runs itself.
- Grade 5: The question doesn't even make sense. There's no role for Will to have vacated.

**The protocol is finished when the Cincinnatus Test passes for every interaction at Grade 4 or above.**

### Connection to P-001

P-001 (No Extraction Ever) is the enforcement mechanism for disintermediation:
- A middleman who adds no value = null player (Shapley axiom)
- A null player taking payment = extraction (P-001 detects it)
- System self-corrects = middleman's revenue goes to zero
- Middleman exits = interaction is now more peer-to-peer
- Grade increases automatically as extraction is eliminated

P-001 doesn't just detect unfairness — it economically starves intermediaries until they're gone. The disintermediation is emergent from the fairness enforcement.

### Origin

Will Glynn, Session 067, 2026-03-19:
> "I need a way to grade out peer to peer decentralization. Because if I figuratively imagine middlemen as satan getting in between people, it has to be identified and ERADICATED from reality."
> "Let's reach the endgame so I can walk the fuck away the second we go viral."
