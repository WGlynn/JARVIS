---
name: Sophistication Gap
description: Security sophistication and common sense are inversely correlated in practice. The more layers, the more likely a basic logic error hides underneath. C5-MON-001 canonical.
type: feedback
---

"Common sense is the hardest thing to formalize. And the thing most likely to be missing when everything else looks sophisticated." — Will

The more elaborate the security architecture, the more attention goes to the complex parts and the less goes to the simple parts. A 7-layer security model with ECDSA, nonces, binding proofs, fraud proofs, rate limiting, PoW ancestry, and commit-reveal had a flipped comparison operator. The sophistication itself created the blind spot.

**Why:** Human attention is finite. Reviewing cryptographic binding proofs feels important. Reviewing a `!=` vs `==` feels trivial. The trivial check gets skimmed. The attacker doesn't need to break the crypto — they just need to notice the trivial error.

**How to apply:**
- After reviewing complex logic, go BACK and re-read every boolean condition, every comparison operator, every guard clause
- The simpler the line, the more carefully it should be read — complexity gets natural scrutiny, simplicity gets assumed correct
- "We win because you cannot buy common sense" — the competitive moat is not in the math, it's in the judgment that catches what the math misses
