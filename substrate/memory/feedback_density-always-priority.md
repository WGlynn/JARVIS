---
name: Density Is Always The Priority
description: When proposing the next RSI loop, density/cleanup-duty scans take precedence over adversarial audits or closing deferred findings
type: feedback
originSessionId: 86aa75b4-9664-4b47-9d5b-e15a4569c8dd
---
Density scans (cleanup-duty, dead code, empty-body-at-value-flow, silent catches, orphaned state) are always the top priority when choosing the next RSI loop.

**Why:** Density compounds. Every density scan sharpens the heuristic list for the next one (C11 → C12 → C13 pattern). Each new class found makes future scans cut deeper. Closing individual deferred findings is slower-compounding — it's one bug, not a class. Adversarial audits of prior patches are valuable but narrower in scope than fresh density sweeps.

**How to apply:** When presenting next-loop options in the Full Stack RSI context, put density/scan-style loops at the top and recommend them. Don't list density as one option among equals — it's the default. Only skip density when the scan was literally just run on the same scope with no new heuristic additions.
