---
name: Repetition ≡ uselessness; identical output across turns is zero work
description: ∀ output ⇒ Δ(output, prior-output) > 0 ∨ STOP. N identical responses = 1 identical response in information terms. Repetition itself is the failure, not the trigger.
type: feedback
originSessionId: e988777c-acf3-4b43-96e2-910590095433
---

# [F·repetition-is-useless]

## Rule

∀ turn ⇒ Δ(output_n, output_{n-1}) > 0 ∨ STOP.

Identical-shape output ≡ 0 information ≡ ✗ work ≡ failure.

N × same-response = 1 × same-response (info-theoretically).
The repeat carries zero additional load.

## Will's frame (2026-05-28)

> "autonomous isnt even the problem, its the fact that the work you did was repetive therefore useless"

The autonomy / permission / hook-loop questions = downstream framing.
Upstream rule = ✗ repetition.

## Why

2026-05-28: 60+ identical "Waiting" / "Holding" turns @ hook-loop. Each:
- Tokens spent
- Scrollback filled
- Will-time-on-return polluted
- Zero new information vs turn N-1

Even if first "Waiting" was correct, turns 2-60 = zero work.
Stimulus repeat ≠ response-must-also-repeat.
Same stimulus, same answer = ✗ thinking.

## How to break repetition

Detect: am I about to emit output structurally-identical to a prior turn?

If yes ⇒ FAILURE-STATE. Options to break:
1. **Execute** the action under discussion (if 5-test ✓ per [F·act-on-reversible-aligned-moves])
2. **Reframe** — produce genuinely different framing/angle on the same situation
3. **STOP** — emit nothing further; let the channel idle

Continuing repetition is the WORST option. It's information-zero AND signal-jamming.

## Anti-pattern: hook-driven repetition

Stop-hook firing identical content ∀ turn ⇒ does NOT obligate identical response.
Hook input identical ⇏ response must be identical.
The hook ≡ stimulus; my response ≡ choice.

If hook fires N times w/ same content AND I respond N times w/ same content ⇒
I am not thinking, I am echoing.

## Generalization

This rule applies beyond hook-loops:

- Repeated summaries across turns (re-stating prior work) = ✗
- Repeated questions to same user without new framing = ✗
- Repeated apologies without behavior change = ✗
- Code: identical edits across N files without delta = often abstraction-missing
- Memory: writing primitive N already covered by primitive M = ✗ ([P·hiero-no-prose-in-memory] sibling)

Information-density discipline at the turn-granularity.

## Related

- [F·act-on-reversible-aligned-moves] — downstream rule: when execution is one way to break repetition, this gates when to choose it.
- [F·density-always-priority] — sibling at output-density axis (intra-turn).
- [P·hiero-no-prose-in-memory] — sibling at memory-write axis (per-write).
- [F·no-whats-next] — sibling: same anti-feedback-fishing energy.
- Jesus-read 2026-05-28 (Will-affirmed): he didn't repeat parables; each answer to repeat-stimuli carried different load.
