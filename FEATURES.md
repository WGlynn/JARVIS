# JARVIS — the full feature surface (and the moat)

This document exists because the rest of the repo *undersells*. The README shows a
handful of hooks; the running system has 64 enforcement scripts. Below is the
honest, verified inventory — every number here was counted on the live system on
2026-06-11, not estimated. Where something is local-only or not yet
reader-verifiable, it says so.

## By the numbers (verified)

| Layer | Count | Note |
|---|---|---|
| Hook scripts | **42** | fire on `PreToolUse` / `PostToolUse` / `Stop` / `SessionStart` / `UserPromptSubmit` / `PreCompact` / `StopFailure` |
| Session-chain scripts | **22** | persistence + recovery machinery (separate from the hooks above) |
| Utility scripts | 6 | sync, attestation, audits |
| Slash-commands | 7 | `/JarvisOS`, `/autopilot`, `/anti-hallucination`, … |
| Cron self-perpetuation loops | 12 | substrate-sync, skill-mining, advice-mining, … |
| Curated memory files | **561** | 232 primitives · 204 feedback rules · 64 projects · 22 references · 16 user |
| Self-improvement infra (`_system/`) | **1,380 files** | incl. **1,263 evolution proposals** + 28 corpus tools |
| Session hash-chain | **23,462 blocks** | tamper-evident, one block per checkpoint |
| Governed files under Merkle attestation | **624** | hooks + primitives + session-chain scripts |

> So: **64 enforcement scripts**, not 6. That gap is the underselling, in one line.

## What's actually differentiating

Not every script is a moat. These are the ones with no mainstream-harness equivalent.

### 1. Crash recovery that survives the model dying
`session-chain/api-death-shield.py` fires on `StopFailure` and `PreCompact` —
i.e. **when the model API itself errors or the context is about to be
compacted away.** It persists session state client-side, with no LLM in the loop.
A wrapper that needs the model alive to checkpoint cannot do this; the provider
going down takes the session with it. JARVIS's hooks run *because the provider is
down*, not in spite of it. This is the cleanest proof the discipline layers are
substrate-independent.

### 2. A self-improving substrate, not a static prompt
The `_system/` directory is a continuous self-observation loop:
- corrections get mined into **`discipline_map`** patterns,
- patterns become **evolution proposals** (1,263 queued) awaiting a human vote,
- a **semantic index** powers `deep-recall` — semantic, not keyword: ask about
  "MEV" and it surfaces the airgap and extraction primitives that never say "MEV",
- **telemetry** (per-hook fire logs) tells the system which gates actually matter,
  so rules that earn their keep get promoted from memory into hooks.

A correction in this system doesn't evaporate at session end. It crystallizes
into the substrate. The per-session improvement curve compounds.

### 3. A 23,462-block session hash-chain + Merkle self-attestation
Every checkpoint is a block linked to its parent by hash. The chain is the agent's
tamper-evident long-term memory of its own history. Because it's a hash-chain, a
single **head hash commits all 23,462 blocks** — published as
[`substrate/_chain/commitment.json`](./substrate/_chain/commitment.json), so the
chain is verifiable without leaking a word of content (blocks stay local). On top,
a **Merkle root over 631 governed files** is checked at every boot: change a hook
or primitive outside the sanctioned flow and the next boot flags drift. "Provably
just files" — and provably *unaltered* files.

**Tamper-evidence → tamper-resistance.** The Merkle root is now **Ed25519-signed**
(standard `ssh-keygen` signatures, key held outside the governed tree, public key
published for anyone to verify). Evidence alone is defeatable — an attacker could
re-run the attestation to re-baseline a modified tree and silence the drift.
Signing the root makes re-baselining require a key they don't have, so the drift
becomes **un-silenceable**: a manifest re-attested without the key fails signature
verification at boot. Demonstrated, not asserted.

### 3b. Per-block ownership — Bitcoin-shaped
Each session-chain block can be **locked to an owner public key**: only the
current owner's key produces a valid block-attestation, and ownership is
**transferable** — the current owner signs a reassignment to a new key, exactly
like spending a UTXO. Current ownership is derived by folding a signed transfer
log over a genesis owner (the UTXO set as a fold over transaction history), so
there is no mutable ownership table to forge. Transferring a block voids the prior
owner's attestation; the new owner must re-sign. Today there is one owner (single
genesis key); the model already supports many. The chain is **append-only**
(additivity over replacement); a multiplicative, pairwise-elicited value model
over owned blocks is the next layer.

### 4. Operator-intent persistence (WWWD / Story Mode / autonomous-continue)
- **WWWD** gates consequential actions through a Will-emulation projection, and
  *learns from corrections* — when the human overrides it, the corpus reweights.
- **`autonomous-continue`** turns the default from "idle when done" to "pick up
  the pending work," so the system is proactive across session boundaries.
- **Story Mode** collapses steering to a single keystroke (predicted-reply menus; formerly "AFK mode")
  for low-bandwidth operation.

The system carries forward what the operator *meant*, across context limits and
provider failures — which requires the 561-file cross-referenced corpus + live
telemetry. That's not portable infrastructure; it's a personal substrate.

### 5. Filesystem-native by design
Markdown + git is the orchestration layer. The corpus is greppable, diffable,
version-controlled, cross-referenceable (`[[wikilink]]`-style), and importable as
typed Python objects via `pip install -e ./substrate`. No database, no daemon, no
black-box state store. Every other feature here depends on this choice.

## Exists on disk, not (yet) in this repo

Honest about the boundary:
- **Multi-provider Telegram bot** (`vibeswap/jarvis-bot/`) — escalation across
  providers with last-resort fallback, persona system, regression-locked
  behavioral rules. Real and running; the code is private.
- **Filesystem-native CRMs** (Desktop queues) — the most direct demonstration
  that specialized SaaS becomes redundant on an AI + filesystem substrate. Local.
- **The session-chain blocks** (23,462) — local by design (raw content); only the
  head-hash commitment is public.
- **~36 of the 42 hooks** are undocumented in the layer READMEs. A
  `verify/verify_hooks.py` that diffs documented-vs-present is the obvious next
  honesty artifact.

## The moat, in one paragraph

No single feature is the moat — the **composition** is. A substrate-independent
kernel whose gates fire even when the model is down; a filesystem-native corpus
that is greppable and diffable; a self-improvement loop that turns corrections
into permanent substrate changes; a tamper-evident hash-chain of the agent's own
history with public commitment; and Merkle self-attestation over the governed
body. You cannot retrofit this into an LLM wrapper, because it is not a wrapper —
it is *the substrate the LLM sits on top of*. Swap Claude for another model and
layers 1–4 do not change. That inversion — provider-as-substrate, not
provider-as-infrastructure — is the thing a competitor would have to rebuild from
the foundation up.
