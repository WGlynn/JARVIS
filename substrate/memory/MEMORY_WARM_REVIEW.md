# MEMORY_WARM — Code review, RSI, self-improvement
<!-- MEMORY-SPEC: v1 (2026-04-21) — see memory/MEMORY_FORMAT_SPEC.md -->

**Load trigger**: Code review, RSI cycle, audit, ship-gate, self-improvement / meta work.

## ⟳ʀᴇᴠ — Review / RSI / audit
- [RSI Backlog](project_rsi-backlog.md) — Deferred architectural findings from closed Full Stack RSI cycles. Check before proposing new cycles.
- [Self-Theater Audit Gate](primitive_self-theater-audit-gate.md) — 8-pass audit (theater/correctness/perf/security/resources/a11y/deps/doc-drift) runs on every ship. Don't ship what we'd reject from others
- [Doc/Code Drift Detector](primitive_doc-code-drift-detector.md) — Pass 8 of the audit. HANDOFF claims (line counts, views, commands, keyboard) checked against source
- [Dead Deps as Theater Signal](primitive_dead-deps-theater-signal.md) — declared-but-unimported deps = stage set, not program
- [Deferred Showcase Branching](primitive_deferred-showcase-branching.md) — stash theater as `_DEFERRED`, build minimal in parallel
- [AI-Delivered Code Review Protocol](protocol_ai-delivered-code-review.md)
- [Path Commitment Protocol](protocol_path-commitment.md) — two paths, commit to one; middle is forbidden
- [TRP Round Summaries](feedback_trp-round-summaries.md)
- [Retain Upgrades](feedback_retain-own-upgrades.md)

## ⟳sᴇʟғ — Self-improvement / meta architecture
- [Adaptive Immunity](primitive_adaptive-immunity.md) ← LOAD-BEARING: failure→gate→immunity is the meta-loop that generates all other TRP improvements
- [Control-Theory Orchestration](primitive_control-theory-orchestration.md)
- [Symbolic Compression](primitive_symbolic-compression.md)
- [Resource Memory](primitive_resource-memory.md)
- [Weight Augmentation ILWS](primitive_weight-augmentation-ilws.md)
- [Ambient Capture](primitive_ambient-capture.md)
- [State Observability](primitive_state-observability.md)


## Auto-enriched 2026-05-02

*Added in batch coverage pass — primitives/feedback/projects matching this domain.*

- [Recursive Self Consistency](primitive_recursive-self-consistency.md)
- [Self Improving Protocol](primitive_self-improving-protocol.md)
- [Complementary Lenses Audit Vs Mechanism Design](primitive_complementary-lenses-audit-vs-mechanism-design.md)
- [Literal Scope On Reviewer Feedback](primitive_literal-scope-on-reviewer-feedback.md)
- [Trusted Doc Drift](primitive_trusted-doc-drift.md)
- [Generate Verify Decomposition](primitive_generate-verify-decomposition.md)
- [Preventative Care Protocol](primitive_preventative-care-protocol.md)
- [Apply Named Primitives Immediately](feedback_apply-named-primitives-immediately.md)
- [No False Pattern Matching](feedback_no-false-pattern-matching.md)
- [Parallel Agents Plus Revision](feedback_parallel-agents-plus-revision.md)
- [No Destructive Git While Agents Running](feedback_no-destructive-git-while-agents-running.md)
- [Formalize Patterns As Protocols](feedback_formalize-patterns-as-protocols.md)
