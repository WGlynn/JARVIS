---
name: F·medium-drafts-html-default
description: ∀ Medium-bound drafts ⇒ default-format = HTML (¬ Markdown). Medium ✗ parses raw .md on paste; HTML round-trips cleanly w/ semantic preservation (h1/h2/p/strong/em/hr) + Medium applies own typography. Exceptions allowed when context warrants (internal pipeline tracking, source-of-truth .md, non-Medium target). Will-named 2026-05-11 after `2026-05-11_cooperative-capitalism-cure.md` paste-noise incident.
type: feedback
originSessionId: 35d175e9-bf70-4d8f-b83a-b82bdd9d8fdf
---
# F·medium-drafts-html-default

## Rule
∀ Medium-bound draft ⇒ default-output-format = HTML.
Exceptions ∈ {internal-pipeline tracking, source-of-truth .md, non-Medium target}.

## Why
Medium's editor ✗ parses raw Markdown on paste. Literal `**`, `*`, `-`, `#` characters appear in published output ⇒ noisy + manual cleanup. HTML semantic tags (h1/h2/p/strong/em/hr) carry through paste ⇒ Medium applies its own typography over them. 2026-05-11 origin: Will pasted `2026-05-11_cooperative-capitalism-cure.md` into Medium, got literal punctuation, surfaced the rule.

## How to apply
- ∀ Medium draft ⇒ ship `.html` w/ semantic tags + minimal `<style>` block for browser-preview only (Medium ignores inline CSS — uses its own typography)
- workflow: double-click `.html` ⇒ browser ⇒ Ctrl+A ⇒ Ctrl+C ⇒ paste to Medium editor
- ship `.md` alongside as source-of-truth iff workflow warrants (pipeline tracking, future edits, GH-mirror)
- exceptions still allowed when target ≠ Medium:
  - ethresearch.ch ⇒ Discourse-compatible (Unicode operators, ¬ mathjax)
  - GitHub README ⇒ Markdown native
  - internal docs / pipeline tracking ⇒ Markdown
- when format ambiguous ⇒ ship both .html and .md, no harm done

## Related
- F·platform-register-matching (sibling: register to platform)
- F·html-over-pptx (sibling: HTML-default for decks; same principle, different target)
- F·screenshot-engineered-phrasing (sibling: format to delivery channel)
- P·ship-web (overlap on HTML artifacts)

## One-line
Medium ✗ parses Markdown on paste ⇒ default to HTML. Exceptions when target ≠ Medium.
