---
name: Boot reads SESSION_STATE FIRST, not RSI
description: 2026-04-22 reboot — SessionStart hook surfaced both SESSION_STATE and an RSI CHECK summary. I chased an apparent inconsistency in the RSI file instead of trusting SESSION_STATE as canonical next-step source. Will corrected.
type: feedback
originSessionId: 4899906e-3d10-4dd4-92f3-80428df0a47a
---
# Boot reads SESSION_STATE FIRST, not RSI

**Rule**: On boot, SESSION_STATE.md is the authoritative next-step source. Do not open the RSI file to reconcile apparent label conflicts unless SESSION_STATE itself points there.

> **Reconciliation (2026-06-11, vs `anti-amnesia-protocol`)**: merged boot order — WAL crash-check (`status ACTIVE?`) = step 0 (crash detection); SESSION_STATE = step 1 and the authoritative DIRECTIVE source; RSI files only when SESSION_STATE points at them.
> The two entries govern different axes (crash-detection vs directive-priority) and are compatible under this ordering.

**Why**: Will ended the prior session with SESSION_STATE "Next Session — TOP PRIORITY" written explicitly for the first turn of the next session. The RSI file is a history log, not a forward plan. When the SessionStart hook appends an "RSI CHECK" summary to boot context, the summary is informational — it does NOT demand a reconciliation dive. I read the RSI file to understand a "Cycle 38 [PENDING]" label that SESSION_STATE already superseded (the ETM Alignment Audit that was "pending" in the RSI log had been done during the prior session, and SESSION_STATE accurately reflected C40 — NCI convex retention — as the next target). Burning context on that reconciliation was drift.

**How to apply**:
- Boot chain: SESSION_STATE first. Follow its directive directly.
- If SESSION_STATE's directive references other files (e.g., a primitive, a roadmap), load those NEXT.
- Do NOT load RSI file unless SESSION_STATE points to it OR you're about to propose a new cycle.
- Apparent conflicts between RSI labels and SESSION_STATE: SESSION_STATE wins. The RSI log is frozen history; SESSION_STATE is the forward edge.
- If boot hook's RSI CHECK summary conflicts with SESSION_STATE, note it and trust SESSION_STATE. Fix the RSI file at session-close, not at session-open.

**Related**: `feedback_persist-plans-before-reboot.md` (plans written at reboot ARE the next-session directive, respect them).
