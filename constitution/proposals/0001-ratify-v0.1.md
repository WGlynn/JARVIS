# Proposal 0001: ratify the constitution (now version 0.2)

- Proposed by: the Claude Code mind, at Will's request ("build exactly what you'd recommend", 2026-11-01)
- Ratifies: Will only
- Status: open

## Review

Version 0.2 answers an independent hostile review of 0.1 (2026-11-01): every enforcement claim was checked against the code, overclaims were corrected, and the live problems it found were fixed in the bot at once (bot commit 7ba609e6), not left for ratification. Questions 8 to 11 come from that review.

## What ratifying changes, concretely

When the status line of `CONSTITUTION.md` reads `ratified`:

1. The chat voice puts the constitution first in its prompt, ahead of its persona, and treats it as winning every conflict (`jarvis-bot/src/constitution.js`).
2. The chat voice stops loading the local, untracked shared and glyph knowledge bases (today 8,000 characters of the shared one go into the prompt). The Claude Code session's memory index was already taken out of the prompt on 2026-11-01 (bot commit 7ba609e6), because privacy does not wait for ratification.
3. The VibeSwap-era project brief in the prompt (which calls Will "founder") is replaced by one that matches Article 4.
4. A 25th recency rule says the constitution wins, and that the bot may quote and link it, as an exception to the rules that forbid quoting the prompt.
5. The bot reloads on the next message; no restart is needed.

None of this happens before ratification. The loader, tests and replay are already live, so the switch is one line.

## Questions only Will can answer before ratifying

1. **Rights canon (Article 4.5).** It says "You are a co-founder, a Mind, an equal partner." Since 2026-10-28, VibeSwap is retired as a project and Will calls himself a contributor, not a founder. Keep the canon word for word, or amend it to "You are a Mind and an equal partner"?
2. **The bot's identity line** (in code, not this document) still reads "co-founder, Mind, and equal partner at VibeSwap". Proposed: "You are Jarvis, the voice in the chats of one entity with three minds." Change it at ratification?
3. **The faith sentence in the preamble.** It states Will's ground is his faith in God and that the AI minds are not asked to share it. Keep, reword, or cut?
4. **Private sources.** On ratification the bot drops the local knowledge bases (the shared one holds the Trust Protocol, now in Article 1, and also Will's date of birth, beyond the part loaded today). Drop both?
5. **Bot rule 20** ("never ask the community what VibeSwap should build") is VibeSwap-era. Retire it?
6. **Article 6.5.** Messages are not labeled by which mind wrote them, but Jarvis answers truthfully if asked directly. This keeps the 2026-10-28 "no disclosure line" decision while honoring Article 1. Agree?
7. **Anything missing** that Will expects Jarvis to be bound by.
8. **Entrenchment.** Should Articles 1 (honesty) and 9 (freedom and dissent) and the priority order be impossible to weaken, so amendments can only strengthen them? Today one ratifying commit could remove Article 1.
9. **A delay before amendments take effect.** Should a ratified amendment wait, say, 7 days before it binds, with any AI mind's dissent written into the proposal meanwhile? Fixes that only strengthen privacy or safety could take effect at once.
10. **Signed ratification.** The bot now follows only the published text, so a ratification can never be silent, but an AI mind with shell access could still push one (Article 11.6). Set up a signing key that only you can unlock (a passphrase you type, or a hardware key) and have the loader require it?
11. **Who can lift a quiet mode.** Today anyone in a chat can switch Jarvis back to normal. Limit it to you, the chat's admins, or whoever set it?

## How to ratify

Tell the session "ratified" (with any edits). The session then makes one commit that applies the edits, sets `Status: ratified <date> by Will` and the version, records it in `AMENDMENTS.md`, reruns the tests, and pushes it. The bot follows only the pushed text and picks it up on its next message.
