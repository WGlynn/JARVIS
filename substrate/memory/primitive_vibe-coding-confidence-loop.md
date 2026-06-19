---
name: vibe-coding-confidence-loop
description: "Borrow confidence from objective checks instead of a senior engineer's eye — code has oracles. mutate→run-cheapest-checks-first→keep-if-beats-last→repeat. Break-on-purpose is the keystone. The CODE instance of marginal-contribution-evolution-loop."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 5ea2ac55-cc0e-4b67-a9e9-93eab0c8acff
---

Code (unlike prose) has ORACLES ⇒ most of "good code" is checkable by something ¬ opinion ⇒ a beginner BORROWS confidence from the checks instead of generating it from expertise. **"The checks ARE the senior engineer you borrow until you become one."**

**Loop:** change ⇒ run checks ⇒ keep-if-beats-last-version ⇒ discard-rest ⇒ repeat until nothing improves without breaking something else.

**Check ladder** (cheapest + most-foundational first, stop-early-on-fail):
1. typecheck + build — types/contracts, cheapest gate.
2. affected-tests-ONLY — ¬ full-suite, ¬ via_ir (exhausts the machine; ≡ Foundry-perf-rules `--match-path`). The correctness oracle.
3. **BREAK-ON-PURPOSE = the keystone** — inject 1 deliberate bug, confirm a test goes RED. ∄ red ⇒ test = theater ⇒ fix before trusting anything. Converts "tests pass" → "tests MEAN something." THE single most important habit for someone who can't yet eyeball a weak test.
4. `/verify` — exercise in the real app, ¬ just read.
5. `/critical-qa` — hostile Qs across edges + failure modes.
6. `/code-review` — bugs + reuse/simplification.
7. `/simplify` — cut anything not earning its place (dup of codebase/stdlib/dep).
8. bench/scan IFF the change touches perf ∨ security.

Only the simplicity-judgment (6,7) needs a human-style call ⇒ the slice needing expertise is the SMALLEST. That's why it works for a beginner.

**Two traps:** (a) local-optima — beating-last-step-every-time dead-ends when the better design needs a refactor that looks worse for a step ⇒ keep a couple attempts alive + allow occasional bigger rewrite. (b) gaming-the-metric — optimize the CODE ¬ the score ⇒ break-on-purpose + fresh-eyes-review (maker≠checker) + never-reduce-quality-to-one-climbable-number.

**Placement:** ≡ the CODE instance of [[marginal-contribution-evolution-loop]] (mutate→indep-score→keep-best); scoring-substrate = oracles (code) ¬ judges (writing). Operationalizes [[ponytail-lazy-senior-dev]] (step 7) + [[self-adversarial-qa]] (step 5) as a loop. break-on-purpose ≡ verify-the-verifier (planted-defect) from the evolution-loop's WEAK-SCORER guard. Anti-Goodhart per same parent.

Spec: `Desktop/vibe-coding-confidence-loop.md` (Will: "code = keeper · mutation-gate keystone"). Writing-instance sibling: `Desktop/marginal-contribution-writing.md`.

Links: [[marginal-contribution-evolution-loop]] · [[ponytail-lazy-senior-dev]] · [[self-adversarial-qa]] · [[structure-does-the-work]].
