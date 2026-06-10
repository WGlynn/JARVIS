---
name: ResearchBatch2026-06-10-Deep
description: Deeper mining pass 2026-06-10 (sibling of [R·research-batch-2026-06-10]). Skills.sh ecosystem · NEW loop patterns (MOSS production-substrate · Meta-Harness · Crab semantics-aware checkpointing · Orchestrator-Executor-Synthesizer split · state-hash loop prevention) · post-LF MCP ecosystem (Tunnels · Sandboxes · Playwright · MCPProxy) · documented anti-patterns (God-tool · Chatty-protocol · Context-rot · Token-blind multi-agent fan-out 58-285% overhead) · Claude Code Routines real triggers. Source-verified, last30days bias.
type: reference
originSessionId: d3ae9e64-adfb-4ba8-aa55-fee4f96e0207
---
# Research Batch 2026-06-10 (Deep)

## ⇒ Skills.sh ecosystem (Section 1)

- **Demand/supply imbalance** ⇒ information-retrieval skills 5× install-rate of code-gen, supply-constrained ⇒ underserved category
- vercel-labs/react-best-practices · 100K+ installs (launch flagship)
- Agensi code-reviewer · most-installed free
- git-commit-writer · pr-description-writer · readme-generator · env-doctor (productivity staples)
- **Firecrawl skill** ⇒ structured scrape/crawl/search · fits Will research loops
- **MCP-builder (Anthropic official)** ⇒ scaffold new MCP servers from spec
- Stripe bundle · payments flows

## ⇒ NEW loop patterns (Section 2)

### MOSS production-substrate evolution
- batch failure evidence → external CLI code-mod → trial-replay in ephemeral worker → consent-gated container swap with health-probe rollback
- borrowable: batch-of-failure-evidence anchor + trial-replay-before-promote
- src: arxiv 2605.22794v2

### Meta-Harness execution-trace feedback
- feed past run-traces (¬ just benchmark scores) to coding-agent proposer
- WAL ≡ trace substrate ⇒ missing primitive = trace-as-proposer-input
- referenced in MOSS paper

### Crab semantics-aware checkpointing
- **75% of agent turns produce zero recovery-relevant state**
- selective-checkpoint ⇒ recovery correctness 8% → 100% ∧ checkpoint traffic -87%
- borrowable: recovery-relevance gate BEFORE WAL-write
- sharper than LangGraph blanket checkpoint
- src: diagrid.io/blog/checkpoints-are-not-durable-execution

### Orchestrator / Executor / Synthesizer split
- separates LLM-brain from tool-hands
- router picks N agents → executor batches concurrent → synthesizer merges
- **always exactly 2 LLM calls regardless of execution shape**
- src: stackademic.com/blog/beyond-the-agentic-loop-the-orchestrator-pattern-for-multi-agent-systems

### State-hashing for loop prevention
- orchestrator-side hard-budget + state-hash repetition detection + monotonic-progress check
- ≡ mechanizes [F·repetition-is-useless] at hook layer (currently advisory-only)
- src: beam.ai/agentic-insights/multi-agent-orchestration-patterns-production

## ⇒ Post-LF MCP ecosystem (Section 3)

- **MCP Tunnels** (research preview 2026-05-19) ⇒ single outbound encrypted connection · enterprise-firewall solved
- **Self-hosted Sandboxes** (public beta 2026-05-19) ⇒ Cloudflare/Daytona/Modal/Vercel
- **Playwright MCP (Microsoft)** ⇒ 30K+ stars · #2 most popular MCP · browser automation
- **MCPProxy** ⇒ gateway pattern matured post-LF · multi-server routing + observability
- ✗ HashiCorp Vault MCP (June ETA, ¬ shipped)
- ⚠ MCP SDK stdio-RCE (April OX disclosure) ⇒ patch + audit before installing stdio-transport servers
- src: workos.com/blog/everything-your-team-needs-to-know-about-mcp-in-2026

