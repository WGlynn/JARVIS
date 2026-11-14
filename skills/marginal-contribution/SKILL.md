---
name: marginal-contribution
description: Score and improve a piece of writing for MARGINAL CONTRIBUTION — what it adds over prior work and the live thread, not polish. Use before declaring any substantive writing "done" (whitepaper, paper, post, reply, design doc, README), or when the user says "score this for contribution", "is this worth sending", "cut the redundancy", "run the writing loop / marginal-contribution loop", "mc this". The writing-side twin of /critical-qa (which is the code side). Operationalizes primitive_marginal-contribution-evolution-loop. Do NOT use for code (use /critical-qa, /code-review, /verify, /simplify) or for grammar/tone polish.
argument-hint: '<path-or-pasted-draft>  [--against <prior-corpus-or-thread>]  [--rewrite]'
user-invocable: true
metadata:
  emoji: "✂️"
---

# marginal-contribution — score writing by what it ADDS, not how polished it is

Operationalizes `primitive_marginal-contribution-evolution-loop` (writing instance) and
`Desktop/marginal-contribution-writing.md`. This is the writing-side twin of the code loop already
wired to `/critical-qa` `/code-review` `/verify` `/simplify`. The thesis: **the value of writing is
its marginal contribution over everything already said.** A flawless paragraph that restates known
material adds nothing. Optimize for the gap, never over-claim.

## Inputs to gather FIRST (the loop is theater without these)
The judge must see the **reference frame**, not just the draft:
1. **The prior work** the piece enters — the existing thread/papers/corpus/codebase on the topic. If a
   path or thread is given via `--against`, read it. Otherwise ask the user for it or name what you
   used. Do not score contribution against nothing.
2. **What the reader already knows.** Audience and the live conversation they are in.
3. The **draft** itself (the real artifact, never a summary).

## The two axes (BOTH required, gate A before climbing B)
- **AXIS-A — contribution to the CONVERSATION.** Reference = all prior work the audience already holds.
  Question: is this worth existing / sending AT ALL? **Gate this FIRST.** If A ≈ 0 (the draft restates
  what's already out there), STOP and say so — no amount of B-polish redeems polished redundancy. This
  is the most common failure of competent writing.
- **AXIS-B — contribution over the LAST ITERATION.** Reference = the previous draft. Question: is this
  revision improving, and has it converged? Climb B only after A passes. Converge when a round cannot
  beat the one before it (B-Δ → 0).

## The judge rubric (score by BREAKING, not by rating 1–10)
Run these as defect-hunts, with the prior work in hand. Rating rationalizes; hunting for the flaw
catches.
1. **REDUNDANCY (axis-A).** Given the full prior exchange, list every draft claim already present in
   it. High overlap ⇒ cut it or compress to a single line; put the document's weight on the gap.
2. **CREDENTIAL-DROP.** Flag every named theorem/framework/buzzword (Shapley, VCG, Myerson, "dogfood"…).
   If the plain concept is already stated and the name adds zero concept, CUT the name.
3. **OVER-CLAIM.** Flag any open question stated as settled, or an idea dressed as a proof. The honest
   move is to label a conjecture a conjecture. (This is what landed the whitepaper's "load-bearing open
   problem rather than a solved one" line — keep that discipline.)
4. **CALIBRATE (verify-the-verifier — the keystone).** Plant one known instance of each failure above
   into a probe draft; confirm the judge flags it. A judge that misses planted defects is theater, and
   its green light is worse than no judge.

## Judge hygiene
- **Maker ≠ checker.** Score with an independent perspective, not the author's. Decorrelate frames; N
  copies of one frame shallow-agree and are wrong together.
- **Pairwise > absolute.** Judges are reliable at "A vs B: which adds more"; unreliable at "rate 1–10".
  When choosing between variants, ask which contributes more, not for a score.
- **Correctness is a HARD GATE**, above usefulness/novelty/Δ. A false claim fails regardless of polish.

## The loop
1. Gate AXIS-A. If it fails, report that and stop (the most valuable output is often "don't send this").
2. Generate a few variants concentrating on the uncovered gap (cut restatement, compress known parts to
   single lines).
3. Score each by the rubric above with independent judgment.
4. Synthesize the winner. Repeat until B-Δ → 0.
5. Output: (a) the **cut list** — what was redundant/credential-drop/over-claim, (b) the **gap** the
   piece should concentrate on, (c) if `--rewrite`, the synthesized draft. Always show the cut list,
   not just the rewrite — the cuts are the contribution.

## Scope
Writing only. For code use the oracle-scored twin (`/critical-qa`, `/code-review`, `/verify`,
`/simplify`). This is not grammar or tone polish; it is contribution measurement.

## North star
Distill what a competent human reviewer would catch into mechanical checks the loop runs without them
(pairwise ground-truth, watched-repo merge/reject signal). A loop is only as good as its verifier;
the goal is a verifier that inherits a human's catch-rate so it catches at scale, author out of seat.
