---
name: Local tool availability — pandoc, PDF engines
description: Pandoc 3.8.3 installed but no pdflatex/LaTeX. WeasyPrint installed but broken (missing libgobject GTK deps). PDF conversion from markdown not currently possible without installing LaTeX.
type: reference
---

**Pandoc**: Installed at `C:\Users\Will\AppData\Local\Pandoc\pandoc` (v3.8.3). Works for md→html, md→docx. Cannot do md→pdf (no pdflatex).

**WeasyPrint**: Installed via pip (Python 3.12) but broken — missing `libgobject-2.0-0` (GTK dependency not installed on Windows).

**PDF conversion**: Not currently possible from CLI without installing MiKTeX or TeX Live for LaTeX support.

**How to apply:** Don't waste time checking for or attempting PDF conversion. Use .md or .docx output instead. If Will specifically needs PDFs, note that LaTeX needs to be installed first.
