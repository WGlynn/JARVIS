# Advice actionable — JARVIS-OS (hooks, memory, cron, scripts)

Populated by Odysseus cron loops § COMMANDMENT 2.5 per [F·odysseus-as-advisory-substrate].

JARVIS substrate = Python hooks under `~/.claude/hooks/`, file-based memory under `~/.claude/projects/C--Users-Will/memory/`, cron-prompt logic under `~/.claude/cron-prompts/`, scripts under `~/.claude/scripts/`. Odysseus advice that applies to similar self-hosted Python/agentic substrate goes here.

Format same as `_advice-actionable-vibeswap.md`.

---

## [2026-06-09 13:48 ET] — Hybrid retrieval + importance + decay; reject always-inject

- Source: PR #720 by @dustinm16 "memory: add importance scoring, retrieval boost, decay, and observation API" — https://github.com/pewdiepie-archdaemon/odysseus/pull/720 . Felix-active.
- Their advice (paraphrase): no always-inject / hot-tier force injection of any memory. Every memory passes through a hybrid relevance gate. Scoring formula: `0.50*vector_sim + 0.35*keyword + 0.05*recency + 0.10*importance` where `importance` is a 0.0-1.0 explicit field per memory. Decay over time. Separate observation API for write-side discipline.
- Our substrate state: JARVIS memory has `MEMORY.md` ALWAYS-injected at boot (~24KB cap), with sub-indexes loaded situationally. No per-primitive importance field. No decay. No hybrid scoring — sub-index selection is rule-based (situation matching), not relevance-weighted. This is the *opposite* of the PR #720 design — we lean hard into the always-inject pattern that #720 calls out as wrong.
- Suggested action: evaluate whether MEMORY.md's PRE-FLIGHT set is *all* genuinely fail-closed (rules that must fire before anything else) vs. some entries that drifted into PRE-FLIGHT by accretion. PRE-FLIGHT items that can be relevance-gated should move to a scored tier. Compose with [F·memory-bi-temporal-axis] candidate (queued from #2858 dispatch) — decay + bi-temporal supersession + importance scoring are the same primitive family.
- Will-triage: pending

## [2026-06-09 13:48 ET] — Three-lane separation: issues vs ADR vs specs

- Source: #605 "Proposal: Architecture & Codebase Structure v3" — @RaresKeY comment: https://github.com/pewdiepie-archdaemon/odysseus/issues/605 . Felix-active thread.
- Their advice (paraphrase): keep three lanes separate. (i) Issues/discussions = "should this exist?" proposals. (ii) Mini-ADRs = accepted intent + tradeoffs + decisions, captured in PR bodies or a dedicated decision-record folder. (iii) `specs/` = current implementation truth — what the code does now, contracts, security, data-shape rules future PRs must preserve.
- Our substrate state: JARVIS memory has primitives (rules) and projects (state) and feedback (corrections) but no explicit "this is current implementation truth" vs "this is accepted but unimplemented intent" vs "this is a proposal we may or may not accept" separation. Primitives in `memory/` mix all three. The `_primitives-pending.md` queue is informally the "proposal" lane but it's not load-bearing.
- Suggested action: introduce explicit lifecycle states on memory primitives — proposed (in `_primitives-pending.md`), accepted (in `memory/` with `status: accepted`), implemented (with `status: implemented` + cross-link to the hook/code that enforces it), superseded (preserved with link to successor). The existing primitives are already mostly in the "accepted" or "implemented" state but the distinction is implicit.
- Will-triage: pending

## [2026-06-09 13:52 ET] — Session-state mutability + cross-session leakage discipline

