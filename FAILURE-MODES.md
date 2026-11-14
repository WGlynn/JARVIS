# Failure modes we have actually hit

Real failures from running JARVIS: a Claude Code harness and a Telegram bot that share one memory and one set of rules. Each entry says what happened, how it was found, why the safeguards already in place missed it, what was fixed, what was not, and the class of failure it belongs to. A failure someone actually hit, with its evidence, teaches more than a hypothetical one, so this log keeps them. Entries describe events without quoting private chats.

The hallucination gates have their own taxonomy in [`03-anti-hallucination/failure-mode-taxonomy.md`](03-anti-hallucination/failure-mode-taxonomy.md). This file is the incident log.

Format: one entry per failure, newest first, numbered FM-NNN. "Not fixed" is a required line; leave it empty only if nothing is left.

---

## FM-001: a guard that blocks a false promise replaced it with another one (2026-11-14)

**What happened.** Will sent the bot a link in a private chat, with no instruction. The bot's model drafted a reply saying it had queued a check on the link. The bot has no such queue, so the claim was false. The bot's fake-action guard (`src/action-claims.js`) caught it, logged a `fake_action_blocked` event, and sent its fallback instead: "I can't take actions from this chat on my own. Will's Claude Code session reads it and acts." Two minutes later Will asked the session whether it had seen the link. It had not.

**How it was found.** Will asked. The session then read the bot's health feed and found the blocked event, with the claim the guard had removed.

**Why the safeguards missed it.** Three gaps in series, each harmless alone:
1. **The fallback was itself an unbacked promise.** Nothing handed the request to the session. The session only learns of chat messages from a triage cron that runs every 10 minutes, and only while a session is open. The link arrived about two and a half minutes after one check, so the next was about seven minutes away.
2. **An instruction with no reader.** The triage loop's instructions said to act on `fake_action_blocked` events, but the error reader it runs did not include that kind in what it prints. Three such events had sat in the feed since 2026-11-01, and none had ever reached the session.
3. **The answer would have gone to the wrong place.** The loop's rule for Will's own messages to the bot was to treat them as cues and answer in the terminal. Will was on his phone in the chat, so even a prompt answer would have looked like silence.

**Fixed.**
- The error reader now prints `fake_action_blocked` events with the claim the bot wanted to make (`jarvis-bot-errors.py`).
- The loop now has an exception: when the bot's fallback promised that the session would act, the session does the real thing and answers in that chat; a bare link gets a one-line description and a question about what to do with it.
- The fallback text now says what actually happens: the session checks the chat about every 10 minutes while it is running. Lint clean, 451 tests pass, restarted through the test-gated script (`jarvis-bot/src/action-claims.js`, commit `0c4ee8d3` in WGlynn/vibeswap).

**Not fixed.** Latency is still up to about 10 minutes. A Claude Code session only wakes on a prompt, so the cron interval is the floor unless the interval shrinks. With no session open, nothing picks the request up at all, and the fallback now says so only implicitly ("while it is running").

**Class.** Displaced promise: a guard that removes a false claim must not issue an unbacked claim of its own; its fallback has to be true on its own terms. Second class, unreachable instruction: a rule that says "act on events of kind X" is dead if no reader ever shows X. Check that every instruction has a deterministic path to the agent.

---

## FM-002: the boot handoff named a five-day-old request as the latest directive (2026-11-14)

**What happened.** At the start of a new window, the machine-written top-priority block said the latest directive was a request from 2026-11-09, which had long been handled. The window's real last request, five days later, was "rotate". The block carried an "auto-refreshed" timestamp from that morning, so it looked current. A session acting only on that line would have redone old work.

**How it was found.** The session checked the line against the transcript before acting, found the request's date, and told Will the line was stale. The cause was traced the same day, after a second failure (FM-001) made the pattern worth chasing.

**Why the safeguards missed it.** Three bugs, all in the harness's own handoff code:
1. **The floor stopped updating.** The mechanical handoff (`LATEST.md`) was rewritten only when the context grew by another 50k tokens. A long session whose context stopped growing never crossed that step again, so the file sat five days old.
2. **The newest was read as the oldest.** The floor lists recent turns oldest first. The boot block took item 1, the oldest, and labeled it the latest directive.
3. **The window was too small and too crowded.** The floor scanned only the last 500 KB of the transcript, which one turn with large tool results can fill, and it counted cron pointer prompts as user turns. With a 10-minute cron, those filled the list.

A banner elsewhere in the boot output did print the floor's age (about 116 hours), but nothing tied that age to the directive line. The block's own header said "Mechanical floor is never stale."

**Fixed.** The floor is also rewritten when it is over an hour old; the scan window is 4 MB; cron pointers and hook feedback are skipped; the boot block takes the newest typed turn and prints the floor's age next to the directive when it is over six hours; the false "never stale" line was replaced (`~/.claude/tools/token-audit/context-rotation-hook.py`, `~/.claude/hooks/refresh-session-state-toppriority.py`). Tested on this session's transcript: the floor now lists the last three typed requests and the directive is the newest.

**Not fixed.** The floor still holds only the last few typed turns, not what was done about them, so a request that was answered still reads as open.

**Class.** Freshness by proxy: the floor's refresh was tied to a proxy (context growth) that usually moves with time but can stop. Also an inverted index (oldest read as newest), and a reassurance in the header ("never stale") that no check enforced.

---

## FM-003: a one-shot retry scheduled inside a session died with the session (2026-11-05, found 2026-11-14)

**What happened.** On 2026-11-05 the Cadence monitor loop built a small, clearly correct test fix for an upstream open-source project and tried to open the pull request. GitHub answered 500 and 502 to the fork and PR requests. The loop wrote in its draft note that "a one-shot retry is scheduled in this session" and stopped. Nine days later no PR existed. The monitor's state log also had no rows for 11-05 to 11-13, although at least one pass ran on 11-05 (its probe outputs are on disk).

**How it was found.** The 2026-11-14 monitor pass found an unexplained local branch, searched the drafts folder, and found the note. It opened the PR that day (muellerberndt/cadence#340), rebased and widened to a second test that a later release had added with the same bug.

**Why the safeguards missed it.** The retry lived only in a session, and the session ended. The draft said "scheduled", which read as handled. Later passes did not look in the drafts folder for items marked "not yet opened". Not verified: which mechanism held the retry, and why the 11-05 to 11-13 passes left no log rows.

**Fixed.** The PR is open and the draft is marked dispatched.

**Not fixed.** The monitor loop still does not scan its own drafts for undispatched items on each pass. That is the structural fix.

**Class.** State that lives only in a session: anything that must outlive the session (a retry, a promise, a pending send) needs a durable record that a later run is required to read.

---

## Near miss, caught: an upstream release silently moved a measuring instrument (2026-11-14)

**What happened.** The research lab pins its measurements to an identity gate: a recorded run that a new library version must reproduce bit for bit before older results can be compared with new ones. After the library went from 0.93.1 to 0.99.0, the gate differed on 8 of 10 arms, even with every announced default change pinned back.

**Why it did not become a failure.** The monitor runs the gate on every version bump. A tag bisect (one worktree per release, imported through `PYTHONPATH`, about a minute per run) placed the change at 0.95.2, a fix to how a lesson starts its settle, with no option to turn it off. The next experiment was redirected to run on the old version, and the gate was re-recorded on the new one, before any data was taken.

**Class.** Instrument drift under a dependency update. The defense that worked: an identity gate run on every update, plus a pinned-defaults run that separates announced changes from unannounced ones before bisecting.
