#!/usr/bin/env python3
"""
Layer 8 Audit — filesystem-substrate integrity check for the JARVIS substrate.

Layers 0-7 of JARVIS cover LLM gen / hooks / context reflection / discipline /
meta-loop / self-observation. Layer 8 = the filesystem substrate underneath
all of that. If the filesystem references are rotten, every higher layer
degrades silently.

Categories audited:
  1. Broken inter-primitive references (filename + [X.slug] shortcodes)
  2. Broken hook script references in settings.json
  3. Broken file-path references inside primitive bodies
  4. Orphan hooks (on disk but not wired into settings.json)
  5. Cron-prompt -> script path validity

Does NOT duplicate link-rot-detector.py (which handles MEMORY.md index <-> file
orphan detection at the index level).

Output:
  - stdout: summary table + top findings
  - report.md: full report grouped by category, capped at 200 lines
              (truncate-and-count tail marker)

Idempotent. Re-run safe. Skips nda-locked/ and .git/.
Stdlib only. Python 3.10+.
"""

from __future__ import annotations

import json
import os
import re
import sys
import traceback
from dataclasses import dataclass, field
from pathlib import Path

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #

CLAUDE_DIR = Path("~/.claude")
MEMORY_DIR = CLAUDE_DIR / "projects" / "C--Users-Will" / "memory"
HOOKS_DIR = CLAUDE_DIR / "hooks"
SESSION_CHAIN_DIR = CLAUDE_DIR / "session-chain"
CRON_DIR = CLAUDE_DIR / "cron-prompts"
SETTINGS_JSON = CLAUDE_DIR / "settings.json"

SELF_DIR = HOOKS_DIR / "layer8-audit"
REPORT_PATH = SELF_DIR / "report.md"

MAX_REPORT_LINES = 200

SKIP_DIR_NAMES = {"nda-locked", ".git", "__pycache__", "_archive", "backups"}

# --------------------------------------------------------------------------- #
# Regex
# --------------------------------------------------------------------------- #

# [P.slug] style HIERO shortcodes. The middot is U+00B7. We accept both
# middot (.) and a plain dot/period as fallback in case files drift.
SHORTCODE_RE = re.compile(r"\[([A-Z])[·.]([a-z0-9][a-z0-9-]*)\]")

# Bare primitive filename references like primitive_foo.md or feedback_bar.md.
PRIMITIVE_FILENAME_RE = re.compile(
    r"\b((?:primitive|feedback|project|reference|user|judgment|relation|fact|opinion)_[a-z0-9][a-z0-9-]*\.md)\b"
)

# Backticked path-ish strings. We pull anything that looks like a file path
# referencing ~/.claude/... or ~/.claude/... or relative
# hook/session-chain/cron-prompts paths.
PATH_IN_BACKTICKS_RE = re.compile(r"`([^`\n]+?)`")

PATH_HINT_RE = re.compile(
    r"(?:^|[\s(])("
    r"(?:~/|~/|~/|\./)?\.claude/[A-Za-z0-9_./-]+"
    r")"
)

# Type prefix -> glyph mapping for shortcode validation. We treat the type
# prefix as a hint and look for the slug in any matching memory file.
TYPE_PREFIX = {
    "U": ("user",),
    "F": ("feedback",),
    "P": ("primitive",),
    "J": ("project",),
    "R": ("reference",),
    "M": ("memory",),
    "O": ("primitive", "feedback"),  # observed used loosely
    "A": ("primitive", "feedback"),
}

# --------------------------------------------------------------------------- #
# Data
# --------------------------------------------------------------------------- #


@dataclass
class Finding:
    category: str
    file: str
    line: int
    reference: str
    detail: str = ""

    def fmt(self) -> str:
        loc = f"{self.file}:{self.line}"
        extra = f"  ({self.detail})" if self.detail else ""
        return f"- {loc}: `{self.reference}`{extra}"


@dataclass
class Report:
    findings: dict[str, list[Finding]] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    def add(self, f: Finding) -> None:
        self.findings.setdefault(f.category, []).append(f)

    def add_error(self, category: str, exc: BaseException) -> None:
        msg = f"[{category}] {type(exc).__name__}: {exc}"
        self.errors.append(msg)

    def total(self) -> int:
        return sum(len(v) for v in self.findings.values())


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def fs_display(p: Path | str) -> str:
    """Forward-slash display path. Always absolute when given a Path."""
    s = str(p)
    return s.replace("\\", "/")


def skip(p: Path) -> bool:
    parts = set(p.parts)
    return bool(parts & SKIP_DIR_NAMES)


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def iter_lines(p: Path):
    text = read_text(p)
    for i, ln in enumerate(text.splitlines(), 1):
        yield i, ln


