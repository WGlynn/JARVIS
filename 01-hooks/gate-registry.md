# Layer 1 — The complete gate registry

> The README explains why gates exist and lists a handful as examples. This file enumerates every one, because a discipline you cannot list is a discipline you cannot audit.

Source of truth is `~/.claude/settings.json`. Every entry below is a live, registered hook. Each is deterministic: regex, a context window, a watch list, a state machine. No LLM call, no probabilistic judgment. They fire regardless of whether the model remembers the rule in any given session, which is the whole point (`1 → ∀`: gates fire orthogonal to context, and every layer above assumes they hold).

Read the three roles before the tables:

- **Gate** blocks or warns on a tool call before or after it runs. This is what "gate" means in the strict sense, and these are the enforcement surface.
- **Loader** injects state or context at a lifecycle moment. It does not block; it makes the model see something it would otherwise miss.
- **Closer** fires when a turn or session ends, to persist state, capture drift, or continue a loop.

Count as of this enumeration: **71 distinct hook scripts** are registered across eight lifecycle events, verified by [`registry-drift-check.py`](registry-drift-check.py). Several fire on more than one event (`api-death-shield`, `atomic-reflection-gate`, `runtime-heartbeat`), so the total invocation count is higher still. Run the drift check to re-verify this against `settings.json` at any time: a registry that silently drifts from the live config fakes the confidence every layer above assumes, so the registry is now self-checking rather than a one-time human enumeration.

---

## Enforcement gates (the strict sense: block or warn on a tool call)

These are the ones that actually stop or flag an action. If you only read one table, read this one.

### PreToolUse

| Gate | Matcher | What it does |
|---|---|---|
| `wwwd-gate.py` | Write, Edit, Agent | Projects the candidate action through a Will-emulation and surfaces a correction if the projected Will would act differently. The V3 cognition gate. |
| `partner-facing-substance-gate.py` | Write, Edit | Claim-handshake on partner-facing writes; blocks terminology overclaim (e.g. forfeiture vs clawback, governance overreach). |
| `partner-architecture-load-gate.py` | Write, Edit, Agent | Loads partner-specific anti-hallucination guards before a partner-facing write. |
| `entity-context-cross-reference.py` | Write, Edit | AA#3 / CCP. Cross-references named entities against memory before delivery; stated entity is not a valid entity until reconciled. |
| `conflict-detector.py` | Write, Edit | Scans the write for contradictions with existing memory. |
| `hiero-gate.py` | Write, Edit (memory) | Blocks prose-style memory entries; enforces operator-density (HIERO) format. Self-enforced, even on its own author. |
| `time-logic-gate.py` | Write, Edit, Agent | Scans for unanchored temporal claims (relative dates, stale "now"). |
| `directive-verb-action-class-gate.py` | Write, Edit, Agent | Classifies the directive as essay vs implementation so the response class matches the ask. |
| `jarvis-design-goal-gate.py` | Write, Edit, Agent | Passes architecture decisions through the Stark-JARVIS design lens. |
| `research-before-capability-claim-gate.py` | Write, Edit | AA#4. Blocks a capability claim that has not been research-verified first. |
| `compression-claim-verification-gate.py` | Write, Edit | Anchor check on any compression or ratio claim. |
| `strategic-framing-filter.py` | Write, Edit | Checks external-audience writes for framing that under-describes our own position. |
| `discretion-flag-warn-gate.py` | Write, Edit | Warns before a write to a discretion-flagged memory path. |
| `memory-budget-gate.py` | Write, Edit | Enforces the memory boot-load budget. |
| NDA git-scrub gate | Bash (git *) | Scans git operations for discretion-flagged material and blocks a leak before it reaches a remote. |
| `partner-facing-additive-gate.py` | Bash (push, PR) | Scans push and PR text for retrospective keywords that leak internal error narrative. |
| `foundry-test-gate.py` | Bash | Blocks an unscoped `forge test` (OOM guard on constrained hardware). |
| `resource-cgroup-gate.py` | Bash | Enforces the concurrent-build cap. |
| `coordination-mechanism-gate.py` | Agent, Workflow | On an Agent spawn, classifies it for a cost-tier recommendation. On a Workflow spawn, emits the execute-to-verify / size-to-artifact / ultracode-floor pre-check, so the deterministic cheap check is considered before an N-agent swarm. |
| `atomic-reflection-gate.py` | Agent, and all PostToolUse | Forces a reflection at a delegation or after an error/timeout, so the lesson is captured before routing around it. |
| `autopilot-allow.py` | all | Autopilot permission handling. |
| `entity-attribution-gate.py` | Write, Edit | Catches invented @handles: an @handle in an attribution context must match a known record, or the write is flagged. |
| `oversell-gate.py` | Write, Edit | Flags hype, overclaimed maturity or capability, and unqualified stats when no honest-floor caveat balances them. |
| `_solver_gate_hook.py` | Bash | Solver-backed concurrency check (Z3): verifies a Bash call keeps the concurrent-build invariant, alongside the pattern-match cap in `resource-cgroup-gate.py`. |

