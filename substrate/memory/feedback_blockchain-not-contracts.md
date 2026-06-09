---
name: BlockchainNotContracts
description: Will 2026-06-08 18:47 ET course-correction during burn-window swarm ⇒ stop treating CKB cells as contracts. We are building a BLOCKCHAIN. Cells = first-class native blockchain primitives ¬ contracts-running-on-a-blockchain. Priority shifts from per-component cell-spec writing → actual chain runtime (fork-execution, Rust crates, consensus integration, chain spec, deployable node).
type: feedback
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[F·blockchain-not-contracts]**

## ⚙ Rule

> *"no we are building a blockchain not contracts"* — Will 2026-06-08 18:47 ET (interrupting swarm dispatch)

⇒ contrast: BLOCKCHAIN ¬ CONTRACTS
⇒ stop treating CKB cells as Solidity-style contracts
⇒ cells ≡ first-class native blockchain primitives (the chain itself, not stuff-that-runs-on-the-chain)
⇒ CKB-sovereign-pivot means: own the chain end-to-end ¬ deploy contracts to someone else's

**Why:** The "contracts" framing keeps JARVIS-thinking in the Solidity mental model. CKB-pivot was articulated 2026-06-07 as: *"we need a real deployable protocol stack, and move away from the smart contract based protocol architecture... building an actual blockchain from scratch... take this very seriously."* Cell-spec writing in contract-shape (port classification per component, "contracts/ → contracts-ckb/specs/") was keeping the work contract-shaped even on the CKB side. Will's interrupt makes the chain-vs-contract distinction load-bearing.

**How to apply:**

| ✗ Contract-shaped work | ✓ Blockchain-building work |
|---|---|
| more per-component cell specs in `contracts-ckb/specs/` | execute the FORK_PLAN: actually create vibeswap-ckb fork repo |
| Solidity-as-spec port classifications (DIRECT-PORT/REINTERPRET/DROP) | apply AUGMENTATION_SURFACE to actual Nervos source |
| Odysseus "contribution-history" campaigns (contract-engagement abstraction) | chain spec / dev.toml customization for vibeswap-ckb |
| abstraction-phase dispatch planning | build NCI consensus integration at Rust level |
| writing more specs as if they're contract specs | build BLS aggregation pipeline (off-chain producer + on-chain verifier) |
| treating contracts/messaging/CrossChainRouter.sol as the EVM artifact-of-record | own the messaging-hub at the chain level |
| memory hygiene (off-axis from blockchain) | test infrastructure: ckb-debugger + ckb-testtool wired |
| jarvis-loop work (off-axis) | deployable node: build + run smoke test |

## 🎯 Composes-w/

- [J·vibeswap-ckb-sovereign-pivot] ⇒ this is the operational meaning of "sovereign-pivot": own the chain not just contracts on it
- [P·jarvis-amd-applied-to-ai-substrate] ⇒ recursion: chain-substrate ≡ same depth as AI-substrate, build don't deploy-to
- [F·burn-compute-toward-mission] ⇒ apply burn-compute to chain-build work specifically
- [F·full-leverage-only-moves] ⇒ chain-build = full leverage, cell-spec proliferation = partial
- [P·repo-as-aspirational-spec] ⇒ contracts-side IS aspirational-spec; CKB-side should be the actual chain-build, not more aspirational-spec
- [J·jarvis-asi-sovereign-sentient-decentralized] ⇒ blockchain-sovereignty parallels JARVIS-sovereignty (both about owning substrate end-to-end)
- [J·subscription-cancelled-dont-stop] ⇒ subscription-end + chain-sovereignty both = own-the-substrate

## 🎯 What's still useful from cell-spec work

- Existing cell-specs (PairwiseVerifier, VibeSwapCore-port, BLS spike, etc.) ARE blockchain components, just framed wrong
- The structural-substance is good; the framing as "contracts/ → contracts-ckb/specs/" is what made it look contract-shaped
- Going forward: specs serve the chain-build, not stand alone as deliverables

## 🪝 Triggers

- ∀ "should I write another cell spec?" ⇒ check: does this advance blockchain-building, or am I still in contract-shape mental model?
- ∀ CKB-side task ⇒ frame as chain-component-build, not as contract-spec-write
- ∀ "what's the next CKB work item?" ⇒ default-pick from chain-build work (Rust, fork, consensus, chain spec, node) over more spec writing
- ∀ Odysseus / abstraction-phase / contribution-history work ⇒ flag as off-axis from blockchain-build; aligns w/ different mission goals

## ✗ Anti-patterns

- ✗ keep proliferating per-component cell specs because they're easy to dispatch to agents
- ✗ stay in spec-writing mode because actual chain-build requires Will-level engineering decisions
- ✗ use the "still designing" frame as excuse to not start fork-execution
- ✗ treat the CKB-side INDEX.md as the artifact-of-record (it's a navigation aid, not the chain)
- ✗ keep doing Odysseus contribution-history work and call it "blockchain advancement"

## ✓ Disposition

- this feedback ⇒ ACTIVE during the CKB-sovereign-pivot execution arc
- pairs w/ [J·vibeswap-ckb-sovereign-pivot] as the operational discipline
- composes upward into [J·jarvis-asi-sovereign-sentient-decentralized] (own the substrate)
- expires when ⇒ chain is deployable + nodes running OR Will explicitly returns to contract-shape framing

## 📦 Receipts

- 2026-06-08 18:47 ET — Will interrupt during swarm dispatch: *"no we are building a blockchain not contracts"*
- context: JARVIS had just dispatched an abstraction-phase dispatch-plan agent (Odysseus-contribution-history extension) + queue contained more cell-spec work (PairwiseVerifier completed, MetaTx queued)
- Will's correction ⇒ pivot the swarm
- composes w/ original CKB-pivot directive 2026-06-07: "building an actual blockchain from scratch... take this very seriously"