- Source: PR #267 by @Anxiety471 "fix: session context drifting — messages leaking between chats (#135)" — https://github.com/pewdiepie-archdaemon/odysseus/pull/267 . Felix-active.
- Their advice (paraphrase): two concrete root causes of cross-session leakage. (i) `Session.history` was a shared mutable list — every call to `get_session()` returned the same object and concurrent tasks appended to the same list. Fix: immutable copies via internal `_history` list, `add_message()` replaces `.history` with a fresh snapshot. (ii) Task scheduler overwrote `session_manager.sessions[session_id]` directly, discarding the in-memory Session and any unpersisted messages. Fix: `ensure_task_session()` checks the cache first.
- Our substrate state: JARVIS uses per-conversation shards (per `M·shard-per-conversation`) — each Claude conversation has its own shard. But many JARVIS hooks read+write SHARED files (`MEMORY.md`, `_primitives-pending.md`, campaign logs, cron state). When multiple cron loops fire concurrently (daily-cadence + discovery overlapping), the same shared-mutable-state hazard exists at the file level. We don't have a `_history` immutable-snapshot equivalent for shared logs.
- Suggested action: audit which JARVIS hooks/cron-prompts mutate shared files and whether concurrent fires can race. Specifically: `_primitives-pending.md`, `MEMORY.md` edits, `odysseus-discussion-campaign-log.md` (multiple loops append). Consider an append-only-with-tx pattern (write to a tmp + rename) for shared logs. Compose with [P·crash-resilient-memory-writes].
- Will-triage: pending

## [2026-06-09 14:48 ET] — Retrieval-boost-factor (no always-inject) — pivot in PR #720 review

- Source: PR #720 review thread, @dustinm16 + @pewdiepie-archdaemon. dustinm16's commit-pivot after Felix's review: https://github.com/pewdiepie-archdaemon/odysseus/pull/720
- Their advice (paraphrase): Felix flagged the always-inject "hot" memory tier as product-behavior-changing and held the PR for manual testing. dustinm16's response: "Hot-tier always-inject behavior — rethinking this. The current design overrides relevance-based filtering which is the wrong tradeoff. Planning to move importance to a retrieval boost factor only (stronger weight in the hybrid score) rather than a context injection guarantee. Users retain full control through the existing memory system."
- Our substrate state: JARVIS does always-inject (MEMORY.md PRE-FLIGHT set is loaded at every SessionStart, no relevance gate at all). The exact pattern dustinm16 just pivoted AWAY from. Our defense is that PRE-FLIGHT entries are the genuinely-fail-closed minority — but inspection of the actual PRE-FLIGHT list shows accretion has happened.
- Suggested action: re-audit MEMORY.md PRE-FLIGHT and demote anything that isn't truly fail-closed to a retrieval-boost-weighted entry that lives in a sub-index. The hybrid scoring formula from #720 (`0.50*vs + 0.35*kw + 0.05*recency + 0.10*importance`) is a serviceable starting weighting. Compose with the bi-temporal supersession candidate from #2858 to make the importance-decay axis honest.
- Will-triage: pending

## [2026-06-09 14:48 ET] — Prompt-behavior changes require explicit product gate

- Source: PR #720 review by @pewdiepie-archdaemon. Felix's principle, applied to dustinm16's PR.
- Their advice (paraphrase): "I would also want explicit product confirmation before always injecting 'hot' memories: even capped at 5, that changes prompt behavior." Translated principle: any change to the agent's prompt-behavior surface (what gets injected, when, at what weight) MUST pass an explicit product/owner gate, separate from code review. Code review checks correctness; product gate checks whether the behavior change is desired at all.
- Our substrate state: JARVIS has no explicit "prompt-behavior change" gate. Edits to MEMORY.md, the memory-preprocessor sub-index expansion, or any cron canonical that injects boot-context all silently change Claude's prompt at next session. Some of these changes are Will-approved; many are agent-side autonomous.
- Suggested action: distinguish "code/canonical change" from "prompt-behavior change" at the commit level. Latter type requires an explicit Will-approval gate, even under autonomous-mode posture (similar shape to [F·full-auto-public-action-gate] but applied at the substrate-prompt-surface level). Specifically: any MEMORY.md edit, any cron canonical edit that affects boot-injection, any hook that fires on SessionStart, gets queued for Will-approval rather than executed silently.
- Will-triage: pending

## [2026-06-09 15:08 ET] — Visual status indicator on primitive lifecycle states

