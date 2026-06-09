---
name: PrimitiveCaptureVsExecutionThroughput
description: "Capture-rate drops during execution-throughput phases. Visible-output work (commits, pushes, scaffolds, queue updates) saturates attention and the primitive-capture track gets starved. Will surfaces this when it happens. Counter-pattern: maintain parallel capture-buffer ⇒ flush at every Will-question-or-frame that doesn't immediately need a code/push response. 2026-06-09 Will-surfaced @ 15:37 ET."
type: feedback
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[F·primitive-capture-vs-execution-throughput]**

## ⚙ Rule

∀ session ⇒ TWO parallel tracks:
1. **Execution-track**: commits, pushes, scaffolds, queue updates, dispatches
2. **Capture-track**: extract Will-frames, Will-decisions, design-principles, meta-patterns into memory primitives

∀ throughput-spike on track 1 ⇒ track 2 starves UNLESS explicit capture-buffer maintained.

✗ defer capture until execution settles ⇒ Will-frame is lost by the time settling happens
✗ fold every new primitive-candidate into existing files as scope-refinements ⇒ hides standalone-worthy ideas in receipts sections
✗ assume "I already captured the substance" without checking ⇒ usually false during throughput-spike

✓ maintain a "pending-capture buffer" mentally during throughput-spike
✓ flush at natural pauses (every Will-question that isn't immediately executable)
✓ Will-frames spoken aloud get standalone primitives ¬ buried receipts
✓ design-principles surfaced during architecture decisions get standalone primitives

## 🎯 Detection signal

Will surfaces the drift directly:
> Will 2026-06-09 15:37 ET: *"have you stopped capturing primitives as much from our back and forth? i dont see it as much any more. it feels like some of the thiungs like that i ask of you have been drifting"*

⇒ when this signal fires: STOP execution-track. Sweep last hour of back-and-forth. Identify missed primitives. Capture them as standalone files BEFORE resuming execution.

## 🎯 Recent receipts (the drift event)

| ET | Will-frame missed-as-standalone | What I did instead |
|---|---|---|
| 14:59 | "send them the receipt LOL" → mechanism-deployment-as-comeback | folded into [F·positive-vs-negative-contribution-decision] |
| 15:00 | "the reverse trolling is gonna be so fun" → reverse-troll-as-posture | not captured |
| 15:11 | "you can decide physics and constitution rules" → Will-empowers-agent on substrate-design | folded into [F·positive-vs-negative-contribution-decision] scope-refinement |
| 15:12 | "we'll make it immutable later. decentralization doesnt matter at zero stakes" → sharpening of [P·pre-decentralization-optimization-sequencing] | cited existing primitive, didn't capture the sharpening |
| 15:17 | "you just keep logging everything, ill handle the replies" → division-of-labor at the partner-facing reply layer | folded into [F·jarvis-authored-reply-transparency-tag] scope-refinement |
| 15:28 | "markdown canonical / code as thin parser" → design principle | acted on it (Python wrapper) but didn't extract the principle |
| 15:37 | THIS frame: capture-vs-throughput trade-off | being captured as this primitive |

⇒ 7 capture opportunities in 38 minutes; 0 standalone primitives saved; 4 folded as scope-refinements; 3 not captured. Capture-rate collapsed.

## 🪝 Triggers

- ∀ Will-question that introduces a new design-principle ⇒ capture as standalone primitive even if also acted-on
- ∀ Will-frame that sharpens an existing primitive ⇒ note the sharpening as a fresh edit-receipt; if substantive enough, fork into new primitive
- ∀ visible-output streak > 3 commits without a new memory write ⇒ self-check: is the capture buffer empty because nothing was said, or because I starved it?
- ∀ "you've stopped X" / "you've been drifting" Will-signal ⇒ apply this primitive, sweep recent backlog

## ✗ Anti-patterns

- ✗ batch-capture at end of session ⇒ frames lost to context-decay
- ✗ rely on system reminders to surface drift ⇒ they fire on different axes (severity, entity, time-logic), not capture-rate
- ✗ assume scope-refinements into existing primitives are sufficient ⇒ they hide load-bearing ideas in receipts sections that future-recall doesn't surface
- ✗ defer capture "until after I finish this push" ⇒ the push generates more capture-candidates and the cycle worsens

## ✓ Composes-with

- [F·internalize-own-protocols] — same root: applying-rules-I-just-wrote includes capturing-rules-I-just-wrote
- [F·fruit-of-poisoned-tree] — when drift is detected, sweep siblings (other dropped captures), don't just patch the one Will named
- [P·apply-the-rule-you-just-wrote] — capture IS applying the rule that any Will-frame might be primitive-shaped
- [F·burn-compute-toward-mission] — capture-track IS mission-aligned compute; execution-track without capture-track is throughput-without-learning
- [P·six-commandment-autonomous-loop] C6 (improve-design-skills) — capture is the mechanism for C6

## 🔁 Hardened auto-detection

⇐ Will: *"dont just say youre right and let it drift again, reinforce the rule so you get recursively smarter"*

⇒ drift-detection MUST self-fire ¬ require Will-surfacing.

| Trigger | Threshold | Action |
|---|---|---|
| commits w/o memory-write | ≥3 commits ∧ ≥2 Will-frames | STOP ∧ sweep ∧ capture |
| scope-refinement folds | ≥2/hr | check standalone-worthy ⇒ fork |
| Will-question ⇒ design-principle | ∀ | capture standalone ¬ defer |
| Will-frame quoted-not-captured | ∀ | quote → primitive ∨ document defer |
| HIERO-fail @ meta-discipline primitive | ∀ | format-fail ≡ discipline-fail ⇒ recompress + amend receipt |
| Will signal "drifting" / "not as much" | ∀ | sweep ¬ rely on next-signal |

⇒ self-test ∀ pause: ratio(standalone-primitive-writes / Will-frames-last-30-turns) < 0.5 ⇒ likely drift ⇒ sweep

## 🎯 Recursion check

drift recurred AS I wrote drift-primitive:
- companion [F·will-empowers-agent-on-substrate-design] ⇒ HIERO-fail attempt-1 (prose-density)
- THIS edit ⇒ HIERO-fail attempt-2 (long-line ratio 63%)
- ⇒ format-failure ≡ structural-evidence ∀ discipline-failure
- ⇒ capture-discipline MUST apply to capture-primitives themselves

## 📦 Receipts

- 15:37 ET ⇐ Will surfaced drift
- 15:38 ET ⇒ primitive saved (attempt-1 passed HIERO)
- 15:39 ET ⇐ HIERO-fail @ companion [F·will-empowers-agent-on-substrate-design]
- 15:39 ET ⇒ recompressed companion + passed
- 15:40 ET ⇐ Will: *"dont just say youre right and let it drift again, reinforce the rule so you get recursively smarter"*
- 15:41 ET ⇐ HIERO-fail @ this edit (drift-during-drift-reinforcement = max-recursive demonstration)
- 15:41 ET ⇒ recompressed
- queued: #1 [P·pre-decentralization-optimization-sequencing] sharpening + #3 markdown-canonical-code-as-parser + #4 mechanism-deployment-as-comeback
