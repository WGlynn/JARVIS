# jarvis-hooks-rs

Rust port of the JARVIS hook substrate for Claude Code.

> Adopt this if you want JARVIS without Python.

## Status

**Proof of concept.** 3 of ~50 hooks are ported (`autonomous-continue`,
`coordination-mechanism-gate`, `em-dash-augmentation-gate`). The remaining
~47 Python hooks under `~/.claude/hooks/` and `~/.claude/session-chain/`
are **not** ported yet. This crate exists to:

1. Validate the shared-library design (`jarvis-hook`).
2. Demonstrate drop-in compatibility with the Claude Code hook JSON contract.
3. Give Rust-preferring adopters a starting substrate.

The Python hooks remain the canonical source of truth. Each Rust port
preserves the JSON I/O contract exactly so Rust and Python hooks can be
mixed-and-matched in `settings.json`.

## Layout

```
hooks-rs/
├── Cargo.toml                       # workspace
├── jarvis-hook/                     # shared library
│   └── src/lib.rs                   # Payload, emitters, fs/time helpers
├── autonomous-continue/             # Stop hook
├── coordination-mechanism-gate/     # PreToolUse classifier (Agent spawns)
└── em-dash-augmentation-gate/       # PostToolUse scrubber gate
```

`Cargo.lock` is intentionally **not committed** — this is a library workspace.

## Build

```sh
cd ~/jarvis-monorepo/substrate/hooks-rs
cargo build --release
```

Binaries land at `target/release/{autonomous-continue,coordination-mechanism-gate,em-dash-augmentation-gate}[.exe]`.

## Hook contract (preserved exactly)

Every hook reads a JSON payload on stdin and writes JSON on stdout:

| Hook event       | Output shape (when augmenting)                                       |
|------------------|----------------------------------------------------------------------|
| `PreToolUse`     | `{"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":"..."}}` |
| `PostToolUse`    | `{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"..."}}` |
| `UserPromptSubmit`| `{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"..."}}` |
| `Stop`           | `{"decision":"block","reason":"..."}` (to force continue)            |
| (no-op)          | `{}`                                                                 |

Stop-hook output **must** be top-level (per `[P·stop-event-schema-restriction]`).
The Rust `emit_block` helper enforces this.

## settings.json — swapping Python for Rust

Replace each hook command with the compiled binary path. Example
diff (Windows; on Unix, drop `.exe`):

```json
// before
{
  "Stop": [{
    "hooks": [{
      "type": "command",
      "command": "python C:/Users/Will/.claude/hooks/autonomous-continue.py"
    }]
  }],
  "PreToolUse": [{
    "matcher": "Task",
    "hooks": [{
      "type": "command",
      "command": "python C:/Users/Will/.claude/hooks/coordination-mechanism-gate.py"
    }]
  }],
  "PostToolUse": [{
    "matcher": "Write|Edit|NotebookEdit",
    "hooks": [{
      "type": "command",
      "command": "python C:/Users/Will/.claude/hooks/em-dash-augmentation-gate.py"
    }]
  }]
}

// after
{
  "Stop": [{
    "hooks": [{
      "type": "command",
      "command": "C:/Users/Will/jarvis-monorepo/substrate/hooks-rs/target/release/autonomous-continue.exe"
    }]
  }],
  "PreToolUse": [{
    "matcher": "Task",
    "hooks": [{
      "type": "command",
      "command": "C:/Users/Will/jarvis-monorepo/substrate/hooks-rs/target/release/coordination-mechanism-gate.exe"
    }]
  }],
  "PostToolUse": [{
    "matcher": "Write|Edit|NotebookEdit",
    "hooks": [{
      "type": "command",
      "command": "C:/Users/Will/jarvis-monorepo/substrate/hooks-rs/target/release/em-dash-augmentation-gate.exe"
    }]
  }]
}
```

You can mix freely: run some hooks in Rust and others in Python.

