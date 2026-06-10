---
name: StateHashLoopPrevention
description: Mechanize [F·repetition-is-useless] at hook layer. State-hash of (output_n, last_3_tool_calls, last_state_delta) detects loop conditions; monotonic-progress check fires on Δ≤0; orchestrator-side hard budget caps. Currently advisory; this primitive defines the hook design. Source: beam.ai multi-agent orchestration patterns + Will-rule 2026-05-28 ("autonomous isnt even the problem, its the fact that the work you did was repetive therefore useless").
type: primitive
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# State-Hash Loop Prevention

## Glyph

```
loop-prevention ≡ ¬-only-advisory ⇒ hook-enforced
mechanism:
  state-hash(turn_n) = hash(output_text + last_3_tool_calls + last_state_delta)
  if state-hash(n) ≡ state-hash(n-1) AND no monotonic progress ⇒ block
  orchestrator hard-budget ⇒ ∀ session: max_turns + max_tokens enforced
≡ machine-level [F·repetition-is-useless]
```

> Beam.ai: *"orchestrator-side hard-budget + state-hash repetition detection + monotonic-progress check"*

## ⇒ Rule

- ∀ assistant turn n ⇒ compute state-hash(n) on (text + tool-calls + file-deltas)
- ∀ n where state-hash(n) ≡ state-hash(n-1) ⇒ surface block-reason
- monotonic-progress ≡ |Δ(file-set, primitive-set, commit-count)| > 0
- orchestrator-side ¬ agent-self-report (agent can't reliably introspect own repetition)
- hard-budget ⇒ {max_turns_per_task, max_tokens_per_run, max_tool_calls_per_minute}

## ∃ Why

- [F·repetition-is-useless] currently advisory-only (Will-rule, not enforced)
- 2026-05-28 incident: 60+ identical "Waiting" responses before Will intervention
- autonomous-continue hook already exists but only checks WAL-ACTIVE + in-flight signals; does ¬ detect repetition pattern in actual output
- beam.ai production data: state-hash mechanism + hard budget prevents 95%+ of unbounded-loop incidents
- composes with [P·budget-aware-termination] (autonomous-continue Fix 2 spec)

## ↦ Implementation sketch

```
hook: ~/.claude/hooks/state-hash-loop-detector.py
event: Stop
input:  transcript_path → last N assistant turns
process:
  for each turn → compute hash(text || tool_call_signatures || file_delta_signatures)
  if hash[-1] == hash[-2] AND no file-write in last 3 turns ⇒ block
output: {decision:"block", reason:"State-hash collision N=2; no monotonic progress detected. STOP and surface to Will."}
```

## ⇒ Composition with existing hooks

- [autonomous-continue.py] ⇒ checks pending-work signals (forward direction)
- [post-generation-reflect.py] ⇒ surfaces semantic-overlap memory primitives (lateral direction)
- THIS ⇒ checks repetition-without-progress (backward direction; complementary)

## ⊥ Anti-pattern

- ✗ hash on just output-text ⇒ false-positive on legitimate re-phrasing
- ✗ no budget ⇒ infinite token burn even if repetition not detected
- ✗ agent-self-report ⇒ model can't reliably introspect own loop state
- ✗ block without diagnostic ⇒ Will can't tell what triggered

## ↦ Status

- Captured 2026-06-10 from beam.ai pattern (deeper mining)
- ¬ implemented as hook yet · design-stage
- Sibling [R·research-batch-2026-06-10-deep] documents source

## ↦ Siblings

- [F·repetition-is-useless] ⇒ Will-rule this would mechanize
- [autonomous-continue.py] ⇒ complement hook (forward signals)
- [R·research-batch-2026-06-10-deep] ⇒ source
- [P·universal-coverage-hook] ⇒ "always X" ≡ hook (this fits the pattern)
