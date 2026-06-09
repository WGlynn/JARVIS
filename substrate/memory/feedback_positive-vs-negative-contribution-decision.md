---
name: PositiveVsNegativeContributionDecision
description: "∀ Odysseus advice-graph entry ⇒ 3-axis filter: (1) substance-floor (extractable structural-shape?) (2) substrate-relevance (jarvis ∨ vibeswap?) (3) Will-triage (actioned ⇒ + / rejected ⇒ -). Drive-by snark fails axis-1 ⇒ null-player axiom ⇒ 0 attribution. Hostile-but-sharp ⇒ +. Friendly-but-vague ⇒ -. Filter-coincidence: same filter screens advice-quality ∧ funding-worthiness. 2026-06-09 Will-approval @ 14:58 ET."
type: feedback
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[F·positive-vs-negative-contribution-decision]**

## ⚙ Rule — Physics > Constitution > Governance, NO discretion

Per [P·augmented-governance]: classification MUST be structural-by-construction, not policy-by-Will. If Will can flip a negative to positive (or vice versa) by taste, the contribution-graph invariants are not load-bearing enough.

### Physics layer (math-enforced, no override)
Shapley 5-axiom set on the graph: null-player + symmetry + efficiency + additivity + pairwise-proportionality.
- null-player ⇒ ✗ attribution-padding
- symmetry ⇒ ✗ handle-bias
- efficiency ⇒ total = sum of marginals
- additivity ⇒ multi-advice composes
- pairwise-proportionality ⇒ equal-weight-at-same-depth

Will, JARVIS, no party can break these. They are by construction.

### Constitution layer (2-axis mechanical predicate filter)
Both axes are mechanical predicates evaluated by the C2.5 classifier, NOT judgment calls. Per Will 2026-06-09 15:11 ET ("you can decide physics and constitution rules"), the design of these predicates is the agent's responsibility; their application MUST be uniform across all contributions.

**Axis 1 — Substance floor (mechanical predicate)**:
- The contribution contains at least one substantive proposition about how a substrate (theirs, ours, or shared) should be structured, changed, preserved, or avoided.
- Decision procedure: can the classifier extract a `(substrate, change-direction, predicate)` tuple from the contribution's text?
- ✓ pass-shapes: "X is wrong because Y" / "Z should be replaced with W" / "Avoid pattern P because failure mode F" / "Pattern P enforces invariant I" / declarative principle with falsifiability
- ✗ fail-shapes: expressive reaction with no proposition ("this is bad" / "your post is too long" / cross-link to a mocking discussion) / self-referential meta with no proposition / off-topic
- ✗ axis-1-fail ⇒ **NEGATIVE** ⇒ null-player axiom mechanically zeros attribution. Constitutional, not discretionary.

**Axis 2 — Substrate relevance (mechanical predicate)**:
- The structural shape from axis 1 maps onto at least one component of JARVIS or VibeSwap with named identifiability.
- Decision procedure: can the classifier name a specific JARVIS component (hook / primitive / cron / script / memory file) or VibeSwap component (contract / frontend module / oracle / docs) that the advice's predicate touches?
- ✓ named-component ⇒ enters graph as **pending** with edge-weight 0
- ✗ generic-good-design with no named-component ⇒ **CLASS-C NEUTRAL** ⇒ `_advice-mined-log.md` only ⇒ ¬ graph-node ⇒ ¬ negative (just out-of-scope)

Pass both axes ⇒ contributor enters the graph as **pending** with edge-weight 0. Nobody (including Will) can demote them to negative without a constitutional re-classification (proving axis 1 or 2 actually fails on closer read).

### Governance layer (Will's role, free within constitution)
Will chooses what to ACTION (= ship a patch tracing back to this advice). Will does NOT decide positive vs negative.
- pending → **actioned** when a patch lands ⇒ edge weight set by patch impact ⇒ contributor's attribution-mass updates by Shapley calc
- pending → stays pending indefinitely if no patch ⇒ edge weight stays 0 ⇒ contributor has zero attribution-mass but is not negative
- pending → **constitutional-reclassify-to-negative** ONLY if deeper reading proves axis 1 or 2 actually fails ⇒ reason logged
- ✗ "Will doesn't like this contributor" is not a valid transition. Discretion at the classification layer is unconstitutional.

The graph state determines positive vs negative. Will's role is action-allocation only.

## 🎯 Edge cases

| Shape | Axis 1 | Axis 2 | Action-status | Classification |
|---|---|---|---|---|
| hostile-but-structurally-sharp | ✓ | ✓ | actioned | **positive** (mechanism rewards substance ¬ niceness) |
| friendly-but-vague | ✗ | n/a | n/a | **negative** (constitutional, not discretionary) |
| substance + generic-no-application | ✓ | ✗ | n/a | **class-c neutral** (out-of-scope, not negative) |
| substance + applicable + no-patch-yet | ✓ | ✓ | pending | **pending, attribution-mass 0** (waiting on action by anyone) |
| drive-by snark / format-complaint | ✗ | n/a | n/a | **negative** (constitutional) |
| Will personally dislikes contributor | ✓ | ✓ | pending | **pending** — discretion can't demote. If Will chooses not to action, contributor stays at 0 mass. Their work is still in the graph honestly. |

