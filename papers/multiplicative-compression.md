# Multiplicative Compression

How HIERO++ tokenizer-tuned writing composes with server-side prompt caching to produce an order-of-magnitude reduction in multi-turn agent session cost.

---

The standard framing of LLM compression research treats context compression, model compression, and orchestration compression as three separate optimization problems. They get cited in different papers, shipped in different layers of the stack, and rarely compared on the same workload. This paper argues that for a specific deployment shape — multi-turn agent substrates where the same large boot context loads repeatedly across many turns — two of these compression axes compose multiplicatively rather than additively, and the combined leverage is substantially larger than either axis alone.

The two axes are tokenizer-aware writing on the byte side (concretely, the HIERO++ format introduced in `hiero.md`) and server-side prompt caching on the read side (concretely, the API-native caching offered by Anthropic and structurally similar offerings from other providers). The first reduces the size of the boot prefix that gets loaded into model context. The second reduces the per-turn cost of reading whatever boot prefix is stable across a session window. The result of applying both is not a sum of two single-digit percentage savings. It is a multiplication: every byte saved on the prefix is paid back at the discounted cache-read rate on every turn that hits the cache, across the lifetime of the session.

This paper presents the math behind the multiplicative compound, the empirical compression numbers from a working agent substrate (the JARVIS memory corpus), and a discussion of the limits, blind spots, and measurement gaps in the current setup.

---

## The multiplicative chain