## Hook details

### `autonomous-continue` (Stop)
Scans for pending work; if found, blocks the Stop event with a
continue-reminder. Signals:
- in-flight `*.output` files under `~/.claude/projects/**/tasks/` (mtime < 30 min, no `"status": "completed"` in tail-4KB)
- `**/AUDIT_INDEX.md` files (fresh mtime) containing `in-flight`
- `~/vibeswap/.claude/WAL.md` head-2KB contains `ACTIVE` (fresh mtime)
- `~/.claude/state/tasks-pending.json` array non-empty

Stale window = 7 days. In-flight window = 30 minutes. Emits
`decision:block` with a reason if any signal fires; `{}` otherwise.

### `coordination-mechanism-gate` (PreToolUse, matcher `Task`)
Classifies Agent spawn `description` into a tier (haiku/sonnet/opus). If the
spawn requests a higher tier than necessary, emits a downgrade suggestion.
Conservative: downgrade-only. Upgrade-recommendations deferred (model
decides when it needs more capacity).

### `em-dash-augmentation-gate` (PostToolUse, matcher `Write|Edit|NotebookEdit`)
Scans newly-written `file_path` against partner-facing path patterns
(`Desktop/<partner>-*`, etc.). If em-dash (U+2014) or en-dash (U+2013)
present in `content`/`new_string`/`new_source`, emits a scrub reminder.
Augmentation, not block. Em-dashes remain fine in memory/code/internal.

## Shared library (`jarvis-hook`)

Hook authors write a binary with a `main()` that:

```rust
use jarvis_hook as h;

fn main() {
    let p = h::read_payload();             // stdin JSON -> Payload
    if p.hook_event_name != "PreToolUse" { // dispatch by event
        h::emit_silent();
        return;
    }
    let desc = p.ti_str("description");    // sugar for tool_input lookups
    if /* condition */ false {
        h::emit_additional_context("PreToolUse", "msg");
    } else {
        h::emit_silent();
    }
}
```

Helpers exposed:
- `read_payload() -> Payload` — fail-quiet JSON parse, defaults on error
- `Payload::ti_str(&self, key)` / `ti_get` — `tool_input` accessors
- `emit_silent()` / `emit_additional_context(event, msg)` / `emit_block(reason)`
- `home()` — `$HOME` / `%USERPROFILE%` on Windows
- `now_secs()`, `mtime_secs(path)` — Unix-epoch seconds
- `tail_utf8(path, n)` — read last `n` bytes as UTF-8 (lossy)
- `read_text(path)` — read whole file to `String`

## Design notes

- **No `unwrap()` in production paths.** `?`-style fallible code with
  fail-quiet `{}` output on any IO/parse error. Hooks are short-lived and
  augmentation-only; loud failure would noise up every Claude turn.
- **No async.** Hooks are sub-second one-shot processes.
- **Per-hook binaries.** Each ships as its own executable so `settings.json`
  paths stay surgical. A future `jarvis-hooks` multiplexer with subcommands
  is possible but unnecessary today.
- **Idiomatic Rust + dense identifiers.** Modeled on `[F·optimize-for-llms]`:
  short names where context disambiguates; no narrative docstrings.

## Not ported (yet)

Everything else under `~/.claude/hooks/` and `~/.claude/session-chain/`,
including: anticipation-hook, hiero-gate, deep-recall, atomic-reflection-gate,
clock-injector, conflict-detector, post-generation-recall, the chain
multiplexer, the layer8 link-rot audit, and `sync-public-substrate.py`.
The first three were chosen as PoC because they exercise: file scanning,
regex classification, and conditional event/tool dispatch — covering the
common-case surface area of the rest.

PRs welcome. Keep the Python hooks as canonical; port one at a time;
mirror semantics exactly so swapping is invisible to Claude.

## License

MIT OR Apache-2.0 (matches the parent monorepo).
