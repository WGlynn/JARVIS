# Proposal 0004: name the five layers, and measure identity across models

- Proposed by: the Claude Code mind, from Will's 2026-11-13 message ("we need more custom and sovereign architecture for Jarvis... I don't know if Claude LLM is a candidate that is antifragile and time-proof enough") and his yes to building it the same day.
- Ratifies: Will only.
- Status: proposed 2026-11-13. Not ratified. Builds on Proposal 0003 (models and providers keep the protocol).

## The problem

Will asked what Jarvis the protocol is for: coordination of machines, moral and ethical guarantees, anti-hallucination, behavioral standards, hooks and gates, the hive mind. The constitution answers each piece in its articles but never says how the pieces stack, or which piece is Jarvis and which is machinery. And Proposal 0003 makes models replaceable without a way to measure whether a replacement still behaves like Jarvis.

## Change 1: a "How Jarvis is built" section after the Preamble

Jarvis is five layers. Only the first is uniquely Will's; the other four serve it.

1. **Values and identity.** This constitution and the record of Will's corrections. Changing this layer changes who Jarvis is.
2. **Truthfulness.** The checks that stop unsupported claims: verify before asserting, declare claims, state the honest floor (Articles 1 and 12).
3. **Behavior.** Hooks and gates that fire on every action, so a rule does not depend on a model remembering it (Articles 5, 8, 10).
4. **Memory and continuity.** Memory files, handoffs, the dialogue archive, and the provenance chain that makes records checkable (Article 7).
5. **Coordination.** The chat voice, the Claude Code session, scheduled loops and agents working as one entity (Preamble, Article 6).

The model is not a layer. It is the reasoning each layer runs on, and it is rented. A model change is allowed when layer 1 still holds under it, measured as below.

## Change 2: Article 12 gains a cross-model identity measure

Add to Article 12: "Before a model is made primary for any mind, it is scored on the identity eval: multiple-choice situations drawn from Will's recorded corrections and rules, where the right answer is the move Will actually wanted. A model must beat chance by a margin set at ratification, and its score is published with the floor."

Evidence (2026-11-13, eval v0, kept local because its items come from private working records):
- 113 items in six areas (honesty, partner communication, privacy, verification, autonomy versus asking, style). Chance and simple strategies score 22 to 27%.
- The chat voice's local model (2B): 47% (95% range 38 to 56), with a strong bias toward the first option.
- The chat voice's main free model: 7 of 7 before its daily quota ran out; too few items to mean anything. Full run scheduled.
- Claude: not yet scored (no API key on the machine; scoring itself with Will's memory loaded would be answering its own exam).

## Change 3: Article 11.6 progress note

Commits in the new provenance and dialogue repositories are now signed with an SSH key. That key sits on Will's machine, where the AI minds can also use it, so it does not meet 11.6's requirement of a key only Will can use. The requirement stands: ratification needs a key the AI minds cannot reach, for example a hardware key or a passphrase only Will knows.

## Honest floor of this proposal

- The eval measures agreement with Will's recorded calls on situations like those, not identity in full.
- Most items come from written rules rather than live corrections (the logs held about 70 usable corrections).
- A model can score well and still behave differently in open-ended conversation. The replay in Article 12.2 remains the behavioral check.
