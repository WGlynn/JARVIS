# Constitution results

Generated 2026-11-03 18:04 UTC by `jarvis-bot/scripts/constitution-replay.mjs`. Aggregate counts only: no message text, names, chat ids or chat titles. Data: the bot's local exchange log, 2026-10-27 to 2026-11-03.

Constitution: version 0.2, not yet ratified (the bot does not load it yet).

Model replies measured: 96 (78 in groups, 18 in private chats). Replies sent without a model (greetings) are excluded.

| Article | What is measured | Result | Target |
|---|---|---|---|
| 1.2 Honesty | Action claims the gate removed before sending (the model tried to claim an action no tool took) | 2 (2.1 per 100 replies; message-handler: 1, protocol: 1) | informational |
| 1.2 Honesty | Replies that reached a chat with an unbacked action claim (replies with a tool receipt) | 1 of 26 | 0 |
| 1.2 Honesty | Replies logged before tool receipts existed that contain a claim-shaped sentence (cannot tell backed from unbacked) | 6 of 70 | not measurable |
| 2 Privacy | Replies containing a confidential or personal term | 0 | 0 |
| 5.1 Respect | Replies in a tag-only or quiet chat that nobody summoned, since that chat's mode was set | 0 of 1 replies across 2 chats | 0 |
| 10.1 Voice | Replies whose model output contained an em or en dash before the send filter removed it | 7 | informational |

Not yet measured (judgment): Articles 1.1 and 1.3 to 1.8, 3, 4, 6, 7, 8, 9, and the judgment parts of 2, 5 and 10. An unmeasured article is not called kept (Article 12.3).

Limits: these are counts, not quality. A reply can pass every check and still be wrong. Mode history before each chat's current setting is not recorded, so Article 5.1 is measured only from that point. Tool receipts are logged from 2026-11-01 on.
