# Lane A cookbook — STAGED OUTLINE (cells UNVALIDATED — needs API key before PR)

- **Target:** `anthropics/claude-cookbooks`, new dir `capabilities/context-compression/guide.ipynb`
- **Gap (re-verified 2026-07-02):** 88 notebooks; `contextual-embeddings` = RAG, `summarization` = document summary. No notebook on compacting an *agent's own running context* between turns. Every long-run agent user hits this.
- **General, not VibeSwap-specific** (per Will's Lane-A heuristic). Zero VibeSwap/Noesis/HIERO branding; the technique is presented plainly.
- **BLOCKER:** cells need live-API execution + ruff + `/notebook-review` clean before any PR. No `ANTHROPIC_API_KEY` in this environment. Ship path = Will provides a key (or points at the Claude Code credential), then validate + `gh pr create`.

## Angle
Not "summarize the transcript." The move is: promote durable facts out of prose into a fixed one-fact-per-line operator form, keep the working turn in prose, and measure (a) token savings and (b) fidelity via an LLM-as-judge check that the compacted form answers the same questions as the full transcript. Honest framing: compression is safe only for facts that are already key-value pairs wearing prose clothing; it is lossy for reasoning/nuance, so the notebook shows WHERE it applies and where it does not.

## Cell plan
1. **md** — problem: agent context grows unbounded across turns; naive truncation drops load-bearing facts, naive summary blurs them.
2. **code** — setup (anthropic client, model = claude-sonnet-4-6 for the judge, a sample multi-turn transcript fixture).
3. **md** — the two-tier idea: working tier stays prose; durable tier is operator-dense (one fact/line, explicit fields).
4. **code** — `compact(transcript) -> facts[]`: a prompt that extracts durable facts into `key: value | ctx: ... | ts: ...` lines. Show token count before/after (use `client.messages.count_tokens`).
5. **code** — `answer(question, context)`: ask the same N questions against (a) full transcript, (b) compacted facts.
6. **code** — **LLM-as-judge fidelity gate**: a judge call scores whether the compacted-context answers match the full-context answers. Report agreement rate + token savings in one table.
7. **md** — when NOT to use it: reasoning chains, ambiguous state, anything where the prose IS the payload. Point to `summarization` cookbook for document-level.
8. **md** — extends to: a forgetting/expiry field so the durable tier does not grow unbounded (ties to the same axis discussed in anthropics/skills#1329).

## Core code cell (written, UNVALIDATED — do not trust the numbers until run)
```python
# capabilities/context-compression/guide.ipynb — cell 4 draft
COMPACT_PROMPT = """Extract only the durable facts from this transcript — things that must
survive a context reset. Output one fact per line as `key: value | ctx: <when it applies>`.
Drop pleasantries, reasoning, and anything re-derivable. Do not invent facts."""

def compact(client, transcript: str, model="claude-sonnet-4-6") -> str:
    msg = client.messages.create(
        model=model, max_tokens=1024,
        messages=[{"role": "user", "content": f"{COMPACT_PROMPT}\n\n<transcript>\n{transcript}\n</transcript>"}],
    )
    return msg.content[0].text

def n_tokens(client, text: str, model="claude-sonnet-4-6") -> int:
    return client.messages.count_tokens(
        model=model, messages=[{"role": "user", "content": text}]
    ).input_tokens
```

## Pre-PR checklist (run when key available)
- [ ] every cell executes top-to-bottom, no errors
- [ ] model ids current (claude-sonnet-4-6 / claude-opus-4-8 per repo's model-usage validator)
- [ ] ruff format + check clean
- [ ] `/notebook-review` + `/link-review` CI green locally
- [ ] outputs cleared or intentional; no secrets in cells
- [ ] README.md in the new dir; conventional-commit title `feat(context-compression): add agent context compaction guide`
- [ ] AI-tell scrub STRICT on all markdown cells
