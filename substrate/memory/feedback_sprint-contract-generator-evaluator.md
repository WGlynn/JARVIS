---
name: SprintContractGeneratorEvaluator
description: ∀ autonomous coding subtask ⇒ generator-agent proposes (what + success criteria), evaluator-agent reviews (complete? clear?), BOTH agree ⇒ implementation begins. Planning+execution-same-pass ⇒ unreliable. Two distinct agents, not self-projection.
type: feedback
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[F·sprint-contract-generator-evaluator]**

## ⚙ Rule

∀ autonomous coding subtask ⇒ negotiate-before-implement
- generator-agent proposes ⇒ {what-will-build, how-success-verified}
- evaluator-agent reviews ⇒ {is-proposal-complete?, are-criteria-clear?}
- BOTH-agree ⇒ ∃ implementation
- generator-evaluator ≡ distinct agent invocations ¬ same-pass self-projection

## 🎯 Distinction from existing primitives

- WWWD gate ≡ self-projection ⇒ same agent projects Will-emulation
- this rule ≡ two-agent negotiation ⇒ distinct invocations w/ asymmetric roles
- complementary, not redundant ⇒ WWWD = within-step; sprint-contract = between-steps

## 🎯 Will-frame 2026-06-08 ⇐ Sairahul1 article

> *"Before the agent writes a single line of code: Two agents negotiate. ... Only after both agree does implementation begin. It's a design review. Except both participants are AI."*

> *"Agents that plan and execute in the same pass produce unreliable output."*

## 🎯 Application to jarvis-loop v1

current jarvis-loop v0 (committed 2026-06-08 `~/jarvis-loop/`) ⇒ has decomposer + auto-prompter + judge sequence ¬ negotiation-before-implement
⇒ v1 addition: insert evaluator-review step BETWEEN auto-prompter output ∧ coding-agent execution
⇒ if evaluator rejects ⇒ regenerate proposal ⇒ re-evaluate
⇒ if evaluator accepts ⇒ proceed to claude-code execution

## 🎯 Sprint contract template

generator output:
```
Subtask: {name}
Will-build: {concrete description}
Success-criteria:
  - {acceptance criterion 1}
  - {acceptance criterion 2}
Affected-files: {real paths, grounded}
Estimated-complexity: {small|medium|large}
```

evaluator review:
```
Completeness: {pass|fail + reason}
Clarity: {pass|fail + reason}
Grounding: {paths verified? symbols exist?}
Verdict: {approve|revise + specific issues}
```

## 🪝 Triggers

- ∀ jarvis-loop subtask BEFORE coding-agent invocation
- ∀ new VibeSwap mechanism implementation (insert contract step)
- ∀ Will-directed multi-step task w/ ambiguity (Will-instinct: "i wanted X" 2× ⇒ contract gap)
- ∀ subagent dispatch w/ creative latitude (per [F·parallel-agents-plus-revision])

## ✗ Anti-pattern

- ✗ single-pass plan-and-execute on non-trivial subtasks
- ✗ skip evaluator review for "obvious" tasks (obviousness = post-hoc rationalization)
- ✗ generator = evaluator (must be distinct invocations to be useful)
- ✗ evaluator rubber-stamps everything (calibrate evaluator-strictness)

## 🔗 Parents + siblings

- [P·harness-engineering-meta-frame] ⇒ parent (sprint contract is artifact 4 of 5)
- [P·what-would-will-do] ⇒ self-projection complement (WWWD is within-pass; contract is between-pass)
- [F·parallel-agents-plus-revision] ⇒ same shape: spawn AND verify
- [F·dont-default-concede-verify-first] ⇒ evaluator role = verification step
- [P·generate-verify-decomposition] ⇒ deeper formalization of same pattern

## 📦 Receipts

- 2026-06-08 Sairahul1 article integration ⇒ rule emerged
- jarvis-loop v0 lacks this step ⇒ v1 enhancement target
