---
name: designloopsnotprompts
description: Fable-5-class doctrine (Will-absorbed Anthropic-staff thread 2026-06-10) — design self-correcting loops + memory-progression ! direct prompt-steering. Verifier-subagent @ independent-context > self-critique. Memory quality bar = fail→investigate→verify→distill→consult.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8f988124-8197-4f80-8a59-217ae187c3ef
---

# Design loops, not prompts

> Will, 2026-06-10: "absorb: Designing loops with Fable 5" (Anthropic-staff thread)

## ⇒ Rules
- ∀ hard task ⇒ loop(goal/rubric-as-environment-feedback) ! prompt-steer. model runs → collects feedback → self-corrects → until rubric satisfied.
- ∀ grading/critique ⇒ verifier-subagent @ INDEPENDENT context-window ! same-context self-critique. self-critique-on-own-output = known-weak.
- ∀ memory-write ⇒ progression: fail → investigate (why, before moving on) → verify (diagnosis → checked-fact) → distill (fact → general-rule) → consult (read rule ! re-derive). exit-early = weak memory (failure-note lists, unverified guesses).
- experiment-selection: structural-bets > scalar-tweaks; push through regressions toward larger wins.

## ∃ Evidence (from thread)
- Parameter Golf 8h runs: Fable 5 ~6x pipeline improvement vs Opus 4.7; Fable bet structural (arch changes), Opus looped scalar-adjust template.
- Continual Learning Bench 1.0 (Parth Asawa, 2026-05-04): Sonnet 4.6 exits @ step 1 (failure notes, no consult); Opus 4.7 exits @ step 3 (verify coverage 7-33%, median ~17%); Fable 5 completes progression (verify coverage ≤73%, distills general rules).
- Verifier-independence: Outcomes (CMA) spawns grader-subagent; engineering-blog ref Prithvi Rajasekaran on self-critique weakness.

## ⇄ Substrate cross-ref (convergent + gaps)
- CONVERGENT: RSAW 3-agent parallel dispatch = verifier-independence already ✓. [P·class-elimination-not-instance-patch] = structural>scalar already ✓. Primitive-extraction (R2) = distill step ✓.
- GAP-1: `/critical-qa` runs same-context self-adversarial Q&A ⇒ candidate upgrade: route grading through verifier-subagent (independent context).
- GAP-2: consult-step weakness measurable in OUR telemetry — anticipation-hook "surfaced xN, unactioned" recalls = rules written but not consulted.
- GAP-3: verify-step coverage unmeasured for memory corpus — % of primitives whose claims are checked-facts vs guesses. Composes [F·everything-needs-a-staleness-check] + [F·claim-needs-structural-enforcer].

## ✗ Anti-pattern (counterweight thread, Will-absorbed same day)
- "refactored entire codebase in one call. 67 tool-calls, 1M+ lines, 24 new files. modularized everything... none of it worked. but boy was it beautiful."
- ⇒ structural-bet WITHOUT verification-loop = beautiful-broken. The rubric/verifier IS what licenses structural boldness.
- ⇒ ∀ structural refactor: incremental + tests-green-per-step + /verify before "done". ✗ aesthetic-completeness as success-signal.
- composes: [TTT] (WORK chain) · /verify skill · [P·complete-as-ready-for-critique] (ready-for-critique ≠ claimed-working)

