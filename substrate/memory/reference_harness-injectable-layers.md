---
name: reference_harness-injectable-layers
description: "Full map of injectable Claude Code harness logic-layers beyond {memory,hooks,crons}. Will's \"the list feels incomplete\" = CONFIRMED. Verified vs current docs 2026-06-26 (code.claude.com/docs)."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 5ce06dac-ae8f-4781-aa94-f0dc9d7625e3
---

Research (bg agent a7a5ecb9, 2026-06-26) vs current docs (`code.claude.com/docs`, `platform.claude.com/docs/agent-sdk`; old `docs.claude.com/.../claude-code` 301s away). Confirms [[feedback_jarvis-anthropic-design-convergence]] AND that JARVIS uses only a FRACTION of the surface.

## ◆ The set is MUCH bigger than {memory, hooks, crons}
- **Hooks = ~30 events** (¬ ~10). New persistence/cognition seams: `SessionStart`(+`watchPaths`,`reloadSkills`), `SessionEnd`, **`PreCompact`/`PostCompact`**, `InstructionsLoaded`, `Setup`, `FileChanged`, `PostToolBatch`(exit2 halts loop), `SubagentStart/Stop`, `ConfigChange`, `TaskCreated/Completed`. Hook `type` ∈ {command,http,mcp_tool,**prompt**,**agent**} ⇒ a hook can itself invoke a model.
- **Slash-commands MERGED into Skills** (one mechanism now).
- **Whole layer-classes unused:** Subagent `memory:` dir · Workflows (deterministic JS orchestration) · Monitors (persistent bg watchers → stdout into context) · MCP **resources** + **prompts** (≠ tools) · plugin `bin/`+LSP+`${CLAUDE_PLUGIN_DATA}` · output-styles (system-prompt layer) · statusline (det IO) · SDK callbacks (`canUseTool`,`sessionStore`,in-proc MCP,`systemPrompt` preset+append).

## ◆ RANKED — top layers to add (persistence/cognition leverage)
1. **Subagent `memory:` dir** — sanctioned per-agent cross-conversation store, auto-injected (first 200ln/25KB of its MEMORY.md). Closest native analog to mind-decentralization. [[project_mind-persistence-mission]].
2. **PreCompact/PostCompact hooks** — ONLY deterministic seam to snapshot/restore across compaction = mind-persistence-across-summarization. **= the missing layer in [[feedback_layered-persistence-defense]]** (we have turn-end hook + daily cron, ✗ compaction-boundary).
3. **Workflows** — plan-as-auditable-code, adversarial cross-review, 16–1000 agents; native home for RSAW/TRP.
4. **SDK `sessionStore`/`sessionStoreFlush` + in-proc MCP** — mirror session to OWN backend = literal mind off hosted-account. [[mind-persistence-mission]].
5. **Monitors** — det bg watchers pump external reality (CI/PR/logs/files) into context unprompted = harness-level [[airgap-problem-blockchain-vs-reality]] closer.
6. **MCP resources/prompts** · 7. **Skill `paths:`** (file-scoped auto-load) · 8. **InstructionsLoaded** (audit what memory entered context) · 9. **Output-styles** (edit system-prompt itself) · 10. **plugin `${CLAUDE_PLUGIN_DATA}`** (update-surviving state dir) + skills-dir zero-install packaging.

## ◆ CORRECTIONS (anti-stale — VERIFY before acting)
- CLAUDE.md `@`-import depth = **4 hops** (¬ 5).
- ⚠ **[[primitive_hook-event-schema-discipline]] / StopSchemaRestriction MAY BE STALE.** Current docs list `hookSpecificOutput.additionalContext` as VALID on Stop. CONFLICT w/ our "caught 3×" experience ⇒ installed-version may differ from latest-docs. **DO NOT flip the rule on doc-reading alone — verify against THIS installed `claude` version.** (Our `persistence-claim-capture.py` is PASSIVE ⇒ safe either way.)
- Task tool family (`TaskCreate/...`) replaced `TodoWrite`, default-OFF as of v2.1.142 (we have it on); gated by `TaskCreated/Completed` hooks.

Full report archived: bg-agent a7a5ecb9 output (session tasks dir).
