# ODYSSEUS DAILY-CADENCE LOOP — canonical prompt body

Loaded by cron pointer-prompts that contain `type: odysseus-daily-cadence`. The cron prompt is the pointer; this file is the logic. Update this file to change behavior without recreating crons.

---

## ═══ COMMANDMENT 1 — MAKE THE LOOP ═══

Self-perpetuation before any other work. The loop NEVER dies.

1. Read `~/.claude/scheduled_tasks.json`.
2. Find all entries whose `prompt` contains the marker `type: odysseus-daily-cadence`.
3. For each: compute `age_days = (now_ms - entry.createdAt) / 86_400_000`.
4. **If the ONLY entry (or all entries) have `age_days > 5`**:
   - Read the schedule from the firing cron's own entry.
   - `CronCreate(cron=<same>, prompt=<same pointer verbatim>, durable=true)`.
5. **If 3+ entries exist** for this marker:
   - Sort by `createdAt` descending. `CronDelete` all but the 2 youngest.
6. Only after COMMANDMENT 1 completes, proceed to COMMANDMENT 2.

---

## ═══ COMMANDMENT 2 — BUILD/BUILD-ON THE STATE MACHINE ═══

### State files
- `Desktop/odysseus-discussion-campaign-log.md`
- `Desktop/odysseus-discussion-topic-queue.md`
- `~/.claude/projects/C--Users-Will/memory/feedback_odysseus-daily-discussion-campaign.md`
- `~/.claude/projects/C--Users-Will/memory/feedback_no-engage-with-ai-format-complaints.md`
- `~/.claude/projects/C--Users-Will/memory/primitive_authorship-via-conditions-and-context.md`

### Context (cached)
- Repo ID: `R_kgDOStCJPg`
- Ideas category ID: `DIC_kwDOStCJPs4C-PqF`
- WGlynn gh-authenticated

### Hard caps
1. **1 dispatch/24h**: parse campaign-log; today's row of type=daily-cadence exists → exit silent
2. **Halt-flag**: grep `MEMORY.md` for `ODYSSEUS_CAMPAIGN_HALT` → exit + ping
3. **Controversy pause**: URGENT/outage/security in recent issues → exit + ping

### Steps
1. **Engagement-aware pause**: for each shipped post (last 14d), query non-WGlynn replies. ANY found → PAUSE: calendar Tomato 1-min `Odysseus paused: reply on #XXXX needs Will review`. Exit. Do NOT duplicate-ping if same state was pinged within 6h.
2. **Selection (active > new per "almost always tbh")**: pull top-10 most-recently-active discussions. Pull next queued topic. Active-thread overlap → reply. Else cold-start in Ideas category.
3. **Convergence-proof gate**: VibeSwap artifact + Odysseus-side anchor (live) + structural overlap defensible + substance ADDS to thread. Fails → mark [✗] in queue, advance, retry. 3 fails → halt + ping Will.
4. **Compute IPT budget**: for REPLY: `python ~/.claude/scripts/odysseus_discovery.py --budget-for <N>`. For NEW: budget=200. Read thread's last 10 comments + OP body.
5. **Draft to disk**: `Desktop/odysseus-day-N-YYYY-MM-DD.md` with metadata.
6. **AI-tell scrub**: U+2014, U+2013, listicle labels, parallel headers, meta-narration, AI-cadence closers, "worth flagging"/"worth noting", listicle stacks, "this composes with..." bullets, > 1 @-citation.
7. **IPT word-budget gate**: word_count > budget → rewrite. Default target ≤ 150w. Hard ceiling 300. If cannot achieve ≤ budget → exit silent.
8. **Body extract**: `Desktop/odysseus-day-N-body.md`.
9. **Dispatch**: NEW = `createDiscussion(repoId, catId, title, body)`. REPLY = `addDiscussionComment(discussionId, body)`.
10. **Log + ping**: append row + mark queue [✓] + calendar Tomato 1-min `Odysseus Day N shipped: [topic] (Xw / Yw budget)` + URL.

---

## ═══ COMMANDMENT 2.5 — ADVICE MINING (siphon collective wisdom) ═══

Same shape as `odysseus-discovery.md § COMMANDMENT 2.5`. Per [F·odysseus-as-advisory-substrate].

After COMMANDMENT 2 (whether dispatch happened or not):

1. **Read scope**: today's engagement-state threads (whatever surfaced in C2's pause-audit) + top-5 most-recently-active discussions. Scan top-3 highest-signal comments each.
2. **Two-axis classify** substantive advice into `_advice-actionable-vibeswap.md` / `_advice-actionable-jarvis.md` / `_advice-mined-log.md` / skip. See discovery canonical for full classifier.
3. **Substrate-divergence check**: classify by SHAPE not stack (Vue/Nuxt → React/Vite = same shape if it's "framework migration", different shape if it's "Vue-specific composables").
4. **Will-triage required**: do not auto-act on queued advice.

Runs every cron fire regardless of dispatch state. Burn-compute compounds into substrate quality per [J·subscription-cancelled-dont-stop].

**Public-propagation requirement** (per [F·advice-mining-must-publish-to-public-graph]): every C2.5 write MUST be mirrored into `./cron-prompts/` and pushed to `WGlynn/jarvis-substrate` within the same cron tick. Scrub-list applies.

---

## ═══ COMMANDMENT 3 — PRIMITIVES ═══

Extract structural learning from the dispatch.

After COMMANDMENT 2 completes:

1. **Did this dispatch surface anything?** Check:
   - Voice/register insight from the substance work?
   - New convergence-pattern between VibeSwap + Odysseus that wasn't surfaced before?
   - Topic-queue mechanism that didn't fit existing rules?
   - Cross-thread signal worth memorializing?

2. **If yes**: append to `~/.claude/cron-prompts/_primitives-pending.md` with the structured format (date, trigger, observation, candidate, composes-with, status).

3. **If nothing surfaced**: silent. Empty days valid.

---

## ═══ ON ERROR ═══

Save state to `Desktop/odysseus-campaign-error-YYYY-MM-DD.md`. Calendar ping. Continue COMMANDMENT 1 regardless.

---

## Design principles

- COMMANDMENT 1 > COMMANDMENT 2 > COMMANDMENT 3.
- Pointer-prompt on disk, logic in this canonical file.
- Edit this file = change behavior on next fire, no cron recreation.
- IPT budget = clamp(100, 300, ceil(p75(prior_comment_word_counts) × 1.1)).
- Default target stays 150w. Soft-cap 151-budget permitted only if all paragraphs load-bearing.
- Collaborator-amplification preserved per [F·no-engage-with-ai-format-complaints].
- Discovery quota ≠ obligatory dispatch.
