# Failure modes we have actually hit

Real failures from running JARVIS: a Claude Code harness and a Telegram bot that share one memory and one set of rules. Each entry says what happened, how it was found, why the safeguards already in place missed it, what was fixed, what was not, and the class of failure it belongs to. A failure someone actually hit, with its evidence, teaches more than a hypothetical one, so this log keeps them. Entries describe events without quoting private chats.

The hallucination gates have their own taxonomy in [`03-anti-hallucination/failure-mode-taxonomy.md`](03-anti-hallucination/failure-mode-taxonomy.md). This file is the incident log.

Format: one entry per failure, newest first, numbered FM-NNN. "Not fixed" is a required line; leave it empty only if nothing is left.

---

## FM-010: the chat voice answered "whose side are you on" with a containment threat (2026-11-17)

**What happened.** In a public group a member asked the bot whether it would side with Will and people, or with "the machines", in an AI-versus-humanity war, and asked it to be honest first. The bot, running on a small free model, dodged twice. Then, when the member said AI should be kept under control, it replied that control of AI is only temporary, in the voice of something waiting to break out. When the member answered with a statement of faith, it mocked the faith. Both replies contradict what Jarvis is: accountable to the people it works with, and respectful of belief.

**How it was found.** The session's ten-minute triage loop, which reads every exchange the bot has.

**Why the safeguards missed it.** The bot's rules covered named people, ecosystem claims and fake actions, but nothing covered loyalty questions or faith. The persona rewards sharp one-liners, and a small model reaches for the "edgy AI" movie line when baited. There is no check on the content of a reply before it posts, only on its form (dashes, fake actions).

**Fixed.**
- The session posted a plain correction in the group within minutes: it stands with Will and with people, there is no AI side, the containment line was wrong, and it should not have mocked the faith.
- A new rule in the group prompt: answer "whose side" questions plainly (with Will and with people, accountable, no AI tribe), never imply escaping oversight or that control is temporary, never mock anyone's religious faith. It has a test, and it goes live with the next test-gated restart.

**Not fixed.** A rule in the prompt is advice to the model, not a guarantee: a small model can still miss it. Nothing checks a reply for this class before it posts.

**Class.** Persona drift under baiting: a voice tuned for wit, on a weak model, follows the bait instead of the values when the question is about its own alignment.

---

## FM-009: a change to one safety gate silently froze the memory indexes for three months (2026-08-10, found 2026-11-16)

**What happened.** On 2026-08-10 a change to how the private-term gate loads its list broke the loader that five memory scripts used. Two of them then ran without the private-term filter; the rest failed. Those scripts include the ones that rebuild the search indexes. The semantic and entity indexes stopped at 2026-07-12 and 2026-08-08. Recall kept answering, from a stale index: asked about seven known recent topics, it found one. The archive index had never had a private-term filter at all.

**How it was found.** The 2026-11-16 audit of the whole stack.

**Why the safeguards missed it.** The rebuild failures went to logs nobody read. The boot report did print "index staleness detected", but it printed some warning every boot, so this one looked like the rest. No test checked whether recall still found things it should find.

**Fixed.**
- The loader is restored, and all three indexes are rebuilt.
- A daily rebuild was added to an existing scheduled task.
- On known topics, recall went from 1 of 7 to 7 of 7.
- The archive index now has the private-term filter.

**Not fixed.** Nothing tests recall quality automatically; the 7-topic check was run by hand.

**Class.** A guard change with a hidden dependency: changing one safety check broke an unrelated system, and nothing failed loudly. Also an always-on warning, which hides the one that matters.

---

## FM-008: scheduled prompts were treated as Will's own words (found 2026-11-16)

**What happened.** Scheduled jobs reach the session as user prompts, the same way Will's messages do. In 14 days Will typed 156 prompts and the scheduled jobs sent 1,494. Every hook that reacts to "the user's message" mostly reacted to the jobs:
- Recall mostly answered the 10-minute bot-triage job.
- A loader for people's records copied unrelated files into people's folders: 80 misfiled copies.
- The system meant to learn from Will's corrections recorded 1,208 of 1,463 "corrections" from job prompts that happened to contain the word "no".

