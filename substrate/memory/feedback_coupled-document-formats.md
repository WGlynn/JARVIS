---
name: Coupled document format protocol
description: When editing documents that exist in multiple formats (e.g. HTML + docx), always regenerate all formats after every edit
type: feedback
---

When a document exists in multiple formats (e.g. `Will_Glynn_Smart_Contract_Engineer.html` + `.docx`), ALWAYS regenerate all derivative formats after every edit to the source file.

Current coupled pair:
- **Source**: `~/Will_Glynn_Smart_Contract_Engineer.html`
- **Derived**: `~/Will_Glynn_Smart_Contract_Engineer.docx` (via `pandoc [source] -o [target]`)

**Why:** Will caught that only the HTML was being explicitly edited. The docx was being regenerated but only by memory, not protocol. If forgotten, the formats drift and the wrong version gets sent.

**How to apply:** After ANY edit to the HTML resume, immediately run pandoc to regenerate the docx. Treat it as one atomic operation — edit + regenerate = one step, not two.
