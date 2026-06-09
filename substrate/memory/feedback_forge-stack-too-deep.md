---
name: Forge stack-too-deep debugging
description: How to find and fix stack-too-deep compilation errors in large Foundry codebases
type: feedback
---

## Stack-too-deep manifests in TWO different ways:
1. **Solidity-level**: "Stack too deep" with file:line reference — fix with scoping `{}` blocks or helper functions
2. **Yul/ABI encoder**: "Variable value0 is N slot(s) too deep inside the stack" with NO file reference — caused by large struct returns or complex ABI encoding

## Binary search with `--skip`:
- `forge build --skip "contracts/dir/*"` excludes directories
- `forge build --skip "test/*" --skip "script/*"` focuses on contracts only
- Remove half the dirs at a time, check which half has the error
- Can take 20+ iterations with 30+ directories

## Root causes in VibeSwap (March 2026):
- Functions with 10+ params (CommitRevealAuction.revealOrderWithPoW)
- Struct constructors with 14+ named fields (VibeRWA.registerAsset)
- Large struct returns: Task(15 fields), RealWorldAsset(15 fields)
- BFS with many locals (FractalShapley.computeCredit)

## Fixes ranked by effectiveness:
1. **Extract helper functions** — reduces peak stack depth across call boundary
2. **Scope blocks `{}`** — only helps for Solidity-level errors, not Yul/ABI
3. **Field-by-field struct population** — instead of named-field constructor
4. **Split getters** — getTaskCore() + getTaskMeta() instead of getTask() returning full struct
5. **Internal mappings** — prevents auto-generated getter for large structs
6. **via_ir=true** — handles arbitrary stack depth but 10x slower compilation

## CI strategy:
- `fast` profile: via_ir=false, optimizer_runs=200, for local dev (fast compilation)
- `ci` profile: via_ir=true, optimizer_runs=1, for CI (correct but slow ~35-40 min on 991 files)
- Don't try to make non-via_ir build work for 990+ file codebases — too many struct returns

**Why:** Spent 2+ hours binary-searching for the `value0` error. The error has NO file reference, making it extremely hard to locate. Save time: use via_ir for CI from the start.

**How to apply:** When forge build fails with stack-too-deep on a large codebase, immediately check if via_ir=true resolves it. If it does, use via_ir for CI and fix the most critical functions for the fast profile.
