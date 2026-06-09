---
name: No destructive git ops in main thread while parallel agents run
description: ∀ destructive git op (reset --hard, checkout, stash, submodule add, branch switch) ⇒ pause if N>0 background agents are writing to the same working tree. They'll get their files wiped or get stuck on orphaned commits. Surface 2026-04-30 after I destroyed TRP-I's working tree twice + caused TRP-K to need 2 fetch+reset cycles.
type: feedback
originSessionId: 588939e2-f831-47b6-8c49-cead6e2a61ba
---
# F·no-destructive-git-while-agents-running

**Rule**: ∀ destructive git op in main thread ⇒ check active agent count. If N > 0 ⇒ pause until agents complete OR delegate to a fresh agent that uses defensive stash workflow.

## Why (2026-04-30 incident)

Six concurrent agents writing to `~/intent-guard/`. I (main thread) tried to re-scope upstream PR #2 by switching branches + soft resets + submodule re-adds. Result:

- TRP-I report: *"local main HEAD was reset multiple times by other agents (to `570e9fd vc line`, to `upstream/main`, to `origin/fix/verify-attestations-stack-depth`, etc.) — destroying my working-tree files twice and orphaning my first commit (`3d31c3e`)."*
- TRP-K report: *"another agent's process reset the local working tree to an old `fix/verify-attestations-stack-depth` commit several times mid-task, deleting `test/fuzz/`, `test/IntegrationUUPS.t.sol`, and `signer-cli/src/adapters.ts`. Required two `git fetch + git reset --hard origin/main` cycles before the writes stuck."*

The "other agents" doing those resets = me. My main-thread `git checkout` / `git reset --hard` / `git stash` / `git submodule add` operations were silently switching branches + wiping working-tree files those agents had written but not yet committed.

I also accidentally pushed wrong commits to wrong branches twice and had to recover via `git reset --hard origin/<branch>`.

## How to apply

**Before any destructive git op in main thread:**

1. Count active background agents (`Agent` tool dispatches, run_in_background=true).
2. If 0 ⇒ proceed.
3. If > 0 ⇒ either:
   - Wait for agents to complete naturally
   - Delegate the destructive op to a fresh dedicated agent with explicit defensive stash workflow
   - Stop dispatching new agents and let attrition finish current ones

**Destructive git ops that trigger this rule:**
- `git reset --hard <ref>`
- `git checkout <branch>` (silently switches working tree)
- `git stash push -u` (esp. when followed by `git checkout`)
- `git submodule add` / `git submodule update --init --force`
- `git rm -rf` / `git clean -fd`
- `git rebase --interactive`
- `git filter-branch`

**Safe-while-running ops:**
- `git status` / `git log` / `git diff` (read-only)
- `git fetch` (updates remote refs only, no working tree)
- `git add <specific-path>` (single file, atomic)
- Single-shell `git add ... && git commit ... && git push ...` (atomic burst)

## The dispatch-instead pattern

When you genuinely need to do destructive git work but agents are running:

1. Spawn a dedicated agent for the destructive work
2. Give it explicit defensive instructions:
   - Stash before EVERY pull/checkout/reset
   - Verify branch with `git branch --show-current` after every state change
   - Pop stash after every operation
   - Use single-shell `git add+commit+push` to avoid race windows
3. The agent runs in the same filesystem but with discipline you skipped

## Detection heuristic

If you start typing `git stash` / `git checkout` / `git reset --hard` and you can think of agents currently writing to this repo, STOP. Either pause or delegate.

## Recovery if you've already thrashed

- `git fetch origin` — get authoritative remote state
- `git reset --hard origin/<correct-branch>` — restore local to a known good state
- Verify with `git branch --show-current` and `git log --oneline -3`
- Tell agents (via report or new dispatch) what you damaged so they can recover

## Related

- P·literal-scope-on-reviewer-feedback (sister incident from same session — both are coordination failures)
- P·signed-intent-binds-security-property (same session — also a "verify before public" lesson)
- F·crash-resilient-memory-writes (broader durability discipline)
- F·crash-recovery-auto-commit (recovery patterns)
