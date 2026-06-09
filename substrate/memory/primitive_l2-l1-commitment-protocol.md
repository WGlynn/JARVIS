---
name: L2 → L1 Commitment Protocol
description: Concrete state-machine specification for the LLM L1/L2 Layering primitive. Maps optimistic-rollup commitment-to-L1 onto Decision lifecycle (proposed → active / revised / reverted). Reference implementation in lineage/app/commitment.py.
type: primitive
originSessionId: 58b19964-c316-4603-98a4-1ffe4fe4f29d
---
**Rule:** when staging L2 (fast/cheap) output for L1 (authoritative) ratification, use a state machine that makes provisional-vs-canonical explicit, records the L1 verdict on every Decision, and refuses to autonomously promote when L1 is unavailable. Never let L2 output enter canonical state without a ratification event.

**Why:** the LLM L1/L2 Layering primitive (primitive_llm-l1-l2-layering.md) is the architectural pattern; the commitment protocol is the contract between layers. Without a contract, three failure modes appear:

- **Undercommitment** — every turn escalates to L1 "to be safe." The L2 cost/speed benefit vanishes.
- **Overcommitment** — L2 outputs treated as canonical. Errors compound silently.
- **Stuck-provisional** — L1 outage leaves Decisions in limbo with no policy for how long they can wait.

The protocol below fixes all three by specifying triggers, verdicts, window bounds, and attribution precisely enough to implement.

**State model (maps to Lineage's DecisionStatus):**

```
    proposed  ──[L1 affirms]──►  active
        │
        ├────[L1 corrects]──►   revised   (old)
        │                      + NEW active Decision linked by
        │                        DecisionEdge(relation='revises'),
        │                        authored by L1
        │
        └────[L1 rejects]───►   reverted  (kept as a scar)
```

**Invariants:**
1. L2 NEVER emits a Decision in any non-`proposed` state.
2. Only the ratifier module transitions out of `proposed`. Enforce at the router layer — other endpoints can create/read but not status-transition.
3. L1 unavailable (API down, rate limited, failure) → Decisions stay `proposed`. NEVER autonomously promote on failure. Provisional is the safe default.
4. `correct` creates a NEW Decision authored by L1, not by the original L2 agent. The `DecisionEdge(relation='revises')` preserves lineage.

**Ratification triggers (ORed; first to fire schedules review):**
- **Time-based** (interval, default 300s) — respects cooloff. Catches slow drift.
- **Count-based** (batch-full, default 10) — bypasses cooloff. A full batch is its own urgency signal.
- **Topic-critical** (topic ∈ {auth, migration, security, ...}) — bypasses cooloff. High-stakes work never sits provisional.
- **Window-expiry** (Decision age > max_provisional_sec, default 900s) — bypasses cooloff. Bounds the worst-case provisional window.
- **User-request** — explicit force. Surfaces canonical output on demand.

**Cooloff semantics:** cooloff blocks only time-based re-triggers. It exists to prevent a slow drip from causing back-to-back L1 calls, not to throttle legitimate urgency. Count / critical / window-expiry all bypass.

**Verdict attribution:**
- Each Decision's `author_id` is the L2 agent that emitted it (role=`"L2:<model>"`).
- The L1 ratifier is recorded in a ratification record + the new active Decision's `author_id` (role=`"L1:<model>"`) on `correct`.
- Original L2 authorship is preserved even when L1 corrects or rejects.

**Metrics that matter:**
- `provisional_oldest_sec > max_provisional_sec` → ratifier stuck. Page operator.
- `reject_rate > 0.3` → L2 drifting. Retrain / prompt-update L2.
- `correct_rate > 0.5` → L2 close-but-not-right. More context to L2 may lift affirm rate.
- `affirm_rate > 0.95` AND `provisional_count < batch/2` → L2 over-qualified. Route more aggressively to L2.

**Analogy table (tight enough that rollup design transfers directly):**

| Protocol element | Blockchain analog |
|---|---|
| L2 emits proposed Decision | L2 mempool / rollup tx |
| Ratification trigger | Block interval / state-root commitment |
| Ratification event | Block finalization |
| L1 affirm | Optimistic-rollup success (no fraud proof) |
| L1 correct | New L1 block supersedes previous state root |
| L1 reject | Fraud proof accepted; state rolled back |
| Provisional window | Optimistic-rollup challenge window |
| `DecisionEdge(relation='revises')` | L2 state root pointing to previous root |

**Applied instance:** `C:/Users/Will/lineage/app/commitment.py` (state machine + ratifier loop + metrics), `tests/test_commitment.py` (14 tests: transitions, triggers, batch priority, full lifecycle, L1-unavailable safety), `docs/COMMITMENT_PROTOCOL.md` (design).

**Related primitives:**
- [LLM L1/L2 Layering](primitive_llm-l1-l2-layering.md) — the architectural pattern this protocol operationalizes.
- [Wardenclyffe Escalation](primitive_wardenclyffe-escalation-pattern.md) — the routing rule that decides which tier gets a task. Wardenclyffe says "start cheap, escalate on signal"; this protocol says "once escalated, here's the ratification contract."
- [Settlement State Durability](primitive_settlement-state-durability.md) — the cross-chain settlement analog. Both use `status → canonical` gated on external ratification; both use durable records + retry paths.
- [Optimistic UI / Durability Split](primitive_optimistic-ui-durability-split.md) — the UI-layer version of "perception ≠ canonical state."

**Standing instruction:** when an AI coding assistant (or any multi-tier AI system) needs to escalate from a cheap model to an expensive one, the escalation MUST carry a ratification contract. Specify triggers, verdicts, window bounds, attribution, and the L1-unavailable failure mode before building the system. Without the contract, the system oscillates between under- and over-committing, and the quality floor never holds.
