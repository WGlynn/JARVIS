---
name: Resource Memory (MIRIX Type 6)
description: Formal tracking of available tools, APIs, skills, MCP servers, and compute budgets per session — the 6th memory type.
type: feedback
---

# Resource Memory (MIRIX Type 6)

## Source

MIRIX (ICLR 2026 MemAgents Workshop) defines a 6-type memory taxonomy for agent systems:
1. Episodic — specific past events
2. Semantic — factual world knowledge
3. Procedural — how-to knowledge, protocols
4. Working — current task context
5. Prospective — future intentions, queued tasks
6. **Resource** — available tools, APIs, compute, and external services THIS session

Resource Memory is Type 6. It is not covered by the other five types and has historically been a blind spot in agent system design.

## What Constitutes Resource Memory in Our System

### Active Tools/Skills Per Session
- Which Claude Code skills are loaded (autopilot, session-start, p001-check, etc.)
- Which Bash tools, Edit tools, Read tools are available
- Any custom skill files present in `.claude/` directories

### API States (MCP Servers Loaded)
- Which MCP servers are active: Gmail, Google Calendar, etc.
- Connection status of each MCP (live vs. deferred vs. unavailable)
- Rate limit state for any API (e.g., how many Gmail calls remain)

### Compute Budget (Hardware from CTO)
- RAM available: 16GB on this machine (Ryzen 5 1600, 6c/12t)
- Max concurrent forge processes: 3
- Via IR status: OFF by default (OOM risk)
- Profile separation: `out-full`, `out-ci`, `out-deploy` prevent cache collision

### Available Models
- **Haiku**: fast, cheap — use for classification, routing, small edits
- **Sonnet**: balanced — default for most tasks (current model)
- **Opus**: deep reasoning — reserve for architecture decisions, novel problems

## How It Is Queried

At session start, before any tool-discovery loop:

1. Check which MCP servers appear in the system-reminder (deferred tool list)
2. Check MEMORY.md `[WARM] Local Tools` section for known installed tools
3. Check `memory/reference_local-tools.md` for tool availability cache (pandoc, pdflatex, etc.)
4. Do NOT ask "is X installed?" if Resource Memory already knows the answer

The anti-pattern to eliminate: an agent spending 3 tool calls discovering pandoc is installed when `reference_local-tools.md` already documents this.

## Who Writes It

- **Session boot sequence** writes initial state: models available, MCP servers detected, hardware profile
- **CTO (Jarvis in coordination role)** updates during session when tool states change
- **Any agent** that discovers a new tool or confirms a tool is missing should write back to `reference_local-tools.md`

The key is write-back discipline. Discovery without persistence is waste.

## Session Lifecycle

```
BOOT:   Read SESSION_STATE.md → check WAL.md → populate Resource Memory
        (tools loaded, MCPs active, hardware profile)

WORK:   Query Resource Memory before any tool-discovery action
        Update on change (new MCP connected, tool confirmed missing)

END:    Persist any new discoveries to reference_local-tools.md
        Clear session-volatile state (rate limit counters, temp MCP states)
        Do NOT clear persistent facts (pandoc installed, pdflatex missing)
```

## Why It Matters

**The waste pattern**: An agent wastes tokens asking "is pandoc installed?" via a bash call when Resource Memory should already know from the last session's write-back.

At 68 Python + 15 Solidity tests, 60+ sessions, 4 active agents — this waste compounds. Each redundant tool-discovery call is:
- ~500-2000 tokens wasted
- A distraction from the actual task
- A signal that the agent is not truly stateful

Resource Memory converts repeated discovery into single-write, many-read. This is the same principle behind the CKB itself.

## Connection to Other Primitives

- **Memory State Rent** (`primitive_memory-state-rent.md`): Resource Memory entries earn their position by access frequency × recency. Stale tool states get evicted.
- **Token Efficiency** (`feedback_token-efficiency.md`): Resource Memory is the first-order defense against discovery waste.
- **Anti-Stale Feed** (`feedback_anti-stale-feed-protocol.md`): Resource Memory must be verified, not assumed. A tool confirmed 10 sessions ago may no longer be available.
- **Agent Tiers** (`feedback_agent-efficiency-tiers.md`): Resource Memory informs which model tier to route a task to — if Opus is available and the task is architectural, use it.

## Operational Rule

> Before issuing any shell command to check if a tool exists, consult Resource Memory first.
> If Resource Memory is silent, run the check ONCE and write back.
> Never run the same discovery check twice across sessions.
