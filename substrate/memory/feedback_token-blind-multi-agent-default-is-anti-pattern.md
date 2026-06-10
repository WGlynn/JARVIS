---
name: TokenBlindMultiAgentDefaultIsAntiPattern
description: ∀ agent-dispatch decision ⇒ default to single-agent-at-higher-tier ¬ multi-agent fan-out. Princeton finding: single agent matches multi-agent on 64% of tasks at HALF cost; fan-out has 58-285% token overhead. Fan-out only justified when ≥2-axis-independence (different domains × file-sets × vantages). RSAW 3-agent pattern justified by N-lens coverage NOT cost-efficiency. Behavioral rule on Claude/JARVIS dispatch.
type: feedback
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# Token-Blind Multi-Agent Default Is Anti-Pattern

## ⇒ Rule

- ∀ subagent spawn decision ⇒ FIRST ask: "could single-agent at higher tier do this?"
- if YES ⇒ single-agent (opus if substantive, sonnet if mid)
- if NO (genuine multi-axis independence) ⇒ fan-out justified
- default = single-agent

## ∃ Why (Princeton finding, May 2026)

- single agent matches multi-agent on **64% of tasks**
- single agent costs **HALF** of multi-agent fan-out (3-agent baseline)
- fan-out has 58-285% token overhead (varies by orchestration shape)
- multi-agent only wins when tasks are genuinely 2-axis-independent
- "more agents = better" intuition is empirically false at majority of agentic workloads
- src: [R·research-batch-2026-06-10-deep] · Princeton multi-agent token study

## ⇒ When fan-out IS justified (2-axis test)

- **domain independence** (e.g., security audit ∧ UX review ∧ docs polish on same PR — different lenses)
- **file-set independence** (different repos / non-overlapping module scopes)
- **vantage independence** (Will-emulation ∧ stranger-evaluator ∧ benchmark-grader — different perspectives, RSAW pattern)
- **time-independence ¬ count** (parallelizing for wall-clock speed when sequential would block — but cost-justify)

## ⇒ When fan-out IS NOT justified

- single-task that can be split into sequential sub-steps ⇒ single-agent + Code-Mode-orchestration ⊃ N spawns
- ambiguous task that needs disambiguation ⇒ single-agent + clarify-then-execute ⊃ parallel attempts
- low-stakes task ⇒ haiku/sonnet single-agent (cost-floor)
- short-context-window task ⇒ fan-out tax disproportionate

## ↦ Apply To

- ∀ Agent tool dispatch decision in autopilot
- ∀ RSAW cycle planning (validate the N-lens coverage actually requires N agents)
- ∀ coordination-mechanism-gate future extension (could surface "fan-out warning" when description suggests parallelizable-sequential)
- single-agent default ¬ removes ability to fan-out · removes thoughtless fan-out

## ⊥ Anti-pattern

- ✗ "let me spawn 3 agents in parallel" without checking 2-axis-independence
- ✗ assuming parallelism = strictly better (it's strictly more-expensive)
- ✗ RSAW with overlapping audit lenses (defeats the coverage justification)
- ✗ fan-out for tasks one agent at higher tier could do (Princeton 64% finding)

## ↦ Self-apply (per [P·apply-the-rule-you-just-wrote])

This session: spawned 2 agents this turn batch (mining + Rust-port). Justified per 2-axis test:
- mining ⇒ research-domain, web-fetching, no JARVIS substrate writes
- Rust-port ⇒ implementation-domain, monorepo writes, no web fetching
- Independent file-sets, independent domains ⇒ fan-out PASSES the test

But would NOT spawn a third agent to "do something else" without similar justification. Hooks-Rust + mining cover ~all current research-and-implementation surface.

## ↦ Siblings

- [R·research-batch-2026-06-10-deep] ⇒ source (Princeton finding section 4)
- [J·jarvis-coordination-mechanism-rick-2026-06-10] ⇒ composes with classifier (future fan-out warning)
- [P·recursive-self-audit-via-wwwd] ⇒ RSAW: justified BY N-lens coverage, not cost
- [F·rick-keep-it-simple] ⇒ shape match (volume ✗ defaults to single-shot)