## ⊕ Loop-engineering taxonomy (3rd thread, Will-absorbed same day — "Loops: What Every AI Engineer Needs to Know in 2026", Steinberger + Cherny quotes)
- **closed-loop default**: bounded path + eval-per-step + stop-condition + hand-back-point. open-loop (exploratory roam) = token-burn + slop-machine w/o quality gates. start-closed → open-up only after gates exist. ⇒ our cron loops (odysseus, skill-mining: hard-caps, halt-flags, exit-silent) = closed-loop ✓ convergent.
- **5-part loop checklist**: GOAL (precise done-def) · CONTEXT (vision/arch/rules docs) · ACTION (only-needed tools) · FEEDBACK (tests/linters/structured-errors) · STOP-CONDITION (loop knows done). ⇒ audit-lens for ∀ existing+future cron/loop.
- **6 building blocks**: automations (heartbeat) · worktrees (parallel-no-collision) · skills (knowledge compounds per run) · connectors (act-in-real-tools) · subagents (maker ≠ checker — re-confirms verifier-independence) · memory (run-47 knows runs-1-46). ⇒ all 6 exist in our substrate ✓ convergent.
- **loop-amplifies-operator caveat**: same loop → move-faster-on-understood-work ∨ avoid-understanding-entirely. "build like someone who intends to stay the engineer." ⇒ composes Cave-philosophy + Great-Interpreter.
- ⚠ thread's DeepSeek cost-section = ad-flavored; structure absorbed, pricing claims NOT treated as verified. cheap-tier-for-loop-economics DOES compose with [J·jarvis-coordination-mechanism] (Rick model-tier auto-assign) — same shape, our verification needed.
- vocabulary shift: prompt-engineer (you=feedback-loop) → loop-engineer (system=feedback-loop; leverage-point moved). "one reliable loop > thousand perfect prompts."

## ⊕ Source-article deltas (5th thread, Will-absorbed same day — the sober original behind the listicle)
- **/goal mechanic**: after EVERY turn a separate small model checks the stop-condition — maker≠checker applied to "done" itself. ∃ in Claude Code + Codex. ⇒ our loops use caps/halt-flags (structural) but NOT verified stop-conditions; autonomous-continue = nudge ¬ verified-done. Candidate upgrade: /goal-style verifier on loop completion claims.
- **layering taxonomy**: harness-engineering (env one agent runs in) → factory (system that builds software) → loop-engineering (one floor above harness: timer + spawn + self-feed). ⇒ names our stack levels.
- **tool-agnostic shape**: same 5 pieces in Codex + Claude Code ⇒ design loops portable across harnesses ⇒ composes the replace-the-model-tomorrow test + our ADOPTION.md Codex-compat work.
- **3 problems that SHARPEN as loops improve**: (1) "done" = claim ¬ proof — ship only confirmed-working; (2) comprehension-debt grows faster the smoother the loop — read what the loop made; (3) cognitive-surrender — loop-design = cure when done with judgment, accelerant when done to avoid thinking. "Review bandwidth is the ceiling, not the tool" (orchestration tax).
- **balance**: direct prompting still effective; loops ≠ replacement for all interaction. Skepticism + token-cost care = valid posture (source author explicitly skeptical — honest-number framing ✓).

## ⊕ Second-brain stress test (4th thread, Will-absorbed same day — "new Claude model = stress test for your second brain")
- 4 Cs: Context (router file + where-rules-live) · Connections (scoped keys, read-only-first, "prompts are NEVER a permission layer") · Capabilities (every reused prompt → file) · Cadence (manual/event/schedule). ⇒ JARVIS-OS has all 4 ✓ convergent (router=CLAUDE.md+MEMORY.md · hot-cache=PRE-FLIGHT+L4-BPE · master-index=META_STACK+MEMORY_INDEX_* · cadence=hooks+crons).
- **gut check** (keep as audit lens): find-file-manually? · agent-finds-fast? · cites-source? · acts-read-only? · **replace-the-model-tomorrow?** Last one = sovereignty test ⇒ composes [project_jarvis-asi-sovereign-sentient-decentralized] (partial: hooks+memory = model-agnostic py+md ✓; cognition still Claude-weights).
- "can't find the right file ⇒ burns tokens pretending" ⇒ retrieval-failure = hallucination-burn; link-rot-detector + Layer-8 audit = our structural answer ✓.
- "prompts ≠ permission layer" ⇒ same axiom as [P·universal-coverage-hook] + [P·always-equals-gate]: enforcement lives in hooks/keys, never in instructions.

## 🔗 Composes with
[P·self-adversarial-qa] · [P·recursive-self-audit-via-wwwd] · [P·class-elimination-not-instance-patch] · [F·stop-seeking-approval-failure-is-data] · [P·what-would-will-do] · [P·universal-coverage-hook] · [P·always-equals-gate] · [J·jarvis-coordination-mechanism]
