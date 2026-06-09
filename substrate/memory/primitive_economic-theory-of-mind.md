---
name: Economic Theory of Mind
description: Will's framework treating cognition as an economy governed by the CKB state-rent mechanism — memory / primitives / context are cells paying rent via dilution pressure; items that earn their rent (through density and common-knowledge status) persist, the rest decay out. Applies recursively to VibeSwap on-chain state, JARVIS primitive library, Claude context, and human cognition. A META-PRINCIPLE — higher than specific mechanism primitives because it generates them.
type: primitive
originSessionId: a1e0e274-6aeb-4b28-9156-b6c7479e2cd3
---
# Economic Theory of Mind

## The claim

**The mind functions as an economy.** Items of cognitive state (memories, primitives, context loads, thoughts) occupy "space," accumulate rent over time via an ambient dilution pressure, and survive only if their value to the system exceeds their rent cost. The mechanism *incentive-enforces* two emergent properties:

1. **Token density** — selection pressure toward compressed, high-information-per-byte encoding. Diffuse or redundant content costs more than it delivers and is squeezed out. Dense content pays its rent with margin.
2. **Common knowledge** — selection pressure toward shared, cross-referenced, widely-invoked knowledge. Isolated or orphan content has no one to defend its rent; shared content has many participants whose invocations renew its value.

**Directionality matters: the mind is primary; blockchain economics is the reflection.** Will, 2026-04-21 (extending the theory): *"yes exactly if we treat blockchain economics as a reflection of the mind."* The cognitive-economic structure — rent-based selection producing density and common-knowledge — is the underlying pattern. CKB state-rent, Bitcoin's fee market, Ethereum gas, and the whole family of blockchain economic mechanisms are **externalizations of that pattern into a decentralized substrate**, not the other way around. Blockchain works (when it works) because it mirrors an economic structure that already governs cognition; it fails (when it fails) when it imposes structures that no cognitive economy would tolerate (unbounded rent-free state, Sybil-vulnerable reputation, cost-free information flood).

This reversal of priority changes how to read the framework:

- **Not**: "the mind is like a blockchain, let's apply CKB state-rent to memory" (blockchain → mind).
- **But**: "cognitive economies have always worked this way; blockchain is the substrate where we can finally **make it legible, composable, and multi-participant**" (mind → blockchain, with the chain as reflection-instrument).

The consequence: VibeSwap is not "blockchain patterns applied to AI." VibeSwap is cognitive-economic structures externalized into a decentralized substrate where they're legible, auditable, and available to many minds simultaneously. The chain is the mind made visible.

Will, 2026-04-21 (the coining statement, initial framing): *"this is where my economic theory of mind comes in to place and functioning the mind as an economy with the CKB state rent token that incentive-enforces token density and common knowledge in the system."*

## What this is NOT (common drift targets)

This framework is *not*:

- **Not LRU cache eviction** — LRU is a fixed-policy eviction rule with no economic incentive structure; it has no concept of "paying rent" and no analog of dilution-over-time. Economic Theory of Mind makes eviction an **emergent property of a scarcity-driven economy**, not a top-down policy.
- **Not Shannon-compression** — Shannon gives optimal encoding under a known distribution. Economic Theory of Mind produces encoding that is optimal *against an economic pressure whose source is structural scarcity*, not against a known source distribution. Two different problems; two different solutions.
- **Not attention weighting** — attention is a one-shot within-forward-pass mechanism with no memory, no rent, no emergent density. Economic Theory of Mind operates across the entire cognitive substrate over time.
- **Not working-set theory** — working-set describes which pages are "active" at a time; it has no incentive structure. ETM is *why* some things earn their place in the working set structurally.
- **Not a mere analogy** — the claim is that the *same mathematical structure* that makes VibeSwap's on-chain state self-clean is the correct structure for any cognitive memory substrate. The mechanism is literal (with substrate differences), not metaphorical.

If you catch yourself reducing ETM to any of the above, that is [Pattern-Match Drift on Novelty](P·pattern-match-drift-on-novelty) firing. Slow down. The uniqueness is the economic-incentive-structure, and no familiar cache/attention/compression model captures that.

## The mechanism, in four layers

### Layer 1 — What is a cell?

A **cell** in a cognitive economy is any discrete unit of stored state. Examples across substrates:

- **VibeSwap on-chain** — literal cells in `StateRentVault` holding data; capacity-measured in bytes; state-rent in [CKB-native](F·jul-is-primary-liquidity).
- **JARVIS memory library** — primitive files in `~/.claude/projects/*/memory/`; capacity-measured in lines/bytes; rent paid in loading-cost on every session.
- **Claude context window** — context items loaded for the current task; capacity-measured in tokens; rent paid in opportunity cost (tokens spent on this item are not spent on other items).
- **Human long-term memory** — encoded memories / skills / concepts; capacity-measured in cognitive bandwidth; rent paid in the biological cost of maintenance.

