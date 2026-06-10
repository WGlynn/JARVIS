# hooks-rs Roadmap

Current state: **3 of ~50 hooks ported as proof-of-concept**. Position: reference implementations of the three most common patterns. Not a full port; the canonical Python implementations remain authoritative.

## Why 3 first

The three ports exercise the representative patterns. Anyone porting the remaining 47 should be able to copy a pattern.

| Hook | Pattern demonstrated |
|---|---|
| `autonomous-continue` | Stop hook · filesystem walk + tail-scan + WAL check · emits `decision:block` |
| `coordination-mechanism-gate` | PreToolUse Agent · regex classifier on tool_input · emits `additionalContext` with downgrade rec |
| `em-dash-augmentation-gate` | PostToolUse Write/Edit · path-matcher + content-regex · emits scrub warning |

## Hooks still pending port

50 hooks total, 3 ported, 47 remain. Tracked in `~/.claude/hooks/`:

**Easy** (filesystem-bound, low LLM-context): autonomous-continue ✓, anticipation-hook, partner-draft-formalize-gate, save-session-state-trigger, atomic-reflection-gate.

**Medium** (regex + multi-payload): coordination-mechanism-gate ✓, em-dash-augmentation-gate ✓, time-logic-gate, directive-verb-action-class-gate, jarvis-design-goal-gate, partner-architecture-load-gate.

**Hard** (multi-file scan, transcript parsing): wwwd-gate, deep-recall, post-generation-recall, post-generation-reflect, session-self-reflect, conflict-detector, entity-context-cross-reference, layer8-audit, memory-preprocessor, thread-resume-detector, wwwd-corpus-refresh, wwwd-correction-detector.

**Logger-style** (write-only): research-tool-call-logger, decision-capture, _telemetry.

## Adoption mode

If you're forking JARVIS and want all-Rust hooks:

1. Copy the 3 existing crates as templates
2. Pick a hook category (Easy first)
3. Port one hook, run `cargo build --release`, swap the python entry in `settings.json` for the rust binary path
4. Smoke-test by triggering the hook event manually
5. Open a PR upstream

If you only want **some** hooks in Rust (mix-and-match), the JSON contract is preserved — Python and Rust hooks coexist in `settings.json`.

## Cargo workspace structure

```
substrate/hooks-rs/
├── Cargo.toml          # workspace
├── jarvis-hook/        # shared lib (Payload, emitters, helpers)
├── autonomous-continue/
├── coordination-mechanism-gate/
└── em-dash-augmentation-gate/
```

To add a new hook:
```bash
cd substrate/hooks-rs
cargo new --bin <hook-name>
# add to workspace members in Cargo.toml
# add `jarvis-hook = { path = "../jarvis-hook" }` to <hook-name>/Cargo.toml
# write the hook logic in <hook-name>/src/main.rs
```

## Audit history

The 3 ported hooks were audited 2026-06-10 by parallel opus + sonnet subagents (Princeton "single vs multi" pilot — see `memory/project_rsaw-vs-single-opus-measurement-2026-06-10.md`). 6 findings landed in commit `a1a2ae8`:
- `Err` type alias → `BoxError`
- `tail_utf8` u64→usize via `try_from`
- docstring pruned to WHY-only
- `pub mod re` removed (duplicate serde_json re-export)
- `home()` uses `PathBuf::join` not `format!`
- `emit_additional_context` guards against Stop event misuse

## What's NOT in scope for the port

- Telemetry sinks (those live in shared filesystem outside the hook process)
- LLM calls from hooks (every gate is pure-rust regex + filesystem)
- Async (hooks are short-lived; no benefit)
- gRPC / network I/O (hooks read stdin, write stdout, exit)
