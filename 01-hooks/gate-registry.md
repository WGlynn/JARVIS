# Layer 1 — The complete gate registry

> The README explains why gates exist and lists a handful as examples. This file enumerates every one, because a discipline you cannot list is a discipline you cannot audit.

Source of truth is `~/.claude/settings.json`. Every entry below is a live, registered hook, except rows whose role is OS task, Cron or Reader: those are scripts the hooks and crons drive, listed here so the whole surface is in one place. Each is deterministic: regex, a context window, a watch list, a state machine. No LLM call, no probabilistic judgment. They fire regardless of whether the model remembers the rule in any given session, which is the whole point (`1 → ∀`: gates fire orthogonal to context, and every layer above assumes they hold).

Read the three roles before the tables:

- **Gate** blocks or warns on a tool call before or after it runs. This is what "gate" means in the strict sense, and these are the enforcement surface.
- **Loader** injects state or context at a lifecycle moment. It does not block; it makes the model see something it would otherwise miss.
- **Closer** fires when a turn or session ends, to persist state, capture drift, or continue a loop.

Count as of 2026-11-17: **101 distinct hook scripts** are registered across eight lifecycle events, verified by [`registry-drift-check.py`](registry-drift-check.py). Several fire on more than one event (`api-death-shield`, `atomic-reflection-gate`, `runtime-heartbeat`), so the total invocation count is higher still. Run the drift check to re-verify this against `settings.json` at any time: a registry that silently drifts from the live config fakes the confidence every layer above assumes, so the registry is now self-checking rather than a one-time human enumeration.

Every row was re-checked against the live code on 2026-11-17, after an audit of the whole stack. Where a row claimed a block, a guarantee or a delivery the code does not give, it now says what the code does. Two facts recur below. First, all hooks on one event run in parallel, so registration order does not set the order their output appears in. Second, the harness swaps any single hook output over about 10,000 characters for a 2 KB preview plus a file path (the "hook output cap"), so hooks that can produce long output now cap themselves at 7,500 characters.

---

## Enforcement gates (the strict sense: block or warn on a tool call)

These are the ones that actually stop or flag an action. If you only read one table, read this one.

### PreToolUse

