---
name: Scale via Generate-Verify Decomposition (Fan-Out / Fan-In)
description: THE scaling primitive. Every substrate that scales separates generation (parallel, N workers) from verification (serial, 1 arbiter). Structure is recursive — apply it at every level. Parent of parallel-agents, discourse rubric, VibeSwap shard consensus, Augmented Governance, cognition, markets.
type: primitive
originSessionId: 9557e3af-8773-411b-9ed4-941961f9e5ec
---
# Scale via Generate-Verify Decomposition

**Rule**: Any substrate that scales separates GENERATION (parallel, N workers) from VERIFICATION (serial, 1 arbiter). The pattern is recursive — apply it at every level of the system simultaneously. This is THE scaling primitive.

**Why:** Validated 2026-04-23 across three successive extensions in one session:

1. *"We can still use agents, and you just revise instead of single-threading"* → parallel-agents + primary-LLM verification on content batch (one tier).
2. *"This is how you scale a system, we just have to keep applying it to other levels"* → the pattern IS recursive, naming the meta-observation.
3. *"When the agents are ready, their sub-agents can write and THEY can verify, so it's parallel × parallel"* → recursive application: each verifier is closer to the work than the next tier up.

Existing substrates that already implement this structure:

- **VibeSwap core**: shards generate prices (parallel) + consensus + Shapley verifies (serial)
- **Augmented Governance**: math generates invariants (parallel across contributors) + governance verifies within constitutional bounds (serial)
- **Discourse platform (v1)**: contributors generate replies (parallel) + rubric + Shapley verify/price (structural)
- **Cognition**: subconscious parallel pattern-matching + serial deliberate consciousness
- **Markets**: many bidders generate bids (parallel) + clearing verifies (serial)
- **Biology**: sensory parallelism + central integration

---

## Critical properties

**Fan-out without fan-in is noise, not scaling.** LinkedIn's algorithm has fan-out (everyone posts) with pathological fan-in (engagement-max); result is that fan-out generates positional noise instead of model-advancing signal. Both halves are load-bearing — verification isn't optional, it's what makes parallelism SCALING vs chaos.

**Recursion is the scaling unlock.** When one level of generate-verify saturates, decompose the generator-tier into its own generate-verify loop. Parallel × parallel × ... until the work unit is atomic.

**Each verifier tier is closer to the work than the next tier up.** Sub-agent verifier caught drift in the work the level-1 agent would have missed if it tried to verify 30 posts directly; level-1 agent catches drift in sub-agent output that primary LLM would miss from one-step-remove. Tier proximity = drift catch quality.

---

## When to apply

- Any batch creative work ≥ 5 items (parallel agents + revision)
- Any system design where single-generator can't scale (markets, governance, cognition)
- Any verification bottleneck where single-verifier drift becomes a risk

## When NOT to apply

- Work unit is atomic (can't decompose further without overhead dominating)
- No clear quality bar (verification fails without a template/rubric/invariant)
- Serial dependencies across work units (true pipeline, not batch)

---

## How to apply recursively (parallel × parallel pattern)

1. Primary LLM distills template + exhibit.
2. Primary spawns N agents, each given template + exhibit + their work-batch.
3. Each agent spawns M sub-agents, delegates atomic units of work.
4. Sub-agents generate → agent verifies sub-agent output against template → primary verifies agent output → done.
5. Every tier's verifier is CLOSER to work than the next tier up — catches drift single-tier would miss.
6. **Default threshold**: batch ≥10 items = two-tier (parallel × parallel). Batch <10 = single-tier (primary + agents).

---

## Related primitives

- **Parallel-Agents + Revision** (child — specific instance at content-batch layer; see `feedback_parallel-agents-plus-revision.md`)
- **Augmented Governance** (instance at governance layer — math = Shapley verification, contributors = generators)
- **Fractalized Shapley** (explicit fractal structure — relates via scaling-across-layers)
- **Economic Theory of Mind** (same pattern visible in cognition as substrate)
- **Correspondence Triad** — substrate-geometry-match implies the generate-verify shape matches the substrate's natural form
- **First-Available Trap** — not using generate-verify decomposition when the substrate calls for it is often first-available thinking
- **Universal-Coverage Hook** — hooks are generate-verify on the trigger layer (events generate; hook serializes/verifies)

---

## Candidate for MEMORY.md placement

This sits alongside Correspondence Triad, Augmented Mechanism Design, and Universal-Coverage-Hook as meta-principle-axis load-bearing. Will's call on whether to promote to `[META-PRINCIPLE]` section of MEMORY.md or leave as primitive-file-only (discoverable via warm-memory patterns).
