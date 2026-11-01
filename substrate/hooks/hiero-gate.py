#!/usr/bin/env python3
"""Memory readability gate — PreToolUse hook for memory writes.

2026-07-20 reversal (Will): "I'm done with the Glyph symbols because it just makes my code
unreadable." The old HIERO gate FORCED glyph/operator density on every memory write. That
requirement is retired: plain-language memories are now first-class, and the token data already
killed HIERO's density rationale (glyphs measured net-negative at ~2.03 tok/glyph).

This gate no longer blocks. It stays only as a light, non-blocking nudge in the NEW direction:
if a memory write is glyph-HEAVY, it emits a gentle reminder to prefer plain words. Frontmatter
(name + description) is likewise a soft nudge, never a block. Fail-open on anything unexpected.
"""
import sys
import json
import re


def emit_note(msg):
    """Non-blocking advisory: print to stderr, exit 0 (the write proceeds)."""
    print(msg, file=sys.stderr)
    sys.exit(0)


try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)  # malformed input -> don't interfere

if data.get("tool_name", "") not in ("Write", "Edit"):
    sys.exit(0)

tool_input = data.get("tool_input", {})
if not isinstance(tool_input, dict):
    sys.exit(0)
file_path = tool_input.get("file_path", "") or ""

MEMORY_PATTERNS = [
    r"[/\\]memory[/\\].*\.md$",
    r"GKB.*\.md$",
    r"SKB.*\.md$",
    r"JarvisxWill_.*\.md$",
]
if not any(re.search(p, file_path, re.IGNORECASE) for p in MEMORY_PATTERNS):
    sys.exit(0)

content = tool_input.get("content") or tool_input.get("new_string", "") or ""
if len(content.strip()) < 200:
    sys.exit(0)

# Strip frontmatter for the body analysis.
body = re.sub(r"^---\n.*?\n---\n", "", content, count=1, flags=re.DOTALL)
words = len(re.findall(r"\b\w+\b", body))
if words < 40:
    sys.exit(0)

# The new direction: prefer plain language. Nudge (never block) if the write is glyph-heavy,
# i.e. leaning on operators/arrows/status-emoji as prose shorthand instead of words.
GLYPHS = re.compile(r"[⇒⇔¬∧∨∈∉⊂⊆→↦↑↓✓✗⊥⊤⊘•†×∀∃∴∵≡≠≥≤·✅🟡🔬⚑⚠▶◐←↔]")
glyph_hits = len(GLYPHS.findall(body))
glyph_density = glyph_hits / max(1, words)

if glyph_density > 0.03 and glyph_hits > 8:
    emit_note(
        "Readability nudge (non-blocking): this memory is glyph-heavy "
        f"({glyph_hits} glyphs / {words} words). Will 2026-07-20 prefers plain words over "
        "symbols ('done with the glyph symbols; it just makes my code unreadable'). "
        "Consider: 'then/implies' over arrows, 'built/designed/open' over status emoji, "
        "words over operators. Writing anyway; this is only a reminder."
    )

# Light structural nudge: memories are indexed by name + description.
if "name:" not in content[:400] or "description:" not in content[:400]:
    emit_note(
        "Note (non-blocking): memory frontmatter should carry `name:` and `description:` "
        "so the index can find it. Writing anyway."
    )

sys.exit(0)
