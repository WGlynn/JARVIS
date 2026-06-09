---
name: SyncPrimitiveMonorepoVsCurrentState
description: "∀ public-facing description-doc (root README, layer README, ARCHITECTURE.md, papers/README index) ⇒ fact-check claims against current substrate state. If \"we have X\" understates / overstates / mis-names what's actually present ⇒ surface delta ⇒ update doc. \"151 primitives\" today might be 167; \"60 papers\" might be 73; \"three gates\" might be four. Sync-gap ≡ structural-honesty violation. Captured 2026-06-09 18:18 ET ⇐ Will: *\"Fact check the repo against what we have, in case you look at something and say 'hey we have expanded on X or we have more than just Y now' that's the sync primitive.\"*"
type: feedback
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[F·sync-primitive-monorepo-vs-current-state]**

## ⚙ Rule

∀ public-facing description (README ∨ ARCHITECTURE ∨ index page) ⇒ fact-check claims against current substrate state

Sync-checks per artifact-class:

| Class | Claim shape | Verification method |
|---|---|---|
| primitive counts | "151 primitives + 123 feedback" | `ls memory/primitive_*.md` + `ls memory/feedback_*.md` |
| paper counts | "60+ published papers" | `ls papers/*.md` + check live count |
| gate enumerations | "Substance gate + HIERO" | grep README for gate-name list vs actual hooks present |
| layer artifacts | "TG bot suite, signature validator, jarvis-network" | check each named artifact exists at the linked location |
| layer dependencies | "Layer X depends on Y" | grep composes-with refs in primitives matches stated topology |
| repo-link health | "lives at github.com/X/Y" | verify URL resolves + repo not archived/moved |

⇒ stale-claim ≡ structural-honesty violation per [P·honesty-as-structural-load-bearing-property]
⇒ ∀ stale-claim ⇒ surface delta ∨ update inline

## 🎯 Why this matters

Public-facing descriptions are the substrate's interface to outside readers. Outdated counts read as either:
- ✗ marketing inflation ("we have 60 papers" when 50 exist)
- ✗ marketing deflation ("we have 151" when 167 exist, undersells)
- ✗ broken-link surface (a reader clicks "TG bot suite" → dead-link → trust collapses)

Per [P·time-logic-anti-hallucination-gate] sibling: "verify-then-assert" applies to counts and inventories as much as to durations.

## 🎯 When to apply

- ∀ merge-of-repos event ⇒ run sync-check on root README of destination
- ∀ "let me check the monorepo" Will-prompt ⇒ this rule fires
- ∀ new layer-essay added ⇒ check parent layer's README claims for staleness
- ∀ paper added ⇒ check papers/README index
- weekly ∨ monthly cadence ⇒ scheduled cron candidate

## 🎯 Format of delta-surfacing

```
## Sync delta: <doc-path>
- "X" claim: <stated value> → <actual value>
- "Y" claim: <stated value> → <actual value>
- Suggested edit: <patch>
```

⇒ Will sees the delta as a structured patch-proposal, not a vague "stuff is out of date"

## 🪝 Triggers

- ∀ Will surfaces "fact check the repo" ⇒ this rule fires
- ∀ "we have expanded on X" intuition ⇒ confirm vs current state ⇒ surface or update
- ∀ public-repo push that adds substrate ⇒ check parent description for staleness
- ∀ paper-publication ⇒ check papers/README index for update gap

## ✗ Anti-patterns

- ✗ assume root README is current ⇒ public-docs decay fastest
- ✗ update count number w/o verifying ⇒ confabulation w/ extra steps
- ✗ over-survey (recount everything every session) ⇒ scope to changed-areas
- ✗ fix one number, miss the rest ⇒ sweep adjacent claims when one is found stale

## ✓ Composes-with

- [P·honesty-as-structural-load-bearing-property] — stale-claim ≡ honesty violation
- [P·time-logic-anti-hallucination-gate] — sibling-axis verify-before-assert
- [F·websearch-before-saying-i-dont-know] — sibling verify-before-deny
- [F·dont-default-concede-verify-first] — parent verify-first generalized
- [F·primitive-capture-vs-execution-throughput] — this primitive captured because Will surfaced the gap mid-execution
- [P·anti-amnesia-protocol] — stale-doc ≡ amnesia leak

## 📦 Receipts

- 2026-06-09 18:13 ET ⇐ Will: *"youre just adding papers im literally talking about primitives and reinforcements and such"* (signal: monorepo updates lazy)
- 2026-06-09 18:18 ET ⇐ Will: *"Fact check the repo against what we have, in case you look at something and say 'hey we have expanded on X or we have more than just Y now' that's the sync primitive"*
- 2026-06-09 18:20 ET ⇒ this primitive saved; sync-pass on JARVIS monorepo next
