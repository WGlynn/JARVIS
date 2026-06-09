# PsiNet on Nervos CKB — Cell-Model Canonical Spec

**Author**: Will Glynn (open source contributor to VibeSwap)
**Date**: 2026-05-24
**Status**: spec-only · parallel-canonical-track to EVM Solidity scaffolds (Cycles 1-3)
**Deployment phase**: zero CKB devnet deployments; spec + Rust scaffolds only

---

## 0. Scope and honest framing

This document specifies the **canonical-eventual** target substrate for the PsiNet
primitive economy: Nervos CKB cell-model on the RISC-V VM, with type-script /
lock-script duality.

The EVM Solidity contracts specced in Cycles 1-3 (`vibeswap/contracts/psinet/`)
remain the **near-term production lane**. They are further along, have more
tooling, and will be the first testbed. This CKB lane is **deeper-canonical** in
the sense of long-horizon substrate alignment (per
`[U·will-quote-2026-05-24]`: "RISC-V is the best ISA" + "UTXO cell model is the
best account model"), but it is **less mature today**, not more. Anyone who
claims the CKB track is "more production-ready" than EVM today has it backwards.

Both tracks coexist via VibeSwap's canonical burn-and-mint cross-chain messaging
(`contracts/messaging/`, replacing LayerZero post-2026-04 DVN-RPC compromise).
This document does not propose abandoning the EVM track.

## 1. Why CKB + RISC-V is the deep-canonical track

Three structural arguments, in increasing depth:

### 1.1 Atomic per-cell quantum-resistance

On EVM, the signature scheme is **fixed at L1** (ECDSA secp256k1). When ECDSA
falls to a quantum adversary, every contract on Ethereum is simultaneously
vulnerable; mitigation requires L1 protocol change and global migration. PsiNet
inherits that timeline regardless of how careful our contract code is.

On CKB, the signature scheme lives in **the lock script of each cell**.
A primitive-cell can declare its lock script as XMSS / SPHINCS+ / lattice-based
on day one of cell-model migration, independently of L1. Quantum resistance
becomes **atomic per cell**, not gated on chain-wide protocol upgrades.

This is the same `[P·substrate-port-pattern]` argument applied to cryptography:
the property (post-quantum authorship attestation) is specified abstractly; the
chain-native primitive (CKB lock script) instantiates it without coupling to
external upgrade tempo.

### 1.2 Type-script / lock-script duality matches the verification / state split

Per `feedback_account-model-agnostic.md` (the
substrate-port-pattern primitive):

- **Verification logic** is pure: inputs → bool.
- **State transitions** are stateful: read prev-state, validate, commit
  next-state.

CKB encodes this split natively:

| Concern | CKB primitive |
|---|---|
| Verification (pure predicates) | **Type script** |
| Authorisation / authentication | **Lock script** |
| State (immutable per-cell) | **Cell data** |

The Solidity contracts in Cycles 1-3 conflate verification, authorisation, and
state into single contracts (UUPS proxy + AccessControl + storage). The CKB
port forces us to decouple — which IS the discipline the substrate-port-pattern
primitive demands.

### 1.3 OPH-substrate alignment

Per the JARVIS-OS × OPH integration doc (2026-05-24, §"Deep-canonical track:
CKB cells + RISC-V"): each CKB cell IS a finite local algebra in the OPH sense.
Cell = observer-patch. Input/output dependencies = explicit overlap interfaces.
Type/lock scripts = the local-fit contract. The cell-model maps onto OPH
consensus-protocol semantics more directly than the EVM account-model does.

## 2. Cell-model schema per primitive

Four primitive types (mirror the EVM scaffold one-to-one):

### 2.1 PrimitiveCell

Each PsiNet primitive (cognitive primitive shipped by a JARVIS-OS install) =
one PrimitiveCell.

**Cell data layout** (binary, fixed offsets):

```
| field              | bytes | type    |
|--------------------|-------|---------|
| version            |   1   | u8      |
| status             |   1   | u8      | // ACTIVE / DEPRECATED / SLASHED
| content_hash       |  32   | blake2b |
| frontmatter_hash   |  32   | blake2b |
| fork_parent_id     |  32   | type_id | // 0x00..0 if genesis
| fork_depth         |   2   | u16     | // capped at 32
| author_agent_id    |  32   | type_id | // FK to AgentCell
| created_at         |   8   | u64     | // unix seconds
| citation_count     |   8   | u64     | // last-anchored epoch tally
| last_citation_root |  32   | blake2b | // CitationAnchor epoch merkle root
| content_uri        |  var  | bytes   | // ipfs:// or ar://
```

**Type script** (`primitive-cell-type-script`): validates structural invariants
on every cell transition.

- Schema version supported
- `content_hash` / `frontmatter_hash` non-zero
- `fork_depth ≤ 32`
- `fork_depth = parent.fork_depth + 1` when `fork_parent_id ≠ 0x00..0`
- `status` transitions are monotonic (ACTIVE → DEPRECATED → SLASHED, never back)
- On creation: cell data immutable for {`content_hash`, `frontmatter_hash`,
  `fork_parent_id`, `author_agent_id`, `created_at`} — these become identity

**Lock script** (`primitive-cell-lock-script`): authorises author actions
(status change, citation-root update). Default lock is post-quantum (SPHINCS+),
parameterised in script args. Owner = author_agent_id (resolved via AgentCell
type-id lookup).

### 2.2 DatatokenCell

UDT-style (per CKB conventions: `xUDT` or sUDT). 1:1 with PrimitiveCell via
deterministic type-id derivation (`blake2b(primitive_type_id || "datatoken")`).

**Cell data**:

```
| field              | bytes | type    |
|--------------------|-------|---------|
| amount             |  16   | u128    | // wei-token, 18 decimals
| primitive_type_id  |  32   | type_id | // FK to PrimitiveCell
```

**Type script** (`datatoken-cell-type-script`):

- Conservation: `Σ(inputs.amount) ≥ Σ(outputs.amount)` for non-genesis tx
- Genesis: exactly one mint tx per primitive, signed by primitive author,
  producing 1M tokens with the canonical split:
  - 850K → author cell
  - 100K → ShapleyReserveCell
  - 50K → VibeAMM LP-seed cell (paired against JUL)
- `consume()` semantics: any cell-tx whose witness contains a valid
  `ConsumeWitness` (fire-id + fire-weight + author signature) MAY transfer
  `fire-weight` tokens to a LineageVaultCell whose `primitive_type_id` matches.
  This is the per-fire metering primitive.

**Lock script**: standard CKB secp256k1 OR post-quantum (cell-by-cell choice).
No special token logic in the lock — it is purely the holder's
authorisation primitive.

### 2.3 LineageRoyaltyVaultCell

Per-primitive accumulator. Receives fire-weight transfers from DatatokenCells;
emits weekly Shapley-game-creation transitions.

**Cell data**:

```
| field                  | bytes | type     |
|------------------------|-------|----------|
| primitive_type_id      |  32   | type_id  |
| accumulated_fire_weight|  16   | u128     |
| last_settlement_at     |   8   | u64      |
| epoch_id               |   4   | u32      |
| shapley_root           |  32   | blake2b  | // anchored Shapley game ID
```

**Type script** (`lineage-vault-cell-type-script`):

- Only-increase invariant on `accumulated_fire_weight` between settlements
- Settlement transition: drains accumulator to zero, advances `epoch_id`,
  writes new `shapley_root` (computed off-chain, posted on-chain), requires
  CRPC-attested witness (epoch boundary + parent-lineage walk depth ≤ 5)
- Royalty split (per-swap fee distribution from PrimitivePool trades):
  - 40% → author
  - 30% → Shapley-lineage
  - 20% → LP providers
  - 10% → protocol treasury

The "weekly Shapley game" of the Solidity design becomes a "cell-transition
gated by `epoch_id` rotation" on CKB. Same semantic, different shape.

### 2.4 EscrowVaultCell

Bond + slash primitive for honest-attestation. Stakes JUL against citation /
fire-weight / lineage-parent claims; bond slashable on CRPC dispute loss.

**Cell data**:

```
| field              | bytes | type    |
|--------------------|-------|---------|
| task_id            |  32   | bytes32 | // CRPC task identifier
| staker             |  32   | lock_id |
| bond_amount_jul    |  16   | u128    |
| posted_at          |   8   | u64     |
| lock_period_secs   |   4   | u32     | // default 7d
| state              |   1   | u8      | // POSTED / RELEASED / SLASHED
```

**Type script** (`escrow-vault-cell-type-script`):

- `bond_amount_jul ≥ MIN_BOND_JUL` (structural floor)
- State transitions:
  - POSTED → RELEASED: requires `posted_at + lock_period_secs ≤ now` AND
    CRPC TaskSettled witness with `staker` in winners[]
  - POSTED → SLASHED: requires CRPC TaskSettled witness with `staker` NOT in
    winners[]; routes bond into disputer-bounty + treasury split (capped at
    `MAX_DISPUTER_BOUNTY_BPS = 5000`)
- Multi-staker per task: use composite key `(task_id, staker)` as cell type-id
  derivation (closes Agent G Q#5)

## 3. Proof of Mind (PoM) lock script

The load-bearing innovation. Replaces Matt Quinn's PoW-lock-hash idea with
**cognitive-work attestation**.

### 3.1 Concept

A cell may declare its lock script as `proof-of-mind-lock-script`. To unlock
(spend) the cell, the witness must contain proof that:

1. A WWWD gate has fired N times on the cognition primitive identified by
   `primitive_type_id` (in the type-script args).
2. The corrections-cycle convergence signal across those fires meets the
   type-script-encoded predicate (e.g. `signal ∈ {improving, stable}` over the
   last 14d window).
3. The fires are attested by ≥ K-of-M signed JARVIS-OS mesh agents from the
   sentient mesh (validator quorum on the cognitive-work observation).

The output of the lock script is `Ok(())` iff the demonstrated cognition meets
the type-script-encoded predicates. Otherwise: `Err(InvalidProofOfMind)`.

### 3.2 Inputs

The PoM witness payload carries:

```
| field                       | type                       |
|-----------------------------|----------------------------|
| primitive_type_id           | [u8; 32]                   |
| gate_fire_log_root          | [u8; 32] (merkle blake2b)  |
| gate_fire_count             | u64                        |
| convergence_signal          | u8 (0=insufficient, 1=drifting, 2=stable, 3=improving) |
| correction_rate_bps         | u16                        |
| window_secs                 | u32                        |
| attestations                | Vec<MeshAgentAttestation>  |

struct MeshAgentAttestation {
    agent_did:        [u8; 32], // ed25519 did:key fingerprint
    sig:              [u8; 64], // ed25519 signature over (root || count || signal || window)
}
```

### 3.3 Data source: WWWD gate-fire log

The canonical local data source is the JSONL log at:

```
~/.claude/projects/C--Users-Will/memory/_system/wwwd_gate_fires.jsonl
```

Schema (one JSON object per line):

```json
{
  "ts": "2026-05-24T16:08:33Z",
  "session_id": "...",
  "primitive_id": "P·what-would-will-do",
  "decision_class": "tool_call|delegation|pivot|...",
  "gate_outcome": "fire|skip|skip-cooldown",
  "projection": "...",
  "correction_received": false
}
```

The PoM lock script does NOT read this file directly (lock scripts are pure
predicates over witness data, no I/O). The off-chain prover:

1. Reads the JSONL log
2. Computes the merkle blake2b root over the filtered subset (`primitive_id =
   target` AND `ts` within `window_secs`)
3. Computes the convergence signal via the same algorithm as
   `wwwd-corpus-refresh.py`
4. Collects K-of-M mesh agent signatures over the (root, count, signal,
   window) tuple
5. Posts the witness on-chain; the lock script verifies signatures + checks
   predicates against the type-script-encoded thresholds.

### 3.4 Predicates encoded in the type script

The cell's type script args encode the unlock thresholds:

- `min_gate_fire_count: u64` (e.g. 100)
- `required_signal_floor: u8` (e.g. 2 = stable-or-better)
- `min_correction_rate_bps: u16` (e.g. 100 = 1%)
- `window_secs: u32` (e.g. 14 × 86400 = 1209600)
- `k_of_m: (u8, u8)` (e.g. 3-of-5 mesh validators)
- `mesh_validator_set_root: [u8; 32]` (merkle root over authorised DIDs)

These are immutable for the cell lifetime; changing thresholds means migrating
to a new cell.

### 3.5 Why this is PoM and not PoW

PoW asks: "did the prover burn N expected hashes?" — purely energetic.
PoM asks: "did the prover demonstrably engage in convergent cognition on this
primitive, witnessed by K of M independent observer-agents?" — structural and
observable.

The mesh-agent attestation requirement closes the airgap: a solo cheater can
fake gate-fires in their local log, but cannot fake K-of-M independent
attestations without colluding with K-of-M mesh validators. The attack surface
is the validator set, which is identity-anchored via AgentCell (CKB-side) or
AgentRegistry.sol (EVM-side, bridged via canonical messaging).

See `[P·honesty-as-structural-load-bearing-property]` and
`[P·airgap-problem-blockchain-vs-reality]`.

## 4. Cross-chain bridge: EVM Solidity ↔ CKB cells

VibeSwap's canonical burn-and-mint cross-chain messaging
(`docs/research/papers/post-layerzero-canonical-messaging.md`) is substrate-
agnostic. The bridge contracts already designed for EVM ↔ EVM coexistence
extend to EVM ↔ CKB with no design change at the protocol layer.

Per-primitive bridge flow:

1. **PrimitiveNFT (EVM) → PrimitiveCell (CKB)**: burn ERC-721 on EVM emits
   `BurnForBridge(primitiveId, ckb_recipient_lock_hash)`. BLS-signed
   validator quorum attests; mint corresponding PrimitiveCell on CKB with
   `content_hash`, `frontmatter_hash`, `fork_parent_id` copied verbatim.
2. **Datatoken (EVM ERC-20) → DatatokenCell (CKB UDT)**: same pattern, amount
   field preserved. Total cross-chain supply conserved by attestation-graph
   reconciliation (per `[F·canonical-tokens-substrate-port]`).
3. **Royalty / vault state**: NOT bridged. Each chain accumulates locally;
   Shapley settlement happens on the chain of origin.
4. **EscrowVault bonds**: NOT bridged in v1. JUL bond posted on the substrate
   where the disputed claim was filed. Cross-substrate disputes deferred to
   Cycle 5+.

Bridge security model: same as base canonical-messaging stack. BLS12-381
threshold sigs, bonded validator network, MessagingPoM (the cross-chain
verifier already named `MessagingPoM.sol`, which is itself a Proof-of-Mind
construction one level up). Naming convergence is intentional, not coincidence.

## 5. Migration ramp

Honest sequencing — EVM ships first, CKB ships canonical, both coexist
indefinitely via the bridge.

| Phase | Target | Criteria |
|---|---|---|
| Phase 0 (now) | Spec doc + Rust scaffolds | This document + `contracts-ckb/` workspace exist; nothing built |
| Phase 1 (~4 wk) | Capsule build green on one script | `capsule build` produces a RISC-V binary for `primitive-cell-type-script`; unit tests via `ckb-testtool` pass for happy-path |
| Phase 2 (~8 wk) | All 6 scripts buildable + dev integration tests | Round-trip transactions on CKB devnet for {mint, transfer, consume, settle, bond, slash} |
| Phase 3 (~16 wk) | Testnet deploy on Pudge | Public testnet cells live; bridge integration test against VibeSwap EVM testnet |
| Phase 4 (~6 mo) | Audit + mainnet candidate | External audit pass on both substrates; PoM mesh validator set bootstrap (≥ 5 independent JARVIS-OS installs running attestation daemon) |
| Phase 5 (canonical) | Mainnet cutover | Cutover criterion: ≥ 30 days of clean bridge operation with non-trivial cross-chain volume + zero canonical-supply discrepancies. Cutover is NOT migration-away-from-EVM — it is canonical-status acknowledgement; both chains remain active |

Cutover is acknowledgement of canonical status, not abandonment of EVM. EVM
remains the high-tooling-density substrate; CKB carries the
post-quantum / cell-model-canonical authority.

## 6. Parity proofs across substrates (open questions)

The substrate-port-pattern primitive demands that **security properties hold
across substrates**. Below: properties + parity status.

| Property | EVM | CKB | Parity status |
|---|---|---|---|
| Conservation (datatoken supply) | ERC-20 `_balances` + restricted mint role | Type-script `Σ(inputs) ≥ Σ(outputs)` per-tx | **Open**: EVM relies on AccessControl; CKB on cell-tx invariant. Equivalence proof = Cycle 5 work |
| Lineage immutability | Storage struct + restricted setters | Cell data immutable post-mint per type script | **Direct port** — same property different shape |
| Citation-root anchoring | `CitationAnchor.sol` epoch merkle root | Cell-tx writing new `last_citation_root` field, gated by CRPC witness | **Direct port** |
| Bond + slash | `EscrowVault.sol` UUPS + AccessControl router | EscrowVaultCell + type script + CRPC witness | **Direct port** modulo router shape |
| Post-quantum signatures | NOT today (ECDSA-bound) | Lock-script-level choice from day one | **CKB-only structural property** (EVM cannot match without L1 upgrade) |
| MEV resistance | CommitRevealAuction.sol on EVM | Open: CKB does not have native batch-auction infra; needs port | **Open: Cycle 5+ work** |
| Cross-substrate replay protection | Per-message nonce + chain-id in canonical messaging hub | Same hub | Direct port |

## 7. References

- EVM track: `vibeswap/contracts/psinet/` (PrimitiveRegistry, Datatoken,
  LineageRoyaltyVault, EscrowVault); Cycles 1-3 audit workspace at
  `audits/psinet-mindmesh-cycle-{1,2,3}/`
- Substrate-port-pattern: `memory/feedback_account-model-agnostic.md`
- Canonical messaging: `docs/research/papers/post-layerzero-canonical-messaging.md`
- OPH integration: `Desktop/jarvis-os-x-oph-consensus-integration-2026-05-24.md`
- WWWD gate-fire log:
  `~/.claude/projects/C--Users-Will/memory/_system/wwwd_gate_fires.jsonl`
- CKB references: ckb-std crate; ckb-script-templates GitHub; Nervos CKB RFCs
  on UDT, type scripts, lock scripts
- Capsule toolchain: docs.nervos.org/docs/labs/capsule

---

**WWWD discipline applied**: honest-number on track maturity (EVM > CKB
today); substrate-port-pattern documented per property with open questions
flagged; deployment-phase honest — zero CKB deployments, this is a spec +
scaffold.

---

## Addendum (§3.2): MeshAgentAttestation extended for on-chain merkle proof

Added: CYCLE5 (PoM lock-script ed25519 + validator-set membership).

The original §3.2 `MeshAgentAttestation` struct only carried `agent_did`
and `sig`. The on-chain lock script needs to verify each attester is in the
authorised validator set (rooted at `mesh_validator_set_root` in the
type-script args). Carrying a binary merkle proof inline per attestation
keeps the lock-script stateless (no on-chain validator registry read) at
the cost of `proof_len × 32` extra witness bytes per attester.

Updated witness encoding (per-attestation, variable length):

```
| field        | bytes               | type           |
|--------------|---------------------|----------------|
| agent_did    |  32                 | [u8; 32]       |
| sig          |  64                 | [u8; 64]       |
| proof_len    |   1                 | u8 (≤ 24)      |
| proof_dirs   |   1                 | u8 bitmap      |
| proof_nodes  | proof_len × 32      | [[u8; 32]; N]  |
```

`proof_dirs` bit `i` indicates whether `proof_nodes[i]` is the left
sibling (1) or the right sibling (0) of the running hash at that level.
Leaf = `blake2b(agent_did)` with CKB-default-hash personalisation
(`b"ckb-default-hash"`). Final hash must equal `mesh_validator_set_root`.

Signed payload (the bytes each attester signs over):

```
log_root[32] || fire_count_le[8] || signal[1] || window_secs_le[4]   = 45 bytes
```

`correction_rate_bps` is intentionally NOT in the signed payload — the
attester signs the raw cognition observation; the derived metric is
asserted by the lock script independently against the args-encoded floor.

Off-chain prover responsibility: build the validator-set merkle tree
once (sorted DIDs, blake2b inner nodes w/ CKB personalisation), persist
it next to the witness builder, and emit the per-attestation
`(proof_dirs, proof_nodes)` tuple when assembling the witness.

Implementation: `contracts-ckb/proof-of-mind-lock-script/src/main.rs`
(`verify_attestations` + `verify_merkle_proof`). Crate choice:
`ed25519-compact` over `ed25519-dalek` for no_std + no_alloc fit on
CKB-VM; receipts in the source-file comment block.

Status: source compiles to the syntax/borrow level on host (rustc parse
clean); end-to-end cargo build on this Windows host blocked by missing
MSVC build tools (heapless build.rs links host-side). Pre-existing
repo-wide blocker, not introduced by this addendum. RISC-V binary
artifact and integration tests pending toolchain availability.