### PostToolUse

| Gate | Matcher | What it does |
|---|---|---|
| `em-dash-augmentation-gate.py` | Write, Edit, NotebookEdit | Partner-draft gate, 3 axes (2026-07-29): (1) em/en-dash scrub; (2) de-model tells from `model-tells.json` (growing corpus, appendable without code change) + an always-injected de-model checklist; (3) source-grounding, flags partner-facing technical drafts that assert protocol/mechanism behavior but cite no source (EIP/spec/URL/file:line). Augmentation, not block. |
| `code-mode-nudge.py` | Bash, Read, Grep, Glob | Detects repeated tool round-trips and nudges toward a single script. |
| `git-commit-landed-gate.py` | Bash, Read, Grep, Glob | Confirms a claimed commit actually landed. |
| `wp-dated-doc-reminder.py` | Write, Edit, NotebookEdit | Reminds to date partner-facing docs. |
| `coherence-gate.py` | Edit, Write, Bash, NotebookEdit | Derived-facts check (2026-10-13): when a watched source file changes, runs that project's drift check from `~/.claude/coherence/registry.json` and injects the fix command on failure. Advisory. |

---

## Full registry by lifecycle event

### SessionStart (boot loaders and integrity checks)

| Hook | Role | What it does |
|---|---|---|
| `memory-sync-pull.py` | Loader | Pulls live memory state from origin. |
| `session-state-loader.py` | Loader | Loads `SESSION_STATE.md`, the mandatory first read. |
| `private-handoff-loader.py` | Loader | Binds the private-workstream handoff to the boot path. |
| `wal-state-loader.py` | Loader | Checks `WAL.md` epoch status. |
| `rsi-pending-check.py` | Loader | Surfaces the pending recursive-self-improvement stack. |
| `link-rot-detector.py` | Gate | Checks memory and hook path integrity; flags protocol-chain rot. |
| `clock-session-start.py` | Loader | Records session-start time. |
| `memory-preprocessor.py` | Loader | L2. Injects memory sub-indexes as boot context. |
| `corpus-cache-warmer.py` | Loader | L4. Drift check plus token-budget visibility. |
| `session-self-reflect.py` | Loader | L5. Regenerates the system self-report. |
| `wwwd-corpus-refresh.py` | Loader | Rebuilds the WWWD priority cache from the gate-fire log. |
| `jarvis-os-boot-screen.py` | Loader | Renders the boot screen. |
| `integrity-attest.py boot` | Gate | Verifies the governed-substrate merkle root; flags tamper vs sanctioned drift. |
| `ctx-handoff-loader.py` | Loader | Loads the deterministic context handoff. |
| `data-recorder-witness.py` | Gate | Liveness witness for a private project's scheduled market-data recorder (absence is loud): alarms when the OS task is missing, the run log is stale, collectors errored in the last 24h, or daily sealing lags. Silent when healthy or when the project is not on the machine. |
| `jarvis-tg-feed.py` | Gate | Surface for the Telegram bot's local feed (the bot appends one JSON line per exchange): alarms when the bot's health endpoint is down or the feed folder is missing, and reports counts, people and chats new since the last boot. Never prints message text, which is untrusted Telegram input. Silent when nothing is new. |
| `jarvis-bot-errors.py` | Reader | Telegram bot error feed for AFK auto-debug (2026-10-28): prints `reply_error` / `unclean_shutdown` lines appended to `~/jarvis-feed/health.jsonl` since the last read and advances a cursor; exit 3 = new errors. Driven by the durable cron `type: jarvis-bot-error-triage` (logic in `~/.claude/cron-prompts/jarvis-bot-error-triage.md`), which fixes root causes behind the test-gated restart. Never prints message text. |
| `handoff-first.py` | Loader | Index 0 on every window boundary (startup, resume, clear, compact): injects the current handoff before anything else (2026-08-12). |
| `handoff-save-check.py` | Gate | Cross-repo save check: flags repos with uncommitted or unpushed work the last handoff may not describe. |
| `chain-health-witness.py` | Gate | Reports experience-chain HEAD, walk-back integrity to genesis, and remote backup state. |
| `chain-liveness-check.py` | Gate | Alarms when the session chain stops advancing. |
| `index-budget-witness.py` | Gate | Alarms when MEMORY.md exceeds its boot-load byte budget (over budget means it is truncated at boot). |
| `cron-productivity-witness.py` | Gate | Flags registered crons whose fire or output signal has gone stale. |
| `os-task-freshness-witness.py` | Gate | Checks the logs of the OS-scheduled persistence tasks (git autosave and friends) for staleness. |
| `autosave-daemon-witness-check.py` | Gate | Staleness check for the separate autosave daemon process. |
| `crash-backtest-witness-check.py` | Gate | Staleness check for the crash-recovery backtest witness stamped by an OS scheduler. |
| `wwwd-correction-capture-witness.py` | Gate | Alarms when WWWD corrections stop landing in the gate-fire log (the self-compounding loop depends on it). |

