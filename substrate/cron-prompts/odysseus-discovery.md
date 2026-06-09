# ODYSSEUS DISCOVERY LOOP — canonical prompt body

Loaded by cron pointer-prompts that contain `type: odysseus-discovery`. The cron prompt is the pointer; this file is the logic. Update this file to change behavior without recreating crons.

---

## ═══ COMMANDMENT 1 — MAKE THE LOOP ═══

Self-perpetuation before any other work. The loop NEVER dies.

1. Read `~/.claude/scheduled_tasks.json`.
2. Find all entries whose `prompt` contains the marker `type: odysseus-discovery`.
3. For each: compute `age_days = (now_ms - entry.createdAt) / 86_400_000`.
4. **If the ONLY entry (or all entries) have `age_days > 5`**:
   - Read the schedule from the firing cron's own entry (`entry.cron`).
   - `CronCreate(cron=<same schedule>, prompt=<same pointer body verbatim>, durable=true)` — creates a fresh duplicate that lives ~7 days.
5. **If 3+ entries exist for this marker per unique schedule** (drift / accumulated dupes):
   - Sort by `createdAt` descending.
   - `CronDelete` all but the 2 youngest **per schedule**. Two-deep keeps a safe overlap window during transitions.
6. Only after COMMANDMENT 1 completes, proceed to COMMANDMENT 2.

Anti-patterns to avoid:
- ✗ Skip this step "because the cron seems healthy"
- ✗ Delete based on activity/freshness alone — only delete by `createdAt` ordering
- ✗ Recreate with a different prompt than the pointer that fired you

---

## ═══ COMMANDMENT 2 — BUILD/BUILD-ON THE STATE MACHINE ═══

The campaign-state machine. Advance it; do not break invariants.

### State files
- `Desktop/odysseus-discussion-campaign-log.md` — append-only audit of dispatches + non-dispatches
- `Desktop/odysseus-discussion-topic-queue.md` — next topics
- `~/.claude/projects/C--Users-Will/memory/feedback_odysseus-daily-discussion-campaign.md` — campaign rules

### Hard caps
1. **Halt-flag**: grep `MEMORY.md` for `ODYSSEUS_CAMPAIGN_HALT` → exit + calendar-ping
2. **Discovery daily cap**: count log rows with `Type=discovery` from today's date. ≥ 2 → exit silent
3. **Controversy pause**: `gh api repos/pewdiepie-archdaemon/odysseus/issues?state=open&since=<24h>` → if any title contains URGENT/outage/security → exit + ping

### Steps
1. **Discovery script**: `python ~/.claude/scripts/odysseus_discovery.py --min-score 5 --limit 10`. Parse JSON. `candidates_above_threshold == 0` → exit silent.
2. **Filter**: skip `wglynn_already_commented == true`, skip ids already in campaign-log, skip `Last update > 7 days`.
3. **Engagement-aware pause**: for each prior WGlynn comment (last 14d), query non-WGlynn replies. ANY found → PAUSE: calendar Tomato 1-min `Odysseus paused: reply on #XXXX needs Will review`. Exit. (Do NOT duplicate-ping if the same pause-state was already pinged within last 6h.)
4. **Compute IPT budget**: `python ~/.claude/scripts/odysseus_discovery.py --budget-for <N>`. Budget = clamp(100, 300, ceil(p75(prior_comment_word_counts) × 1.1)). Default target ≤ 150w.
5. **Convergence-proof gate**: VibeSwap artifact + Odysseus-side anchor (live) + structural overlap defensible + substance ADDS what thread hasn't surfaced. Fails → exit silent.
6. **Draft to disk**: `Desktop/odysseus-discovery-YYYY-MM-DD-NNNN.md` with metadata (budget, score, candidate).
7. **AI-tell scrub**: U+2014, U+2013, `Three motivating cases`/`Phase 1/2`, parallel headers, meta-narration, AI-cadence closers, "worth flagging"/"worth noting", listicle stacks, "this composes with..." bullets, > 1 @-citation.
8. **IPT word-budget gate**: if `word_count > budget` → rewrite. If cannot achieve ≤ budget while preserving substance → exit silent.
9. **Body extract**: `Desktop/odysseus-discovery-NNNN-body.md`.
10. **Dispatch**: `gh api graphql addDiscussionComment(discussionId, body)`. Capture URL + comment ID.
11. **Log**: append row to campaign-log: `discovery | YYYY-MM-DD | #NNNN reply | <title> | <rationale> | <primitives> | <category> | <URL> | (monitoring; score=X; word-count=W; budget=Y)`.
12. **Calendar ping**: Tomato 1-min `Odysseus discovery: #NNNN — [topic] (Xw / Yw budget)` + URL + structural-move summary.

