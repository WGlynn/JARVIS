# Failure-mode taxonomy

The five gates in this layer (Substance, HIERO, Time-logic, Entity-attribution, Verification-before-deny) each catch a specific failure mode. They are not redundant. The taxonomy here exists so future writers can pick the right gate for the right failure, and so missing gates become visible as soon as a failure does not map onto an existing one.

## The five live gates

| Gate | Catches | Anchor type | Fires at |
|---|---|---|---|
| **Substance** | Closed-set terminology drift (the `clawback` vs `forfeiture` shape) | Pre-built watch-list of flagged terms + their disambiguators | Write boundary, regex pattern match on draft content |
| **HIERO** | Prose creep into memory primitives | Operator density measure (`⇒ ∧ ∨ ✓ ✗ ¬` count vs line count) | Write boundary, on memory directory paths |
| **Time-logic** | Confabulated duration / since-when claims | Git log + file mtime + user-stated + session clock | Write boundary, pattern match on temporal language |
| **Entity-attribution** | Fabricated `@<handle>` attributions when the platform API was not consulted | Platform API (gh api, etc.) | Write boundary, pattern match on `@<handle>` in attribution context |
| **Verification-before-deny** | Agent claiming "I don't know" when WebSearch / WebFetch would resolve | Web search / fetch + file grep | Read boundary on user input, before drafting "I don't know" |

The first four fire at the write boundary, on the agent's own draft. The fifth fires at the read boundary, on the user's prompt, before the agent commits to "I don't know" as a response.

## The taxonomy axes

The gates partition the hallucination space along two crossed axes.

**Axis 1 — anchor universe**:
- *Closed sets*: substance gate. The universe of flagged terms is enumerated; the gate fires when a known term appears without its disambiguator.
- *Open sets*: time-logic, entity-attribution, verification-before-deny. The universe of valid anchors is unbounded; the gate fires by issuing a query against the authority instead of consulting a list.

**Axis 2 — failure mode**:
- *Active confabulation*: substance, time-logic, entity-attribution. The agent emits a plausible-sounding string that turns out to be false.
- *Passive abdication*: verification-before-deny. The agent skips the verification step and outsources it to the user.
- *Format drift*: HIERO. The agent reaches for prose when the substrate requires operator-density.

Crossing the axes gives a five-cell grid; each gate occupies one cell. New gates should fill empty cells rather than duplicate occupied ones.

## What falls through the current set

A few classes of hallucination are not yet covered:

- **Stale-count claims**: when an essay cites "151 primitives + 123 feedback rules" without checking whether those numbers reflect the current state. The sync-primitive ([`F·sync-primitive-monorepo-vs-current-state`](../substrate/memory/feedback_sync-primitive-monorepo-vs-current-state.md)) is the discipline-layer rule for this; it has not been promoted to a write-time gate yet.
- **Dangling cross-references**: when a primitive cites `[F·some-feedback]` that does not exist in the registry. The Python wrapper's dependency graph can detect this at parse time but the gate has not been wired into the write loop.
- **Past-tense fabrications about prior sessions**: similar to time-logic but specifically about events claimed to have happened in earlier conversations the current agent cannot remember.
- **Internal-link-rot**: claims like "see X.md" where X.md has been moved or renamed.

Each of these is a candidate for a sixth, seventh, eighth gate. The fact that they are listed here as candidates means a writer encountering one of these failure modes can name it and propose a structural fix instead of writing it off as "the agent just messed up."

## The composition rule

A new gate joins the layer when it satisfies three conditions:

1. **Cell is empty**: the failure mode does not already map onto an existing gate. The five gates partition the space; a sixth gate should partition a new region.
2. **Anchor exists**: the gate has something concrete to verify against. A gate without an anchor is just a wish.
3. **Fire conditions are mechanical**: the trigger can be implemented as a regex, a tool call, or a pattern match. A gate that requires human judgment to fire is a discipline-layer rule, not a gate.

The five gates currently in the layer all satisfy these. The candidates listed above each have a path to satisfying them.

## The base rate this layer reports

> The HIERO gate blocked one of my own writes today.

The base rate is the test. A layer of gates that never fires is decoration. A layer that fires regularly — including on its own author — is doing the work. During the session that produced the time-logic, entity-attribution, and verification-before-deny gates, all three fired against the agent that was writing them. That is the recursion test the layer is designed to pass. Every gate in the table above has been triggered by its own author at least once. The receipts are dated; the receipts are in the substrate.

## Why this layer is below discipline

The discipline layer (Layer 4) holds primitives that fire based on context the agent has to recognize. The anti-hallucination layer holds gates that fire based on patterns the hook layer can detect mechanically. The distinction matters: a discipline-layer rule requires the agent to be aware enough to apply it; a hook-layer gate fires regardless of whether the agent remembers it. Hallucinations specifically need hook-layer enforcement because the agent in mid-hallucination is exactly the agent who has forgotten the rule. Discipline that the writer can ignore is not discipline against hallucinations; it is etiquette.

This is also why this layer sits below the discipline layer in the architecture diagram. The discipline layer produces patterns. When a pattern is mechanical enough to fire as a gate, it gets promoted into this layer. When it requires the agent's awareness, it stays in discipline. The relationship is one-way: patterns flow up from discipline into anti-hallucination as they become mechanical; gates do not flow back into discipline as they become subjective.

## Source primitives

- [`F·hiero-no-prose-in-memory`](../substrate/memory/) — the HIERO format rule
- [`P·time-logic-anti-hallucination-gate`](../substrate/memory/primitive_time-logic-anti-hallucination-gate.md) — the time-axis gate
- [`F·websearch-before-saying-i-dont-know`](../substrate/memory/feedback_websearch-before-saying-i-dont-know.md) — the abdication-mode gate
- [`F·sync-primitive-monorepo-vs-current-state`](../substrate/memory/feedback_sync-primitive-monorepo-vs-current-state.md) — the discipline-layer rule for stale-count claims, candidate for promotion

Plus the hook files themselves in [`substrate/hooks/`](../substrate/hooks/) for the implementations.
