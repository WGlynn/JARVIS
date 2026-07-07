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
| `coordination-mechanism-gate.py` | Agent | Classifies an agent spawn for a cost-tier recommendation before it runs. |
| `atomic-reflection-gate.py` | Agent, and all PostToolUse | Forces a reflection at a delegation or after an error/timeout, so the lesson is captured before routing around it. |
| `autopilot-allow.py` | all | Autopilot permission handling. |

### PostToolUse

| Gate | Matcher | What it does |
|---|---|---|
| `em-dash-augmentation-gate.py` | Write, Edit, NotebookEdit | Scans partner-facing drafts for em and en dashes and surfaces a scrub warning. Augmentation, not block. |
| `code-mode-nudge.py` | Bash, Read, Grep, Glob | Detects repeated tool round-trips and nudges toward a single script. |
| `git-commit-landed-gate.py` | Bash, Read, Grep, Glob | Confirms a claimed commit actually landed. |
| `wp-dated-doc-reminder.py` | Write, Edit, NotebookEdit | Reminds to date partner-facing docs. |

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
| `anticipation-hook.py` | Loader | Date-anchored, stale-PENDING, and unactioned-recall scan. |
| `story-mode-gate.py` | Gate | Story Mode menu enforcement and number-reply interpretation. |
| `runtime-heartbeat.py user-prompt` | Closer | Runtime liveness heartbeat. |

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

---

## Why this file exists

The README makes the case for gates and shows a few. `ARCHITECTURE.md` counts them. Neither lists them, and an un-listed gate is one nobody can verify still fires, still matches the right tool, or still means what its name claims. This registry closes that gap: it is the layer's self-audit surface, the thing you diff against `settings.json` to catch a gate that silently fell out of the config or a script that lingers on disk with no registration.

The deeper reason is the one the README already states and this file makes checkable: any rule that must fire regardless of attention belongs here, not in memory. Memory is `O(context) × O(sessions)`. A gate is `O(1) × O(∞)`. You can only trust that trade if you can see the whole set.

See the [README](README.md) for the philosophy, [Layer 3](../03-anti-hallucination/) for the worked anti-hallucination gates, and [ARCHITECTURE.md](../ARCHITECTURE.md) for where Layer 1 sits under everything else.
