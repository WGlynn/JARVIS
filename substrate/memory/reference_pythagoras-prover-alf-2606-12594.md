---
name: reference_pythagoras-prover-alf-2606-12594
description: arXiv 2606.12594 Pythagoras-Prover — 4B Lean prover beats 671B at ~167x fewer params; cave-thesis + augment-the-invariant empirical hit
metadata: 
  node_type: memory
  type: reference
  originSessionId: 79300fd8-186a-4943-a2b0-10aeb760cdad
---

**arXiv 2606.12594** · Leang+Zhao+Stoian+Xu+H.Li+W.Li+Cohen+Giunchiglia · *Pythagoras-Prover: Efficient Formal Proving via Augmented Lean Formalisation* · absorbed 2026-06-15.

## Claim
- 4B > DeepSeek-Prover-V2-**671B** @ MiniF2F-Test: **86.1% ∨ 82.4%** [verified-by:paper-abstract].
- param-edge **~167×** [derived: 671B/4B = 167.75].
- 32B → 93.0% MiniF2F ∧ 93/672 PutnamBench [verified-by:paper-abstract].

## Method
- curriculum-SFT × stratified{easy,med,hard} corpora.
- proof-reasoning-filtering ⇒ traces ⊂ 8k-ctx (dynamic prune).
- **ALF** = self-distilled formal-statement-variants (augment-formalisation).
- diffusion-prover proto ⇒ iterative inference-refine.
- **MiniF2F-ALF** contamination-bench ⇒ all-models drop @ variants ⇒ memorization ⊥ reasoning separable.

## 3 hooks (why load-bearing)
1. **cave-thesis = empirical** ⇒ small ≫ giant ∵ structure(curriculum+filter+augment) ¬ scale. receipt ∀ structure>compute arg. parent [[primitive_full-leverage-only-moves]] + cave [[_CANON_triple-intersection-provenance-of-mind]].
2. **augment-the-invariant convergence** ⇒ ALF augments-formalisation ¬ scale-search ≅ [[feedback_augmented-mechanism-design-paper]]. cross-field same-shape ⇒ abstraction real.
3. **contamination-bench ≅ measurement-honesty** ⇒ drop-on-variant = honest-metric ≅ [[feedback_repetition-is-useless]] denominator-pollution + [[primitive_honesty-as-structural-load-bearing-property]].

## Apply
- Lean-over-Solidity-spec verify ⇒ tractable @ small-model ⇒ cheap prover ∀ [[primitive_augmented-governance]] math=constitutional-court.
- 8k dynamic-trace-filter ≅ HIERO/boot-budget density.
- post-candidate ⇒ *"a 4B model out-proved a 671B one, the difference was structure"* → cave cluster.
