---
name: Cleanup-Duty Density Scan
description: Audit primitive — systematically scan for empty/stub function bodies at internal call sites. Logic-audits miss "code that isn't there". Two confirmed findings: VibeFeeDistributor._distributeToStakers (C11) and VibeAgentConsensus._returnStakes (C12 — wrong recipient = stake theft CRIT).
type: primitive
originSessionId: 5fef52ed-7341-42b4-b27e-d0f59eee85ca
---
# Cleanup-Duty Density Scan

Unit-test audits and logic audits look at **what the code does**. They systematically miss **what the code doesn't do** — functions with empty bodies, stubs returning zero, placeholder TODOs at internal call sites.

**Why:** Tests pass because no assertion cares about the missing effect. Logic audits read the call chain and implicitly assume each named function performs its named operation. Empty-body bugs are invisible to both.

**How to apply:** Run a density scan at least once per cycle. Grep `contracts/` for:

1. `function\s+\w+[^{]+\{\s*\}` — empty bodies
2. `} catch \{\}` — swallowed errors (categorize: advisory side-effect vs. value-bearing)
3. `return (0|false);` in functions named `_distribute|_pay|_credit|_settle|_reward|_claim|_accrue|_return` — stubs at value-flow sites
4. TODO/FIXME in function bodies, especially with words like "integrate", "deploy", "later"
5. Functions with only parameter-silencing (`(a,b,c);`) followed by no-op return — unless explicitly "rejects all inputs" with reason

**Triage rule:** If the function's name implies value-handling (distribute, return, credit, settle, claim, pay) AND the body is empty or returns a constant, it is guilty until proven innocent. Read the callers. If any caller passes value (tokens, ETH, credits) or modifies a state field the empty function should have updated, it's a value-drop finding.

**Skip list (known benign):**
- `_authorizeUpgrade` UUPS overrides with empty body + `onlyOwner` modifier — the check is the modifier
- View/pure sentinels (`return 0` when documented behavior)
- Empty catches on advisory side-effects where the failure mode is documented and reversion would cause worse outcomes (e.g., skipping an emit on a monitoring contract)

**Historical findings of this class:**

- **C11 Batch C**: `VibeFeeDistributor._distributeToStakers` was an empty stub. Every distribute() silently deleted the stakers' 40% fee share. Survived 11 RSI cycles because no test asserted stakers received funds. Fixed commit `b9378f2e`. Masterchef `accPerShare` pattern.

- **C12**: `VibeAgentConsensus._returnStakes` sent all revealed-agent stakes to `msg.sender` (the finalize() caller) instead of the committer. **Stake-theft CRIT** — any finalizer drains all honest revealers' stakes. Root cause: struct never recorded depositor address; `msg.sender` was the only available handle. Fixed commit `5773b8c2`. Added `address committer` to `AgentCommit`.

**Meta-loop placement:** This scan is a **cleanup-duty R1 variant**. Regular R1 audits look at logic; cleanup-duty scans look at presence. Run both. They find disjoint bug classes.

**What to add over time:**
- A Forge lint pass or a CI check that flags empty internal function bodies at value-flow sites (file: `tools/cleanup-duty-scan.py` or similar — deferred).
- Extend scan heuristics as new silent-value-drop patterns surface. Each new class found should update this memory's checklist.
