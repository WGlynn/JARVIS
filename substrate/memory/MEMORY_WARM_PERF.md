# MEMORY_WARM — Performance and UI
<!-- MEMORY-SPEC: v1 (2026-04-21) — see memory/MEMORY_FORMAT_SPEC.md -->

**Load trigger**: Optimizing latency, bottleneck analysis, UI responsiveness, scaling.

## ⟳ᴘᴇʀғ — Performance / UI primitives
- [NC-Max Bottleneck Breaking](primitive_nc-max-bottleneck-breaking.md) — measure every layer, find the real constraint, attack the unexpected dimension
- [Speculative Execution (Idle)](primitive_speculative-execution-idle.md) — pre-compute during idle so commit is free
- [Optimistic UI / Durability Split](primitive_optimistic-ui-durability-split.md) — UI on intent, durability below
- [Observer Effect Discipline](primitive_observer-effect-discipline.md) — don't cause the latency you measure
- [Superlinear Adoption Scaling](primitive_superlinear-adoption-scaling.md) — each adopter contributes capacity via content-addressed caches


## Auto-enriched 2026-05-02

*Added in batch coverage pass — primitives/feedback/projects matching this domain.*

- [Mitosis Constant](primitive_mitosis-constant.md)
- [Hook Cutoff Optimization](feedback_hook-cutoff-optimization.md)
