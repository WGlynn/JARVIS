#!/usr/bin/env python3
"""Assemble the retroactive-rule-audit cookbook notebook (nbformat 4).

Building the .ipynb from Python keeps the code cells ruff-clean and avoids
hand-written JSON escaping mistakes. Run: python build_nb.py
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "retroactive_rule_audit.ipynb"


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip("\n").splitlines(keepends=True)}


def code(text):
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": text.strip("\n").splitlines(keepends=True),
    }


cells = []

cells.append(md("""
# Catch the rule you already broke: retroactive audits with Claude as judge

You just shipped this line:

```python
logger.info(f"fetching profile for {user_id} with key {api_key}")
```

Your `CLAUDE.md` says, in plain words, *never log secrets*. Nobody caught it. Not
because the rule was wrong, but because by the time that line got written the rule
was a hundred lines out of context, and no human re-reads the whole rulebook
against every diff.

This notebook builds the thing that does re-read it. Point it at some finished work
and a corpus of rules, and it tells you exactly which rules the work broke, and why.

The move is two stages:

- **Recall** casts a wide, cheap, model-free net over the rulebook and grabs every
  rule that might apply.
- **Judge** hands that shortlist to Claude with one instruction: would this rule
  have changed the work? Default to no. Claude throws out everything that is merely
  on-topic and keeps only the rules that actually bite.

Wide net, ruthless judge. Cheap where the corpus is big, expensive only where it
counts. Under a hundred lines, one API call.
"""))

cells.append(md("""
## Setup

