---
name: md-to-pdf
description: Convert a markdown file to a typography-styled PDF. Use when the user asks to "PDF this", "make a PDF", "convert to PDF", "print this letter / doc", or wants any markdown rendered for sharing outside the terminal (email, DM, print). Wraps a pandoc + Chrome-headless pipeline with two style presets. Single source of truth — never re-implement the pandoc + chrome flow inline.
argument-hint: '<path-to-markdown>  [--style letter|memo]  [--output <path.pdf>]  [--keep-html]'
allowed-tools: Bash, Read
user-invocable: true
metadata:
  emoji: "📄"
---

# md-to-pdf — markdown → typography-styled PDF

**When invoked**: User wants a markdown file rendered to PDF for sharing or reading outside the terminal — correspondence, memos, drafts, anything where Telegram-DM / VS-Code-preview readability is insufficient.

**Why this exists**: On 2026-04-27 (letter-to-a partner incident) Claude rebuilt the pandoc + Chrome-headless pipeline inline — wrote a temp CSS file, tracked down pandoc's path, debugged Chrome's Windows-path quirks, cleaned up intermediates manually. Will called it out: *"that should be offloaded to a tool somehow."* This skill is that tool. **Do not re-implement the pipeline inline.** Call the script.

---

## Step 1 — Locate the markdown source

The input is whatever markdown file the user wants rendered. If the user pointed at a specific path, use it. If they said "this letter" / "the draft" / "the doc we just worked on", use the most recent `.md` file we just wrote or edited in this conversation.

If genuinely ambiguous, ask before running. One question beats one wrong PDF.

---

## Step 2 — Pick a style

Two presets, both letter-size paper:

- **`letter`** (default): serif body (Georgia / Iowan Old Style / Palatino), sans-serif headings, 11.5pt at 0.9″×1″ margins. For correspondence, long-form drafts, anything that benefits from bookish typography. Use this unless the user explicitly says otherwise.
- **`memo`**: sans-serif throughout, 10.5pt at 0.7″×0.8″ margins, tighter line-height. For internal memos, status reports, dense reference docs.

If the user named the artifact a "letter" / "draft" / "essay" / "post" / "writeup" → `letter`.
If they named it a "memo" / "report" / "status" / "brief" / "notes" → `memo`.
If unclear, default to `letter`.

---

## Step 3 — Run the script

```bash
~/.claude/scripts/md-to-pdf.sh <input.md> [--style letter|memo] [--output <path.pdf>] [--keep-html]
```

Output defaults to `<input-dir>/<input-basename>.pdf` (same directory as the source, same basename). Don't pass `--output` unless the user wants a different location.

Don't pass `--keep-html` unless the user explicitly wants the HTML intermediate (they almost never do).

---

## Step 4 — Report

Tell the user:
- **Where the PDF landed** (full path).
- **Style used** (letter / memo).
- **Size in KB** (a sanity signal — anything under 5KB or over 5MB is suspect).
- One line on what the user can do next ("open in your PDF reader" / "drag into Telegram / email" — match the use case the user mentioned).

Do NOT narrate the pandoc/Chrome pipeline internals. The user doesn't care about pandoc's path or Chrome's headless flags — those are implementation details now living in the script.

---

## Don't

- Don't re-implement the pandoc + Chrome pipeline inline. The whole point of this skill is consolidation.
- Don't add a third style preset on the fly without asking — preset additions belong in the script, not in conversation.
- Don't preview the HTML or open the PDF unless the user asks. The user knows where their files are.
- Don't suggest LaTeX-based alternatives ("we could use XeLaTeX / wkhtmltopdf") — the Chrome path is the load-bearing one because it's the only path we've validated end-to-end on this machine.

---

## If the script fails

Check in order:
1. **`pandoc not found`** → the script auto-detects pandoc at `~/AppData/Local/Pandoc/pandoc` and `/c/Program Files/Pandoc/pandoc.exe`. If neither exists, tell the user pandoc needs to be installed.
2. **`Chrome not found`** → similar, looks at standard Windows + macOS paths.
3. **`Access is denied` writing PDF** → the output path probably has a permissions issue or the file is open in a viewer. Suggest the user close any open instance and retry.
4. **Empty/tiny PDF (<5KB)** → the markdown was empty or the HTML conversion silently failed. Re-run with `--keep-html` and inspect the intermediate.

Don't troubleshoot pandoc or Chrome internals beyond this — escalate to the user.
