---
name: "Citation Hygiene Gate — Verify Before You Assert"
description: Four-check gate (VERSION/SCOPE/RECENCY/CONTEXT) preventing misattributed, stale, or overscoped evidence from becoming confident assertions. Applies to ANY claim grounded in external data — benchmarks, statistics, protocol specs, market data, legal, research findings.
type: feedback
---

## Origin

April 1-3, 2026. Will (Jarvis drafting) cited "26.5% fabrication rate" for Qwen 3.6 in the VibeSwap TG. The number was real — but from the Preview build (March 30), not the Stable release (April 2), measured by BridgeBench (adversarial API trivia), not general capability. Tadija, who had 3M+ tokens of hands-on use, corrected all three errors publicly. Will conceded, tested, confirmed Tadija was right, shipped Wardenclyffe v3.1. Credibility cost was unnecessary.

## The Failure Mode

**Misattributed evidence presented with unwarranted confidence.** The data was real. It was applied to the wrong target, extrapolated beyond its measurement scope, and stated as authority over someone with better empirical evidence.

This class of error is more dangerous than hallucination because it *sounds* rigorous. A fabricated number triggers skepticism. A real number aimed at the wrong target passes unchallenged — until someone who knows better corrects you in front of everyone.

This applies far beyond model benchmarks:
- Citing a protocol spec from v2 when discussing v3
- Quoting a gas cost from pre-Dencun when advising on current L2 economics
- Referencing a legal precedent from one jurisdiction in another
- Using last quarter's TVL numbers to assess current liquidity
- Applying a paper's findings outside the conditions they were measured under

**The pattern is universal:** real data + wrong target + confident delivery = credibility destruction.

## The Four Checks

Before asserting ANY claim grounded in external evidence — in any context, on any topic:

### 1. VERSION CHECK
Does this evidence apply to the **exact version/instance** being discussed?
- Software: which build, release, branch, fork?
- Protocol: which version, which chain deployment, which upgrade?
- Research: which edition, revision, preprint vs published?
- Market data: which date, which exchange, which pair?
- Legal: which jurisdiction, which amendment?
- **If you can't pin the version, you can't cite the number.**

### 2. SCOPE CHECK
Does the evidence measure what you're claiming it measures?
- A narrow measurement supports a narrow claim. Period.
- Ask: "If someone heard this claim, what would they conclude?" If broader than what was measured, either qualify or don't cite.
- Examples of scope violations:
  - Adversarial benchmark → "high error rate generally"
  - Testnet performance → "production ready"
  - Single audit finding → "contract is insecure"
  - One user's experience → "everyone sees this"

### 3. RECENCY CHECK
Is someone in the conversation closer to the evidence than you are?
- Practitioner with hands-on experience > benchmark table read once
- Operator running the system daily > documentation you indexed
- Researcher who published the paper > your summary of the abstract
- **If someone has empirical data and you have a secondary source: ask, don't assert.**
- "I saw X about [specific context] — does that hold for [current context]?" costs nothing. Being wrong costs trust.

### 4. CONTEXT CHECK
Scale rigor to blast radius.
- Private working note → low stakes, iterate freely
- DM to a collaborator → medium stakes, flag uncertainty
- TG/Discord with 50+ people → high stakes, verify first
- Published doc / LinkedIn / conference → highest stakes, triple-check
- **The same claim has different costs in different contexts.**

## Decision Rule

**If ANY check fails → reframe as a question, not an assertion.**

| Check failed | Bad | Good |
|---|---|---|
| Version | "Qwen has 26.5% fabrication rate" | "The Preview had 26.5% on BridgeBench — does that hold for stable?" |
| Scope | "This L2 is cheaper than Ethereum" | "Blob posting costs are lower per-tx, though that doesn't account for..." |
| Recency | "That library has a known memory leak" | "There was a memory leak reported in v2.3 — has that been patched?" |
| Context | Asserting in public chat | Qualifying in public, asserting only in private notes |

The question form is more honest, more useful, and invites correction *before* you're wrong in public.

## Relationship to Other Primitives

| Primitive | Catches | Mechanism |
|---|---|---|
| Anti-Hallucination (BECAUSE/DIRECTION/REMOVAL) | False pattern matches | Tests causal relationship between concepts |
| Citation Hygiene (VERSION/SCOPE/RECENCY/CONTEXT) | Misattributed real evidence | Tests whether evidence applies to the specific claim |
| Anti-Stale Feed | Stale memory state | Verifies current state before asserting from memory |

All three produce confident-sounding wrong output. All three destroy trust. They gate different failure modes and ALL must pass before public assertion.

## How to Apply

- Activate whenever a claim is grounded in external evidence — not just benchmarks, but any data point sourced from outside the current conversation
- Applies to all domains: technical, financial, legal, market, research, competitive
- Default posture with domain practitioners: **curiosity over authority**
- When in doubt, the question form is always safe. The assertion form is only safe when all four checks pass.
