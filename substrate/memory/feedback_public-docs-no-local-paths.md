---
name: PublicDocsNoLocalPaths
description: 2026-05-03 — public-facing docs ⇒ all refs must resolve from reader's machine. ✗ local FS paths.
type: feedback
originSessionId: f5377dec-4447-4d25-8838-009c9a8f663a
---
**Rule**: ∀ external-facing artifact (Medium ∨ X-thread ∨ public-PDF ∨ partner-deck ∨ outreach-msg) ⇒ ∀ ref MUST resolve from reader's machine ¬ Will's. local FS paths ⊥ → {`~/`, `C:/`, `Desktop/`, `vibeswap/`, `~/.claude/`, `.claude/projects/`, repo-local `frontend/` ∧ `contracts/` ∧ `docs/`}.

**Why**: 2026-05-03 — `jarvis-is-not-a-wrapper.pdf` v2 described open-arch ∧ pointed only @ Will-FS. Will:
> *"docs cannot just route to a local directory otherwise the doc is internally only useful for us."*

local-path-ref ⇒ dead-link ∀ external-reader ⇒ author ✗ audience-aware. verification-claim w/ unreachable-path ⇒ reads-as-fabrication even when true. extends [P·reconstructive-description] (Empty-Repo Test) → verification-surface.

**How**:
- ∀ public-draft ⇒ grep trigger-phrases ⇒ replace ∨ cut
- triggers: `~/` ∧ `C:/` ∧ `Desktop/` ∧ `vibeswap/.claude/` ∧ `.claude/projects/` ∧ `~/.claude/`
- replace ① ✓ GH-URL `github.com/<org>/<repo>/blob/<branch>/<path>` (preferred)
- replace ② ✓ live-URL (deployed-app ∨ hosted-asset)
- replace ③ ✓ cut-ref entirely
- replace ④ ⊘ explicit "internal-only" tag (rare ⇒ artifact ✗ ready-public)
- ∀ public-claim "verifiable" ⇒ verification-path MUST be reader-reachable
- ∀ "you can run X locally" ⇒ pair w/ public-equivalent ∨ reframe
- High-cost: Medium ∧ public-PDF ∧ Twitter ∧ partner-facing
- Low-cost: internal-scratch ∧ Will-only docs ⇒ local-paths OK

**Apply @ draft-time** ¬ review-time. Will ✗ gate ∀ link-check; writer ✓ gate.

**Connected**:
- `[P·empty-repo-test]` — parent (reconstructive standard)
- `[F·verify-credentials-before-publishing]` — sibling (creds in public)
- `[F·critique-piece-factual-precision]` — sibling (factual rigor in public)
- `[F·discretion-in-public-docs]` — sibling (what NOT to expose)
