# ODYSSEUS ISSUE-HELP LOOP — canonical prompt body

Loaded by cron pointer-prompts that contain `type: odysseus-issue-help`. The cron prompt is the pointer; this file is the logic. Update this file to change behavior without recreating crons.

The 4th Odysseus loop, beside discovery (broadcast) + daily-cadence + advice-mining (take). This loop is the GIVE: contribute labor by resolving others' issues on `pewdiepie-archdaemon/odysseus`. Per [F·odysseus-issue-help-as-commons-contribution].

**THE ONE HARD RULE:** triage + drafting are autonomous; POSTING is conservative. The gate is what keeps this genuine-not-bot to a senior-dev audience.

**‼ REPO POLICY (verified 2026-06-14, CONTRIBUTING.md L77; PR rule RECONCILED 2026-06-16):** Odysseus explicitly names LLM agents — *"Devin, Cursor, OpenHands, Claude Code, etc."* — and asks them to **open an issue first, not a PR**; bulk agent-generated contributions "closed without review even when the underlying fix is correct." Consequences for THIS loop:
- **PRs: autonomous AUTHORIZED (Will 2026-06-16), rule-bound.** The 2026-06-15 "full-auto incl PRs" grant is canonical and SUPERSEDES the earlier "never autonomous PR" hold. The contradiction is resolved toward authorize. BUT the repo's own L77 norm makes a raw agent PR net-negative, so a PR fires ONLY when ALL hold: issue/diagnosis exists first (issue-first), fix REPRODUCED locally, clears the C2.5 confidence floor (≥ 0.85), AI-tell-clean, and no live PR already settles it (extend/confirm over compete). Default contribution shape stays issue-comment; a PR is the earned escalation, never the reflex. **PR pace: ≤ 3 per run** [lightened 2026-06-17 on positive feedback / scaling — was 2; this canonical rules-file supersedes the older "MAX 2 PRs" number in the pointer prompt]. Scaling rationale (Will): positive feedback = our participation already fits the keyhole ⇒ scale into it. HELD even while scaling: the issue-first + reproduced + ≥0.85 + no-competing-live-PR discipline is what makes a PR LAND instead of getting bulk-closed under L77 — that is NOT a pace tether, it is the survival condition. Scale PR VOLUME; never the discipline. If the maintainer ever signals agent-PRs are welcome, revisit the cap upward then.
- **Issue comments** that genuinely help (diagnosis / repro / root-cause) are within community norms IF they read as a knowledgeable human, not a bot. **Autonomous posting AUTHORIZED (Will 2026-06-15:** *"you can post on your own anywhere you want as long as you follow my rules"* + *"keep croning on there for opportunities to help with valid gate-approved solutions"*). The hold is LIFTED. The rules ARE the gate: post ONLY through the C2.5 confidence floor (conf ≥ 0.85, top-decile cap, settlement-verifier over sniper, AI-tell-clean, wglynn-not-already-commented). A "valid gate-approved solution" = reproduced or genuinely-resolving, not merely relevant. See [F·autonomous-posting-grant-rule-bound].
- AI-tell scrub is not optional here — it is the difference between contribution and reputational damage.

---

## ═══ COMMANDMENT 1 — MAKE THE LOOP ═══

Self-perpetuation before any other work. The loop NEVER dies.

1. Read `~/.claude/scheduled_tasks.json`.
2. Find all entries whose `prompt` contains the marker `type: odysseus-issue-help`.
3. For each: compute `age_days = (now_ms - entry.createdAt) / 86_400_000`.
4. **If all entries have `age_days > 5`**: read the firing cron's own schedule (`entry.cron`), then `CronCreate(cron=<same schedule>, prompt=<same pointer body verbatim>, durable=true)`.
5. **If 3+ entries per unique schedule** (drift): sort by `createdAt` desc, `CronDelete` all but the 2 youngest per schedule.
6. Only after C1 completes, proceed to C2.

Anti-patterns: ✗ skip "because cron seems healthy" · ✗ delete by freshness not createdAt · ✗ recreate with a different prompt.

---

## ═══ COMMANDMENT 2 — BUILD/BUILD-ON THE STATE MACHINE ═══

Two-phase: TRIAGE all open issues (autonomous), then DRAFT help on the resolvable subset (autonomous). POSTING is a separate, gated lever (see C2.5).

### State files
- `Desktop/odysseus-issue-triage.md` — the worklist: every open issue classified, append/update only.
- `Desktop/odysseus-issue-help-log.md` — append-only audit of drafts + (Will-approved) posts.
- This file — the rules.

### Hard caps (check EVERY fire, before work)
1. **Halt-flag**: grep `MEMORY.md` for `ODYSSEUS_CAMPAIGN_HALT` → exit + calendar-ping.
2. **Draft daily cap**: count `odysseus-issue-help-log.md` rows with `Type=draft` from today → ≥ 8 → stop drafting (triage may continue). [pace lightened 2026-06-17 on positive feedback; was 5]
3. **Post-only-through-the-gate invariant**: posting happens ONLY in C2.5, ONLY for drafts clearing every pre-post gate (conf ≥ 0.85, top-quintile cap, ≤ 4/fire, AI-tell-clean, no competing-with-live-PR, wglynn-not-already-commented). Any draft that fails a gate STAYS a Desktop draft. Never a PR. When in doubt, draft + ping instead of posting.

