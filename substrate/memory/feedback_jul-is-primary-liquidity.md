---
name: JUL is Primary Liquidity, Not Just PoW Bootstrap
description: JUL is the money layer of the three-token system — PoW-objective + fiat-stable — not merely the mechanism for minting CKB-native. NEVER describe JUL as a bootstrap mechanism and NEVER suggest collapsing it as a simplification.
type: feedback
originSessionId: a1e0e274-6aeb-4b28-9156-b6c7479e2cd3
---
JUL has **two standalone load-bearing roles** and one downstream effect:

1. **Economy**: primary liquidity. JUL is the money layer — PoW-objective + fiat-stable = the network's medium of exchange.
2. **Consensus**: PoW pillar of NCI. Contributes the `0.10 · PoW` component, log-scaled, providing the time-of-genuine-work dimension of attack asymmetry.
3. **Downstream nicety**: JUL-burn also bootstraps CKB-native entry into circulation. Clean side effect, not the reason JUL exists.

The two primary roles (economy + consensus) are independent and each load-bearing. The bootstrap property is a welcome coincidence that falls out of the design.

**Why JUL works as money:**
- **PoW objectivity** — every JUL is backed by verifiable SHA-256 computational work. Anyone can independently verify that mining occurred. This is Bitcoin-style trust applied to the primary-liquidity layer of a cooperative-capitalism system.
- **Fiat-like stability** — JUL behaves as a neutral medium of exchange; its supply responds to mining demand rather than speculation, giving it the stability characteristics of fiat without the centralized issuer.
- **Combined: money.** PoW-objective means no one can fake it; fiat-stable means it's usable as a unit of account; neutral and mineable means it flows freely as a medium of exchange.

**The three-token decomposition (correct framing):**
- **JUL** = money (PoW-objective, fiat-stable, primary liquidity)
- **VIBE** = governance share (PoM-weighted, 21M cap, Shapley-distributed)
- **CKB-native** = state-rent capital (PoS-aligned, elastic, cell-occupation)

Each role is orthogonal. Each token serves its own axis. Together they give the three-dimensional consensus weight function (NCI: 10% PoW + 30% PoS + 60% PoM). Collapsing any one of the three destroys the corresponding axis and the consensus property.

**How to apply:**
- When describing the three-token system in any document (whitepaper, pitch, blog, Medium, Reddit, index), lead with JUL's *monetary role*, not its role as CKB precursor.
- The JUL → CKB burn pathway is one of several JUL uses (others: direct trading, settlement asset, liquidity pairing, fee payment in a native-chain deployment). Do not present burn as JUL's "purpose."
- NEVER suggest collapsing JUL as a complexity-reduction lever. It would destroy the primary-liquidity axis, PoW objectivity, and fiat-like stability simultaneously. The complexity budget for keeping JUL is justified by what the role delivers.
- When the user-facing complexity of three tokens is raised as a concern, the right answer is "users only need to reason about one or two at a time; JUL for transacting, VIBE for governance, CKB-native is mostly infrastructure," not "let's collapse a pillar."

**Why the rule exists:** On 2026-04-21 Claude described JUL primarily as a bootstrap mechanism for CKB-native and suggested collapsing it if complexity became a barrier. Will corrected: *"the JUL serves its own purpose as primary liquidity in the network because it has POW objectivity and fiat-like stability ... dont forget that EVER."* This is a load-bearing design principle, not a passing detail. Any drift from it in future docs or conversations is a direct Verbal→Gate violation.
