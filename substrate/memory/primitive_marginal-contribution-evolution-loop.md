---
name: marginal-contribution-evolution-loop
description: "General self-improvement loop — evolve any artifact by iterating mutate → independent-score → synthesize. Fitness = marginal-contribution Δ over the PREVIOUS iteration (not a literal Shapley value). Scoring is substrate-matched (objective oracles for code, judges for writing). Guarded vs local-optima (population) + Goodhart (un-gameable oracles). Parent of [[shapley-scored-writing]] + the vibe-coding confidence loop."
metadata: 
  node_type: memory
  type: primitive
  originSessionId: 42e998bd-7972-4258-851f-d518d024b116
---

**[P·marginal-contribution-evolution-loop]**

**THESIS (Will 2026-06-18): INHERITED CATCH-RATE = the future of loop engineering. period.**
a loop is only as good as its verifier; weak verifier = generate-and-rubber-stamp (the 2026-06-18 rating-judges). phase-change = verifier INHERITS a competent human's catch-rate (via deepfunding pairwise-distillation) ⇒ catches at scale, human-out-of-seat. ∴ north-star metric for ANY loop = verifier's catch-rate on planted defects, benchmarked vs the human. ¬ bigger-models ¬ more-variants — verifiers that actually catch.

artifact-quality ⇒ optimize MARGINAL-CONTRIBUTION via evolution.
LOOP = mutate → independent-score → synthesize → repeat.
fitness = 2 ORTHOGONAL AXES (below); converge ⇔ axis-B Δ→0 AND axis-A gate passed.

**"Shapley" = metaphor ¬ literal** (Will 2026-06-18: *"i was using shapley as a metaphor of sorts for marginal contribution optimization"*).
- apt: Shapley ≡ averaged-marginal-contribution ∴ good hook
- LITERAL Shapley only in 2 cells: (a) split credit among co-contributors, (b) parsimony/reuse cut
- ✗ claim literal "Shapley value of X" in SHARED docs ⇒ invites pedantic rebuttal; lead w/ "marginal contribution", Shapley = framing-hook + 1-clause tell

**Two axes (orthogonal reference-frames · BOTH required):**
- AXIS-A · contribution-to-CONVERSATION — ref = ALL prior-work audience-holds (thread · paper · corpus · codebase). Q: worth-existing/sending at all? ≡ [[redundancy-not-unread-is-the-comms-failure]] measured.
- AXIS-B · contribution-over-LAST-ITERATION — ref = my gen_N draft. Q: improving? converged? ≡ the evolution Δ.
- high-B ∧ low-A = polished-redundancy: converge beautifully on something ¬worth-sending ← THE v2-MEV-note failure 2026-06-18.
- ORDER: gate AXIS-A FIRST (A≈0 ⇒ STOP, ∄ B-polish redeems) THEN climb B to converge. (failure-mode: climb B, never measure A vs the real conversation.)
- judges see A only if FED A's reference (the conversation) ¬ only-the-variants — why 2026-06-18 AI-judges caught little.

**Substrate-matched scoring** ([[substrate-port-pattern]] applied to the SCORE step):
- WRITING — ∄ ground-truth ⇒ JUDGMENT (indep judges, perspective-diverse). axes: correctness-gate · usefulness · novelty · marginal-Δ.
- CODE — ∃ ORACLES ⇒ tests(unit+property+fuzz) · types+contracts · scanners · mutation-testing · benchmarks. step = Pareto-positive oracle-Δ (≥1 up ∧ 0 regress). judgment only on simplicity/reuse.
- the loop is CONSTANT; the evaluator is substrate-matched. ← the whole generalization.

**Guards (proper MD ¬ optional):**
- WEAK-SCORER (PRIMARY — the real failure observed 2026-06-18: judges caught little). rating ≠ detecting. fixes:
  1. SCORE-BY-BREAKING — prompt judge to find fatal-flaw / strongest-objection / refute; ✗ rate-1-10. rating rationalizes, defect-hunt catches.
  2. VERIFY-THE-VERIFIER — plant a KNOWN defect, confirm judge flags it. miss ⇒ judge=theater ⇒ green-light = false-confidence (worse than no judge). = break-on-purpose keystone @ judge-layer.
  3. feed REAL artifact ¬ summary; let judge verify sources independently.
  4. DECORRELATE frames/models; N-copies-one-frame ⇒ shallow-agree, all-wrong-together.
