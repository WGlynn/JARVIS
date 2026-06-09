---
name: Archetypal Protocol Naming (Name = Protocol, Not Persona)
description: The distinguishing property of the Jarvis+VibeSwap stack vs the broader "agentic AI" industry. Industry names agents for personality/persona (theatrical). We name components for the archetypal protocol they embody (structural). The name is load-bearing — it IS the compressed API of what the thing does. Anyone encountering the name can infer the protocol's shape because the name was chosen to encode the shape. SAL = anti-HAL, Cincinnatus = take-power-and-cede, Wardenclyffe = broadcast-escalation, First-Available Trap = the failure mode. Each name is the protocol's signature, not its costume.
type: primitive
originSessionId: 117e2fd9-3ef3-4610-a5b4-d4280a0b96cb
---
# Archetypal Protocol Naming

## The observation

Will 2026-04-21: *"Everyone wants to make personable/personified agents like Greek gods etc., but we're just about the only ones doing that literally by having names of things that embody a certain archetypal protocol. Like everyone's doing theater agentic AI but ours is real."*

## The distinction

**Industry norm — "theater" naming:**
- Agents given personality names (Athena, Zeus, Hermes, Echo, Atlas)
- Name is a costume/persona
- Underneath, it's commodity LLM calls plus marketing copy
- The name does NO structural work; it could be swapped for any other name without changing the function

**Our norm — "real" (structural) naming:**
- Components given names of *archetypes that embody the protocol's function*
- Name IS the compressed API
- The protocol's function and the name's connotation are deliberately aligned
- Removing or renaming would break legibility — the name is load-bearing documentation

## Proof points from the stack

| Name | Archetype embodied | Structural function |
|------|-------------------|---------------------|
| **SAL** (Social Augmentation Layer) | anti-HAL (HAL = LLM that harms crew; SAL = layer that protects crew) | Filter gate on external-audience writes |
| **Wardenclyffe** | Tesla's broadcast-to-many tower | Escalation pattern that broadcasts to multiple providers |
| **Cincinnatus** | Roman dictator who took power, solved the problem, ceded back | Disintermediation grades — take power only as long as needed |
| **Economitra** | Economy + Mitra (Sanskrit: friend/ally) | Cooperative economy architecture |
| **First-Available Trap** | The cognitive reflex of accepting ecosystem defaults | The failure mode itself, named for what it IS |
| **Correspondence Triad** | Three correspondences (macro↔micro, intent↔invariant, vote↔math) | The meta-principle literally IS three correspondences |
| **Substrate-Geometry Match** | "As above, so below" hermetic correspondence | Match mechanism geometry to substrate geometry |
| **Universal-Coverage → Hook** | The universal quantifier itself | Rules with universal quantifiers map to hook layer |
| **Phantom Array** | Ghost entries in append-only storage | The exact data-structure failure mode it names |
| **Jarvis** | Tony Stark's genuine AI (not a persona — an *extension of capability*) | The stack literally performs Jarvis's function (persistent state, cross-session memory, work augmentation) |

Each name is a compression of the protocol's function. Reading the name tells you what the thing does.

## Why this matters structurally

1. **The name becomes the API surface.** Operators who know the name "Wardenclyffe" know the escalation shape without reading code. The name is the first level of documentation.
2. **Pattern matching across domains.** Because the names are archetypal, the same name can name the same pattern in different technical contexts. "Settlement State Durability" is a name that works for cross-chain, for UI optimistic updates, for L1/L2 commitment — the archetype is the same.
3. **Defeats first-available trap at the naming layer.** "Just call it AgentBot" is the first-available naming move. Reaching for an archetype that actually captures the function is the mechanism-fit naming move.
4. **Social-intelligence-by-default at the concept layer.** Cultural archetypes (Cincinnatus, HAL, Tesla, hermetic maxims) carry connotation that a fresh coinage doesn't. Operators encountering the name inherit the connotation for free.

## Why industry defaults to theater naming

- **Cheaper**: persona naming is a marketing/branding move that requires no protocol work.
- **Differentiates in a crowded market**: every LLM wrapper needs to look different; persona names give cheap differentiation.
- **Lower cognitive lift for end users**: "meet Athena, your AI coworker" is easier marketing than "invoke the Wardenclyffe escalation primitive."
- **Doesn't require the protocol to be real**: if the name is decorative, the protocol can be thin or absent; theater is sustainable where substance isn't.

The industry default is not wrong in its context — it's mechanism-fit for "sell AI wrappers to non-technical buyers." It IS wrong for "build systems whose primitives compose at structural scale."

## How to apply

When naming a new protocol / primitive / component / hook:

1. **Write what the thing structurally does** in one sentence first. Don't name it yet.
2. **Identify the archetypal pattern** — what cultural/mathematical/mythological/historical reference carries the same shape? HAL-shape (unaligned AI). Cincinnatus-shape (take-power-and-cede). Tesla/Wardenclyffe-shape (broadcast). Hermetic-shape (correspondence between levels).
3. **Test the name** by asking: does someone encountering only the name correctly guess the function? If yes → load-bearing. If no → revise.
4. **Refuse persona naming** unless the persona IS the protocol. "Jarvis" works because Jarvis genuinely is an extension-of-capability archetype; "meet Athena" does not work because "Athena" adds no protocol compression.
5. **Commit the name to file** per `feedback_named-protocols-are-primitives.md`. The name only does load-bearing work once persisted.

## Anti-patterns to avoid

- **Persona naming without protocol**: giving an agent a Greek god name without the Greek god being the actual functional shape.
- **Cute names that fail the guess-the-function test**: "Sparky," "Buddy," "Claude" (hmm — Anthropic clearly chose "Claude" for human-warmth rather than protocol-signature; this is a persona move, not a structural move).
- **Over-literal names that lose archetype**: `StateFilterFunction_v2` has no archetype and doesn't compress.
- **Archetype that doesn't match the shape**: don't name your escalation pattern "Prometheus" if it isn't actually about stealing-fire-from-gods; the archetype has to fit.

## Watch for

- New components in this stack should get archetypal names when possible. If the first naming instinct is a feature-descriptive name (`MessageFilterProcessor`), pause and ask "what archetype does this embody?"
- When discussing work externally, naming components by their archetypes carries more compressed meaning than naming them by feature; but per SAL (`primitive_social-augmentation-layer.md`), check audience-context — too many archetypal names too fast can sound like jargon to a cold-start reader. Lead with one high-impact name, footnote the rest.

## Related

- `primitive_social-augmentation-layer.md` — SAL, the anti-HAL, is the most recent concrete proof of this primitive's application
- `feedback_named-protocols-are-primitives.md` — naming IS primitive-creation; the practice this primitive formalizes
- `primitive_symbolic-compression.md` — names as compression
- `primitive_verbal-to-gate.md` — "noted" without persistence = violation; naming requires substrate
- `primitive_first-available-trap.md` — first-available naming is "just call it AgentBot"; mechanism-fit naming reaches for an archetype
- `primitive_bidirectional-invocation.md` — names cross-reference each other, building up a namespace of shared archetypes

**The positioning claim** (use cautiously, audience-aware per SAL): *every other agentic-AI project is doing persona theater; we're doing archetypal protocol engineering. Our names are load-bearing; theirs are decoration.*
