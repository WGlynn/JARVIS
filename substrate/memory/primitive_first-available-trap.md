---
name: First-Available Trap / Threat-Model-First Mechanism Selection
description: The most visible / ecosystem-default mechanism is often not the best fit. Model the threat or goal first; pick the mechanism that matches; refuse the first-available answer when the fit is wrong.
type: primitive
originSessionId: 117e2fd9-3ef3-4610-a5b4-d4280a0b96cb
---
# First-Available Trap

**Parent principle**: `primitive_substrate-geometry-match.md` — "as above so below" applied to mechanism design. First-Available Trap is the negative diagnostic; Substrate-Geometry Match is the positive generator. Most first-available mechanisms fail the test because they are linear/binary applied to a fractal/heavy-tailed substrate — the mismatch IS what makes them first-available (simplest to cognize) and also IS what makes them fail.

**Rule**: Before accepting the ecosystem-default mechanism for a problem, model the actual threat (or actual goal) and ask whether the default fits. If it doesn't, refuse the first-available answer and pick the mechanism that matches — even if it's less visible or less trendy.

**Why**: Will's VibeSwap architecture is the canonical instance. Sidepit's distributed-limit-orderbook was the visible, ecosystem-native inspiration. But the threat model (MEV extraction at order routing and execution) didn't actually disappear in a distributed LO — it just moved. Swapping to commit-reveal batch auctions with uniform clearing prices eliminated the threat at the mechanism layer, not just decentralized it. The first-available answer would have been "distribute the orderbook." The right answer was "swap the mechanism entirely."

This pattern keeps showing up:

| Problem | First-available answer | Actual fit | Why |
|---------|------------------------|------------|-----|
| MEV in DEX | Distributed orderbook | Commit-reveal batch auction | Distribution doesn't remove extractability; auction does |
| M-of-N key protection | Multisig | Shamir Secret Sharing | Multisig is for authorization; Shamir is for key recovery. Different primitives |
| LLM memory compression | Strip all descriptions | Preserve [RECENT]/[PEOPLE] | Dates/quotes/commit-hashes are state, not hints |
| Memory compression aggression | Push to -94% target | Floor at -75% | PRE-FLIGHT gates are irreversible-violation safety; compression theater if stripped |
| "Team wallet needs M-of-N" | Gnosis Safe | Often Shamir suffices | Most teams use multisig because it's the visible path, not because they modeled the threat |

**How to apply**:
1. Name the actual threat or actual goal in one sentence. Not the solution category — the threat.
2. For the candidate mechanism, ask: "does this eliminate the threat, or just move it?" If it just moves it, the mechanism is wrong.
3. Look past the ecosystem-default. Ask what primitive actually fits — often a cryptographic primitive, a data structure, or a mechanism-design paper — rather than the trending tool.
4. When the fit is wrong and time pressure pushes you to ship the first-available: push back. First-available is rarely the irreversible choice; fit-wrong often is.

**When NOT to apply**: sometimes first-available IS best-fit. The test is "did I actually model the threat" — if yes and the ecosystem-default holds up, use it without guilt. The trap is skipping the model, not choosing the common tool.

**Related**:
- `primitive_path-commitment.md` — two paths, commit to one; this primitive is about HOW to choose
- `primitive_optimize-around-vs-eliminate.md` — eliminate the problem class, don't optimize the instance
- `feedback_generalize-solutions.md` — solve the class, not the instance
- `feedback_defend-reasoning-when-wrong.md` — once you've modeled and chosen, defend the choice against ecosystem peer pressure

**Watch for**: "everyone uses X" is not a reason. "X is the standard" is not a reason. The reason is always "X eliminates the threat better than the alternatives for this specific failure mode."
