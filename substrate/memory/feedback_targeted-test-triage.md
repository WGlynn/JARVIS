---
name: Targeted Test Triage — Never Full Suite First
description: When fixing failing tests, build cache first then run by directory/cluster. Never block on a full forge test run.
type: feedback
---

# Targeted Test Triage Protocol

When facing a large number of failing tests, NEVER start with a full `forge test` run. It blocks the entire workflow for 10+ minutes on Will's hardware.

**Why:** On 2026-03-28, a full `forge test --summary` run clogged the session for 30+ minutes, blocking all other work and mempool-ing Will's messages. Targeted runs keep the conversation responsive and fix failures faster.

**How to apply:**
1. `FOUNDRY_PROFILE=fast forge build` first — warm the cache (background)
2. While building, triage by reading test files and contract interfaces directly
3. Once cache is warm, run tests by directory: `forge test --match-path "test/agents/*"`
4. Fix cluster by cluster, smallest-to-largest for quick wins
5. Never run full suite until you believe all clusters are fixed
6. Use `--match-contract` and `--match-test` for surgical runs during fixes
7. This is BIG-SMALL rotation applied to testing — keep momentum, never block