## ⇒ Anti-patterns (Section 4)

- **God-tool** ⇒ `run_command(action, params)` mega-tool with 15-value action enum ⇒ hallucinates wildly. Will has discrete skills ✓
- **Chatty protocol** ⇒ tool returns ID forcing follow-up lookup ⇒ inline payload preferred
- **Context rot @ 20-30 turns** ⇒ measurable 2%/step retention loss · 0.85^10 = 19.7% success on 10-step workflows · eviction + compaction matter more than longer windows
- **Unbounded loops** ⇒ hard budget enforced by orchestrator ¬ agent self-report
- **Hidden state retry storms** ⇒ race on shared resource without idempotency key (Will WAL idempotency ✓)
- **Token-blind multi-agent default** ⇒ Princeton: **single agent matches multi-agent on 64% of tasks at HALF cost**; fan-out overhead 58-285% tokens ⇒ ✗ default to fan-out (relevant to RSAW dispatch patterns)
- src: atlan.com/know/agent-harness-failures-anti-patterns/ · digitalapplied.com/blog/agentic-workflow-anti-patterns-orchestration-mistakes-2026

## ⇒ Claude Code Routines real triggers (Section 5)

Released 2026-04-14 research preview · Anthropic cloud-run · ¬ local machine
- Triggers ⇒ {Schedule, API, GitHub}
- Min schedule = 1 hour
- Daily caps ⇒ Pro=5 · Max=15 · Team/Ent=25
- **Runs WITHOUT approval prompts** ⇒ prompt explicitness ≡ safety surface

Real shipped triggers (practitioners 2026-05):
- nightly 2am ⇒ pull top Linear bug → fix attempt → draft PR (Anthropic example)
- weekly Fri 4pm ⇒ read merged PRs → category-group → CHANGELOG.md PR
- weekly ⇒ list 30d-stale branches → Slack one-click delete (¬ auto-delete)
- GitHub PR open ⇒ filtered review automation
- 5am daily ⇒ Gmail triage via connector → drafts → Slack summary
- weekly docs-drift ⇒ scan merged PRs → stale-doc flags → update PR

⇒ Will's cron-prompts substrate ≡ local-counterpart · Routines = cloud-hosted GitHub-webhook-native
⇒ caveat: routines own under personal GitHub identity · no team sharing in preview
- src: claude.com/blog/introducing-routines-in-claude-code · code.claude.com/docs/en/routines

## ↦ 5 borrowables ranked by leverage

1. **Crab semantics-aware recovery-relevance gate** ⇒ apply BEFORE WAL/checkpoint writes. JARVIS WAL currently logs heavily; 75% drop expected without losing recovery fidelity. HIGH leverage.
2. **State-hash loop prevention** ⇒ mechanizes [F·repetition-is-useless] as hook (orchestrator-side hard budget + state-hash + monotonic-progress). HIGH leverage.
3. **Token-blind multi-agent warning** ⇒ extend coordination-mechanism-gate to flag fan-out-without-justification per Princeton 64%/half-cost finding. MEDIUM-HIGH leverage. Composes with classifier.
4. **MOSS trial-replay-before-promote** ⇒ container-swap-with-rollback discipline for JARVIS substrate-modification primitives (auto-arsenal promotion). MEDIUM leverage.
5. **Routines as cloud-counterpart to cron-prompts** ⇒ GitHub-webhook-native is the new primitive; Will's cron-prompts is local. Worth experimenting with for 1 use-case (e.g., Odysseus daily-discussion). MEDIUM leverage.

## ↦ Siblings

- [R·research-batch-2026-06-10] ⇒ first pass (Bifrost · Inworld · CKB · agent-ecosystem overview)
- [J·jarvis-coordination-mechanism-rick-2026-06-10] ⇒ Tier 3 + token-blind warning composes
- [P·code-mode-orchestration] ⇒ Bifrost Code Mode primitive
- [F·repetition-is-useless] ⇒ the rule state-hashing would mechanize
