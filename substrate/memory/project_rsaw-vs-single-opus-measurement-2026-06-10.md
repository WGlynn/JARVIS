---
name: RSAWvsSingleOpusMeasurement
description: Empirically validate Princeton finding (single-agent matches multi-agent on 64% of tasks at HALF cost; fan-out 58-285% overhead) on Will's own JARVIS audit task surface. Hypothesis: RSAW 3-agent-parallel-sonnet may underperform single-opus-sequential at lower cost for at-least-one-domain audits. Pilot run 2026-06-10: 1 opus + 1 sonnet audit hooks-rs/jarvis-hook/src/lib.rs (just-shipped Rust port). Pilot ¬ full RSAW 3×; minimal-cost falsification step before burning a full 4-agent experiment.
type: project
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# RSAW vs Single-Opus Measurement

## ⇒ Hypothesis under test

**H0** (Princeton): single-agent at tier_N matches multi-agent fan-out at tier_N-1 on 64% of tasks; multi-agent fan-out costs 58-285% more tokens.

**H1** (RSAW justification): N-lens parallel coverage produces findings single-agent misses on JARVIS-specific audit tasks (HIERO compliance, LLM-optimization adherence, hook-contract preservation).

If H0 holds for JARVIS audit tasks ⇒ RSAW 3-agent pattern should be reserved for genuinely 2-axis-independent tasks only.

If H1 holds ⇒ RSAW retains its current usage shape (N-lens coverage justifies cost).

## ⇒ Pilot design (2026-06-10, minimal)

**Target**: `~/jarvis-monorepo/substrate/hooks-rs/jarvis-hook/src/lib.rs`  
*Why this file*: just shipped by Rust-port agent same session. Real fresh artifact. Three-lens scope: (1) correctness vs Python original, (2) idiomatic Rust, (3) LLM-optimization compliance.

**Agents**:
- Agent-A: **opus** subagent. Single-run sequential audit covering all 3 lenses.
- Agent-B: **sonnet** subagent. Same task, same lenses.

**Measure**:
- finding count (raw)
- finding quality (subjective by Will, or by claude-judge)
- duration (ms reported by Agent tool)
- token usage (`<usage>` block in task return)

**Compare**: opus vs sonnet at SAME task. Validates whether tier matters on JARVIS audit tasks.

## ↦ Future full experiment (if pilot motivates)

- Agent-A: opus, 3 lenses sequential
- Agent-B: sonnet, lens-1 (correctness)
- Agent-C: sonnet, lens-2 (idiom)
- Agent-D: sonnet, lens-3 (LLM-optimization)
- Compare A's findings vs (B ∪ C ∪ D)
- Cost: ~4× pilot

## ⇒ Decision tree on pilot result

| pilot finding | next move |
|---|---|
| opus ≈ sonnet quality | sonnet sufficient for this task class; no RSAW fan-out needed |
| opus > sonnet substantially | tier-A matters; full RSAW vs opus-only experiment justified |
| sonnet finds things opus misses | fan-out value confirmed; RSAW retained |
| both find same things | task is too easy to discriminate; pick harder audit target |

## ⇒ Pilot results 2026-06-10

Both agents returned. Same audit task, same file, two tiers.

| metric | sonnet | opus | ratio |
|---|---|---|---|
| findings | 10 | 13 | opus +30% |
| tokens | 22,865 | 31,260 | opus +37% |
| duration | 24.4s | 34.2s | opus +40% |
| effective cost (≈5× per-token premium) | 1.0× | ~6.8× | |
| verdict | needs-revision | production-ready | divergence on severity-weight |

### Overlap analysis

**Both caught** (load-bearing findings):
- `Err = Box<dyn std::error::Error>` shadows std `Err` variant (medium)
- `tail_utf8` u64→usize truncation on 32-bit targets (low portability nit)
- WHAT-narrating docstring on `tail_utf8` (low LLM-optimization)
- Section banners + identifier choices = ✓ (no finding)
- Fail-quiet contract preserved, no raw `unwrap()` (no finding)

**Opus-unique** (3 mediums):
- Duplicate serde_json re-export strategy (pub use root + pub mod re)
- `home()` uses `format!` not `PathBuf::join` for Windows paths
- No `#[must_use]` on emitters (idiomatic)

**Sonnet-unique** (1 medium):
- `emit_additional_context` takes event string from callers → Stop hook could call with PreTool schema (cross-contamination risk)

### Interpretation

- opus ~30% more findings at ~6.8× cost for this task class
- both caught all surface-bug-class issues
- opus added depth-of-idiom critique (naming, namespace, attribute-use)
- sonnet added a real risk finding (cross-contamination) opus missed
- discriminating axis = depth-of-idiomatic-critique ≠ surface-bug catching

### Princeton hypothesis validation (single-tier slice)

- broadly confirmed at single-agent tier: opus better, ¬ 6× better in proportion to cost
- sonnet sufficient for surface-bug-catching audits
- opus justified only when depth-of-idiom is load-bearing (architecture decisions, naming conventions, ecosystem-fit reviews)

### For RSAW pattern (multi-agent slice — NOT pilot-tested)

- pilot was 1×opus vs 1×sonnet, NOT 3×sonnet-parallel vs 1×opus
- since sonnet caught a real risk opus missed, multi-vantage value plausibly real
- 3×sonnet ≈ 0.6× opus token cost (3 × 23K = 69K vs 31K)
- but ALSO 0.6× the per-finding cost ratio if findings are independent
- worth running full experiment if a higher-stakes audit task surfaces

### Decision applied

- task class "code audit, surface bugs" ⇒ default sonnet (good-enough, cheap)
- task class "architecture or naming-convention audit" ⇒ consider opus
- multi-agent fan-out ⇒ defer; not justified by pilot signal alone
- Princeton finding STANDS as JARVIS-applicable for this task class

### Concrete fixes from pilot (both agents agreed)

1. Rename `Err` type alias → `BoxError` or `DynError` (medium)
2. Replace `tail_utf8` u64 param with usize OR `usize::try_from(n)` (low)
3. Prune `tail_utf8` docstring to one line WHY-only (low LLM-optimization)
4. Consolidate serde_json re-export strategy (pick one: root or `pub mod re`) (opus-unique medium)
5. `home()` use `PathBuf::join` instead of format! (opus-unique medium portability)
6. Add guard or rename on `emit_additional_context` to prevent Stop-hook cross-contamination (sonnet-unique medium)

→ 6 fixable findings · all under 15 LoC total · Rust-port follow-up worth one focused commit.

## ↦ Siblings

- [F·token-blind-multi-agent-default-is-anti-pattern] ⇒ rule this empirically tests
- [P·recursive-self-audit-via-wwwd] ⇒ RSAW canonical pattern under measurement
- [R·research-batch-2026-06-10-deep] ⇒ Princeton finding source
- [J·jarvis-coordination-mechanism-rick-2026-06-10] ⇒ classifier this informs
