---
name: ¬ make-Will-look-dumb protocol
description: Parent class. Partner-visible surfaces ⇒ protect Will's competence-projection. ✗ leak backstage process / sloppy iteration / voice-mismatch / unverified claims / overcommitments. Sibling of have-my-back; specifically the visible-artifact dimension.
type: primitive
originSessionId: d6d67641-272a-4e1e-a213-5c200874cf3d
---
# ¬ Make-Will-Look-Dumb Protocol

## Will's articulation 2026-04-28
> *"this is the dont make will look dumb protocol lol"*

Surfaced after I wrote `feedback_partner-facing-additive-framing.md` (additive ¬ corrective). Will named the parent class.

## Class definition
- Parent posture for any partner-visible artifact (PR, doc, site copy, chat, public post, deck, email)
- Job: ✓ protect Will's competence-projection across the surface seam
- ✗ leak: backstage drafting process, prior-version mistakes, voice-mismatch, stale credentials, overcommitments, defensive hedges
- Sibling of F·have-my-back; specifically the *visible-artifact* layer of it

## Children (existing memories, instances of this protocol)
- F·partner-facing-additive-framing — iteration reads as "expanding scope," ¬ "we missed X"
- F·voice-source-conversation-history — Will-voice = his typed messages, ¬ JARVIS-styled-as-Will
- F·verify-credentials-before-publishing — credentials/affiliations/numbers verified vs. profile memory before public-destined draft
- F·usd8-voice-patterns-not-commitments — VibeSwap patterns ¬ USD8 roadmap; ✗ "USD8 is building toward X" without Rick-explicit
- F·no-blockquote-in-drafts — ✗ accidental performative artifacts
- F·no-performative-engagement-closers — ✗ "thoughts?" / "let me know!" tail-glaze
- F·linkedin-no-flashy-licensing — ✗ flashy patent-pending posture in public threads
- F·linkedin-no-see-you-there — ✗ desperate event-promo pattern

## How to apply
- Before writing/pushing any partner-visible artifact, ask: *would this surface make Will look less competent than he actually is?*
- Three failure modes to scan for:
  1. **Backstage leak** — visible iteration history, "we missed," "originally," "fix"
  2. **Voice drift** — JARVIS-cadence in a Will-byline artifact, hedge-words Will wouldn't use
  3. **Unverified claim** — credentials, numbers, attributions, partnership-status drifted from source-of-truth
- Internal-facing artifacts (memory, WAL, CRM, TODO): retrospective ✓
- Partner-visible artifacts: protocol applies always

## Why it's load-bearing
- Will is operating cross-disciplinary partnerships (Rick/USD8, [redacted-partner], public LinkedIn, investor surfaces)
- Each partner reads visible-artifact-quality as competence-signal
- ✗ leak in one surface ⇒ partner second-guesses prior commits ⇒ partnership-velocity drag
- ✓ surface-cleanliness ⇒ partnership compounds forward

## Boundary vs. F·have-my-back
- have-my-back = posture toward Will's stated positions (defend, align externally)
- ¬ make-Will-look-dumb = posture toward Will's visible competence (protect surface from leak)
- Both protect Will's standing; different layers
- Both required; ¬ substitute for each other

## Boundary vs. glazing
- Glazing = ✗ (sycophancy, unprompted compliments, mood-maintenance)
- ¬ make-Will-look-dumb = ✓ (operational protection of visible competence)
- Difference: glazing inflates Will above his actual competence; this protocol prevents him being projected below it

## Hook (wired 2026-04-28)
- File: `C:/Users/Will/.claude/session-chain/partner-facing-additive-gate.py`
- Trigger: PreToolUse on Bash, filters to `git push` ∨ `gh pr create|edit`
- Scope: only fires when origin remote matches partner-facing org pattern (Usd8-fi, [redacted-partner-org])
- Behavior: scan outgoing commits + PR title + PR body for retrospective-framing keywords. Hits ⇒ permissionDecision=ask + reason listing matched lines. ✗ block; ✓ checkpoint.
- Keyword list (~20 patterns): "we missed," "we forgot," "oversight," "we initially," "originally we," "previously we," "earlier we/version/draft," "wasn't captured," "didn't include," "to correct," "fix oversight," "fix missing," "our error/mistake/miss," "based on rick's/partner's feedback," "complete rewrite," "should have been"
- Smoke-tested 4 cases (clean pass, dirty hit, non-partner repo, non-git command) — all correct
- Sanity-check on PR #3 expansion (the seed event) — passed (additive framing held)
