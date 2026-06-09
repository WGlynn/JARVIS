#!/usr/bin/env python3
"""UserPromptSubmit hook: auto-load MEMORY_WARM_*.md files on situation match.

Background
----------
MEMORY.md was tiered (2026-04-21) into a ~4.8KB HOT layer always loaded, and
8 warm files (~13KB total) that load only when relevant. The HOT layer's
[WARM-MAP] tells Claude which file to Read on match, but that requires Claude
to remember to Read it. This hook automates it: grep the user's prompt for
situation keywords, inject matching warm-file contents as additionalContext.

Contract
--------
- stdin: JSON { prompt, session_id, cwd, ... } (Claude Code UserPromptSubmit payload)
- stdout: JSON { hookSpecificOutput: { hookEventName, additionalContext } }
  — the additionalContext string is prepended to Claude's context for this turn.
- stderr: observability logging (doesn't affect Claude)

Safety
------
- Fails silent on parse/read errors (sys.exit 0). Never blocks the user.
- Caps total injected bytes to MAX_INJECT_BYTES so a multi-hit prompt can't
  flood context (defeats the purpose of the tier split).
- Dedupes: if the same file would be loaded twice, loads once.

Run standalone:
    echo '{"prompt":"working on vibeamm"}' | python memory-warm-loader.py
"""
import json
import os
import sys

MEMORY_DIR = os.path.expanduser("~/.claude/projects/C--Users-Will/memory")
MAX_INJECT_BYTES = 20000  # hard ceiling; if exceeded, rank by keyword-hit count

# Situation → warm-file trigger keywords. All keyword matches are substring,
# case-insensitive. A single keyword hit triggers the file load.
WARM_MAP = {
    # NDA-gated employer context. On these triggers, load the daily-reports rule
    # and employment mandate so future-me knows location + format + cadence.
    "nda-locked/feedback_[REDACTED-NDA]-daily-reports.md": [
        "[REDACTED-NDA]", "[REDACTED-NDA]", "[REDACTED-NDA]", "[REDACTED-NDA]", "[REDACTED-NDA]",
        "daily report", "daily work report", "daily [REDACTED-NDA]", "[REDACTED-NDA] report",
        "[REDACTED-NDA]", "[REDACTED-NDA]", "pre-stage set",
    ],
    "nda-locked/project_[REDACTED-NDA]-[REDACTED-NDA]-mandate.md": [
        "[REDACTED-NDA]", "[REDACTED-NDA]", "[REDACTED-NDA]", "[REDACTED-NDA]",
        "[REDACTED-NDA]", "[REDACTED-NDA]", "[REDACTED-NDA]",
        "deterministic intelligence", "[REDACTED-NDA]",
    ],
    "MEMORY_WARM_TRP.md": [
        "solidity", "vibeamm", "vibe amm", "commitreveal", "commit-reveal",
        "vibeswapcore", "nci", "shardoperatorregistry", "shapleydistributor",
        "crosschainrouter", "trp cycle", "trp round", "audit round",
        "foundry", "forge test", "forge build",
        "layerzero", "oapp", "integration primitive", "phantom array",
        "merkle dispute", "commit-dispute", "rebase-invariant",
        "settlement-time", "batch invariant", "collateral path",
        "post-upgrade init", "deposit identity",
    ],
    "MEMORY_WARM_REVIEW.md": [
        "code review", "self-theater", "audit gate", " rsi",
        "review cycle", "ship gate", "ship-gate",
        "doc drift", "doc/code drift", "8-pass audit",
        "path commitment", "ai-delivered review",
        "self-improvement", "adaptive immunity",
        "dead deps", "deferred showcase",
    ],
    "MEMORY_WARM_GOV.md": [
        "governance", "mechanism design", "bond size", "challenge window",
        "slash split", "voting threshold", "axiom gate", "p-001",
        "token architecture", "three-token", "3-token", "three token",
        "constitutional", "extractive load", "gev resistance",
        "zero fee", "cincinnatus", "disintermediation",
        "augmented governance", "citation hygiene", "anti-hallucination",
        "substrate-geometry", "substrate geometry", "fractal scaling",
        "golden ratio", "natural form", "mechanism-fit",
        "first-available", "path b", "as above so below",
        "ultimate design principle",
    ],
    "MEMORY_WARM_PERF.md": [
        "performance", "latency", "optimize", "optimization",
        "bottleneck", "nc-max", "speculative execution",
        "observer effect", "optimistic ui", "durability split",
        "superlinear", "scaling",
    ],
    "MEMORY_WARM_COMPRESS.md": [
        "compress", "compression", "context explosion", "reboot",
        "memory.md", "token budget", "glyph", "tier split",
        "hot/warm", "hot-warm", "recall floor", "symbolic compression",
    ],
    "MEMORY_WARM_ARCHIVE.md": [
        "philosophical", "convergence thesis", "parallelism convergence",
        "jarvis independence", "rosetta covenant", "graceful inversion",
        "eliminate, don't optimize", "game theory primitive",
        "web3 security", "ethsecurity", "pashov", "medium rollout",
        "outreach",
    ],
    "MEMORY_WARM_RECENT.md": [
        "anthropic unresponsive", "cogcoin", "mit bitcoin", "cogproof",
        "job search", "nci three-token", "jarvis bot rsi",
        "oracle audit", "fee architecture", "deepfunding",
        "marketing rollout", "allium", "lawson floor", "trp tier",
    ],
    "MEMORY_WARM_PEOPLE.md": [
        "ashwin", "deepfunding", "tadija", "vedant", "edith",
        "jay berg", "sidepit", "dlob", "first-available trap",
    ],
}


def score_prompt(prompt_lower: str) -> list[tuple[str, int]]:
    """Return [(filename, hit_count)] sorted by hit_count desc, excluding zeros."""
    scores = []
    for fname, kws in WARM_MAP.items():
        hits = sum(1 for kw in kws if kw in prompt_lower)
        if hits > 0:
            scores.append((fname, hits))
    scores.sort(key=lambda t: -t[1])
    return scores


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception as e:
        print(f"[memory-warm-loader] stdin parse failed: {e}", file=sys.stderr)
        sys.exit(0)

    prompt = (payload.get("prompt") or "").lower()
    if not prompt:
        sys.exit(0)

    ranked = score_prompt(prompt)
    if not ranked:
        sys.exit(0)

    chunks: list[str] = []
    total = 0
    loaded: list[str] = []

    for fname, hits in ranked:
        path = os.path.join(MEMORY_DIR, fname)
        if not os.path.exists(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"[memory-warm-loader] read {fname} failed: {e}", file=sys.stderr)
            continue
        if total + len(content) > MAX_INJECT_BYTES:
            print(
                f"[memory-warm-loader] skip {fname} (would exceed {MAX_INJECT_BYTES}B cap)",
                file=sys.stderr,
            )
            continue
        chunks.append(f"<memory-warm file='{fname}' hits={hits}>\n{content}\n</memory-warm>")
        total += len(content)
        loaded.append(f"{fname}({hits})")

    if not chunks:
        sys.exit(0)

    additional = (
        "Situation-matched warm memory loaded (from MEMORY.md [WARM-MAP] auto-loader):\n\n"
        + "\n".join(chunks)
    )

    out = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": additional,
        }
    }
    print(json.dumps(out))
    print(f"[memory-warm-loader] loaded: {', '.join(loaded)} ({total}B)", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
