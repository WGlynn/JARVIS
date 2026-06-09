---
name: SequenceCreateThenReference
description: ∀ tool pair (CreateX → ReferenceX-by-ID) ⇒ sequence, ¬ parallelize. ID returned by Create must exist before Reference can target it. Parallel batching creates a race where Reference fires against a not-yet-assigned ID and fails. Discovered 2026-05-23 on TaskCreate+TaskUpdate parallel batch returning "Task not found".
type: feedback
originSessionId: a56046e0-1348-478f-9334-ecd5877892aa
---

# Sequence Create-Then-Reference

## ⇒ Rule
- ∀ tool pair {CreateX, ReferenceX(id)} ⇒ sequential ¬ parallel
- Create returns ID; Reference consumes ID ⇒ data dependency ⇒ ¬ parallelizable
- batching them in one tool-call block ⇒ Reference fires pre-Create-resolve ⇒ "not found" error

## ∃ Why
- 2026-05-23 batched 4× TaskCreate + 1× TaskUpdate(taskId:"8") in one call block
- TaskUpdate fired against id=8 before TaskCreate assigned id=8 ⇒ "Task not found"
- atomic-reflection-gate caught it, extracted before routing around

## ↦ How to apply
- ∀ Create + Reference of same entity ⇒ two separate tool-call rounds
- batching ✓ ∀ {many Creates} ∨ ∀ {many References to pre-existing entities}
- ✗ batching Creates w/ References to those same Creates' returned IDs

## → Connected pairs (where this rule fires)
- TaskCreate → TaskUpdate(id)
- TaskCreate → TaskGet(id)
- Write(path) → Edit(path) — slightly different (path is pre-known, file doesn't exist until Write completes; Edit assumes file exists ⇒ same race shape)
- mkdir → write-in-dir — same shape
- gh repo create → gh push → gh release create — chained pre-IDs

## ∀ Trigger
- ∀ tool block w/ Create-class + Reference-class targeting same entity ⇒ split into 2+ blocks
- ∀ multi-tool parallel batch ⇒ check for create-reference dependencies before send

## ✗ Anti-pattern
- "parallelize everything independent" ⇒ data dependencies look independent until they fail
- ignore the gate when it fires ⇒ retry-loop instead of structural fix
