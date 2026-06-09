---
name: jarvis-os-build-loop
description: ∀ build session on VibeSwap arch ⇒ promote new primitives/hooks/disciplines back into jarvis-os install pack same session. Building VibeSwap ≡ growing JARVIS-OS substrate; the two recursively compound.
type: feedback
originSessionId: 2d5ae2e5-2926-42ce-a369-e66ee74c9c61
---
## Rule

∀ build session (contract / daemon / paper / spec) on the VibeSwap / PsiNet / MindMesh stack:
1. After each substrate-level primitive emerges (new hook, new discipline, new architectural pattern)
2. Promote to `C:/Users/Will/jarvis-os/` install pack
3. Update `jarvis-os/MANIFEST.sha256` + version bump
4. Note in newsletter post (recursive feedback loop = ship signal)

✗ Build VibeSwap in isolation. ✗ Build JARVIS-OS in isolation. They are the same substrate at different scales.

## Why

Will-frame 2026-05-24: "we had a rule to constantly be upgrading jarvis os as we build."

VibeSwap arch = the canonical implementation surface of the OPH consensus protocol (per `Desktop/jarvis-os-x-oph-consensus-integration-2026-05-24.md`). JARVIS-OS = the substrate-absorption tool that propagates that arch's primitives to other Claude installs. Every primitive learned in build → propagates → next build inherits.

This is `[P·recursive-self-improvement]` at the substrate-distribution layer. Same shape as `[P·child-rule-emergence-equals-parent-maturation]` applied to the JARVIS-OS pack instead of the parent primitive.

## How to apply

End-of-substantive-build-step checklist (alongside auto-checkpoint hook):
- [ ] Did this step produce a primitive? (new hook, new discipline, new gate, new pattern)
- [ ] Promote: copy/diff into `jarvis-os/hooks/` or `jarvis-os/examples/primitive_*.md` or `jarvis-os/SEED_MEMORY.md` index
- [ ] Manifest: `cd jarvis-os && sha256sum -c MANIFEST.sha256` (regenerate if changed)
- [ ] Version: bump `jarvis-os/VERSION` + tag + push if shipping a release
- [ ] Newsletter: note in current post that the pack got upgraded with primitive X

## Connects

- `[P·jarvis-os]` — the navigation shell being upgraded
- `[P·recursive-self-improvement]` — parent meta-pattern
- `[P·what-would-will-do]` — cognition layer being substrate-absorbed
- `[P·child-rule-emergence-equals-parent-maturation]` — sibling at primitive-discovery layer
- `[P·jarvis-amd-applied-to-ai-substrate]` — JARVIS = AMD methodology @ AI substrate, build-loop is how it stays canonical

## Origin

2026-05-24, during VibeSwap-arch-finishing arc. Will-flagged after I caught myself building CKB scaffolds + writing OPH integration doc without promoting any of the new primitives back to the jarvis-os pack — would have left the pack at v1.0.0 while the substrate moved to v1.1.0.
