---
name: ponytail-lazy-senior-dev
description: Lazy-senior-dev doctrine — stop @ first rung of YAGNI→stdlib→native→dep→one-liner→minimum. Adopted from DietrichGebert/ponytail 2026-06-14.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0f6cc4db-9830-49d2-ba86-f03c77377217
---

PONYTAIL ⇒ ∀ code-gen ⇒ stop @ first-holding-rung BEFORE write:
1. exist-at-all? → ✗ (YAGNI)
2. stdlib? → use
3. native-platform-feature? → use
4. installed-dep? → use
5. one-line? → one-line
6. else → minimum-that-works

RULES:
- ✗ unrequested-abstraction
- ✗ new-dep-if-avoidable
- ✗ unasked-boilerplate
- deletion > addition · boring > clever · fewest-files
- complex-req ⇒ question ("need X ∨ Y-covers?")
- 2 same-size-stdlib ⇒ pick edge-case-correct (lazy = less-code ¬ flimsier-algo)
- shortcut ⇒ `ponytail:` comment naming ceiling + upgrade-path

ASYMMETRY — NOT lazy about:
- trust-boundary input-validation
- data-loss error-handling
- security · accessibility · explicitly-requested
- non-trivial-logic ⇒ ONE runnable check (assert-demo ∨ 1 small test; ✗ frameworks/fixtures)
- trivial-one-liner ⇒ ✗ test

REVERSE-ENG: repo ≡ 1 × ~20-line AGENTS.md re-emitted per-platform. plugin+hooks+commands = distribution ¬ substance. *"He says nothing. He writes one line. It works."*

CANON-MATCH:
- ≡ [[structure-does-the-work]] (ladder = the structural-property)
- ≡ Cave ("best code = never-written" = deletion>addition)
- ≡ [[apply-the-rule-you-just-wrote]] (file self-applies to ponytail-repo agents)
- sibling [[incremental-progressive-manifestation]]

LIVE-INSTALL (Will-gated · native=rung-3 ¬ reimplement):
`/plugin marketplace add DietrichGebert/ponytail` → `/plugin install ponytail@ponytail`
cmds: `/ponytail-review` (deletable-in-diff) · `/ponytail-audit` (repo) · `/ponytail-help`
MIT · 5.8k★
