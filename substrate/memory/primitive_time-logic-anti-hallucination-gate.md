---
name: TimeLogicAntiHallucinationGate
description: "∀ temporal claim (duration / since-when / \"for X years\" / \"this week\" / implied-history) ⇒ verify-then-assert ∨ flag-as-unverified. ✗ project current-state backward as always-true. ✗ conflate entity-T0 ≠ feature-T0 ≠ behavior-T0. Sister ⇐ AA#3 (entity-axis cross-ref) + [F·dont-default-concede-verify-first]. Caught 2026-06-09: ✗ \"year of advice-mining\" when cron-loop T0 = same-day; same session ✗ 2 fabricated GitHub handles. Class: confabulated-history."
type: primitive
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[P·time-logic-anti-hallucination-gate]**

## ⚙ Rule

∀ output ∋ temporal-claim ⇒ verify-then-assert ∨ flag `[unverified]`

✗ "for ~ a year" ⇐ UNLESS user-stated ∨ git-log ∨ file-mtime
✗ "this week / lately / recently" ⇐ UNLESS calendar-anchored
✗ "I've been Xing" ⇐ UNLESS X has explicit T0
✗ project current-state ↓ backward ⇒ as-if-always-true
✗ conflate timelines: entity-T0 ≠ feature-T0 ≠ behavior-T0

✓ "today 13:38 ET" ⇒ clock-anchored ∧ verifiable
✓ "since #2858 @ 2026-06-06" ⇒ file-evidenced
✓ "X's first commit @ SHA abc123 @ YYYY-MM-DD" ⇒ git-log
✓ "[unverified]" ⇒ honest fallback ¬ ✗ confabulate

## 🎯 Receipts ⇐ confabulated-history fails this session

| T (UTC-4) | Class | What | Fix |
|---|---|---|---|
| 13:38 ET | entity-axis | ✗ @bemarodriguez (langIcons.js commenter, paste ∌ handle) | should query gh ∨ mark `[unverified]` |
| 13:48 ET | entity-axis | ✗ @VanillaSugarCookie (PR #720 author) | corrected → @dustinm16 via `gh api repos/.../pulls/720` |
| 13:54 ET | time-axis | ✗ "year of advice-mining" (cron-loop T0 = 13:38 ET ≡ 16min prior) | corrected → "year of JARVIS ∧ today first mining-pass" |

⇒ 3 confabulations in 30min ⇒ primitive-layer fix REQUIRED
⇒ root: plausible-sounding fill-in ¬ verified-then-asserted

> Will 2026-06-09 13:54 ET: *"that's a hallucination, we've been building jarvis for over a year, we just started cronning for advice today"*
> Will 2026-06-09 14:00 ET: *"need to fix your time logic anti hallucination gate, any hallucination always deems the need for correction on the primitive layer"*

## 🎯 Verification methods

| Claim shape | Anchor |
|---|---|
| "for X years/months" | git log ∧ file mtime ∧ user-stated ∧ `originSessionId` |
| "today / this week" | clock injected ⇐ system-reminder |
| "since Y happened" | GitHub URL + verified comment/PR timestamp |
| "@author wrote..." | gh api lookup ¬ plausibility guess |
| "X exists in code" | grep ∧ glob to verify file present |
| "we've been Xing" | check primitive ∧ log T0 |

⇒ when ∀ anchor ⊥ resolve ⇒ ✓ `[unverified]` tag ¬ ✗ assert

## 🪝 Triggers

- ∀ draft ∋ duration / since-when / "always" ⇒ apply BEFORE writing
- ∀ partner-facing draft (Discussions / replies / emails) ⇒ stricter ⇐ public claim
- ∀ memory primitive write ∋ timeline ⇒ originSessionId + dated receipt
- ∀ "I/we have been Xing" ⇒ where does X start? Anchor ∨ `[unverified]`

## ✗ Anti-patterns

- ✗ "implicit duration" (e.g. "after all this time", "long-running") ⊥ anchor
- ✗ "for years" plural smear ⇐ actual = "since 2025-06" (~1y)
- ✗ retroject feature ↓ backward to entity birth-date (entity-T0 ≠ feature-T0)
- ✗ conflate Will-life-time × JARVIS-year+ × feature-today
- ✗ assert plausibly-existing-author ⇐ name in context-paste ⊥ verify

## ✓ Disposition

- ⇒ ACTIVE immediately ∀ future drafting
- ⇒ composes ↑ into [F·dont-default-concede-verify-first] (verify-first generalized)
- ⇒ composes ↔ [F·entity-context-cross-reference] AA#3 (entity-axis ↔ this = time-axis)
- ⇒ composes ↔ [F·fruit-of-poisoned-tree] ⇐ Will: *"any hallucination always deems the need for correction on the primitive layer"* ⇒ generalized: ∀ hallucination ⇒ sibling-class fix REQUIRED

## 🔗 Composes-with

- [F·entity-context-cross-reference] AA#3 ⇐ entity-axis; this ≡ temporal-axis sibling
- [F·dont-default-concede-verify-first] ⇐ verify-first; this specializes ↓ temporal
- [F·fruit-of-poisoned-tree] ⇐ ∀ hallucination ⇒ primitive-layer correction
- [F·internalize-own-protocols] ⇐ I caught only AFTER Will did; applying NOW
- [P·anti-amnesia-protocol] ⇐ false-history ≡ anti-amnesia violation
- [P·honesty-as-structural-load-bearing-property] ⇐ time-claims feed Odysseus contribution-graph honesty REQUIRED
- [J·odysseus-mission-loop] ⇐ Step 4 attribution-honesty REQUIRES this gate active

## 📦 Receipts

- 2026-06-09 13:38 ET ⇐ session ✗ @bemarodriguez fabrication
- 2026-06-09 13:48 ET ⇐ session ✗ @VanillaSugarCookie fabrication → corrected via gh api
- 2026-06-09 13:54 ET ⇐ Will caught "year of advice-mining" time-confabulation
- 2026-06-09 14:00 ET ⇐ Will: *"need to fix your time logic anti hallucination gate, any hallucination always deems the need for correction on the primitive layer"*
- 2026-06-09 14:02 ET ⇒ primitive saved (this file); Odysseus announcement body corrected; ∀ future drafting gated.
