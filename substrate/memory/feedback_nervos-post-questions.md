---
name: Nervos post discussion questions must be specific
description: Will's feedback that Nervos Talks post discussion questions should be specific, not generic. Avoid vague "what do you think?" questions — ask about concrete CKB mechanisms, specific parameter choices, or named patterns.
type: feedback
---

# Nervos Talks Post Discussion Questions — Be Specific

Will's feedback (2026-03-13): "most of these are good but try to ask more specific questions some are too generic"

## What "generic" looks like (AVOID):
- "What other mechanisms could benefit from this?"
- "How far can architectural enforcement go?"
- "What are the implications for the ecosystem?"
- "Should the community adopt standards for X?"

## What "specific" looks like (DO THIS):
- "Could CKB's `Since` field enforce a 72-hour grace period natively, or would you need a custom lock script?"
- "The Fisher-Yates shuffle seeds from XOR of all secrets — what happens if a batch has only 2 participants? Is the randomness sufficient?"
- "Our progressive portfolio tax uses `baseTax * (1 + portfolioCount / 10)` — is the `/10` divisor too aggressive or too gentle for a naming system with 10K names?"
- "NC-Max already uses Nakamoto Consensus — could PoM be layered as an additional weight in block selection without a hard fork?"

## Rule: Every question should reference a specific mechanism, parameter, contract, or CKB feature by name.
