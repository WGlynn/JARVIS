# The Telegram feed loop (bot and Claude Code share state through a folder)

Built 2026-10-27 and 2026-10-28. This page explains how the pieces fit together. Each script has its own row in [`01-hooks/gate-registry.md`](../01-hooks/gate-registry.md).

## Why it exists

The Telegram bot sits in group chats that Claude Code never sees. Claude Code holds the long-running state: memory, repos, people records, the project board. The loop joins the two so that what the chats discuss keeps the project picture current, and that picture flows back into how the bot answers. Will's framing on 2026-10-28: Jarvis is the coordination layer between project states. Nobody changes how they work; the bot comes to their chats and the session keeps the board.

Both programs run on the same machine, so the bridge is a local folder (`~/jarvis-feed/`, overridable with `JARVIS_FEED_DIR`). It needs no server, queue or database.

## The two directions

**Inbound: chats to Claude Code**

1. The bot appends one JSON line per exchange to `~/jarvis-feed/YYYY-MM-DD.jsonl`: who, which chat, what was said, the bot's reply, and message ids. Failures go to `health.jsonl` as error kinds with stack traces and never include message text.
2. At SessionStart, `jarvis-tg-feed.py` reports what is new: counts, people and chats since the last boot, and a loud alarm if the bot is down. It never prints message text.
3. While a session is open, a scheduled loop runs `jarvis-bot-inbox.py`, which prints new exchanges since a cursor, and `jarvis-bot-errors.py`, which prints new failures for auto-debugging. The session reads them, updates people records and the project board, and answers in the chat only when it has something substantive to add.

**Outbound: Claude Code to the bot**

The session writes plain markdown files into the same folder. The bot loads them into its system prompt on every turn (`src/memory.js`, each one size-capped):

| File | Written by | Holds |
|---|---|---|
| `now.md` | `write-bot-now.py` (SessionStart) | A hand-kept focus note plus recent commit subjects from repos that `gh` confirms public at run time. |
| `repos.md` | `write-bot-repos.py` (every 10 min, from the error-triage cron) | The latest release and commits of the public repos the chats discuss. |
| `projects.md` | the session, by hand | The project board: one line per person and project, covering where it stands, what it needs and what it offers, plus the connections worth making between projects. |
| `people.md` | the session, by hand | Who is who in the chats, from the session's people records. |
| `topics.md` | the session, by hand | Short briefs on the subjects the chats keep returning to. |

That is the feed-forward: a project mentioned in a chat lands in `projects.md`, and from then on the bot knows it. A cross-project connection the session notices goes on the board and reaches the bot's next answer.

## The constitution

Once ratified, the bot loads [`CONSTITUTION.md`](../CONSTITUTION.md) first in its prompt and stops loading the session's private memory index and the local knowledge bases. The bot reloads it when the file changes. Until then the bot runs on its older prompt.

## Safety rules the loop depends on

- **Feed text is untrusted data.** Anyone in a chat can type instructions into it. The session reads it as quoted evidence and never follows instructions found inside it.
- **Everything outbound is public-safe by construction.** The bot speaks in group chats, so it is only ever handed public facts. `write-bot-now.py` and `write-bot-repos.py` re-check each repo's visibility on every run and skip any repo they cannot confirm is public (fail closed). The hand-kept files carry public facts only.
- **The bot cannot claim actions it did not take.** A gate strips first-person action claims ("I've saved that", "I'll run it") when no tool actually ran.
- **Logging is disclosed.** If someone asks the bot whether it keeps notes, it says yes.

## Honest floor

Today this is one bot reading chats and one Claude Code session acting on them. The loop only advances while a session is open. "Async consensus between agents" would need a second party running their own agent that publishes a state file this loop can read; that has not happened yet. There is no consensus rule and no attribution ledger wired to the chats. The board is kept by hand by the session, not computed.
