# SHIP CHECKLIST — context-memory-compaction cookbook notebook
Built + execution-validated 2026-07-03 (full-auto). PR HELD for Will.

## Artifact
- Staged: `~/JARVIS/anthropic-campaign/lane-a/context-compression/guide.ipynb`
- 27 cells (17 md / 10 code). Title: "Structured Context Compaction for Long Agent Runs".
- Target on PR: `anthropics/claude-cookbooks` : `capabilities/context-memory-compaction/guide.ipynb`
- Branch: `wglynn/add-context-memory-compaction`
- Commit: `feat(capabilities): add context-memory-compaction guide`

## Verified this session (full-auto)
- [x] gap confirmed (no existing context/memory-compaction notebook)
- [x] runs top-to-bottom KEYLESS (in-process exec, clean) — core claim needs no API key
- [x] measured: raw 1452 tok -> COMPACT 176 (12%) -> +FORGET 133 (9%) = 91% reduction
- [x] fidelity 7/7 probes recovered from compacted state; stale fact correctly evicted
- [x] API-gated cells skip cleanly with an honest message when no key present
- [x] AI-tell scan ZERO (em/en-dash, delve, robust, leverage-verb, Phase N, worth-noting)
- [x] ruff line-length: 0 code cells >100 chars; all code cells compile
- [x] current model ids (claude-opus-4-8 / sonnet-4-6 / haiku-4-5)
- [x] general: no VibeSwap/Noesis/JARVIS branding
- [x] adversarial QA: both agents accept-with-fixes; fixes applied by finalize pass

## Remaining before PR (mechanical CI-mirror + the outward gate)
- [ ] `uv run ruff check --fix` + `uv run ruff format` in a claude-cookbooks checkout
- [ ] `python scripts/validate_notebooks.py`
- [ ] `/notebook-review` + `/link-review` (confirm every URL resolves)
- [ ] optional: run the API-gated cross-check cells once with a real ANTHROPIC_API_KEY to populate outputs
- [ ] OUTWARD GATE: Will's eyes, then PR (first Lane-A contribution; held per speak-for-you outward discipline)

## To ship (once Will says go)
1. fork/clone `anthropics/claude-cookbooks`
2. `cp guide.ipynb capabilities/context-memory-compaction/guide.ipynb`
3. run the 4 CI-mirror checks above
4. branch + conventional commit + `gh pr create` with a narrow description
