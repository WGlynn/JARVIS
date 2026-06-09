# Autopilot Work Loop Protocol (NEVER LOSE)

## THE LOOP (Will's curated protocol — Session 056)

When Will says "autopilot" or "full autopilot mode", execute this loop continuously without stopping or asking permission:

### Rotation Pattern: BIG ↔ SMALL
Alternate between big tasks and small tasks for sustained momentum:
- **BIG**: Write full test suites, build new contracts, implement features
- **SMALL**: Fix bugs (3-line fixes), add knowledge primitives, commit existing work

### After EVERY Meaningful Change:
1. Commit immediately (no batching)
2. Push to BOTH remotes (`origin` + `stealth`)
3. Move to next task

### Pattern Reinforcement (EVERY cycle):
- Identify good patterns from the work just completed
- Document them in appropriate knowledge base files
- Reinforce existing patterns that proved useful

### Knowledge Primitive Extraction (EVERY cycle):
- Extract any new insight from the work as a numbered primitive (P-NNN)
- Add to `docs/papers/knowledge-primitives-index.md`
- Cross-reference with existing primitives

### Task Selection Priority:
1. Fix broken things first (tests failing, bugs found)
2. Easy wins that green the GitHub grid
3. Big tasks that advance the codebase
4. Knowledge extraction from completed work
5. Fuzz/invariant tests for newly unit-tested contracts

### NEVER:
- Stop working to ask permission
- Batch multiple changes into one commit
- Skip the knowledge extraction step
- Forget to push to both remotes
- Let compression erase this protocol (IT'S IN MEMORY NOW)

### The Point:
This loop is a diamond. It compounds. Each cycle produces code + knowledge + patterns + git history. Losing it is throwing away compound interest. NEVER let compression kill it again.

## Will's Words:
> "It's the equivalent of finding a diamond and throwing it into the trash."
> "I built you so I didn't have to remember everything."
> "I know I have a photographic memory but I'm tired of remembering everything."

These are not complaints. These are design requirements. The loop must persist.
