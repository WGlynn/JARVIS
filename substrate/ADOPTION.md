# Adopting JARVIS — Fork-and-Replace Guide

JARVIS is single-operator-by-design. The load-bearing differentiator is **WWWD** (What Would Will Do): every autonomous decision projects through a corpus of operator-corrections before executing. That makes the substrate non-portable as-is. This guide shows how to fork and seed your own operator-corpus.

## What you take, what you replace

| Layer | Take as-is | Replace |
|---|---|---|
| L1 — Hooks (50 Python) | ✓ all generic gates | swap `wwwd-gate.py` for your own |
| L2 — Persistence | ✓ markdown + git | seed your own primitives |
| L3 — Anti-hallucination | ✓ AA#1–4, HIERO, conflict, time-logic | re-tune entity lists |
| L4 — Discipline corpus | ✗ Will-specific | replace with your corpus |
| L5 — Meta-protocols | ✓ AMD / AGov / SubstrateGeomMatch / etc. | n/a |
| L6 — Agent overlay | ✓ Claude Code + skills + cron | n/a |
| L7 — Stateful apps | ✗ Will-specific | yours |
| L8 — Filesystem | ✓ universal | n/a |

## Three-step seed

### Step 1 — Fork

```bash
gh repo fork WGlynn/JARVIS --clone --remote
cd JARVIS/substrate
```

### Step 2 — Replace WWWD corpus

The WWWD corpus is a directory of correction transcripts that build the operator-emulator. Seed yours:

```bash
mkdir -p memory/_system/wwwd_corpus_seed
# Drop in 30–50 of your real conversation excerpts where you corrected an AI
# Each file: <YYYY-MM-DD>-<topic>.md, body = your correction + why
# The L3 auto-arsenal will start mining patterns once 30+ files exist
```

What to seed:
- Times you said "actually, do X instead" — correction-pattern
- Times you said "no, that's not what I meant" — disambiguation-pattern
- Times you said "always / never / from now on" — rule-promotion-pattern
- Times you praised a specific approach — validation-pattern (record alongside)

### Step 3 — Rebuild the cognition gate

The WWWD hook at `hooks/wwwd-gate.py` projects candidate actions through the corpus. Update its config:

```python
# in wwwd-gate.py, near the top
OPERATOR_NAME = "your-name-here"
OPERATOR_CORPUS = Path.home() / '.claude' / 'projects' / '<your-claude-project>' / 'memory' / '_system' / 'wwwd_corpus_seed'
```

Run a few dispatch decisions; the gate will start firing recommendations based on your corpus.

## Skills that port without change

These work for any operator:
- `/classify` — cost-aware tier recommendation
- `/critical-qa` — self-adversarial Q&A on code
- `/JarvisOS` — boot-surface for the substrate

## What doesn't port

- Partner-arch gates for specific named people (Will's relationships)
- USD8 architecture guards (Will's specific partnership)
- Will-personal correspondence patterns

These files start with `feedback_` or `project_` prefix referring to specific people. Skip importing those into your fork; they'll be dead refs and the audit will flag them.

## CLAUDE_PLUGIN_ROOT compatibility (Codex CLI)

OpenAI's Codex CLI ships its own hook system that mirrors Claude Code's event schema and sets `CLAUDE_PLUGIN_ROOT` + `CLAUDE_PLUGIN_DATA` for plugin compatibility. JARVIS hooks run unmodified on Codex CLI after pointing the env vars at your substrate root.

```bash
export CLAUDE_PLUGIN_ROOT=~/JARVIS/substrate
export CLAUDE_PLUGIN_DATA=~/.codex/jarvis-data
codex  # hooks fire on the same events
```

Source: docs.openai.com/codex/hooks and verified against Claude Code hook schema in code.claude.com/docs/en/agent-sdk/hooks.

## When you outgrow the fork

If your corpus matures enough that you're correcting AI in domain-specific ways the original substrate doesn't address, write your own primitives. Don't fork JARVIS twice; build on the meta-protocols (L5) and let your L4 corpus diverge.

## Known limitation: git-history leakage class

The `discretion: nda | partner-private | internal` frontmatter flag prevents future syncs from mirroring a file to the public substrate. It does NOT scrub git history if a pre-flag version was already pushed to a public remote.

If you add the flag retroactively to a file that was previously public:
- Future syncs: file is excluded, mirror copy is deleted from the public substrate (good).
- Git history on the public remote: still retains the pre-flag content (bad).

To fully eliminate the leak, you need a `git filter-branch` / `git filter-repo` rewrite + force-push on the public remote. That is destructive and history-rewriting, so the sync script does not do it automatically.

**Class-mitigation**: tag files with the right discretion flag at creation time, not retroactively. Treat history-leakage as a separate cleanup task that requires explicit operator decision (rewrite vs accept).

## Cited primitives

- [P·what-would-will-do] — the cognition-gate this guide replaces
- [P·jarvis-os] — the navigation shell
- [F·optimize-for-llms] — applies to your fork too
- [F·no-bullshit-do-the-research] (AA#4) — copies clean
