---
name: trp2
description: Run the workflow-level HIERO compaction loop — formally "Turing Recursion Protocol 2.0" (TRP 2.0). Derive new deterministic substrate components — gates, hooks, crons, skills, primitives, anchors, loops — from the real bottlenecks in OUR projects (Noesis, VibeSwap, JARVIS, Story Mode) and from the act of building them, building off existing components recursively. The hype-sphere calls this "loop engineering"; the rigorous description is workflow-level HIERO compaction + bottleneck dissolution. Invoke when Will says "run trp2", "run the learning loop", "derive components", "keep building the shell", or wants autonomous substrate self-improvement grounded in our actual work.
---

# TRP 2.0 — workflow-level HIERO compaction loop (formal definition)

Compacted from its first run (2026-06-16 session): one command replaces the prompt-sequence that steered it. Per [F·compact-workflows-into-commands]. Naming: rigorous = "workflow-level HIERO compaction"; hype-reflection = "loop engineering" (cf. [F·will-original-precedes-hype-reflection]).

## Args (optional)
- **subject**: `noesis` | `vibeswap` | `jarvis` | `story-mode` | `all` (default `all`). The project whose build is the bottleneck-source this round.
- **n**: components to derive this run (default: open-ended — keep going until told to stop or context-rotation).

## Operating frame (load before deriving)
- **Bottleneck lens** [F·primitives-are-bottleneck-dissolutions]: every component must NAME the throughput-governing constraint it dissolves. Names no bottleneck = ceremony-noise → short-track or drop.
- **Build off existing, recursively**: extend rules/components we ALREADY have; do not greenfield. Each compounds the prior ([P·code-text-inspiration-loop]).
- **Convergence** [F·jarvis-anthropic-design-convergence]: prefer the form mirroring a harness primitive — gate↔PreToolUse/PostToolUse hook, loop↔cron/Workflow, delegation↔subagent, command↔skill, context-compaction↔HIERO.
- **Honest-number** [U·will-intellectual-dishonesty-frame]; **pivot-until-read** [F·pivot-until-read-not-global-pause] (one blocked item never freezes the loop).

## Procedure (start → finish)
1. **SCOPE** — pick subject (arg or sweep `all`). State which project's build is the source.
2. **MINE BOTTLENECKS** — examine the real build (contracts, Rust, hooks, prompts, memory) for recurring friction / hard rules / silent failures. Prefer constraints already named in CLAUDE.md, `_primitives-pending.md`, WAL, or session pain.
3. **CLASSIFY (short-track, C3)** — needs-structure → full component; narrow/obvious → one-line fix or log, no ceremony.
4. **DERIVE** — build each in the convergent form:
   - **gate/hook** → `~/.claude/hooks/*.py` (PreToolUse/PostToolUse)
   - **cron** → durable `CronCreate` + `~/.claude/cron-prompts/*.md` canonical (pointer+logic split)
   - **primitive** → `memory/<type>_<slug>.md` (HIERO-dense) + MEMORY pointer
   - **skill** → `~/.claude/skills/<name>/SKILL.md`
   - **anchor** → Schelling/reference point in the relevant doc/memory
5. **TEST** — trust-boundary components (hooks/gates fire on every tool call) are dry-run tested against real input shapes BEFORE wiring. Never ship an untested gate; risky ones ship disabled with a note.
6. **WIRE** — hook → `settings.json` (re-validate JSON, utf-8, after); cron → durable; primitive → commit memory + pointer; skill → skills dir. A bad wire can break the session, so validate.
7. **COMMIT** — per-component. Memory → memory repo. Public-safe substrate → `jarvis-os-public`/`jarvis-substrate`. **Noesis → private remote ONLY, never public** (leak-gate).
8. **COMPACT (recursive)** — if a new multi-prompt sub-workflow emerged, formalize IT into a command too ([F·compact-workflows-into-commands]).
9. **MENU** — end with the Story Mode menu (loop continue-affordance). Keep looping until Will stops it.

## Invariants
- Follow existing rules; HIERO on memory writes; keep Noesis private; one blocked item ⇒ pivot not halt.
- Each run leaves the substrate MORE operator-extension, not less ([J·jarvis-design-goal-forever]).
