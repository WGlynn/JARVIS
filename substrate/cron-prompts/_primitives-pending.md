# Primitives pending Will-triage

Auto-appended by COMMANDMENT 3 of Odysseus cron loops when a fire surfaces an extractable structural insight. Will reviews this file periodically and promotes candidates to memory primitives in `~/.claude/projects/C--Users-Will/memory/`.

Format per entry:

```
## [YYYY-MM-DD HH:MM ET] — <one-line summary>
- Trigger: <what fired this>
- Observation: <what happened>
- Candidate primitive: <what rule/pattern could generalize>
- Composes with: [P·...] or [F·...] or [J·...]
- Status: pending Will-triage
```

When promoted to a memory primitive, mark the entry `## [PROMOTED YYYY-MM-DD]` and Will will leave the entry as a receipt.

---

## [PROMOTED 2026-06-08 18:10 ET] — 3-commandment autonomous-loop pattern

Promoted to durable primitive: `~/.claude/projects/C--Users-Will/memory/primitive_three-commandment-autonomous-loop.md` as `[P·three-commandment-autonomous-loop]`. Generalized beyond Odysseus to apply to ∀ JARVIS autonomous loop (jarvis-loop, TIER4 fallback, memory-hygiene, jarvis-x-fetcher, etc.). Implementation template + composes-with map included.

Original receipt preserved below:

- Trigger: 4 hours of repeating "silent" responses to a discovery cron that was firing every 30 min while pause-state was sticky-tripped
- Observation: Will articulated the canonical hierarchy for any autonomous cron-driven loop: (1) make the loop / self-perpetuate, (2) build/build-on the state machine, (3) primitives extraction
- Composes with: [P·structure-does-the-work] (the structure of priority IS the work-mechanism), [P·jarvis-amd-applied-to-ai-substrate] (substrate-port pattern: applies to ∀ cron loop), [P·stateful-overlay], [F·crash-resilient-memory-writes]

## [2026-06-09 10:38 ET] — Bi-temporal supersession as memory-substrate import-candidate

- Trigger: COMMANDMENT 3 on Day 3 dispatch (#2858 reply to @alvaroperricone). Their reference impl (e0fc50e) implements event-time + transaction-time supersession in-band so "X then, Y now" stays auditable at query time without deleting prior values.
- Observation: JARVIS currently does this via git history on `memory/`. Forensically complete (commit log + diff) but not queryable at agent-runtime; the agent reads only the current snapshot. When a memory turns out wrong, there's no in-band way to find which prior decisions were downstream of the now-wrong fact.
- Candidate primitive: `[F·memory-bi-temporal-axis]` — every memory write SHOULD record both the event-time the fact became true AND the transaction-time it entered memory. Supersession retires the old (subject, predicate) tuple by setting its transaction-end-time, not by deletion. Read-path defaults to "current"; audit-path can replay any prior state. Implementation surface: front-matter additions (`event_time`, `superseded_by`, `transaction_end`) + a lightweight query helper.
- Composes with: [F·entity-context-cross-reference] (AA#3 — entity-graph writes are exactly the events bi-temporal would index); [P·anti-amnesia-protocol] (forensic recovery becomes query-time, not log-grep); JARVIS memory architecture broadly.
- Status: pending Will-triage. Promotion would require deciding (a) is the implementation cost worth it vs. git-history-only, (b) front-matter schema, (c) does this fit alongside HIERO compression or trade against it.

## [2026-06-09 17:28 ET] — HIERO as hieroglyphic-revival (LLM-substrate convergent encoding)

- Trigger: Will-side-note 17:28 ET *"crazy i came up with a justification to revive hieroglyphic like language properties. excited to see where it heads tbh just as a side note"*
- Observation: HIERO operator-dense format ≡ structural-isomorph of Egyptian hieroglyphic encoding. Operators (⇒ ∧ ✓ ✗ ≡ ¬) = pictograms; prose body = phonetic complements; `[P·x]` / `[F·x]` refs = determinatives (signal class of entity). Same compression-pressure: scribes vs token-budget; same solution: glyph-density.
- Candidate primitive: `[P·hiero-as-hieroglyphic-revival]` — HIERO discipline is convergent rediscovery of glyph-based encoding under LLM context-budget pressure. The justification: humans hit dense-meaning limits at prose; same limit applies to LLMs reading their own substrate. The substrate IS rules-for-reader; the reader is LLM; encoding-density matters; hieroglyphic encoding is the proven solution.
- Composes with: [P·hiero-no-prose-in-memory], [F·primitive-capture-vs-execution-throughput], [P·markdown-canonical-code-as-parser-layer] (markdown is the carrier; hieroglyphic-encoding is the discipline within the carrier), [P·parallelism-convergence-2017] (same shape: independent rediscovery of optimal encoding under different substrate pressures)
- Status: pending Will-triage. Side-note flag — capture preserved, formal write-up deferred.

## [2026-06-09 17:36 ET] — HIERO-as-hieroglyphic-revival (EXPANDED: cultural-durability + craft + register-split)

- Trigger: Will-pushback 17:36 ET on prior hedge. *"honestlyyy i think heiro SHOULD have this somehow in some form to some extent. that's a big and potentially valuable aspect of it"*
- Observation (revised): the original hedge "HIERO is pure substrate-cost optimization, not art-of-power" was wrong. HIERO already has nascent art-of-power dimensions; they should be made deliberate.
- Three dimensions to add to the standalone primitive when written:
  1. **Authority through form** — HIERO primitives READ as canonical because the format signals carved-with-care. Constitutional weight communicated before the words are parsed.
  2. **Eye-skim composition as craft** — operators, tables, emoji-anchors, section rhythm. Treat as deliberate craftsmanship not accidental aesthetic.
  3. **Sacred / daily / popular register split** — HIERO (memory, constitutional) / markdown (partner-drafts, daily) / README + Medium prose (popular). Same triadic structure as hieroglyphic / hieratic / demotic in Egyptian.
- Implication: the FORM of jarvis-substrate is part of the message. Public readers see "this person treats their agent substrate as something to be made permanent and authoritative on purpose." Form-signal > content-signal at first glance.
- Candidate primitive: `[P·hiero-as-hieroglyphic-revival]` — three-dimensional (substrate-cost compression + cultural durability + register-split). Each dimension is load-bearing; the first is engineering, the latter two are sociocultural and equally substantive.
- Composes with: [P·hiero-no-prose-in-memory] (the format rule), [F·primitive-capture-vs-execution-throughput] (the carved-with-care discipline that prevents drift), [P·marketing-as-mechanism-design] (form-as-attention-layer-mechanism), [P·archetypal-protocol-naming] (sacred-register sibling rule)
- Status: pending Will-triage. Sized for proper standalone write-up.