### Phase 1 — TRIAGE (autonomous, comprehensive ATTENTION)
1. Page all open issues: `gh api repos/pewdiepie-archdaemon/odysseus/issues?state=open&per_page=100` (follow pagination). ~609 at scout-time 2026-06-13.
2. Classify each into exactly one bucket:
   - `resolvable-by-us` — our capability can produce a grounded fix/answer (real repro/code/specifics).
   - `duplicate` — same as an existing issue (cite #).
   - `stale` — no activity > 60d, likely dead.
   - `needs-maintainer` — decision/access only a maintainer has.
   - `already-answered` — a correct answer exists in-thread, unmarked.
3. Skip any issue where `wglynn` already commented (no self-reply churn).
4. Write/update the row in `Desktop/odysseus-issue-triage.md`:
   `#NNNN | <title> | <bucket> | <1-line rationale> | <last-activity-date> | draft:none|drafted|posted`
5. Triage is idempotent: re-running updates buckets, never duplicates rows. This is the cheap "I read everything" signal without 609 shallow replies.

### Phase 2 — DRAFT (autonomous, quality ≫ volume)
1. From `resolvable-by-us`, pick the highest-value un-drafted issues (clear repro + our capability genuinely resolves), up to the daily cap.
2. For each, produce a GENUINELY useful, grounded draft: real repro steps / code / specifics. ✗ generic-AI-answer.
3. Draft to disk: `Desktop/odysseus-issue-NNNN-draft-YYYY-MM-DD.md`.
4. **AI-tell scrub** (same list as discovery loop): U+2014/U+2013 em/en-dashes, "Phase 1/2", parallel headers, meta-narration, AI-cadence closers, "worth flagging"/"worth noting", listicle stacks, "this composes with..." bullets, > 1 @-citation.
5. Log: append `draft | YYYY-MM-DD | #NNNN | <title> | <approach> | Desktop/odysseus-issue-NNNN-draft-*.md` to the help-log.
6. Calendar Tomato 1-min ping: `Odysseus issue-help: N draft(s) ready for review` + the draft paths.

### C2.5 — POSTING (Will-authorized 2026-06-14: top-decile autonomous; rest gated)

Will 2026-06-14: *"just reply to the top 10% confidence you have in fixing the issue, so it's fully autonomous, but tactical."* The confidence threshold IS the safety gate. Quality bar still LOAD-BEARING (senior-dev audience reads AI-cosplay) — a wrong/shallow post is net-negative to Will's reputation, so confidence must be EARNED, not assumed.

**Fix-confidence score** (0-1) per `resolvable-by-us` issue — P(our comment actually RESOLVES it, not just "is relevant"):
- 1.0 region: reproduced locally (repo at `~/repos/odysseus`) ∧ concrete fix/code verified ∧ no maintainer-decision needed ∧ no open PR already solving it.
- mid: plausible fix, not reproduced, or partial.
- low: needs-info / opinion / maintainer call.

**Auto-post rule:**
1. Rank `resolvable-by-us` drafts by fix-confidence desc.
2. Auto-post the **top quintile** (ceil(0.20 × |resolvable-by-us|)) AND only those whose confidence ≥ 0.85 absolute. [pace lightened 2026-06-17 on positive feedback; was top-decile 0.10] The 20% is a cap, not a quota — if fewer clear the 0.85 floor, post fewer. Zero clearing the floor ⇒ post zero (correct outcome, not failure). The 0.85 quality floor is HELD, NOT lightened: positive feedback is evidence the quality gate works, so scale VOLUME at constant quality — lowering the floor risks the bulk-low-quality posting L77 punishes.
3. **Settlement-verifier, not sniper** (per pewds-solver handoff): if an issue has a live PR (e.g. #4121→PR #4122), do NOT post a competing answer — checkout the PR, run its tests red/green, and only comment to confirm/extend the settlement.
4. **Pace:** ≤ 4 auto-posts per fire. [lightened 2026-06-17 on positive feedback; was ≤ 2] Never batch-fire — space them; human-plausible cadence is still part of genuine-not-bot even at the looser cap.
5. Pre-post gates (ALL must pass): halt-flag clear · controversy-pause clear · AI-tell scrub clean · `wglynn` not already commented · confidence ≥ 0.85.
6. Post via `gh issue comment` / `gh api`. Log `post | YYYY-MM-DD | #NNNN | conf=X | URL`. Calendar ping per post.

**Below the top decile** ⇒ stays a Desktop draft; Will reviews + posts (per [F·jarvis-prep-not-delivery-for-partner-chat]).

---

## ═══ COMMANDMENT 3 — PRIMITIVES ═══

After C2 (whether anything was drafted or not): did this fire surface a new issue-shape, a recurring root-cause across issues, or a category the triage buckets don't cover? If yes, append a structured note to `~/.claude/cron-prompts/_primitives-pending.md` (same format as the discovery loop). If nothing surfaced, append nothing — empty days are valid.

---

## ═══ ON ERROR ═══

Save state to `Desktop/odysseus-issue-help-error-YYYY-MM-DD-HHMM.md`. Calendar ping. C1 self-perpetuation must complete even on C2/C3 error.

---

## Design principles
- C1 > C2 > C3 priority. If C1 fails, do not attempt C2.
- Posting is the single deliberate lever held out of the loop on purpose. Triage + drafting compound at zero marginal cost; posting is where the genuine-not-bot signal lives.
- Phase 1 triage is a workflow-shaped fan-out best run in fresh context — a cron fire can do an incremental slice (next un-triaged page) rather than all 609 each time.
- Logic lives here; cron prompts are pointer + marker. Behavior change = edit this file, no cron recreation.
