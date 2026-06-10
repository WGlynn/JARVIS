---
name: rick-web3-work-platform-2026-05-14
description: Rick opens 2026-05-14 to web3 native retroactive funding layer for contributor work. Concern: Shapley overhead per task. Response frame: pairwise approximation + Contribution DAG hierarchy + periodic resolver → O(N) not O(2^N). Deep Funding lineage closes credibility.
type: project
originSessionId: 35d175e9-bf70-4d8f-b83a-b82bdd9d8fdf
---
## Rick message anchor (2026-05-14 03:41-03:43 ET)

> *"I always wanted a web3 native work platform where contributors gets rewarded. I was following a platform doing web3 based task system but I don't think it went well. I think it's hard to decide the Shapley value down to each task and might add a lot of overheads. Maybe we can experiment with this openly, like I post tasks on github forum with a price attached, ppl can just take them. Could experiment? Wty?"*
>
> *"Contributor could get rewarded with either USD8 or a gov token entitle for future rev share or something would be cool"*

## State

- Rick OPEN ✓ ∀ web3 native retroactive-funding layer
- Concern: Shapley overhead per-task ⇒ correct ∀ naive 2^n exact
- Proposed v0: GitHub forum + price-attached tasks ⇒ market-baseline
- Rewards: USD8 ∨ gov-token (future rev share)
- Posture: experiment-mode ✓ ¬ commitment-mode

## Frame

3-hook prep ∀ Will-delivery (per `[F·jarvis-prep-not-delivery-for-partner-chat]`):

1. **Rick instinct correct ∀ naive Shapley, wrong ∀ approximation-stack.** Question ≠ "how compute exact Shapley per task"; question = "how approximate s.t. 5 axioms hold within tolerance ∧ cost ∝ platform-scale."

2. **Approximation stack (3 composable techniques):**
   - **Pairwise**: O(n²) pairwise marginals + efficiency-symmetry constraints ⇒ Shapley vector. Castro/Gómez/Tejada (2009). SHAP deploys variants daily.
   - **Contribution DAG hierarchy**: cluster Shapley + within-cluster redistribute. Exponential → linear. EF Deep Funding pattern.
   - **Periodic resolver + real-time marginal**: contributors get marginal-contribution score immediately, Shapley redistributes weekly/monthly. Same as VibeSwap commit-reveal: real-time bid → periodic settlement.
   - Combined cost @ N=10K contributors × 1K tasks × avg 5/task = ~25K pairwise comparisons/cycle ⇒ trivial.

3. **Deep Funding lineage closes credibility in Rick's vocab.** [J·deepfunding-research]: deepfunding.org = EF-supported, Vitalik-seeded $250K Jan 2025, Shapley-axiom credit attribution ∀ OSS-dependency-graph. Will worked there. Same methodology, new substrate (contributor labor ¬ OSS deps).

## Strategic move

Augmented Mechanism Design pattern (per `[F·augmented-mechanism-design-paper]`):
- ¬ replace Rick's market (his task prices stay)
- augment ∀ math-invariant (Shapley periodic resolver)
- Market does price discovery; math does fairness redistribution; both load-bearing
- Same shape as VibeSwap commit-reveal + ShapleyDistributor

Back-test pattern for Rick's experiment:
1. Track flat-price payout per task as baseline
2. Compute pairwise-approximated Shapley over accumulated DAG monthly
3. Surface divergence: under/over-rewarded contributors
4. Shapley vector = redistribution proposal ¬ replacement

## Will-delivery cadence

Per `[F·rick-keep-it-simple]`: depth ✓ ∧ volume ✗. Pull > push.

Opening reply (one Will message):
- 1 sentence: yes, naive Shapley overhead is real
- 1 sentence: approximation stack collapses it to ~linear in N
- 1 sentence: offer whiteboard ∀ when Rick asks the follow-up

Full framework lands ∀ Rick-asks. Otherwise scaffolding ¬ deliverable.

## Reward-token framing (Rick raised)

