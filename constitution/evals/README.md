# How the constitution is verified

Article 12 says every article must state how it is enforced and how it is tested, and that results are published. This folder explains both.

## 1. Tests: does the code enforce what the document says it enforces?

The code-enforced parts have tests in the bot's suite (`jarvis-bot/test/constitution.test.js`). The suite runs before every restart through `scripts/restart-local.ps1`, which refuses to restart onto failing code. A forced restart (`-Force`) skips the suite, and running the bot directly never runs it, so this is a strong default, not a guarantee.

| Article | Test ids | What they check |
|---|---|---|
| 1.2 No claimed action without a receipt | H1 to H5, the reply-path scan, and the web chat check | The action gate removes unbacked action claims, keeps them when a tool ran, and sits in front of every reply path, including the web chat (a source scan fails if a new path is added without it). It matches fixed phrasings, so rewordings can pass. |
| 1.2 and 5.1 Mode claims | M1 to M4 | A claimed mode change is removed unless it happened; a claim about the current mode passes only when it matches the chat's stored mode. |
| 2.1 Private sources stay out | P1 to P3 | The session's memory index is never loaded; once ratified, the local knowledge bases are left out too; group prompts carry no one's private DM topics. |
| 4.2 Contributor, not founder | A4 | The ratified project brief never says "founder". |
| 5.1 Quiet requests change the mode | R1 to R8 | Requests to stay quiet change the mode, including the documented "jarvis be quiet" with the name first or last; ordinary sentences do not. |
| 8.1 No funding asks | A8 | The automatic notice that asked chats for tip-jar funding cannot come back. |
| 10.1 No em or en dashes | V1 | The send filter removes them and keeps number ranges readable. |
| 11.3 Drafts never govern | A11 | Only a status line reading "ratified" turns the constitution on, and only in the published text: a local edit or an unpushed commit never ratifies (checked with a throwaway git repo). |
| 12.1 Every article is labeled | A12 | Each article in `CONSTITUTION.md` declares "Enforced by" and "Tested by". |

A test is only worth something if it can fail. The every-reply-path test was checked against the code from before the media-path fix: it flags that path as ungated, and it passes after the fix.

## 2. Replay: does the bot's real behavior match?

`jarvis-bot/scripts/constitution-replay.mjs` replays the bot's local exchange log against the articles and writes [`../RESULTS.md`](../RESULTS.md).

- **Counts only.** Message text, names, chat ids and chat titles never leave the machine. The published file holds aggregate numbers and the date range.
- **No private terms in the public code.** The list of confidential and personal terms lives in a local file that is never published; the replay loads it at run time. If it cannot, privacy is reported as NOT MEASURED, never as zero.
- **Unmeasured means unmeasured.** Articles that rest on judgment are listed as not yet measured. They are never reported as kept (Article 12.3).

To run it on the machine that hosts the bot: `node scripts/constitution-replay.mjs` from `jarvis-bot/`.

## 3. Not built yet

- Graded checks for the judgment articles (honest floor, no extraction, the roles of the minds). The plan is a rubric per article, graded on a sample of real replies, with the grading method published next to the scores.
- Results over time. Today `RESULTS.md` is a snapshot; it should become a dated series so drift is visible.
