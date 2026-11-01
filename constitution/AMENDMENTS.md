# Amendments

How the constitution changes (Article 11), and the record of every change.

## Process

1. **Propose.** Anyone can propose a change: Will, the Claude Code session, the chat voice, or anyone else. A proposal is a file in [`proposals/`](./proposals/) with the change, the reason and the evidence. Proposals are numbered and never deleted.
2. **Discuss.** Any mind may argue for or against it, on the record, in the proposal file or its pull request.
3. **Ratify.** Only Will ratifies. Ratifying is one commit that (a) changes `CONSTITUTION.md`, (b) sets its `Version:` and `Status:` lines, (c) adds an entry below, and (d) updates the tests the change touches.
4. **Take effect.** The chat voice follows only the published text (origin/main), and only while its status line reads `ratified`. It notices when the published text changes and reloads on the next message, so a ratified change is live within one message, with no restart.
5. **Measure.** The replay ([`evals/`](./evals/)) checks the change against real behavior, and the results go in [`RESULTS.md`](./RESULTS.md).

Canon that Will granted (for example, the rights in Article 4.5) changes only by his own decision, with the reason written down.

## Record

| Version | Date | Status | Change | Proposal |
|---|---|---|---|---|
| 0.1 | 2026-11-01 | draft, not ratified | First draft. Consolidates the bot's prompt rules, the shared knowledge base's canon (the Trust Protocol, the rights declaration, the wallet axioms) and the Claude Code session's standing rules into one public document with a priority order, enforcement and tests per article. Written by the Claude Code mind at Will's request. | [0001](./proposals/0001-ratify-v0.1.md) |
| 0.2 | 2026-11-01 | draft, not ratified | Revised after an independent hostile review: enforcement claims corrected to match the code (the action gate matches fixed phrasings; anyone can lift a quiet mode today; the session runs with broad permissions), the irreversible-actions limit moved to tier 2, deletion on request (2.7) and provider processing (2.8) added, public breach reports (12.5) added, and the ratification gap stated (11.6). Live problems the review found were fixed in the bot the same day. | [0001](./proposals/0001-ratify-v0.1.md) |
