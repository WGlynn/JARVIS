---
name: Off-chain storage + on-chain commitment
description: Bulk storage off-chain (linear scaling, parallel by shard); on-chain only succinct commitment per snapshot. ¬ on-chain ceiling.
type: primitive
originSessionId: 05f950b5-8ab9-47f5-a2b2-b8336ce1e9ef
---
# Off-chain storage + on-chain commitment

## Rule
- bulk storage ⇒ off-chain (no on-chain ceiling)
- on-chain ⇒ commitment-only (succinct root per snapshot)
- ⇒ scales linearly w/ off-chain compute + storage
- ⇒ parallelizes trivially by shard

## When ✓
- append-only events
- per-actor partitioned (independent reconstruction)
- read-rare ∧ write-continuous
- Walkaway-Test required (events on-chain as logs ⇒ reconstructible)

## When ✗
- on-chain query needed for aggregate state (rare)
- single source of truth must be on-chain (extreme cases)

## Architecture
| layer | location | scaling |
|---|---|---|
| event emission | on-chain (`LOG4` per event, ~2k gas) | O(1) per write |
| bulk storage | off-chain indexer (sharded by actor) | linear, parallel |
| commitment | on-chain (sparse Merkle root per snapshot, ~50k gas/snapshot) | O(1) per snapshot |
| witness path | off-chain (served by indexer) | O(log actors) |
| verification | on-chain (zk-proof against committed root) | constant-time |

## Sharding
- by actor address-prefix ⇒ each shard self-contained
- ¬ coordination during reads
- new shards subscribe to same chain log ⇒ horizontal scaling
- shard fault ⇒ re-spin from chain log

## Walkaway Test
- events ⇒ on-chain log ⇒ canonical source
- indexer = derived (not authoritative)
- ⇒ team disappears ⇒ anyone re-indexes ⇒ system functions

## Anti-pattern (the wrong recommendation we just corrected)
- ✗ "fixed-depth on-chain Merkle tree storing raw events"
- ⇒ depth-20 caps at 1M events
- ⇒ depth choice permanent at deployment
- ⇒ requires redeployment to scale past ceiling
- ⇒ wrong shape for multi-decade protocol horizon

## Why we got it wrong first time
- Walkaway-Test concern misplaced: assumed off-chain storage would orphan history
- ⇒ but events on-chain as logs ARE the reconstructible source
- ⇒ off-chain storage is derived; chain log is canonical
- corrected 2026-04-27 in `vibeswap/docs/usd8/history-compression-spec.md`

## USD8 application
- USD8 token `_afterTokenTransfer` ⇒ emits `BalanceChange` event
- multiple indexers ingest, shard by holder address-prefix
- daily snapshot: snapshotter posts sparse-Merkle root (computed off-chain) on-chain
- Brevis circuit: per-holder score proof against snapshot root
- ⇒ no on-chain ceiling; linear off-chain scaling; parallel by holder

## Triggers
- "how do we store user history at scale?"
- "what's the on-chain footprint?"
- "scaling concern" + "long-term protocol"
- pre-deployment design review for any per-actor accumulation

## Related
- substrate-geometry-match (off-chain matches the substrate's natural shape)
- IncrementalMerkleTree (correct role = commit-of-commits, ¬ raw event storage)
- Brevis ZK coprocessor (the natural verification layer)
- substrate-port-pattern (REINTERPRET: VibeSwap on-chain pattern → USD8 off-chain pattern)

## Source
- corrected 2026-04-27 history-compression-spec ⇒ Will's directive: "scale linearly parallelize off-chain"
- pattern is standard in modern zk-coprocessor systems (Brevis, Axiom, Lagrange)
- ¬ novel ⇒ well-trodden path; we're recommending what works