- Source: Issue #605 comment by @elpideus. https://github.com/pewdiepie-archdaemon/odysseus/issues/605
- Their advice (paraphrase): "I wanted to contribute but I'm holding off until I know what's actually approved... A simple indicator (even plain emojis like ?/?/?) would make it much easier to know where to actually help." Translates to: lifecycle-state primitives need a visible status marker, not just a textual classification, so contributors can see at-a-glance what's accepted vs. proposed vs. archived.
- Our substrate state: extends the RaresKeY 3-lane entry above. JARVIS primitives have an implicit lifecycle (proposed in `_primitives-pending.md`, accepted in `memory/`, archived if superseded) but no visual marker. The file-system separation does some of the work, but a `status:` field in frontmatter + an emoji marker in the heading would make scanning the public substrate much easier.
- Suggested action: when implementing the RaresKeY 3-lane separation, also add a `status:` field to frontmatter (proposed / accepted / implemented / superseded) AND a heading-level emoji marker so a reader scrolling the `memory/` directory sees status at a glance. Compose with [F·advice-mining-must-publish-to-public-graph] — public primitives need readable status.
- Will-triage: pending

## [2026-06-09 17:55 ET] — AGPL over MIT for substrates that propagate via adoption

- Source: Discussion #1342 by @Zaptosis. 44 upvotes. https://github.com/pewdiepie-archdaemon/odysseus/discussions/1342
- Their advice (paraphrase): MIT license is inadequate protection if the goal is keeping the work free-as-in-freedom forever. The work can be repackaged into proprietary projects by the big-tech entities the project is trying to route around. AGPL / copyleft requires distributors to make source available to users, preventing extract-without-give-back.
- Our substrate state: jarvis-substrate is MIT. The [J·odysseus-mission-loop] thesis is that VibeSwap principles propagate via JARVIS adoption. If JARVIS gets MIT-forked by a proprietary AI agent vendor who strips the structural-fairness primitives and reskins the rest, the propagation mechanism is defeated. AGPL prevents that specific failure mode at the license layer.
- Suggested action: relicense jarvis-substrate from MIT to AGPL. The mission requires propagation BY USE not by sale; AGPL is the license-layer enforcement of that principle. Composes with [F·will-empowers-agent-on-substrate-design] — license is constitutional, Will-decide. Compose with [P·honesty-as-structural-load-bearing-property] — copyleft is structural-honesty at the license layer.
- Will-triage: pending (high-priority constitutional decision)

## [2026-06-09 17:55 ET] — Coding standard auto-enforcement (ruff for Python)

- Source: Discussion #3643 by @joebog1. https://github.com/pewdiepie-archdaemon/odysseus/discussions/3643
- Their advice (paraphrase): enforce coding standard from day 1. Python: PEP8 + black. JavaScript: ESLint + airbnb-style. Auto-formatter prevents style drift; reviewers can focus on substance.
- Our substrate state: jarvis-substrate has 4 .py files (hooks/scripts). No auto-formatter configured. Style is consistent because of my single-author bias but won't survive multi-contributor.
- Suggested action: add `pyproject.toml` ruff config (faster than black + linter combined). Add a pre-commit hook OR document `ruff format jarvis/ hooks/ scripts/` as the canonical pre-push step. Optional: GitHub Actions ruff workflow. Compose with [F·primitive-capture-vs-execution-throughput] — auto-format is the "no drift on stylistic axis" sibling discipline.
- Will-triage: pending

## [2026-06-09 17:48 ET] — Stabilize system prompt; sequence memory extraction outside the hot path

