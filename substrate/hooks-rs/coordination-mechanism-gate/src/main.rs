// PreToolUse hook port. Classify Agent spawn description → recommend
// cheaper tier when applicable. Downgrade-only (conservative).
// Source: ~/.claude/hooks/coordination-mechanism-gate.py

use jarvis_hook as h;
use regex::Regex;

const TRIVIAL: &[&str] = &[
    r"\b(list|count|show|print|read|fetch|get|check)\s+\w+\b",
    r"\b(weather|date|time|status|version)\b",
    r"\b(rename|move|copy|delete) (a |the )?file\b",
];

const SUBSTANTIVE: &[&str] = &[
    r"\b(design|architecture|spec|implement|build|refactor|migrate)\b",
    r"\b(security|audit|verification|formal)\b",
    r"\b(multi-step|cross-?cut|plan|strategy|roadmap)\b",
    r"\b(comparison|side-by-side|landscape|survey)\b",
];

fn tier_rank(t: &str) -> Option<u8> {
    match t {
        "haiku" => Some(0),
        "sonnet" => Some(1),
        "opus" => Some(2),
        _ => None,
    }
}

fn first_match<'a>(pats: &'a [&'a str], hay: &str) -> Option<&'a str> {
    for p in pats {
        if let Ok(re) = Regex::new(p) {
            if re.is_match(hay) {
                return Some(p);
            }
        }
    }
    None
}

fn classify(d: &str) -> (&'static str, String) {
    let dl = d.to_lowercase();
    if let Some(p) = first_match(SUBSTANTIVE, &dl) {
        return ("opus", p.to_string());
    }
    if let Some(p) = first_match(TRIVIAL, &dl) {
        return ("haiku", p.to_string());
    }
    if d.chars().count() < 80 {
        return ("haiku", "short description (<80 char)".into());
    }
    ("sonnet", "default mid-tier".into())
}

fn main() {
    let p = h::read_payload();
    let desc = p.ti_str("description");
    if desc.is_empty() {
        h::emit_silent();
        return;
    }
    let (rec, why) = classify(desc);
    let actual_raw = p.ti_str("model");
    let actual = if actual_raw.is_empty() {
        "sonnet".to_string()
    } else {
        actual_raw.to_lowercase()
    };
    if actual == rec {
        h::emit_silent();
        return;
    }
    let (Some(ar), Some(rr)) = (tier_rank(&actual), tier_rank(rec)) else {
        h::emit_silent();
        return;
    };
    if rr >= ar {
        h::emit_silent();
        return;
    }
    let head: String = desc.chars().take(120).collect();
    let msg = format!(
        "[COORDINATION-MECHANISM GATE]\n\
         Agent spawn: {head}\n\
         Cost-saving opportunity: {actual} → {rec} ({why})\n\
         Set model={rec} if task is genuinely this trivial. Augmentation only; proceed if classifier is wrong."
    );
    h::emit_additional_context("PreToolUse", &msg);
}
