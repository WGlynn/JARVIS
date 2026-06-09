---
name: Blast-Radius-Ascending Cycle Order (multi-cycle sessions)
description: 2026-04-23 heuristic from triple-cycle session (C40b + C41 + C43). When shipping multiple independent cycles in one session, order them by ascending blast radius — most-isolated/additive first, most-invasive last. Builds momentum + reduces end-of-session regret-risk when energy flags.
type: primitive
originSessionId: 2599425c-2d6c-48c6-a7e1-6457f46d33f3
---
# Blast-Radius-Ascending Cycle Order

## The observation (2026-04-23)

Will greenlit three cycles in one session: C40b (wire retention into NCI vote), C41 (Shapley novelty multiplier), C43 (attested circuit-breaker resume). Triaged order on the fly:

- **C43 first** — new isolated code path (`attestResume`), existing behavior unchanged when flag off.
- **C41 second** — additive extension with backwards-compat default (1.0x multiplier is identity).
- **C40b last** — surgical change to existing active path (`vote()` weight accumulation). Most invasive, highest regression-risk.

Result: clean landing, no regressions, momentum built through the session.

## The principle

When shipping multiple independent cycles in one session, **order ascending by blast radius**:

1. **Smallest blast**: new isolated path. No existing call sites touched.
2. **Moderate blast**: additive extension with backwards-compat default. Existing call sites behave identically when the extension is unused.
3. **Largest blast**: modification of existing active path. All existing callers now see the new behavior.

Within each tier, also prefer cycles with:
- Smaller contract surface (easier to reason about).
- More localized tests (faster to verify).
- Clearer correctness criterion (less design ambiguity).

## Why this ordering works

### Momentum compounds forward
Shipping the easy thing first builds confidence + loads context. By the time you reach the invasive change, you've already:
- Re-familiarized with the test harness.
- Verified your build environment works.
- Shipped two commits, which makes the third commit feel smaller.

### Risk decays backward
If you shipped the invasive change first and broke something, you'd stall. Shipping it last means:
- If the session energy runs out mid-invasive-change, the isolated + additive changes are already banked.
- If the invasive change is aborted mid-flight, the session still produced two shipped deliverables.

### Design surprises surface early on isolated changes
Small isolated cycles surface environmental issues (pre-existing compile breaks, test flakes, build-system quirks) BEFORE you've committed to the harder surgical change. C40a's hidden lesson applies: verify the environment on the smallest possible cycle first.

## Counter-cases

Not every multi-cycle session benefits from this ordering:

- **When cycles have dependencies**: if cycle B reads from cycle A's state, ship A first regardless of blast radius.
- **When the invasive change is the load-bearing one**: if the session's goal is the invasive cycle and the others are "nice-to-have" support, ship the main one first. Otherwise the support cycles become ends in themselves and the main cycle gets pushed to next session.
- **When external pressure forces order**: ship order dictated by external deadlines (e.g., "must land before the governance vote at 2pm").

## Practical checklist mid-session

Before starting the next cycle in a multi-cycle session, ask:
1. Is this cycle's change additive (new code path) or modifying (existing code path)?
2. Does the cycle's blast radius exceed the next candidate's? If yes, defer.
3. Does the cycle depend on outputs of any un-shipped cycle? If yes, unblock the dependency first.
4. Am I ~60% through my usable session energy? If yes and the remaining cycle is invasive, split to next session.

## Related primitives

- [Text→Code: Verify First, Ship Second](./primitive_text-to-code-verify-first.md) — this session's C40a precedent. Verification-first IS a form of blast-radius-ascending (verify before writing code = smallest possible blast).
- [Token Mindfulness](./primitive_token-mindfulness.md) — discipline to stop and triage order before pattern-matching to "whichever cycle I noticed first."
- [First-Available Trap](P·first-available-trap) — the anti-pattern this primitive counters. Shipping "first available" cycle without blast-radius triage = random order = momentum loss.

## One-line summary

*Multi-cycle sessions: ship by ascending blast radius — isolated-new first, additive-with-default second, surgical-active-path last. Momentum compounds forward; risk decays backward. Verified 2026-04-23 across C40b + C41 + C43 in a single session, no regressions.*
