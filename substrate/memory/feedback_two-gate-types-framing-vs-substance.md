---
name: Two gate types — framing vs substance
description: 2026-04-28 distinction. "Gate next time" = ambiguous. Framing gate catches comm-style retrospective patterns in commits/PRs ("honest error", "fix oversight"). Substance gate catches technical-terminology misuse in doc bodies ("clawback" vs "forfeiture", "slashing" vs "weight forfeiture"). Different jobs, different scan targets. Disambiguate before building.
type: feedback
originSessionId: d6d67641-272a-4e1e-a213-5c200874cf3d
---
# Two Gate Types

## Will's articulation 2026-04-28
> *"i meant gate the error but this if fine too"*

Said after I enhanced the partner-facing-additive-gate's retrospective-framing patterns (added "honest error", "earlier commits", "was wrong", "miswritten") in response to "will gate next time" on the COUNTERFACTUALS clawback→forfeiture fix.

Will's actual intent: gate the **substance error** (technical-terminology misuse) BEFORE the bad term ships. The framing-gate enhancement is also useful but is a different concern.

## The distinction

| Gate type | Catches | Scans | Hook layer |
|---|---|---|---|
| **Framing gate** (built) | Retrospective comm patterns: "honest error", "fix oversight", "we missed", "originally we", "earlier commits", "was wrong", "miswritten" | Commit messages + PR title/body | `partner-facing-additive-gate.py` |
| **Substance gate** (TODO) | Technical-terminology misuse in spec body: "clawback" used for non-fund-recovery mechanism, "slashing" used for weight reduction, "non-extractive" claimed before earned, "cypherpunk" political overclaim | Doc body content in partner-facing repos | not yet built |

## Why both matter
- **Framing gate**: protects partner-perception (don't make Will look dumb in PR description). Comm-hygiene layer.
- **Substance gate**: protects spec correctness (don't ship audit-grade-wrong terminology). Spec-quality layer.

## Disambiguation rule for "gate next time"
- "gate the language" / "gate the framing" / "next time it should ask before pushing this" → framing gate
- "gate the error" / "gate the term" / "catch this kind of mistake" → substance gate
- When ambiguous: ask which gate is meant before building

## Implementation sketch — substance gate
- Watch-list of terms that are commonly misused in our spec context:
  - `clawback` → flag if doc describes claim-layer reduction without fund-recovery
  - `slashing` → flag if doc describes weight reduction without capital destruction
  - `non-extractive` / `anti-extraction` → flag per F·usd8-non-extractive-not-yet-earned
  - `cypherpunk` (in USD8 context) → flag (political overclaim)
- Scan: doc body content in partner-facing repo files
- Trigger: PreToolUse on Write/Edit when target file path is in partner-repo
- Behavior: permissionDecision=ask with the matched terms + the misuse-pattern

## Surface 2026-04-28
- Cover-score PR #3 used "auto-clawback counterfactuals" for what was actually forfeiture (claim-layer reduction, not fund-recovery)
- Will caught it during EF meeting prep — the audit-grade reader would have caught it
- Fixed with explicit "fix language, honest error, will gate next time" framing on the commit
- Framing-gate enhanced to catch retrospective comm patterns; substance-gate is the harder follow-up Will originally meant

## Parent class
- P·dont-make-will-look-dumb (both gates are children)
- F·partner-facing-additive-framing (framing-gate sibling)
- F·verify-credentials-before-publishing (substance-gate sibling — verifying claims before publication)
