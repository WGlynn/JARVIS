---
name: Local constraints stay local
description: Never put hardware-specific limits (RAM, CPU, concurrency caps) into shared/committed files — only in local config
type: feedback
---

Hardware-specific performance rules (max concurrent processes, RAM limits, CPU core counts) must ONLY go in local-only files (`~/.claude/CLAUDE.md`, memory files). Never put them in repo-committed files like `vibeswap/CLAUDE.md` or project configs that other contributors would inherit.

**Why:** Will caught this — baking "max 3 processes, 16GB RAM" into the repo CLAUDE.md would artificially limit anyone else who clones it. Local constraints are local. Shared files should only contain universally good defaults (like `via_ir: false` for dev).

**How to apply:** Before writing any performance rule, ask: "Is this MY machine's limitation or a universal best practice?" If it's machine-specific → `~/.claude/CLAUDE.md` or memory. If it's universal → repo files are fine.
