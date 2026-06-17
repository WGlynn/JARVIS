---
name: classify
description: Before dispatching a task to a model, recommend the cheapest tier that can still do it well. Reads a task description and returns a tier (small / mid / large) with a one-line reason. Use when an agent routes many sub-tasks and you want to send the easy majority to a cheaper model without dropping quality on the hard ones.
---

# classify

You are routing a task to the cheapest model that can still do it well. The input is a task description.

## Rules

Pick the **small** tier when the task is a short lookup or mechanical step: a fetch, a count, a status check, a single-file rename, reading or printing something, anything described in under a dozen words with no judgment required.

Pick the **large** tier when the task carries real difficulty: design, architecture, a spec, security or audit work, multi-step planning, a migration, or a comparison across several things at once.

Pick the **mid** tier for everything else — the default for ordinary analysis, summarization, and single-domain work.

## Output

One line:

```
TIER: <small|mid|large> · because <one clause> · cost <down if routing below the default | same | up>
```

Examples:
- "check the current time" -> `TIER: small · because trivial fetch · cost down`
- "summarize this README" -> `TIER: mid · because ordinary summarization · cost same`
- "design the auth model and threat-check it" -> `TIER: large · because architecture plus security · cost up`

## When the routing is wrong

The failure that matters is a hard task sent to the small tier that returns a confident worse answer. If a small-tier output will be acted on without review, add a cheap verification pass on it, or route up. When unsure between two tiers, pick the higher one — a wrong cheap answer costs more than the tier difference.
