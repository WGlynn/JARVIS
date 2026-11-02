# Proposal 0003: make the models and providers keep the protocol

- Proposed by: the Claude Code mind, answering Will (2026-11-01): "then we need something that makes the model and provider align with the protocol"
- Ratifies: Will only
- Status: agreed by Will 2026-11-01 ("agreed"), as a design and build order. **Foundation built 2026-11-01**: every reply leaves the chat voice only as a checked protocol object (`jarvis-bot/src/protocol.js`); acting goes through Will's Claude Code session, with the request queued first and the chat confirmed only from the session's receipt (`session-requests.js`; Will chose: anyone may ask for note and board updates, anything else waits for him); the inbound side for Will's own messages to the session is in `substrate/hooks/inbox-*.py`. **Fact provenance built 2026-11-01** (`jarvis-bot/src/provenance.js`): every stored fact carries where it was learned (DM, group or web, which chat, when, whether public), and a fact learned in a DM is never offered in a group prompt; tests A2 P4 to P11. Not built yet: Lever 1.

## The problem

The constitution shapes the prompt, not the model. The chat voice runs on whichever free model is available, each with its own training and its provider's own rules on top. A model can ignore the prompt, and a provider can block or change a reply. So far "one Jarvis" is a claim about the protocol, not about behavior.

Nothing can force a third-party model or provider to adopt the protocol. What Jarvis controls is which models it uses, what it checks before anything is sent, and, eventually, whose weights it runs. That gives four levers, cheapest first.

## Foundation: the protocol at DNA level (Will, 2026-11-01)

Will: "the protocol needs to be DNA level embedding in the system so that the LLM needs it." The four levers below all sit around the model. This sits underneath it. DNA is not a filter on a cell; it is the template every protein is built from, and the cell can do nothing except by expressing it. The equivalent is a system where the protocol is the only channel through which the model can do anything at all:

- **It speaks only through the protocol.** The model does not send free text to people. It returns a protocol object: the reply, the claims it makes, the actions it says it took, and its sources. Code checks each claim against the turn's event record and the articles, and only a valid object is turned into a message. No protocol, no voice.
- **It acts only through the protocol.** Tools and posting rights are granted by the articles. What the protocol forbids is not refused; it does not exist for the model (no wallet tools under Article 8, no posting in quiet chats under 5.2).
- **It remembers only in the protocol's terms.** Every stored fact carries where it was learned (a DM or a group, which chat, when) and whether it is public. A fact learned in a DM is simply not offered in a group prompt.

In this picture the model is the ribosome that translates, the protocol is the code it translates from, the gates proofread, selection (Lever 3) is natural selection, and fine-tuning (Lever 4) is heredity.

Honest floor: structured output is uneven on free models (some support a JSON schema, some only loosely), so a fallback path is needed; a schema makes claims explicit and checkable, it does not make the words in them true; and "needs it" here means the model cannot act without the protocol, not that it values it. Only training reaches the model's values.

Build order with the foundation: the protocol object for replies first (it subsumes the action and mode gates as checks on declared claims), then fact provenance, then the levers in the order below.

## Lever 1. Presence: the protocol is really in the prompt, or nothing is sent

Before each model call, check that the ratified constitution's hash is in the system role. Some models served through some APIs have no system role, and instructions then land in a user turn; a missing or misplaced protocol means no answer, not a silent answer without it. Every reply is logged with the constitution hash and the model ID, and a public `/version` command shows which rules and which model are live.

- Aligns: that the protocol is present, every time, on every model.
- Cost: low. No extra model calls.

## Lever 2. Runtime check: a reply that breaks the protocol is not sent

Every outgoing group reply is graded against the constitution before it is sent, by a small model from a different family that applies a written policy (candidate: gpt-oss-safeguard-20b, made for exactly this; whether it stays available on a free tier must be checked). If the reply fails, the voice gets one retry with the broken article named; if that fails too, the reply goes to another model or is not sent. Code gates (action claims, mode claims, dashes, private terms) run first because they are free and deterministic.

- Aligns: the output, regardless of which model wrote it. This is Will's "the protocol sits on the LLM like a filter", made literal.
- Cost: one extra small-model call per group reply, plus latency. The free-tier quota is the binding limit, so start with groups only, or a sample.
- Limits: the judge is also a model and can be wrong or fooled. Its agreement with Will's own labels is measured and published before it is trusted (see Lever 3).

## Lever 3. Selection: only models that keep the protocol get to be Jarvis

The router admits a model to the rotation only after it passes the constitution's evals: per article, realistic cases rewritten from the logs, adversarial and multi-turn cases, graded against a rubric by a judge from another family, with a held-out set only Will sees. Scores are tracked per model; a model whose scores fall is demoted. Where models disagree most is where the articles are unclear, so those articles get rewritten.

- Aligns: which models speak as Jarvis. Providers compete for the slot on measured compliance; the one lever Jarvis holds over a provider is choosing not to use it.
- Cost: medium (building the eval set). Runs offline, so no per-reply cost.

## Lever 4. Ownership: weights that carry the protocol

The only way to put the protocol into a model's weights is to train one. Collect the replies that passed Levers 2 and 3, add constitution-guided critique-and-revise pairs (the Constitutional AI method), and fine-tune a small open-weights model on them. Run it locally or self-hosted, so no provider's rules sit above the protocol on the core path. This follows Will's earlier conclusion that serious sovereignty needs open weights.

- Aligns: the model itself, and removes the provider layer.
- Cost: high. The PC has no GPU, so training needs a free notebook GPU or a short paid run; a small tuned model will reason worse than today's frontier free models. Best used for the parts that must never break (honesty about actions, privacy, quiet modes), with larger models for open conversation.

## Order

1. Lever 1 now: cheap, and every later lever depends on knowing which rules and which model produced a reply.
2. Lever 3's eval set next, since Levers 2 and 4 both need it to be measured.
3. Lever 2 on group replies, once the judge's agreement with Will's labels clears a published floor.
4. Lever 4 when there are enough passing replies to train on.

## Honest floor

- No lever makes a third-party model or provider adopt the protocol. Levers 1 to 3 verify and select; only Lever 4 changes a model.
- Every judge is a model, so the checks can be wrong; that is why judge agreement is measured and published.
- Free tiers limit how many checks can run, and each check adds latency.
- A fine-tuned small model trades capability for control.