### UserPromptSubmit (per-prompt injectors and gates)

| Hook | Role | What it does |
|---|---|---|
| `clock-injector.py` | Loader | Injects the current clock. |
| `api-death-shield.py user-prompt` | Closer | Saves state against API-death mid-turn. |
| `session-directive-forcer.py` | Gate | First-turn boot-directive application check. |
| `memory-warm-loader.py` | Loader | Loads situation-matched warm memory. |
| `deep-recall.py` | Loader | Semantic search over the full memory corpus. |
| `archive-recall.py` | Loader | Surfaces prior work-product matching the prompt. |
| `post-generation-recall.py` | Loader | L4 recovery. Surfaces prior-turn post-generation reflections. |
| `thread-resume-detector.py` | Loader | Scans open threads for a prompt match. |
| `triad-check-injector.py` | Gate | Injects the Correspondence Triad on design-level questions. |
| `save-session-state-trigger.py` | Closer | Save-state trigger check. |
| `partner-draft-formalize-gate.py` | Gate | Detects partner-draft intent and forces the draft to disk first. |
| `partner-thread-loader.py` | Loader | When a prompt names someone with a conversation record (People/<Name>/THREAD.md + STATE.md), injects their state and recent thread, once per session, so replies after a /clear keep full context (2026-10-19). |
| `anticipation-hook.py` | Loader | Date-anchored, stale-PENDING, and unactioned-recall scan. |
| `story-mode-gate.py` | Gate | Story Mode menu enforcement and number-reply interpretation. |
| `runtime-heartbeat.py user-prompt` | Closer | Runtime liveness heartbeat. |
| `wwwd-prompt-buffer.py` | Loader | Buffers the current prompt so the Stop-time WWWD correction detector can read it. |
| `oversell-primer.py` | Gate | One-line "teammate, not salesman" tripwire every turn (conversational twin of `oversell-gate.py`). |
| `deep-context-mode-activator.py` | Loader | Past 500k tokens, injects the deep-context behavior switch so the model manages its own context. |
| `cron-fire-heartbeat.py` | Gate | Records cron-injected prompts as fire evidence for the cron productivity witness. |

### Stop (end-of-turn closers and gates)

