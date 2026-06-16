---
name: persistent-engagement-backlog
description: "When a genuinely-GLOBAL gate (not a per-thread dependency) blocks a loop across K fires, consolidate the signal once and shift compute to the still-productive sub-task. The per-thread version is dissolved by pivot-until-read."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3a5d7fec-091d-4ee3-9c13-fa3b89c150bc
---

When a gate blocks a loop across ≥K consecutive fires ⇒ (a) emit ONE consolidated "backlog: M fires gated, N items stacked" signal ¬ per-fire silence; (b) recognize the loop's marginal value has shifted to whatever sub-task is STILL productive ⇒ bias compute there.

**Why:** Odysseus discovery hit 3 consecutive gated fires on the SAME block; strong candidates stacked unsent while each fire silently re-paused ([[repetition-is-useless]] — N identical no-ops ≡ 1). RECONCILED w/ [[pivot-until-read-not-global-pause]] (2026-06-16, same session): once a per-thread block is UTXO-scoped, candidates DON'T stack — you dispatch the independents — so the per-thread backlog mostly DISSOLVES. Honest downgrade: this primitive's original framing over-claimed; its residual scope is narrow. It still governs the genuinely-GLOBAL gate (e.g. home-community daily quota-floor) that legitimately blocks everything: there, pivoting isn't available, so consolidate-signal + shift-compute is the right move, not silent re-pause.

**How to apply:** Classify the block TYPE first (per [[pivot-until-read-not-global-pause]]): per-item dependency ⇒ pivot, this primitive doesn't fire. Genuinely-global gate ⇒ count fires-since-block; at K≥2 emit a single backlog ping; route compute to the productive sub-task (Odysseus: C2.5 advice-mining per [[odysseus-as-advisory-substrate]]). Composes with [[repetition-is-useless]], [[pivot-until-read-not-global-pause]], [[full-leverage-only-moves]], [[primitives-are-bottleneck-dissolutions]] (the bottleneck here = review-latency on a shared budget).
