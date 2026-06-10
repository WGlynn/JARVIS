---
name: hybrid-rep-nft-contribution-marker
description: Per-contribution soulbound NFT collapses 3 token functions into 1 — provenance record (IP marker without exclusivity) + reputation atom (monotonic) + revenue-share claim (dynamic Shapley). DAG node ≡ NFT. The on-chain instantiation of contribution-dag-replaces-ip.
type: primitive
originSessionId: 35d175e9-bf70-4d8f-b83a-b82bdd9d8fdf
---
## Claim

- ∀ validated contribution ⇒ mint soulbound NFT carrying 3 fn:
  - **Provenance** ≡ content-hash + timestamp + contributor-addr + linked-co-contributor-NFTs + parent-DAG-node ⇒ IP-marker w/o exclusivity
  - **Reputation atom** ≡ holding NFT = 1 unit rep; monotonic; never erodes
  - **Revenue-share claim** ≡ NFT → DAG node → current Shapley vector → periodic settlement slice
- Result: 1 token, 3 fn, indexable ∀ NFT-ecosystem tooling

## Why hybrid > separate tokens

- Previously: rep-token (monotonic) + rev-share-token (dynamic Shapley)
- Hybrid: both collapse into 1 soulbound NFT per contribution
- Architecture simpler ¬ more complex
- DAG node ≡ NFT ⇒ no translation layer; graph IS the NFTs
- Composable w/ NFT-ecosystem natively (wallets, marketplaces, indexers, DAOs)

## Prior art reference (load-bearing)

- **Hypercerts** (CoLab + Protocol Labs + Filecoin, 2023-2024)
- Fractionable NFTs representing "claims about impactful work"
- Scope + time period + contributors + beneficiaries + impact tags
- Deployed ∀ Gitcoin grants rounds + retroactive public-goods funding
- Differentiation: Hypercerts = coarse-grained (per-project / per-round); ours = per-contribution + Shapley-axiom-bound DAG + revenue flow
- Same direction, more granular, w/ math layer they don't have
- Positioning: ✓ prior-art exists (signals legitimacy), ✓ structurally distinct

## Connects to mutation-instability dissolution

- `[P·shapley-mutation-instability-dissolution]` 4-move stack still applies
- Move 4 (rep-token ⊥ rev-share-token) collapses into hybrid-NFT, doesn't break
- NFT count monotonic (have N, only grows)
- Revenue-share per NFT dynamic but converges in expectation
- Cleaner implementation, same structural guarantees

## Tradeoffs

- **Gas cost @ scale** ⇒ L2 deployment + lazy-mint pattern + batch-mints + ERC-1155 ∀ fungible-within-class
- **Wallet bloat** (N contribs = N NFTs) ⇒ aggregation views + per-cluster grouping
- **Mint authority** ⇒ attestation layer (who validates+mints?); dry-run: manual; platform: cluster-managers via fractal-DAG hierarchy
- **Legal IP status** ⇒ NFT = provenance + revenue-claim; actual IP rights governed by attached license. NFT replaces EXCLUSIVITY fn of IP w/ reputation+revenue-flow, ¬ licensing fn

## Dry-run pitch upgrade (Rick context)

- Pre-NFT dry-run: pick 3-5 USD8 contribs, compute Shapley, calibrate vs gut
- Hybrid-NFT dry-run: same + mint retroactive contribution NFTs to those 5 contributors
- Magic moment gets stronger: ¬ just spreadsheet numbers ✓ tangible artifact-per-task in their wallets w/ on-chain provenance + revenue-share entitlement
- Cost: low. Soulbound ERC-721 + small contract + cheap L2 (Base etc.). Same prototype budget.

## Clarification — USD8 is orthogonal, NOT collapsed into the NFT

- Rick's "USD8 or gov token" framing = under-resolved (named both pieces as alternatives)
- Truth: they are layers, ¬ alternatives
- **USD8** = settlement CURRENCY ⇒ when Shapley fires periodically, payout flows out in USD8
- **Gov-NFT** = persistent CLAIM ⇒ NFT entitles holder to slice of every future USD8 settlement
- USD8 flows THROUGH gov-NFTs. Two layers, connected.
- The NFT collapses 3 functions (provenance + rep-atom + revenue-share-claim), NOT USD8+gov-token
- ∀ Rick-prep: do NOT frame as "NFT collapses both" — frame as "NFT replaces three separate systems (IP registry + rep scoreboard + revenue-share contract); USD8 stays as the currency flowing through"
- Will-corrected 2026-05-14 06:23 ET after JARVIS muddled the mechanic in initial draft

## Connects

- `[P·contribution-dag-replaces-ip]` — this primitive is the on-chain token-layer instantiation of the parent claim
- `[P·shapley-mutation-instability-dissolution]` — mutation-stability properties survive the token-collapse
- `[P·fractalized-shapley-games]` — fractal DAG ≡ NFT-relationship-graph
- `[F·jul-is-primary-liquidity]` — 3-token role separation as design-pattern precedent
- `[P·airgap-problem-blockchain-vs-reality]` — NFT-as-provenance is the on-chain anchor for off-chain work attestation; airgap-bridging via attestation layer
- Hypercerts (external) — closest prior art; differentiate on granularity + math

## Origin

Will asked 2026-05-14 06:12 ET during Rick partner-prep: "could the rep token be hybrid nft as well so each contribution is its own IP marker as well?"

Answer: yes, and structurally stronger — collapses 3 token fn into 1, gives contributors tangible per-task artifacts, sharpens the dry-run pitch significantly. Prior art exists in Hypercerts; our differentiation is per-contribution granularity + Shapley-axiom-bound DAG + revenue-flow integration.

Captured as primitive because this is a load-bearing design choice for any Rick-platform implementation, and the hybrid-NFT shape will keep recurring across attribution conversations.
