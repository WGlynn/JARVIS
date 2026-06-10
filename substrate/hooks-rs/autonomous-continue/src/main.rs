// Stop-event hook port. Scans for pending-work signals; if any, emit
// decision=block with continue-reminder so the model picks up next unit.
// Source: ~/.claude/hooks/autonomous-continue.py
//
// Signals:
//   1. in-flight task .output files (mtime < 30min, no completion marker)
//   2. AUDIT_INDEX.md files containing "in-flight" (mtime fresh)
//   3. WAL.md ACTIVE marker (mtime fresh)
//   4. ~/.claude/state/tasks-pending.json non-empty
//
// Stale window = 7d; in-flight window = 30min.

use std::path::{Path, PathBuf};

use jarvis_hook as h;
use serde_json::Value;

const IN_FLIGHT_WINDOW_S: u64 = 30 * 60;
const STALE_SIGNAL_S: u64 = 7 * 24 * 60 * 60;
const TAIL_BYTES: u64 = 4096;
const WAL_HEAD_BYTES: usize = 2000;

fn session_root() -> PathBuf {
    h::home().join(".claude").join("projects")
}
fn audit_root() -> PathBuf {
    h::home().join("audits")
}
fn wal_path() -> PathBuf {
    h::home().join("vibeswap").join(".claude").join("WAL.md")
}
fn tasks_pending() -> PathBuf {
    h::home().join(".claude").join("state").join("tasks-pending.json")
}

fn iter_dirs(p: &Path) -> impl Iterator<Item = PathBuf> {
    std::fs::read_dir(p)
        .ok()
        .into_iter()
        .flatten()
        .flatten()
        .filter(|e| e.file_type().map(|t| t.is_dir()).unwrap_or(false))
        .map(|e| e.path())
}

fn find_inflight_agents() -> Vec<String> {
    let mut out = Vec::new();
    let root = session_root();
    if !root.exists() {
        return out;
    }
    let now = h::now_secs();
    let cutoff = now.saturating_sub(IN_FLIGHT_WINDOW_S);
    for proj in iter_dirs(&root) {
        for session_dir in iter_dirs(&proj) {
            let tasks = session_dir.join("tasks");
            if !tasks.is_dir() {
                continue;
            }
            let entries = match std::fs::read_dir(&tasks) {
                Ok(e) => e,
                Err(_) => continue,
            };
            for entry in entries.flatten() {
                let p = entry.path();
                if p.extension().and_then(|s| s.to_str()) != Some("output") {
                    continue;
                }
                let Some(mt) = h::mtime_secs(&p) else {
                    continue;
                };
                if mt < cutoff {
                    continue;
                }
                let tail = h::tail_utf8(&p, TAIL_BYTES).unwrap_or_default();
                if tail.contains("\"status\": \"completed\"")
                    || tail.contains("\"status\":\"completed\"")
                {
                    continue;
                }
                if let Some(stem) = p.file_stem().and_then(|s| s.to_str()) {
                    out.push(stem.to_string());
                }
            }
        }
    }
    out
}

fn walk_md(root: &Path, name: &str, out: &mut Vec<PathBuf>) {
    let entries = match std::fs::read_dir(root) {
        Ok(e) => e,
        Err(_) => return,
    };
    for entry in entries.flatten() {
        let p = entry.path();
        if p.is_dir() {
            walk_md(&p, name, out);
        } else if p.file_name().and_then(|s| s.to_str()) == Some(name) {
            out.push(p);
        }
    }
}

fn find_inflight_audit_cycles() -> Vec<String> {
    let mut hits = Vec::new();
    let root = audit_root();
    if !root.exists() {
        return hits;
    }
    let now = h::now_secs();
    let cutoff = now.saturating_sub(STALE_SIGNAL_S);
    let mut found = Vec::new();
    walk_md(&root, "AUDIT_INDEX.md", &mut found);
    let home = h::home();
    for p in found {
        let Some(mt) = h::mtime_secs(&p) else {
            continue;
        };
        if mt < cutoff {
            continue;
        }
        let text = match h::read_text(&p) {
            Ok(t) => t,
            Err(_) => continue,
        };
        if text.to_lowercase().contains("in-flight") {
            let rel = p.strip_prefix(&home).unwrap_or(&p);
            hits.push(rel.to_string_lossy().into_owned());
        }
    }
    hits
}

fn wal_active() -> bool {
    let p = wal_path();
    if !p.exists() {
        return false;
    }
    let Some(mt) = h::mtime_secs(&p) else {
        return false;
    };
    if mt < h::now_secs().saturating_sub(STALE_SIGNAL_S) {
        return false;
    }
    let text = match h::read_text(&p) {
        Ok(t) => t,
        Err(_) => return false,
    };
    let head_end = text.char_indices().nth(WAL_HEAD_BYTES).map(|(i, _)| i).unwrap_or(text.len());
    text[..head_end].contains("ACTIVE")
}

fn pending_tasks_count() -> usize {
    let p = tasks_pending();
    if !p.exists() {
        return 0;
    }
    let text = match h::read_text(&p) {
        Ok(t) => t,
        Err(_) => return 0,
    };
    let v: Value = match serde_json::from_str(&text) {
        Ok(v) => v,
        Err(_) => return 0,
    };
    if let Some(arr) = v.as_array() {
        return arr.len();
    }
    if let Some(arr) = v.get("tasks").and_then(Value::as_array) {
        return arr.len();
    }
    0
}

fn main() {
    let _ = h::read_payload();

    let agents = find_inflight_agents();
    let cycles = find_inflight_audit_cycles();
    let wal_dirty = wal_active();
    let n_pending = pending_tasks_count();

    let mut signals: Vec<String> = Vec::new();
    if !agents.is_empty() {
        let head: Vec<&str> = agents.iter().take(6).map(String::as_str).collect();
        signals.push(format!(
            "{} subagent(s) still running: {}",
            agents.len(),
            head.join(", ")
        ));
    }
    if !cycles.is_empty() {
        signals.push(format!(
            "audit cycle workspace marked 'in-flight': {}",
            cycles[0]
        ));
    }
    if wal_dirty {
        signals.push("WAL.md epoch ACTIVE (not closed)".into());
    }
    if n_pending > 0 {
        signals.push(format!(
            "{} pending tasks queued at {}",
            n_pending,
            tasks_pending().display()
        ));
    }

    if signals.is_empty() {
        h::emit_silent();
        return;
    }

    let mut msg = String::from(
        "[AUTONOMOUS CONTINUE GATE]\n\
         Pending work detected. Per `feedback_autonomous-production-default.md`:\n  \
         ∀ active session ⇒ continue-producing = default · ack-w/o-follow-on = failure.\n\n\
         Signals:\n",
    );
    for s in &signals {
        msg.push_str("  · ");
        msg.push_str(s);
        msg.push('\n');
    }
    msg.push_str(
        "\nAction: continue producing on the next turn. Do not idle, do not wait for \
         user approval unless genuinely blocked. If pool is at capacity and you are \
         waiting on agent returns, that IS continuing — but say so explicitly rather \
         than going silent. Orchestrate during dispatch per RSAW Phase 2.5.",
    );

    h::emit_block(&msg);
}