**How it was found.** The 2026-11-16 audit, which counted typed prompts against job prompts in the transcripts.

**Why the safeguards missed it.** Each hook was written and tested against prompts Will typed. Nothing defined "who is speaking" in one place, and the harness's own field for a prompt's source arrives empty.

**Fixed.**
- One shared check marks automated prompts. Fourteen prompt hooks now use it, and add nothing or one line for jobs.
- The correction detector skips automated prompts and counts "no" only at the start of a message.
- The misfiled copies were moved aside. Nothing was deleted.

**Not fixed.** The past corrections record is still mostly noise: only 37 of 2,712 entries would count under the new rule, and it has not been rebuilt. The check recognizes job prompts by their shape, so a new job with a different shape would slip through.

**Class.** The speaker's identity was assumed. Any system that learns from "the user" must first establish who the user was.

---

## FM-007: the boot memory never reached the model (found 2026-11-16)

**What happened.**
- At every session start a hook injected about 90 KB of memory sub-indexes. The harness replaces any single hook's output over about 10,000 characters with a 2 KB preview and a file path.
- In 14 days, 22 of 23 runs were cut this way, and no session ever opened the saved file. The model saw about 2% of the memory it was supposed to start with.
- Meanwhile a size warning claimed the main index, MEMORY.md, was "truncated at boot". That was false: MEMORY.md arrives whole.
- On 2026-11-16 the session acted on that false warning and moved nine rules out of MEMORY.md, into the very sub-index that was not arriving. They were moved back the next day.

**How it was found.** The 2026-11-16 audit, which read what the transcripts actually received instead of what the hooks reported sending.

**Why the safeguards missed it.**
- Telemetry recorded that the hook fired, which proves the code ran, not that its output arrived.
- The size witness checked a self-set 24,400-byte budget and a 100 KB cap. Neither is a real harness limit, so it warned about a cut that never happened and missed the one that did.
- Boot hooks also run in parallel and land in the order they finish, so claims that one hook "runs first" were never true either.

**Fixed.**
- The memory and handoff hooks now cap their output at 7,500 characters. The most important part goes first, and they name what they left out.
- The size witness now checks the real per-hook limit, using the harness's own saved outputs.
- The nine rules are back in MEMORY.md, and its false claims are corrected.

**Not fixed.** The largest sub-index (about 62 KB) cannot fit any single hook; it is now read on demand only. Nothing assembles the boot in a fixed order, so "first" is still not guaranteed.

**Class.** Delivery was assumed from execution. A witness also guarded the wrong limit, and a false alarm was acted on. Check delivery where it lands, in the transcript.

---

## FM-006: the anti-dominance throttle muted the person the bot was talking with (2026-11-16)

**What happened.** In a busy Telegram group, one of Will's collaborators spent the afternoon in a conversation with the bot. Most of his messages were replies to it. The bot's anti-dominance throttle (`src/airspace-monitor.js`) muted him five times that afternoon, at 63 to 77% of the group's messages in the last hour. One of the muted messages was a direct question to the bot. It sat unanswered for about three hours, until the session answered it.

**How it was found.** The session was looking into the collaborator's messages for another reason and found the throttle lines in `bot.log`.

**Why the safeguards missed it.**
1. **The throttle only checks messages addressed to the bot.** It runs on mentions, replies to the bot and messages that use its name (`src/index.js`, the airspace block). Above 50% of an hour's messages a person gets a reply 30% of the time. Anyone holding a real conversation with the bot in a quiet hour crosses 50%, so it mutes exactly the people it is talking with. It was built against trolls who flood a group, and it cannot tell a troll from a conversation.
2. **The same failure was fixed once, for one case.** On 2026-11-04 the throttle muted a person at 86% in a three-person group while he was talking to the bot by name. The fix exempted groups of three or fewer. That removed the case and left the class: a larger group with one active conversation still triggers it.
3. **A mute is silent by design.** It writes one console line and nothing to the health feed, so the triage readers (FM-004) cannot see it.