- INTERPRETATION-BOUND — variation covers failure-modes ⇔ agent interprets {vary-space ∧ objective} right; else = thorough coverage of WRONG space. ∴ pin the objective; coverage bounded by interpretation ¬ variant-count. signal-rank: interpretation-independent-oracle > diverse-frame-judges > 1-judge > more-variants-1-interpretation (theater). kin: [[cooperative-game-elicitation-stack]] (the v is the hard part).
- GOODHART — optimize-score ⇒ game-evaluator. fix: un-gameable oracles, ✗ single climbable scalar. kin: [[observer-effect-discipline]].
- LOCAL-OPTIMA (secondary) — population + exploratory/refactor mutations; ✗ kill on single down-step. NOTE: weaker than it looks — bounded by interpretation (above).

**DISTILL human-judgment → mechanical checks (THE scaling move · ¬ opinion):**
human-in-loop = BOOTSTRAP ¬ solution. if loop only catches when human-in-seat ⇒ ✗ scale ⇒ worthless.
∀ human-catch ⇒ convert to author-independent check AI-judge runs WITHOUT the human.
catches = deterministic rules ([[handshake-math-terminology-determinism]]) ¬ opinions ∴ distillable. ≡ [[what-would-will-do]] (corrections = training-signal → next-projection-stronger → human-needed-less each pass). Will 2026-06-18: *"you MUST distill my human judgement to scale. it's not an opinion thing."*
**MECHANISM = deepfunding** ([[deepfunding-research]], Will 2026-06-18: *"that is deepfunding and pairwise"*): human PAIRWISE judgments (A-vs-B: which adds more) = ground-truth → distilled model generalizes to scale across all cases, ¬ ask-human-per-case. **PAIRWISE > absolute-rating = THE weak-judge fix**: judges reliable @ A-vs-B, unreliable @ rate-1-10 (the 2026-06-18 rating-judges caught little ∵ absolute). pairwise-fairness verifier (github WGlynn/pairwise-fairness) = axiom-check on output. ∴ the loop = deepfunding pointed at artifact-evolution.
**INGESTION** (Will 2026-06-18: *"this is why i always was asking you to keep tabs on their repo"*): the pairwise ground-truth AT SCALE = WATCHED REPOS. every merge / reject / review-comment = a free human "good/not" pairwise call. repo-watch loops (skill-mining · odysseus-advice-mining · anthropic-watcher · partner-repo tabs) = the INGESTION ARM feeding the distilled catch-rate. ∴ aim them at JUDGMENT-harvest (what reviewers catch · accept/reject/why) ¬ only techniques/opportunities.
Judge-rubric distilled from 2026-06-18 catches (feed judge the REAL conversation + run these):
1. REDUNDANCY (axis-A) — given full prior-exchange, list every draft-claim already present; flag if overlap high. [caught: v2-note ≈ post#4]
2. CREDENTIAL-DROP — flag every named theorem/framework/buzzword (Shapley·VCG·dogfood…); plain-concept-already-stated ∧ name-adds-0-concept ⇒ CUT. [caught: forced-Shapley/VCG/jargon]
3. OVER-CLAIM — flag open-Q-as-settled · formality-∄-proof ⇒ label conjecture-as-conjecture.
4. CALIBRATE (verify-verifier) — plant 1 known instance of each ⇒ judge MUST flag ∨ judge=theater.
goal: AI-judge inherits human catch-rate ⇒ loop scales human-out-of-seat.

**Inexperienced-engineer value (the WHY):** oracles = the senior-dev you don't have yet. judgment-surface shrinks → ~simplicity-only. confidence = oracle-trust ¬ self-trust.
KEYSTONE = mutation-gate: break-on-purpose ⇒ a test MUST go red. converts "tests pass" → "tests MEAN something". weak-passing-tests = the classic beginner trap ⇒ this gate kills it.

**Env constraints (hard):** ✗ mass-test-gen ([[lighter-test-generation]] — crashed before; fix/strengthen existing > spawn new) · targeted Foundry only (--match-path · ¬ via_ir · ≤3 concurrent) · maker≠checker ([[design-loops-not-prompts]]).

**Instances:** WRITING (judgment-scored) → `Desktop/marginal-contribution-writing.md` · CODE (oracle-scored, mutation-gate keystone, wired /critical-qa·/code-review·/verify·/simplify) → `Desktop/vibe-coding-confidence-loop.md`.

Composes: [[substrate-port-pattern]] · [[substrate-geometry-match]] · [[recursive-trp-rsi-on-docs]] (this = its principled-objective generalization) · [[ponytail-lazy-senior-dev]] (the simplicity/reuse cell) · [[first-available-trap]] (the audit that birthed the metaphor-clarification) · [[cooperative-game-elicitation-stack]] (Shapley=distribution-layer, needs a v) · [[atomized-shapley]] · [[self-adversarial-qa]] · [[code-text-inspiration-loop]] · [[complete-as-ready-for-critique]]
