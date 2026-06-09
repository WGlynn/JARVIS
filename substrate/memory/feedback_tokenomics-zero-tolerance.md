---
name: Tokenomics Zero Tolerance — Never Guess, Never Conflate
description: Tokenomics is the ONE area where mistakes are nearly unforgivable. Verify every property against source contracts before writing code or tests.
type: feedback
---

Tokenomics mistakes are nearly unforgivable. Money mistakes don't have a `git revert`.

**What happened:** Jarvis conflated JUL (elastic energy token, EVM, PoW-mined) with the CKB-native token (circulating cap, state rent, NOT YET IN CONTRACTS). The MEMORY.md entry was ambiguous and read as one token description.

**Why this matters:** If this confusion had propagated into contract code or deploy scripts, it could have created wrong emission schedules, wrong cap logic, or wrong economic behavior — all of which are catastrophic once deployed to mainnet.

**How to apply:**
1. NEVER guess token properties. Read the contract source.
2. NEVER conflate tokens that share some properties. They are SEPARATE economic instruments.
3. Before writing ANY test or code touching tokenomics: re-read the contract, the interface, and the architecture doc.
4. The three tokens are:
   - VIBE: Ethereum/Base, 21M lifetime cap, Shapley-distributed, ERC20Votes governance
   - JUL: EVM, elastic rebase, SHA-256 PoW mining, PI controller, energy-backed
   - CKB-Native: NOT YET BUILT. Nervos CKB, circulating cap, state rent model
5. When uncertain about tokenomics, STOP and ask Will. Don't construct plausible-sounding answers.
