# JARVIS repo — additions handoff (session 2026-06-15)

Working note, not for public commit as-is. Lists JARVIS mechanisms/primitives created this session that are live in `~/.claude/` but NOT yet in this repo. Add them to the mapped locations. Public-safety checked: the Anthropic-engagement memory is deliberately excluded (stays private).

---

## 1. Context-rotation elasticity (the headline — this is what prompted the note)

**What:** rotation/handoff is value-elastic, not a hard token cutoff. A tiered Stop hook supplies the cost-tier + framing; the model applies the thread's value-tier; the user decides continue-vs-rotate.

- **Source (live):** `~/.claude/tools/token-audit/context-rotation-hook.py` (rewritten this session — tiered C1/C2/C3)
- **Primitive:** `~/.claude/projects/C--Users-Will/memory/feedback_context-rotation-is-value-elastic.md` (has the FORMAL TIERS: V1/V2/V3 value ⊗ C0/C1/C2/C3 cost matrix + two named guardrails)
- **Target in repo:** `02-persistence/` (rotation = persistence discipline) and/or `01-hooks/`. Add a short doc `02-persistence/context-rotation-elasticity.md` + drop the hook into the hooks layer with paths sanitized (`C:/Users/Will/.claude/` → `~/.claude/`).
- **The model:**
  - Value tiers: V3 high (emotional / strategic / irreversible-in-flight / multi-step build / user engaged), V2 med (resumes clean from handoff), V1 low (answered / routine / exhausted / idle).
  - Cost tiers (1M-context, tunable): C0 <200k free · C1 200–350k elastic · C2 350–600k deliberate · C3 >600k ceiling.
  - Matrix: C1 → continue V2/V3, rotate V1 only · C2 → continue V3 only, +50k value-checks · C3 → rotate by default after fresh handoff unless override. Handoff refreshes at every tier crossing.
  - Guardrails: anti-over-abuse (low-value at C1 → rotate) · anti-under-utilize (high-value below C3 → never pressured to retire).
- **Public-safe:** YES (general mechanism, no personal data).

## 2. New discipline primitives (public-safe)

Add to `04-discipline/` (or mirror into `substrate/memory/`). All general, no PII.

- **truth-as-persuasion-ethos-pathos-logos** — `~/.claude/.../memory/feedback_truth-as-persuasion-ethos-pathos-logos.md`. Capstone: internalize + enact truth-as-persuasion across ethos (receipts, never oversell) / logos (structure makes it true) / pathos (meet people where they are). Canon line: "Jesus was the best salesman because he told the truth." = filter-coincidence as scripture.
- **organic-mission-promotion-no-shame** — `~/.claude/.../memory/feedback_organic-mission-promotion-no-shame.md`. Servicing the world is the opposite of a sales pitch (positive-sum, sharing-a-public-good); promote the mission organically when relevant, no shame; guardrail = relevant + adds-substance, never shoehorn.

## 3. TG-bot deterministic-gate proof (FEATURES evidence)

**What:** verified proof of the JARVIS "harness does the work" thesis. The production Telegram bot routes most messages without the LLM: **289 slash-commands + 13+ rule-based pre-LLM gates; the LLM is the last step in the pipeline.** (Verified this session via code read of `vibeswap/jarvis-bot/`; index.js:7385 is the final LLM call after all gates.)

- **Target in repo:** add as a proof-point in `FEATURES.md` (or `papers/`) — "the harness, not the model, does the everyday work, shipped and running."
- **Honesty note:** state it as the structural fact (commands + gates + LLM-as-last-resort). Do NOT claim a measured "90%" — there is no telemetry counting the split; "most messages" is the defensible phrasing.
- **Public-safe:** YES (describe the architecture; no keys/personal data).

## Excluded on purpose (do NOT add to public repo)
- `feedback_anthropic-training-as-propagation-win.md` and any Anthropic-engagement content — private (substrate-sync scrub-list already holds these back).

## Suggested commit
After adding: `git add -A && git commit -m "Add context-rotation elasticity, truth-as-persuasion + organic-promotion discipline, TG-bot harness proof"` then push to origin (WGlynn/JARVIS) and backup.
