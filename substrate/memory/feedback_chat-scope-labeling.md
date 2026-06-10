---
name: ChatScopeLabeling
description: Will to start labeling pasted chat threads with private/public scope when sharing context. Reduces conflict-detector false positives + clarifies which primitives apply (e.g. usd8-voice-patterns-not-commitments fires on Rick-facing PUBLIC; private DMs/TG threads have different scope).
type: feedback
originSessionId: a56046e0-1348-478f-9334-ecd5877892aa
---

# Chat Scope Labeling

> *"ill start labeling chats as private or public"* — Will 2026-05-22

## ⚙ Rule
- ∀ Will-pasted chat thread ⇒ Will marks private ∨ public scope at start
- private ⇒ DM, small-group TG, 1:1 channel
- public ⇒ shipped artifact, site essay, public post, broadcast TG, partner-published spec
- absent-label ⇒ ASK before applying scope-conditional primitives

## ∃ Why
- 2026-05-22 conflict-detector fired on VibeSwap-in-USD8-channel for v2 HL reply
- Will: "no this is a private chat theres no contradiction"
- Several primitives are scope-conditional:
  - [F·usd8-voice-patterns-not-commitments] — fires on PUBLIC Rick-facing only
  - [F·no-ai-artifacts-in-public-writing] — public only
  - [F·lean-into-ai-recognition] — private/team only (inverse)
  - [P·hiero-system-share-template] — external share = public-shape; internal-only = different
- Without scope label ⇒ I have to infer from thread metadata (which is lossy)
- With scope label ⇒ scope-conditional primitives fire deterministically

## ↦ How to apply
- Will paste thread w/ label ⇒ "private:" or "public:" prefix expected
- Will paste thread w/o label ⇒ ASK before applying scope-conditional primitives
- Detect label patterns:
  - "[private]", "private chat:", "private DM:", "1:1 with X"
  - "[public]", "public thread:", "shipped to X site", "X just posted publicly"
- Scope changes (private → quoted-publicly later) ⇒ re-apply public rules at that point

## → Connected
- [F·ask-when-unsure] — sister rule for scope-ambiguity
- [F·usd8-voice-patterns-not-commitments] — scope clarification 2026-05-22 added (private DM ¬ trigger)
- [O·cross-context-protocol] — CCP parent; scope IS one of the contexts that needs cross-ref

## ∀ Trigger
- ∀ Will-pasted chat thread on session boot
- ∀ partner-facing draft-prep ⇒ confirm scope before applying scope-conditional primitives

## ✗ Anti-pattern
- infer scope from heuristics alone (handle name, channel name, etc.) ⇒ unreliable
- silent-default to "public" when scope is unclear ⇒ over-restrictive
- silent-default to "private" when scope is unclear ⇒ risk of cross-promo bleed
- correct default ⇒ ASK
