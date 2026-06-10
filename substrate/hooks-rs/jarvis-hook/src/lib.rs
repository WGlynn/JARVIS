// jarvis-hook: shared substrate for Claude Code hook binaries.
// Contract: stdin JSON -> Payload, stdout JSON (Output) or "{}" for no-op.
// Hooks are short-lived processes; ✗ async, ✗ panic in prod path.

use std::env;
use std::io::{self, Read, Write};
use std::path::PathBuf;
use std::time::{SystemTime, UNIX_EPOCH};

use serde::{Deserialize, Serialize};

pub use serde_json::{json, Value};

pub type Err = Box<dyn std::error::Error>;
pub type R<T> = Result<T, Err>;

// ============ Payload ============

#[derive(Debug, Deserialize, Default)]
#[serde(default)]
pub struct Payload {
    #[serde(alias = "hookEventName")]
    pub hook_event_name: String,
    #[serde(alias = "toolName")]
    pub tool_name: String,
    #[serde(alias = "toolInput")]
    pub tool_input: Value,
    pub session_id: String,
    pub cwd: String,
    #[serde(flatten)]
    pub extra: serde_json::Map<String, Value>,
}

impl Payload {
    pub fn ti_str(&self, k: &str) -> &str {
        self.tool_input.get(k).and_then(Value::as_str).unwrap_or("")
    }
    pub fn ti_get(&self, k: &str) -> Option<&Value> {
        self.tool_input.get(k)
    }
}

pub fn read_payload() -> Payload {
    let mut s = String::new();
    if io::stdin().read_to_string(&mut s).is_err() || s.trim().is_empty() {
        return Payload::default();
    }
    serde_json::from_str(&s).unwrap_or_default()
}

// ============ Output emitters ============

#[derive(Debug, Serialize)]
struct PreToolCtx<'a> {
    #[serde(rename = "hookEventName")]
    hook_event_name: &'a str,
    #[serde(rename = "additionalContext")]
    additional_context: &'a str,
}

#[derive(Debug, Serialize)]
struct PreToolWrap<'a> {
    #[serde(rename = "hookSpecificOutput")]
    hook_specific_output: PreToolCtx<'a>,
}

#[derive(Debug, Serialize)]
struct StopBlock<'a> {
    decision: &'a str,
    reason: &'a str,
}

pub fn emit_silent() {
    let _ = writeln!(io::stdout(), "{{}}");
}

pub fn emit_additional_context(event: &str, msg: &str) {
    let w = PreToolWrap {
        hook_specific_output: PreToolCtx {
            hook_event_name: event,
            additional_context: msg,
        },
    };
    match serde_json::to_string(&w) {
        Ok(s) => {
            let _ = writeln!(io::stdout(), "{}", s);
        }
        Err(_) => emit_silent(),
    }
}

pub fn emit_block(reason: &str) {
    let w = StopBlock { decision: "block", reason };
    match serde_json::to_string(&w) {
        Ok(s) => {
            let _ = writeln!(io::stdout(), "{}", s);
        }
        Err(_) => emit_silent(),
    }
}

// ============ Filesystem / time helpers ============

pub fn home() -> PathBuf {
    if let Ok(h) = env::var("HOME") {
        return PathBuf::from(h);
    }
    if let (Ok(d), Ok(p)) = (env::var("HOMEDRIVE"), env::var("HOMEPATH")) {
        return PathBuf::from(format!("{}{}", d, p));
    }
    if let Ok(u) = env::var("USERPROFILE") {
        return PathBuf::from(u);
    }
    PathBuf::from(".")
}

pub fn now_secs() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|d| d.as_secs())
        .unwrap_or(0)
}

pub fn mtime_secs(p: &std::path::Path) -> Option<u64> {
    let st = std::fs::metadata(p).ok()?;
    let mt = st.modified().ok()?;
    mt.duration_since(UNIX_EPOCH).ok().map(|d| d.as_secs())
}

/// Tail-read the last `n` bytes of a file as UTF-8 (lossy on bad bytes).
/// Used by stop hooks that scan file ends for completion markers.
pub fn tail_utf8(p: &std::path::Path, n: u64) -> R<String> {
    use std::io::{Seek, SeekFrom};
    let mut f = std::fs::File::open(p)?;
    let len = f.metadata()?.len();
    let start = len.saturating_sub(n);
    f.seek(SeekFrom::Start(start))?;
    let mut buf = Vec::with_capacity(n as usize);
    f.take(n).read_to_end(&mut buf)?;
    Ok(String::from_utf8_lossy(&buf).into_owned())
}

pub fn read_text(p: &std::path::Path) -> R<String> {
    Ok(std::fs::read_to_string(p)?)
}

// ============ Re-exports (so binaries don't need to depend on serde_json directly) ============

pub mod re {
    pub use serde_json;
}
