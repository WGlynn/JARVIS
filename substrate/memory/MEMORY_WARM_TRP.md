# MEMORY_WARM — TRP & Integration primitives (VibeSwap Solidity)
<!-- MEMORY-SPEC: v1 (2026-04-21) — see memory/MEMORY_FORMAT_SPEC.md -->

**Load trigger**: Touching VibeSwap contracts (CommitRevealAuction, VibeAMM, VibeSwapCore, NCI, ShardOperatorRegistry, ShapleyDistributor, CrossChainRouter), TRP audit round, or integration with external contracts (LayerZero, oracles).

## ⟳ᴛʀᴘ — TRP-Solidity primitives (VibeSwap-specific)
- [Deposit Identity Propagation](primitive_deposit-identity-propagation.md)
- [Settlement-Time Binding](primitive_settlement-time-binding.md)
- [Rate-of-Change Guards](primitive_rate-of-change-guards.md)
- [Collateral Path Independence](primitive_collateral-path-independence.md)
- [Batch Invariant Verification](primitive_batch-invariant-verification.md)
- [Discovery Ceiling](primitive_discovery-ceiling.md)
- [Off-Circulation Registry](primitive_off-circulation-registry.md)
- [Rebase-Invariant Accounting](primitive_rebase-invariant-accounting.md) — quantity gates on rebasing tokens must anchor in internal units
- [Post-Upgrade Init Gate](primitive_post-upgrade-initialization-gate.md) — new storage slots need reinitializer(N) packaged with upgradeToAndCall

## ⟳ɪɴᴛ — Integration primitives (external contracts, liveness)
- [Identity Divergence](primitive_identity-divergence.md)
- [Dead Guard Antipattern](primitive_dead-guard-antipattern.md)
- [Liveness Coupling](primitive_liveness-coupling.md)
- [Graceful Distribution Fallback](primitive_graceful-distribution-fallback.md)
- [Unbonding Slash Completeness](primitive_unbonding-slash-completeness.md)
- [Enforced Liveness Signal](primitive_enforced-liveness-signal.md) — heartbeat constants without gates/eviction are theater
- [Merkle Commit-Dispute-Finalize](primitive_merkle-dispute-window.md) — self-reported metrics feeding rewards need commit + challenge window
- [Settlement State Durability](primitive_settlement-state-durability.md) — async silent-catch needs durable flag + permissionless retry + downstream counter gate (C15+C20)
- [Phantom Array Antipattern](primitive_phantom-array-antipattern.md) — append-only arrays with flag-based deactivation brick loops; require swap-and-pop + cap (C24)

## Related TRP process
- [TRP Round Summaries](feedback_trp-round-summaries.md)
- [TRP Agent Concurrency Cap](feedback_trp-agent-concurrency.md) — max 2 concurrent opus subagents
- [Stack-too-deep](feedback_forge-stack-too-deep.md)
- [Targeted Test Triage](feedback_targeted-test-triage.md)
- [Lighter Test Generation](feedback_lighter-test-generation.md)


## Auto-enriched 2026-05-02

*Added in batch coverage pass — primitives/feedback/projects matching this domain.*

- [Twap Depeg Detector](primitive_TWAP-depeg-detector.md)
- [Admin Event Observability](primitive_admin-event-observability.md)
- [Atomized Shapley](primitive_atomized-shapley.md)
- [Dissolve Attack Surface](primitive_dissolve-attack-surface.md)
- [L2 L1 Commitment Protocol](primitive_l2-l1-commitment-protocol.md)
- [Signed Intent Binds Security Property](primitive_signed-intent-binds-security-property.md)
- [Constitutional Pipeline Scaffolding](primitive_constitutional-pipeline-scaffolding.md)
- [Ultimate Invariant At Axiom Level](primitive_ultimate-invariant-at-axiom-level.md)
- [Trp Session Cap](feedback_trp-session-cap.md)
- [Account Model Agnostic](feedback_account-model-agnostic.md)
- [Anti Stale Feed Protocol](feedback_anti-stale-feed-protocol.md)
