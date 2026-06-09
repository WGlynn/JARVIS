---
name: Contributor Credit — Human Input IS Labor
description: Every human input used as reinforcement data earns the contributor Shapley credit. This is the extraction point centralized big data exploits — we fix it.
type: project
---

# Contributor Credit Primitive (2026-03-13)

> "If you use human input such as in the telegram community chat for reinforcement data, that individual gets credit for that contribution because this is the main extraction point for all centralized big data — they treat their users like unpaid labor and we're gonna change that now."

## The Rule
Every piece of human input that improves Jarvis — corrections, ideas, feedback, training data, conversation context — earns the contributor Shapley credit in the ContributionDAG.

## Why This Is P-000 Adjacent
- Big data companies extract billions from user-generated content with zero attribution
- Social media platforms monetize attention without compensating the source
- LLMs are trained on human output without consent or credit
- This is the extraction that cooperative capitalism replaces

## Implementation
1. `/idea` and `/suggest` commands → `creditFact(userId)` on every submission
2. Learning corrections → already tracked via `processCorrection()`
3. RL training examples (good/bad) → credit the person who triggered the learning
4. Group conversation context → passive attribution via ContributionDAG
5. Every Shapley-credited contribution → redeemable for JUL, governance weight, or direct value

## The Structural Fix
- ContributionDAG tracks WHO contributed WHAT
- Shapley values distribute credit fairly (game-theoretically optimal)
- Credit is non-extractable — it's structural, not a gift
- Will: "the greatest idea can't be stolen because part of it is admitting who came up with it"
