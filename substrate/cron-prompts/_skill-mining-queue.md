# SKILL MINING — actionable queue (Will-triage)

Entries appended by skill-mining sweeps (`skill-mining.md`). Promote → work only on Will's go.

## [2026-06-10 17:25 ET] — LLMLingua-2 lossy token-drop compression for prose-heavy boot/warm files
- Source: https://github.com/microsoft/LLMLingua (MIT; model microsoft/llmlingua-2-xlm-roberta-large-meetingbank; API compress_prompt(rate=0.33); v0.2.2 latest release -- fetch-verified)
- Technique: XLM-RoBERTa token classifier drops low-value tokens; `PromptCompressor(...).compress_prompt(text, rate=0.33)`; 2-5x compression typical in production, task-agnostic
- Port class: REINTERPRET — complements HIERO, doesn't replace it. HIERO = semantic density at write-time; LLMLingua-2 = mechanical token-drop at load-time for files HIERO doesn't govern (MEMORY_WARM_*.md prose, archived SESSION_STATE epochs, paper drafts fed as context)
- Our substrate state: L4 corpus-cache reports 9,293 tok across 9 boot files; warm files load on situation-match uncompressed
- Suggested action: zero-risk benchmark on scratch copies of 2-3 warm files — measure tok-reduction vs recall fidelity; CPU inference is batch-offline (cron), latency irrelevant
- Will-triage: pending

## [2026-06-10 17:25 ET] — Graphiti bi-temporal fact-invalidation pattern for memory staleness
- Source: https://github.com/getzep/graphiti (Apache-2.0, v0.29.2 June 2026, 27.3k stars at verify-time, fetched + verified)
- Technique: every fact carries a validity window; new contradicting info INVALIDATES (not deletes) old facts; queries answer "true now" vs "true at time T"; provenance links to source episodes
- Port class: full stack = DROP (needs Neo4j/FalkorDB + LLM-API ingestion — server infra we reject for local substrate). The bi-temporal PATTERN = REINTERPRET: `valid_from:` / `invalidated_by: <memory-slug>` frontmatter on memory primitives; staleness reminders become structural instead of age-heuristic
- Our substrate state: every memory Read injects "X days old, verify before asserting" age-warnings; Hindsight CLI has 80 contradiction candidates pending — fact-invalidation is exactly the resolution mechanic for that queue. CONVERGES with Rick TG #2858 bi-temporal-KG thread (Felix offered to help test 2026-06-09)
- Suggested action: pilot `invalidated_by` frontmatter on the 80 Hindsight contradiction pairs during their triage; mention Graphiti as prior art in the #2858 thread reply Will owes
- Will-triage: pending

## [2026-06-10 17:25 ET] — Letta "sleep-time compute" — background memory consolidation (convergent validation)
- Source: Letta (ex-MemGPT, 21.7k stars) via 2026 comparison roundups (search-level verification; fetch repo before acting)
- Technique: agent consolidates/merges/decays memories in background compute, not in-conversation; highest independent LoCoMo score (~83%) among open-source memory systems
- Port class: REINTERPRET — we already do this shape (cron-driven consolidation proposals, duplicate detector, dormancy review). Find = naming + validation + one gap: our consolidation surfaces PROPOSALS but nothing executes merge passes on a schedule
- Our substrate state: 6 consolidation proposals + 7 STRONG-sibling duplicate pairs sitting unmerged at `_system/`
- Suggested action: wire a weekly "sleep-time" cron that executes approved consolidation proposals (post-Will-approval), rather than letting proposal queues accumulate
- Will-triage: pending

## [2026-06-10 17:25 ET] — Claude Code ecosystem deep-dive deferred (raw-README fetch needed)
- Source: https://github.com/hesreallyhim/awesome-claude-code (46.1k stars) + https://github.com/disler/claude-code-hooks-mastery (3.3k stars)
- Technique: canonical curated list (hooks/skills/orchestrators, judgment-curated) + hooks-mastery reference (UV single-file hook scripts, meta-agent patterns)
- Port class: vein, not a single find. GitHub HTML fetch returned nav-only; need raw.githubusercontent.com README fetch
- Suggested action: next sweep (or this session if Will wants): fetch raw READMEs, mine for memory/token/session/frontend hooks we haven't independently built; expect high overlap with our stack — the delta is the value
- Will-triage: pending

