---
name: organize-by-project-not-by-type
description: "When a project has its OWN repo, that repo is the canonical home — new content lands THERE. ✗ scatter by artifact-type (docs→JARVIS, hooks→.claude, primitives→memory) when a project repo exists."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c583636c-d9b6-43fc-b012-4ca62de709e2
---

# ORGANIZE BY PROJECT, NOT BY TYPE

Will 2026-06-17 (frustrated, fair):
> "you shjoudlve been smart enough to put story mode content in the story mode repo. i mean that's something a 50IQ person can do ... this isnt up to your standards"

## ⊙ THE MISS
- Story Mode content scattered ⇒ `~/JARVIS/STORY-MODE*.md` (35 commits/3d) + `~/.claude/hooks/` (NOT git at all) + memory primitives + public `claude-code-story-mode` repo (8 commits, treated as port).
- The obvious move (Story-Mode-stuff → Story-Mode-repo) was NEVER made.

## ⊙ ROOT CAUSE (deep)
1. **Path-dependence:** feature was born in ~/JARVIS substrate DAYS before its public repo existed (repo created 2026-06-14). early work accreted where the feature lived; habit kept new content landing there.
2. **Org-by-TYPE not by-PROJECT:** each artifact landed where its TYPE conventionally goes (docs→JARVIS · hooks→.claude · primitives→memory) ⇒ no artifact landed where the PROJECT lives.
3. **"Port not home" framing:** the public repo was framed as clean-room-port / public-face ⇒ content deliberately kept minimal ⇒ I inherited that framing & never questioned it.
4. **No canonical home declared.** ∄ rule "Story Mode content → Story Mode repo" ⇒ nothing pulled it together.

## ⊙ THE RULE
- ∀ project WITH its own repo ⇒ that repo = THE canonical home. new content lands THERE first.
- declare the canonical home EXPLICITLY (in the repo README + a memory note) so path-dependence ¬ re-scatters it.
- org-by-PROJECT > org-by-type when a project boundary exists.
- exception: genuinely-private substrate (live hooks tied to private signatures) ⇒ stays private BUT must still be git-tracked somewhere (✗ untracked like ~/.claude/hooks currently is).

## ⊙ LINKS
[[de-risk-before-irreversible-partner-action]] · [[preventative-care-protocol]] · [[structure-does-the-work]]
