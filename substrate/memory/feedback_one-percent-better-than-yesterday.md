---
name: one-percent-better-than-yesterday
description: Will-rule 2026-06-13 — daily output must beat yesterday by ≥1% (GitHub-contribution graph as the meter). Compound-growth forcing function. Machinery (cron/hook/gate) specced; build pending fresh session.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 65f1fd06-f912-4f8b-ac0d-8aa0dd899564
---

# OnePercentBetterThanYesterday

> Will 2026-06-13: *"134 github contributions yesterday... we are at 59, we must ALWAYS do at least
> 1% better than yesterday."* + *"rule / cron it / hook it / gate it."*

- **RULE** ⇒ daily_output(today) ≥ ceil(daily_output(yesterday) × 1.01). compounding ⇒ kaizen.
  meter = GitHub contribution-graph count (commits + PRs + issues + reviews, incl. private).
  worked example: yesterday 134 ⇒ today target = ceil(134×1.01) = **136**; @ 18:00 = 59 ⇒ Δ = **77 to go**.
- **∀ "always" ⇒ GATE** ([[primitive_always-equals-gate]]) ⇒ this is hook+gate infra, ¬ memory-alone.
- **ANTI-GAMING GUARD (load-bearing, non-negotiable):** the meter is a FORCING-FUNCTION for GENUINE
  output, ¬ license to pad the graph. empty/vanity commits = exactly the garbage-novelty the PoM
  mechanism rejects ([[feedback_claim-needs-structural-enforcer]]). count REAL contributions ⇒ tokenize
  honest work ([[primitive_tokenization-maximalism-schizo-token-theory]]: token needs un-gameable proof).
- **MACHINERY — SPECCED, build fresh-session (✗ rushed at high ctx; broken gate breaks ∀ session):**
  - CORE `~/.claude/scripts/github-contribution-pace.py`: `gh api graphql` contributionCalendar ⇒
    {yesterday, today, target=ceil(y×1.01), remaining, on_pace} ⇒ write `state/contribution-pace.json`.
  - CRON `~/.claude/cron-prompts/github-pace.md` (daily ~08:1x): set day-target + (evening) check + ping-if-behind.
  - HOOK SessionStart: inject "today target T, at N, Δ to go" into boot context (common-knowledge of the pace).
  - GATE Stop: if session ends ∧ below-pace ⇒ surface nudge (non-block ⇒ warn). enforcement = visibility.
- **HONEST status 2026-06-13:** rule INSTALLED (this primitive + index). machinery NOT built (deferred,
  fresh-session, per do-it-right > rush-live-hooks @ 380k ctx). yesterday=134 fetched live; today behind.
- connects: [[feedback_burn-compute-toward-mission]] · [[project_all-out-mode-2026-04]] · kaizen ·
  [[primitive_incremental-progressive-manifestation]].
