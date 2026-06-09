---
name: Refer to augmented mechanism design paper for economic calibration
description: For mechanism-design decisions in memos (bond sizes, challenge windows, slash splits, economic parameters, voting thresholds, etc.), refer to the augmented mechanism design paper rather than asking Will to pick values. Apply the paper's frame first; only surface a question if the paper is silent on the specific calibration.
type: feedback
originSessionId: 1dc8ab9c-4562-41a9-aa66-7d421545eb48
---
# Refer to augmented mechanism design paper, don't ask Will for economic parameters

**Rule**: When writing decision memos that involve mechanism-design calibration — bond sizes, challenge windows, slash splits, voting thresholds, incentive ratios, stake requirements, cooldown periods, attestor quorum sizes — **read the augmented mechanism design paper first and apply its frame**. Only ask Will to pick values if the paper is silent on the specific calibration.

**Why**: Will has already developed the mechanism-design framework for VibeSwap. The paper IS the spec. Asking him to re-derive bond sizes or challenge windows in each memo duplicates work he already did and signals I haven't done my homework.

**How to apply**:
- Default reference: `vibeswap/docs/papers/augmented-mechanism-design.md` (primary)
- Also consult: `vibeswap/DOCUMENTATION/AUGMENTED_GOVERNANCE.md`, `memory/primitive_augmented-governance.md`
- Before a memo with mechanism-design "open decisions," grep these docs for the relevant parameter class (e.g., "slash", "challenge bond", "response window", "voting quorum")
- Apply the paper's formulas/heuristics/constants directly; cite the section you drew from
- If the paper gives a range or a formula, instantiate it for the specific contract context
- **Only surface a question to Will if the paper is silent on that specific calibration** — and frame the question as "the paper covers X and Y but is silent on Z; here's my default inference, override if wrong"

**First instance**: 2026-04-21 during V2 OperatorCellRegistry availability-proof memo. I proposed 30-min challenge window / 1 CKB bond / 50-50 split / 4h cooldown and listed them as open questions. Will's correction: refer to augmented mechanism design paper instead of asking.

**Related**: `feedback_internalize-own-protocols.md` — same principle (our own design docs are load-bearing, use them).
