---
name: CogProof Absorbed into VibeSwap
description: MIT Bitcoin Expo hackathon ended 2026-04-12, no win. CogProof IP fully absorbed into VibeSwap protocol stack. No separate branding.
type: project
originSessionId: fdbbd97a-2c43-4390-8937-2bb5d0e0092a
---
CogProof submitted to MIT Bitcoin Expo Hackathon 2026 (April 10-12). Did not win. As of 2026-04-13, all CogProof IP is absorbed into VibeSwap's protocol stack. No more separate branding or hackathon constraints.

**What CogProof was:** Behavioral reputation infrastructure for Bitcoin-native agent economies. JS/Node demo layer over VibeSwap's existing Solidity mechanisms.

**What gets absorbed:**
- 6 fraud detectors → `BehavioralReputationVerifier.sol` (already in `contracts/reputation/`)
- 9 credential types with weighted scoring → `CredentialRegistry.sol` (already in `contracts/reputation/`)
- Lawson floor (5% minimum Shapley guarantee) → folds into `ShapleyDistributor.sol`
- Compression mining → merges with CogCoin miner at `cogcoin-miner/`
- Bitcoin OP_RETURN mapping → CogCoin bridge layer

**What was always VibeSwap's:** commit-reveal engine, Shapley distributor, Fisher-Yates shuffle

**Code locations:**
- JS demo: `vibeswap/cogproof/` (hackathon artifact, no longer primary)
- Solidity: `vibeswap/contracts/reputation/` (production path)
- CogCoin miner: `cogcoin-miner/`
- Integration doc: `vibeswap/docs/COGPROOF_INTEGRATION.md`

**Why:** Hackathon ended, no external obligation to maintain separate branding. The reputation layer is native to VibeSwap now.

**How to apply:** Reference CogProof components as VibeSwap-native. Don't treat cogproof/ as a separate project. The JS layer was a demo — the Solidity contracts are the real implementation.
