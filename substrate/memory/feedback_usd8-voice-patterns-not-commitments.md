---
name: USD8 Voice — Patterns Available, Not Commitments Made
description: When writing USD8 / Rick-facing material, frame VibeSwap patterns as architectural OPTIONS available to USD8, NOT as commitments USD8 has made. USD8 is Rick's project; VibeSwap implementations ¬ USD8 roadmap by default.
type: feedback
originSessionId: 79044125-45c4-486a-9ac0-ec65bb0d9b76
---
# USD8 Voice — Patterns Available, Not Commitments Made

## ⚙ Rule
- USD8 is Rick's project ¬ Will's
- VibeSwap-implemented patterns ¬⇒ USD8 commitments by default
- Frame VibeSwap patterns in USD8 context as "pattern available" / "architectural direction" / "VibeSwap is building X; USD8 has the option"
- ✗ "USD8 is building toward X" | "USD8 will X" | "USD8 commits to X" — unless Rick has EXPLICITLY committed

## Why
- 2026-04-27 incident across 4 USD8 site essays: framed "the augmented governance layer USD8 is building toward" — implied USD8 commitments Rick hadn't made
- Will caught it twice: first generally (*"just dont pretend usd8 has any augmented governance yet we are still building"*), then on a specific bullet (fact-check request that surfaced even "is building toward" overstates Rick's commitment)
- Error pattern: conflated VibeSwap's playbook with USD8's roadmap. Wrote in Will-voice as if VibeSwap-direction = USD8-direction.

## How to apply
For any VibeSwap mechanism / architecture / pattern referenced in USD8 material:

- ✗ "USD8 is building toward X"
- ✗ "USD8 will adopt X"
- ✗ "USD8 commits to X"
- ✗ "USD8's augmented governance layer"
- ✓ "the pattern X — VibeSwap is building this — is available for USD8 to adopt"
- ✓ "the architectural direction that closes this attack class"
- ✓ "USD8 has the option to adopt the same pattern"
- ✓ "VibeSwap is building this layer; USD8 has the option"

Be honest about VibeSwap's status too — partial-implementation cases require honest framing on VibeSwap side as well (e.g., "GovernanceGuard forthcoming" ¬ "GovernanceGuard deployed").

## When this applies
- ALL Rick-facing SHIP material (specs, papers, site content, audits, briefs, published docs)
- ALL USD8-related PUBLISHED writing
- ANY partner-project writing where the partner has their own decision-making authority
- Any "we ↔ they" framing where "they" haven't actually said yes

## When this does NOT apply (scope clarification 2026-05-22)
- Private TG chats / DMs where another participant explicitly pulls for VibeSwap context
- 1:1 conversations w/ USD8-circle contacts who are keen to learn VibeSwap (HL | CKBased.bit, etc.)
- The primitive's load-bearing concern is "VibeSwap promo bleeding into Rick's PUBLIC domain". Private-channel teaching answers to genuinely-curious participants ¬ violate this.
- Detection: published artifact (site, spec, audit, public post) ⇒ rule applies. Private 1:1 / small-channel chat w/ pull-for-context signal ⇒ rule does NOT apply.

## Distinct from
- VibeSwap material itself (Will's project, Will commits, present-tense for deployed code is fine)
- Pure mechanism-design discussion abstracted from any specific protocol (no commitment claim involved)
- Things Rick HAS publicly committed to (use those directly)

## Anti-pattern
- Will-voice for Rick's project ⇒ implicit commitments on Rick's behalf
- Asserting VibeSwap implementations as USD8 plans ⇒ overclaim
- Failing to distinguish VibeSwap-deployed | USD8-adopted | USD8-considered | USD8-could-adopt
- "USD8 is building toward [specific architecture]" without Rick's published commitment to that specific architecture

## Sister rule — No VibeSwap self-promo in USD8/Rick-facing material
- 2026-04-27 incident extension: even brief "VibeSwap is building this; USD8 has the option" framings read as VibeSwap promo on Rick's site
- Will: *"hey no vibeswap self promotion in these docs"*
- Rule ⇒ ALL VibeSwap references stripped from USD8/Rick-facing site content, partner specs, audits
- Substitute neutral attribution: "production implementations exist to draw from" | "established mechanism-design pattern" | "the architectural direction" | "drawn from existing playbook"
- Rick's site is for USD8, not for cross-promoting Will's other work
- If Rick wants to invoke VibeSwap, that's his call ¬ ours

## Detection heuristic
Before shipping any USD8-facing draft, grep for:
- "USD8 is building" | "USD8 will" | "USD8's [architecture name]" | "USD8 commits"
- For each match: is this Rick's published commitment? If no ⇒ reframe as "pattern available" / "architectural direction" / "USD8 has the option"
- ALSO grep for "VibeSwap" — every match in USD8-facing material gets removed or replaced with neutral framing
- Both checks run before render. The corpus has no VibeSwap mentions in Rick-facing site content unless Rick has explicitly invoked the comparison.

## Related
- `feedback_voice-source-conversation-history` — sister rule on voice sourcing
- `feedback_rick-keep-it-simple` — sister rule on Rick-facing material discipline
- `feedback_have-my-back-operational-definition` — Rick is now a partner; respect his decision-making authority
- `P·anti-hallucination-protocol` — BECAUSE / DIRECTION / REMOVAL test catches commitment-overclaims at write-time