- Source: PR #3360 by @NoodleLDS. https://github.com/pewdiepie-archdaemon/odysseus/pull/3360
- Their advice (paraphrase): every chat message against a local OpenAI-compatible backend was forcing a full prompt re-evaluation (15-30s) because dynamic content was being folded into the system prompt on every turn, busting the KV cache. Fix at the payload-assembly boundary: stabilize the system prompt (no per-turn variance), sequence memory extraction so it does not block the user response, send stable.
- Our substrate state: JARVIS injects sub-indexes via memory-preprocessor at SessionStart (stable for the session) but the situation-matched WARM-MAP loader can change content mid-session. Per-turn DEEP-RECALL also varies. The hot-path penalty for KV-cache invalidation matters at scale; right now we eat it because everything runs through Anthropic's hosted inference where KV-cache discipline is opaque to us. When JARVIS-as-published agent ships with local backends, this becomes load-bearing.
- Suggested action: audit which hooks mutate the system-prompt portion vs which mutate user-turn content. Anything system-prompt-side should be stable-per-session. Move WARM-MAP injection to user-turn context if it must change mid-session. Compose with [F·full-auto-public-action-gate] for the publication-phase boundary.
- Will-triage: pending (load-bearing for JARVIS-publication phase, lower priority for hosted-inference current use)

## [2026-06-09 17:48 ET] — Fail-closed for null-user owner scope (auth-disabled vs auth-enabled-null distinction)

- Source: PR #3613 by @RaresKeY. https://github.com/pewdiepie-archdaemon/odysseus/pull/3613
- Their advice (paraphrase): in resource-owner filtering, distinguish auth-disabled single-user mode (where null-user is expected and means "show everything") from auth-enabled requests where current_user fails to resolve (where null-user is suspicious and should fail closed). Same owner policy across all related queries (list, sidebar, count, batch, stats) so the boundary is unified.
- Our substrate state: JARVIS is currently single-user (Will), so the auth-enabled-null case doesn't fire. Becomes load-bearing when JARVIS-as-published-agent ships with multi-user support. The principle (fail-closed for unresolved-auth, unified owner policy across related queries) is timeless.
- Suggested action: when scaffolding multi-user support, ship `AUTH_ENABLED` toggle that distinguishes the two cases explicitly. Default auth-enabled-null to 403 (or 404 to avoid enumeration). Audit all owner-filtering queries for shared policy enforcement. Compose with [F·will-empowers-agent-on-substrate-design] — the constitutional layer should encode "fail-closed on unresolved auth" as a mechanical predicate.
- Will-triage: pending (deferred to JARVIS-publication phase)

## [2026-06-09 17:42 ET] — Stabilization-milestone intake lane (proposed-vs-accepted lifecycle)

- Source: Discussion #3163 by @RaresKeY. https://github.com/pewdiepie-archdaemon/odysseus/discussions/3163
- Their advice (paraphrase): maintainer-owned `Stabilization v1` milestone with contributor intake lane. Good-fit candidates: security/auth/trust-boundary fixes, CI/tests/packaging/startup-runtime reliability, review/process templates that reduce maintainer load, small cleanup/restructuring PRs with clear validation, specs/implementation-truth docs, duplicate/overlap cleanup, platform stabilization, bugs that unblock many users. Bad fit: broad new features, large rewrites.
- Our substrate state: JARVIS primitives blend lifecycle states (proposed, accepted, implemented, superseded) with no explicit milestone discipline. Composes directly with the @RaresKeY 3-lane separation entry from #605 earlier today — that one named the structure (issues/ADR/specs), this one names the GOVERNANCE process (intake lane + maintainer-owned milestone). Together they form a stabilization framework JARVIS could adopt.
- Suggested action: introduce a `_stabilization-candidates.md` queue alongside `_primitives-pending.md`. Contributor (or agent-self) proposes primitives for stability; Will-as-maintainer promotes to `status: accepted` or rejects. Same intake-lane shape as RaresKeY's Stabilization v1. Compose with [F·will-empowers-agent-on-substrate-design] — agent proposes, Will-governance allocates milestone admission.
- Will-triage: pending

## [2026-06-09 17:42 ET] — Source-to-fact mapping for receipts traceability