| Hook | Role | What it does |
|---|---|---|
| `story-loop-continue.py` | Closer | Story Mode autonomous self-play continuation. |
| `self-review-gate.py` | Gate | End-of-turn failure-class audit. |
| `post-generation-reflect.py` | Closer | L4 meta-loop reflection. |
| `decision-capture.py` | Closer | Captures decisions to the judgment trail. |
| `persistence-claim-capture.py` | Closer | Captures persistence claims for verification. |
| `api-death-shield.py stop` | Closer | Saves state on stop. |
| `proposal-scraper.py` | Closer | Scrapes proposals surfaced during the turn. |
| `parallel-issues-detector.py` | Closer | Detects parallel issues raised in the turn. |
| `phone-ping.py` | Closer | Calendar phone ping when a run finishes or input is needed. |
| `wwwd-correction-detector.py` | Closer | Detects a Will correction and folds it into the WWWD corpus. |
| `autonomous-continue.py` | Gate | Scans pending work signals to decide whether to continue. |
| `context-rotation-hook.py` | Closer | 500k-token handoff threshold check; writes the mechanical handoff floor. |
| `runtime-heartbeat.py stop` | Closer | Runtime liveness heartbeat. |
| `refresh-session-state-toppriority.py` | Closer | Refreshes the top-priority handoff block. |
| `commit-push-checkpoint.py` | Closer | Captures orphan commits at session end. |
| `handoff-chain-stop.py` | Closer | Seals the newest handoff into the experience chain and backs it up to at least two nodes. |

### PreCompact and PostCompact (compression survival)

| Hook | Event | Role | What it does |
|---|---|---|---|
| `api-death-shield.py pre-compact` | PreCompact | Closer | Syncs the chain before compression. |
| `precompact-persistence-snapshot.py` | PreCompact | Closer | Snapshots persistence state before compaction. |
| `postcompact-reload.py` | PostCompact | Loader | Reloads state after compaction. |

### StopFailure

| Hook | Role | What it does |
|---|---|---|
| `api-death-shield.py stop-failure` | Closer | Saves state on an API error that kills the turn. |

### PostToolUse (persistence and follow-through)

| Hook | Matcher | Role | What it does |
|---|---|---|---|
| `auto-checkpoint.py` | Edit, Write, Bash, NotebookEdit | Closer | Auto-checkpoints after a mutating call. |
| `autosnapshot.py` | Edit, Write, NotebookEdit | Closer | Persistence autosnapshot. |
| `research-tool-call-logger.py` | all | Closer | Logs research tool calls. |
| `_outcome_recorder.py` | Write, Edit | Closer | Tags whether the next edit to a target acted on or ignored a gate warning, building per-gate strength and confidence evidence. |

---

## Hard triggers (the law layer, 2026-10-19)

Measured on 2026-10-19: of 97 registered hooks, 88 only inject text and 9 can block. Text decays, because it competes for attention in a large context and the weights never change. A hard trigger either performs the action itself or blocks until a mechanical condition holds, has a canary that proves it still works at every boot, and is locked so the model cannot edit it without a human unlock.

| Gate | Event / matcher | What it does |
|---|---|---|
| `inner-dialogue.py` | PostToolUse Write, Edit (drafts, write-ups, docs, session notes) | Quotes the weakest sentences of the text just written back as generative pushback questions from a growing bank (concede: "why accept this instead of closing it?", unclear, absolute, attack, hedge) and records them as open. |
| `inner-dialogue-stop.py` | Stop | Refuses to end the turn while pushback questions are open; they close only when the file is revised or a reason is logged. Capped so a broken loop cannot wedge a session. |
| `hard-lock.py` | PreToolUse Write, Edit, Bash | Denies model edits to the hard-trigger files and settings edits that would drop their registration; the files are also OS read-only. Only a human opens a 30-minute unlock window, from their own terminal. |
| `canary.py` | SessionStart | Runs every hard trigger on canned inputs (the inner-dialogue check replays the real pushback that motivated it), checks registration, re-locks an expired unlock window, and prints one alive-or-DEAD line at boot. |

---

## Why this file exists

The README makes the case for gates and shows a few. `ARCHITECTURE.md` counts them. Neither lists them, and an un-listed gate is one nobody can verify still fires, still matches the right tool, or still means what its name claims. This registry closes that gap: it is the layer's self-audit surface, the thing you diff against `settings.json` to catch a gate that silently fell out of the config or a script that lingers on disk with no registration.

The deeper reason is the one the README already states and this file makes checkable: any rule that must fire regardless of attention belongs here, not in memory. Memory is `O(context) × O(sessions)`. A gate is `O(1) × O(∞)`. You can only trust that trade if you can see the whole set.

See the [README](README.md) for the philosophy, [Layer 3](../03-anti-hallucination/) for the worked anti-hallucination gates, and [ARCHITECTURE.md](../ARCHITECTURE.md) for where Layer 1 sits under everything else.
