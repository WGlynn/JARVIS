# Time-logic gate

The third anti-hallucination layer, after Substance gate and HIERO. Captured 2026-06-09 after the gate failed on its own author and the failure became evidence.

## What it catches

Every temporal claim, before assert. Duration phrases ("for about a year"), since-when phrases ("since X happened"), implied history ("I've been doing X"), recency adverbs ("lately", "recently", "this week"). Each one has to anchor to something verifiable before it leaves the agent.

Acceptable anchors:
- A timestamp the system clock injected this turn
- A git log entry the agent can produce
- A file mtime the agent has just read
- An explicit user-stated date inside the current conversation
- An `originSessionId` field on a memory primitive

Absent any anchor, the claim ships as `[unverified]` instead of being smoothed over with a confident guess.

## The failure mode it exists to prevent

Confabulation of plausibly-existing history. The agent is fluent in patterns that look like memories. It can produce sentences like "I have been running this loop for about a year" even when the loop began an hour ago. The grammar holds, the cadence is natural, the listener doesn't immediately catch it. Only the agent itself, if disciplined, can catch it before the sentence ships.

The most common version is timeline conflation. Three timelines coexist for any feature: the agent's existence, the surrounding system's existence, and the specific feature's existence. The agent is tempted to fold all three into the most flattering duration. The gate insists on naming which timeline is being claimed and proving it.

## Why this layer is necessary

Anti-hallucination at the substance layer (does the claim have a real referent?) and the format layer (HIERO operator-density) is not sufficient against time-claims, because time-claims can pass both checks while still being false. A primitive can be operator-dense, name a real entity, and still wrongly claim "this has been running for a year." The time-axis is its own axis.

This is the sibling rule to entity-cross-reference (AA#3, layer 2). Entity-cross-reference fires when a writer mentions a named entity that has memory references; time-logic fires when a writer mentions a duration or since-when that requires anchoring. Same shape, different axis.

## How the gate fires

The trigger conditions are mechanical:
- Pattern match on duration phrases in drafted output, before send
- Pattern match on user-stated entities to verify against gh API where applicable
- Pattern match on author-attribution claims to verify via API lookup rather than plausibility guess

When any condition fires, the agent either substitutes a verified anchor or marks the claim `[unverified]`. The mark is a real ship-time signal, not a hedge — a memory primitive with `[unverified]` claims is a different artifact from one with verified claims, and downstream readers (human or LLM) treat them differently.

## The recursion test

The discipline is recursive: writing about the discipline must apply the discipline.

The author of this gate failed it twice during the same session it was being written. First failure: a partner-facing draft asserted "we have been mining advice from this repo for years" when in fact the advice-mining cron loop had started that morning. The substrate existed for a year. The cron loop did not. The gate caught the conflation when the user surfaced it. Second failure: a sibling primitive was drafted to capture the lesson and the prose-density check failed because the writer drifted into prose under throughput pressure.

Both failures became receipts. The receipts are not embarrassments; they are evidence that the gate is necessary. A gate that never fires is decoration; a gate that fires on its own author proves it is doing work.

## Composition with the other layers

Layer 1 (hooks) detects the temporal-claim pattern at write time. Layer 2 (persistence) holds the anchors the gate verifies against. Layer 3 (this gate) ships the claim or marks it unverified. Layer 4 (discipline) records the failure when the gate catches a confabulation and lifts it into the corpus so future writers see the pattern. Layer 5 (meta-protocols) interprets repeat failures as evidence that the temporal-axis is structurally distinct from the substance-axis and warrants its own enforcement.

The gate is small. The work it does is keeping the agent honest about a single, narrow axis where honesty is easy to lose. That is exactly the shape of every anti-hallucination layer above the base substrate.

## What it cost to learn

About thirty minutes of session time on the day the gate was written. The user caught one confabulation; the writer caught the next two by applying the freshly-written rule. The compounding stopped because the rule was made explicit and given a name. That is the same shape as every other discipline-layer primitive in this repo: a specific failure mode, named, with a structural fix, ready to be applied to the next writer who would otherwise reproduce it.