def list_memory_files() -> list[Path]:
    out = []
    for child in MEMORY_DIR.iterdir():
        if child.is_dir():
            continue
        if child.suffix != ".md":
            continue
        out.append(child)
    return out


def primitive_index() -> dict[str, Path]:
    """
    Map slug -> file path for every primitive-ish memory file.
    Slug = filename without the type prefix and .md suffix.
    """
    idx: dict[str, Path] = {}
    for p in list_memory_files():
        stem = p.stem
        if "_" not in stem:
            # bare-stem file (e.g., autopilot-loop.md) — index by full stem
            idx[stem] = p
            continue
        prefix, _, slug = stem.partition("_")
        if prefix in {
            "primitive", "feedback", "project", "reference",
            "user", "judgment", "relation", "fact", "opinion",
            "protocol",
        }:
            # Last writer wins; conflicts here are upstream's problem.
            idx[slug] = p
    return idx


def filename_index() -> set[str]:
    return {p.name for p in list_memory_files()}


def resolve_path_hint(raw: str) -> Path | None:
    """
    Turn a textual path reference into an absolute Path.
    Returns None if it doesn't look like something we can check.
    """
    s = raw.strip().strip(".,;:)")
    if not s:
        return None

    # Trim trailing markdown punctuation
    while s and s[-1] in "`'\")":
        s = s[:-1]

    # Normalize separators for parsing
    s_fwd = s.replace("\\", "/")

    if s_fwd.startswith("~/.claude/"):
        return CLAUDE_DIR / s_fwd[len("~/.claude/"):]
    if s_fwd.startswith("~/"):
        return Path("C:/Users/Will") / s_fwd[2:]
    if s_fwd.startswith("~/.claude/"):
        return CLAUDE_DIR / s_fwd[len("~/.claude/"):]
    if s_fwd.startswith("~/.claude/"):
        return CLAUDE_DIR / s_fwd[len("~/.claude/"):]
    if s_fwd.startswith(".claude/"):
        return CLAUDE_DIR / s_fwd[len(".claude/"):]
    return None


def looks_like_claude_path(s: str) -> bool:
    s_fwd = s.replace("\\", "/")
    return (
        ".claude/" in s_fwd
        and (s_fwd.endswith(".py") or s_fwd.endswith(".md") or s_fwd.endswith(".json")
             or s_fwd.endswith(".sh") or s_fwd.endswith(".bat") or s_fwd.endswith(".vbs"))
    )


# --------------------------------------------------------------------------- #
# settings.json hook extraction
# --------------------------------------------------------------------------- #


def load_settings() -> dict:
    try:
        return json.loads(SETTINGS_JSON.read_text(encoding="utf-8"))
    except Exception:
        return {}


def extract_hook_commands(settings: dict) -> list[tuple[str, str]]:
    """
    Returns list of (event_name, command_string) tuples. Walks the
    hooks.* tree generically so future event types are covered.
    """
    out: list[tuple[str, str]] = []
    hooks = settings.get("hooks", {})
    if not isinstance(hooks, dict):
        return out
    for event_name, entries in hooks.items():
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            for h in entry.get("hooks", []) or []:
                if not isinstance(h, dict):
                    continue
                cmd = h.get("command")
                if isinstance(cmd, str) and cmd.strip():
                    out.append((event_name, cmd.strip()))
    return out


def extract_script_path_from_command(cmd: str) -> Path | None:
    """
    Hook commands look like 'python C:/.../foo.py arg1 arg2'. Pull the
    first token that resolves to a real-ish .py path.
    """
    toks = cmd.split()
    if not toks:
        return None
    candidates = [t for t in toks if t.endswith(".py") or t.endswith(".sh") or t.endswith(".bat")]
    if not candidates:
        return None
    p = resolve_path_hint(candidates[0])
    if p is not None:
        return p
    # Fall back to literal interpretation
    return Path(candidates[0])


# --------------------------------------------------------------------------- #
# Category 1 — broken inter-primitive references
# --------------------------------------------------------------------------- #


