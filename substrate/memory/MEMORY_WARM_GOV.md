# MEMORY_WARM — Governance, mechanism design, economic params
<!-- MEMORY-SPEC: v1 (2026-04-21) — see memory/MEMORY_FORMAT_SPEC.md -->

**Load trigger**: Governance decisions, mechanism-design params (bond sizes, challenge windows, slash splits, voting thresholds), token-architecture choices, anti-extraction axiom work.

## ⟳ɢᴏᴠ — Governance primitives
- [Cincinnatus / Disintermediation Grades](primitive_disintermediation-grades.md)
- [Augmented Governance](primitive_augmented-governance.md)
- [Anti-Hallucination Protocol](primitive_anti-hallucination-protocol.md)
- [Citation Hygiene Gate](primitive_citation-hygiene-gate.md)
- [Axiom Gate / P-001 Extraction Gate](feedback_p001-extraction-gate.md)
- [Mechanism Design Paper](feedback_augmented-mechanism-design-paper.md) — for bond sizes / challenge windows / slash splits / voting thresholds, read the augmented mechanism design paper first, don't ask Will for economic parameters

## Related — token/constitutional architecture
- [Consensus Constitution](primitive_consensus-constitution.md) — 3 tokens = separation of powers. Tinbergen's Rule. Lead with constitutional framing, not token count.
- [CKA / Cell Knowledge Architecture](primitive_cell-knowledge-architecture.md) — UTXO model for knowledge
- [GEV Resistance](primitive_gev-resistance.md) — MEV is a feature, GEV-resistance is the architecture
- [Extractive Load](primitive_extractive-load.md) — public-facing name for GEV

## Anti-extraction axioms
- [No Extraction Self-Correction / The Cost](primitive_no-extraction-self-correction.md)
- [Zero-Fee Principle Enforcement](feedback_zero-fee-principle-enforcement.md)

## Mechanism selection
- [First-Available Trap](primitive_first-available-trap.md) — threat-model first; ecosystem-default often isn't best-fit. Commit-reveal batch auctions vs Sidepit LO; Shamir vs multisig; what to compress vs preserve.
- [Substrate-Port Pattern](primitive_substrate-port-pattern.md) — per-component DIRECT-PORT / REINTERPRET / DROP ✓ classify ¬ all-or-nothing
- [Cooperative-Game Elicitation Stack](primitive_cooperative-game-elicitation-stack.md) — Shapley ⇒ how distribute, ¬ produce v. 4 layers. Pairwise-aug = Goodhart defense
- [Marketing as Mechanism Design](primitive_marketing-as-mechanism-design.md) — substrate-match + augmented-MD + augmented-gov ⇒ attention layer. 5 primitives mirror protocol-MD

## ⟳ ᴠɪʙᴇ→ᴜsᴅ8 — VibeSwap-portable contract primitives (2026-04-27 batch)
- [Off-chain storage + on-chain commitment](primitive_off-chain-storage-onchain-commitment.md) — bulk off-chain ⇒ ¬ ceiling; commit-only on-chain; parallel by shard
- [Circuit Breaker (attested resume)](primitive_circuit-breaker-attested-resume.md) — multi-level pause; cooldown=floor; resume needs attestation
- [TWAP depeg detector](primitive_TWAP-depeg-detector.md) — ring-buffer TWAP; spot-vs-TWAP deviation ⇒ trip breaker
- [VerifiedCompute (bonded dispute)](primitive_verified-compute-bonded-dispute.md) — off-chain compute + bond + dispute window ⇒ slash on lie
- [IssuerReputation (mean-reversion)](primitive_issuer-reputation-mean-reversion.md) — penalty-only counter; 30-day half-life recovery; ¬ founder dominance

## ⟳ ᴍᴇᴛʜᴏᴅ — Methodology / theory layer (2026-04-27 Batch 2 + 3a, glyph-KB conversion)
- [Augmented Mechanism Design (Methodology)](primitive_augmented-mechanism-design-methodology.md) — augment ¬ replace; 4 invariant types (Structural ∧ Economic ∧ Temporal ∧ Verification) composed 2-4 at a time; paper = parameter authority
- [Shapley 5-Axiom Set + Anti-MLM](primitive_shapley-5-axiom-set.md) — Shapley = unique fair distribution; 4 classical + Pairwise-Proportionality (5th, on-chain); event-based scoping; anti-MLM by Σ φ = v(N)
- [Composable Fairness (Arrow Inversion)](primitive_composable-fairness-arrow-inversion.md) — Arrow ⇒ voting impossibility; Glynn 2026 ⇒ mechanism-composition possibility; Shapley = unique composition rule preserving IIA
- [Fairness Fixed Point (Iterated Shapley)](primitive_fairness-fixed-point-iterated-shapley.md) — single-round fair ≠ iterated fair; existence ✓ Brouwer; uniqueness ✗ open; mitigations bound drift
- [Cooperative Markets (Mutualization Frame)](primitive_cooperative-markets-mutualization-frame.md) — multilevel selection theorem ⇒ cooperative design = evolutionarily stable; W_coop > W_extr always
- [Coordination Primitive (Infrastructure Frame)](primitive_coordination-primitive-as-infrastructure-frame.md) — VibeSwap = category like email/git/OAuth; uncontested + unstable; moat = attention-graph density compounding
- [Fibonacci Rate Limit (Scale-Invariant)](primitive_fibonacci-rate-limit-scale-invariance.md) — per-(user,pool) damping at 23.6/38.2/50/61.8% + cooldown = window × 1/φ; ¬ preferred timescale ⇒ attacker can't hide under threshold
- [Cincinnatus Walkaway Test](primitive_cincinnatus-walkaway-test.md) — founder-independence as design target; 7 preconditions + 30-day zero-intervention test + 6-phase Walkaway Sequence
- [Hobbesian Trap Dissolution (IIA)](primitive_hobbesian-trap-dissolution.md) — traditional defenses preserve the weapon; IIA REMOVES the weapon ⇒ defection becomes impossible, ¬ costly; phase transition


## Auto-enriched 2026-05-02

*Added in batch coverage pass — primitives/feedback/projects matching this domain.*

- [Dual Cap Monetary Architecture](primitive_dual-cap-monetary-architecture.md)
- [Crypto Primitive Selection](primitive_crypto-primitive-selection.md)
- [Ungovernance Time Bomb](primitive_ungovernance-time-bomb.md)
- [Tokenomics Zero Tolerance](feedback_tokenomics-zero-tolerance.md)
