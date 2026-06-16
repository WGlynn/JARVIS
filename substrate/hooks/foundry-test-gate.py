#!/usr/bin/env python3
"""foundry-test-gate.py — PreToolUse(Bash) gate enforcing the VibeSwap Foundry rule.

Derived from OUR build (VibeSwap, Ryzen 5 1600 / 16GB): the CLAUDE.md hard rule
"NEVER `forge test` without --match-path or --match-contract" (full 80+ file suite
OOMs the box, esp. with parallel agents). Per [P.always-equals-gate] a "NEVER" must
live as a deterministic gate, not as prose in memory; per [F.jarvis-anthropic-design-convergence]
a JARVIS gate == a harness PreToolUse hook. Bottleneck dissolved: OOM from an
unscoped forge test ([F.primitives-are-bottleneck-dissolutions]).

Block decision uses exit code 2 (+ stderr), NOT JSON additionalContext, per
[P.stop-event-schema-restriction] (avoid fragile hook-output schemas).

Contract:
  stdin  : PreToolUse event JSON { tool_name, tool_input:{ command } }
  exit 0 : allow (not Bash, not a forge test, or properly scoped)
  exit 2 : block (bare forge test) — stderr carries the reason
"""
import json
import re
import sys

# A real `forge test` invocation at command position: start, after a shell
# separator (; && || | & ( newline), or after an ENV=val assignment prefix
# (e.g. FOUNDRY_PROFILE=ci forge test). Deliberately does NOT match `forge test`
# sitting inside a quoted string like `git commit -m "forge test fix"`.
FORGE_TEST = re.compile(r"(?:^|[;&|(\n]|[A-Za-z_][A-Za-z0-9_]*=\S+\s)\s*\bforge\s+test\b")
# Any scoping/safe flag that makes the run bounded -> allowed.
SCOPED = re.compile(
    r"--match-path|--match-contract|--match-test|--mp\b|--mc\b|--mt\b|--list|--help|-h\b"
)


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0  # never block on a parse failure — fail open for safety of UX

    if event.get("tool_name") != "Bash":
        return 0
    cmd = (event.get("tool_input") or {}).get("command", "") or ""

    if not FORGE_TEST.search(cmd):
        return 0
    if SCOPED.search(cmd):
        return 0

    sys.stderr.write(
        "BLOCKED: bare `forge test` detected.\n"
        "VibeSwap rule (CLAUDE.md): NEVER run `forge test` without --match-path or "
        "--match-contract. The 80+ file suite OOMs this box (Ryzen 5 1600 / 16GB), "
        "especially with parallel agents.\n"
        "Fix: scope it, e.g. `forge test --match-path test/SomeTest.t.sol -vvv` or "
        "`forge test --match-contract VibeAMM`. (Add --list to just enumerate.)\n"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