def audit_primitive_refs(report: Report) -> None:
    cat = "1. Broken inter-primitive references"
    try:
        slug_idx = primitive_index()
        fname_idx = filename_index()
        for p in list_memory_files():
            if skip(p):
                continue
            for lineno, ln in iter_lines(p):
                # Shortcodes
                for m in SHORTCODE_RE.finditer(ln):
                    prefix, slug = m.group(1), m.group(2)
                    # Whitelist of slugs we know are conceptual, not files.
                    # Most named shortcodes should resolve to a memory file.
                    if slug in slug_idx:
                        continue
                    # Unknown slug — record.
                    report.add(Finding(
                        category=cat,
                        file=fs_display(p),
                        line=lineno,
                        reference=m.group(0),
                        detail=f"no memory file for slug '{slug}'",
                    ))
                # Bare filename refs
                for m in PRIMITIVE_FILENAME_RE.finditer(ln):
                    fname = m.group(1)
                    if fname in fname_idx:
                        continue
                    report.add(Finding(
                        category=cat,
                        file=fs_display(p),
                        line=lineno,
                        reference=fname,
                        detail="primitive filename not found",
                    ))
    except Exception as exc:
        report.add_error(cat, exc)


# --------------------------------------------------------------------------- #
# Category 2 — broken hook script references in settings.json
# --------------------------------------------------------------------------- #


def audit_settings_hooks(report: Report) -> None:
    cat = "2. Broken hook scripts in settings.json"
    try:
        settings = load_settings()
        cmds = extract_hook_commands(settings)
        # We don't have line numbers from the parsed json — approximate by
        # scanning the raw text for the command string.
        raw = SETTINGS_JSON.read_text(encoding="utf-8", errors="replace").splitlines()
        for event, cmd in cmds:
            script = extract_script_path_from_command(cmd)
            if script is None:
                continue
            if script.exists():
                continue
            # Find line number by substring match (best-effort).
            line = 0
            needle = cmd.split()[1] if len(cmd.split()) > 1 else cmd
            for i, ln in enumerate(raw, 1):
                if needle in ln:
                    line = i
                    break
            report.add(Finding(
                category=cat,
                file=fs_display(SETTINGS_JSON),
                line=line,
                reference=cmd,
                detail=f"{event}: script not found at {fs_display(script)}",
            ))
    except Exception as exc:
        report.add_error(cat, exc)


# --------------------------------------------------------------------------- #
# Category 3 — broken file-path refs inside primitives
# --------------------------------------------------------------------------- #


def audit_paths_in_primitives(report: Report) -> None:
    cat = "3. Broken file-path refs in primitives"
    try:
        for p in list_memory_files():
            if skip(p):
                continue
            for lineno, ln in iter_lines(p):
                # Pull backticked tokens AND the path-hint regex; dedupe.
                seen: set[str] = set()
                candidates: list[str] = []
                for m in PATH_IN_BACKTICKS_RE.finditer(ln):
                    candidates.append(m.group(1))
                for m in PATH_HINT_RE.finditer(ln):
                    candidates.append(m.group(1))
                for raw in candidates:
                    if raw in seen:
                        continue
                    seen.add(raw)
                    if not looks_like_claude_path(raw):
                        continue
                    resolved = resolve_path_hint(raw)
                    if resolved is None:
                        continue
                    if resolved.exists():
                        continue
                    report.add(Finding(
                        category=cat,
                        file=fs_display(p),
                        line=lineno,
                        reference=raw,
                        detail=f"resolved -> {fs_display(resolved)} (missing)",
                    ))
    except Exception as exc:
        report.add_error(cat, exc)


# --------------------------------------------------------------------------- #
# Category 4 — orphan hooks (on disk but not wired into settings.json)
# --------------------------------------------------------------------------- #


def audit_orphan_hooks(report: Report) -> None:
    cat = "4. Orphan hooks (on disk, not in settings.json)"
    try:
        settings = load_settings()
        cmds = extract_hook_commands(settings)
        wired: set[str] = set()
        for _event, cmd in cmds:
            for tok in cmd.split():
                if tok.endswith(".py") or tok.endswith(".sh") or tok.endswith(".bat"):
                    p = resolve_path_hint(tok)
                    if p is not None:
                        wired.add(fs_display(p.resolve() if p.exists() else p))
                    else:
                        wired.add(fs_display(Path(tok)))

        hook_dirs = [HOOKS_DIR, SESSION_CHAIN_DIR]
        for hd in hook_dirs:
            if not hd.exists():
                continue
            for child in hd.iterdir():
                if not child.is_file():
                    continue
                if child.suffix != ".py":
                    continue
                # Skip private/helper modules (leading underscore).
                if child.name.startswith("_"):
                    continue
                # Skip self.
                if child.resolve() == (SELF_DIR / "layer8_audit.py").resolve():
                    continue
                disp = fs_display(child)
                disp_resolved = fs_display(child.resolve())
                if disp in wired or disp_resolved in wired:
                    continue
                report.add(Finding(
                    category=cat,
                    file=fs_display(hd),
                    line=0,
                    reference=child.name,
                    detail="hook present on disk; no settings.json command references it",
                ))
    except Exception as exc:
        report.add_error(cat, exc)


