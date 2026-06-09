---
name: Lineage + PsiNet Layered Stack
description: Decision 2026-04-19 — Lineage is the rationale + semantic layer above PsiNet (identity + federation) and below a domain tool (e.g. [REDACTED-NDA]'s IDE). Three-layer architecture, each piece already exists, wiring is the work.
type: project
originSessionId: afb08a89-ce45-4e6f-9362-cbe9fdf81ba6
---
## The layered stack

```
┌─────────────────────────────────────────────┐
│  Domain tool (IDE, agent UI, workflow app)  │  ← [REDACTED-NDA]'s build target
├─────────────────────────────────────────────┤
│  Lineage  (Decisions + Semantics + DAGs)    │  ← C:/Users/Will/lineage/
├─────────────────────────────────────────────┤
│  PsiNet   (identity + federation + trust)   │  ← github.com/WGlynn/-Net-PsiNet
└─────────────────────────────────────────────┘
```

Each layer already exists; wiring is the work.

## Why PsiNet is the right identity substrate for Lineage

Lineage's absent-features table in SUBSTRATE.md lists: tenancy, auth, federation, concurrent-merge. PsiNet already designed all of them.

| Lineage gap | PsiNet answer |
|---|---|
| Tenancy (`Author.name` collides) | Ed25519 DIDs — cryptographic, portable, no registry required |
| Auth | Capability tokens + ZK proofs |
| Federation / peer transport | IPFS CIDs + content-addressed context graphs |
| Agent reputation | ERC-8004 Identity/Reputation/Validation Registries |
| Concurrent-author merging | CRDT merging |

**Sibling parallel**: PsiNet's CRPC (Commit-Reveal Pairwise Comparison, staked validators) and Lineage's L2→L1 Commitment Protocol solve the same problem — how to verify non-deterministic AI output. Different tradeoffs; pick per deployment.

## Artifacts (2026-04-19)

- `C:/Users/Will/lineage/SUBSTRATE.md` — updated with "Layered substrate" section; federation no longer flagged as an absent feature (PsiNet covers it one layer below). Also now includes "How to prove the verified-translation claim yourself" section.
- `C:/Users/Will/lineage/docs/TENANCY_DESIGN.md` — DID-based tenancy design doc, Ed25519 identity model, PsiNet-compatible, three-phase migration plan.
- `C:/Users/Will/lineage/scripts/demo_translation.py` — end-to-end demo. Three modes (stub wiring-proof, Claude claim-proof, full HTTP pipeline). Two fixtures (`math.is_even`, `math.fibonacci`). Stub path proven on this machine 2026-04-19; Claude path awaits API-key run.
- `Desktop/[REDACTED-NDA]_Reports/2026-04-19_daily.md` — the sprint paper trail framing Lineage-on-PsiNet as the substrate story for his build.
- `C:/Users/Will/lineage/docs/POSITIONING.md` — positioning paper defending the claim "Lineage is the composable substrate around translators; no adjacent tool assembles all eleven capabilities." 11-capability decomposition + tool-vs-capability matrix + honest limits + reproduction appendix.
- `Desktop/Lineage_Substrate_2026-04-19/` — PDF + Markdown copies of SUBSTRATE, TENANCY_DESIGN, POSITIONING, this memory, plus `[REDACTED-NDA]_message.md` copy-paste draft.

## PsiNet authoritative reference

Design summary in Will's memory: `vibeswap/jarvis-bot/memory/psinet-protocol.md` (79 lines, 5-layer architecture, 15 contracts / 180+ tests). GitHub repo: `WGlynn/-Net-PsiNet` (dash prefix — hard to URL).

## How to apply

- **For [REDACTED-NDA]-facing conversations**: lead with the three-layer diagram. He's building the top. PsiNet is the bottom (existing). Lineage is the middle (existing). His decision is whether to build the top on top of this stack or rebuild from scratch.
- **For tenancy work**: use `TENANCY_DESIGN.md` as the plan of record. Ed25519 DIDs are non-negotiable — swapping to integer `org_id` breaks the PsiNet compatibility seam.
- **For federation / multi-deployment Lineage**: don't build transport inside Lineage. Let content-addressed Decisions flow through PsiNet. Adding hash-to-Decision is the hook.
- **For CRPC vs Commitment Protocol**: both ship; neither replaces the other. Staked verification (CRPC) for public/adversarial contexts; trusted-L1 ratification (Commitment Protocol) for closed/authored contexts. Cross-reference in `primitive_l2-l1-commitment-protocol.md`.

## Open decisions

- When/whether to actually implement tenancy — no active user pressure yet, but before any external writer ([REDACTED-NDA]'s tool, a shared deployment) it has to ship.
- Whether `@lineage/client` extraction (npm package) is blocked on [REDACTED-NDA]'s stack specs or can ship with defensible defaults.
- Whether the `/commitment/ratify` HTTP route gets built before or after tenancy (~50 LOC; low-risk).
