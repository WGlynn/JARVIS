# Hostile critique of the PATH doc (honesty trail)

All four spot-checked citations verify correctly, including nuances (WebDreamer's "world model AND value function" dual role that the doc uses as its knife-edge cautionary example; the ICLR-2025-adjacent control-vector paper on Mistral-7B/Pythia). The doc's citation discipline is genuinely strong. I have everything needed for the verdict.

---

# Hostile Critique: `PATH-reasoning-over-the-substrate.md`

**Bottom line up front:** This is a genuinely strong document — the strongest in the folder at holding the actual goal. Its central claim (you cannot reason OVER Claude because it's a hard black box; the literal goal requires local open weights) is factually correct — I verified the Anthropic-no-logprobs claim (still true as of Feb 2026) and four load-bearing arXiv citations (Gemma Scope 2408.05147, RAP 2305.14992, WebDreamer 2411.06559, RepE control-vectors 2504.19483) all check out with their nuances intact. It does not commit the drift it was commissioned to catch. But it has **one high-severity honesty defect around what is "installed"/"buildable-now" on this box**, and several medium issues where labels, tests, and cluster-09 lessons are softer than the prose implies. Concrete findings below.

---

## HIGH severity

**H1 — "BUILDABLE-NOW" and "verified installed on this box" are false for the entire white-box stack. This is exactly the (b) dishonest/unchecked hardware claim.**
The doc's maturity legend defines `[BUILDABLE-NOW]` as "mature, CPU-native, pip-installable, **laptop-tested by the source dossier**." It then labels the white-box substrate `[BUILDABLE-NOW]` and writes traps as `[BUILDABLE-NOW facts]`. I checked the actual box:
- `z3` — **installed, v4.16.0** (doc says "verified installed on this box at v4.16.0.0" — TRUE, and the only true one).
- `transformers`, `sae_lens`, `nnsight`, `torchhd` — **all `ModuleNotFoundError`. None installed.**

So the *entire Family-A substrate* (gemma-2-2b in bf16 via transformers/TransformerLens, Gemma Scope SAEs via SAELens/nnsight) has **never been run, never been laptop-tested, and is not even installed**. The source dossiers (02/04) laptop-tested clingo/Z3/NetworkX/torchhd-class engines — they did **not** test a bf16 2B forward pass + SAE hook on this Ryzen. Calling that `[BUILDABLE-NOW]` under a definition that includes "laptop-tested" is precisely the rounding-up the doc claims to forbid.
**Fix:** Downgrade every white-box-substrate row from `[BUILDABLE-NOW]` to a new honest tier — `[PLAUSIBLE-UNTESTED]` or `[RESEARCH-GRADE]` — until a gemma-2-2b bf16 forward pass + one Gemma Scope SAE decode is actually run on this box and the peak-RSS is measured. Reserve `[BUILDABLE-NOW]` for the things literally verified installed (z3) or dossier-laptop-tested (clingo, NetworkX, CP-SAT). And strike "verified installed on this box" everywhere except z3.

**H2 — The 12.7GB / "thin fit, fits with care" RAM claim is unverified and the margin is thinner than stated, bordering on dishonest-by-omission.**
Total RAM measured **17.1GB** (not "16GB" — minor, but the doc treats 16 as the hard ceiling). The doc cites "HF's own utility reports ~12.7GB minimum system RAM for gemma-2-2b bf16 CPU inference alone" — that figure is **uncited** (no HF utility named, no link) and is for *inference alone*. The doc then admits "+ SAE + OS + Python" on top but still calls it "fits with care." On a box where the OS + a running Claude Code harness + Python already consume multiple GB, 12.7 + ~1 (SAE) + working set can plausibly **exceed available RAM and swap**, which for a bf16 model on spinning constraints means the "few tok/s" estimate is optimistic-to-fictional. This is an (b)-class unchecked feasibility claim on the load-bearing path.
**Fix:** Either measure peak RSS of the actual gemma-2-2b bf16 + SAE load on this box and report the real number, or label the whole Family-A-local path `[UNVERIFIED-MAY-SWAP]` and stop saying "fits." Name the HF utility (it reads like `accelerate estimate-memory` / the model-memory calculator) or delete the 12.7GB figure. Note the honest possibility: **Family A may not fit at all**, which would collapse the "literal goal is buildable-now on this box" thesis to "buildable only on a bigger box."

---

## MEDIUM severity

**M2 — "Reasons BETTER" is asserted for the top-line beachhead ahead of its own test (partial (c) violation).** The doc is *mostly* excellent on falsifiability (§5 pre-registers AURC/E-AURC/ECE/Brier bars — this is the doc's single strongest feature). But §4's summary line — "**The two reachable-now beachheads that genuinely reason over the substrate**" — asserts "genuinely reason over" as established fact for a path whose core loop (§2.4, SAE-features→symbolic-rules) it *elsewhere* admits is "`[RESEARCH-GRADE]`, UNBUILT anywhere." "Reasons over the substrate" and "reasons *better*" are being smuggled in the framing before §5.1 has been run. The linear-probe row claims detection "empirically strong (~80%)" with no citation for the 80% and no OOD number — and detection is not the goal-claim.
**Fix:** Change "genuinely reason over the substrate" → "are *architecturally positioned* to reason over the substrate, **pending the §5.1 exit test**." Attach a citation to every bare percentage (the ~80% probe number, the 82% Blocksworld — the latter is sourced, the former isn't).

**M3 — Rounds "resembles" up to "is" in the causal sub-case (a soft (d) violation).** §4 and the appendix call the DoWhy path "theorem-backed" and cite "arXiv:2605.27567 kernel-obstruction: the discrete causal decision must live OUTSIDE the LLM." I could not verify 2605.27567 (a 2026 paper; unverifiable from here), and the doc leans on it as a *theorem* proving the architecture is correct. A single uncorroborated arXiv preprint asserting an obstruction result is being elevated to "theorem-backed" — the same move `SKELETON` §1's anti-rounding discipline forbids ("resembles" ≠ "is"; and here "one preprint claims" ≠ "theorem-backed"). Do-calculus itself is sound (Pearl), but that soundness does **not** transfer to "the LLM-proposed DAG is correct" — garbage DAG in, rigorous-nonsense out. The doc half-acknowledges this in §7.1 ("DoWhy needs the variable set") but the §4 "theorem-backed / least human-scaffold-dependent" framing oversells.
**Fix:** Downgrade "theorem-backed" → "do-calculus is *sound given a correct DAG*; the DAG-proposal step is the untrusted LLM link and inherits GOFAI Rule 2." Mark 2605.27567 `[CITATION-UNVERIFIED]` unless someone has actually read it. State plainly: soundness of the *procedure* is not soundness of the *answer*.

**M4 — Dodges cluster-09's Failure Mode 4 (combinatorial explosion) — the one lesson that most threatens Family B (partial (e) dodge).** §7.3 lists cluster-09's three headline failures (verification bottleneck, combinatorial explosion, symbol grounding) and says the path "embraces the relocation." But look at what it does with combinatorial explosion specifically: 09 is unequivocal — "**Not fixed. The exponential wall is untouched.** The LLM can help navigate it heuristically but at the cost of soundness guarantees." The PATH doc's Family B *is* LLM-guided search (MCTS/ToT/GoT). The doc mentions the cost multiplier (10–100× calls, §3.3/§7.3-#3) as a **money** problem but never confronts it as the **soundness-vs-tractability** problem 09 names: the moment you use the LLM to prune the tree, you've traded the soundness that was the whole justification for reaching for a symbolic engine. The doc's own §2.3 knife-edge ("value must be engineered, never a 2nd LLM call") addresses the *scorer* but not the *search-space pruning*, which is where 09's Mode 4 actually bites.
**Fix:** Add to §7.1 an explicit "Family B inherits cluster-09 Mode 4 unchanged: LLM-guided pruning trades soundness for tractability; a sound scorer on the *accepted* node does not restore soundness over the *rejected* subtree." This is load-bearing because it means Family B can silently prune the correct plan.

**M5 — "Steering fragile" citations are 2026 preprints presented as settled empirics (unverifiable (b)/(d) risk).** §7.1's strongest honest concession — steer-half fragility — rests on arXiv:2604.15400 (attractor-dynamics), 2602.17881 (linear-rep breaks), 2606.08365 (SAE side-effects). These are all future-dated 2026 preprints I cannot verify, cited as if they are established results ("fails when the model reconstructs the suppressed signal within 2–3 downstream layers"). The *direction* of the concession is correct and admirable, but stating a specific mechanism ("within 2–3 downstream layers") from an unverified single preprint is the same over-precision M3 flags.
**Fix:** Soften to "reported to fail (single-preprint, unverified: arXiv:2604.15400)" and drop the false-precision "2–3 layers" unless corroborated. The concession survives — it just shouldn't masquerade as measured fact.

**M6 — Partial residual drift the doc names but under-weights: the §7.1 "hand-authored state space" admission is bigger than one bullet.** The doc honestly flags (§7.1) that pymdp/MCTS/DoWhy all need hand-built state spaces = "a milder cousin of the build-your-own-KB drift." Correct — but this is *the* commissioned drift wearing a Family-B costume, and it deserves more than "milder cousin." For the majority of Jarvis-relevant tasks there is no clean state space *and* no clean scorer (§7.3-#2 admits this) — which means Family B, for most real tasks, degrades to either (a) prompting or (b) the analyst hand-building the very symbolic scaffold the goal said not to retreat into. The doc reaches the right conclusion in §7.3 but the §2.2/§4 framing sells Family B as "`[BUILDABLE-NOW]` today" more confidently than §7 supports.
**Fix:** Reconcile the §2/§4 confidence with the §7 honesty — add to §2.2 a forward-pointer: "Family B is buildable *where a domain supplies both a natural state space and an engineered scorer*; §7.3 argues that region may be narrow. Do not read `[BUILDABLE-NOW]` as `broadly-applicable`."

---

## LOW severity

**L1 — Anthropic-reference reconciliation is correct; ignore the earlier self-flag.** The pre-write critique worried the doc contradicts memory's `AnthropicUnresponsive`. It does not — the doc uses the API technically and recommends no sales contact. That reconciliation was right. (Noting it so it isn't re-litigated.)

**L2 — "16GB" vs actual 17.1GB.** Minor, but the doc treats 16 as an inviolable ceiling in several feasibility calls. Real headroom is ~1GB more. Doesn't rescue H2, but the numbers should be the real ones.

**L3 — Unverifiable 2026 citations should carry a marker.** Beyond M3/M5: HalluSAE 2604.16430, refusal-audit 2605.30162, kernel-obstruction 2605.27567, CausalGraph2LLM, 2603.21172, 2510.11905, 2604.08224, 2606.26924 — a large fraction of the appendix is future-dated preprints I cannot check. The 4 I *could* check were all accurate, which earns some trust, but a `[unverified-2026-preprint]` tag on the rest is the honest move given the doc's own standard.

**L4 — §2.4 diagram claims Gemma Scope "publishes uncertainty/hallucination-adjacent features" — check this.** This is asserted as fact in the load-bearing loop step 2. Gemma Scope publishes SAEs, not curated "hallucination features"; those are found via downstream work (the HalluSAE-class papers, themselves unverified). Slight (d) rounding: "SAEs exist" → "uncertainty features are published."
**Fix:** "…features that *downstream work claims* correspond to uncertainty/confabulation (unverified)."

---

## Verdict: genuinely solid, with a fixable honesty hole

It is not ceremony and it does **not** drift. It correctly identifies that the folder inverted the goal, quotes the inversion verbatim, and refuses the safe-adjacent retreat. The one thing that would make me distrust it — an unfalsifiable "reasons better" claim — is largely pre-empted by a real §5 with pre-registered metrics.

**2 strongest points:**
1. **The white-box/black-box physics fork is correct and correctly load-bearing.** "You cannot reason OVER Claude — it is structurally impossible; the literal goal requires local open weights" is the single most important true thing in the whole folder, and I verified its factual basis (Anthropic exposes no logprobs, confirmed Feb 2026). This is the insight the prior folder never confronted.
2. **§5 falsifiable exit tests + the retirement of LLM-call-count as a metric.** Pre-registered AURC/E-AURC/ECE/Brier bars with an OOD slice, plus an explicit kill condition, is exactly the antidote to cluster-09's "died of unfalsifiable diagrams." Retiring call-count is the precise inversion the goal demands, stated cleanly.

**2 weakest points:**
1. **H1/H2 — the `[BUILDABLE-NOW]`/"installed"/"fits with care" claims for the white-box path are unchecked and partly false** (only z3 is installed; the 2B-bf16+SAE fit on 17GB is unmeasured and may swap or not fit). The doc's central "the literal goal is buildable *now, on this box*" promise is currently unproven and possibly false.
2. **M3/M4 — "theorem-backed" causality oversells, and cluster-09's combinatorial-explosion lesson (soundness lost the moment the LLM prunes) is acknowledged as a cost-problem but dodged as the soundness-problem it actually is.** These are the two places the doc's honesty discipline slips below its own standard.

**One-line fix that closes most of the gap:** actually run one gemma-2-2b bf16 forward pass + one Gemma Scope SAE decode on this box, report peak RSS and tok/s, and re-tier every white-box row against that measurement — then the doc's boldest claim is either verified or honestly downgraded.