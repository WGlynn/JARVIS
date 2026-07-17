# Non-LLM Intelligence — 10-LOOP status (2026-07-17)

The 10 LOOPs of Jarvis's CPU-local, non-LLM reasoning substrate. Each turns a piece of the ETM
("mind = economy") thesis from philosophy into a **falsifiable mechanism** that runs on commodity
hardware (Ryzen 5 1600 / 16 GB / no GPU), zero LLM calls on the reasoning path. Honest labels:
✅ built + verified · 🟡 designed · 🔬 exit-test open (needs accruing runtime data). Never rounded up.

Tooling lives in `tooling/`; the live wiring is in the operator's hook substrate. Built in the open.

| # | LOOP | module | verified result | status |
|---|------|--------|-----------------|--------|
| 1 | Memory-graph deduction (ASP) | `_asp_*` + `_asp_fallback` | 945 nodes / 2810 edges, clingo≡fallback differential, deterministic <0.5s | ✅ built + wired (graph-health cron) |
| 2 | Structured critic feedback | `_critic` | 9/9 self-test; **5 live gates** emit CRITIC-JSON (conflict-detector, compression-claim, time-logic, entity-context, wwwd 7737×) | ✅ built + **wired live** |
| 3 | Local solver gates (Z3+CP-SAT) | `_solver_gate` / `_scheduler` | 25/25 pytest; sound concurrency invariant + adversarial fixture; CP-SAT ≥ greedy | ✅ built + **wired live** (PreToolUse Bash) |
| 4 | Associative recall (Hopfield/VSA) | `_hopfield_recall` | 27/27 pytest; **honest-negative: cosine wins aggregate (100% vs 98%), but Hopfield catches 2 partial-cue cases cosine misses** → keep cosine primary, Hopfield as complement | ✅ built + verified (falsifiable test stopped the over-claim) |
| 5 | Belief layer / truth-values | `_truthvalue` / `_outcome_probe` | 19/19 pytest; revision math commutative≡pooled; outcome-recorder **wired live** (PostToolUse) | ✅ built + wired |
| 6 | Typed KR + sound inference | `_kr_check` / `_kr_schema.ttl` | 10/10 pytest; RDFS closure (rdflib+owlrl); **3 SPARQL checks catch 11 real inconsistencies** on live corpus (170 dead wikilinks) | ✅ built + verified |
| 7 ★ | Economic attention allocator | `_attention` | **centrality+recency 0.425 vs 0.350 centrality-alone vs 0.149 random**; recency HELPS (recovers Will's boot-set) | ✅ built; 🔬 real exit-test (beat MEMORY.md on task-success) data-gated |
| 8 | Decision arbitration (WWWD active-inference) | `_wwwd_infer` | 31/31 pytest; Dirichlet-Categorical (no pymdp); **OOD-uncertainty calibration PASS** (OOD 1.000 vs in-dist 0.002); accuracy test N-gated (1 correction / 7825 fires) | ✅ built + verified; 🔬 accuracy data-gated |
| 9 | Self-improvement as evolution (GP + MAP-Elites) | `_gate_evolve` | 44/44 pytest; **MAP-Elites 30 niches, no monoculture**; shadow-catch of a missing_gate class (low-confidence → correctly not promoted); no eval/exec | ✅ built + verified; 🔬 promotion data-gated |
| 10 | Noesis bridge (single→multi-node) | `_noesis_bridge` | 6/6 pytest; **LOOP 7 allocator satisfies Noesis `ValueOracle` seam contract** (lib.rs:283) → valid `v(S)` drop-in; shared value→standing→allocation pipeline | ✅ built (structural isomorphism code-grounded) |

## The through-line
LOOP 7 is the crux: an attention *economy* over the memory graph decides what loads into context —
ETM as mechanism, not metaphor. LOOP 10 shows that same *value → standing → scarce-allocation* rule is
the one Noesis runs at stakes (JARVIS allocates context budget; Noesis allocates consensus finality
weight). The isomorphism is **structural** — same seam, same contract, same pipeline — **not**
function-identity (`centrality ≠ temporal_novelty`). That honest bound is the point: Jarvis is the
zero-stakes lab where the mechanism is proven before the staked chain turns on.

## Honest open edges
- LOOP 7 real exit test (beat hand-tiered MEMORY.md on context-tokens × task-success) needs a runtime
  workload replay + per-primitive outcome data — data-gated, not yet passed. The recovery-proxy (0.425)
  is a necessary, not sufficient, precondition.
- LOOPs 2/5/8 exit tests want ≥1 week of live gate-outcome data (the outcome-recorder just went live).
- LOOP 10 is a code-grounded structural proof; running Noesis's Rust test-suite against the shared rule
  is the next step to upgrade "structural isomorphism" → "shared implementation."
