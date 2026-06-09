---
name: Forge build/test performance rules
description: via_ir OFF by default, max 3 parallel forge processes, targeted tests only, separate output dirs per profile
type: feedback
---

Default profile now uses `via_ir = false` (changed 2026-03-28). Via IR is 3-10x slower and 2-3x more RAM — on 16GB with parallel agents, it OOMs.

**Why:** Ryzen 5 1600 (6c/12t) + 16GB RAM. Multiple agents running `forge test` with via_ir = true causes OOM crashes, cache corruption, and stalls. Build output is massive and burns context.

**How to apply:**
- Default profile = no via_ir. Use `FOUNDRY_PROFILE=full` only for deploy validation or bytecode size checks
- NEVER run full test suite (80+ files). Always `--match-path` or `--match-contract`
- Max 3 concurrent forge processes across all agents
- `full`/`ci`/`deploy` profiles write to separate `out-*` dirs to prevent cache corruption
- Write correct code first by reading interfaces. If build check needed, run in background
- Batch compilation: write multiple files, then one build. Don't block on output
- Stack-too-deep → use `--skip` to binary-search, then `FOUNDRY_PROFILE=full` for just that contract
- NEVER run `forge clean` during parallel agent runs — it wipes the shared cache and forces every agent to recompile from scratch
