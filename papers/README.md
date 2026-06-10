# Papers

The essays that specify or justify pieces of the JARVIS architecture, plus the broader canonical-thinking corpus.

## JARVIS-specifying essays

| File | What it is |
|---|---|
| [`jarvis-is-not-a-wrapper.md`](./jarvis-is-not-a-wrapper.md) | The source-of-truth essay that specifies this repo. Eight layers, concrete artifacts, five verification checks. |
| [`jarvis-is-not-a-wrapper.x-thread.md`](./jarvis-is-not-a-wrapper.x-thread.md) | 22-tweet condensed version for X / Twitter. Each tweet ≤280 chars. |
| [`structural-fairness-has-a-name.md`](./structural-fairness-has-a-name.md) | The brand-anchor essay. Names the chain (Shapley 5-axiom + AMD + Augmented Governance + Composable Fairness Arrow Inversion) that "structural fairness" actually is. Published on Medium 2026-06-09. |
| [`hiero.md`](./hiero.md) | Dictionary paper for the HIERO operator-density memory format. Converts JARVIS from personal architecture to public protocol by publishing the format other operators need to read the corpus. |
| [`multiplicative-compression.md`](./multiplicative-compression.md) | Argues that HIERO++ byte-side compression composes multiplicatively with API-side prompt caching. Byte-side measurements are direct (MEMORY.md 6,779 → 3,026 tok, -55% on 2026-06-10). The order-of-magnitude session-cost cut is derived arithmetic from Anthropic's published cache pricing × measured byte reductions; cache-hit telemetry on the running substrate not yet wired — paper flags this gap explicitly. |

## Canonical-thinking corpus

125 markdown papers (59 with PDF companions) live in this directory. Major series:

- **Augmented-X series** (89 papers) — Augmented Mechanism Design, Augmented Governance, Augmented AI Alignment, Augmented Antitrust, Augmented Carbon Markets, Augmented Education, Augmented Cybersecurity, etc. Each applies the math-enforced-invariants methodology to a different domain.
- **Shapley + fairness math** — five-axioms-paper (multilingual: en/es/zh), composable-fairness-arrow-inversion, atomized-shapley, contribution-dag-lawson-constant, harberger-license-mechanism.
- **VibeSwap mechanism design** — commit-reveal-batch-auctions, clearing-price-convergence-proof, from-mev-to-gev, five-layer-mev-defense-ckb, execution-settlement-separation, cooperative-capitalism, cooperative-emission-design, cooperative-game-elicitation-stack.
- **Airgap and consensus** — airgap-problem-onepager, asymmetric-cost-consensus, nakamoto-consensus-infinite, ckb-economic-model-for-ai-knowledge.
- **Substrate philosophy** — convergent-architecture, dissolving-the-owner, knowledge-primitives-index, human-symbolic-compression, idea-execution-value-separation.

Each paper is markdown, greppable, version-controlled, and cross-referenced from memory primitives via the Code ↔ Text Loop. A subset have PDF companions for partner-distribution.

The same corpus is mirrored at [`vibeswap/docs/research/papers/`](https://github.com/wglynn/vibeswap/tree/master/docs/research/papers) — JARVIS holds the canonical copies, VibeSwap maintains its own copy as the substrate-of-record for VibeSwap-internal cross-references.
