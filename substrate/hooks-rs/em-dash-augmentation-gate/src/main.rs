// PostToolUse hook port. Scan partner-facing drafts for em-dash (U+2014)
// and en-dash (U+2013); emit augmentation context if any present.
// Source: ~/.claude/hooks/em-dash-augmentation-gate.py

use jarvis_hook as h;
use regex::Regex;

const PARTNER_FACING_PATTERNS: &[&str] = &[
    r"/desktop/[^/]*[_-]reply[-_.]",
    r"/desktop/[^/]*[_-]draft[-_.]",
    r"/desktop/outreach[_-]",
    r"/desktop/outreach_pitches/",
    r"/desktop/usd8[_-]",
    r"/desktop/kim[_-]",
    r"/desktop/bernhard[_-]",
    r"/desktop/tom[_-]",
    r"/desktop/rick[_-]",
    r"/desktop/anthropic[_-]",
    r"/desktop/[REDACTED-NDA][_-]",
    r"/desktop/jp[_-]",
    r"/desktop/[0-9]{4}-[0-9]{2}-[0-9]{2}_[^/]*linkedin",
    r"/desktop/[0-9]{4}-[0-9]{2}-[0-9]{2}_[^/]*medium",
    r"/desktop/[0-9]{4}-[0-9]{2}-[0-9]{2}_[^/]*ethresearch",
    r"/desktop/[0-9]{4}-[0-9]{2}-[0-9]{2}_[^/]*email",
    r"/desktop/[0-9]{4}-[0-9]{2}-[0-9]{2}_[^/]*letter",
    r"/desktop/ethresearch[_-]",
    r"/desktop/medium[_-]",
    r"/desktop/linkedin[_-]",
    r"/desktop/telegram[_-]",
    r"/desktop/[^/]*[_-]pitch[-_.]",
    r"/desktop/[^/]*[_-]letter[-_.]",
    r"/desktop/[^/]*[_-]email[-_.]",
    r"/desktop/[^/]*[_-]message[-_.]",
    r"/desktop/[^/]*[_-]post[-_.]",
    r"/desktop/[^/]*[_-]thread[-_.]",
    r"/desktop/[^/]*[_-]dm[-_.]",
];

fn build_regexes() -> Vec<Regex> {
    PARTNER_FACING_PATTERNS
        .iter()
        .filter_map(|p| Regex::new(p).ok())
        .collect()
}

fn is_partner_facing(path: &str, res: &[Regex]) -> bool {
    if path.is_empty() {
        return false;
    }
    let norm = path.replace('\\', "/").to_lowercase();
    res.iter().any(|r| r.is_match(&norm))
}

fn count_em_dashes(s: &str) -> usize {
    s.matches('\u{2014}').count() + s.matches('\u{2013}').count()
}

fn main() {
    let p = h::read_payload();
    if p.hook_event_name != "PostToolUse" {
        h::emit_silent();
        return;
    }
    let tool = p.tool_name.as_str();
    if !matches!(tool, "Write" | "Edit" | "NotebookEdit") {
        h::emit_silent();
        return;
    }
    let path = p.ti_str("file_path");
    let res = build_regexes();
    if !is_partner_facing(path, &res) {
        h::emit_silent();
        return;
    }
    let content = match tool {
        "Write" => p.ti_str("content"),
        "Edit" => p.ti_str("new_string"),
        "NotebookEdit" => p.ti_str("new_source"),
        _ => "",
    };
    let count = count_em_dashes(content);
    if count == 0 {
        h::emit_silent();
        return;
    }
    let msg = format!(
        "[EM-DASH AUGMENTATION GATE] {count} em-dash(es) detected in \
         partner-facing draft at {path}. Per [F·em-dash-filter-for-conversations], \
         partner-facing drafts must filter em-dashes before delivery. \
         Replace with comma, period, colon, or parens depending on context: \
         mid-clause em-dash -> comma or sentence-split; parenthetical em-dash -> parens; \
         range/connection em-dash -> 'to'/'vs' or split. \
         Edit the file to scrub before the user paste-sends. \
         This gate augments awareness, it does not block the write."
    );
    h::emit_additional_context("PostToolUse", &msg);
}
