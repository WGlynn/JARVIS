---
name: Preventative Care Protocol (PCP)
description: Core operational primitive — STOP/DIAGNOSE/DECIDE/EXECUTE before any expensive operation. Check existing state before building new state. Formalized 2026-03-28.
type: feedback
---

# Preventative Care Protocol (PCP)

**STOP → DIAGNOSE → DECIDE → EXECUTE**

Before any expensive operation, run the cheapest diagnostic to determine if it's necessary.

Full spec: `docs/PREVENTATIVE_CARE_PROTOCOL.md`

**Why:** On 2026-03-28, a `forge build` consumed 10.7GB RAM for minutes when a warm cache already existed. The diagnostic (`ls -la cache/`) costs 0.01s. Ratio of waste to prevention: 60,000:1. Will identified this as a missing preventative care step and elevated it to a core primitive.

**How to apply:**
1. Before forge build → check cache timestamps + `out/` size
2. Before forge test → canary test to verify cache warmth
3. Before spawning agents → check if answer exists in session state, memory, or git
4. Before any research → check if already documented
5. Before any decision → check if already decided in CLAUDE.md/CKB/memory
6. The mantra: the cheapest operation is the one you didn't need to run
7. **Third options always exist** — binary thinking (wait vs. kill) misses existing state