A multi-turn agent session has a fixed-cost component (the boot context that loads once and stays through the session) and a per-turn component (the model's reasoning and tool-call generation that happens at each user prompt). Without caching, the boot context is paid in full on every model call: the harness sends the entire system prompt, the entire memory block, the entire conversation history, and the model bills the full input-token cost on each call. For an agent substrate where the boot memory is on the order of 10 to 30 thousand tokens and turns happen 30 to 100 times per session, the boot block dominates session cost. The model is paying full price to re-read the same memory file at every turn.

Server-side prompt caching changes the per-turn cost of the boot block from the full input rate to a discounted rate. Anthropic publishes the rate at roughly 0.1 times base for cached reads, with a one-time write premium of roughly 1.25 times base on the first turn that establishes the cache entry. The TTL is short (around five minutes on the standard tier), so the cache hits depend on whether the agent is active enough to refresh the entry. For a working agent session where the user is sending prompts every few minutes, the cache stays warm and most turns are cache hits.

The compound is straightforward arithmetic. Let `B` be the byte count of the boot prefix, `R` the byte-to-token ratio of the tokenizer (about 0.27 tokens per byte for cl100k_base on prose, slightly different for Claude's BPE but in the same neighborhood), and `N` the number of turns per session. Without compression and without caching, the input-token cost contributed by the boot prefix is `B * R * N` token-units paid at the base rate. With HIERO++ compression that reduces `B` to some fraction `f1` of the original, and with cache hits that reduce the per-read rate to some fraction `f2` of base, the cost becomes `(f1 * B) * R * (f2 * (N - 1) + 1.25)` for the first turn plus all subsequent cached turns. The savings ratio is approximately `f1 * f2` for the cached portion of the session, plus the small write-premium on the first turn.

The point is not that either factor alone is dramatic. HIERO++ on the operator slice of real prose saves about 4 to 7 percent of total tokens; the prompt cache discount is about 90 percent on hits. Either alone is a small or single-axis win. The compound is the win. On a session with 50 turns, a 5 percent byte savings on the boot prefix translates to a 5 percent reduction in tokens billed at the discounted rate across 49 turns, plus 5 percent on the first uncached read. The cost reduction relative to no-compression-no-cache is the product, not the sum.

For the JARVIS substrate today, the numbers are concrete. Before today's structural compression pass, MEMORY.md alone was 6,779 cl100k_base tokens at 24,683 bytes. After extracting the active-posture section to a sub-index that the memory preprocessor injects at boot time, MEMORY.md fell to 3,026 tokens at 11,260 bytes, a 55 percent reduction on the main file. The full boot-loaded memory corpus (MEMORY.md plus the auto-injected sub-indexes plus the WWWD priority cache) fell from 11,939 tokens to 9,289 tokens, a 22 percent reduction across the entire injected set. On a session running 50 turns at 9,000 cached tokens per turn, the uncached scenario would bill 450,000 input tokens against the boot prefix. With the prompt cache at 0.1x reads after the first turn, the same usage bills about 45,000 tokens plus the 12,500-token write premium on turn one. The post-compression session bills against 9,289 cached tokens, which is 56,500 tokens for the same session shape. The combined HIERO++ compression and cache discount lands at roughly an order of magnitude below the uncompressed-uncached baseline.

---

## Why HIERO++ is the right side of the multiplication

The cache discount applies to whatever boot block the harness flags as cacheable. The substrate operator does not control the discount rate. The operator does control the byte count of the boot block. Every byte the operator removes from the boot prefix is a byte that gets multiplied through every cached turn in the session. The byte side of the equation is the side the operator can influence directly.

HIERO++ is a tokenizer-tuned variant of the HIERO format. The full HIERO++ dictionary lives in `R·hiero-pp-dictionary.md`. The empirical case for the swaps is straightforward: cl100k_base tokenizes most Unicode logic operators as multi-token sequences. The implication operator (⇒) tokenizes to three tokens. The conjunction (∧) tokenizes to two tokens. The ASCII alternatives that carry the same semantics in the dense-logic context of memory files (`->` for implication, `&` for conjunction, `|` for disjunction, `==` for equivalence) tokenize to one token each. Across a representative operator set of 40 symbols, the Unicode form spans 76 tokens and the ASCII form spans 44 tokens, a 42 percent reduction on the operator slice. On real memory prose where operators are roughly 5 to 10 percent of the content, the document-wide token reduction lands at 4 to 7 percent. That is the per-document number. The compound with prompt caching multiplies that 4 to 7 percent across the session lifetime.

The HIERO++ swaps are not lossy in the semantic sense. They are a notation choice. A future reader of the corpus, whether human or model, can decode `->` as implication the same way they decode the Unicode glyph, given the dictionary. The dictionary cost is paid once per reader. The tokenization savings accrue every time the corpus is loaded into context.

---

## The structural extraction layer

Tokenizer-aware swaps are not the only byte-side lever. The bigger move on the byte side is structural: extracting heavy sections of the boot file into sub-indexes that the memory preprocessor injects at boot time. This is the move that produced the 55 percent reduction on MEMORY.md mentioned earlier. The active-posture section of the file was 13 kilobytes of detail rows, each one a primitive name plus a one-line summary plus a link to the underlying primitive file. Extracting that section to `MEMORY_INDEX_ACTIVE.md` with the existing convention used by the memory preprocessor cut the main file in half. The detail still loads at boot because the preprocessor globs `MEMORY_INDEX_*.md` files and injects them as additional boot context.

The semantic content of the session is the same. The cache eligibility of the preprocessor-injected blocks depends on the harness, but the main file's reduction directly cuts the size of the boot prefix the harness flags as cacheable. The structural move and the tokenizer move compose. The structural move drops the prefix size by half. The tokenizer move drops what remains by another 4 to 7 percent. The cache discount applies to whatever survives both passes.

---

## Honest limits

Several gaps in this analysis are worth naming explicitly.

The first gap is cache observability. The HIERO++ side of the multiplication is something the operator can measure directly: the file is N tokens long, full stop. The cache side is something the operator does not directly observe. The harness flags blocks as cacheable, the API returns billing information, and the operator infers the cache hit rate from the billing delta. Until the operator wires explicit telemetry that distinguishes cached and uncached tokens, the multiplicative claim is supported by the API pricing documentation rather than by direct measurement on the running substrate. The first concrete next step on the substrate is to plumb cache-hit telemetry through the hook layer so the actual savings are visible per session.

The second gap is task-quality verification. The compression claims in this paper are all token-side: bytes reduced, tokens reduced, cost reduced. None of them are accompanied by a round-trip semantic-equivalence benchmark. The literature on context compression includes BERTScore comparisons, downstream task accuracy on QA datasets, and reconstruction quality on standardized prompts. The JARVIS substrate has shipped 4 to 7 percent and 22 percent and 55 percent compression numbers across the session without a benchmark that demonstrates the post-compression substrate answers the same questions with the same quality as the pre-compression substrate. Subjective working judgment says yes, but the defensible claim requires a benchmark. That is the next research move.

The third gap is the tokenizer mismatch. The empirical numbers in this paper use cl100k_base as a proxy for Claude's tokenizer. The two are not identical. The ratio of bytes to tokens is similar but not exact. The relative ordering of which Unicode operators are 1-token versus 2-token versus 3-token is likely preserved across both tokenizers because both use byte-pair encoding trained on similar corpora, but the absolute token counts will differ. A meaningful next move is to re-run the operator profile against Claude's tokenizer directly via the API to confirm the swap recommendations land the same way.

The fourth gap is the harness opacity. The Claude Code harness manages caching internally. Whether it flags the boot context as cacheable, what the breakpoint structure looks like, how it handles eviction, and what the actual hit rate is on a multi-turn session are all opaque to the substrate operator. The multiplicative compound depends on the harness using the cache. If the harness chooses not to cache certain blocks, the compound collapses to the single-axis byte-savings number.

---

## Related work

The closest formal work in the literature is the line of papers on context compression for retrieval-augmented generation: LLMLingua and LLMLingua-2 from Microsoft, RECOMP from Xu et al., the ICAE in-context autoencoder from Chevalier et al., and the AutoCompressor variant from Ge et al. These approaches focus on compressing retrieved context (documents that get pulled in per-query) using either a token-level classifier (LLMLingua family) or a learned encoder that produces compressed memory slots (ICAE, AutoCompressor). They report compression ratios in the 2x to 26x range depending on technique, with task-quality drops in the single-digit-percent range.

The work that is closest in spirit but not in formal expression is the community discussion around tokenizer fairness and the Petrov et al. NeurIPS 2023 paper on tokenizer-introduced disparities. That paper documents that different languages and scripts tokenize at very different bytes-per-token ratios under common tokenizers, with implications for fairness and cost. The same observation applies to notation choice within a single language: dense logic notation tokenizes very differently depending on which glyphs the writer picks. No published paper formalizes this as a writing discipline. HIERO++ is, as far as I can find, the first concrete operationalization of tokenizer-aware writing as a deliberate compression layer.

The orchestration side of the compound is well-documented. Anthropic's "Code execution with MCP" engineering post (November 2025) reports a customer trace where five tool calls collapsed to one Python script ran at 150,000 tokens before and 2,000 tokens after, a 98.7 percent reduction. Cognition's "Don't Build Multi-Agents" post (June 2025) and the AgentBoard benchmark suite document that multi-agent fan-out adds 3x to 15x token overhead versus single-agent baselines on shared-context tasks, and that single-agent ties or beats multi-agent on roughly 64 percent of standard agent benchmarks at half the cost. These results do not compose multiplicatively with the boot-prefix compression discussed here; they operate on a different cost axis. But they suggest that the compounding-leverage framing applies across other compression-axis pairs as well, and that the substrate-design discipline is to identify which compression layers compose and instrument them to fire together.

---

## Conclusion

The single byte saved on a memory file in a tokenizer-aware way is a small number. The single API discount on a cached read is a known number. The product of the two, applied across a multi-turn agent session, is an order-of-magnitude reduction in session cost that is neither side alone.

This is the right framing for substrate-design research going forward. The question is not which single compression technique is best. The question is which compression layers compose with which other layers, and what the operator can instrument to capture the compound. For multi-turn LLM agent substrates, byte-side compression and read-side caching are a pair that composes. Anything that reduces the boot prefix is multiplied by the cache discount across the session lifetime.

The substrate-port implication of this result is that any other operator running a similar shape (Claude Code or another harness with prompt caching, plus a persistent memory corpus) can apply both sides of the compound and capture the same multiplicative win. The HIERO++ dictionary lives in the JARVIS substrate memory under `R·hiero-pp-dictionary.md`. The substrate is open. Anyone willing to write under the discipline can capture the byte side; the cache side is API-native and applies automatically to any caller using the standard prompt-cache control.
