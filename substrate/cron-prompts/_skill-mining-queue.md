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

## [2026-06-11 13:53 ET] — claude-memory-compiler: PreCompact safety-net hook + nightly compile trigger + memory-corpus lint
- Source: https://github.com/coleam00/claude-memory-compiler (raw README fetch-verified 2026-06-11; Cole Medin, Apr 2026, Karpathy-LLM-KB lineage)
- Technique: dual-hook capture — SessionEnd PLUS **PreCompact** ("safety net": long sessions auto-compact multiple times before SessionEnd fires; without PreCompact, mid-session context is lost to summarization before extraction ever runs). flush.py extracts via Agent SDK → daily/YYYY-MM-DD.md → compile.py auto-triggers after 6PM-local if today's log changed (no cron needed). Retrieval = index-first, no RAG: "at personal scale (50-500 articles) the LLM reading a structured index.md outperforms vector similarity"; RAG needed ~2,000+ articles. lint.py = 7 health checks on the knowledge corpus (`--structural-only` skips paid checks).
- Port class: REINTERPRET, three separable deltas vs our stack: (1) **PreCompact coverage** — audit whether our R2 memory-extraction path fires on PreCompact; if only SessionEnd/manual, mid-session compactions silently eat extractable context — exactly the failure class this hook closes; (2) **memory-corpus lint** — we have duplicate-detector + contradiction candidates but no unified N-check structural linter over memory/; (3) "compile-if-changed after 6PM" = cron-free trigger pattern (we already run real crons — note only)
- Our substrate state: memory-preprocessor SessionStart injection = their index-inject, already convergent; R2 extraction exists; index-first-over-RAG validates our no-vector-DB memory architecture from an independent implementation
- Suggested action: (zero-risk) grep ~/.claude/settings.json + hooks/ for PreCompact registration, report gap; (Will-triage) if gap real, register PreCompact → extraction hook per [P·always-equals-gate]
- Verifier (self, rubric 4-pt): 1 PASS (raw README fetched) | 2 PASS ("237 stars day one" claim from search EXCLUDED as unverified) | 3 PASS (REINTERPRET defensible — we own most of the shape; deltas named) | 4 PASS (audit=zero-risk, hook-registration=triage). VERDICT: PASS
- Will-triage: pending

## [2026-06-11 13:53 ET] — llm-knowledge-base (Karpathy-arch original): /kb-merge consolidation mechanic + read-before-write concept dedup
- Source: https://louiswang524.github.io/blog/llm-knowledge-base/ (blog fetch-verified 2026-06-11) → repo https://github.com/louiswang524/llm-knowledge-base (NOT separately fetched — blog-level verification)
- Technique: (1) read-before-write merge — compiling a new source about existing concept X reads wiki/concepts/X.md and UPDATES it, never duplicates ("the wiki converges — it doesn't fragment"); (2) **/kb-merge** — consolidates near-duplicate concepts: synthesize both articles → rewrite backlinks vault-wide → archive absorbed article WITH redirect note; (3) index-first Q&A + kb_search.py fallback (TF-IDF keyword + sentence-transformers semantic, cached in .kb/search_index.json). Author's honest limits: no staleness detection, index strains as it grows
- Port class: REINTERPRET — /kb-merge is the executable merge procedure our consolidation queue lacks: we have 6 consolidation proposals + 7 STRONG-sibling duplicate pairs sitting unmerged (the Letta sleep-time entry flagged the same gap from the scheduling side; this supplies the per-merge algorithm: synthesize → re-link → archive-with-redirect). Archive-with-redirect also rhymes with the queued Graphiti `invalidated_by` mechanic — invalidate, don't delete
- Our substrate state: duplicate-detector emits pairs but no merge executor; memory links are slug-references (= their backlinks); MEMORY_INDEX_* = their index.md
- Suggested action: when the consolidation-proposal triage runs, use the 3-step /kb-merge procedure as the merge spec; fetch their skill files first for the exact prompt shape (1 fetch, next sweep or on-demand)
- Verifier (self, rubric 4-pt): 1 PASS-with-note (blog fetched; repo internals not — marked) | 2 PASS (no perf numbers claimed) | 3 PASS (REINTERPRET: their Obsidian/raw-source pipeline ≠ our substrate, the merge mechanic ports) | 4 PASS (action concrete, correctly deferred to existing triage). VERDICT: PASS
- Will-triage: pending

