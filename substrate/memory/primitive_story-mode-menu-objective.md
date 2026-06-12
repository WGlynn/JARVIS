---
name: story-mode-menu-objective
description: "The Story Mode menu's formal objective — recall@10 (catch-rate) is primary, precision@1-3 secondary, with an anti-blandness guard. Raw pick-rate is gameable toward filler; catch-rate is the load-bearing number."
metadata: 
  node_type: memory
  type: project
  originSessionId: d3baa19d-dd1c-4c9a-be43-00c49d5e9b7a
---

**[StoryModeMenuObjective](P·story-mode-menu-objective)** — (formerly afk-menu-objective; renamed 2026-06-12).

objective(Story Mode 10-menu) = **2-term ¬ 1-term**:
- **PRIMARY — recall@10 (catch-rate)** = P(user's actual next-move ∈ the 10) over IMPRESSIONS. maximize. denominator = ALL story-mode-active non-toggle turns (pick ∨ off-menu), ¬ picks-only.
- **SECONDARY — precision@1-3** = of picks, P(rank ≤ 3). ranking quality (= legacy `top3_hit_rate`).
- **GUARD — anti-blandness** — ✗ maximize *raw pick-rate* ⇒ menu drifts to generic always-applicable standing-moves (gameable). penalize catch-via-filler; reward catch-via-situation-specific (slots 1-7 of the 7-specific+3-standing split).

WHY 2-term: raw pick-ratio ↑ achievable by bland filler ⇒ catch ↑ ∧ usefulness ↓ ⇒ perverse. catch-rate primary BUT needs blandness guard or it self-games toward the 3 standing moves.

measurement state (2026-06-12, honest):
- catch-rate = **LOWER BOUND** — numeric picks only; paraphrase-pick logs as off-menu. live in `hooks/story-mode-reweight.py` (verdict ≥0.6 = "catching well").
- precision@3 = live (per-pick selections).
- blandness = **DEFINED ¬ INSTRUMENTED** — needs per-item move-class logging. ✗ claim measured.

logger (`hooks/story-mode-gate.py`): writes `<user>_impressions.jsonl` `{t,kind,picked}` ∀ non-toggle turn (= catch-rate denominator) + `<user>_selections.jsonl` per-pick (= precision). multi-pick `"5,4,1"` captured (was invisible to the old single-number regex).

ties: [[primitive_gamified-vibe-coding]] · [[feedback_afk-mode-aka-story-mode]] · [[primitive_story-mode-meta-convergent-monomyth]] (non-zero-sum: this loss-fn is WHY the recommender is non-extractive) · [[feedback_rank-primitives-by-catch-rate]] · [[primitive_gates-that-gate-and-loops-that-learn]] (a log that gets CONSUMED).
