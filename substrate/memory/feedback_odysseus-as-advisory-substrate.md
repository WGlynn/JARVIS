---
name: OdysseusAsAdvisorySubstrate
description: "∀ Odysseus thread ⇒ READ for technical advice senior devs give pewdiepie (recognized non-dev). Same advice often applies to VibeSwap/JARVIS substrate (recognized non-dev-built-with-AI). Two-axis filter: (a) directly-applies-to-our-substrate ⇒ queue for action, (b) generic-pattern-worth-remembering ⇒ feedback primitive. Mission isn't only outgoing dispatch; siphon the collective wisdom into our own codebase. Will 2026-06-09."
type: feedback
originSessionId: fa79e2f6-c3ad-4437-b4a7-ff92f216988e
---
**[F·odysseus-as-advisory-substrate]**

## ⚙ Rule

The Odysseus repo is being audited in public by senior contributors who recognize the AI-cosplay pattern in pewdiepie's code. We share that pattern: VibeSwap and JARVIS are also "non-dev-built-with-heavy-AI-assistance." Advice given to Odysseus is therefore advice given to us, for free, by people we don't pay.

∀ Odysseus discovery / discussion / PR sweep ⇒ collect substantive technical advice ⇒ classify against our substrate ⇒ either queue-for-action or save-as-pattern.

**Will:** *"we're syphoning the collective wisdom of pewdiepies repo to fix our own."*

## Why

The dispatch-only frame ("post substantive replies, build reputation") was correct but undercounted Odysseus's value. The repo is also a free advisory channel for our own codebase. Every senior contributor commenting on Odysseus is implicitly reviewing the AI-generated patterns we ALSO produce.

The example that surfaced this: a comment (id `58plmahm02xg1`, author not captured in Will's paste — to be verified) said *"first order of business would be migrating this to a proper framework, like Next.js or Nuxt... I am pretty sure the AI when writing langIcons.js was cosplaying Odysseus."* @georgebrianb replied "I agree, happy to contribute — CI/CD, previews, autodeploys, LLM-security-checks; would be my first OSS contribution." That's a frame Will recognized — the same AI-cosplay file-shape probably exists in VibeSwap-frontend or JARVIS scripts.

## How to apply

### In the cron loops (odysseus-discovery + odysseus-daily-cadence):

New step between C2 (dispatch) and C3 (primitives):

**COMMANDMENT 2.5 — ADVICE MINING (parallel track)**

1. For each thread surfaced (whether dispatched-on or not) AND for the most-recently-active 10 threads at sweep time:
   - Read the top-3 highest-signal comments (longest, most reactions, or from a recognized senior dev)
2. Classify each piece of advice:
   - **(a) directly-applies-to-vibeswap-frontend** (React+Vite+Tailwind) — append to `_advice-actionable-vibeswap.md`
   - **(b) directly-applies-to-jarvis-os** (Python hooks + memory + cron) — append to `_advice-actionable-jarvis.md`
   - **(c) generic-good-design-no-action** — note in advice-log, no queue entry
   - **(d) odysseus-specific-no-action** — skip
3. Append to `~/.claude/cron-prompts/_advice-actionable-{target}.md` with: thread #, comment URL, paraphrase, our-substrate-assessment, suggested-action.
4. Will reviews periodically; (a)/(b) entries can be promoted into actual codebase work.

### One-off audit posture

When mining advice, treat *form* of advice as primary signal, not just content:
- "X is AI-cosplay" → look for our equivalent
- "you should theme through ONE file" → check our component sprawl
- "missing CI/CD / autodeploys" → check our pipeline
- "no security checks" → check ours

## 🪝 Triggers

- ∀ odysseus-discovery cron fire ⇒ run C2.5 advice-mining sweep
- ∀ odysseus-daily-cadence cron fire ⇒ run C2.5 against today's engagement-state threads
- ∀ ad-hoc Odysseus thread read ⇒ apply 2-axis classifier

## ✗ Anti-patterns

- ✗ apply Vue/Nuxt advice to React+Vite codebase verbatim — same SHAPE of advice, different stack
- ✗ queue advice as actionable when the substrate truly diverges
- ✗ skip mining because dispatch didn't happen this loop — mining is independent of dispatch
- ✗ act on advice without Will-triage — queue first

## ✓ Disposition

- This rule ⇒ active immediately ∀ Odysseus cron loops
- Composes upward into [P·structure-does-the-work] (Odysseus IS the structure doing the work of auditing us)
- Pairs with [F·odysseus-daily-discussion-campaign] (dispatch frame) — together = full bidirectional flow

## 🔗 Composes-with

- [F·odysseus-daily-discussion-campaign] — outgoing dispatch; this is the incoming-advice complement
- [P·structure-does-the-work] — Odysseus's audit-by-senior-devs is structure we don't have to build
- [P·repo-as-aspirational-spec] — same shape: our repo as wishlist; advice patches the wishlist
- [P·jarvis-amd-applied-to-ai-substrate] — siphoning is a substrate-port move

## 📦 Receipts

- 2026-06-09 13:38 ET — Will pasted @bemarodriguez comment on #2999 saying "AI was cosplaying Odysseus when it wrote langIcons.js" + @georgebrianb offering CI/CD/autodeploys + LLM-security-check help as their first OSS contribution. Will framed: *"I figured since im equally not a real dev, we could add active reading of everything to the chron and you can identify advice that would also improve / fix our repo and codebase and then act on it. we're syphoning the collective wisdom of pewdiepies repo to fix our own."*
- Primitive saved same turn; canonical odysseus-discovery.md updated to add COMMANDMENT 2.5.
