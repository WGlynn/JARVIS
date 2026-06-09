---
name: Superlinear Scaling via Content-Addressed Contribution
description: Architect systems so each new adopter contributes more capacity than they consume. Work product is content-addressed and shareable. Cache hit rate rises with N — latency drops superlinearly because popular items cluster.
type: primitive
originSessionId: 58b19964-c316-4603-98a4-1ffe4fe4f29d
---
**Rule:** the performance of a system should *improve* with adoption, not degrade. Every adopter's locally-computed artifact (hash, translation, render, proof, cached page, compile output) should be content-addressable and shareable. Cache hit rate compounds with N; for popular items, latency drops superlinearly because top-K dominate lookup load.

**Why:** conventional systems scale linearly-or-worse with users — more users means more database load, more CPU, more bandwidth per origin. Inverting this requires each user to become a *contributor* to shared capacity, not just a consumer. This is the same architectural move NC-Max made at the consensus level (transactions pre-disseminated across the network so blocks commit faster), that BitTorrent made at the transport level (more peers = more upload = faster downloads), and that IPFS/libp2p make at the content layer (content-addressed lookups resolve from the nearest holder). Every adopter is an edge cache.

**How to apply:**

1. **Make work product content-addressable.** Keys are hashes of the content, not UUIDs or human names. Two clients that compute the same artifact produce the same key automatically; de-duplication is free.
2. **Local cache, then peer cache, then compute.** On any lookup: check local IndexedDB / OPFS / LMDB, then ask peers via a gossip or DHT layer, only fall back to the origin if both miss.
3. **Announce by intent, not by identity.** A client that holds artifact `hash=abc...` announces `(hash → available-at-me)` over the federation channel. Peers query by hash, not by author.
4. **Instrument cache hit rate.** Track local-hit / peer-hit / miss ratios. The ratio is the health metric: as adoption grows, hit rate should climb to an asymptote. If it doesn't, the addressing scheme is wrong — artifacts aren't actually shareable.
5. **Resist identity-anchored caching.** "User X's cells" is the wrong partition; it fragments the cache by author. The right partition is by content-hash or by topic-hash.
6. **Design for the federation hook from day one, even if it's a no-op.** A schema that keys by UUID is hard to federate later. A schema that keys by hash is federation-ready before the transport exists. The cost of designing for it up front is near-zero; the cost of retrofitting is prohibitive.

**Critical invariants:**
- **Idempotent writes.** Putting the same `(hash, content)` twice must be safe. Without this, federation has a split-brain problem.
- **Deterministic hashing.** Same input → same hash, across clients, platforms, versions. Canonicalize before hashing (sort keys, normalize whitespace, UTC dates).
- **No per-client secrets in the addressable artifact.** Anything identity-specific must live outside the content-addressed store, or the cache degrades to per-client.

**Applied instances:**
- Lineage IDE plugin: worker's IndexedDB stores cells keyed on draft ID + SHA-256 hash. `peerAnnounce` handler stub documents the federation hook — replace with a real transport (WebSocket, libp2p, nostr, WebRTC) and the plugin becomes a p2p edge cache. (`Desktop/lineage-ide-plugin-minimal/src/lineage-worker.ts`.)

**Analogies (and what they share):**
- BitTorrent — more peers = more upload capacity.
- NC-Max — transactions pre-disseminated before block commit.
- BitTorrent's rarest-first also maps: federate the *least-available* artifacts preferentially.
- IPFS / libp2p — content addressing as the substrate.
- CDN — same idea with centralized edge control instead of p2p.
- Folding@home / SETI@home — contribution of idle compute, not cache, but the same inversion of "more users = more capacity."

**Anti-patterns:**
- Identity-keyed caches. `(user_id, resource)` as a lookup key locks each artifact to one owner even when the content is identical.
- Origin-only architecture with horizontal scaling as the only lever. Adds cost per user, does not invert.
- Caches that never announce. If an edge holds an artifact nobody can discover, it might as well not exist.
- Hashing with non-deterministic inputs (timestamps, random salts, dict insertion order).

**Related primitives:**
- [NC-Max Bottleneck Breaking](primitive_nc-max-bottleneck-breaking.md) — the methodology that applied to consensus produced two-step confirmation; applied to UI produced speculative execution; applied to network produces this primitive.
- [Speculative Execution Over Idle Gaps](primitive_speculative-execution-idle.md) — the local-client version of the same inversion: do the work before it's needed.
- [Optimistic UI / Durability Split](primitive_optimistic-ui-durability-split.md) — the UI-layer cousin; federation lives in the same layer as durability.

**Standing instruction:** when a new project asks "how will this scale?", the first answer to try is "each new user makes it faster." If that answer is architecturally foreclosed by the initial design, revise the design before writing more code. Hash-addressable artifacts, local-first storage, and a federation hook (even a no-op one) are the three seeds.
