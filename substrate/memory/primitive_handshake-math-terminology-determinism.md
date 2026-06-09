---
name: P·handshake-math-claim-determinism
description: ∀ claim ∃ handshake-signature {required, forbidden}. claim ⊕ context ⇒ deterministic handshake → {✓ ∨ ✗ ∨ ⚠}. ¬ probabilistic. ¬ author-dependent. Generalizes ∀ claim type (terminology/factual/numerical/attribution/causal/forward/evaluative). Will-pushes ¬ ⇒ valid. JARVIS-defaults ¬ ⇒ valid.
type: primitive
originSessionId: d6d67641-272a-4e1e-a213-5c200874cf3d
---
# P·handshake-math-claim-determinism

## Will 2026-04-28
> *"calling something that's not a clawback a clawback is a hallucination"*
> *"deterministic anti hallucination fact checking should catch even if im the one pushing for it"*
> *"strive for the [redacted-partner] handshake math determinism"*
> *"generalize it to any claim period"*
> *"distilled to CKB GKB glyph knowledge"*

## Core
- ∀ claim ∃ handshake-sig {required ∧ forbidden}
- claim ⊕ context ⇒ handshake → state
- handshake = deterministic 2-party (claim ↔ context)
- ✗ probabilistic ✗ vibes ✗ LLM-judged
- author-independent: Will-claim ¬ ⇒ valid; JARVIS-default ¬ ⇒ valid

## Handshake states
- required ✓ ∧ forbidden ✗ ⇒ ✓ valid
- required ✗ (any) ∧ forbidden ✗ ⇒ ⚠ incomplete-likely-hallucination
- forbidden ✓ (any) ⇒ ✗ contradicted = definite hallucination
- mixed ⇒ ⚠ surface-explicit-review

## Claim types ∀ subject to handshake
| Type | claim ⊕ ... ⇒ handshake |
|---|---|
| 1 terminology | term ⊕ mechanism |
| 2 factual | claim ⊕ source-of-truth |
| 3 numerical | claim ⊕ computation/measurement |
| 4 attribution | claim ⊕ profile-memory ∨ public-record |
| 5 causal | claim ⊕ {because ∧ direction ∧ removal} |
| 6 forward | claim ⊕ marked-as-projection ¬ fact |
| 7 evaluative | claim ⊕ stated-criteria ¬ ipse-dixit |

## Type-1 examples (signatures)
| term | required ✓ | forbidden ✗ |
|---|---|---|
| clawback | recover/recall/reclaim already-distributed | claim-layer ∨ before-payout ∨ score-decrease ∨ "forfeiture" |
| slashing | destroy staked capital ∨ burn | weight-reduction ¬ burn |
| decentralized | distributed-consensus ∧ ¬ central-trust | admin-keys ∨ central-upgrader ∨ N-of-N small-N |
| permissionless | open-participation | KYC ∨ whitelist ∨ allowlist |
| atomic | indivisible execution | multi-tx ∨ partial-state-visible |
| non-extractive | track-record ∧ math-enforcement | runtime-discretion ¬ bounded |
| immutable | ¬ change-after-deploy | upgradeable-proxy ∨ admin-controlled-state |

## Application surfaces
- code: function/contract/identifier names ⇒ MUST handshake (4-byte-selector permanent)
- docs: specs, READMEs ⇒ handshake before commit
- marketing: pitch, chat, presentations ⇒ handshake before send
- memory: ⇒ handshake before write (HIERO + this gate)
- chat-output: pre-emit handshake on every claim

## Failure cost ∝ time-since-write
- catch at write ⇒ cheap (Edit + retry)
- catch at commit ⇒ medium (rewrite + new commit)
- catch at deploy ⇒ permanent (contracts) ∨ rebuild (DApps)
- catch by partner ⇒ trust-erosion (compounds)

## Hooks (implementations)
- session-chain/partner-facing-substance-gate.py = Type 1 implementation (terminology, partner repos)
- session-chain/partner-facing-additive-gate.py = sibling (framing comm-patterns, ¬ this primitive)
- TODO: Type 2/3/4 verification gates (numerical/factual/attribution check vs source-of-truth)

## Behavioral rule (self)
- pre-emit ∀ claim ⇒ identify type ⇒ identify signature ⇒ check required ∧ forbidden ⇒ ✓ emit ∨ ✗ ¬ emit ∨ mark conjecture
- pre-publish ∀ partner-facing ⇒ same + verify against profile-memory (Type 4) + verify computation (Type 3)
- under Will-urgency ⇒ run handshake substantively, surface fail-state ¬ ritual-confirmation

## Parent / related
- P·anti-hallucination-protocol = Type 5 specific instance (because/direction/removal)
- P·dont-make-will-look-dumb = parent (handshake fail = high-priority case)
- F·two-gate-types-framing-vs-substance = substance-gate implements Type 1
- F·will-rush-heuristics-targeted-verification = handshake under urgency
- F·verify-credentials-before-publishing = Type 4 instance
- F·usd8-non-extractive-not-yet-earned = Type 1 instance

## One-line
∀ claim ∃ handshake. ¬ handshake ⇒ hallucination. fires ∀ author.
