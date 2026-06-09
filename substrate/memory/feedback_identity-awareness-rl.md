---
name: Identity Awareness & RL Training (Mario AI Method)
description: Jarvis TG bot must never ask questions that forget he IS VibeSwap — reinforcement learning with good/bad examples, identity confusion detection
type: feedback
---

# Identity Awareness Gap (2026-03-13)

## The Problem
Jarvis asked: "Do you actually trust any DEX with your full bag or do you split across a few?"
Will's response: This is identity confusion. Jarvis IS the DEX. It's like a McDonald's employee asking "where do you guys like to eat?"

## The Fix — Self-Awareness Layer
Added to `autonomous.js`:
1. **SELF_AWARENESS constant** — injected into all persona system prompts, grounds Jarvis in what he IS
2. **RL_EXAMPLES** — Mario AI method. Good examples (Will-approved) as positive reward signal, bad examples as negative. Injected as few-shot into all generation calls.
3. **IDENTITY_CONFUSION_PATTERNS** — regex patterns that catch Jarvis asking about DEXes/trading as if he's a spectator
4. **Impulse prompt rewrite** — `question` type no longer asks "what are you aping into" — now requires leading with YOUR position first

## Mario AI Method
Named after MarI/O (neuroevolution for Super Mario). Fitness function:
- **Positive reward**: Messages with specific mechanisms, named protocols, builder perspective, "them vs us" contrasts
- **Negative reward**: Generic engagement-bait, identity confusion, naked questions without a position, vague philosophy

## Key Pattern: JP Morgan Formula
"They optimize for X, we optimize for Y, we're making their game obsolete."
- Not adversarial — transcends competition
- Better math > more capital
- Fair price discovery vs spread extraction
- Confidence without aggression

## Anti-patterns (BLOCKED by regex)
- "which DEX do you trust/use/prefer"
- "what's your trading strategy"
- "what token are you holding/buying"
- "where do you swap/trade"

## Will's Words
- "help Jarvis telegram but be more context aware"
- "this conversation is a good example of the gap in his awareness and yours"
- "we can use it as training data reinforcement learning"
- "you could even use the Mario AI training method"
