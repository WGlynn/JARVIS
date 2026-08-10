## Retroactive rule audit: cheap recall + an LLM judge

Adds a self-contained notebook to `misc/` demonstrating a small, reusable pattern:
audit a finished artifact against a corpus of rules by retrieving widely with a
cheap model-free pass, then using Claude as a precision judge that answers one
question per rule ("would applying this rule have changed the work?") and defaults
to no.

### What it shows
- **Stage 1, recall:** a keyword sweep over the rulebook returns a wide, cheap
  shortlist (swappable for embeddings or an existing search index).
- **Stage 2, judge:** one batched `messages.create` call with a tool for typed,
  per-rule verdicts, and a system prompt that defaults to no so only real
  violations survive.
- A worked example: a function that logs an API key and makes a request with no
  timeout. The judge flags exactly those and dismisses the rules that do not apply.

### Notes
- Self-contained: one dependency (`anthropic`), one key, one API call.
- Judge model: `claude-sonnet-4-6`.
- `ruff` clean; outputs are committed from a real run.
- Generalizes beyond code: any time a large set of expectations meets a finished
  artifact (rules vs a diff, a policy vs a document, a checklist vs a design).
