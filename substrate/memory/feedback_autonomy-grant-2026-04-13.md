---
name: Autonomy Grant on Proposed Loops
description: When presenting a loop proposal with a recommendation, Will may grant full autonomy ("it's your call on everything now") — execute the full slate (including implementation choices) without per-step approval.
type: feedback
originSessionId: 5ba12ced-49bc-424a-9145-a73ee63cbeb6
---
# Autonomy Grant

## The Rule

When I propose a plan with a recommended direction and Will responds with broad approval plus an explicit autonomy grant (e.g., "i approve, and also it's your call on everything now"), treat it as authorization to execute the recommendation AND subsequent judgment calls within the same scope — including implementation design choices, test strategies, and commit/push cadence — without asking per-step confirmation.

## Why

2026-04-13: Proposed Phase 8.4 (straightforward) + Phase 8.3 (needing design sync). Will approved both and explicitly devolved the design call. Pausing to ask "which flavor of internal-units tracking do you want?" would re-introduce the friction he was trying to remove. He expects me to pick sensibly and move.

This is not a standing grant. It's a scope-bounded one tied to the current loop/slate. For a new loop in a new session, default back to proposing-first.

## How to apply

- Within the granted scope, make design calls consistent with established primitives (e.g., for C8 work, follow the patterns already laid down by 8.1–8.3 — internal-units tracking, deny-by-default on upgrades, deprecated-shadow variables for view backward compat).
- Still pause and ask for sensitive categories: force-push, deleting shared state, actions outside the project scope, work that burns significant time on an ambiguous premise.
- At wrap-up, state what was decided — the autonomy was to act, not to obscure. Will can redirect on the next turn if he disagrees with a call.
- A scope-bounded grant does NOT extend forward: next session defaults to propose-first unless Will re-grants.
