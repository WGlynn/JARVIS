# Contributing to JARVIS

JARVIS is a personal substrate first. The author runs it as their daily Claude Code overlay, so the contribution bar isn't "is this useful in general?" — it's "is this load-bearing for someone actually using the substrate?" That makes the contribution surface narrower than most projects, but the parts that are open are *genuinely* open.

## What we accept

**Hooks** (`substrate/hooks/`) — new gates for `PreToolUse`, `SessionStart`, `Stop`, etc. The bar:
- Self-contained Python 3.10+, stdlib only (or document the dep clearly).
- Reads JSON from stdin, emits JSON to stdout in the documented hook contract.
- Fail-quiet on missing inputs unless the hook is load-bearing (in which case fail-loud with a `[WARN]` line — see [`primitive_boot-hook-fail-loud.md`](./substrate/memory/primitive_boot-hook-fail-loud.md)).
- Includes a one-paragraph docstring explaining the *signal* it surfaces.

**Primitives** (`substrate/memory/`) — new patterns, feedback rules, projects, references. The bar:
- Follow the HIERO format (operator-density, no prose). See [`substrate/memory/MEMORY_FORMAT_SPEC.md`](./substrate/memory/MEMORY_FORMAT_SPEC.md) and any existing primitive as a reference.
- Filename: `<type>_<slug>.md` where type is `primitive` / `feedback` / `project` / `reference`.
- One claim per primitive. If you can split it into two, do.
- Cross-link to siblings via shortcodes (`[X·slug]`) and ensure `MEMORY.md` references it.

**Verify scripts** (`verify/`) — new falsifiable checks against architectural claims. The bar:
- Each script tests *one* claim.
- Output: pass/fail + a one-line reason. Zero exit code on pass.
- No network calls, no mutation of the substrate.

**Layer essays** (`01-hooks/` through `08-filesystem-as-substrate/`) — improvements to the architecture description per layer. The bar:
- The essay points to *concrete artifacts* in `substrate/` or linked repos. No floating abstractions.
- If you're proposing a new layer-essay, open an issue first.

## What we don't accept (without prior discussion)

- New top-level directories or modules — open an issue.
- Renames or restructures of `substrate/jarvis/` Python package — open an issue.
- New CLI subcommands — open an issue.
- Edits to the `01-08` layer-essay structure (adding files inside an existing layer is fine).
- Papers in `papers/` — these are author-voiced essays. Submit via issue + draft link, not direct PR.

## How to propose a change

1. **Read the corresponding existing artifact first.** If you're adding a hook, read 3-4 existing hooks. If a primitive, read 5. Match the voice and density.
2. **Open an issue** if your change is bigger than one file. Use the [feature request template](./.github/ISSUE_TEMPLATE/feature_request.md).
3. **Run `python -m jarvis verify`** before opening the PR. If you added a primitive, this catches malformed frontmatter and broken cross-references.
4. **PR title format**: `[hook] <name>: <one-line signal>` for hooks, `[primitive] <slug>: <one-line claim>` for primitives, `[verify] <claim being checked>` for verify scripts, `[layer N] <change>` for layer essays.
5. **PR description**: what claim/signal does this add? what existing artifact is it adjacent to? what does verify say?

## What gets fast-tracked

- Bug fixes (broken cross-references, hook crashes, typos in load-bearing artifacts).
- Compatibility patches (Python version, Windows encoding, etc.).
- Verify-script additions for already-shipped architectural claims.

## 10-minute recipes (concrete templates)

These are copy-paste starting points so you don't have to figure out the scaffolding.

### Add a PreToolUse hook

```bash
cd substrate/hooks
cp templates/hook-pretool-template.py your-hook-name.py
# edit DETECT_PATTERNS and ADVISORY_MESSAGE inside
# register in ~/.claude/settings.json under PreToolUse with the right matcher
# add a payload sample to tests/test_hook_contract.py
pytest tests/ -k your-hook  # smoke-test
```

The template handles fail-quiet, telemetry logging, partner-facing path filtering, and the JSON output contract. Fill in three constants.

### Add a Rust hook

```bash
cd substrate/hooks-rs
cargo new --bin your-hook-name
# in your-hook-name/Cargo.toml: add `jarvis-hook = { path = "../jarvis-hook" }`
# add to workspace members in hooks-rs/Cargo.toml
# write hook in your-hook-name/src/main.rs (copy from existing 3 for patterns)
cargo build --release
```

See `substrate/hooks-rs/ROADMAP.md` for which of the 3 reference shapes (autonomous-continue / coordination-mechanism-gate / em-dash-augmentation-gate) is closest to your hook.

### Run the full test suite

```bash
cd substrate/hooks && pytest tests/ -v                                   # python hook contract tests (parametrized over all hooks)
cd substrate/hooks-rs && cargo test --release                            # rust hook tests
python verify/verify_primitive_corpus.py                                  # corpus integrity
python verify/verify_no_secrets.py                                        # no leaks
cd substrate/hooks/layer8-audit && python layer8_audit.py                 # link-rot audit
```

All five run in CI on push. Layer 8 hard-fails when broken-ref count > baseline (46 as of 2026-06-10).

## What gets slow-tracked or declined

- Refactors of the existing substrate that don't change behavior. The substrate is shaped by usage, not engineering preference.
- "Cleanup" PRs that touch many files for stylistic reasons. The voice is intentional.
- Anything that hides personal-substrate provenance (e.g. removing the "I run this on my Claude" framing). The repo is honest about being one person's substrate, and that's a feature.

## Bug reports

Use the [bug report template](./.github/ISSUE_TEMPLATE/bug_report.md). Include:
- Which hook / primitive / verify script.
- The exact command run.
- The full stderr / stdout.
- Your Claude Code version + Python version + OS.

## License

By contributing, you agree your contribution is licensed under the MIT License (see [`LICENSE`](./LICENSE)).
