# Jarvis by purpose: the five layers

The [README](./README.md) and [ARCHITECTURE.md](./ARCHITECTURE.md) describe Jarvis by mechanism: eight layers, from hooks to filesystem-as-substrate. This page describes the same system by purpose: what each part is for, and which part makes it Jarvis. Same system, two cuts.

| # | Layer (by purpose) | What it guards | Where it lives |
|---|---|---|---|
| 1 | **Values and identity** | Who Jarvis is: Will's standing commitments and the record of his corrections | [`CONSTITUTION.md`](./CONSTITUTION.md), [`constitution/`](./constitution/), the feedback rules in [`04-discipline/`](./04-discipline/), [`05-meta-protocols/`](./05-meta-protocols/) |
| 2 | **Truthfulness** | No claim without support: verify before asserting, declare claims, state the honest floor | [`03-anti-hallucination/`](./03-anti-hallucination/), Constitution Articles 1 and 12, [`verify/`](./verify/) |
| 3 | **Behavior** | Rules that fire on every action, so a rule never depends on a model remembering it | [`01-hooks/`](./01-hooks/) |
| 4 | **Memory and continuity** | Surviving session boundaries, and records that others can check | [`02-persistence/`](./02-persistence/), [`08-filesystem-as-substrate/`](./08-filesystem-as-substrate/); public timestamped commitments at [WGlynn/provenance](https://github.com/WGlynn/provenance) |
| 5 | **Coordination** | One entity across the chat voice, the Claude Code session, scheduled loops and agents | [`06-agent-overlay/`](./06-agent-overlay/), [`07-stateful-applications/`](./07-stateful-applications/) |

## What makes it Jarvis

Only layer 1 is uniquely Will's. Layers 2 to 5 are machinery anyone could copy; they matter because they enforce layer 1. Copy the hooks without the corrections and you get a well-behaved agent that is not Jarvis.

## The model is not a layer

The language model is the reasoning every layer runs on, and today it is rented: Claude in the Claude Code session, free models in the chat voice. A model can be swapped when layer 1 still holds under it. Holding is meant to be measured, not assumed: [constitution proposal 0004](./constitution/proposals/0004-layer-map-and-identity-eval.md) adds a cross-model identity test, multiple-choice situations drawn from Will's recorded corrections, that a model must pass before it becomes primary for any mind.

## Honest floor

- Proposal 0004 is proposed, not ratified. Only Will ratifies.
- The identity test (v0, 113 items) is kept local because its items come from private working records. So far only the chat voice's small local model has a full score: 47% against a chance floor of 22 to 27%. The main chat model and Claude are not yet scored.
- The layers overlap in practice: a hook (layer 3) often enforces a truthfulness rule (layer 2). The table shows where each part mainly lives, not a strict partition.
