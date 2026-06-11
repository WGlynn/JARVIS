---
name: blockownershipbitcoinshaped
description: "Per-block ownership + signing for the governance chain, Bitcoin-shaped (Will 2026-06-11 'only the producer can sign, anyone with rights to a block can, like bitcoin, starting with myself'). PROVEN: current owner = genesis folded over signed transfer log (UTXO-style); only current owner attests/transfers; transfer→old sig stale→new owner re-signs. Additive (append-only) ¬ replacement; value model → multiplicative next. Inputs→output provenance required per block."
metadata:
  node_type: memory
  type: project
  originSessionId: 8f988124-8197-4f80-8a59-217ae187c3ef
---

# Block ownership — Bitcoin-shaped, additive, multiplicative

> Will 2026-06-11: *"only the producer of the block can sign it, but anyone who gets the rights to a block can. just like bitcoin, starting with myself only."* + *"inputs for each block SHOULD be there to prove how the output came about."* + *"additivity over replacement... and multiplicativity over that."* Plan v2 CONFIRMED + PROVEN. `~/.claude/hooks/block-ownership.py`.

## ⊨ The model (PROVEN, not claimed)
- block = session-chain block (the unit a session PRODUCES) ¬ the file-merkle snapshot. "producer of the block" ⇒ chain.
- **ownership = genesis owner folded over a signed transfer log** (UTXO set = fold over tx history; ✗ giant 23k table).
- **only the current owner's key** can `attest` ∨ `transfer` a block (Bitcoin: control = key). non-owner attest ⇒ REFUSED.
- **transfer** = current owner SIGNS reassignment to a new pubkey ⇒ registry folds it ⇒ new owner is the valid signer. proven: Will→bob, then Will REFUSED, bob OK.
- **transfer voids prior attestation**: post-transfer verify ⇒ STALE ⇒ new owner must re-attest. (rights moved ⇒ old sig no longer authoritative.)
- "starting with myself only" = genesis `jarvis@local`; model already multi-owner + transferable, registry just points all at one key today.
- ADDITIVE module: does ✗ touch live chain-write path (chain.py / auto-checkpoint.py). standard primitives (Ed25519 ssh-keygen + sha256).

## ⊕ Will's two framings → existing primitives
- **additivity over replacement** ⇒ blocks APPEND-ONLY (Bitcoin ledger; ✗ mutate/replace history). ties [P·incremental-progressive-manifestation] · [F·augmentation-dont-replace] · [P·apply-the-rule-you-just-wrote]. the chain + transfer-log are both append-only by construction.
- **multiplicativity over additivity** ⇒ block VALUE compounds ¬ merely sums. ties [P·compounding-prompt-trajectory] · Shapley (multiplicative marginal value) · rarity×quality×freshness (multiplicative weight, [J·contribution-compact]). NEXT: a multiplicative value/credit model on owned blocks (¬ flat count).

## ◈ Inputs→output provenance (Will requirement)
- each block MUST carry the INPUTS that produced the output ⇒ derivation is provable/reproducible ("prove how the output came about").
- current chain block schema = {id, parent, timestamp, prompt, response, checkpoints, hash} ⇒ prompt(input) + parent(prior-state) + response(output) ALREADY present ⇒ basic provenance EXISTS.
- enhancement = capture FULL input context (loaded memory, tool-calls, model-id) ⇒ full reproducibility. + the per-block owner-signature now AUTHENTICATES the provenance (who produced it, unforgeable).

## 🔗 Composes
- [P·tamper-resistance-via-signed-attestation] (this = per-block extension of the signed-root resistance) · [P·off-chain-storage-onchain-commitment] · [P·cell-knowledge-architecture] (UTXO-for-knowledge — blocks-as-cells now have owners) · [P·open-weights-for-serious-sovereignty] (open-and-caged; blocks attributable to a producer)
- proven by demo ¬ claimed [F·no-bullshit-do-the-research]. TODO: multiplicative value model + full input-context capture.
