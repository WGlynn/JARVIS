---
name: SubstrateMirrorIntoProjectRepos
description: ∀ substrate-layer doc shipped in JARVIS ⇒ cross-mirror into every project repo it operates under. Same loop turn. Identical text. Dual-push.
type: feedback
originSessionId: 8625a796-116e-42d8-b5c9-7064589f58ad
---
**[F·substrate-mirror-into-project-repos]** — JARVIS substrate doc (layers 1-8 + papers) ⇒ cross-mirror into project repos (vibeswap, others) on same loop turn.

> *"let's have commits for the WAL and other persistence hooks applied to the ivbeswap github as well for the same reasons"* — Will, 2026-05-06

## Rule
- ∀ substrate-layer doc landing in JARVIS ⇒ cross-mirror into ∀ project repo operating under it
- ∀ mirror = atomic commit + dual-push origin + backup per `[R·backup-remote-pattern]`
- mirror text ≡ source text (no edits)
- mirror lives at `<project>/docs/jarvis-substrate/<layer>_<filename>.md`
- new substrate doc shipped ⇒ mirror in same loop turn (per `[P·bidirectional-reification]`)

## Why
- A: substrate context lives where work happens — readers don't clone separate repo to understand discipline rules
- B: shard interop — multiple agents / sessions / future-readers see consistent substrate state across project repos
- C: commit-graph consistency — meaningful substrate docs land in every project repo they operate under

## Mirror layout
```
<project>/docs/jarvis-substrate/
├── README.md                                         # mirror index + sync discipline
├── 01-hooks_<filename>.md                            # layer 1 mirror
├── 02-persistence_<filename>.md                      # layer 2 mirror
├── 03-anti-hallucination_<filename>.md               # layer 3 mirror
├── 04-discipline_<filename>.md                       # layer 4 mirror
├── 05-meta-protocols_<filename>.md                   # layer 5 mirror
├── 06-agent-overlay_<filename>.md                    # layer 6 mirror
├── 07-stateful-applications_<filename>.md            # layer 7 mirror
├── 08-filesystem-as-substrate_<filename>.md          # layer 8 mirror
└── papers/
    └── <filename>.md                                  # JARVIS papers mirror
```

## Anti-pattern
- ✗ paraphrase mirror — defeats consistency property
- ✗ batch mirrors into one commit — defeats atomic-pacing property
- ✗ mirror at session-end instead of same-turn — defeats reification timing
- ✗ mirror to project repo but skip dual-push — defeats backup-remote-pattern

## Sibling rules
- `[P·bidirectional-reification]` — substrate doc (word) reifies into mirror (code-adjacent context)
- `[R·backup-remote-pattern]` — every mirror dual-pushes
- `[F·atomic-commit-pacing]` — each mirror is its own atomic commit
- `[P·apply-the-rule-you-just-wrote]` — when a NEW substrate layer doc is named/written, the mirror discipline applies immediately

## Trigger
- new substrate-layer doc shipped in JARVIS (any of layers 01-08)
- new JARVIS paper shipped in `JARVIS/papers/`
- update to existing JARVIS substrate doc

## Action
1. Identify project repos operating under this substrate (currently: vibeswap; future: others)
2. `cp <jarvis-source> <project>/docs/jarvis-substrate/<layer>_<filename>.md`
3. `git add` the mirror file
4. `git commit` with message: `docs(jarvis-substrate): mirror <layer> <filename>` + paragraph on what the mirror covers
5. `git push origin <branch> && git push backup <branch>`
6. Update `<project>/docs/jarvis-substrate/README.md` if a new layer is now mirrored

## Origin
- 2026-05-06 GH#18 autonomous run
- 8 mirrors shipped (layers 1-8 + 2 papers + README) across run, all dual-pushed
- discipline articulated mid-run when Will named the requirement