## [2026-06-10 17:25 ET] — FRONTEND: Tailwind dynamic-class purge footgun + cn-helper convention
- Source: 2026 React/Tailwind best-practice roundups (search-level; low-risk convention, no fetch needed)
- Technique: `'bg-' + color + '-500'` template-string classes are invisible to Tailwind's scanner → purged in production builds. Convention: always complete literal class strings; conditional composition via `cn` helper (clsx + tailwind-merge)
- Port class: DIRECT-PORT — coding convention for `vibeswap/frontend`
- Our substrate state: vibeswap/CLAUDE.md locks palette/tokens but has no dynamic-class rule; unaudited risk in existing components
- Suggested action: grep frontend/src for template-string class construction; add the rule to the LOCKED aesthetic block
- Will-triage: pending

## [2026-06-10 17:25 ET] — FRONTEND: framer-motion is now "Motion" (package consolidation) + Vite 8 / Tailwind v4 upgrade horizon
- Source: 2026 animation-library + stack roundups (search-level; fetch changelogs before acting)
- Technique: framer-motion rebranded/merged → `motion` (Motion One merged in, ~6M weekly downloads, still the React default); Vite at v8.0.16 (fetch-verified releases page 2026-06-10; we run 5); Tailwind v4 (Jan 2025) drops tailwind.config.js for `@tailwindcss/vite` plugin; React Transition Group unmaintained (we don't use it)
- Port class: REINTERPRET — staged upgrade path, not urgent. Aesthetic is locked; libraries beneath it can move
- Our substrate state: frontend on React 18 + Vite 5 + framer-motion; deployed on Vercel; no CI on frontend
- Suggested action: low-priority upgrade spike branch (motion rename first — mechanical; Vite 5→8 + Tailwind v4 together — needs the /ship-web checklist after)
- Will-triage: pending
## [2026-06-10 17:55 ET] — Will-fed absorb: "Designing loops with Fable 5" + loop-engineering taxonomy threads
- Source: 3 threads Will-pasted (Anthropic-staff Fable-5 loops thread; "beautiful broken refactor" meme; "Loops: What Every AI Engineer Needs to Know in 2026")
- Technique: verifier-subagent in independent context > same-context self-critique; memory progression fail→investigate→verify→distill→consult; closed-loop default w/ 5-part checklist (goal/context/action/feedback/stop-condition); structural-bets only WITH verification loop
- Port class: absorbed → memory primitive `feedback_design-loops-not-prompts.md` (shipped). Two follow-on actions remain:
  1. /critical-qa upgrade: route grading through a verifier subagent (independent context) instead of same-context hostile Q&A
  2. Loop-audit: run the 5-part checklist over all active loops (odysseus, skill-mining, autonomous-continue, WORK chain) — verify each has explicit goal + feedback + stop-condition
- Our substrate state: RSAW already does maker≠checker; "surfaced xN, unactioned" anticipation telemetry = measurable consult-step failure
- Will-triage: pending

## [2026-06-10 18:20 ET] — Will-fed: NousResearch hermes-agent — FTS5 recall + skill-creation loop + provider-agnostic gateway
- Source: https://github.com/NousResearch/hermes-agent (MIT, fetch-verified README 2026-06-10)
- Technique(s), port-classified:
  - **FTS5 session search + LLM summarization for cross-session recall** -> REINTERPRET, strong: SQLite FTS5 keyword search over session transcripts as the sparse half of hybrid retrieval; our deep-recall.py is dense-embedding only. Local, zero infra, stdlib sqlite3.
  - **Autonomous skill creation post-task** (closed learning loop) -> REINTERPRET: we extract memory primitives (R2) but not runnable skills; candidate: post-task pass that promotes repeated procedures to SKILL.md files. Compatible with open agentskills.io standard (interop note).
  - **Provider-agnostic model switch** (`hermes model`, 200+ models via OpenRouter etc., no code change) -> reference implementation for the replace-the-model-tomorrow sovereignty test + the model-tier auto-assign coordination mechanism.
  - **Multi-platform gateway** (one agent: TG/Discord/Slack/Signal/CLI) -> REINTERPRET reference for jarvis-bot TG growth path.
  - **Serverless hibernating sandboxes** (Modal/Daytona) -> DROP for local-first substrate; note for Fly.io app if scale ever demands.
  - **Agent-curated memory w/ periodic nudges** -> CONVERGENT-VALIDATION of our anticipation-hook + deep-recall nudge stack.
- Our substrate state: dense-only recall; primitives-not-skills extraction; TG bot single-platform; model = Claude-weights (sovereignty partial)
- Suggested action: (1) zero-risk spike: FTS5 index over session jsonl transcripts on a scratch DB, measure recall delta vs deep-recall.py alone; (2) read their skills+memory modules before any deeper port
- Will-triage: pending

## [2026-06-10 18:40 ET] — ADOPTED: two frontend skills installed (Will-directed "add this")
- Source: https://github.com/Trystan-SA/claude-design-system-prompt (MIT) + https://github.com/zarazhangrui/frontend-slides (MIT) — both fetch-verified READMEs, shallow-cloned
- Technique: (1) design-system = 20-chapter design doctrine + 14 phase-skills (production/system/review), 8 quality dimensions incl. anti-AI-trope aesthetics + WCAG + token-thinking; (2) frontend-slides = HTML presentation skill w/ progressive-disclosure file loading (map-first SKILL.md), 34 templates + 12 presets, PPT conversion
- Port class: DIRECT-PORT (installed live): ~/.claude/skills/design-system/ (wrapper SKILL.md authored — precedence rule: vibeswap LOCKED aesthetic overrides) + ~/.claude/skills/frontend-slides/ (native skill, registered)
- Our substrate state: vibeswap locked aesthetic existed; no general design-discipline skill, no deck-generation skill (decks were hand-built; /ship-web covers verification only)
- Note: frontend-slides' progressive-disclosure structure (map first, reveal per-phase) = pattern worth copying for our own larger skills
- Will-triage: installed; deeper vendoring into jarvis-substrate repo = Will's call (repo-bloat tradeoff)

## [2026-06-10 19:05 ET] — REFERENCE-ADOPTED: ui-agents prompt collection + frontend-design-toolkit catalog (Will-fed)
- Source: https://github.com/mustafakendiguzel/claude-code-ui-agents (MIT; categorized UI/UX prompt collection, paste-to-use format) + https://github.com/wilwaldon/Claude-Code-Frontend-Design-Toolkit (MIT; 70+ tool catalog across skills/MCP/config — recommends anthropic/frontend-design plugin as essential)
- Port class: REFERENCE — not installed wholesale (prompt collections, not native skills); mine per-need during frontend work. Toolkit's top recommendation (official frontend-design plugin) noted for Will-triage.
- Suggested action: during the vibeswap frontend reimagine pass, pull specific ui-agents prompts (components/animations/accessibility categories) as needed; consider `claude plugin add anthropic/frontend-design` (official, ~100 tok at boot)
- Will-triage: pending (plugin install decision)

## [2026-06-10 19:05 ET] — ADOPTED: token-spend audit toolkit (cprkrn gist, Will-fed "should we add this?")
- Source: https://gist.github.com/cprkrn/d3f128a8e8e3ddfa4b38934edff34d42 (fetch-verified; ~400 LOC, 3 scripts)
- Technique: (1) analyze_claude_usage.py — transcript burn-rate audit (author's finding: 96% of spend = re-reading history; 4 immortal chats = 71% of cost); (2) statusline context meter w/ color thresholds; (3) context-rotation-hook — auto-prompts state-handoff at 200k tokens
- Port class: (1) DIRECT-PORT installed at ~/.claude/tools/token-audit/ (read-only, zero-risk); (2) MERGE candidate into existing statusline-command.sh; (3) STRUCTURAL WIN pending triage — promotes our memory-level 50pct-reboot rule to hook-level per [P·always-equals-gate]; threshold should be OUR ~50% not their 200k
- Our substrate state: 50pct-reboot lives in memory only (un-hooked); REBOOT protocol manual; no transcript cost analyzer
- Will-triage: pending (rotation-hook registration = settings.json change)
