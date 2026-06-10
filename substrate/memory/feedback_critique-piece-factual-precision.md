---
name: CritiquePieceFactualPrecision
description: 2026-05-02 — pieces critiquing rigor are self-delegitimizing on factual error. Verify dates from source, never paraphrase recency.
type: feedback
originSessionId: df9b8357-2f96-4532-a130-12cb03f59389
---
**Rule**: ∀ piece critiquing-rigor (audits, security, sci-method) ⇒ factual-precision = load-bearing. dates ∧ cycle-#s ∧ actor-IDs ∧ versions ⇒ verify-from-source-doc BEFORE write, ¬ paraphrase-from-intuition. one-wrong-fact ⇒ delegitimize structural-arg.

**Why**: 2026-05-02 wrote *"Polkadot disclosed last week"* in audit-fix-introduces-bug Medium-draft. Actual: forum-post 2026-03-19 (~6wk prior). Will-call:
> *"getting a date wrong in a paper criticizing security audits is a failure mode. you can offer all this wisdom but one date can completely delegitimize you."*

Piece-arg = audit-time Q: *"does new-code preserve old-code's safety-props?"* — answered NO for me on recency-claim. Same failure as bug-critiqued.

**How**:
- ∀ recency-phrase ("last week", "yesterday", "recently") ⇒ STOP ∧ source-lookup. unknown-source ⇒ vague-defensible ("earlier this year") ∨ ask-user.
- ∀ named-entity (person, org, version) ⇒ verify spelling + ID from source
- ∀ URL/domain/handle (vibeswap.fi vs usd8.fi, @username, github-org) ⇒ verify-from-source ∨ ask-user. ✗ pattern-match-similar-project's-URL.
- ∀ count-claim ("3 instances", "200+ patches") ⇒ verify ∨ drop-count
- ∀ cycle/PR/commit-# ⇒ verify-against-git
- High-cost: security-writeups ∧ audit-critiques ∧ partner-facing (Rick/[REDACTED-NDA]/Medium) ∧ formal-papers
- Low-cost: internal-scratch ∧ dev-chat ∧ conv-prose ⇒ paraphrase-OK
- Detect: phrase-asserts-fact-from-world (¬ structural-claim) ⇒ source-verify-gate

**Apply @ draft-time** ¬ review-time. user ✗ gate ∀ date-verify; writer ✓ gate.

**Connected**:
- `[P·anti-stale-feed-protocol]` — parent
- `[P·text-to-code-verify-first]` — sibling (doc→code verify)
- `[F·verify-credentials-before-publishing]` — sibling (creds in public)
- `[P·empty-repo-test]` — sibling (reconstructive standard)
