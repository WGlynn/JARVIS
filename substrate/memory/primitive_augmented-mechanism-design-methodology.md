---
name: Augmented Mechanism Design (Methodology)
description: Augment markets/governance with math-enforced invariants ¬ replace. 4 invariant types (Structural ∧ Economic ∧ Temporal ∧ Verification) composed 2-4 at a time. Paper = parameter authority.
type: primitive
originSessionId: 79044125-45c4-486a-9ac0-ec65bb0d9b76
---
# Augmented Mechanism Design — Methodology

## ⚙ Rule
- Replace ✗ ⇒ admins / new trust-points / new failure modes / new capture surfaces
- Augment ✓ ⇒ market still functions ∧ math-enforced invariant rules out bad behavior by construction

## 📍 Source
- `vibeswap/DOCUMENTATION/AUGMENTED_MECHANISM_DESIGN.md` (246 lines)
- Extract: 2026-04-27 (Batch 2, glyph-KB conversion)

## 🧩 Four invariant types
- **Structural** ⇒ holds by construction. Ex: uniform clearing price, Fisher-Yates from XOR'd secrets
- **Economic** ⇒ cost asymmetry; breaking possible but unprofitable. Ex: 10e18 CKB cell bond, 50% slash + 75% mind-score reset on equivocation
- **Temporal** ⇒ time-lock constraint. Ex: 8s commit / 2s reveal, 7-day unbond, 1-day claim TTL
- **Verification** ⇒ cryptographic attestation. Ex: EIP-712 domain-separated sigs, Merkle-proof commits, ZK-proof of off-chain compute

## 🔧 6-step apply protocol
1. State the property concretely
2. Identify which invariant types enforce it
3. Compose 2+ types (defense-in-depth)
4. Size parameters from paper §, ¬ from tuning
5. Triad-check the resulting design
6. Ship with regression tests (test = executable form of invariant)

## 📊 Real composed mechanisms
- **Commit-Reveal Batch Auction** = Structural ∧ Temporal ∧ Verification
- **OperatorCellRegistry** = Economic ∧ Temporal ∧ Verification
- **ClawbackCascade** = Structural ∧ Economic ∧ Temporal ∧ Verification

## 💵 Paper = parameter authority
- All concrete numbers ⇒ `memory/feedback_augmented-mechanism-design-paper.md` § references
- ¬ invent values; look them up
- §6.1 Temporal | §6.2 sybil-bond sizing | §6.5 Compensatory split | §7.3 unbonding | §7.4 contest

## ✓ When applicable
- Mechanism design where market/governance functions but extraction surface exists
- Composability boundaries (cross-protocol, cross-chain)
- Any "should we add an admin?" question

## ✗ When inapplicable
- Pure infrastructure (consensus, networking) — different design layer
- Parameter tuning of well-designed mechanism — paper §, ¬ this primitive

## 🚨 USD8 application
- DIRECT-PORT — methodology is substrate-independent
- Cover Pool fee distribution = Structural (Shapley closed-form) ∧ Verification (Brevis proof on inputs)
- Snapshot commitment = Verification (sparse-Merkle root) ∧ Temporal (daily cadence)

## 🪝 Triggers
- "should we add an admin / role / oracle?" ⇒ STOP, run methodology
- "how do we prevent X?" ⇒ frame as invariant ¬ as rule
- New mechanism design proposal ⇒ Step 1-6 mandatory

## ⚠ Anti-pattern
- Rule-based enforcement ("admin catches X, slashes them") ⇒ discretion ⇒ trust-point ⇒ capture surface
- Single invariant type ⇒ ¬ defense-in-depth
- Tuning parameters ad-hoc ⇒ paper § exists for a reason

## 🔗 Related
- `P·substrate-geometry-match` — geometry first, methodology second
- `P·augmented-governance` — accountability layer (Physics > Constitution > Governance)
- `P·correspondence-triad` — Step 5 gate
- `feedback_augmented-mechanism-design-paper` — parameter authority
