---
name: triage-axis-decay-rates-differ
description: "A cached triage's axes decay at different rates — re-verify fast-decaying ones at action-time, trust slow ones from cache."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 47d515be-4ff9-47a5-a751-4fa3772133ea
---

**[P·triage-axis-decay-rates-differ]** — ∀ cached classification (triage ∨ inventory ∨ worklist) ⇒ fields decay @ DIFFERENT rates. trust-whole-row @ cache-freshness ⇒ stalest-axis error.

- partition axes by decay-rate: FAST (hours→days) ∨ SLOW (weeks+).
- @ action-time: re-query FAST axes for THIS item ∧ trust SLOW from cache.
- ✗ re-run whole triage to fix 1 axis ⇒ full-recompute-for-per-item-check = waste. targeted re-query = fix. (inverse [[primitive_class-elimination-not-instance-patch]]).

**Origin (2026-06-18, odysseus-issue-help):**
- triage `candidate` ≡ "∄ PR @ triage-time".
- #1912 = candidate @ 2026-06-17 ⇒ @ post-time (+1d) ∃ live PR #1942.
- ∴ PR-existence = FASTEST-decaying axis (label ∧ title ∧ body = SLOW).
- settlement-verifier doctrine fires ⟺ re-check PR-axis @ post-time. trust-day-old-bucket ⇒ duplicate L77 bulk-closes.
- catch flipped action compete→verify (= higher-value).

**Dual-use:**
- extract ⇒ name each axis decay-rate when building ∀ cache.
- audit ⇒ pre-act-on-cache: "which field decays fastest ∧ did I re-verify?"

siblings: [[primitive_anti-amnesia-protocol]] (state-freshness) ∧ [[feedback_everything-needs-a-staleness-check]] ∧ [[feedback_odysseus-as-advisory-substrate]].