# --------------------------------------------------------------------------- #
# Category 5 — cron-prompt -> script path validity
# --------------------------------------------------------------------------- #


def audit_cron_prompts(report: Report) -> None:
    cat = "5. Cron-prompt script path validity"
    try:
        if not CRON_DIR.exists():
            return
        for p in CRON_DIR.iterdir():
            if not p.is_file():
                continue
            if p.suffix != ".md":
                continue
            for lineno, ln in iter_lines(p):
                seen: set[str] = set()
                candidates: list[str] = []
                for m in PATH_IN_BACKTICKS_RE.finditer(ln):
                    candidates.append(m.group(1))
                for m in PATH_HINT_RE.finditer(ln):
                    candidates.append(m.group(1))
                for raw in candidates:
                    if raw in seen:
                        continue
                    seen.add(raw)
                    if not looks_like_claude_path(raw):
                        continue
                    resolved = resolve_path_hint(raw)
                    if resolved is None or resolved.exists():
                        continue
                    report.add(Finding(
                        category=cat,
                        file=fs_display(p),
                        line=lineno,
                        reference=raw,
                        detail=f"resolved -> {fs_display(resolved)} (missing)",
                    ))
    except Exception as exc:
        report.add_error(cat, exc)


# --------------------------------------------------------------------------- #
# Report writer
# --------------------------------------------------------------------------- #


CATEGORY_ORDER = [
    "1. Broken inter-primitive references",
    "2. Broken hook scripts in settings.json",
    "3. Broken file-path refs in primitives",
    "4. Orphan hooks (on disk, not in settings.json)",
    "5. Cron-prompt script path validity",
]


def render_report(report: Report) -> str:
    lines: list[str] = []
    lines.append("# Layer 8 Audit Report")
    lines.append("")
    lines.append("Filesystem-substrate integrity check for the JARVIS memory + hook substrate.")
    lines.append("")

    # Summary table
    lines.append("## Summary")
    lines.append("")
    lines.append("| # | Category | Findings |")
    lines.append("|---|----------|---------:|")
    for cat in CATEGORY_ORDER:
        n = len(report.findings.get(cat, []))
        lines.append(f"| {cat[0]} | {cat[3:]} | {n} |")
    lines.append(f"| - | **TOTAL** | **{report.total()}** |")
    lines.append("")

    if report.errors:
        lines.append("## Errors during audit")
        lines.append("")
        for e in report.errors:
            lines.append(f"- {e}")
        lines.append("")

    # Findings grouped
    for cat in CATEGORY_ORDER:
        items = report.findings.get(cat, [])
        lines.append(f"## {cat}  ({len(items)})")
        lines.append("")
        if not items:
            lines.append("_clean_")
            lines.append("")
            continue
        for f in items:
            lines.append(f.fmt())
        lines.append("")

    # Truncate to MAX_REPORT_LINES.
    if len(lines) > MAX_REPORT_LINES:
        kept = lines[: MAX_REPORT_LINES - 1]
        dropped = len(lines) - len(kept)
        kept.append(f"... [truncated: +{dropped} more lines]")
        lines = kept

    return "\n".join(lines) + "\n"


def render_summary_stdout(report: Report) -> str:
    rows = []
    rows.append("Layer 8 Audit  (filesystem-substrate integrity)")
    rows.append("=" * 48)
    for cat in CATEGORY_ORDER:
        n = len(report.findings.get(cat, []))
        rows.append(f"  {cat:<55} {n:>5}")
    rows.append("-" * 48)
    rows.append(f"  {'TOTAL':<55} {report.total():>5}")
    if report.errors:
        rows.append("")
        rows.append(f"  errors: {len(report.errors)}")
        for e in report.errors:
            rows.append(f"    - {e}")
    rows.append("")
    rows.append(f"  report: {fs_display(REPORT_PATH)}")
    return "\n".join(rows)


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #


def main() -> int:
    report = Report()

    audits = [
        audit_primitive_refs,
        audit_settings_hooks,
        audit_paths_in_primitives,
        audit_orphan_hooks,
        audit_cron_prompts,
    ]
    for fn in audits:
        try:
            fn(report)
        except Exception as exc:  # never abort the whole audit
            report.add_error(fn.__name__, exc)
            traceback.print_exc(file=sys.stderr)

    # Ensure output dir exists; write report.
    SELF_DIR.mkdir(parents=True, exist_ok=True)
    try:
        REPORT_PATH.write_text(render_report(report), encoding="utf-8")
    except Exception as exc:
        print(f"layer8_audit: could not write report: {exc}", file=sys.stderr)

    print(render_summary_stdout(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
