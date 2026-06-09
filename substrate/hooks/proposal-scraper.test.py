#!/usr/bin/env python3
"""
Tests for proposal-scraper.py. Run: python proposal-scraper.test.py

Each case is a regression fence. Case 2 + Case 3 were added 2026-04-15 after the
scraper false-positived on its own completion summary. Don't delete them.
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("proposal_scraper", HERE / "proposal-scraper.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
looks_like_proposal = mod.looks_like_proposal

passed = 0
failed = 0


def test(name, text, expected):
    global passed, failed
    actual = looks_like_proposal(text)
    mark = "PASS" if actual == expected else "FAIL"
    if actual == expected:
        passed += 1
    else:
        failed += 1
    print(f"  {mark} {name}  (expected={expected}, got={actual})")


print("\nProposal Scraper Tests\n")

# ---- MUST TRIGGER ----

test(
    "Case 1: Cycle-11 style with C{N}-{A-Z} labels",
    """Full-Stack RSI — Cycle 11 options:

- **C11-A**: Fresh scope — audit NCI again
- **C11-B**: Property-based fuzzing — offCirculation invariants
- **C11-C**: Meta-audit — review the C9/C10 fixes themselves
- **C11-D**: Extend challenge-response pattern to other metrics

Which of these is the next loop?""",
    True,
)

test(
    "Case 2: explicit **Option A** / **Option B** headers",
    """Three angles to consider:

**Option A**: Wire directly into the existing chain
**Option B**: Opt-in wrapper on send sites only
**Option C**: Skip wiring, run as advisory only""",
    True,
)

test(
    "Case 3: prose 'Option A:' style",
    """Two paths:

Option A: rebuild from scratch with the new primitive
Option B: keep existing code, add a shim layer""",
    True,
)

test(
    "Case 4: numbered bold + keyword 'options'",
    """Four options for the next loop:

1. **Fresh NCI audit** — rebase-invariance check
2. **Property-based fuzzing** — off-circulation invariants
3. **Meta-audit** — review C9/C10 patches
4. **Generalization** — extend challenge-response

Pick one to start.""",
    True,
)

test(
    "Case 5: numbered bold + keyword 'propose'",
    """I propose three directions:

1. **Add logging** to the gate
2. **Extend coverage** to degen persona
3. **Wire into send sites** once you approve""",
    True,
)

# ---- MUST NOT TRIGGER ----

test(
    "Case 6: the 2026-04-15 false positive (completion summary with numbered bold list, no keyword)",
    """Done. Summary of decisions taken and what's live:

**What's in `src/` now (live files, behavior-affecting):**
- **`src/persona.js`** — patched. Universal structural rules spliced into all 4 personas.
- **`src/voice-gate.js`** — importable post-draft filter, persona-aware.
- **`src/voice-gate.test.js`** — **10/10 passing**.

**Decisions I made on your behalf:**
1. **Not auto-wired** at send sites. Gate is importable; wiring is your call.
2. **`src/` is single source of truth.** Deleted the staging copy.
3. **Persona split**: structural rules universal, voice rules standard-only.

**To go live:** add ~10 lines from the README wiring example.""",
    False,
)

test(
    "Case 7: diagnostic prose (no numbered list, no explicit labels)",
    """The scraper ate its own tail. Response had structured bullets which match the
numbered-bold heuristic. Fix: require keyword proximity. Classic every-hammer-sees-nails.""",
    False,
)

test(
    "Case 8: single numbered bold line (insufficient structure)",
    """Quick note:

1. **Ship it** and move on.""",
    False,
)

test(
    "Case 9: ordinary message with the word 'option' but no structure",
    "I think option A from yesterday is still the right call, let's do that.",
    False,
)

test(
    "Case 10: empty / short input",
    "",
    False,
)

test(
    "Case 11: structured prose with plain bullets, no numbering, no keyword",
    """Here's what I did:
- Patched persona.js
- Added voice-gate module
- Wrote smoke tests""",
    False,
)

test(
    "Case 12: documentation example mentioning **C11-A** inside backticks (2nd false positive, 2026-04-15)",
    """Patched proposal-scraper.py: strong patterns still auto-trigger on explicit
option labels (`**Option A**`, `**C11-A**`, `Option A:`). The numbered-bold-list
heuristic is now demoted. Cleaned PROPOSALS.md; test fence in place.""",
    False,
)

test(
    "Case 13: fenced code block containing trigger patterns should not fire",
    """Here's the regex we use:

```python
STRONG_PROPOSAL_PATTERNS = [
    re.compile(r"\\*\\*Option [A-Z]\\*\\*"),
    re.compile(r"\\*\\*C\\d+-[A-Z]\\*\\*"),
]
```

That's how it works.""",
    False,
)

test(
    "Case 14: real **Option A** outside backticks still triggers (must not over-strip)",
    """Two paths to consider:

**Option A**: keep the current approach
**Option B**: refactor the whole module""",
    True,
)

print(f"\n{passed} passed, {failed} failed\n")
sys.exit(0 if failed == 0 else 1)
