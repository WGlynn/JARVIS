---
name: no-blockquotes-on-copy-paste-drafts
description: "Will pastes drafts into TG / chat / docs — markdown blockquote prefix `>` becomes a visible '|' bar in the destination and breaks copy-paste UX. Use plain text + triple-dash frame instead. (Frontmatter repaired 2026-06-10 after originSessionId-injection regression on 2026-06-09 corrupted the YAML by embedding a closing originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
inside the description string.)"
type: feedback
originSessionId: 8e0b2388-5171-43d5-a501-c272f20c2f6f
---

**Rule:** ∀ draft-content Will-will-copy-paste ⇒ plain-text bracketed by `---` separators. ✗ markdown `>` blockquote prefix.

> *"please stop with the white vertical bars containing the text bodies, you are killing me in copy paste instances"* — Will, 2026-04-30

> *"please stop with the vertical white bars on the side of things, i know it's helpful for me viewing, but it's impossible to copy and paste what you write"* — Will, 2026-04-24 (origin)

**Why:**
- `>` prefix copies-with-content ⇒ pastes into TG/email/etc. as junk-prefix per line
- formatting-carry compounds across paste-targets (TG → strips inconsistent; LinkedIn/Medium → carries; chat clients → varies)
- copy-paste-friction = direct production-cost (Will is forwarding to Rick, [REDACTED-NDA], partners, daily)

**How to apply:**
- ∀ draft-for-Will-to-send-elsewhere ⇒ plain-text + `---` framing above and below
- paste-targets ∈ {TG, email, LinkedIn, Medium, X, chat-clients, doc-PRs}
- ✗ `>` blockquote on draft-for-paste content
- ✓ `>` blockquote ∀: in-memory-file Will-quote anchors (different context, not pasted), tiny inline-quoted phrases in conversational text
- code blocks (```) ✓ for code/CLI/JSON ¬ prose-drafts (fence-strip varies by renderer)
- ambiguous ⇒ default plain-text + separators

**Detection:**
- if I'm about to wrap multi-line draft prose in `>` ⇒ STOP, switch to plain + `---`
- "here's the draft" / "ready to paste" / "send this to X" = paste-bound signal

**Consolidation note (2026-05-15):** merged `feedback_no-blockquotes-on-copy-paste-drafts.md` (2026-04-24 origin) into this primitive. Same rule, older prose form; both Will-quotes preserved.
