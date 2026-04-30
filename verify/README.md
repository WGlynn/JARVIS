# Verify

> Don't take this on faith. Concrete checks any reader can run.

The architecture described in [the essay](../papers/jarvis-is-not-a-wrapper.md) is verifiable. The verification surface is the filesystem, the git history, the regression tests, and the live logs. Five checks any reader can run independently.

## 1. The hook layer is real

```bash
# In a JARVIS-equipped environment:
ls ~/.claude/session-chain/
# Expected: partner-facing-substance-gate.py, partner-facing-additive-gate.py,
#           hiero-gate.py, triad-check-injector.py, ...
```

Read `partner-facing-substance-gate.py` — the watch list + context disambiguator regexes are ~200 lines of plain Python. Look at recent commits to the partner-facing repos for evidence of writes that would have shipped wrong terminology and got blocked at write-time.

The hooks are deterministic — no LLM call, no probabilistic judgment. Regex + context window + watch list.

## 2. The persistence layer is real

```bash
# In the vibeswap repo:
cat .claude/SESSION_STATE.md
cat .claude/WAL.md
git log --oneline .claude/SESSION_STATE.md | head -20
```

[`vibeswap/.claude/SESSION_STATE.md`](https://github.com/wglynn/vibeswap/blob/master/.claude/SESSION_STATE.md) and [`vibeswap/.claude/WAL.md`](https://github.com/wglynn/vibeswap/blob/master/.claude/WAL.md) are git-tracked. The most recent commits to those files show every state transition — every session boot, every cycle close, every reboot continuation point.

Read the commit history. Each commit is a session epoch.

## 3. The discipline layer is real

```bash
# In a JARVIS-equipped environment:
ls ~/.claude/projects/*/memory/primitive_*.md | wc -l    # Expected: ~151
ls ~/.claude/projects/*/memory/feedback_*.md | wc -l     # Expected: ~123
```

Each is a markdown file with a trigger and action. Many have been added in the last 30 days — `git log` would show capture timestamps if the memory directory were public. Public-safe summary lives in [`vibeswap/.claude/JarvisxWill_GKB.md`](https://github.com/wglynn/vibeswap/blob/master/.claude/JarvisxWill_GKB.md).

## 4. The TG bot is real

```bash
fly logs -a jarvis-vibeswap | grep -E "(router|escalation|wardenclyffe|consensus|crpc|inner-dialogue)"
```

Watch a single user message walk five providers, register three shards, activate BFT consensus, and emit a self-correction insight, in two seconds. The escalation log in [the essay](../papers/jarvis-is-not-a-wrapper.md#stateful-applications) is real output captured during a Claude API outage.

Public mirror: [`github.com/WGlynn/jarvis-network`](https://github.com/WGlynn/jarvis-network).

## 5. The published artifacts are real

```bash
ls vibeswap/docs/papers/*.md | wc -l    # Expected: 60+
```

Each is canonical thinking on a specific topic, cross-referenced from memory primitives, shipped through the Code ↔ Text Loop. [Browse them on GitHub](https://github.com/wglynn/vibeswap/tree/master/docs/papers).

The essay that produced this monorepo — [`jarvis-is-not-a-wrapper.md`](../papers/jarvis-is-not-a-wrapper.md) — is itself one of those papers, copied here as the source-of-truth specification for the repo.

## What you'll *not* be able to verify externally

Some surfaces are intentionally private:

- **MEMORY.md contents** — has personal context, partner-specific signals
- **Off-repo paper trails** — for collaborations that aren't public
- **Some hook watch lists** — contain partner-confidential terminology
- **Active session state** — current cycle work, in-flight items

The architecture is shown; the contents are not. The discipline is verifiable by the existence of the files and the git history. The contents stay where they belong.

## What "verifiable" means here

> The architecture is not a story. The architecture is in the file system, in the hook scripts, in the regression tests, in the git history, and in the live logs.

The wrapper accusation is falsified by direct observation. The verification surface is the filesystem.