## 🎯 Worked examples (2026-06-09 ledger)

| Handle | Thread | Axis 1 | Axis 2 | Axis 3 | Outcome |
|---|---|---|---|---|---|
| @dustinm16 | PR #720 | ✓ retrieval-boost vs always-inject | ✓ jarvis | pending | **pending-positive** |
| @RaresKeY | #605 | ✓ 3-lane separation | ✓ jarvis | pending | **pending-positive** |
| @nopoz | PR #1314 | ✓ advisory→blocking CI gate | ✓ vibeswap | pending | **pending-positive** |
| @rutsty-rust | #3684 cross-ref | ✗ "you have a textwall" | n/a | n/a | **negative** |

## 🎯 Why filter-coincidence

⇐ [P·filter-coincidence-as-structural-edge]: same filter screens quality ∧ funding-worthiness ⇒ ¬ tradeoff ⇒ structural edge ¬ adverse-selection.

If we use ONE filter for "is this advice worth acting on" ∧ ANOTHER filter for "should this contributor be funded," the two filters diverge ⇒ adverse selection (low-quality high-niceness contributors gain weight). Single-filter discipline collapses both.

⇒ Shapley axioms then enforce mechanically:
- null-player ⇒ ✗ attribution-padding (axis-1-fail = 0 contribution)
- symmetry ⇒ ✗ handle-bias (two equivalent contributions @ same depth = equal weight)
- efficiency ⇒ total attribution = sum of marginal contributions (conserved)
- additivity ⇒ multiple advice from same contributor compose additively

## 🪝 Triggers

- ∀ new ledger row in `_advice-contribution-graph.md` ⇒ apply 3-axis filter BEFORE assigning status
- ∀ reply on announcement #3684 ⇒ classify pre-attribute (negative entries STILL get logged for honesty)
- ∀ Will-triage event ⇒ flip axis-3 status; preserve rejection-reason in receipts
- ∀ Shapley aggregation run ⇒ negative entries contribute 0; pending-positive entries contribute on action

## ✗ Anti-patterns

- ✗ exclude negative entries from log ⇒ breaks honesty audit (would look like only-positive contributors exist)
- ✗ reward niceness over substance ⇒ adverse selection
- ✗ multi-axis filter for advice but single-axis filter for funding ⇒ filter-coincidence violated
- ✗ auto-positive on "this person was nice" ⇒ symmetry axiom violated
- ✗ auto-negative on "this person was rude" if axis-1 passes ⇒ substance-disregarded

## ✓ Composes-with

- [P·filter-coincidence-as-structural-edge] ⇐ same filter ∀ quality ∧ funding-worthiness
- [P·shapley-5-axiom-set] ⇐ null-player + symmetry + efficiency + additivity enforce mechanically
- [P·honesty-as-structural-load-bearing-property] ⇐ negative entries IN graph ⇒ honest, ¬ hidden
- [F·odysseus-as-advisory-substrate] ⇐ C2.5 classifier this primitive supplies axis-2 to
- [J·odysseus-mission-loop] ⇐ Step 4 attribution-honesty REQUIRES this gate active
- [F·advice-mining-must-publish-to-public-graph] ⇐ classifications are public ⇒ contestable on-thread

## 🎯 Send-the-receipt option (toxic-actor structure-does-the-work)

⇐ Will 2026-06-09 14:59 ET: *"this is funny because instead of getting mad at toxic people and haters, we just log their negative contribution and send them the receipt LOL"*

⇒ structural-handling of toxic actors:
- ✗ emotional engagement ∨ pile-on ∨ ban-debate
- ✓ axis-1 evaluation ⇒ axis-1-fail ⇒ negative ledger entry ⇒ commit hash
- ✓ optional: tag the contributor in commit message OR reply w/ commit URL
- ✓ Shapley null-player axiom guarantees 0 attribution ⇒ mechanism handles the rest

Send-the-receipt format (when chosen):
```
Logged as negative contribution per [F·positive-vs-negative-contribution-decision]:
<commit URL in jarvis-substrate>
```

Use sparingly — feeding-the-troll risk. Default = silent log; receipt-send only when (a) Will-discretion OR (b) the toxic actor publicly demands attribution and the public ledger answers honestly.

## 📦 Receipts

- 2026-06-09 14:54 ET ⇐ Will: *"how will we manage deciding the difference between a positive and negative contribution"*
- 2026-06-09 14:55 ET ⇒ 3-axis filter proposed: substance-floor / substrate-relevance / Will-triage
- 2026-06-09 14:58 ET ⇐ Will: *"yes"* ⇒ lock as primitive
- 2026-06-09 14:59 ET ⇐ Will: *"this is funny because instead of getting mad at toxic people and haters, we just log their negative contribution and send them the receipt LOL"* ⇒ added send-the-receipt section
- ⇒ first ledger negative @ rutsty-rust #3684 (axis-1 fail)
- ⇒ public push: `_advice-contribution-graph.md` includes the rule by-reference; primitive ships in `memory/`