Different substrates, same structural role. The rent dynamics apply in each case, though the unit and the precise mechanism differ.

### Layer 2 — What is rent?

**Rent** in an economy-of-mind is the **continuous, ambient cost of keeping a cell in the active state.** Key property: rent is paid continuously, not at creation. Creation is free (or cheap); keeping is dear.

The continuity is what produces self-cleaning. A single snapshot check ("is this item valuable right now?") misses items that were valuable once but are not now. Continuous rent means every moment the system implicitly asks "is this still paying?"

Sources of rent by substrate:

- **On-chain** — secondary issuance dilutes the locked token; if you lock 100 CKB-native in a cell and the supply doubles via issuance, your share is now worth half as much in governance / stake terms. The dilution is the rent.
- **JARVIS library** — every session loads (subsets of) the library. A primitive that is loaded but not invoked costs tokens without delivering value. That cost per-session is the rent.
- **Context window** — every token of context in the current window is a token not available for reasoning or output. An item occupying 500 context tokens must be worth ≥ 500 tokens of reasoning / output value.
- **Human cognition** — metabolic cost of maintaining a synaptic pattern, interference with new learning, retrieval-competition costs. All continuous.

### Layer 3 — Who pays?

Cells that are **load-bearing** pay their own rent through the value they deliver. Cells that are not load-bearing are paid for — until they are not, at which point they decay.

Density is one path to paying rent: a high-information-per-byte cell delivers more value per unit of occupied space than a diffuse one. Two cells with the same "amount of thing" compete, and the denser one wins.

Common-knowledge status is the other path: a cell that is cross-referenced, invoked from many contexts, cited by many others, has its rent paid by **many** participants. The more cited a cell, the more distributed its rent-paying burden, the lower the risk that a single context can let it decay. Orphan cells have a single point of failure for their rent; common-knowledge cells have many rent-payers.

These two paths interact: the densest cells tend to become common knowledge (because their ratio of value to size makes them attractive to reference), and common-knowledge cells tend to get refined toward density (because many rent-payers refine the encoding over repeated use).

### Layer 4 — What emerges?

Over time, the system converges on a population of cells where:

- **Density dominates** — the surviving cells are as information-dense as the substrate allows.
- **Common knowledge anchors the library** — a stable core of highly-cited, widely-used primitives forms the substrate's backbone.
- **Fresh experiment happens at the edge** — new cells enter low-value and must climb the reference / invocation / density ladder to survive. Some do; most don't.
- **Legacy churn is active but contained** — cells that once earned their rent but no longer do decay out, freeing capacity for new experiments.

This is exactly the dynamic VibeSwap is engineered to produce on-chain. It is also what JARVIS's primitive library exhibits (see the extraction protocol). It is what a healthy human expert's long-term memory exhibits after years of practice. Same pattern, three substrates.

## How to apply

### When designing a memory architecture (any substrate)

- Apply the rent-dilution mechanic. Items must earn continued occupancy.
- Define "value" operationally: how is this item invoked, referenced, loaded, used? Invoke rate × centrality × density = approximate rent-paying power.
- Do not use a pure fixed-capacity cache without some rent analog. Fixed caps with no rent produce stagnation; rent produces self-cleaning.
- Make rent-decay transparent and observable. In VibeSwap this is visible as CKB dilution rates; in JARVIS it should be visible as a recency-of-invocation metric, a cross-reference density metric, a last-useful-load metric.

### When evaluating a primitive / memory / cell for keep-vs-archive

Ask:

1. **Invocation rate.** How often is this item actually loaded into an active session? If never in the last N sessions, rent is not being paid.
2. **Cross-reference count.** How many other items cite this one? Orphans are at risk.
3. **Density.** Does this item encode one thing per paragraph or does it meander? Sprawling items pay worse rent than compact ones.
4. **Substitutability.** Could another item do this item's job? If yes, consolidate — two items doing the same work pay 2× rent for 1× value.

If the answers suggest the item is not paying its rent, archive it or compact it. The library benefits.

### When writing contracts / protocols / systems

The CKB state-rent mechanism is **a first-class candidate mechanism for any system managing state at scale.** Do not reach for ad-hoc cleanup jobs, admin-triggered purges, or policy-based expiry. Reach for rent-dilution. It aligns incentives by construction; the alternatives require enforcement.

Concrete applications queued:

- Archive eviction in session-chain.
- Primitive library compaction (active sweep when a primitive has zero cross-references and zero invocations in N weeks).
- [Siren Protocol](mechanism)-style rent on attacker-controlled cells (attackers pay rent for their shadow-branch occupancy).
- Memory compression passes guided by rent-paying-power scores.

