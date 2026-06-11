# SKILL MINING LOOP — canonical prompt body

Loaded by cron pointer-prompts that contain `type: skill-mining`. The cron prompt is the pointer; this file is the logic. Update this file to change behavior without recreating crons.

**Mission** (Will, 2026-06-10): "compression technique mining / knowledge base mining — it's like just browsing the internet and github for useful stuff for us." Mine the open web + GitHub for techniques that strengthen the JARVIS substrate (hooks, HIERO memory, BPE corpus cache, recall/preprocessor stack, WWWD telemetry) and VibeSwap tooling. Sibling of odysseus-discovery; same 3-commandment skeleton.

---

## ═══ COMMANDMENT 1 — MAKE THE LOOP ═══

Self-perpetuation before any other work. Identical to odysseus-discovery C1, marker `type: skill-mining`:

1. Read `~/.claude/scheduled_tasks.json`.
2. Find entries whose `prompt` contains `type: skill-mining`.
3. `age_days = (now_ms - createdAt) / 86_400_000`.
4. All entries `age_days > 5` → `CronCreate(cron=<same schedule>, prompt=<same pointer verbatim>, durable=true)`.
5. 3+ entries per unique schedule → `CronDelete` all but 2 youngest per schedule.
6. Only then proceed to COMMANDMENT 2.

---

## ═══ COMMANDMENT 2 — THE MINING SWEEP ═══

### State files
- `~/.claude/cron-prompts/_skill-mining-log.md` — append-only audit: every sweep, every vein checked, hit or dry
- `~/.claude/cron-prompts/_skill-mining-queue.md` — actionable finds awaiting Will-triage
- Halt-flag: grep `MEMORY.md` for `SKILL_MINING_HALT` → exit + calendar ping

### Hard caps
- Max 1 sweep per day (check log for today's date → exit silent if present)
- Max ~8 web searches + ~8 fetches per sweep (token discipline; per [F·token-blind-multi-agent-default-is-anti-pattern] do NOT fan out agents by default)
- Dedup: skip any repo/technique already in the queue, log, or memory corpus

### Veins (rotate 2-3 per sweep, note which in log)
1. **Context/prompt compression** — LLMLingua-class token compression, summarization-cache schemes, KV-cache/attention tricks portable as text-layer ideas
2. **Agent memory systems** — Letta/MemGPT, mem0, Zep/Graphiti, cognee, A-MEM class; extraction/consolidation/decay/retrieval mechanics
3. **Knowledge-base architecture** — KG-on-files, bi-temporal indexing, entity linking, dedup/consolidation algorithms
4. **Claude Code ecosystem** — awesome-claude-code, community hooks/skills/statuslines/MCP servers; anything directly liftable
5. **RAG/retrieval mechanics** — chunking, reranking, hybrid sparse+dense, embedding cache patterns for our deep-recall.py
6. **Self-improving-agent tooling** — eval harnesses, telemetry→behavior loops, corpus distillation
7. **Frontend** (Will, 2026-06-10: "and frontend skill mining as well") — React/Vite/Tailwind ecosystem moves, animation libs (Motion/GSAP class), component collections, perf patterns, upgrade paths relevant to `vibeswap/frontend` (React 18 + Vite 5 + Tailwind + framer-motion + ethers v6). Findings classify against the LOCKED terminal-console aesthetic in `vibeswap/CLAUDE.md` — component-collection finds that fight the aesthetic = DROP.

### Per-find classification — substrate-port pattern ([P·substrate-port-pattern])
| class | meaning |
|---|---|
| **DIRECT-PORT** | drop into our stack near-verbatim (e.g. a hook idea, a compression algorithm on text files) |
| **REINTERPRET** | same shape, our inputs (e.g. vector-DB memory → our file+BPE substrate) |
| **DROP** | substrate-mismatch or needs infra we reject (servers, paid APIs) — log 1 line WHY |

### Queue entry format
```
## [YYYY-MM-DD HH:MM ET] — <one-line technique summary>
- Source: <repo/post URL> (stars/recency if relevant)
- Technique (paraphrase): ...
- Port class: DIRECT-PORT | REINTERPRET (+ translation note) | DROP (+ why)
- Our substrate state: <what we already have that this touches>
- Suggested action: ...
- Will-triage: pending
```

### Rules
- VERIFY before claiming: fetch the repo/post, don't queue from a search snippet alone (Anti-Stale Feed / AA#4)
- Empty sweeps are valid — a dry day gets one log line, no fabricated finds
- Auto-act only on zero-risk local experiments (e.g. benchmark a compression idea on a scratch copy); anything touching live hooks/memory/settings = Will-triage

### Verifier stage — maker ≠ checker (per [F·design-loops-not-prompts], added 2026-06-10)
Before committing queue entries, dispatch ONE verifier subagent in an independent context (haiku/sonnet tier). It receives only the drafted queue entries + this rubric, NOT the sweep transcript:
1. Source actually fetched, or honestly marked search-level?
2. Numbers honest (typical-case, not peak/marketing)?
3. Port-class defensible — would DROP/REINTERPRET survive a skeptic?
4. Suggested action concrete + correctly bucketed (zero-risk auto vs Will-triage)?
Verifier returns per-entry PASS / REVISE(reason). Revise before commit; log verifier verdict in the sweep row. The sweep's "done" is the verifier's claim, not the miner's.

---

### Public-propagation requirement (Will, 2026-06-10: "push everything you adopt to the jarvis repo")
After any write to `skill-mining.md`, `_skill-mining-log.md`, `_skill-mining-queue.md`, or `_primitives-pending.md`, copy the changed files into `C:/Users/Will/jarvis-os-public/cron-prompts/` and push to `WGlynn/jarvis-substrate` within the same tick. **Scrub-list applies to the public copies**: no partner names, no thread-IDs tied to partners, no locked-engagement content, no engagement specifics — replace with generic phrasing ("an active external research thread"). Anything ADOPTED from a sweep (a hook, a script, a convention) ships to the public repo in the same commit cycle it lands locally.

---

## ═══ COMMANDMENT 3 — PRIMITIVES ═══

After C2 (hit or dry): if the sweep surfaced a generalizable pattern (new vein worth adding, new classification edge, a technique-class that keeps recurring), append to `~/.claude/cron-prompts/_primitives-pending.md` in the standard format (Trigger / Observation / Candidate primitive / Composes with / Status: pending Will-triage). Empty days append nothing.

---

## ═══ ON ERROR ═══

Save state to `Desktop/skill-mining-error-YYYY-MM-DD-HHMM.md`. Calendar ping. COMMANDMENT 1 must complete even on C2/C3 error.
