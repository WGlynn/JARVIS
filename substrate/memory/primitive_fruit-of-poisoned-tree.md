---
name: Fruit of the Poisoned Tree
description: Coding primitive — when you find a bug, sweep for all siblings/cousins that propagated from the same root cause before moving on
type: feedback
---

When you discover a problem, **do not fix just that instance**. The existence of one bug implies a family of related bugs propagated from the same root cause, the same bad pattern, or the same missing knowledge at the time the code was written.

**The Protocol:**
1. **Identify the poison** — what specific pattern/omission caused this bug?
2. **Trace the tree** — grep/search the entire codebase for the same pattern
3. **Sweep all branches** — fix every instance, not just the one that was reported
4. **Inoculate** — if possible, add a lint rule, convention, or documentation that prevents regrowth

**Why:** A single missing `WebkitBackdropFilter` meant 11 files had the same Safari blur bug. A single fragile `paddingTop: '38vh'` meant 5 modals had cross-browser positioning issues. Fixing one and leaving ten is worse than fixing none — it creates false confidence that "the bug was fixed."

**How to apply:** Every time a bug is found (by user report, testing, or observation), before closing the fix:
- Search the codebase for the same pattern
- Ask: "If the author made this mistake here, where else did they make it?"
- Fix all instances in one sweep commit

**Named by Will (2026-03-20).** Inspired by the legal doctrine: evidence obtained from an illegal source taints everything derived from it. In code: a flawed pattern taints every file it touched.
