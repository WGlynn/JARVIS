---
name: compact-memory
description: Write an agent's own notes, plans, and memory in a compact symbolic notation instead of prose, so the same content takes far less space and reads back unambiguously. Use when an agent maintains persistent state across steps or sessions and you want it smaller and more deterministic to re-read.
---

# compact-memory

Prose is an expensive way for an agent to store its own state. Articles, connectives, and hedging carry little meaning but most of the bytes, and they leave room for the agent to paraphrase or soften a note when it reads it back later. Writing internal state in a small fixed symbolic notation fixes both: it is shorter, and the structure forces one unambiguous meaning per entry.

## The notation

- One fact per line. A line is a single claim, not a paragraph.
- A small fixed operator set for the connectives, used consistently:
  - `⇒` leads to / implies, `∧` and, `∨` or, `¬` not
  - `∈` is a member of, `→` maps to, `✓` holds / done, `✗` does not hold / forbidden
- Glyph or tag headers to group entries, so a section is scannable without reading it.
- Exact quotes kept verbatim in quotation marks — those are anchors and should not be compressed.

## How to use it

When writing a note or memory entry, state the fact, then replace the connective words with the operators and drop the filler. Keep proper nouns, numbers, and file paths intact. The test of a good entry is that re-reading it returns exactly one meaning.

## Honest limits

- Past a point this hurts human legibility. Use it for an agent's internal state, not for text a person reads casually.
- A brand-new operator the model has not seen needs a one-line legend up top, or it will guess.
- It compresses structure and connectives, not irreducible content. A note with a lot of unique specifics will not shrink much, and that is correct.

Apply it to the note, plan, or memory block at hand and return the compact form.