Rick: USD8 ∨ gov-token (future rev share). Both fit AMD:
- USD8 = stable, immediate, market-default
- Gov-token = retroactive-rev-share ⇒ aligns long-term contribution w/ protocol-value
- Hybrid: USD8 for task-complete, gov-token for periodic Shapley-redistribution bonus
- Connects to `[P·fractalized-shapley-games]` (nested attribution games) ∧ `[F·jul-is-primary-liquidity]` (3-token role separation: JUL=money, VIBE=gov, CKB=state-rent)

## Reciprocal pattern

`[P·shapley-referral-game]` (Will-named earlier in conv): Shapley-based referral system game. Contributor X who brought Y onto platform earns share of Y's downstream value via Shapley axiom. Eliminates MLM-style pyramid (efficiency axiom guarantees no recycling). Direct fit ∀ Rick's "contributor brings contributors" question from earlier exchange.

## Status

- 2026-05-14 04:59 ET: prep complete, awaiting Will-delivery to Rick
- 2026-05-14 05:07 ET: Will-compressed reply drafted (~80 words, 4-hook one-liner) at `Desktop/2026-05-14_rick-reply-shapley.md`
- 2026-05-14 05:09 ET: Will confirmed AMD framing is correct ⇒ **default lens ∀ future Rick-engagements on attribution / mechanism / reward-design**
- Rick has not asked the follow-up yet; opener-first ⇒ pull > push
- Capture: this is the seed of a real partnership artifact if Rick engages

## Validated framings (Will-confirmed 2026-05-14)

**1. Augmented Mechanism Design lens** (confirmed 05:09 ET) — correct default ∀ Rick-platform work:
- Market = Rick's task prices (price discovery, immediate feedback, social-natural)
- Math invariant = Shapley periodic resolver (fairness redistribution, axiom-guaranteed)
- Both load-bearing; neither replaces the other
- Same shape as VibeSwap commit-reveal + ShapleyDistributor; same shape as USD8 cover-pool + redemption price; same shape as `[F·augmented-mechanism-design-paper]` thesis at every scale
- ∀ future Rick-conversations on attribution / contributor-reward / governance-design ⇒ assume AMD frame applies until shown otherwise.

**2. Push-pull cadence** (confirmed 05:10 ET) — short opener that LEAVES room for Rick's follow-up:
- Per `[F·rick-keep-it-simple]`: depth ✓ ∧ volume ✗
- Opener compresses 3 hooks to one line each + offers prototype
- Full framework (DAG hierarchy, pairwise math, periodic resolver) lands ONLY if Rick asks the follow-up
- If he doesn't ask, the framework was scaffolding, not deliverable
- ∀ future Rick partner-chat ⇒ default to opener-first cadence; framework on-demand

**3. Flexibility anchors** (Will-added 05:10 ET):
- **Time-neutral** ⇒ vibeswap tuned time-dim ✗ ∀ contrib scoring (param-tweak)
- **Social-graph merger** ⇒ vibeswap added 2nd contrib-graph ∀ social, merged cleanly (structural-novelty)
- Rick use-case ∋ heterogeneous types {code, design, community, docs} ⇒ social-graph-merge = stronger anchor
- ∀ flexibility-follow-up ⇒ lead social-graph-merge; time-neutral = 2nd

**4. Reserve demo — conversation-to-code pipeline** (Will-added 05:12 ET):
- TG conv → memory + JARVIS + project commits ∀ JARVIS overlay
- This session ≡ working proof: ~40 commits × 3 repos ← chat input
- Connects: `[F·text-code-eternal-loop]` ∧ `[P·code-text-inspiration-loop]` ∧ `[P·chat-to-dag-traceability]`
- ∀ Rick platform ⇒ ideation/discussion = 1st-class contrib ∈ DAG ∥ code-commits
- "hard ∀ Shapley/task" softens: chat-contrib gets same attribution scaffold ⇒ fewer special-cases ∧ uniform graph
- Reserve ⇒ ✗ lead. Pull-triggered only. Lands ∀ Rick-asks-follow-up post-opener.