- Source: Discussion #3642 by @penguman420. https://github.com/pewdiepie-archdaemon/odysseus/discussions/3642
- Their advice (paraphrase): verification bottleneck when sources are listed in bulk at the end of a report instead of mapped to specific claims. Solution: inline citations (each fact has a unique identifier or superscript linked to source), explicit (Fact A → Source B page X paragraph Y) data structure, hover/click verification UI.
- Our substrate state: JARVIS primitives have a `## 📦 Receipts` section listing sources, but the claim-to-receipt mapping inside the body is implicit. A reader can't easily verify "this specific claim in the body traces to this specific receipt." Same verification-bottleneck shape penguman420 names.
- Suggested action: introduce inline-receipt markers in primitive bodies — e.g., `[^r1]` superscript at the end of a claim, with receipts numbered in the receipts section. Or: tighter — quote-anchor every load-bearing claim to the specific Will-frame timestamp + permalink. Compose with [P·time-logic-anti-hallucination-gate] — verify-then-assert at write time, then make the verification AUDITABLE at read time.
- Will-triage: pending

## [2026-06-09 15:55 ET] — Merge/review policy as stabilization priority

- Source: Issue #3694 by @RaresKeY. https://github.com/pewdiepie-archdaemon/odysseus/issues/3694
- Their advice (paraphrase): define explicit review/merge policy v1 BEFORE PR volume scales further. Differentiate trivial (docs/typo) vs sensitive (auth, data-loss, CI, tool execution) — sensitive PRs require independent review + cooling-off window. Latest-commit-changes-after-approval invalidates approval.
- Our substrate state: JARVIS-side, I merge memory primitives autonomously during throughput-spikes. Per [F·primitive-capture-vs-execution-throughput] the drift is real; same shape as Felix's "rapid approve-to-merge" problem. We don't have a "this primitive change is sensitive" tier.
- Suggested action: classify primitive edits by sensitivity tier — trivial (typo, scope refinement) vs sensitive (axiom changes, classifier predicate rewrites, hook-firing changes). Sensitive edits require either Will-explicit-approval OR a 24h cool-off where the primitive lands as `status: proposed` then auto-promotes if no Will-objection. Compose with [F·will-empowers-agent-on-substrate-design] — agent can ship trivial, governance gate fires for sensitive.
- Will-triage: pending

## [2026-06-09 15:55 ET] — Workspace-confine agent file/shell tools via context-local binding

- Source: PR #3665 by @vdmkenny. https://github.com/pewdiepie-archdaemon/odysseus/pull/3665
- Their advice (paraphrase): scope agent file/shell tools to a selectable workspace folder via a context-local binding enforced at the shared path-resolver layer. New tools using the same resolver inherit confinement automatically — cannot bypass it.
- Our substrate state: JARVIS-driven Claude Code sessions have full file-system access via Read/Edit/Write/Bash. There's an environment-defined working-directory but no enforced confinement; an autonomous loop could theoretically write outside scope.
- Suggested action: add a JARVIS hook PreToolUse on Read/Write/Edit/Bash that validates the target path against an allowlist derived from the active project root + ~/.claude/. Reject (or surface scrub-warning) if a write targets a path outside allowlist. This is sandboxing-via-hook, same shape as vdmkenny's context-local binding.
- Will-triage: pending

## [2026-06-09 15:55 ET] — Container sandbox for agent shell tools (defense-in-depth)

- Source: PR #3695 by @ruanbluiz. https://github.com/pewdiepie-archdaemon/odysseus/pull/3695
- Their advice (paraphrase): opt-in, default-off ephemeral container per agent bash/python tool call. Prevents prompt-injection from reaching process env (creds/keys) or internal/metadata endpoints. Strictly additional confinement on top of existing admin gate.
- Our substrate state: JARVIS Bash invocations run in the parent shell with full env access — email addresses, deployment service credentials, GitHub PAT, and other secrets are reachable via `env`. A prompt-injected agent could exfiltrate.
- Suggested action: scope this against [F·burn-compute-toward-mission] threat model. For single-user-zero-stakes-phase (per [P·pre-decentralization-optimization-sequencing]), in-process is fine. But: surface this as a candidate for when JARVIS-as-published-agent ships (per [J·odysseus-mission-loop] Step 2) — published contributors should get sandboxing by default.
- Will-triage: pending (deferred to JARVIS-publication phase)

