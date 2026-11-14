# Skills

Claude Code skills from the Jarvis setup. Each folder holds one `SKILL.md`; copy the folder into `~/.claude/skills/` and invoke it as `/<name>`.

| Skill | What it does |
|---|---|
| [`literature-loop`](./literature-loop/SKILL.md) | Improve a paper, or a whole corpus of papers, in rounds: audit against the code, parallel read-only reviews through different reader lenses, one fixer per wave, internal and cross-paper coherence, a claims registry for the corpus, and a stop rule. |
| [`classify`](./classify/SKILL.md) | Classify a task description to recommend the cheapest viable Claude tier (haiku / sonnet / opus). |
| [`critical-qa`](./critical-qa/SKILL.md) | Self-adversarial Q&A on a code artifact. |
| [`house-style`](./house-style/SKILL.md) | Extract an opinionated design house-style from a reference (URL/screenshot/Dribbble) into concrete tokens + an HTML template, then apply it, so UI stops looking generic/"vibe-coded |
| [`marginal-contribution`](./marginal-contribution/SKILL.md) | Score and improve a piece of writing for MARGINAL CONTRIBUTION — what it adds over prior work and the live thread, not polish. |
| [`md-to-pdf`](./md-to-pdf/SKILL.md) | Convert a markdown file to a typography-styled PDF. |
| [`ship-web`](./ship-web/SKILL.md) | Verification checklist that MUST run before declaring any web artifact (HTML, deck, page, doc) "shipped" / "live" / "done." Enforces viewport meta tag, responsive breakpoints, live |
| [`trp2`](./trp2/SKILL.md) | Run the workflow-level HIERO compaction loop — formally "Turing Recursion Protocol 2.0" (TRP 2.0). |

Third-party skills used locally (design-system, frontend-slides, last30days) are not mirrored here; get them from their own repositories under their licenses.
