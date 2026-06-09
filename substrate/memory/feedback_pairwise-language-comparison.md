---
name: pairwise-language-comparison
description: ∀ language-choice decision (per architecture-piece / stack-layer / app / module) ⇒ run pairwise comparison BEFORE committing. ✗ default-language. Pairwise = CRPC discipline applied to language selection.
type: feedback
originSessionId: 2d5ae2e5-2926-42ce-a369-e66ee74c9c61
---
## Rule

∀ piece-of-architecture (contract, daemon, frontend, backend, library, script, doc-format, build-tool):
1. Enumerate ≥ 2 candidate languages whose substrate-geometry matches the piece
2. Pairwise compare on: substrate-fit · tooling-density · safety · perf · team-familiarity · ecosystem-lock-in
3. Choose winner per piece; ✗ inherit choice from adjacent piece without re-comparing
4. Document the comparison in-line at the decision point

## Why

Will-frame 2026-05-24: "pairwise comparison calculations to determine best language for each piece of architecture or stack or layer or app or anything really."

Default-language-bias = `[P·first-available-trap]` at the language layer. Solidity-everywhere / TypeScript-everywhere / Python-everywhere is the inverse-failure-mode of `[F·account-model-agnostic]` — at the language layer instead of the substrate layer.

CRPC primitive applied to language selection: same shape (pairwise compare → winner with receipts) at a different layer. Substrate-port-pattern at the implementation-language layer.

## How to apply

At every NEW architectural-piece decision-point:
1. State the piece + its purpose
2. List ≥ 2 candidate languages
3. Pairwise-table on the 6 axes above
4. Commit choice + receipts (inline comment, doc section, or commit message)

If reusing a piece's language for a sibling piece without re-comparing ⇒ violation. Adjacent piece may have different substrate-geometry-match.

## Examples

| Piece | Candidate A | Candidate B | Winner | Why |
|---|---|---|---|---|
| CKB type/lock scripts | Rust (RISC-V) | C (RISC-V) | Rust | substrate-native via ckb-std; safety + ecosystem |
| EVM contracts | Solidity | Vyper | Solidity | tooling density + Cycles 1-3 baseline |
| Frontend (vibeswap) | TypeScript | Rust+WASM | TypeScript | iterability + React ecosystem |
| Mesh attestation daemon | Python | Rust | Python (v1) | consistency with existing hook-stack (all Python); Rust v2 if perf demands |
| Standalone rosetta backend | Node+SQLite | Rust+SQLite | Node | already chosen, monorepo consistency |
| NCI consensus node | Rust (libp2p) | Go (CometBFT) | Rust | substrate-honest crypto + memory safety |
| Unhackability essay | Markdown | LaTeX | Markdown | consistent with docs/research/papers/ |
| ckb-testtool fixtures | Rust | n/a | Rust | only sane choice (test-tool is Rust) |

## Connects

- `[F·account-model-agnostic]` — sibling at substrate layer
- `[P·substrate-port-pattern]` — parent meta-principle (DIRECT-PORT / REINTERPRET / DROP)
- `[P·first-available-trap]` — failure-mode prevented (language-default)
- `[P·substrate-geometry-match]` — geometry of language ≡ geometry of substrate
- CRPC primitive (`PairwiseVerifier.sol`) — same pairwise-compare shape applied to consensus

## Origin

2026-05-24, mid-VibeSwap-arch-finishing arc. Will-named while reviewing the JARVIS-OS × OPH × CKB cell-model + EVM stack — observed that language choice had been inherited per-layer without per-piece comparison.
