---
name: tamperresistanceviasignedattestation
description: "Tamper-RESISTANCE for the governance substrate (2026-06-11, Will 'next step is tamper resistance, start with standard'). Merkle = tamper-EVIDENT; signing the root (Ed25519, ssh-keygen) = tamper-RESISTANT — drift becomes un-silenceable without the key. Standard primitive, no new deps. Key outside governed tree, never synced; verify needs only pubkey. Proven: keyless manifest edit → SIGNATURE INVALID."
metadata:
  node_type: memory
  type: primitive
  originSessionId: 8f988124-8197-4f80-8a59-217ae187c3ef
---

# Tamper-resistance = sign the attestation root (evidence → resistance)

> Will 2026-06-11: *"the merkle makes governance tamper evident, the next step is tamper resistance. start with standard."* Shipped in `~/.claude/hooks/integrity-attest.py`.

## ⊥ Evidence vs resistance (the load-bearing distinction)
- **merkle root alone = tamper-EVIDENT**: a changed file changes the root ⇒ boot detects drift. BUT an attacker can re-run `commit` to re-baseline the manifest ⇒ silences the drift. evidence ¬ resistance.
- **sign the root = tamper-RESISTANT**: `commit` now requires a key held OUTSIDE the governed tree ⇒ attacker can match the root but cannot produce a valid SIGNATURE ⇒ drift becomes un-silenceable without the secret.

## ⇒ Standard primitive (crypto = selection ¬ invention, [P·crypto-primitive-selection])
- claim shape = "these files are authentic/authorized" ⇒ DIGITAL SIGNATURE (¬ ZK, ¬ exotic). "start with standard."
- Ed25519 via `ssh-keygen -Y sign/verify`, namespace `jarvis-attest`. no new deps (OpenSSH present). py `cryptography`/`nacl` absent; gpg present (fallback).
- verify checks the manifest signature against the LIVE recomputed root ⇒ matching-the-root-without-resigning fails. proven: corrupt sig / keyless re-baseline ⇒ `⚠ SIGNATURE INVALID` @ verify ∧ boot.

## 🔑 Key discipline
- private key `~/.claude/keys/jarvis-attest` — OUTSIDE GOVERNED ∧ outside all sync sources (substrate-sync covers hooks/session-chain/scripts/memory/cron only) ⇒ NEVER leaves machine. confirmed.
- verify = PUBLIC key only ⇒ automated boot path touches NO secret. signing = manual/occasional sanctioned re-attest.
- pubkey + allowed_signers published to memory/_system/ ⇒ attestation externally verifiable (anyone recomputes root + checks sig).

## ⊖ Honest tiers (complete-as-ready-for-critique)
- **tier 1 (NOW)**: on-disk key, no passphrase. resists: remote/automated tampering, manifest/file edits without the key, accidental drift. does NOT resist a local-root attacker who reads the key + re-signs.
- **tier 2 (NEXT)**: passphrase + OS-keychain/TPM/YubiKey ⇒ key non-exfiltratable (hardware signs, never exports).
- **defense-in-depth**: anchor signed manifest to GitHub (substrate-sync already pushes) ⇒ even local key compromise DIVERGES from public signed history = detectable.

## 🔗 Composes
- [P·off-chain-storage-onchain-commitment] (files local, commitment public — now SIGNED) · [P·structure-does-the-work] · [P·honesty-as-structural-load-bearing-property]
- [P·open-weights-for-serious-sovereignty] (open-and-caged: this is the cage made unforgeable) · [P·substrate-anchoring-provably-just-files] (the resistance upgrade to "provably just files")
- [F·no-bullshit-do-the-research] — proven by tamper-sim, ¬ claimed.
