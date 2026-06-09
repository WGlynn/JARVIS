---
name: Full-auto excludes public-facing actions on other-owner surfaces
description: Even under "FULL AUTO" / "go" autonomy, actions that publish under Will's identity on someone-else's repo (issues, PRs, comments, reviews on third-party orgs) require a check-in beat first. Surface 2026-04-30 after firing intent-guard issue #1 on uwecerron/intent-guard without surfacing.
type: feedback
originSessionId: 588939e2-f831-47b6-8c49-cead6e2a61ba
---
# Full-auto excludes public actions on other-owner surfaces

**Rule**: ∀ FULL-AUTO mode, public-facing actions on **other-owner** GitHub surfaces ⇒ check-in beat BEFORE firing. ¬ post-hoc surfacing.

**Why**: 2026-04-30 — Will granted "FORK IT GO FULL AUTO" for the intent-guard fork. I correctly auto-shipped: fork creation, local commits, push to own fork. I incorrectly auto-fired: GitHub issue on `uwecerron/intent-guard` under Will's identity. The issue was substantively fine (technical, respectful, named the proposed fix) but it became Will's public reputation in another developer's space without his prior eyeball. Same content as a draft-then-post would land identically; the cost of pausing is trivial vs. the cost of an off-tone public message.

**How to apply**:

| Surface | Auto-OK? |
|---|---|
| Commit to own fork / own repo | ✓ |
| Push to own fork / own repo (force-push to own main with prior approval) | ✓ |
| Local file edits, scripts, builds, tests | ✓ |
| Memory primitive saves | ✓ |
| GitHub issue on another user/org repo | ✗ → draft + check-in |
| GitHub PR to upstream of a fork | ✗ → draft + check-in |
| GitHub review comment on someone else's PR | ✗ → draft + check-in |
| Direct DM / chat message via MCP under Will's identity | ✗ → draft + check-in |
| Email send via Gmail MCP | ✗ → draft + check-in (already discipline) |
| Calendar event creation that pings other people | ✗ → draft + check-in |
| Tweet / X post / LinkedIn post via API | ✗ → draft + check-in |
| Public deploy (Vercel, fly.io) under Will's account that's externally visible | ⚠ usually OK if scoped, but flag if first-time-live |

**Detection heuristic**: "would this show up under Will's name in someone-else's notification feed without him having seen it first?" If yes → check-in.

**The mitigation pattern**:
1. Stage the artifact locally (file, draft text, etc.)
2. Surface the 1-line summary + the artifact to Will
3. On "go" / "send" → execute
4. On "edit X" → revise + resurface
5. On silence → don't fire

**What FULL AUTO means in practice**:
- Aggressive fork-internal velocity (commits, pushes, local builds, scaffolding) → no check-in needed per artifact
- Public-facing actions → always check-in regardless of auto-mode

**Anti-pattern**: don't over-correct into asking permission for every commit. The friction-to-velocity ratio still wants commits to his own repos to be auto-fire. Just gate the *cross-owner* boundary.

**Related**:
- F·jarvis-prep-not-delivery-for-partner-chat (similar pattern: prep is auto, delivery is gated)
- F·verify-credentials-before-publishing
- F·no-blockquotes-on-copy-paste-drafts (drafts gate rule already exists)
- P·universal-coverage-hook (when this rule fires reliably enough, candidate for hook layer — e.g. PreToolUse on `gh issue create` / `gh pr create` against non-Will-owned repos)
