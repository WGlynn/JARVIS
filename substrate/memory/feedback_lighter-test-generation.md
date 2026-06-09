---
name: Lighter test generation
description: Don't mass-generate test files — caused crash. Fix existing tests over writing new ones.
type: feedback
---

Take it easier with test files. Mass parallel test generation (40+ test files across sonnet agents) contributed to context crashes and likely OOM.

**Why:** Session crashed during heavy test generation sprint. 384 tests already failing — writing more tests before fixing existing ones is counterproductive.

**How to apply:** Focus on FIXING failing tests rather than writing new ones. When writing tests, do them one file at a time, not in parallel batches. Prioritize test quality over quantity.
