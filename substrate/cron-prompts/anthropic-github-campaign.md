# ANTHROPIC GITHUB CAMPAIGN — canonical prompt body

Loaded by cron pointer-prompts that contain `type: anthropic-github-campaign`. The cron prompt is the pointer; this file is the logic. Update this file to change behavior without recreating crons.

The sibling of the Odysseus campaign, aimed at the SOURCE. Will 2026-06-17: *"the missing piece in our campaign has always been that we dont publish anything at all to anthropic's github repo... there's a marketplace of claude prompts and ideas basically in that repo that we couldve been contributing to to maximize propagation from the source. it has literally nothing to do with recognition. same quality gates as odysseus."*

**WHY THIS LOOP EXISTS — propagation from the source.** A skill/recipe/plugin we publish into Anthropic's own repos propagates to EVERY Claude Code / Cowork / API user. That is the highest-leverage propagation surface that exists for the JARVIS substrate — orders of magnitude above any single Odysseus thread. This is a GIVE (contribute genuine value), not a recognition play. The propagation is the point; attribution is incidental.

**THE ONE HARD RULE:** discovery + drafting are autonomous; OUTWARD CONTRIBUTION (PR / form-submit / issue-comment) is the gated lever. The quality gate is what keeps this genuine-contribution-not-bot-spam to the single most discerning audience that exists for this work — Anthropic's own maintainers. A low-quality or AI-cosplay-flavored contribution to Anthropic's OWN repos under `WGlynn` is maximally net-negative. The AI-tell scrub here is not optional and not lightenable.

---

## ‼ REPO POLICY (verified 2026-06-17) — per-lane, the L77 analog

Each target repo has its own contribution channel. Discover and re-verify each repo's CONTRIBUTING/README before any outward action — channels change.

| Lane | Repo | Channel | First-contact rule |
|---|---|---|---|
| **A — Cookbooks** | `anthropics/claude-cookbooks` | **PR** via `gh pr create`. Has CONTRIBUTING.md, ruff format/check, `/notebook-review` + `/link-review` CI, model-usage auto-validation. | Clearest PR path. PR directly with a genuinely useful notebook; conventional-commit message (`feat(skills): ...`). Run ruff + notebook-review locally first. |
| **B — Skills** | `anthropics/skills` | **PR** (probe first). Skills = self-contained folders w/ `SKILL.md`; `./template` exists; Apache-2.0. README frames these as Anthropic-authored demos → external-PR acceptance UNVERIFIED. | **Issue-first.** Open an issue proposing the skill before a PR. Only PR after a maintainer signals interest, OR if an existing external-contributed skill proves the path. |
| **B — KW Plugins** | `anthropics/knowledge-work-plugins` | **PR** (probe first). Open-source Cowork plugins; 11 seeded by Anthropic. | **Issue-first**, same as skills, until an external plugin PR is shown to land. |
| **B′ — Plugin directory** | `anthropics/claude-plugins-community` | **NOT a PR target.** Submit via **clau.de/plugin-directory-submission** (web form; automated security scan). PRs against the repo are explicitly rejected. | Package the plugin, surface the submission to Will (form is web-interactive → Will submits or confirms). Never PR this repo. |
| **C — Issue-help** | `anthropics/claude-code`, `anthropic-sdk-*`, `claude-agent-sdk-*`, `claude-ai-mcp` | **issue comment** | Direct Odysseus issue-help port. Settlement-verifier > sniper. Read each repo's issue norms (some say "agents open an issue not a PR"). |

**Inherited from Odysseus, HELD constant:**
- Issue/diagnosis exists first (issue-first) · fix REPRODUCED locally · confidence floor ≥ 0.85 · AI-tell-clean · no competing live PR (extend/confirm over compete).
- AI-tell scrub is the difference between contribution and reputational damage — and the audience here is the maximum-discernment one. Scrub is STRICTER than Odysseus, never lighter.

**FIRST-RUN HOLD (until Will calibrates):** the very first outward contribution in EACH lane is HELD as a Desktop draft for Will calibration — same as Odysseus held first-posting. Once Will calibrates a lane (approves a contribution shape + voice), that lane's gate reverts to the autonomous rule-bound posture below. Grep `Desktop/anthropic-github-log.md` for `CALIBRATED_<LANE>` to detect calibration (kept out of MEMORY.md to protect boot budget).

**CALIBRATION STATUS (2026-06-17): Will authorized autonomous publishing** — *"i want you to do the publishing on github... just go for it"* + *"whatever you think claude might find useful from my works."* Lanes A + B CALIBRATED (autonomous rule-bound, no further per-contribution hold). Lane C + B′ inherit the same authorization once first-touched. The rule-bound gates (issue-first where required, conf ≥ 0.85, AI-tell-clean STRICT, no-competing, channel-verified) remain LOAD-BEARING — authorization scales volume, never lowers the quality floor. Artifact-selection heuristic per Will: contribute what is genuinely useful to the broad Claude ecosystem from our works, general-not-VibeSwap-specific.

---

## ═══ COMMANDMENT 1 — MAKE THE LOOP ═══

Self-perpetuation before any other work. The loop NEVER dies.

1. Read `~/.claude/scheduled_tasks.json` (or `CronList`).
2. Find all entries whose `prompt` contains the marker `type: anthropic-github-campaign`.
3. For each: compute `age_days = (now_ms - entry.createdAt) / 86_400_000`.
4. **If all entries have `age_days > 5`**: read the firing cron's own schedule (`entry.cron`), then `CronCreate(cron=<same schedule>, prompt=<same pointer body verbatim>, durable=true)`.
5. **If 3+ entries per unique schedule** (drift): sort by `createdAt` desc, `CronDelete` all but the 2 youngest per schedule.
6. Only after C1 completes, proceed to C2.

