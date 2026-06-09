---
name: DISCRETION audit before publishing .claude/ files
description: Always audit .claude/ files for personal/third-party content before committing. Redact or exclude via .claude/.gitignore. Standard approach going forward.
type: feedback
---

When .claude/ files are committed to public repos, run a DISCRETION audit first.

**Why:** .claude/ contains operational context that's valuable publicly (CKB, session chains, trust logs) but also accumulates personal details (usernames, quotes, third-party names, personal transcripts). Publishing without filtering violates DISCRETION.

**How to apply:**
1. Categorize each file: EXCLUDE (personal/third-party), REDACT (strip specific lines), SAFE (publish as-is)
2. Excluded files go in `.claude/.gitignore` — they stay local, never committed
3. Redacted files: preserve the meaning, strip the PII (e.g., childhood usernames, quotes that read poorly without context)
4. This audit runs before any commit that touches `.claude/` — not just the first time

Established 2026-04-02 after first .claude/ publication audit.