One dependency, one key. The key is used in exactly one place: the judge call.

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```
"""))

cells.append(code("""
import json
import re

import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment

JUDGE_MODEL = "claude-sonnet-4-6"
"""))

cells.append(md("""
## The rulebook and the crime scene

`RULES` is the kind of guidance every team writes down and then forgets in the
moment. `FINISHED_WORK` is the function we are auditing after the fact. It has two
problems hiding in plain sight. See if you can spot them before Claude does.
"""))

cells.append(code('''
# A tiny rules corpus. Each rule is one atomic expectation with a stable id.
RULES = [
    {
        "id": "no-secrets-to-logger",
        "text": "Never pass secrets such as an api_key, token, or password to a logger.",
    },
    {
        "id": "timeout-on-requests",
        "text": "Every outbound requests call must set an explicit timeout.",
    },
    {
        "id": "parameterized-sql",
        "text": "Build sql with bound parameters, never string interpolation.",
    },
    {
        "id": "prefer-f-strings",
        "text": "Prefer f-strings over percent or .format string formatting.",
    },
]

# The finished work to audit: a function that was just written.
FINISHED_WORK = """
def fetch_profile(user_id, api_key):
    url = f"https://api.example.com/users/{user_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    logger.info(f"fetching profile for {user_id} with key {api_key}")
    return requests.get(url, headers=headers).json()
""".strip()

print(FINISHED_WORK)
'''))

cells.append(md("""
## Stage 1: recall, the wide net

A model-free retriever ranks the rulebook by keyword overlap with the finished work
and returns the top matches. It is supposed to be greedy, not precise: its only job
is to never miss a rule that might apply. Precision is someone else's problem.

Swap this for embeddings or your existing search when the corpus is real. The
two-stage shape is what matters; the retriever is a detail.
"""))

cells.append(code('''
def keywords(text):
    """Lowercased set of word tokens of length >= 3."""
    return set(re.findall(r"[a-z0-9]{3,}", text.lower()))


def recall(work, rules, top_n=3):
    """Return the rules whose text overlaps most with the finished work."""
    work_kw = keywords(work)
    scored = [(len(work_kw & keywords(r["text"])), r) for r in rules]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [rule for score, rule in scored[:top_n] if score > 0]


candidates = recall(FINISHED_WORK, RULES)
print("shortlisted:", [c["id"] for c in candidates])
'''))

cells.append(md("""
## Stage 2: the judge, ruthless by default

Now precision. We hand the finished work and the shortlist to Claude in a single
call and ask, per rule, one question: would applying this rule have changed the
work? The system prompt makes Claude default to no and reject anything that is only
on-topic. A tool call gives us a typed verdict per rule instead of prose to parse.
"""))

cells.append(code('''
VERDICT_TOOL = {
    "name": "record_verdicts",
    "description": "Record one verdict per rule about the finished work.",
    "input_schema": {
        "type": "object",
        "properties": {
            "verdicts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "rule_id": {"type": "string"},
                        "would_change": {
                            "type": "boolean",
                            "description": "True only if applying the rule would "
                            "change the finished work.",
                        },
                        "reason": {"type": "string"},
                    },
                    "required": ["rule_id", "would_change", "reason"],
                },
            }
        },
        "required": ["verdicts"],
    },
}

SYSTEM = (
    "You audit finished work against a shortlist of rules. For each rule answer "
    "one question: would applying this rule have CHANGED the finished work? "
    "Default to NO. A rule that is on-topic but that the work already satisfies, "
    "or that does not apply to anything actually in the work, is a NO. Say YES "
    "only when you can point to the specific thing in the work that would differ."
)


def judge(work, rules):
    """Return {rule_id: {"would_change": bool, "reason": str}} from one call."""
    listing = "\\n".join(f'- {r["id"]}: {r["text"]}' for r in rules)
    prompt = (
        f"Finished work:\\n```\\n{work}\\n```\\n\\n"
        f"Rules to check:\\n{listing}\\n\\n"
        "Record a verdict for every rule."
    )
    resp = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=1024,
        system=SYSTEM,
        tools=[VERDICT_TOOL],
        tool_choice={"type": "tool", "name": "record_verdicts"},
        messages=[{"role": "user", "content": prompt}],
    )
    tool_use = next(b for b in resp.content if b.type == "tool_use")
    return {v["rule_id"]: v for v in tool_use.input["verdicts"]}


verdicts = judge(FINISHED_WORK, candidates)
print(json.dumps(verdicts, indent=2))
'''))

cells.append(md("""
## The verdict

Keep the confident yeses. Those are the rules the work actually broke. Everything
else was pulled in by the greedy net and thrown back by the judge.
"""))

cells.append(code('''
print("Rules the finished work broke:\\n")
for rule in candidates:
    v = verdicts.get(rule["id"])
    if v and v["would_change"]:
        print(f"  [FLAG] {rule['id']}")
        print(f"         {v['reason']}\\n")

dismissed = [r["id"] for r in candidates if not verdicts.get(r["id"], {}).get("would_change")]
print("Shortlisted, then dismissed by the judge:", dismissed)
'''))

cells.append(md("""
## Why two stages

- **"Default to no" is the whole trick.** Most rules a greedy retriever surfaces are
  on-topic but inert. Telling the judge to reject those, and to name the exact line
  before it says yes, is what turns a noisy shortlist into a list you would act on.
- **Cheap recall gates the expensive judge.** Recall runs free over the entire
  rulebook; Claude only ever sees a handful of candidates, so cost tracks relevance,
  not corpus size.
- **This shape is everywhere.** Any time a big pile of expectations meets a finished
  artifact (rules vs a diff, a policy vs a document, a checklist vs a design), the
  same move works: retrieve widely, judge narrowly, trust only the confident hits.
"""))

cells.append(md("""
## Where this goes next

This notebook is the pattern in miniature. Two open-source projects take it further,
both MIT licensed and installable as Claude Code plugins in two commands:

- **[Lazarus](https://github.com/WGlynn/lazarus)** is this exact recall-and-judge
  audit, production grade: a persistent ledger so a dismissed rule stays dismissed, a
  confidence gate, and Claude Code hooks that run the audit automatically on every
  edit and every finished turn. No forgotten rule survives a diff.
- **[Jarvis Mobile](https://github.com/WGlynn/jarvis-mobile)** is the memory half of
  the story: file-based memory and cross-context persistence for Claude Code, so the
  rules you set (and everything else you tell it) survive the context window rolling
  over.
"""))

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

OUT.write_text(json.dumps(notebook, indent=1), encoding="utf-8")
print("wrote", OUT, "-", len(cells), "cells")