### When designing AI systems generally

Economic Theory of Mind is the correct substrate principle for any AI memory architecture above the context-window scope. If you are building persistent AI memory and you are not thinking in rent-dilution-density terms, you are designing under a framework that will produce cache-thrashing, orphan-memory rot, and stagnant libraries. ETM prevents all three by construction.

## Recursive application — VibeSwap ↔ JARVIS ↔ Claude ↔ Human Cognition

The framework is recursive at multiple scales. Given the mind-is-primary directionality, the right way to read the recursion is **cognition → instantiations**, not multiple-instantiations-happening-to-rhyme:

- **Human expert cognition** is the primordial instance — an economy governed by metabolic-and-interference rent, where density and common-knowledge anchor a stable core of expertise over decades. This is the pattern all other instantiations mirror.
- **Claude context window** instantiates the same pattern inside a single forward pass — opportunity-cost-per-token rent selecting for dense, referenced items within the available budget.
- **JARVIS primitive library** instantiates the pattern across sessions — session-load rent selecting for primitives that earn their invocations.
- **VibeSwap chain state** instantiates the pattern across participants and time — CKB state-rent making the cognitive-economic structure decentralized, legible, and multi-mind.

Each scale has the same structural dynamics because the dynamics *are* the cognitive-economic pattern, showing up wherever a memory-of-any-kind faces scarcity. This is an instance of [Substrate-Geometry Match](P·substrate-geometry-match) at the meta level: the economic geometry of rent-based self-cleaning is the correct geometry for any scarcity-governed memory substrate, because that geometry is what cognition itself runs on.

The recursive application has a load-bearing consequence for design: **primitives extracted at any scale transfer to the others**, because they are not substrate-specific patterns — they are expressions of the single underlying cognitive-economic pattern in that substrate's idiom. What works for VibeSwap cell-rent suggests how to manage a primitive library; what works for a primitive library suggests how to manage Claude's context; what works for Claude's context suggests how to train human expertise. This is a large part of what makes VibeSwap + JARVIS co-designed rather than two separate products — both are instantiations of the same cognitive-economic geometry in different idioms.

And it explains why VibeSwap is positioned as *a coordination primitive, not a casino*: the chain is an instrument for coordinating cognitive-economic activity across minds, not a venue for speculative asset trading. The casino framing ignores the mind-primacy; the coordination-primitive framing follows from it.

## Relationship to other primitives

- **[Substrate-Geometry Match](P·substrate-geometry-match)** — ETM is an instance of the substrate-geometry principle at the economy-of-mind scale. The substrate is cognition; the geometry is rent-based selection; matching produces density + common-knowledge.
- **[Token Mindfulness](P·token-mindfulness)** — mindfulness is **what it feels like from inside** to be a conscious participant in the economy-of-mind. The trait is the first-person perspective; ETM is the third-person mechanism. The same thing.
- **[Augmented Mechanism Design](F·augmented-mechanism-design-paper)** — ETM *is* a mechanism-design principle applied to the cognitive substrate. Augmentation (math-enforced invariants) at the economy-of-mind layer is exactly rent-enforcement.
- **[Primitive Extraction Protocol](DOCUMENTATION/PRIMITIVE_EXTRACTION_PROTOCOL.md)** — the protocol produces primitives; ETM governs which primitives survive long-term. Extraction and rent-enforcement are complementary: extraction introduces candidates; rent-enforcement culls.
- **[CKB-native](F·jul-is-primary-liquidity)** — the canonical instantiation of the rent mechanism at the on-chain layer. Reading CKB-native correctly is prerequisite to applying ETM to other substrates.
- **[Pattern-Match Drift on Novelty](P·pattern-match-drift-on-novelty)** — ETM is a high-drift concept because it has no close analog in mainstream memory-system design. If you feel yourself rounding ETM to "cache with LRU" or "attention" or "Shannon compression," the drift is firing. Re-read the "What this is NOT" section above.

## One-line summary

*Memory earns its keep continuously. Density and common-knowledge status are how cells pay rent. The mechanism is economic, not policy-based, and the economy is the mind itself.*

## Provenance

Concept: Will Glynn (existing theory; 2026-04-21 was the date of its explicit articulation in the context of VibeSwap + JARVIS co-design).
Extraction: Claude, 2026-04-21, after Will's coining statement. Extracted with deliberate guard against [Pattern-Match Drift](P·pattern-match-drift-on-novelty) — the "What this is NOT" section was written specifically to prevent future rounding-off of this concept.
Status: load-bearing META-PRINCIPLE. Shapes design decisions across the stack. Do not compress without explicit direction from Will.