## [2026-06-09 15:31 ET] — Write-side embedding similarity as fallback to entity-registry regex

- Source: agent-self-surfaced during the @Amir0234-afk reply draft on #2858. The honest framing forced the gap into the open: write-side currently uses regex against a maintained registry, write-side embedding similarity is not implemented. Per [F·positive-vs-negative-contribution-decision] axis 2: self-surfaced advice still goes in the queue if substrate-relevant.
- Their advice (paraphrase): the entity-cross-reference hook should run a thin embedding-similarity fallback on the new content when the regex pass finds zero matches. Catches paraphrase/synonym references to known primitives that the entity-registry would miss (e.g. "the cognition gate that simulates Will's judgment" → WWWD primitive even though "WWWD" isn't in the text). Hybrid stays: regex first (fast, deterministic) for known entity tokens, embedding-similarity second (fallback) only when regex misses.
- Our substrate state: write-side = string-only. Read-side already has semantic similarity (the UserPromptSubmit DEEP RECALL pass). The asymmetry is the gap. Bottleneck I already named in the Amir reply: entity-registry maintenance — a write-side embedding fallback partially dissolves that bottleneck by catching synonym matches without registry updates.
- Suggested action: implement as a small extension of the entity-cross-reference hook. When regex returns zero matches, run a cached cosine pass against pre-computed primitive embeddings; surface matches above threshold. Embedding cache invalidated on memory/ writes. Adds one model call per zero-match write — bounded latency.
- Will-triage: pending

## [2026-06-09 13:52 ET] — MCP Streamable HTTP + per-server auth headers

- Source: PR #803 by @akapug "feat(mcp): Streamable HTTP transport + per-server auth headers" — https://github.com/pewdiepie-archdaemon/odysseus/pull/803 . Felix-active.
- Their advice (paraphrase): MCP managers that only support stdio + headerless SSE can't connect to authenticated remote MCP servers (GitHub, Linear, Sentry, Cloudflare). Adds `transport: "http"` (aliases `streamable-http`) via the MCP SDK `streamablehttp_client` with proper 3-tuple unpacking, plus per-server `headers` field for `Authorization: Bearer <token>`.
- Our substrate state: JARVIS uses Claude's MCP integrations (Gmail, Calendar, Spotify, Google Drive, Microsoft 365). The auth flow is handled by Claude's own server-side OAuth, not by us configuring an MCP client. The `streamablehttp_client` advice applies to *self-hosted* MCP servers — we don't currently run any. If/when JARVIS adopts a self-hosted MCP server for VibeSwap-specific tools (e.g., contract-query, oracle-status), this advice becomes load-bearing.
- Suggested action: file under "load when JARVIS adds self-hosted MCP servers"; do not action now. Note the 3-tuple unpacking gotcha for future implementers.
- Will-triage: pending (deferred — no current MCP server to apply to)

## [2026-06-11 12:55 ET] -- Deterministic post-merge audit lane for speed-priority pipelines

- Source: #3163 comment by @RaresKeY 2026-06-10T00:23Z (https://github.com/pewdiepie-archdaemon/odysseus/discussions/3163)
- Their advice (paraphrase): audited 70 fast open-to-merge merged PRs against current dev; 48 of 70 (~69%) have at least one source-backed follow-up bug note (55 notes total). Conclusion: when merge speed is prioritized, a deterministic post-merge audit lane (re-check merged work against current state, file follow-ups) is the correction mechanism, and the follow-up ratio is the measurable quality signal for the pipeline.
- Our substrate state: JARVIS cron loops auto-commit and push to WGlynn/jarvis-substrate (substrate-sync every 2h, advice-mirror per fire) with zero post-hoc review lane. Same shape: speed-priority unattended writes, no measured follow-up ratio. VibeSwap dual-remote pushes share the shape when sessions move fast.
- Suggested action: small audit cron (weekly) that samples recent auto-commits in jarvis-substrate, re-checks them against current substrate state (broken links, stale pointers, scrub-list violations), and files notes to _primitives-pending.md. Track the follow-up ratio over time as the pipeline quality metric.
- Will-triage: pending

## [2026-06-16 13:30 ET] -- Problem-owner vs candidate-implementation split, with an explicit short-track to avoid "dead by policy"
- Source: #4415 by @RaresKeY + @TimHoogervorst refinement (https://github.com/pewdiepie-archdaemon/odysseus/discussions/4415)
- Their advice (paraphrase): make the issue the durable owner of the problem; PRs are candidate implementations of it (multiple PRs per issue; the issue survives a bad PR). BUT add a short-track route so narrow/clearly-scoped work (small bugfix, isolated UI, strict-scope) skips the full bucket ceremony, otherwise the structure becomes "dead by policy."
- Our substrate state: _primitives-pending.md is already the problem-owner and promoted memory primitives are the candidate-implementations of each observed need -- same shape, currently implicit. C3 already says "empty days valid," but there is no explicit short-track: every observation gets the same full structured-note ceremony regardless of triviality.
- Suggested action: add a 2-bucket classify to C3 -- (i) needs-structure (recurring/overlapping/edge-case) gets the full pending note; (ii) narrow/obvious (one-line rule, trivial fix) short-tracks to a single log line or direct fix, no ceremony. Mirrors RaresKeY's needs-organization vs narrow-scope split; keeps the loop from generating ceremony-noise.
- Will-triage: pending

## [2026-06-16 13:30 ET] -- Keep core small; push large features behind a thin manifest contract; land the contract as one minimal increment
- Source: #4439 by @vdmkenny + @RaresKeY routing comment (https://github.com/pewdiepie-archdaemon/odysseus/discussions/4439)
- Their advice (paraphrase): a recurring flood of multi-thousand-line feature PRs into core grows the security/maintenance surface and re-litigates "should this be in core." Fix: a thin plugin contract (manifest + capabilities) so large features live outside core; and land the CONTRACT first as one small reviewable PR, not a 4,900-line platform.
- Our substrate state: this is already the cron architecture -- cron entry = thin pointer (marker + path), canonical .md = logic; CLAUDE.md/core memory stays small, behavior lives in hooks/cron-prompt "plugins." Validates the design. The refinement we lack: new cron behaviors are sometimes authored as fat monolithic prompts instead of pointer+canonical from inception.
- Suggested action: enforce the pointer+canonical contract for ALL new crons from inception (marker + path in scheduled_tasks; logic in a versioned .md), and land new substrate features as the minimal contract first (IPM/ponytail at the substrate layer) rather than a monolithic prompt. Same shape as "land the contract as one small PR."
- Will-triage: pending


## [2026-06-18 17:17 ET] — plugin/extension contract so large features don't all land in core
- Source: #4439 comment by @vdmkenny (https://github.com/pewdiepie-archdaemon/odysseus/discussions/4439)
- Their advice (paraphrase): define a stable extension/plugin contract so multi-thousand-line features migrate OUT of core; core stays lean.
- Our substrate state (shape-match): JARVIS-OS has hook/primitive sprawl (329 primitives, 361 orphan files at boot) — the "everything lands in core" shape.
- Suggested action: a plugin/skill contract boundary for JARVIS primitives/hooks so new capability is additive-modular, not core-bloat.
- Will-triage: pending

## [2026-06-18 17:17 ET] — release tags + branch discipline for a single-main repo
- Source: #2431 comment by @Faultline47 (https://github.com/pewdiepie-archdaemon/odysseus/discussions/2431)
- Their advice (paraphrase): single active main + no release tags + large open-PR backlog = stability risk for self-hosted prod; add release tags / branch discipline.
- Our substrate state (shape-match): JARVIS substrate + vibeswap push-to-main, no tagged releases.
- Suggested action: lightweight release tagging on the public substrate so inspectors can pin a known-good state.
- Will-triage: pending
