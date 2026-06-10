---
name: SemanticCheckpointRelevanceGate
description: ∀ checkpoint/WAL-write candidate ⇒ evaluate recovery-relevance BEFORE writing. Skip when no semantic delta. Source: Crab (Diagrid 2026) — 75% of agent turns produce zero recovery-relevant state; selective checkpoint raised recovery correctness 8%→100% AND cut checkpoint traffic 87%. Currently JARVIS WAL + auto-checkpoint write on every file-mutating tool call; this primitive defines the selectivity filter that would replicate the Crab result for JARVIS substrate.
type: primitive
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# Semantic Checkpoint Relevance Gate

## Glyph

```
∀ checkpoint-candidate ⇒ recovery-relevant? ∈ {yes, no}
  recovery-relevant ⇔ ∃ ≥1 of:
    (a) state-mutation crossed logical-boundary (commit · session-close · phase-transition)
    (b) commit happened (SHA produced)
    (c) decision-shaped statement in turn output
    (d) primitive added/modified (file in memory/*.md)
    (e) hook/script source changed (executable substrate)
  recovery-relevant ¬ ⇒ skip checkpoint (silent)
expected delta:
  WAL traffic ↓ ~87% (Crab benchmark)
  recovery correctness ↑ 8%→100% (Crab benchmark)
```

> Crab (Diagrid 2026): *"75% of agent turns produce zero recovery-relevant state. Selective checkpoint raised recovery correctness 8%→100%, cut checkpoint traffic 87%."*

## ⇒ Rule

- ∀ checkpoint write candidate ⇒ run relevance-gate FIRST
- relevance-gate := check {commit-happened, file-content-actually-changed, decision-stated, primitive-mutated, hook-changed}
- if zero matches ⇒ skip (silent, log nothing)
- if ≥1 match ⇒ proceed with checkpoint
- gate decision recorded in telemetry (for future tuning)

## ∃ Why

- current JARVIS auto-checkpoint.py fires PostToolUse on every Edit|Write|Bash|NotebookEdit
- many of those calls produce zero recovery-relevant state (e.g., reading then writing identical content; ephemeral diagnostic Bash)
- Crab data: blanket-checkpoint costs 87% wasted IO + dilutes recovery signal
- aligns with [F·optimize-for-llms] — minimize noise in state-substrate

## ↦ Implementation sketch (for hook layer)

```
gate location: ~/.claude/hooks/semantic-checkpoint-relevance.py
event: PostToolUse (matcher = Edit|Write|Bash)
input: stdin JSON payload (tool_use_result + tool_input + cwd)
process:
  - if Bash ⇒ check exit code 0 ∧ ≥1 file mtime changed (or ≥1 commit SHA in output)
  - if Edit/Write ⇒ check file content actually changed (hash comparison)
  - if NotebookEdit ⇒ check cell-content delta non-empty
  - if none match ⇒ return {} (skip checkpoint downstream)
  - if match ⇒ pass-through (auto-checkpoint.py fires as before)
output: gate decision logged to _system/checkpoint_gate_fires.jsonl
```

## ⇒ Composition with existing hooks

- auto-checkpoint.py (existing) ⇒ blanket checkpointing
- THIS relevance-gate ⇒ filter that decides whether auto-checkpoint should proceed
- could implement as: relevance-gate runs BEFORE auto-checkpoint; sets env var; auto-checkpoint reads env var

## ⊥ Anti-pattern

- ✗ relevance-gate too aggressive ⇒ misses recovery-critical state
- ✗ no telemetry ⇒ can't tune thresholds based on actual recovery incidents
- ✗ blanket skip on read-only tool calls without confirming truly nothing changed (defensive verify)
- ✗ agent-side self-report ⇒ tool must externally verify file mutation

## ↦ Status

- Captured 2026-06-10 from Crab finding (deeper-mining agent return)
- ¬ implemented as hook yet · design-stage
- Holding for Will-review before shipping (PostToolUse hooks on every file op are critical-path)

## ↦ Siblings

- [R·research-batch-2026-06-10-deep] ⇒ source
- [P·anti-amnesia-protocol] ⇒ WAL-discipline this filters
- [P·state-hash-loop-prevention] ⇒ sibling pattern (different axis: repetition vs relevance)
- [F·optimize-for-llms] ⇒ minimize-noise aligns
