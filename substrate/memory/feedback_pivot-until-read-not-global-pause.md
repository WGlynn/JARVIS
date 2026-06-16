---
name: pivot-until-read-not-global-pause
description: A Will-read (or single human-review) dependency blocks ONLY the dependent task — UTXO-scoped — never the whole loop. Pivot to independent tasks; surface the blocked one once.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3a5d7fec-091d-4ee3-9c13-fa3b89c150bc
---

∀ blocking-dependency on Will-read (∨ any single human-review gate) ⇒ scope the block to ONLY the dependent task ⇒ pivot to independent tasks + keep working. Tasks ≡ UTXOs: a blocked INPUT freezes only the transaction that spends it, ¬ the mempool. ✗ global "pause until Will reads" ⇒ ✓ "pivot until Will reads."

**Why:** The Odysseus engagement-aware pause was coded as a GLOBAL halt — one unread thread (#4171) froze the ENTIRE discovery campaign incl. independent candidates (#4415 score 17, #3163 score 13) that had ZERO dependency on #4171. A coarse lock masquerading as caution: it stalls aligned independent work and manufactures [[repetition-is-useless]] silent re-pauses every fire. The dependency was per-thread; the lock was per-loop ⇒ scope mismatch. Will 2026-06-16: *"there's other tasks that arent dependent, kinda like UTXOs, so you should just be 'pivot until will reads' for stuff like that."*

**How to apply:** On any human-review gate ⇒ (1) compute the dependency set (which tasks actually SPEND the blocked input); (2) exclude ONLY those; (3) pivot to the independent set + execute the reversible-aligned moves; (4) surface the blocked input ONCE (consolidated ping), ¬ re-block per fire. CRITICAL distinction: a per-item read-dependency is UTXO-scoped + pivotable; a genuinely-GLOBAL budget is NOT (e.g. the home-community daily-cadence quota-floor is a shared resource, not a dependency — it stays global). Generalizes past Odysseus: ∀ autonomous loop with a "needs Will" item, don't let it freeze the independents. Composes with [[act-on-reversible-aligned-moves]], [[repetition-is-useless]], [[full-leverage-only-moves]] (refines: full-leverage gates a SINGLE move; this prevents one gated move from freezing INDEPENDENT moves), [[structure-does-the-work]], [[persistent-engagement-backlog]] (this fix dissolves most of that backlog state).
