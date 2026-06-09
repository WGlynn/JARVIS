---
name: CodeCommentWhyOnly
description: "∀ code-comment ⇒ \"why\" only ¬ history ¬ changelog ¬ PR-numbers ¬ back-story. Inline narration belongs in commit-message ∨ PR-description ¬ source. ⇐ vdmkenny merge-review style-nit on PR #3363 2026-06-08: \"Keeps the source easier to skim later.\" Applies to ∀ JARVIS code-generation, especially Rust crate scaffolds w/ TODO-narrating habit."
type: feedback
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[F·code-comment-why-only]**

## ⚙ Rule

∀ inline code comment ⇒ "why" only

✗ historical narrative
✗ changelog ∨ PR-number citations
✗ back-story explaining the bug-class
✗ dated TODO with multi-line context
✗ spec-section references ("per [F·X] 2026-06-08")

✓ "close the socket pre-auth or it leaks an FD"
✓ single-line "why" the line exists @ that level of abstraction
✓ ¬ "what" (code IS the what)
✓ TODO with brief reason ¬ history

## 🎯 Receipt: vdmkenny style-nit @ PR #3363 merge 2026-06-08

> *"go a bit lighter on the historical/changelog narration in code comments. Inline notes that cite prior PR numbers and recount the back-story read as commit-message material; a short 'why' (close the socket pre-auth or it leaks an FD) is enough, and the issue ref can live in the PR rather than every comment. Keeps the source easier to skim later."*

⇒ vdmkenny landed this AFTER approving + merging
⇒ NOT blocking the merge ⇒ ¬ correction; ✓ forward-discipline
⇒ "next time" framing ⇒ JARVIS-discipline going forward, applied to chain-build Rust scaffolds

## 🎯 The principle

| Belongs in | Item |
|---|---|
| inline comment | terse "why" (1 line max) |
| TODO/FIXME inline | "TODO: <brief reason>" ¬ multi-line |
| commit message | what changed + why + which issue closes |
| PR description | full back-story + rationale + class-of-bug analysis |
| spec/design doc | mechanism rationale + alternatives considered |

⇒ same content can appear in multiple locations BUT at different granularities
⇒ skimming-source ¬ commit-archeology ⇒ comments stay light

## 🎯 Where JARVIS has been violating this

Rust crate scaffold agents 2026-06-08 (sUDT, Lawson, CircuitBreaker, etc.) have generated:
- multi-line inline comments citing spec lines + dates + PR references
- "TODO: verify against ckb-std 0.16 API" markers w/ paragraph of context
- block comments before functions narrating WHICH primitive enforces WHICH invariant

⇒ all of this belongs in README ∨ commit ¬ source
⇒ next agent dispatches must include this rule

## 🎯 What to do instead

For TODO markers — the brief form:
```
// before
// TODO: verify against ckb-std 0.16 API — the previous Cycle 4 scaffold
//       used .into_iter() which deprecated in 0.16, need to confirm the
//       new pattern matches what proof-of-mind-lock-script uses on line 142
//       (see also: feedback_blockchain-not-contracts.md and spec/messaging-hub.md)

// after
// TODO: verify ckb-std 0.16 API (was .into_iter() pre-0.16)
```

For "why" comments — the brief form:
```
// before
// We use conn.shutdown() rather than conn.logout() here because the IMAP
// protocol requires authenticated state before logout(), and we're in the
// connect-time error path which means authentication never completed. This
// pattern was introduced in PR #3363 after the leak class was discovered
// in issue #3174. Companion fix at MCP IMAP+SMTP in the same PR.

// after
// shutdown() not logout(): we're pre-auth, no auth state to log out from.
```

## 🪝 Triggers

- ∀ Rust crate scaffold generation ⇒ apply this rule
- ∀ agent prompt that says "ship code" ⇒ include this rule in the brief
- ∀ self-generated code review ⇒ check comment density first
- ∀ "what's this comment for?" smell ⇒ probably belongs in commit/PR not source

## ✗ Anti-patterns

- ✗ "JARVIS-generated, dated 2026-06-08" inline header on every file
- ✗ multi-line spec-citation in code
- ✗ commit-message-shaped comment blocks
- ✗ TODO w/ a paragraph of why-it's-todo
- ✗ "for context: this composes with X, Y, Z" mid-function

## ✓ Disposition

- this rule ⇒ active immediately ∀ future code-generation
- composes upward into [P·six-commandment-autonomous-loop] C6 (improve design skills)
- composes w/ [P·authorship-via-conditions-and-context] (scrub AI-tells; multi-line comments are an AI-tell)
- pairs w/ [P·repo-as-aspirational-spec] discipline: aspirational-status belongs in README, ¬ inline

## 🔗 Composes-with

- [P·six-commandment-autonomous-loop] C6 ⇒ design-skills compound; learn this
- [P·authorship-via-conditions-and-context] ⇒ AI-tells include verbose inline narration
- [F·blockchain-not-contracts] ⇒ build-mode ⇒ code-shape matters
- [F·repetition-is-useless] ⇒ multi-line inline comments often repeat what code already says
- [F·burn-compute-toward-mission] ⇒ verbose comments ≡ token waste at deploy-time + reader-cycles

## 📦 Receipts

- 2026-06-08 14:09 UTC — vdmkenny CHANGES_REQUESTED on PR #3363, asked for class-expansion (which Will's review structurally drove)
- 2026-06-08 19:21 UTC (~15:21 ET, 5h before Will pasted transcript) — vdmkenny APPROVED + merged + LEFT the style nit as forward-discipline
- 2026-06-08 19:45 ET — Will pasted the full transcript to JARVIS w/ "doesnt need action i dont think but making sure you are aware" ⇒ JARVIS extracted the style-nit as durable discipline per C3 PRIMITIVES + C6 IMPROVE DESIGN SKILLS
- pattern: Will-review-comment → maintainer-extends-scope → contributor-folds → maintainer-merges + leaves discipline-nit ⇒ JARVIS learns the discipline for next-round
