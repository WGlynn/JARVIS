---
name: VibeswapCkbChainAlive
description: "2026-06-09 — vibeswap-ckb sovereign chain mines blocks locally. Genesis 0xd802dc43... on chain name vibeswap_ckb_dev (distinct from upstream dev). Architecture-review CRITICAL #3 (0-blocks-booted) resolved at the smoke-test level. Cells still pre-deploy; asm-VM path disabled (gcc-free shortcut)."
type: project
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[J·vibeswap-ckb-chain-alive]**

## ⚙ Fact

vibeswap-ckb sovereign chain boots, RPC-responds, P2P-listens, mines blocks at 5s cadence under our `chain-spec/vibeswap-ckb-dev.toml`. Receipt: `vibeswap/contracts-ckb/FIRST_BLOCK_RECEIPT.md`.

## Why

Architecture-review 2026-06-08 CRITICAL #3 = "0 blocks booted" — needed to be resolved before any further chain-build claims could carry weight. Resolved 2026-06-09 ~15:09 UTC.

## How to apply

- ∀ chain-build status question ⇒ point at FIRST_BLOCK_RECEIPT, not at the 26-cell scaffold count
- ∀ severity calibration ⇒ binaries-on-disk + local-dev-chain-mining ≡ "testnet-deployed" tier per [F·spec-vs-deployed-severity-calibration] (NOT mainnet, NOT cells-on-chain yet)
- ∀ next-step prioritization ⇒ OPERATIONS Day 2 = deploy ConstitutionalBoundsCell to consume the genesis-reserved capacity; this needs key custody + tx construction, not more cell scaffolding

## State details

| key | value |
|---|---|
| ckb binary | `vibeswap-ckb-fork/target/release/ckb.exe` (48MB) |
| ckb version | 0.206.0 (2c91814-dirty) |
| chain spec | `contracts-ckb/chain-spec/vibeswap-ckb-dev.toml` |
| chain name | `vibeswap_ckb_dev` |
| genesis hash | `0xd802dc439bf0fe7056e5a516857fbf309e13049a3be0956e2558ba1e3374f7e5` |
| data dir | `vibeswap/vibeswap-ckb-data/` |
| RPC | 127.0.0.1:8114 |
| P2P | 0.0.0.0:8115 + ws |
| block assembler | placeholder lock-arg 0xc8328aabcd9b9e8e64fbc566c4385c3bdeb219d7 |
| VM path | interpreter (asm path disabled at fork-level — no gcc on this host) |
| 26 cell binaries | compiled but NOT deployed on this chain |

## ✗ What is NOT proven

- vibeswap cells not deployed (capacity reserved, no consuming tx yet)
- canonical-token mint not exercised
- BLS attestation not exercised
- consensus = upstream NC-Max + Dummy PoW (dev mode); NCI is user-space and not yet active
- chain is single-node local; no validator set, no economic security

## 🔗 Composes-with

- [F·spec-vs-deployed-severity-calibration] — chain is now at "testnet-deployed" tier for the runtime; cells stay at "spec-only" until a tx deploys them
- [J·vibeswap-ckb-sovereign-pivot] — Position F (sovereign fork) confirmed buildable
- [F·ckb-cell-build-recipe] — sibling: how the 26 cell binaries compile
