---
name: compact-workflows-into-commands
description: "After a complex multi-prompt workflow runs once, formally define it start-to-finish into a single invocable command (skill / saved Workflow). Workflow-level HIERO — compacts a prompt-sequence into one command the way HIERO compacts context into operators."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3a5d7fec-091d-4ee3-9c13-fa3b89c150bc
---

∀ complex multi-prompt workflow ⇒ after 1st successful run, FORMALLY DEFINE it start→finish into a single invocable COMMAND (skill ∨ saved Workflow script). ⇐ Will 2026-06-16: *"formally define complex multi prompt workflows so they semantically compact into commands the same way HIERO compacts context."* HIERO compacts CONTEXT→operators; this compacts a WORKFLOW (prompt-chain)→command. Next invocation = one command, ¬ reconstruct the prompt sequence.

**Why:** A workflow that took N prompts to steer the first time (refocus → mine bottlenecks → derive component → test → wire → commit, recursively) costs N prompts EVERY time until compacted. Prompt-reconstruction is the bottleneck ([[primitives-are-bottleneck-dissolutions]]); a named command dissolves it. Direct convergence hit: a Claude-Code SKILL / saved Workflow IS this primitive already ([[jarvis-anthropic-design-convergence]] — the harness ships the command-compaction primitive; use it, don't reinvent).

**How to apply:** After a multi-prompt workflow completes run #1 ⇒ (1) extract the INVARIANT procedure (steps that recur); (2) parameterize the variable parts (subject/project/scope) as args; (3) write it as `~/.claude/skills/<name>/SKILL.md` (name + description frontmatter) for `/<name>` invocation, OR a saved Workflow script for fan-out; (4) name post-hoc from the form ([P·name-follows-form-follows-function]). Trigger phrase: *"we did this as a prompt-sequence and will redo it."* Recursive: if a sub-workflow emerges mid-run, compact IT too. Sibling of HIERO (the context-compaction analogue). Composes with [[jarvis-anthropic-design-convergence]], [[incremental-progressive-manifestation]], [[universal-coverage-hook]], [[what-would-will-do]].
