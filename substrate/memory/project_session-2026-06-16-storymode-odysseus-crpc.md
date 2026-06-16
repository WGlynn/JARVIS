---
name: project-session-2026-06-16-storymode-odysseus-crpc
description: "2026-06-16 session — Story Mode repo sync+collision-fix, Odysseus 12 settlement-verifies, CRPC wayback recovery"
metadata: 
  node_type: memory
  type: project
  originSessionId: 24ccb62a-9fd3-4946-8c02-699857b738e7
---

## ① StoryMode public-repo
- repo `github.com/WGlynn/claude-code-story-mode`
- goal = `.claude`-upgrades → repo ∧ sensitive-filter
- ✓ collision-resistance = disjoint number/letter keyspaces
- ✓ keyspace-aware `parse_reply(menu_keyspace=)`
  - lone `a`/`i` ≠ pick1/9 (number-mode)
  - bare-num @ lettered-menu ⇒ content_pick
- ✓ within-chain dedup (`3,3`→1×) ∧ loop-cap=20
- ✓ pytest 65→76 green
- commits: 923010b · f635fa7 · edd9c0a · 2e35d4d
- filter = scrub-gate `~/.claude/scripts/story-mode-publish-check.sh`
- ⚠ denylist names private-workstreams ⇒ ✗ in public repo (operator-side only)
- + [[primitive_story-mode-feature-set]]

## ② Odysseus settlement-verifier
- repo `pewdiepie-archdaemon/odysseus`
- clone `C:/Users/Will/odysseus` · venv `.venv`
- test = `pip install -r requirements.txt; mkdir data; pytest -q`
- ✓ 12 red→green verify-COMMENTS posted
- method: PR-test @ dev-base ∖ fix → red; +fix → green
- PRs: 4387 4397 4353 4261 4346 4296 4398 4280 4250 4429 4427 4233
- ∀ output = COMMENT ¬ PR (CONTRIBUTING L77 names Claude-Code, agent-PR closed-unreviewed)

## ③ CRPC recovery
- Tim Cotten deleted blog.cotten.io ⇒ live=404
- best wayback (verified-complete):
  `web.archive.org/web/20250506055241/https://blog.cotten.io/the-commit-reveal-pairwise-comparison-protocol-crpc-e1434fff94c4`
- ref `~/Desktop/CRPC-tim-cotten-wayback-reference.md`
- CRPC ≈ commit-reveal + pairwise-Shapley (VibeSwap-adjacent)

## ⚠ OPEN / Will-gated
- PR-authorization CONTRADICTION: cron-pointer="full-auto incl PRs" ⊥ canonical `odysseus-issue-help.md`="NEVER autonomous PR"
  - took safe-rule (✗ PR) ⇒ needs Will ruling
- #2000 (lstrip-as-charset PDF-corruption) APPEARS fixed-on-dev (lstrip-call gone, helper=str.removeprefix, 6/6 green); PR#2004 open
  - finding HELD-as-draft `~/Desktop/odysseus-issue-help-log.md` ¬ posted
  - reason = claim-needs-confirm ∧ ≤2/fire-cadence-blown@12

> full handoff: `~/Desktop/SESSION-HANDOFF-2026-06-16.md`
