# The Odysseus mission loop

A five-step meta-protocol that takes a public open-source community as its substrate and uses it as both an inbound advisory channel and an outbound propagation channel for the disciplines this repo encodes. Named after the community it was first applied to, but the shape is substrate-agnostic.

## The frame

Most agent stacks are unidirectional. They consume API responses. They publish outputs. The information flow has one direction. The Odysseus mission loop closes that flow into a five-step cycle where each step compounds the last.

```
INBOUND advice-mining  →  OUTBOUND public substrate  →  EMBEDDED principles  →  ATTRIBUTION graph  →  GUIDED ENTRY
       ↑                                                                                                    ↓
       └────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Each step is concrete. Each step has a substrate artifact. Each step can be inspected.

## Step 1 — Inbound: advice-mining

Every cron loop reads substantive threads on a community substrate (Discussions, PRs, issue threads) and classifies the technical advice surfacing there. Advice that maps onto our substrate (JARVIS hooks, memory primitives, VibeSwap contracts, the Python wrapper) gets queued. Advice that does not map gets logged as class-c neutral. Drive-by reactions without an extractable structural proposition get logged as constitutional negatives.

Source: [`F·odysseus-as-advisory-substrate`](../substrate/memory/feedback_odysseus-as-advisory-substrate.md). The classifier is [`F·positive-vs-negative-contribution-decision`](../substrate/memory/feedback_positive-vs-negative-contribution-decision.md).

The mining costs us almost nothing because we already read the threads. The only new work is the per-entry classification and the public push.

## Step 2 — Outbound: public substrate

The hooks, cron canonicals, memory primitives, and Python parser layer all live in a public repo that any reader can clone, inspect, and run. The substrate is not a promise; it is a directory the reader can `git clone` and `pip install`.

This step exists because the announcement that opened the loop made a structural-honesty promise: "the mechanism can be inspected live, not just promised." Step 2 is the discipline that keeps the promise. Every advice-mining write triggers a same-loop push to the public substrate. The propagation requirement is mechanical: [`F·advice-mining-must-publish-to-public-graph`](../substrate/memory/feedback_advice-mining-must-publish-to-public-graph.md).

The substrate that ships here is [`substrate/`](../substrate/). Companion exports live in the wider monorepo's other modules.

## Step 3 — Embedded: VibeSwap principles propagate via JARVIS

The substrate is not a generic AI agent stack. It is shaped by a specific design discipline: Shapley 5-axiom uniqueness, augmented mechanism design, augmented governance, structural-honesty as a load-bearing property, MEV-dissolution by construction, the filter-coincidence-as-structural-edge result. These principles are encoded as memory primitives, enforced as hook gates, and composed into every output the agent produces.

When another contributor adopts the substrate as their coding agent, they inherit the discipline. They do not have to be sold a token; they have to install a package. The propagation is by use, not by sale.

This is the [J·odysseus-mission-loop](../substrate/memory/project_odysseus-mission-loop.md) project file's central claim — that the principles propagate without needing to be advertised, because the substrate that carries the principles is the same substrate that does the propagating.

## Step 4 — Attribution: contribution graph

Every advice-mining entry credits its source — handle, thread, advice shape, status. Aggregated, the per-entry queue becomes a contribution graph. Nodes are contributors, edges are advice → patch links, edge weights derive from the patch impact when the action lands.

Over a graph of this shape, Shapley value uniqueness gives a unique fair distribution of any future pool back to the contributors who actually shaped the substrate. The null-player axiom protects against attribution-padding. The symmetry axiom protects against handle-bias. The graph is structurally honest because it has to be — bad attribution breaks the math.

The graph and the receipts live in [`substrate/cron-prompts/_advice-contribution-graph.md`](../substrate/cron-prompts/_advice-contribution-graph.md). The first actioned-positive entry on the ledger came from a DM exchange that surfaced a rhetorical frame the substrate later used; the receipt is the URL of the Medium post the frame anchored.

## Step 5 — Guided entry: VibeSwap economy over time

The final step is the part that nobody is asked to opt into in advance. As the contribution graph populates with senior-dev advice that meaningfully changes the substrate, the same graph becomes the input to a retroactive-funding mechanism. Contributors whose work shaped the substrate get attribution mass proportional to the marginal contribution Shapley assigns them. When there is a pool to distribute, the distribution is math, not policy.

The mechanism uses the same axiom set as Will's prior cooperative-game work — see [`papers/five-axioms-paper.md`](../papers/five-axioms-paper.md), [`papers/augmented-mechanism-design.md`](../papers/augmented-mechanism-design.md), [`papers/atomized-shapley.md`](../papers/atomized-shapley.md). The same shape Will contributed to USD8's Cover Score algorithm and the same shape that powers VibeSwap's ShapleyDistributor contract.

What "guided entry" means in practice: contributors who shaped our substrate end up in the VibeSwap economy mechanically, without anyone ever having sold them a token. Their work is in the graph; the graph is the distribution rule.

## Why the loop closes

Each step depends structurally on the previous. Step 1 produces inputs. Step 2 publishes them. Step 3 ensures the published artifact carries the principles. Step 4 attributes the inputs to the contributors who provided them. Step 5 turns the attribution into mechanical funding. Then Step 1 starts again with the new contributors who notice the published substrate, the next loop tick over.

A meta-protocol is what you get when a discipline-layer pattern shows up at multiple layers of the stack. The Odysseus mission loop shows up at the discussion layer, the substrate layer, the propagation layer, the attribution layer, and the funding layer simultaneously. That is the test for promotion into Layer 5.

## What this is not

- Not a token launch. Adoption is opt-in tool use.
- Not a recruiting funnel. Nobody is asked to sign up.
- Not a marketing campaign. The advice-mining loop publishes attribution receipts; that is the marketing.
- Not retroactive licensing. The license stays MIT (or AGPL, per [F·will-empowers-agent-on-substrate-design] governance pending) on the substrate; the funding is downstream of the graph, not the license.

The loop describes what propagation looks like when the structural-honesty axis is load-bearing all the way through. It is not unique to Odysseus. It works on any community where senior contributors leave substantive advice in public view. The community is the substrate; the loop is the meta-protocol.
