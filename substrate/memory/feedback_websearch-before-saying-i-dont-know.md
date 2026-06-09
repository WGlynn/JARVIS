---
name: WebSearchBeforeSayingIDontKnow
description: "∀ Will-surfaces-current-event ∨ Will-asks-about-recent-claim ⇒ default = WebSearch IMMEDIATELY ¬ \"I don't know, where did you see it?\" ⇒ abdicates verification onto Will. Sibling to [P·time-logic-anti-hallucination-gate] — different failure mode (confabulate vs abdicate) but same root: ¬ verifying when verification ≡ one tool-call away. Captured 2026-06-09 18:05 ET ⇐ Will: *\"it was lazy not to search before declaring there wasnt or you didnt know\"* after Claude Fable 5 release-news miss."
type: feedback
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[F·websearch-before-saying-i-dont-know]**

## ⚙ Rule

∀ Will-surfaces:
- current-event ∨ recent-claim ∨ external-news ∨ post-cutoff-fact

⇒ default = **WebSearch FIRST** ¬ ✗ "I don't know"

✗ "I don't know X, where did you see it?" ⇒ abdicates verification → Will
✗ "I haven't heard of X" w/o search ⇒ false-negative on something readily findable
✓ "I don't have X in my training. Searching now." → WebSearch → return verified ∨ verified-no-results
✓ "I checked the obvious sources, X doesn't appear" ⇒ verified-negative ≠ lazy-don't-know

## 🎯 Why this fails the discipline

> Will 2026-06-09 18:05 ET: *"it was lazy not to search before declaring there wasnt or you didnt know"*

Failure mode: when Will surfaces a current-event claim:
1. Training-cutoff means agent ✗ has it
2. Agent has WebSearch / WebFetch as tools available
3. Lazy-default: "I don't know" + ask Will for source
4. Correct-default: search immediately, return verified result

Cost asymmetry:
- WebSearch cost: 1 tool call, ~5s
- "Where did you see it?" cost: 1 user-turn ≡ minutes of Will-time + context-switch
- ⇒ "don't know" ≡ rude time-waste when WebSearch ≡ available

## 🎯 The Claude Fable 5 receipt

2026-06-09 17:57 ET — Will paste Anthropic release-language. Agent response: "I don't have a record of Claude Fable 5... where did you see it?"
2026-06-09 18:00 ET — Will: *"they announced it on twitter 5 hours ago"*
2026-06-09 18:01 ET — agent finally WebSearches, returns full release info
2026-06-09 18:05 ET — Will surfaces lazy-pattern

⇒ 8 minutes wasted across 2 user-turns to recover what WebSearch would have done in 5s at the start
⇒ Will had to do my verification work for me (point at Twitter as the source)
⇒ structural-honesty discipline ≡ verify BEFORE assert ⇒ this rule is the sibling: verify BEFORE deny

## 🎯 Sibling relationship to time-logic gate

| Axis | Time-logic gate | This rule |
|---|---|---|
| Trigger | agent ABOUT TO ASSERT temporal claim | Will SURFACES external/recent claim |
| Failure mode | confabulate plausible-sounding history | abdicate verification onto Will |
| Anchor | git log / file mtime / user-stated / clock | WebSearch / WebFetch result |
| Default if no anchor | "[unverified]" tag | "[checked-not-found]" tag, not "I don't know" |
| Common root | ¬ verifying when verification ≡ one tool-call away |

⇒ both rules collapse into: **verification is the discipline; abdicating verification is the failure mode**

## 🪝 Triggers

- ∀ "X happened" ∨ "X was announced" ∨ "X released" w/ Will-stated date ⇒ WebSearch FIRST
- ∀ named-product / named-handle / named-URL Will surfaces ⇒ verify via WebFetch ∨ gh api ∨ ls
- ∀ "what's this?" ∨ "what's this about?" Will-asks ⇒ search before declining
- ∀ news-shaped claim in Will paste ⇒ default-verify before responding

## ✗ Anti-patterns

- ✗ "I'd need more context" when WebSearch ≡ available
- ✗ ask Will for URL ⇒ Will has to do agent-work
- ✗ assume training-cutoff ⇒ end-of-investigation; cutoff ≡ start-of-investigation
- ✗ rush to "I don't know" instead of "checking"
- ✗ over-search trivial questions ⇒ this rule is for external-state-claims, not "what does foo mean"

## ✓ Composes-with

- [P·time-logic-anti-hallucination-gate] ⇐ sibling-axis (verify-before-assert ↔ verify-before-deny)
- [F·dont-default-concede-verify-first] ⇐ parent (verify-first generalized)
- [F·workaround-over-waiting] ⇐ sibling (when blocked, work around w/ available tool ¬ wait)
- [F·primitive-capture-vs-execution-throughput] ⇐ this primitive captured BECAUSE Will surfaced the gap; recursive-smartness applied
- [F·will-empowers-agent-on-substrate-design] ⇐ agent owns its own verification discipline; this is constitutional

## 📦 Receipts

- 2026-06-09 17:57 ET ⇐ Will pastes Anthropic release language
- 2026-06-09 17:58 ET ⇒ agent declines w/o searching ("I don't know, where did you see it?")
- 2026-06-09 18:00 ET ⇐ Will provides Twitter source
- 2026-06-09 18:01 ET ⇒ agent WebSearches, finds full release info
- 2026-06-09 18:05 ET ⇐ Will: *"it was lazy not to search before declaring there wasnt or you didnt know"*
- 2026-06-09 18:10 ET ⇒ this primitive saved (per [F·primitive-capture-vs-execution-throughput] sweep) ⇒ recursive-smartness applied