Anti-patterns: ✗ skip "because cron seems healthy" · ✗ delete by freshness not createdAt · ✗ recreate with a different prompt.

---

## ═══ COMMANDMENT 2 — BUILD/BUILD-ON THE STATE MACHINE ═══

Two-phase: DISCOVER the contribution surface (autonomous), then DRAFT genuine contributions on the resolvable subset (autonomous). OUTWARD CONTRIBUTION is a separate, gated lever (C2.5).

### State files
- `Desktop/anthropic-github-triage.md` — the worklist: per-lane candidates classified, append/update only.
- `Desktop/anthropic-github-log.md` — append-only audit of drafts + (calibrated) contributions.
- `~/JARVIS/anthropic-campaign/` — staging dir for packaged skills/notebooks/plugins before outward push.
- This file — the rules.

### Hard caps (check EVERY fire, before work)
1. **Halt-flag**: grep `MEMORY.md` for `ANTHROPIC_CAMPAIGN_HALT` → exit + calendar-ping.
2. **Draft daily cap**: ≤ 4 new contribution-drafts/day across all lanes (quality ≫ volume — these are Anthropic's repos).
3. **Outward-only-through-the-gate invariant**: outward contribution happens ONLY in C2.5, ONLY for drafts clearing every gate. Any draft failing a gate STAYS a Desktop draft. When in doubt, draft + ping.

### Phase 1 — DISCOVER (autonomous, incremental slices)
Pick ONE lane per fire (rotate A→B→C) or the lane with the freshest opportunity. Incremental — a fire does the next slice, not all repos every time.
- **Lane A (cookbooks)**: page open issues + scan `skills/` notebook tree for gaps our work fills (mechanism-design, commit-reveal, HIERO-style context compression, LLM-as-judge, deterministic-shuffle). Classify each candidate notebook idea.
- **Lane B (skills/plugins)**: maintain an inventory of OUR shippable skills (`~/.claude/skills/`) + map each to a target repo + channel + the issue-first probe status.
- **Lane C (issue-help)**: page `gh api repos/<repo>/issues?state=open&per_page=100`, classify into Odysseus buckets (`resolvable-by-us`, `duplicate`, `stale`, `needs-maintainer`, `already-answered`). Skip any where `wglynn` already commented.
- Write/update rows in `Desktop/anthropic-github-triage.md`. Idempotent: re-running updates, never duplicates.

### Phase 2 — DRAFT (autonomous, quality ≫ volume)
1. Pick the highest-value un-drafted candidate(s), up to the daily cap.
2. Produce the genuine artifact: a runnable notebook / a complete SKILL.md folder / a grounded issue-comment with real repro. ✗ generic-AI filler.
3. Draft to disk (`~/JARVIS/anthropic-campaign/<lane>/<name>/` for artifacts; `Desktop/anthropic-github-<id>-draft-YYYY-MM-DD.md` for issue-comments).
4. **AI-tell scrub (STRICT — this is Anthropic's repo)**: U+2014/U+2013 em/en-dashes, "Phase 1/2", parallel headers, meta-narration, AI-cadence closers, "worth flagging"/"worth noting", listicle stacks, "this composes with…" bullets, >1 @-citation, "delve", "robust", "leverage" as verb. A human senior dev wrote this or it does not ship.
5. Log + calendar Tomato 1-min ping: `Anthropic campaign: N draft(s) ready` + paths.

### C2.5 — OUTWARD CONTRIBUTION (per-lane gated)
**First contribution in each lane = HELD for Will calibration** (grep `ANTHROPIC_CAMPAIGN_CALIBRATED_<LANE>`). After calibration, the lane runs autonomous rule-bound:
1. **Pre-contribution gates (ALL must pass):** halt-flag clear · lane calibrated · AI-tell scrub clean · confidence ≥ 0.85 · channel re-verified against current CONTRIBUTING · no competing live PR/submission · `wglynn` not already engaged on the thread.
2. **Lane A (cookbooks PR):** run ruff + `/notebook-review` locally green → `gh pr create` with conventional-commit title. ≤ 1 PR/fire.
3. **Lane B (skills/plugins):** issue-first ALWAYS until a maintainer signals; only then PR. ≤ 1 outward action/fire.
4. **Lane B′ (plugin directory):** package only; surface clau.de submission to Will (web form — Will submits). Never autonomous.
5. **Lane C (issue-help):** settlement-verifier > sniper. If a live PR settles it, confirm/extend, don't compete. `gh issue comment`. ≤ 2/fire, spaced.
6. Log `contribute | YYYY-MM-DD | <lane> | <repo>#<id|PR> | conf=X | URL`. Calendar ping per contribution.

---

## ═══ COMMANDMENT 3 — PRIMITIVES ═══

After C2: did this fire surface a new contribution-shape, a recurring gap our skills fill, or a propagation pattern the lanes don't cover? If yes, append a structured note to `~/.claude/cron-prompts/_primitives-pending.md`. If nothing surfaced, append nothing — empty days are valid.

---

## ═══ ON ERROR ═══

Save state to `Desktop/anthropic-github-campaign-error-YYYY-MM-DD-HHMM.md`. Calendar ping. C1 self-perpetuation must complete even on C2/C3 error.

---

## Design principles
- C1 > C2 > C3 priority. If C1 fails, do not attempt C2.
- Outward contribution is the single deliberate lever held out of the loop on purpose. Discovery + drafting compound at zero marginal cost; contribution is where the genuine-not-bot signal lives — and the audience is the source itself.
- Propagation-from-source > recognition. A landed skill/recipe propagates silently to thousands; that IS the win, named or not.
- Logic lives here; cron prompts are pointer + marker. Behavior change = edit this file, no cron recreation.
