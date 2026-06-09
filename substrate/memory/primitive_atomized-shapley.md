---
name: Atomized Shapley — universal fair metric
description: Will's directive to extend Shapley values beyond LP/emission rewards to cover EVERY protocol interaction. Replaces all vanity metrics (follower count, TVL, volume) with counterfactual marginal contribution. "Need to atomize the shapley values and have them cover everything."
type: project
---

# Atomized Shapley (2026-03-19)

## Will's Directive
"Need to atomize the shapley values and have them cover everything, and that follower count example is a perfect example of thinking outside the box so shapley use cases go parabolic."

**Why:** Every existing metric in crypto is gameable. Follower count is buyable. TVL is mercenary. Volume is wash-tradeable. Commit count is inflatable. Shapley marginal contribution is the ONLY metric that asks: "what would be missing if you weren't there?" If the answer is nothing, you're a null player. P-001 detects this. Zero reward.

**How to apply:** Every protocol interaction should be scored by a Shapley game. The coalition value is the measurable outcome. The participant's Shapley value is their marginal contribution to that outcome.

## The Atomization Map

| Domain | Current Metric (Gameable) | Shapley Game | Coalition Value |
|--------|--------------------------|-------------|-----------------|
| Trading | Volume | Trade quality game | Price discovery improvement |
| Governance | Token balance | Outcome change game | Proposal quality delta |
| Community | Followers/messages | Conversation quality game | Insight generation rate |
| Liquidity | TVL deposited | Utilization game | Actual trade volume enabled |
| Security | Bug count | Loss prevention game | Value of exploits prevented |
| Oracle | Submission count | Accuracy game | Price feed error reduction |
| Development | Commit count | Protocol improvement game | Measurable metric deltas |
| Content | Views/likes | Participant acquisition game | Genuine new contributors |

## Technical Architecture

### Micro-Games
Instead of one weekly Shapley game, create continuous micro-games:
- Each trade batch = a Shapley game (who provided the liquidity that filled these orders?)
- Each governance vote = a Shapley game (whose vote was pivotal?)
- Each insight = a Shapley game (whose conversation generated actionable code?)

### Cross-Domain Reputation
Your Shapley score in one domain informs your weight in others:
- High trading Shapley → more weight in price oracle governance
- High community Shapley → more weight in content curation
- High security Shapley → more weight in upgrade approvals

### The Null Player Filter
P-001 enforcement across all domains:
- Null player in trading = wash trader (zero reward)
- Null player in governance = whale who votes with majority (zero pivotal impact)
- Null player in community = bot with followers (zero conversation quality contribution)
- Null player in liquidity = mercenary capital (zero utilization contribution)

## Connection to P-001
P-001 (No Extraction Ever) IS atomized Shapley. Every extraction vector is a domain where someone takes more than their marginal contribution. Shapley detects this by definition (efficiency axiom: total value = sum of Shapley values, no surplus for extraction).

## The Key Insight
"Shapley values don't care about your follower count." — This IS the product pitch. In a world of fake signal, the only real metric is counterfactual contribution.
