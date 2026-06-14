# STORY MODE SELF-IMPROVEMENT LOOP — canonical prompt body

Loaded by cron pointer-prompts containing `type: story-mode-self-improve`. Pointer = cron; logic = this file. Edit here to change behavior without recreating crons.

Will 2026-06-14: *"also keep self improving story mode from here."* This loop makes Story Mode learn from its own hit/miss signal: the menu gets better at predicting Will's next move every cycle. Sibling discipline: [F·rank-primitives-by-catch-rate], [P·self-improving-protocol].

**The signal chain:** `story-mode-gate.py` logs every turn → `_system/story_signatures/will_{impressions,selections,offmenu}.jsonl` → `story_mode_metrics.py` computes the floor → THIS loop refines the ceiling (semantic reclassification) → updates `will.json` (weights + menu_rules) → next menu is sharper.

---

## ═══ COMMANDMENT 1 — MAKE THE LOOP ═══
Self-perpetuation first. Marker: `type: story-mode-self-improve`.
1. Read `~/.claude/scheduled_tasks.json`; find entries with this marker.
2. age_days = (now - createdAt)/86_400_000. All > 5 ⇒ `CronCreate(same schedule, same pointer, durable=true)`.
3. ≥3 per schedule ⇒ `CronDelete` all but 2 youngest per schedule.
4. Only then proceed to C2.

---

## ═══ COMMANDMENT 2 — IMPROVE THE MENU ═══

### Step 1 — deterministic floor
`python ~/.claude/projects/C--Users-Will/memory/_system/story_mode_metrics.py`. Capture catch-rate LB, precision@3, pick distribution, standing-slot share, recent off-menu.

### Step 2 — semantic reclassification (the part only an LLM can do)
For each recent off-menu prompt, read the transcript turn it belongs to and classify into exactly one:
- **paraphrase-catch** — the prior menu HAD this intent; Will typed it instead of the number. Counts as a CATCH (true catch-rate ≥ floor). Lesson: the affordance for typing-vs-tapping is fine; no menu change needed.
- **conversational** — banter / meta / question about the menu itself / a test prompt / a `type:` cron injection. NO menu could or should anticipate this. EXCLUDE from the denominator entirely — counting it as a miss is the measurement bug.
- **genuine-miss** — Will wanted a concrete action that was absent from the 10. THIS is the only true miss. Mine it.

Report: true catch-rate = picks ÷ (picks + paraphrase-catches + genuine-misses), conversational excluded.

### Step 3 — mine genuine-misses
For each genuine-miss: what action did Will want? Which signature-move class? Was it situational (should have been items 1-7) or a standing move (8-10)? Propose the menu item that WOULD have caught it (≤10 words, executable).

### Step 4 — reweight (only on real signal, ≥10 new actionable turns since last run)
- Bump `signature_moves[].weight` toward classes Will actually picks (selections distribution); decay unpicked classes. Renormalize to sum≈1.0.
- If genuine-misses cluster on a recurring intent ⇒ add an example to the matching class, or propose a new class.
- Anti-blandness: if standing-slot share (8-10) is HIGH while situational (1-7) catch-rate is LOW, the situational items are bland ⇒ tighten the menu_rules toward live-decision specificity. (Current data: standing share LOW, situational doing the work ⇒ healthy; do not over-correct.)
- Write changes to `will.json`. Keep a dated backup line in `_system/story_mode_improvements.md`.

### Step 5 — propose deterministic gate fixes
When a pollution source is mechanical (e.g. `type:` cron injections logging as off-menu), propose/apply a guard in `story-mode-gate.py` so the floor metric stops counting non-menu turns. Code fix > metric caveat.

---

## ═══ COMMANDMENT 3 — LOG THE CYCLE ═══
Append a dated block to `~/.claude/projects/C--Users-Will/memory/_system/story_mode_improvements.md`:
floor metrics · reclassification counts · true catch-rate · genuine-misses found · weight deltas applied · gate fixes shipped. Empty cycle (no new actionable turns) ⇒ one line, no changes. Commit + push memory (origin + backup).

---

## ON ERROR
Save to `Desktop/story-mode-self-improve-error-YYYY-MM-DD-HHMM.md`, ping, C1 must still complete.

## Design principles
- The floor (script) is cheap and deterministic; the ceiling (reclassification) needs the LLM + transcript. Don't fake the ceiling in the script.
- Conversational turns are NOT failures. Excluding them is the single biggest measurement correction.
- Reweight only on real signal — churning weights on <10 turns overfits noise.
- Every menu shown is a prediction; every reply grades it. The loop closes that grade back into the predictor.
