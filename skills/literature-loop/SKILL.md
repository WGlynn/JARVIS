---
name: literature-loop
description: Run a multi-round improvement loop on a paper (whitepaper, research paper, spec, litepaper), or on a whole corpus of papers - audit against current truth, parallel read-only reviews through different reader lenses, one fixer per wave, internal and cross-paper coherence, stop when only nitpicks remain. Generalized from the Noesis whitepaper v5.6 to v5.7 loop (Will 2026-11-13, "we will eventually be doing this with our entire code base of literature").
---

# /literature-loop: improve a paper, or a corpus of papers, in rounds

Input: `$ARG` = a paper path (one-paper mode) or a directory or list of papers (corpus mode).

## The rules (every round, every agent)
1. **Work on a copy.** One-paper mode: `~/Desktop/<Name>-vNEXT-work/` holds a copy of the paper and everything it includes. Nothing in a repo changes until Will approves the final round.
2. **Authority order for facts:** the code, then the project's canonical reference (for Noesis, ARCHITECTURE.md, whose numbers point to constants), then handoffs and roadmaps, then docs changed after the paper's date. A paper is never its own authority, and an older paper is never an authority over newer code.
3. **No numbers from memory.** Open the constant or the result file and cite file:line.
4. **Status discipline:** built, designed, open. Never rounded up. A claim without support becomes a stated limitation, not a quiet deletion.
5. **The author's goal statement leads.** Read the project's goal memory first (for Noesis: incentive alignment and honest behavior; capital resisted only as the weakest value signal).
6. **Coherence, two kinds.** Internal: no two paragraphs of the paper contradict each other (abstract, intro, body, figures, captions, status tables and conclusion repeat claims; all must match). Cross-paper: papers that overlap must agree on facts and status in their own words ("overlap in coherence," not merged).
7. **Plain words, no em or en dashes** in new text. Each paper keeps its own register.
8. **Two agents at a time, maximum.** Reviews are read-only and can run in parallel; exactly one fixer edits a working copy at a time.
9. **Every round's output is new and dated** (review files, PDFs named `<Name>-vNEXT-rN-YYYY-MM-DD-HHMM.pdf`). Never overwrite an earlier round.
10. **Reviews are claims, not facts.** A fixer verifies every review finding against the code before applying it, and a fact-check round follows every fixer: it checks each claim the fixer added or changed, independently. (In the Noesis v5.7 loop, round 1 applied a reviewer's misreading and reversed a correct result in three places; the fact-check caught it, 12 bad claims out of 112.)
11. **Log everything** in `~/Desktop/<Name>-vNEXT-LOOP.md`: one line per round, plus a "Decisions for Will" list for items that are design choices rather than text fixes.
12. **Fixers edit in small steps and report as they go.** Small Edit calls only, never a whole-file rewrite; one progress line in the LOOP file per finished item, so a stalled fixer is visible. Apply a fact-check before any restructuring review, while its locations still match the text. (In the Noesis v5.7 loop, the restructuring fixer went silent for over an hour after its first edits and had to be stopped.)

## One-paper mode: the rounds
- **0. Audit:** everything outdated, wrong, overclaimed or missing against the authority order; plus the overlap map with sibling papers (scope each owns, shared claims with locations, current contradictions with reconciled facts and per-paper wording).
- **Reader lenses (read-only, run two at a time):** skeptical researcher (support, sourcing, proofs, referee objections); adversary (for each claimed defense: cheapest attack, does the code stop it, HOLDS / PARTIAL / CLAIMED-ONLY); newcomer (structure, plain language, can an outsider follow it); internal coherence (claim table: every load-bearing claim and every place it is stated, flag disagreements); cross-paper coherence (against the overlap map).
- **Fact-check (after every fixer):** verify each new or changed claim independently against the code; verdicts CORRECT, WRONG, UNSUPPORTED, MISLABELED, plus "says missing but the code has it".
- **Fixers:** each applies all finished reviews in one pass, verifies every number, then reads the whole paper start to finish and aligns every restatement before finishing. Rebuilds the PDF if a TeX toolchain works; never fakes one.
- **Stop rule:** stop after a round whose reviews find only MINOR items, or after 6 rounds in a session. Three rounds in a row with zero new findings means the paper has hit its discovery ceiling; move attention elsewhere.
- **Approval:** Will reads the last PDF and the Decisions list. Only then does the working copy replace the repo version, as a new version number, with a changelog entry.

## Corpus mode: the whole literature
1. **Inventory:** list every paper (path, project, version, last commit date, audience, status) into `~/Desktop/literature-inventory-YYYY-MM-DD.md`. Sources: each project's docs/, papers/, whitepaper/, research/ and README-level overviews.
2. **Claims registry:** per project, one canonical file of load-bearing facts, each with its source pointer and status (for Noesis this sits beside ARCHITECTURE.md). Papers cite the registry's facts; the registry cites the code. This is what makes cross-paper coherence checkable at scale: a paper is coherent when every load-bearing claim matches a registry entry.
3. **Priority order:** outward-facing and most-read first (whitepapers, litepapers, one-pagers, public FAQs), then papers others cite, then internal research.
4. **Run one-paper mode per paper**, two agents at a time, sharing the registry. Each loop's findings that change a fact go to the registry first, then to every paper that states that fact (a fact change fans out; that is the point of the registry).
5. **Corpus coherence pass:** after a batch, one reviewer checks every paper's load-bearing claims against the registry and lists mismatches.

## Origin
Built 2026-11-13 from the Noesis whitepaper loop (Desktop/noesis-whitepaper-v5.7-LOOP.md): audit found 31 items, skeptic review 37, with blockers on finality, commit-reveal, standing farming and wash. Will added internal coherence ("the paragraphs arent contradicting each other"), cross-paper overlap in coherence, two agents at a time, and asked for this generalization.