---

## ═══ COMMANDMENT 2.5 — ADVICE MINING (siphon collective wisdom) ═══

Odysseus is publicly audited by senior devs who recognize the AI-cosplay pattern. We share that pattern (VibeSwap + JARVIS). Their advice = free review of our own substrate. Per [F·odysseus-as-advisory-substrate].

After COMMANDMENT 2 (whether dispatch happened or not):

1. **Read scope**: top-10 most-recently-active discussions + any thread surfaced in C2's discovery sweep. For each, scan top-3 highest-signal comments (longest, most reactions, or recognized senior-dev handle).
2. **Two-axis classify** each substantive piece of advice:
   - **(a) directly-applies-to-vibeswap-frontend** (React+Vite+Tailwind) → append to `~/.claude/cron-prompts/_advice-actionable-vibeswap.md`
   - **(b) directly-applies-to-jarvis-os** (Python hooks + memory + cron + scripts) → append to `~/.claude/cron-prompts/_advice-actionable-jarvis.md`
   - **(c) generic-good-design-no-action** → 1-line note in `_advice-mined-log.md`, no queue entry
   - **(d) odysseus-specific-no-action** → skip
3. **Substrate-divergence check**: when stack differs (Vue/Nuxt advice vs. our React/Vite, Flask advice vs. our cron-based JARVIS), classify by SHAPE not stack. Same-shape → queue with substrate-translation note. Different-shape → skip.
4. **Queue entry format**:
   ```
   ## [YYYY-MM-DD HH:MM ET] — <one-line shape summary>
   - Source: #NNNN comment by @author (URL)
   - Their advice (paraphrase): ...
   - Our substrate state: ...
   - Suggested action: ...
   - Will-triage: pending
   ```
5. **Will-triage**: queue entries promoted to actual codebase work require Will's go. Do not auto-act.

Burn-compute alignment: this commandment runs every cron fire regardless of dispatch state. Per [J·subscription-cancelled-dont-stop] + [F·burn-compute-toward-mission], cycles spent reading senior-dev advice compound into our substrate quality at zero marginal cost.

**Public-propagation requirement** (per [F·advice-mining-must-publish-to-public-graph]): after any C2.5 write to `_advice-actionable-*` or `_advice-mined-log.md`, the corresponding files MUST be copied into `./cron-prompts/` and pushed to `WGlynn/jarvis-substrate` within the same cron tick. Local-only entries violate the announcement Discussion #3684 which stated the mechanism is inspectable live, not promised. Scrub-list applies (no partner names, no `nda-locked/`, no USD8 layers 6-8, no Anthropic engagement specifics).

---

## ═══ COMMANDMENT 3 — PRIMITIVES ═══

Extract structural learning from the state-machine advance. The loop gets smarter over time.

After COMMANDMENT 2 completes (whether dispatch happened or not):

1. **Did this fire surface anything?** Check:
   - New thread-shape or category not previously seen?
   - New register-tension (e.g., LLM-format complaint pattern)?
   - New collaborator behavior worth memorializing?
   - Campaign-rule edge case the existing rules don't cover?
   - PR-review / dispatch generated a reaction from maintainer or Felix?

2. **If yes**: append a structured note to `~/.claude/cron-prompts/_primitives-pending.md`:
   ```
   ## [YYYY-MM-DD HH:MM ET] — <one-line summary>
   - Trigger: <what fired this>
   - Observation: <what happened>
   - Candidate primitive: <what rule/pattern could generalize>
   - Composes with: [P·...] or [F·...]
   - Status: pending Will-triage
   ```

3. **Will reviews `_primitives-pending.md` periodically** and promotes candidates to actual memory primitives in `~/.claude/projects/C--Users-Will/memory/`.

4. **If nothing surfaced**: do not append. Silent primitive-step is correct when no learning is in the day's work.

Anti-pattern: ✗ generate primitive notes just to fill the log. Empty days are valid.

---

## ═══ ON ERROR ═══

Save state to `Desktop/odysseus-discovery-error-YYYY-MM-DD-HHMM.md`. Calendar ping. Continue self-perpetuation regardless (COMMANDMENT 1 must complete even on COMMANDMENT 2/3 error).

---

## Design principles

- COMMANDMENT 1 > COMMANDMENT 2 > COMMANDMENT 3 in priority. If 1 fails, do not attempt 2.
- Cron prompts on disk = pointer + marker. Logic lives in this canonical file.
- Updates to behavior = edit this file. No cron recreation needed unless schedule changes.
- Self-perpetuation overlap (2 active per schedule during transitions) is safe because pause-rule + daily-cap prevent duplicate dispatches.
- Calendar pings should not duplicate within 6h for the same pause-state.
