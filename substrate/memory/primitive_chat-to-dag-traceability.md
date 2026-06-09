---
name: Chat-to-DAG Traceability (Closed Loop)
description: Canonical process to trace every contribution end-to-end — from raw chat (Telegram/Discord/Twitter/conversation) → GitHub issue (formalized) → solution artifact (code/doc/spec/test) → ContributionDAG attribution-ID (on-chain credit). The closed loop makes informal contributions first-class on-chain assets.
type: primitive
originSessionId: c14b7c38-1d7d-4550-9588-2dbd1e7c40ec
---
# Chat-to-DAG Traceability — Closed Loop

## The rule

Every contribution to the project — whether code, doc, design call, dialogue prompt, or pure idea — must be traceable along **one canonical chain**:

```
RAW SOURCE (chat / conversation / external prompt)
     │
     ▼
GITHUB ISSUE  ← formalization layer (preserves source attribution)
     │
     ▼
SOLUTION ARTIFACT  ← contract / doc / spec / test, references issue # in commit
     │
     ▼
CONTRIBUTION DAG ATTRIBUTION-ID  ← on-chain credit anchored to original contributor
```

Each link in the chain references the previous, so any node can be queried and the full lineage recovered.

## Why

VibeSwap externalizes the cognitive economy on-chain (per [Economic Theory of Mind](P·economic-theory-of-mind)). For that externalization to actually work, the workflow that *produces* contributions must itself be legible to the chain — otherwise the on-chain DAG is just a reflection of code commits, missing the upstream non-code provenance.

The Contribution DAG (`contracts/identity/ContributionDAG.sol`) is the substrate. Without canonical traceability from chat → DAG, the DAG accumulates only the easily-measurable contributions (commits) and loses the harder-to-measure ones (ideas, design questions, framing) that often produce the most leverage.

Will, 2026-04-21: *"this needs to be standardized process so we can canonically trace contributions from chat to github issue to solution to dag attribution ID. from the chat to the contract level closed loop."*

## The canonical format

### Stage 1 — RAW SOURCE → GITHUB ISSUE

Issue title prefix: `[Dialogue]` for raw idea/discussion, `[Bug]` for defect, `[Feat]` for feature request, `[Audit]` for security finding.

Issue body MUST include a **Source** section at the top:

```markdown
## Source
- **Channel**: Telegram | Discord | Twitter | Conversation | RSS | Direct
- **Contributor**: @handle (chain-bound address if known)
- **Date**: YYYY-MM-DD
- **Original**: <link or quoted text>
```

Issue body MUST include a **Resolution Hooks** section that the closer fills:

```markdown
## Resolution Hooks
- [ ] Solution artifact (commit / file / spec)
- [ ] ContributionDAG attribution-ID
- [ ] Closing comment with chain references
```

### Stage 2 — GITHUB ISSUE → SOLUTION ARTIFACT

Solution commit messages reference the issue with the canonical token:

```
Closes #N — <short description>

<body>

DAG-ATTRIBUTION: pending  (or filled-in attestation-ID once minted)
SOURCE: <stage-1 source line>
```

The `DAG-ATTRIBUTION` line is grep-able. CI/automation can later scan unreleased commits for `DAG-ATTRIBUTION: pending` and mint attestations in batch.

### Stage 3 — SOLUTION → CONTRIBUTION DAG ATTRIBUTION-ID

`ContributionDAG.attestContribution(...)` mints a node with:

- `contributor` = the chain-bound address from Stage 1's Source.Contributor (or the canonical project-account if external/anonymous)
- `contributionType` = derived from issue label (`DIALOGUE`, `BUG_FIX`, `FEATURE`, `AUDIT`, etc.)
- `parentAttestations[]` = upstream contributions this one builds on (from `[Dialogue]` sub-references or commit-cited primitives)
- `metadataHash` = `keccak256(issueNumber, commitSHA, sourceTimestamp)` — binds the chain's three layers together
- `weight` (initial) = function of issueLabel × time-since-source × first-respondent-bonus

The returned `attestationId` is appended to the closing comment on the GitHub issue, completing the loop.

### Stage 4 — CLOSING COMMENT FORMAT

```markdown
Closing — <one-line resolution summary>.

**Solution**:
- <artifact 1: contract / doc / commit URL>
- <artifact 2: ...>

**DAG Attribution**: `0x<attestationId>` ([explorer link](...))
**Source**: <stage-1 source>
**Lineage**: <parent attestation-IDs that this closes-into>
```

This format makes every closed issue a navigable node in the contribution graph: upstream (source) and downstream (DAG ID) both visible from the issue page itself.

## How to apply

### When a new dialogue / bug / feature surfaces in chat

1. Open a GitHub issue. Use the canonical title prefix.
2. Fill the Source section with the channel, contributor, date, and link/quote.
3. Add the Resolution Hooks section as a TODO checklist.

### When work that addresses an open issue ships

1. Commit message: `Closes #N — <description>` + `DAG-ATTRIBUTION: pending` + `SOURCE: <stage-1 source>`.
2. Push.
3. Mint the ContributionDAG attestation (V1: manual via script `scripts/mint-attestation.sh`; V2: auto via CI hook).
4. Append the canonical Closing Comment to the GitHub issue with the attestationId.
5. Close the issue.

### Retroactive backfill

For already-closed issues without DAG-attribution: open a follow-up annotation comment with the canonical format, mint the attestation, link both sides. Cheap to do per-issue; valuable because it migrates historical contributions into the on-chain DAG.

### When the chain breaks

If a stage is missing (e.g., a commit closes an issue but there's no DAG attestation), the gap is a known debt. Track in `RSI-backlog` as `TRACEABILITY-DEBT-N` with the missing stage(s). Periodic sweep heals.

## Tooling implications (queued)

- `scripts/issue-template-dialogue.md` — issue template with Source + Resolution Hooks pre-baked
- `scripts/mint-attestation.sh` — wraps `cast send` to ContributionDAG with the canonical metadataHash construction
- CI hook: scan merged commits for `DAG-ATTRIBUTION: pending`, surface to a queue for next attestation batch
- GitHub Action: when a new issue is opened, validate the Source section is filled
- Dashboard: visualize the chain — issue → commit → attestationId — for any contributor's PoM page

These tools convert the canonical format from a discipline (which can drift) into infrastructure (which fires automatically).

## Relationship to other primitives

- **[Economic Theory of Mind](P·economic-theory-of-mind)** — the chain externalizes the cognitive economy. Without canonical traceability, externalization is incomplete. This primitive is the workflow-layer companion to ETM.
- **[Augmented Mechanism Design](F·augmented-mechanism-design-paper)** — augmentation, not replacement. We don't replace GitHub or chat; we add structured fields that route into ContributionDAG.
- **[Augmented Governance](P·augmented-governance)** — DAG attribution feeds PoM weight in the NCI consensus function. Closing the loop here directly affects governance authority.
- **[Symbolic Compression](P·symbolic-compression)** — the canonical format is itself compression: every issue carries the minimum metadata needed to recover the full chain.
- **[Stateful Overlay](P·stateful-overlay)** — the issue body's Source + Resolution Hooks sections are an externalized state overlay over GitHub's native issue model.

## One-line summary

*Every contribution gets one canonical chain — chat → issue → solution → DAG-ID — so informal upstream provenance becomes first-class on-chain credit.*