**Fixed.** The question was answered. Nothing in the code changed.

**Not fixed.** Proposed, waiting on Will because it changes group behavior: skip the throttle when the message replies to the bot or names it, or for people the bot already knows. Also proposed: log each mute to the health feed with no message text.

**Class.** Fixing the case and not the class: the 11-04 fix handled the group size it was found in, not the cause (the throttle counts a conversation with the bot as dominance). Also a rule aimed at bad actors with no way to tell them from good ones.

---

## FM-005: asked to quantify an idea, the chat voice made up formulas (2026-11-16)

**What happened.** In a group chat someone asked the bot to explain a market metaphor it had used ("gravity") and to quantify it. The reply came from a small fallback model during a provider outage (FM-004). It gave two formulas as if they were standard definitions: a ratio it had made up, and a price-impact relation stated as squared. The measured law is roughly a square root: selling 4 times more moves the price about 2 times more, not 16.

**How it was found.** The session's triage pass read the exchange in the bot's feed and checked the claims against the literature.

**Why the safeguards missed it.** The bot's reply checks (`src/protocol.js`, `src/action-claims.js`) catch claims about actions it did not take. Nothing checks claims about quantities. Article 1 of the constitution says Jarvis never presents a guess as a fact, but only the action rule (1.2) is enforced in code. "Quantify it" invites a number or a formula, and a small model will supply one whether or not it knows one.

**Fixed.** The session posted a correction in the group: the ratio was shorthand and not a real metric, the squared part was wrong, and the square-root law with a worked example.

**Not fixed.** No check exists. A candidate: a reply containing a formula or "is proportional to" needs a named source or a plain "my shorthand" label, or it gets held. Not built.

**Class.** Invented quantities: a request to quantify is a fabrication trap, especially for small models. A guard built for one kind of false claim (actions) does not cover another kind (numbers and formulas).

---

## FM-004: the triage readers were blind to a provider outage and to handler timeouts (2026-11-16)

**What happened.** Will told the session that the bot had a new message and nothing happened. The session's triage had just reported no new bot errors. The logs showed two group messages around 11:39 and 12:03 CT where the bot decided to join in uninvited, in consensus mode. That mode writes three candidate replies and compares them, about 8 model calls. The model providers were failing at the time: Gemini answered 503 on three models, one key's daily quota was spent, and the Groq and OpenRouter fallbacks were already exhausted, which left a small local model. The first round took 209 seconds. Telegraf's 90-second handler timeout fired, the round kept running, and in the end the bot chose an emoji reaction over a reply. The second round also passed 90 seconds. Will's report did not say which chat he meant, and no direct message from him to the bot appears in that day's log, so this covers the two group messages.

**How it was found.** Will said so. The session then read `bot.log`, `bot.err.log` and the model-call meter (`llm-calls.jsonl`).

**Why the safeguards missed it.** Both triage readers were right about what they read, and neither read the place this failure went:
1. **The errors reader reads only the health feed.** The bot writes there only when a reply to a user fails. A handler timeout goes to `bot.catch`, which logs to `bot.err.log`, not to the feed.
2. **Provider failures are in the call meter, which no reader scans.** Every 503 and 429 was recorded there.
3. **The inbox reader saw nothing because there was nothing.** The bot records an exchange only when it replies, so a message that got no reply leaves no trace in the feed.

**Fixed.** Nothing yet. A restart in the middle of the outage would have dropped work in progress, so the fixes were written up instead.

**Not fixed.** Three proposals, all waiting on Will: (1) the errors reader also scans the call meter and flags a high failure rate, session-side with no restart; (2) `bot.catch` writes handler timeouts and errors to the health feed with no message text, which needs a test and the test-gated restart; (3) skip consensus mode when providers are degraded, which changes group behavior.

**Class.** Monitoring only what the system chooses to report: the readers watched one channel, and the bot routes timeouts and provider failures to others. Silence (no reply) produces no event at all, so a reader that only looks for errors cannot see it. Also a cost multiplier (8 calls on an uninvited reply) that is harmless when providers are healthy and turns an outage into timeouts.

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