## [2026-06-11 13:53 ET] — T2-RAGBench evidence: BM25 beats SOTA dense on entity/numeric-heavy corpora → design input for the FTS5 hybrid spike
- Source: https://arxiv.org/abs/2604.01733 (abstract fetch-verified 2026-06-11; 23,088 queries / 7,318 mixed text+table financial docs)
- Technique/evidence: two-stage hybrid retrieval + neural reranking = Recall@5 0.816, MRR@3 0.605, beats all single-stage; **BM25 outperforms state-of-the-art dense retrieval** on this corpus; HyDE/multi-query expansion "limited benefit for precise numerical queries". Fusion-tuning details circulating with this paper (RRF k=10 > k=60; convex α=0.5 > RRF) are SEARCH-LEVEL — not in the abstract, full-paper check before citing
- Port class: REINTERPRET (evidence, not code) — our memory corpus is slug/primitive-ID/exact-term shaped, i.e. the query class where BM25 wins. Strengthens the already-queued hermes FTS5 hybrid-recall spike from "worth trying" to "evidence-backed"; also: skip HyDE-style query expansion for deep-recall.py, evidence says low ROI for precise queries
- Our substrate state: deep-recall.py = dense-only; FTS5 spike queued 2026-06-10 with no eval design yet
- Suggested action: fold into the FTS5 spike spec — eval = held-out query set from real recall misses, compare dense vs FTS5-only vs hybrid; start rank-fusion simple (RRF), tune only if the held-out set says so
- Verifier (self, rubric 4-pt): 1 PASS (abstract fetched; ablation numbers explicitly downgraded to search-level) | 2 PASS (typical-case benchmark numbers, limitations quoted) | 3 PASS | 4 PASS (zero-risk: it's eval design for an already-queued spike). VERDICT: PASS
- Will-triage: pending

## [2026-06-11 13:53 ET] — awesome-harness-engineering: ~450-entry curated harness list — standing reference vein + 3 flagged tools
- Source: https://github.com/ai-boost/awesome-harness-engineering (raw README fetch-verified 2026-06-11)
- Technique: curated list spanning memory/state, context delivery+compaction, evals, observability, permissions. Flagged for us: **headroom** (compress tool outputs/logs BEFORE context entry; "60-95%" = marketing-level, unverified), **context-mode** (sandbox bulky data outside LLM, retrieve fragments via BM25 — same shape as our corpus-cache idea), **MemPalace** ("96.6% R@5 LongMemEval, zero LLM calls" — unverified, but zero-LLM-call local-first matches our substrate constraints). Also catalogs Anthropic auto-mode two-stage permission classifier + Agent SDK 5-layer permission order as design references
- Port class: list = REFERENCE-ADOPT (standing vein, like awesome-claude-code); the 3 flagged tools = each needs own fetch-verify before any port call — NOT queued individually to keep numbers honest
- Our substrate state: tool-output compression gap is real (large Bash/WebFetch outputs enter context raw); BPE corpus cache covers boot files only
- Suggested action: next sweep budget-permitting, fetch headroom + MemPalace READMEs and port-classify properly; add this list to the vein-4/6 rotation as a source
- Verifier (self, rubric 4-pt): 1 PASS (list README fetched; per-tool claims explicitly marked unverified) | 2 PASS (marketing numbers flagged as such) | 3 PASS (REFERENCE not DIRECT-PORT — defensible) | 4 PASS (next-sweep fetch action, zero-risk). VERDICT: PASS
- Will-triage: pending

## [2026-06-11 13:53 ET] — VEIN-4 CLEANUP RESOLVED: awesome-claude-code README is mid-restructure; THE_RESOURCES_TABLE.csv is the minable surface
- Source: https://raw.githubusercontent.com/hesreallyhim/awesome-claude-code/main/README.md (fetched: literally a TODO page, "new organizational system being prepared") + https://raw.githubusercontent.com/hesreallyhim/awesome-claude-code/main/THE_RESOURCES_TABLE.csv (fetched: alive, full resource table)
- Technique: 2026-06-10 deferred fetch closed. CSV standouts vs our stack: **recall** (zippoxer — FTS search over CC sessions + resume; converges with hermes FTS5 + our spike), **claude-code-tools** (pchalasani — anti-compaction session-continuity skills; same problem-class as PreCompact find above), **agnix** (linter for agent config files — rhymes with memory-lint), **parry** (prompt-injection scanner for hooks — security gap we haven't covered), **Dippy** (AST-based auto-approve for safe bash — alternative to our allowlist approach), plus claude-session-restore, cchistory, Claudex, claude-devtools, cc-sessions, cchooks, claude-hooks (TS), Context Engineering Kit, Context Priming, TDD Guard
- Port class: vein-map, not a single find. Three convergence clusters: session-FTS-recall (3rd independent sighting), anti-compaction (2nd), agent-file linting (2nd). Convergence count = prioritization signal
- Suggested action: queue-rule for future sweeps: mine the CSV not the README until restructure lands; parry (hook injection-scan) = the one genuinely novel capability — candidate for a dedicated fetch next sweep
- Verifier (self, rubric 4-pt): 1 PASS (both URLs fetched, dry README honestly reported) | 2 PASS (no numbers claimed) | 3 PASS (vein-map class honest) | 4 PASS. VERDICT: PASS
- Will-triage: pending

## [2026-06-12 11:54 ET] — parry-guard non-ML layers → pure-Python PostToolUse output scanner (tool-output injection/secret gap) [FETCH-VERIFIED]
- Source: https://github.com/vaporif/parry-guard (Rust, 95.6%). WebFetch this sweep confirmed verbatim: "these detection mechanisms are separable from ML models" + the non-ML layers "run before ML classification in the detection pipeline."
- Technique: PreToolUse/PostToolUse/UserPromptSubmit hooks. PostToolUse scans TOOL OUTPUT for injection+secrets, auto-taints project on hit. UserPromptSubmit audits .claude/ for dangerous perms + injected hook commands. Separable non-ML layers: unicode-invisible/PUA/homoglyph/RTL; Aho-Corasick known-injection-phrases; 40+ credential regexes (AWS/GitHub/cloud/DB-URI/keys); tree-sitter bash-exfil AST (base64/hex/ROT13/network-sink). Fail-closed.
- Port class: REINTERPRET — re-implement the PATTERN CONCEPTS in Python, NOT extract Rust. DROP the ML half (DeBERTa/Llama via ONNX/Candle, HF-gated models, Rust binary) = local-transformer infra we reject for a hook. The 3 light layers (invisible-unicode + injection-phrase Aho-Corasick + secret-regex) are trivially portable; the tree-sitter bash-AST layer is the heavier one.
- Our substrate state: fail-closed privacy leak-gate + NDA gate + NoCredsInChat all govern what WE EMIT. We do NOT scan INCOMING tool output for injection/secrets — real gap, cf. anthropics/claude-code#22915 ("prompt injection appended to every Read tool output").
- Suggested action: zero-risk local experiment — prototype tool-output-scan.py (PostToolUse) with the 3 light layers on a SCRATCH copy; benchmark false-positive rate on our own recent tool outputs before any live wire. Will-triage to go live.
- Verifier (sonnet subagent): REVISE → applied (tagged FETCH-VERIFIED, added separability quote, softened port to concept-reimpl).
- Will-triage: pending

## [2026-06-12 11:54 ET] — session-FTS recall: 3rd–4th convergence sighting [SEARCH-VERIFIED]
- Source: https://github.com/zippoxer/recall (Rust TUI) + samzong/Recall (hybrid FTS+semantic) + arjunkmrm/recall (SQLite FTS5 skill). SEARCH-level only — repos NOT WebFetched this sweep; treat detail as snippet-inference.
- Technique: full-text index over raw session JSONL; exact-string search + resume; agent-callable, no MCP.
- Port class: REINTERPRET (low priority). We have semantic deep-recall + BPE cache; gap = EXACT-string recall over session transcripts. SQLite FTS5 over JSONL = liftable shape (arjunkmrm proves FTS5-as-skill).
- Our substrate state: deep-recall = semantic embeddings; session-chain = 23k blocks; NO exact-string FTS over transcripts.
- Suggested action: convergence = real capability class (now 3rd–4th sighting incl. prior hermes FTS5). Source-fetch zippoxer/arjunkmrm next sweep, then evaluate a sqlite FTS5 index over session JSONL as exact-match complement to deep-recall. Will-triage.
- Verifier (sonnet subagent): REVISE → applied (tagged SEARCH-VERIFIED, lowered confidence).
- Will-triage: pending

## [2026-06-18 13:02 CT] — headroom: deterministic tool-output compressors (JSON/AST) as a PostToolUse layer [FETCH-VERIFIED]
- Source: https://github.com/chopratejas/headroom (Apache-2.0). Raw README fetch-verified 2026-06-18. (Flagged for fetch by the 2026-06-11 awesome-harness-engineering entry — that next-action is now closed.)
- Technique: content-type routing. **SmartCrusher** = deterministic JSON collapse (arrays-of-dicts / nested / mixed); **CodeCompressor** = deterministic AST-aware (Py/JS/Go/Rust/Java/C++); **Kompress-base** = HuggingFace ML model for prose; image = ML router. CacheAligner stabilizes prefixes for provider KV-cache hits. **CCR (Compress-Cache-Retrieve)** store is reversible — exposes a `headroom_retrieve` tool/MCP so the model fetches the full original on demand. Invocation: library `compress()`, proxy (`headroom proxy`), MCP server, or CLI `headroom wrap claude|codex|cursor|aider|copilot`. Python 3.10+, granular extras (`[code]`,`[ml]`,`[mcp]`,`[proxy]`...).
- Honest numbers (per-task README benchmarks, NOT a flat headline): code-search 17,765→1,408 tok (92%); SRE-debug 65,694→5,118 (92%); GH-issue-triage 54,174→14,761 (73%); codebase-explore 78,502→41,254 (47%). Accuracy parity (GSM8K/SQuAD2/BFCL) shown at "19–32% compression". The marketed "60-95%" is a RANGE across tasks, not a guaranteed rate.
- Port class: REINTERPRET — port the DETERMINISTIC half (SmartCrusher JSON-collapse + CodeCompressor AST concepts) as a PostToolUse tool-output compressor in pure Python; DROP the ML half (Kompress-base HF model + ONNX-from-cdn + image router = local-transformer infra we reject for a hook). Reversible-CCR + `headroom_retrieve` shape is worth copying conceptually (compress-with-escape-hatch).
- Our substrate state: large Bash/WebFetch tool outputs enter context raw; BPE corpus cache covers boot files only; no incoming-tool-output compression. **GATED on Entry below** — the harness may already drop oversized tool outputs to disk natively; measure that before building anything.
- Suggested action: (after the native-harness audit below) zero-risk prototype of a JSON/code tool-output collapser on a SCRATCH copy of recent large tool outputs; measure tok-reduction + reversibility. Will-triage before any live wire.
- Verifier (sonnet subagent): PASS (numbers honest, range unpacked, ML/deterministic split maps to our infra-reject constraint, action correctly gated + zero-risk).
- Will-triage: pending

## [2026-06-18 13:02 CT] — MemPalace: independent convergent-validation of index-first-over-RAG (+ verbatim-vs-HIERO design tension) [FETCH-VERIFIED]
- Source: https://github.com/MemPalace/mempalace (MIT). Raw README fetch-verified 2026-06-18 (impostor .net/.tech/.com domains avoided per the repo's OWN security note — only the GitHub repo is canonical).
- Technique: stores conversation VERBATIM (no summarize/extract), retrieves via semantic search over a pluggable backend (default ChromaDB; `backends/base.py` allows SQLite/Qdrant/pgvector). Structured index = **wings** (people/projects) / **rooms** (topics) / **drawers** (verbatim content) for scoped search. Deps: ChromaDB + NumPy + gRPCio + local embedding model ~300MB (embedding-gemma-300m or all-MiniLM-L6-v2 ~30MB).
- Honest numbers: raw mode **96.6% R@5 LongMemEval (500q) with ZERO API/LLM** (README confirms "no API key, no cloud, no LLM at any stage"); hybrid-v4 98.4% (held-out 450q); +LLM-rerank ≥99%. Repo's OWN BENCHMARKS.md flags the last 0.6% as "teaching to the test". ⚠ The "170 tokens at startup" figure circulating in search results is UNVERIFIED — the README fetch did NOT confirm any startup token cost; **do not cite it**. ⚠ Whether room/topic classification is regex/heuristic vs LLM is NOT disclosed in the README — UNVERIFIED (search claimed regex/keyword; could not confirm).
- Port class: mostly CONVERGENT-VALIDATION of our index-first-over-RAG architecture from an independent implementation (their claim: "structure alone = +34% accuracy"). Full stack = DROP (ChromaDB vector-DB dependency = infra we reject). The wings/rooms/drawers scoped-search shape is a *conditional* REINTERPRET onto our warm-map situation routing — **conditional because if room/topic classification turns out to be LLM-backed, it's DROP not REINTERPRET (an API dependency at classify-time)**; resolve the classification mechanism before treating it as portable. DESIGN-TENSION worth holding: their verbatim-no-summarize stance is the OPPOSITE of our write-time HIERO compression — a real counter-argument, not to resolve here.
- Our substrate state: deep-recall.py dense + BPE cache + MEMORY_INDEX_* (= their index) + warm-map sharding (= wings/rooms via [P·cell-knowledge-architecture]); HIERO compresses at write-time.
- Suggested action: no port. Logged as convergent validation; hold the verbatim-vs-HIERO tension as an open design question for Will. Zero action.
- Verifier (sonnet subagent): REVISE → applied (170-tok figure demoted to do-not-cite; port-class made conditional on classification mechanism per LLM-at-classify-time = DROP).
- Will-triage: pending (design-tension only)

## [2026-06-18 13:02 CT] — Claude Code NATIVE context management: may already cover the tool-output-bloat gap headroom targets [SEARCH-LEVEL; params unverified]
- Source: Anthropic platform docs + cookbook (compaction beta, context-editing, memory tool) = search-verified, docs pages NOT individually fetched. ⚠ The two harness-level mechanism SPECIFICS below come from THIRD-PARTY blogs (finisky.github.io, codex.danielvaughan.com), NOT Anthropic docs — treat all parameters (~50K char, ~2KB preview, Edit-only forked agent) as SEARCH-CLAIMED, UNVERIFIED; the audit step confirms or refutes them.
- Technique trio (first-party API, search-verified): (a) server-side **Compaction** (beta header `compact-2026-01-12`; auto-triggers at a token threshold, min 50K; emits a typed compaction block, drops prior blocks); (b) **Context-editing / tool-result clearing**; (c) **Memory tool** (cross-session persistence). PLUS two harness-level mechanisms reported by third-party analysis (UNVERIFIED params): (1) **tool-output-to-disk** — a tool result exceeding ~50K chars allegedly written to a file with only a ~2KB preview kept in context; (2) **Session Memory** — a forked background agent (shares prompt-cache prefix, restricted to Edit on a notes file) maintains a markdown notes file used AS the compaction summary, avoiding an extra LLM call; full LLM summary only as fallback.
- Port class: REFERENCE + REINTERPRET. Key cross-reference: IF the harness's native oversized-tool-output→disk behavior is real, it MAY already cover much of the gap Entry "headroom" targets externally — so the headroom port decision is GATED on first measuring what the harness already drops. Session Memory converges with our memory-extraction + the 2026-06-11 claude-memory-compiler PreCompact finding.
- Our substrate state: memory-preprocessor SessionStart inject + R2 extraction; we run on the Claude Code harness (not raw API) so the compaction beta header is reference-only.
- Suggested action: zero-risk audit — check whether THIS harness build writes oversized tool outputs to on-disk full-result files (look for them), and confirm the ~50K threshold empirically. That audit GATES the headroom prototype above. Will-triage on anything live.
- Verifier (sonnet subagent): REVISE → applied (harness-mechanism params demoted to SEARCH-CLAIMED/UNVERIFIED with correct provenance; trio kept at search-level; gate logic kept).
- Will-triage: pending
