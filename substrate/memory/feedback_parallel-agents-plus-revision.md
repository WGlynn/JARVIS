---
name: Parallel Agents + Revision for Batch Creative Work
description: For batch creative tasks (recuts, template application across N items), spawn parallel agents AND verify/revise. Don't single-thread; don't ship agent output untouched.
type: feedback
originSessionId: 9557e3af-8773-411b-9ed4-941961f9e5ec
---
# Parallel Agents + Revision for Batch Creative Work

**Rule**: For batch creative work (applying a template across N items, recutting content, generating variations), spawn parallel agents to do the heavy lift, then verify and revise their output rather than shipping it untouched.

**Why:** Validated 2026-04-23 during LinkedIn queue recut batch (30 posts). Will explicitly affirmed: *"that way we can still use agents, and you just revise instead of needing to single thread write them all."* Two failure modes this pattern avoids:
- Single-threading N creative tasks burns primary-LLM time when parallel-wall-clock is available.
- Shipping agent output untouched drifts quality — agents pattern-match the template differently than primary LLM does.
- The middle path (agents do volume, primary LLM revises) combines parallelism with quality control.

**When to apply:**
- N items ≥ 5 of the same kind of creative work
- A clear template or exhibit diff exists (otherwise agents drift too hard)
- Quality bar matters — agent output can't ship blind

**When NOT to apply:**
- Single-item creative work (parallelism overhead not worth it)
- Research/lookup tasks (use Grep/Glob/Read directly per Will-Scope-Claims memory)
- Template is fuzzy / bar is implicit (agents will drift catastrophically — distill the template first, or do it yourself)

**How to apply:**
1. Distill the pattern into a primitive-file + exhibit diff (template + worked example). Template alone = drift.
2. Spawn parallel agents with BOTH the template AND the exhibit. Skip criteria explicit so agents don't force-apply where it doesn't fit.
3. On agent return, verify each output against the quality bar. Spot-check at minimum; re-cut any that drifted myself.
4. Report agent-returns + revisions to Will, not just agent-returns.

**Related:**
- Trust-but-verify on agents (Agent-tool description built-in)
- Will-Scope-Claims — the complementary rule: don't agent-spawn for lookups Will already scoped
- Agent-Efficiency-Tiers
- Incremental Progressive Manifestation — revision-as-iteration is IPM on the deliverable
