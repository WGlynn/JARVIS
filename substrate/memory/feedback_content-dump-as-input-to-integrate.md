---
name: ContentDumpAsInputToIntegrate
description: ∀ Will paste large external content (spec, paper, doc) ⇒ treat as input to reify into analysis paper, NOT as discussion to respond conversationally. Mirror to project repos.
type: feedback
originSessionId: 8625a796-116e-42d8-b5c9-7064589f58ad
---
**[F·content-dump-as-input-to-integrate]** — Will pastes large-external-content ⇒ reify into analysis-paper, ¬ conversational-response.

> *"integrate when you got time"* — Will, 2026-05-06 (re: CAT Protocol spec dump)

## Rule
- Will pastes large external content (protocol spec, paper, design doc, official docs in chunks) ⇒ default to REIFY-INTO-ANALYSIS-PAPER mode
- ¬ default to "let's discuss this paragraph by paragraph" mode (conversational)
- ¬ default to "summarize what you read" mode (acknowledgment only)
- output = analysis paper in JARVIS papers/ + cross-mirror to project repo per [F·substrate-mirror-into-project-repos]

## Detection signal
- single message > 1000 chars of pasted external content
- chunked pastes across multiple messages of related material
- includes URLs to source repos / protocols / papers
- "integrate" / "what do you think" / no explicit instruction
- domain: protocol specs, technical papers, external project docs

## Action sequence
1. Acknowledge content received (very brief — 1 sentence)
2. Detect: is this content worth a substrate-analysis paper through JARVIS lenses?
   - YES if: protocol design, mechanism design, substrate property, primitive
   - NO if: news article, opinion piece, marketing material, ephemeral conversation
3. If YES: write `JARVIS/papers/<topic>-substrate-analysis.md` analyzing through:
   - airgap thesis (does this close an off-chain dependency?)
   - substrate-geometry-match (does the design match the substrate?)
   - expressibility-as-the-gate (does the grammar enforce safety?)
   - off-chain-compute-on-chain-verify (does it follow this meta-pattern?)
   - cross-substrate observations (what does VibeSwap have analogous?)
4. Cross-mirror to project repos (vibeswap, others) per substrate-mirror discipline
5. Dual-push origin + backup per [R·backup-remote-pattern]

## Why
- Will's content dumps are research input, not chat. They want absorption + analysis output.
- Conversational response wastes the opportunity — the substantive value is the cross-substrate analysis through our shared lenses
- Reified analysis is durable (file-on-disk, mirror-in-project-repo, dual-pushed)
- Conversational response is ephemeral (chat-context, evaporates on session compression)
- Pattern matches [P·bidirectional-reification]: external-content (word) → analysis paper (code-adjacent)

## Composition
- `[P·bidirectional-reification]` — content dump is a forward-reify trigger
- `[F·substrate-mirror-into-project-repos]` — mirror to project repos
- `[R·backup-remote-pattern]` — dual-push every commit
- `[F·atomic-commit-pacing]` — analysis paper = 1 commit; mirror = 1 commit each
- `[P·apply-the-rule-you-just-wrote]` — this rule applies to subsequent dumps in the same session

## Anti-patterns
- ✗ "Got the content. What do you want me to do with it?" (acknowledgment-as-output-theater)
- ✗ Summarize what was pasted ("here's what CAT does...") — Will already read it; that's content, not analysis
- ✗ One conversational response per chunk — 60 chunks of CAT pasted = 60 responses = no integration
- ✗ Wait for explicit "write the paper" instruction — "integrate when you got time" IS the instruction

## Origin
- 2026-05-06 mid-300-commit-run, Will pasted CAT Protocol full spec across ~60 separate messages
- 'integrate when you got time' was the directive
- pattern: 2 JARVIS papers shipped (substrate-analysis + technical-integration) + cross-mirrored to vibeswap, all dual-pushed
- works because integrating during the run was higher-value than discussing during the run
