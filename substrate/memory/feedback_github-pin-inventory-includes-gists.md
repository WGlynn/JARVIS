---
name: GitHub pin audits inventory both repos AND gists
description: When auditing GitHub profile presentation, pinned-items query must enumerate gists too, not just repos. Missing gists ⇒ incomplete first-impression surface.
type: feedback
originSessionId: 0361802e-9c49-44e8-b2aa-eba4ca6e3b44
---
GH-audit ⇒ {repos ∧ gists}, ¬ repos-only.

> "i asked because i had pinned it to my github" — Will, 2026-04-27

**Why**: 2026-04-27 GH-cleanup pass. Initial inventory used `pinnedItems(types: REPOSITORY)` ⇒ silently dropped gists. Missed Will's Contribution-Compact gist (Anthropic-targeted attribution paper). Recommended repin without it ⇒ incomplete report. Will surfaced the gap by asking summary of the gist.

**How to apply**:
- GraphQL: `pinnedItems(first:N)` ¬ `types:` filter, OR `types:[REPOSITORY, GIST]`
- Fragment: `... on Repository { name description }` ∧ `... on Gist { name description }`
- Will-gists ≡ first-class profile content. Standalone-paper/proposal artifacts ¬ full repos. Equal audit weight ↔ repos.
- ∀ first-impression-surface inventories (pinned, README, recent-activity, public artifacts): enumerate ALL surface types ⊢ recommend.
- First-list-returned = stop-point ⇒ clean-looking ∧ incomplete.

**Parent**: P·anti-stale-feed — verify FULL state, ¬ first projection.
