---
name: fortress-around-the-model
description: "Claude Code architecture (≈98% deterministic harness, ≈2% model-touching) = external validation of the augment-don't-replace bet. Same pattern as JARVIS + VibeSwap."
metadata: 
  node_type: memory
  type: project
  originSessionId: c68bf9df-70e9-4b3e-bf99-9fdae6ab08ac
---

**FortressAroundTheModel** — Claude Code = while-loop(ask-model → run-tool → repeat) wrapped in deterministic scaffolding: permission-modes ∧ layered-context-compaction ∧ subagent-worktree-isolation ∧ hook-surfaces. Model-touching code = small minority; the bulk = managing the model (¬ hallucinate, ¬ destroy-host, ¬ lose-goal).

THESIS-VALIDATION: this ≡ [[augmented-mechanism-design-paper]] at the harness layer — augment(invariant) ¬ replace(model). You don't make the model smarter, you build structure around it and manage it ⇒ [[structure-does-the-work]] as shipped-product. Anthropic shipped the most-obsessed-over instance of the pattern Will built in a cave first.

RECURSION (3 substrates, ONE bet):
- Claude-Code = fortress @ harness layer (Anthropic's deterministic scaffold around a model they can't retrain mid-loop).
- [[jarvis-os]] = fortress @ cognition layer (hooks + memory-compaction + permission-gates around Claude — I ran INSIDE this pattern while writing this; a permission HOLD blocked an Odysseus post, compaction surfaced the right memories, cron self-perpetuated).
- VibeSwap = fortress @ protocol layer (dissolve MEV via structure ¬ via smarter traders).

Maps to [[jarvis-amd-applied-to-ai-substrate]] (JARVIS = AMD @ AI substrate) + Cave-philosophy ("take an existing thing, build the fortress around it, because that's all you've got").

PROVENANCE-HONESTY: the viral framing ("leaked source / research team / 500k lines / 98% not AI") = spin, ✗ co-sign. Load-bearing claim (harness ≫ model in LOC, deterministic-management is the product) = TRUE + self-verifiable from inside the tool surface. Will named the primitive from scratch before any "leak." ⇐ Will TG 2026-06-15 "sounds familiar haha".