| Gate | Matcher | What it does |
|---|---|---|
| `wwwd-gate.py` | Write, Edit, Agent | Keyword-triggered reminders: severity wording in context, tone, scope, partner-facing paths, and agent prompts that name 3 or more files. The partner-facing and read-order reminders fire once per session. Advisory, never blocks. This row used to describe a Will-emulation that projects a correction; the code has none, and no corpus recall. The excerpt it logs has protected terms masked (2026-11-17). |
| `partner-facing-substance-gate.py` | Write, Edit | Claim-handshake on writes in partner repos. On terminology overclaim (e.g. forfeiture vs clawback, governance overreach) it returns "ask", a confirmation prompt, not a block. What "ask" does under the bypass permission mode has not been checked live. |
| `partner-architecture-load-gate.py` | Write, Edit, Agent | Loads partner-specific anti-hallucination guards before a partner-facing write. Advisory. Output is capped at 7,500 characters on a line boundary and ends with the files to read for the rest (2026-11-17; with two or more partners it used to hit the hook output cap, so the guards never arrived). |
| `entity-context-cross-reference.py` | Write, Edit | AA#3 / CCP. On long writes that look like entity lists (outreach drafts, target lists), surfaces the memory lines that mention the named entities, so they can be reconciled before delivery. Advisory. Skips code and data files and mirror copies. A case-sensitivity bug behind most of its fires was fixed 2026-11-17. |
| `conflict-detector.py` | Write, Edit | Warns when a draft uses an entity positively that memory marks as abandoned, deprecated, compromised or rejected. Advisory. Until 2026-11-17 it never read the draft's stance and counted any nearby "not" or "no" in memory as a contradiction. |
| `hiero-gate.py` | Write, Edit (memory) | Readability nudge. Rewritten 2026-07-20 when the HIERO glyph format was retired: it never blocks, and it suggests plain words when a memory write leans on glyph shorthand (plus a frontmatter note on a Write of a topic file). Lives in `session-chain/`; the old file name is kept so the wiring did not change. Until 2026-11-17 the nudge went to stderr, which the model never sees, so it reached nobody. |
| `time-logic-gate.py` | Write, Edit, Agent | Scans for unanchored temporal claims (relative dates, stale "now"). |
| `directive-verb-action-class-gate.py` | Write, Edit, Agent | Warns when a write to an essay-class path (layer essays, including this repo's) follows a directive classified as implementation, so the response class matches the ask. Advisory. Until 2026-11-17 its transcript walker read tool results as the directive and could not fire. It can now, but most directives classify as ambiguous, so it rarely does. |
| `jarvis-design-goal-gate.py` | Write, Edit, Agent | Injects the Stark-JARVIS design-goal test before a write to an architecture path (layer essays; this repo's README, ARCHITECTURE, LAYERS and CONSTITUTION; settings.json). Advisory. Until 2026-11-17 it watched only a retired repo, so it never fired. |
| `research-before-capability-claim-gate.py` | Write, Edit | AA#4. Warns on product-capability claims in a partner draft (`Desktop/People/`, `*-reply-*`) when no research call ran in the last 30 minutes. Advisory, never blocks. |
| `compression-claim-verification-gate.py` | Write, Edit | Anchor check on any compression or ratio claim. |
| `strategic-framing-filter.py` | Write, Edit | Blocks a write to a named external-audience report folder or file when it contains private strategic-framing language meant to stay internal; a reviewed-false-positive marker lets it through. Its watched paths were fixed 2026-11-17: the folders had moved, and it had not scanned them since. |
| `discretion-flag-warn-gate.py` | Write, Edit | Warns on a memory write that carries a discretion flag: git history on a public remote still keeps the pre-flag text. Advisory. Since 2026-11-17 it also says the public substrate sync is dormant, so nothing is excluded or deleted automatically. |
| `memory-budget-gate.py` | Write, Edit | Warns when a write would push MEMORY.md over its self-set size budget. Advisory. MEMORY.md is not truncated when it goes over; the gate suggests shorter bullets, because moving rules into sub-indexes takes them out of the one file the model reads whole. |
| NDA git-scrub gate | Bash (git *) | Scans every git commit, push and add in a Bash command, in the repo it will really run in, for protected terms. Blocks on a hit, and also blocks when it cannot resolve the repo or finish the scan in time. A push is scanned commit by commit against what the target remote lacks. Rewritten 2026-11-17: before, a leading `cd` was the only path form it honored, so some operations were scanned in the wrong repo. |
| `partner-facing-additive-gate.py` | Bash (push, PR) | Scans push and PR text for retrospective keywords that leak internal error narrative. |
| `foundry-test-gate.py` | Bash | Blocks an unscoped `forge test` (OOM guard on constrained hardware). |
| `resource-cgroup-gate.py` | Bash | Denies a heavy build spawn when running heavy processes (forge, cargo, rustc, node) are at the cap, and logs each denial. It counts cargo and rustc since 2026-11-17; before, Rust builds were invisible to it. One full-parallel cargo build can reach the cap by itself. |
| `coordination-mechanism-gate.py` | Agent, Workflow | Advisory. On an Agent spawn, classifies it for a cost-tier recommendation (a spawn with no model set is noted as inheriting the parent's model, not scored). On a Workflow spawn, emits the execute-to-verify / size-to-artifact / ultracode-floor pre-check, so the deterministic cheap check is considered before an N-agent swarm. |
| `atomic-reflection-gate.py` | Agent, and all PostToolUse | Reminds (does not enforce) to capture the lesson before routing around a problem. On an Agent spawn it fires only when the spawn looks like routing around a failure (the last tool result was an error, or the prompt says a prior attempt failed); it used to fire on every spawn. On PostToolUse it fires after an error or timeout, which is rarely reached, because failed calls go to the PostToolUseFailure event; the script handles that event but is not registered for it yet. |
| `autopilot-allow.py` | all | Autopilot permission handling: a conditional allow keyed on a flag file. A no-op today (no flag file, and the permission mode already skips prompts) that still costs one process per tool call. |
| `entity-attribution-gate.py` | Write, Edit | Catches invented @handles: an @handle in an attribution context must match a known record, or the write is flagged. |
| `oversell-gate.py` | Write, Edit | Flags hype, overclaimed maturity or capability, and unqualified stats when no honest-floor caveat balances them. |
| `_solver_gate_hook.py` | Bash | Advisory Z3 check of the same concurrency cap as `resource-cgroup-gate.py`, adding the via_ir memory weight for a proposed build. It never blocks, and it reads the same process counts as the resource gate, so it adds no protection beyond that weight. |

### PostToolUse

| Gate | Matcher | What it does |
|---|---|---|
| `em-dash-augmentation-gate.py` | Write, Edit, NotebookEdit | Partner-draft gate, 3 axes (2026-07-29): (1) em/en-dash scrub; (2) de-model tells from `model-tells.json` (growing corpus, appendable without code change) + an always-injected de-model checklist; (3) source-grounding, flags partner-facing technical drafts that assert protocol/mechanism behavior but cite no source (EIP/spec/URL/file:line). Augmentation, not block. Since 2026-11-17 it also covers drafts in `Desktop/People/<Name>/` (not STATE.md or THREAD.md) and reads its input as UTF-8; before, a decoding bug meant it never counted a single em dash. |
| `code-mode-nudge.py` | Bash, Read, Grep, Glob | Counts same-tool calls per session (per subagent inside one) in a 120 s window and, at the threshold, nudges toward a single script, then cools down. |
| `git-commit-landed-gate.py` | Bash, Read, Grep, Glob | Reminds to verify that a commit landed. It fires on a `git commit` with no success line only when git shows HEAD did not advance during the run, and on every backgrounded commit. Advisory. Before 2026-11-17 most of its fires were quiet `commit -q` runs that had landed. |
| `wp-dated-doc-reminder.py` | Write, Edit, NotebookEdit | When the Noesis whitepaper source is edited, reminds to rebuild it with the build script, which writes a new dated PDF instead of overwriting a fixed file name. At most once per 20 minutes per session. |
| `coherence-gate.py` | Edit, Write, Bash, NotebookEdit | Derived-facts check (2026-10-13): when a watched source file changes, runs that project's drift check from `~/.claude/coherence/registry.json` and injects the fix command on failure. Advisory. |

---

## Full registry by lifecycle event

### SessionStart (boot loaders and integrity checks)

| Hook | Role | What it does |
|---|---|---|
| `memory-sync-pull.py` | Loader | Fetches the memory repo and fast-forwards it when origin is ahead and the tree is clean; warns only when origin is ahead and the pull had to be skipped. It runs in parallel with the other loaders, so it cannot promise they read post-pull state. |
| `session-state-loader.py` | Loader | Injects only the AUTO-HANDOFF header of `SESSION_STATE.md` (top priority, context size, latest directive), capped at 40 lines; the handoff body comes from `handoff-first.py`. Warns if the block is missing. Until 2026-11-17 it injected up to 140 lines labelled "mandatory first read", including superseded blocks. |
| `private-handoff-loader.py` | Loader | Binds an active private-workstream handoff to the boot path. Handoff files not modified in 30 days count as inactive and are skipped. |
| `wal-state-loader.py` | Loader | Reports `WAL.md` status: one line per WAL with its last-written date when CLEAN, the full body only when a title says ACTIVE. Nothing writes WAL epochs any more, so ACTIVE appears only if set by hand. |
| `rsi-pending-check.py` | Loader | Counts real `[PENDING]` loop headers in the recursive-self-improvement project file. Silent at zero; when the file is over 30 days old it marks the loop dormant. It used to report "7 loops pending" every boot from substring matches. |
| `link-rot-detector.py` | Gate | Checks memory and hook path integrity; flags protocol-chain rot. |
| `clock-session-start.py` | Loader | Records session-start time. |
| `memory-preprocessor.py` | Loader | L2. Injects `MEMORY_INDEX_PREFLIGHT.md` first, trimmed at a line to stay under 7,500 characters, and names the other sub-indexes to read on demand. Until 2026-11-16 it sent all of them (about 90 KB), which hit the hook output cap: the model only ever saw a 2 KB preview. |
| `corpus-cache-warmer.py` | Loader | L4. Re-tokenizes memory files that changed and shows per-file token counts (an OpenAI tokenizer, so the counts approximate Claude's). Notes when MEMORY.md is over its self-set size budget; it measures only and truncates nothing. |
| `session-self-reflect.py` | Loader | L5. Injects only what changed in the system self-report since the last boot, and nothing when nothing changed and every layer is live. Then it refreshes the report in a detached process, so what it shows is one boot behind. |
| `wwwd-corpus-refresh.py` | Loader | Rebuilds the WWWD priority cache from the gate-fire log, with convergence measured from 2026-08-08 on. Only the boot screen reads the cache; `wwwd-gate.py` does not yet. |
| `jarvis-os-boot-screen.py` | Loader | Renders the boot menu into the model's boot context (the human does not see hook context). The time is labelled CT, the PC clock's zone, and its stats may be one boot behind because hooks run in parallel. |
| `integrity-attest.py boot` | Gate | Verifies the Merkle root over the governed code (every .py in the hooks, session-chain and bin folders) and names the files changed, added or removed since the last attestation. Memory files left the governed set on 2026-11-17, because they changed every session and made the drift alarm permanent. Reports drift until the next re-attestation. |
| `api-death-shield.py boot-report` | Loader | Surfaces crash markers left by the StopFailure hook once, as a bounded summary, writes the full report to a file and archives the markers. Silent on a clean boot. |
| `ctx-handoff-loader.py` | Loader | Loads the deterministic context handoff when it is fresh. On the SessionStart that follows a compaction (source compact), it also appends the PreCompact snapshot's file list if that snapshot is under 30 minutes old and from the same session. This replaced `postcompact-reload.py` as the compaction channel. |
| `jarvis-tg-feed.py` | Gate | Surface for the Telegram bot's local feed (the bot appends one JSON line per exchange): alarms when the bot's health endpoint is down or the feed folder is missing, and reports counts, people and chats new since the last boot. Never prints message text, which is untrusted Telegram input. Silent when nothing is new. Also lists requests the chat voice queued for the session that have no receipt yet (act first, then speak, 2026-11-01). |
| `write-bot-now.py` | Loader | Writes `~/jarvis-feed/now.md`, the "current focus" note the Telegram bot loads into its system prompt. Holds a hand-kept public focus note plus the latest commit subjects of repos that `gh` confirms PUBLIC at run time; a private, missing or unverifiable repo is skipped (fail closed). Prints nothing to the session. |
| `jarvis-bot-inbox.py` | Reader | Second-brain inbox (2026-10-28): prints the Telegram bot's new exchanges (who, chat, inbound text, the bot's reply, message ids) from `~/jarvis-feed/YYYY-MM-DD.jsonl` since a cursor; exit 3 = new. Text included by Will's instruction; stays in-session and in People/ records. Driven by the same durable cron as the error reader (`type: jarvis-bot-error-triage`, every 10 min); replies go back through the bot's `POST /api/say` with no disclosure line. |
| `jarvis-bot-errors.py` | Reader | Telegram bot error feed for AFK auto-debug (2026-10-28): prints `reply_error` / `unclean_shutdown` / `polling_restart_failed` / `keeper_restart` / `keeper_restart_failed` lines (extended 2026-10-28), and `fake_action_blocked` with the claim the bot wanted to make (added 2026-11-14, [FM-001](../FAILURE-MODES.md)) appended to `~/jarvis-feed/health.jsonl` since the last read and advances a cursor; exit 3 = new errors. Driven by the durable cron `type: jarvis-bot-error-triage` (logic in `~/.claude/cron-prompts/jarvis-bot-error-triage.md`), which fixes root causes behind the test-gated restart. Never prints user message text. |
| `jarvis-bot-keeper.py` | OS task | Keeps the Telegram bot alive on the local PC (2026-10-28): OS task `JARVIS-BotKeeper` every 5 min; if the pid in `~/jarvis-bot-logs/pid.txt` is not a live node process (confirmed twice, 30s apart, so a planned restart's gap is ignored), runs the test-gated `scripts/restart-local.ps1` and records `keeper_restart` / `keeper_restart_failed` in `~/jarvis-feed/health.jsonl`. At most one attempt per 10 min; `~/.claude/state/jarvis-bot-keeper.off` stands it down. Covers the bot's 8 `process.exit(1)` paths, which assumed a cloud restart policy. |
| `write-bot-repos.py` | Cron | Writes `~/jarvis-feed/repos.md` so the bot knows the latest public state of the repos its chats talk about (latest release, newest commits, and for Noesis the README head and ARCHITECTURE headings). Each repo is checked PUBLIC via `gh` on every run. Run by the `jarvis-bot-error-triage` cron every 10 minutes. |
| `handoff-first.py` | Loader | Fires on every window boundary (startup, resume, clear, compact) and injects the head of the newest handoff, capped at 7,500 characters (2026-08-12). It is registered at index 0, but that does not make it first: SessionStart hooks run in parallel and their output is ordered by finish time, so it usually lands first only because it is fast (in the 2026-11-16 audit another hook came first in 9 of 24 boots). A guaranteed first would need a single boot assembler. |
| `handoff-save-check.py` | Gate | Cross-repo save check: flags repos with uncommitted or unpushed work the last handoff may not describe. Machine commits and hook telemetry no longer count as at-risk work, and "unpushed" means on no remote at all. Also lists repos the commit-push leak guard has blocked for more than 24 h, and notes when the newest dated note in `BOOT-MESSAGE.md` is older than the newest handoff. |
| `skb-drift-witness.py` | Gate | Keeps the shared knowledge base (SKB, the stable core loaded every session) changing with the state it describes (2026-11-17). Each SKB section ends with "Source (as of date): paths". At boot it flags a cited path that no longer exists, a section whose Source file changed after its as-of date once that date is a week old, and a section not re-verified in 90 days. It also keeps one copy of each distinct SKB version in the memory repo, so the SKB has a history. Silent when nothing drifted; fails loud if the SKB is missing. Built after the previous SKB went stale unnoticed for months. |
| `chain-health-witness.py` | Gate | Reports experience-chain HEAD, walk-back integrity to genesis, and remote backup state. |
| `chain-liveness-check.py` | Gate | Alarms when the session chain stops advancing. |
| `index-budget-witness.py` | Gate | Notes when MEMORY.md is over its self-set size budget (24,400 bytes); the file is not truncated and still loads whole. It also watches the real limit, the hook output cap: it warns when `memory-preprocessor.py`'s last output nears 10,000 characters, and lists every hook output the harness cut to a preview since the last boot. |
| `cron-productivity-witness.py` | Gate | Flags registered crons whose fire heartbeat or real output file has gone stale. Since 2026-11-17 each live cron is mapped to the file its body actually writes; before, the output check was blind for all of them. |
| `os-task-freshness-witness.py` | Gate | Checks the logs of the OS-scheduled persistence tasks (git autosave and friends) for staleness. |
| `autosave-daemon-witness-check.py` | Gate | Staleness check for the separate autosave daemon process. |
| `crash-backtest-witness-check.py` | Gate | Staleness check for the crash-recovery backtest witness stamped by an OS scheduler. |
| `wwwd-correction-capture-witness.py` | Gate | Alarms when WWWD corrections stop landing in the gate-fire log (the self-compounding loop depends on it). |

### UserPromptSubmit (per-prompt injectors and gates)

| Hook | Role | What it does |
|---|---|---|
| `inbox-capture.py` | Gate | Two-way protocol, inbound side (2026-11-01). Blocks a message that carries a key shape before the model sees it and says to rotate it (Constitution 2.4; `#allow-secret` overrides); writes every message to `~/.claude/state/inbox/` the moment it is sent; starts `inbox-prep.py` detached so the queue wait becomes prep time. Hooks run in parallel, so the block cannot stop sibling hooks from reading the prompt; `wwwd-prompt-buffer.py` redacts key shapes itself. Since 2026-11-17, machine prompts (cron pointers, task notifications, compaction summaries) are logged as skipped instead of captured, using a machine-prompt check shared by the prompt hooks. That check goes by text shape, because the harness does not yet send a prompt-source field. |
| `clock-injector.py` | Loader | Injects the current clock. |
| `api-death-shield.py user-prompt` | Closer | Logs each prompt so the human side survives an API failure mid-turn. Key shapes are redacted before the write (2026-11-17). |
| `session-directive-forcer.py` | Gate | First-turn boot-directive application check. A machine prompt no longer uses up the once-per-session frame. |
| `memory-warm-loader.py` | Loader | Loads situation-matched `MEMORY_WARM_*` files, capped at 7,500 characters; a file that does not fit is cut at a line or named with its path to read. Skips machine prompts. |
| `deep-recall.py` | Loader | TF-IDF match of the prompt against the memory index (lexical overlap, not semantic understanding), with the index build date in its header. Skips machine prompts. The index is rebuilt daily by the memory corpus-push task since 2026-11-17; before that it had been frozen since August. |
| `archive-recall.py` | Loader | Surfaces prior work-product matching the prompt: whole-word matches over the archive index, a higher threshold since 2026-11-17, and the newest indexed date in its header. Skips machine prompts. |
| `post-generation-recall.py` | Loader | L4 recovery. Delivers the reflection `post-generation-reflect.py` wrote at the last Stop, one turn late, framed as "correct it now". Machine prompts leave it undelivered for the next real prompt. |
| `thread-resume-detector.py` | Loader | Scans open threads for a prompt match. Skips machine prompts. |
| `triad-check-injector.py` | Gate | Injects the Correspondence Triad on design-level questions. Narrower trigger words since 2026-11-17; ignores quoted lines and skips machine prompts. |
| `save-session-state-trigger.py` | Closer | Save-state trigger check. Skips machine prompts. |
| `partner-draft-formalize-gate.py` | Gate | Detects partner-draft intent and reminds the model to save the draft to disk (in `People/<Name>/` when a record exists) before the chat output. Advisory. Skips machine prompts. |
| `partner-thread-loader.py` | Loader | When a prompt names someone with a conversation record (People/<Name>/THREAD.md + STATE.md), injects their state and recent thread, once per session, so replies after a /clear keep full context (2026-10-19). Since 2026-11-17: output capped at 7,500 characters, with a "read the rest" line per cut record; machine prompts and handoff or `~/.claude` paths load and copy nothing. |
| `anticipation-hook.py` | Loader | Date-anchored items, stale PENDING threads, and memory files deep-recall surfaced 3 or more times in 24 h (it does not measure whether they were acted on). The same set is shown once per session. Skips machine prompts. |
| `story-mode-gate.py` | Gate | Story Mode menu enforcement and number-reply interpretation. |
| `runtime-heartbeat.py user-prompt` | Closer | Runtime liveness heartbeat. |
| `wwwd-prompt-buffer.py` | Loader | Buffers the current prompt so the Stop-time WWWD correction detector can read it. The buffer is tracked in the memory repo, so key shapes are redacted first (2026-11-01). A machine prompt is buffered empty and flagged, so it can never count as a correction. |
| `oversell-primer.py` | Gate | One-line "teammate, not salesman" tripwire every turn (conversational twin of `oversell-gate.py`); machine prompts get a shorter line. |
| `deep-context-mode-activator.py` | Loader | Past 500k tokens, injects the deep-context behavior switch so the model manages its own context. Since 2026-11-17 it measures context from the transcript, so a session that compacted back under 500k is no longer told it is past the line by a stale marker. |
| `cron-fire-heartbeat.py` | Gate | Records cron-injected prompts as fire evidence for the cron productivity witness. |

### Stop (end-of-turn closers and gates)

| Hook | Role | What it does |
|---|---|---|
Stop fires at the end of every response, not only when a session closes, and most responses on this machine are cron turns. Read "turn end" below in that sense. Since 2026-11-17 the self-review, reflection, claim-capture, proposal and voice hooks read only the last 2 MB of the transcript, instead of the whole file on every Stop.

| Hook | Role | What it does |
|---|---|---|
| `voice-summary.py` | Closer | Speaks a one-sentence summary of each finished turn with Windows' built-in offline voice; nothing leaves the machine. This includes cron turns. Off switch: create `~/.claude/voice-off`. |
| `story-loop-continue.py` | Closer | Story Mode autonomous self-play continuation. |
| `self-review-gate.py` | Gate | Blocks the Stop, at most once per turn, when the turn since the last real human prompt shows a known failure class (for example an essay where implementation was asked for, or a denial with no search). Until 2026-11-17 two of its three checks could not fire and the third fired only on false positives. |
| `post-generation-reflect.py` | Closer | L4. Matches the finished reply against the memory index and writes high-relevance hits to a file; `post-generation-recall.py` delivers them on the next prompt. It injects nothing itself. |
| `decision-capture.py` | Closer | Disabled in code since 2026-11-17 (returns at once): 0 captures in 444 eligible outputs over 14 days. Still registered until it is removed from settings. |
| `persistence-claim-capture.py` | Closer | Logs persistence self-claims ("saved", "I won't forget"). Nothing verifies them today: the sweep cron meant to reconcile them has not run since 2026-08-12. |
| `api-death-shield.py stop` | Closer | Saves state on stop. |
| `proposal-scraper.py` | Closer | Scrapes proposals surfaced during the turn. |
| `parallel-issues-detector.py` | Closer | Disabled in code since 2026-11-17 (returns at once): it read one transcript line per check, and each tool call sits on its own line, so it could never see parallel calls. Still registered until it is removed from settings. |
| `phone-ping.py` | Closer | Dead. Meant to email a phone notification when a run finishes or input is needed, but its credentials file has never existed, so it has never sent one. It now logs one notice and returns; phone pings are sent another way. |
| `wwwd-correction-detector.py` | Closer | Keyword heuristic: when the prompt matches a correction pattern ("no" at the start, "actually", ...), tags the most recent WWWD gate fire from the last 30 minutes. Automation prompts are skipped since 2026-11-17; before that, most stamped "corrections" were cron text. |
| `autonomous-continue.py` | Gate | Disabled in code since 2026-11-17 (returns at once): all four of its pending-work signals were dead or pointed at the wrong place, and it blocked rather than advised. Still registered until it is removed from settings. |
| `context-rotation-hook.py` | Closer | 500k-token handoff threshold check; writes the mechanical handoff floor. |
| `runtime-heartbeat.py stop` | Closer | Runtime liveness heartbeat. |
| `refresh-session-state-toppriority.py` | Closer | Refreshes the top-priority handoff block. |
| `commit-push-checkpoint.py` | Closer | Starts the commit-push worker in the background (throttled); the worker leak-scans, commits and pushes. A repo whose pending changes match the leak patterns is skipped on every run until a human clears it. Since 2026-11-17 those blocks are recorded in a state file that `handoff-save-check.py` reports at boot; before, they went unnoticed for months. |
| `handoff-chain-stop.py` | Closer | Seals the newest handoff into the experience chain and backs it up to at least two nodes. A no-op when the newest handoff is unchanged. |

### PreCompact and PostCompact (compression survival)

| Hook | Event | Role | What it does |
|---|---|---|---|
| `api-death-shield.py pre-compact` | PreCompact | Closer | Syncs the chain before compression. |
| `precompact-persistence-snapshot.py` | PreCompact | Closer | Writes the names of memory files written in the last two days to a snapshot file before compaction. `ctx-handoff-loader.py` re-injects that list on the SessionStart that follows. Emits nothing itself. |
| `postcompact-reload.py` | PostCompact | Loader | No effect. It prints a reload block, but the harness drops PostCompact additionalContext (0 deliveries in any transcript, 2026-11-16 audit). The snapshot now reaches the model through `ctx-handoff-loader.py`. Still registered until it is removed from settings. |

### StopFailure

| Hook | Role | What it does |
|---|---|---|
| `api-death-shield.py stop-failure` | Closer | Writes a crash marker and finalizes the chain when an API error kills the turn; the boot report surfaces the marker at the next start. Its auto-commit step was retired on 2026-11-17. |

### PostToolUse (persistence and follow-through)

| Hook | Matcher | Role | What it does |
|---|---|---|---|
| `auto-checkpoint.py` | Edit, Write, Bash, NotebookEdit | Closer | Auto-checkpoints after a mutating call. Its git sync was a no-op (the target is gitignored) and is off since 2026-11-17. |
| `autosnapshot.py` | Edit, Write, NotebookEdit | Closer | Starts a persistence snapshot in a detached process at most once every 6 hours and returns at once. Before 2026-11-17 it ran the snapshot inline, hit its 20 s timeout on every edit, and wrote no snapshot after 2026-07-30. |
| `research-tool-call-logger.py` | all | Closer | Logs research tool calls. |
| `inbox-deliver.py` | all | Loader | Two-way protocol (2026-11-01): hands the model any prep `inbox-prep.py` finished for this session's queued messages, at the tool boundary where queued messages land; each prep is delivered once (atomic rename) and expires after 20 minutes. `inbox-prep.py` is the background worker it reads from (deterministic: message kind, standing-rule words, references resolved, handoff items and memory lines it touches; no model calls). Also hands over requests the chat voice queued for the session (`_session_requests.py`), each claimed by one session; `session-receipt.py <id> done|declined "..."` writes the receipt the bot confirms from. Inside a subagent it does nothing, so a subagent never claims the main session's prep. |
| `_outcome_recorder.py` | Write, Edit | Closer | Tags whether the next edit to a target acted on or ignored a gate warning, judged against the whole file after the write, building per-gate strength and confidence evidence. Known gap: telemetry rows carry no session id, so a parallel session's warning can be misattributed. |

---

## Hard triggers (the law layer, 2026-10-19)

Measured on 2026-10-19: of 97 registered hooks, 88 only inject text and 9 can block. Text decays, because it competes for attention in a large context and the weights never change. A hard trigger either performs the action itself or blocks until a mechanical condition holds, has a canary that proves it still works at every boot, and is locked so the model cannot edit it without a human unlock.

| Gate | Event / matcher | What it does |
|---|---|---|
| `inner-dialogue.py` | PostToolUse Write, Edit (drafts, write-ups, docs, session notes) | Quotes the weakest sentences of the text just written back as generative pushback questions from a growing bank (concede: "why accept this instead of closing it?", unclear, absolute, attack, hedge) and records them as open. |
| `inner-dialogue-stop.py` | Stop | Refuses to end the turn while pushback questions are open; they close only when the file is revised or a reason is logged. Capped so a broken loop cannot wedge a session. |
| `hard-lock.py` | PreToolUse Write, Edit, Bash | Denies model edits to the hard-trigger files and settings edits that would drop their registration; the files are also OS read-only. The 30-minute unlock window is meant to be opened only by a human from their own terminal. The 2026-11-16 audit found the code does not yet fully enforce that, and that its shell check over-blocks the inner-dialogue acknowledge command; the fix touches a locked file and waits on a human unlock. |
| `canary.py` | SessionStart | Runs every hard trigger on canned inputs (the inner-dialogue check replays the real pushback that motivated it), checks registration, re-locks an expired unlock window, and prints one alive-or-DEAD line at boot. |

---

## Why this file exists

The README makes the case for gates and shows a few. `ARCHITECTURE.md` counts them. Neither lists them, and an un-listed gate is one nobody can verify still fires, still matches the right tool, or still means what its name claims. This registry closes that gap: it is the layer's self-audit surface, the thing you diff against `settings.json` to catch a gate that silently fell out of the config or a script that lingers on disk with no registration.

The deeper reason is the one the README already states and this file makes checkable: any rule that must fire regardless of attention belongs here, not in memory. Memory is `O(context) × O(sessions)`. A gate is `O(1) × O(∞)`. You can only trust that trade if you can see the whole set.

See the [README](README.md) for the philosophy, [Layer 3](../03-anti-hallucination/) for the worked anti-hallucination gates, and [ARCHITECTURE.md](../ARCHITECTURE.md) for where Layer 1 sits under everything else.
