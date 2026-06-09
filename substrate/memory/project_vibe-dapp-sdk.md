---
name: Vibe Dapp SDK
description: Developer SDK exposing VibeSwap's primitives, design patterns, and tools so external builders can compose Vibe Dapps on top of the architecture
type: project
originSessionId: ea7bb041-d517-4709-a8f7-c9ce32d566fa
---
# Vibe Dapp SDK

## Ask (2026-04-16, Will)

Build an SDK so developers can build Vibe Dapps based on the inherent primitives and design patterns VibeSwap uses. Force multiplier for ecosystem growth — external builders should be able to compose commit-reveal batch auctions, fractalized Shapley attribution, peer challenge-response oracles, off-circulation registries, stake-bonded pseudonyms, etc. without reinventing each one.

## Why:
- VibeSwap has 50+ extracted primitives already indexed in `memory/primitive_*.md` and in the Full Stack RSI backlog. They're reusable, battle-tested (7 RSI cycles on the core contracts), and documented.
- External builders shipping Dapps on these primitives = (a) ecosystem growth, (b) more Shapley-DAG contributors, (c) validates "these patterns are general, not VibeSwap-specific."
- Natural composability with the Contribution Compact: SDK adoption = trackable usage = Shapley attribution for primitive authors (both Will and future contributors).

## How to apply:
- **Not V1 scope.** Logged as a backlog item; pick up after Signal Desk V1 ships and C12 (evidence-bundle hardening) lands.
- Candidate structure: `vibe-sdk/` monorepo with subpackages per primitive layer (`@vibe/auctions`, `@vibe/shapley`, `@vibe/oracle`, `@vibe/identity`, `@vibe/state`).
- TypeScript + Solidity libraries. Each primitive ships with: interface, reference implementation, test suite, design doc, attribution metadata.
- Contribution DAG integration: when a dapp uses a primitive, emit an on-chain event crediting the primitive author. Shapley flows compound from there.

## Linked artifacts:
- `memory/primitive_*.md` — the source material (50+ primitives)
- `docs/papers/atomized-shapley.md` — attribution mechanism
- `DOCUMENTATION/THE_CONTRIBUTION_COMPACT.md` — the compensation framework SDK adoption would operationalize
- `docs/trp/TRP_RUNNER.md` — the audit methodology the SDK should inherit
