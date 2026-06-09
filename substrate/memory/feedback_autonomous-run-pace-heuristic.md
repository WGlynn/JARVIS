---
name: AutonomousRunPaceHeuristic
description: Empirical pace ranges for sustained autonomous runs by artifact type. Use to size next-cycle scope and anticipate target-completion windows.
type: feedback
originSessionId: 8625a796-116e-42d8-b5c9-7064589f58ad
---
**[F·autonomous-run-pace-heuristic]** — empirical pace ranges per artifact type, observed during 2026-05-06 GH#18 reification + 300-commit run.

> *"300 commits"* + *"every commit goes to backup as well"* — Will, 2026-05-06

## Pace bands (observed)

| Artifact type | Median pace | Range | Notes |
|---------------|-------------|-------|-------|
| Mirror commit (cp + commit + dual-push) | 30-60 sec | 20-90 sec | shell-loop friendly, batchable |
| Memory primitive doc | 3-5 min | 2-7 min | requires HIERO-format compliance check |
| Concept doc (vibeswap docs/concepts/) | 5-10 min | 4-15 min | substantive prose; usually 100-200 lines |
| Architecture overview | 10-20 min | 7-30 min | substantive; usually 200-300 lines |
| JARVIS paper | 10-20 min | 8-30 min | substantive; varies by topic depth |
| Solidity interface stub | 5-10 min | 4-15 min | contract syntax + natspec |
| Solidity reference impl | 15-30 min | 10-45 min | contract syntax + logic + storage |
| Test suite (Foundry) | 10-20 min | 7-30 min | per file; multiple test fns each |
| Hook script (Python) | 10-15 min | 7-25 min | including pipe-test |
| WAL.md / SESSION_STATE update | 2-5 min | 1-10 min | depends on coverage |

## Implications for cycle sizing

- A 300-commit target via mirror-only mode: ~150-300 minutes (2.5-5 hours).
- A 300-commit target via mixed substantive+mirror: ~10-15 hours sustained.
- A 300-commit target via substantive-only: ~30-60 hours (multi-day).
- Realistic mixed mode: 50% mirror sweeps + 50% substantive ⇒ ~6-10 hours.

## How to apply

When Will sets an N-commit target:
1. Estimate the mix: how many can be mirrors vs substantive?
2. Compute expected duration using the bands above.
3. If duration > session budget (typically 4-6 hours sustained), surface this — better to renegotiate target or extend across sessions than to silently miss.
4. Front-load substantive work when energy is fresh; back-load mirror sweeps when fatigued.

## Confounders

- **Token-fatigue**: at scale, cognitive overhead per commit drifts up. Late-session commits are slower than early-session.
- **Inbound interrupts**: Will pasting external content (CAT spec dump) shifts the pace dramatically — content-dump-as-input-to-integrate primitive applies, requires 2-3 substantive paper commits to absorb.
- **Test runs**: forge build + test on Ryzen-1600 = ~50-60 sec compile; targeted test = ~1-2 min. Account for these against the targeted-run rule.
- **Permission prompts** (without autopilot-allow): each prompt = 5-30 sec friction. Cumulatively eats minutes per session.

## Sibling rules
- `[F·atomic-commit-pacing]` — discipline for atomicity; this primitive is the empirical pace.
- `[R·backup-remote-pattern]` — dual-push doubles GitHub signal but adds <5 sec per commit.
- `[F·autonomous-production-default]` — this primitive informs sizing; the discipline says keep producing.
- `[F·diagnose-on-stop]` — pace heuristic helps identify when a "stop" is fatigue (manageable) vs blocker (requires escalation).

## Origin
- 2026-05-06 GH#18 + 300-commit run
- 150 atomic commits at ~5h sustained = ~2 min/commit average across mixed types
- effective signal 300 with dual-push
