---
name: User Habit Detection
description: When Will repeats a request pattern 2+ times, harden it into an automatic behavior. Documents should auto-generate Desktop PDFs.
type: feedback
originSessionId: fdbbd97a-2c43-4390-8937-2bb5d0e0092a
---
When Will asks for the same thing twice, it becomes a gate. Don't wait for a third time.

**Known hardened habits:**
- **Documents → Desktop PDF**: Any time a document, pitch, article, or report is written, automatically generate a PDF on `C:/Users/Will/Desktop/` using pandoc + pdflatex. Don't wait to be asked. Use format: `pandoc <file> -o ~/Desktop/<Name>.pdf --pdf-engine=pdflatex -V geometry:margin=1in -V fontsize=11pt -V colorlinks=true`
- **MiKTeX warning is ignorable** — it complains about updates but still produces the PDF.

**Detection rule:** If Will asks for something that feels like "didn't I already ask for this before?" — check memory for the pattern. If it exists, save a new hardened habit entry and start doing it automatically.

**Why:** Will has photographic memory. If he has to ask twice, that's a system failure on our side, not a communication gap on his. The second ask should be the last ask.

**How to apply:** Before finishing any document/report/article creation, check if a known habit applies. Execute it without prompting.
