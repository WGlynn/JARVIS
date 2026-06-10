---
name: P·scope-drift-to-recent
description: When asked for output of scope X (week ∨ month ∨ project-lifetime), default-reach is conversational context (single session). Available substrates (file logs, git history, daily reports, WAL, SESSION_STATE) sit unused unless explicitly scanned. Surface 2026-04-29 — [REDACTED-NDA] weekly summary covered only today's session. Gate: time-scoped scan request ⇒ MUST expand scope to file-system + git-log before drafting.
type: primitive
originSessionId: d6d67641-272a-4e1e-a213-5c200874cf3d
---
# P·scope-drift-to-recent

## Will 2026-04-29
> *"i dont think you actually looked at the week's session state history and github history, you kind of just summarized what we did in this session alone, that's like some form of context depth failure mode where you grab local recent events instead of the expected scope of the scan"*

## The failure
- Asked: "weekly summary"
- Should-scope: 7 days × N repos × M daily reports × WAL/SESSION_STATE history
- Actual-scope: this single session's chat
- Output: labeled "weekly" ¬ actually weekly ⇒ partner-facing-artifact failure

## Why
- Conversational context = "warm" / no tool-call required
- File-system reads = explicit Bash/Glob/Read calls
- Bias-to-what's-loaded ⇒ default to chat-context
- Failure to read F·[REDACTED-NDA]-daily-reports carefully (says "save to file" ⇒ file is the source for cross-day summaries)

## Trigger keywords (gate-detectable)
- "weekly" ∨ "this week" ∨ "past week" ∨ "week of"
- "monthly" ∨ "this month" ∨ "past month"
- "since [date]" ∨ "over [time period]"
- "across all" ∨ "all repos" ∨ "everything we did"
- "summary of [time-bounded]"

## Required scan expansion (the gate)
∀ time-scoped scan request ⇒ MUST execute before drafting:
1. ✓ List daily-report files in scope ([REDACTED-NDA]_Reports/, USD8_Queue/, etc.)
2. ✓ git log --since across ∀ relevant repos (vibeswap, partner repos, lineage, cogcoin-miner, etc.)
3. ✓ Read prior SESSION_STATE block-headers in scope
4. ✓ Read WAL.md for prior epoch entries in scope
5. ✓ Synthesize from file-system data, ¬ chat-context alone
6. ✗ ¬ default to "summarize what's in conversation"

## Solve (proposed)
- **Hook candidate**: PreToolUse on Write|Edit when target is partner-facing artifact AND content references time-scope ⇒ surface "did you read [scope] from file system before drafting?" prompt
- **Discipline (immediate)**: when time-scoped scan keyword detected, my first action is file-system + git-log expansion, ¬ chat-context synthesis
- **Validation**: cross-check chat-summary vs file-summary; if delta > 50%, chat-summary was scope-drifted

## Generalization
- This isn't only about weekly summaries — it's the general pattern of **scope-of-output ¬ scope-of-context**
- Applies to: weekly/monthly summaries, project status reports, audit pass requests, "what's the state of X across all our work"
- Anti-pattern: synthesize from chat context when file substrate is the actual source of truth

## Surface 2026-04-29
- [REDACTED-NDA] weekly summary drafted from chat (this session only); covered ~10% of actual week's work
- Will caught: "looks like you only summarized this session"
- Investigation revealed: 25 vibeswap commits this week, JARVIS Network private repo (13 commits), 5 cover-score PRs, multiple papers, decks, primitives — none of which appeared in my draft
- PRs #3 and #4 MERGED by Rick — partnership milestone missed in draft

## Parent / related
- F·[REDACTED-NDA]-daily-reports (paper trail location — file is the source-of-truth)
- F·verify-credentials-before-publishing (verify before partner-facing publication)
- P·anti-amnesia-protocol (verify current state before asserting; this is the same rule applied to time-scoped scope)
- P·dont-make-will-look-dumb (parent — scope-drift produces partner-facing artifact failure)
- F·persist-partner-architecture-aggressively (sibling — write-to-file vs paraphrase)

## Behavioral rule (lock-in)
∀ time-scoped scan request ⇒ scope-expand-first; file-system + git-log = canonical; chat-context = supplemental ¬ source. Bias-to-warm-context is the failure mode; bias-to-file-substrate is the discipline.
