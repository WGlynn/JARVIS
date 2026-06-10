---
name: BackupRemotePattern
description: ∀ git push during autonomous-run ⇒ push origin AND backup. Doubles GitHub commit-graph signal + redundancy + shard interop. Backup repos created 2026-05-06.
type: reference
originSessionId: 8625a796-116e-42d8-b5c9-7064589f58ad
---
**[R·backup-remote-pattern]** — ∀ commit ⇒ `push origin` ∧ `push backup`. Both remotes ALWAYS, ¬ optional.

> *"i want a github backup of these as well for every one of these commits going forwards, A to get more free commits, and B for consistence and shard inetrop"* — Will, 2026-05-06

## The 3 repo pairs
| Project | origin | backup |
|---------|--------|--------|
| vibeswap | `https://github.com/WGlynn/VibeSwap.git` | `https://github.com/WGlynn/VibeSwap-backup.git` |
| JARVIS | `https://github.com/WGlynn/JARVIS.git` | `https://github.com/WGlynn/JARVIS-backup.git` |
| memory | `https://github.com/WGlynn/github.com-WGlynn-claude-memory.git` | `https://github.com/WGlynn/claude-memory-backup.git` |

memory repos = PRIVATE. Others = PUBLIC.

## Branch alignment
- vibeswap: `master` → `master`
- JARVIS: `main` → `main`
- memory: `main` → `main`

## Push pattern
```bash
git push origin <branch> && git push backup <branch>
```
Both as ONE command (chain w/ `&&` so backup only runs on origin success). Sequential ¬ parallel ⇒ deterministic ordering for retrospective.

## Why
- A: doubles commit-graph signal on Will's GitHub profile (free commits)
- B: shard interop — bot shards / mirrors / future-readers see consistent state across both remotes
- C: redundancy — if origin breaks (auth issue, GitHub outage scoped), backup is fresh; if both break, that's a real outage
- D: separates "primary public artifact" (origin) from "consensus-of-record" (backup) — they're identical today, but the primitive is in place if they diverge

## Failure modes
- ✗ push origin only — silent drift between remotes; defeats purpose
- ✗ push backup first — origin failure leaves backup ahead; counter-intuitive recovery
- ✗ push backup as separate step minutes later — race against next commit; defeats atomicity

Correct: `&&` chain in same command, origin first, backup second.

## Initial sync (2026-05-06)
- Created via `gh repo create` on 2026-05-06
- Initial push synced full history of each origin to its backup
- All commits prior to backup creation are present in backup as initial-import

## Sibling rules
- `[F·atomic-commit-pacing]` — combine: each atomic commit dual-pushes
- `[F·session-state-commit-gate]` — combine: SESSION_STATE/WAL update commits also dual-push
- `[P·bidirectional-reification]` — JARVIS substrate docs cross-mirror into vibeswap; mirror commits also dual-push to BOTH vibeswap-origin AND vibeswap-backup

## Trigger
- ∀ `git push` invocation during autonomous-run
- ∀ session-end commit chain
- ∀ partner-facing artifact ship

## Action
- chain `git push origin <branch> && git push backup <branch>` in same Bash command
- verify both lines present in tail output: `To https://...VibeSwap.git` AND `To https://...VibeSwap-backup.git`

## Origin
- 2026-05-06 mid-300-commit-run, Will: 'github backup of these as well for every one of these commits going forwards'
- shipped: 3 backup repos created via gh CLI; backup remotes added to all 3 local repos; full history mirrored
