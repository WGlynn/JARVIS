#!/usr/bin/env python3
"""Gap-3 dissolution: cross-BPE convergence test for HIERO++ swap recommendations.

Rationale: if the swap-table rank-ordering is stable across multiple
independently-trained BPE tokenizers (cl100k_base GPT-4, o200k_base GPT-4o,
plus any Claude-community port), then the cl100k_base proxy is good enough
for the swap recommendations even though Claude's exact tokenizer differs.

The absolute token counts will differ between BPEs. The *which-ops-save-tokens*
ranking is what the HIERO++ dictionary depends on, and that is what we test.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

try:
    import tiktoken
except ImportError:
    print("pip install tiktoken", file=sys.stderr)
    sys.exit(1)

HIERO_OPS = [
    ("forall", "∀", "ALL"),
    ("implies", "⇒", "->"),
    ("rev_impl", "⇐", "<-"),
    ("iff", "⇔", "<->"),
    ("and", "∧", "&"),
    ("or", "∨", "|"),
    ("not", "¬", "!"),
    ("xor", "⊕", "^"),
    ("equiv", "≡", "=="),
    ("neq", "≠", "!="),
    ("leq", "≤", "<="),
    ("geq", "≥", ">="),
    ("in", "∈", "in"),
    ("subset", "⊂", "sub"),
    ("superset", "⊃", "sup"),
    ("union", "∪", "U"),
    ("intersect", "∩", "N"),
    ("orthogonal", "⊥", "_|_"),
    ("therefore", "∴", ":."),
    ("because", "∵", ".:"),
    ("check", "✓", "OK"),
    ("cross", "✗", "NO"),
    ("delta", "Δ", "D"),
    ("infinity", "∞", "inf"),
    ("nabla", "∇", "grad"),
    ("arrow", "→", "->"),
    ("dagger", "†", "+"),
    ("bullet", "•", "*"),
    ("dot", "·", "."),
    ("times", "×", "x"),
]

# Two reference BPEs from tiktoken — both publicly distributed,
# both independently trained, different vocab sizes (100k vs 200k).
ENCODERS = {}
try:
    ENCODERS["cl100k_base (GPT-4)"] = tiktoken.get_encoding("cl100k_base")
except Exception as e:
    print(f"cl100k_base unavailable: {e}")
try:
    ENCODERS["o200k_base (GPT-4o)"] = tiktoken.get_encoding("o200k_base")
except Exception as e:
    print(f"o200k_base unavailable: {e}")

# Try Hugging Face's Claude tokenizer community port if available.
try:
    from transformers import AutoTokenizer
    try:
        hf_tok = AutoTokenizer.from_pretrained("Xenova/claude-tokenizer")

        class HFAdapter:
            def __init__(self, t): self.t = t
            def encode(self, s): return self.t.encode(s, add_special_tokens=False)

        ENCODERS["claude-community-port"] = HFAdapter(hf_tok)
    except Exception as e:
        print(f"(Xenova/claude-tokenizer not loaded: {e})")
except ImportError:
    print("(transformers not installed; skipping community Claude tokenizer)")

if not ENCODERS:
    print("No tokenizers available. Aborting.")
    sys.exit(1)

# For each tokenizer, compute (uni_tok, ascii_tok, delta) per op.
results = {name: [] for name in ENCODERS}
for name, enc in ENCODERS.items():
    for op_name, uni, ascii_alt in HIERO_OPS:
        u_n = len(enc.encode(uni))
        a_n = len(enc.encode(ascii_alt))
        results[name].append((op_name, uni, u_n, ascii_alt, a_n, u_n - a_n))

# Build convergence matrix: does each tokenizer agree on the sign of the delta?
print("\n" + "=" * 78)
print("Cross-BPE convergence test — HIERO++ swap recommendations")
print("=" * 78)
print(f"\n{'op':<14} ", end="")
for name in ENCODERS:
    print(f"{name[:24]:>26} ", end="")
print()
print("-" * (14 + 27 * len(ENCODERS)))

agree_count = 0
disagree_count = 0
for i, (op_name, uni, ascii_alt) in enumerate(HIERO_OPS):
    deltas = []
    for name in ENCODERS:
        d = results[name][i][5]
        deltas.append(d)
    signs = [(1 if d > 0 else (-1 if d < 0 else 0)) for d in deltas]
    all_agree = len(set(signs)) == 1
    if all_agree:
        agree_count += 1
    else:
        disagree_count += 1
    print(f"{op_name:<14} ", end="")
    for j, name in enumerate(ENCODERS):
        u_n = results[name][i][2]
        a_n = results[name][i][4]
        d = results[name][i][5]
        marker = "SAVE" if d > 0 else ("LOSE" if d < 0 else "tie")
        print(f"  {uni}({u_n}) {ascii_alt}({a_n}) {marker}{'+'+str(abs(d)) if d else ''}".ljust(27), end=" ")
    print()

print("-" * (14 + 27 * len(ENCODERS)))
print(f"\nAgreement (all BPEs agree on save/lose/tie): {agree_count}/{len(HIERO_OPS)} = {100*agree_count/len(HIERO_OPS):.0f}%")
print(f"Disagreement: {disagree_count}/{len(HIERO_OPS)}")

if disagree_count == 0:
    print("\n[GAP 3 RESULT] Swap recommendations are STABLE across all tested BPEs.")
    print("cl100k_base is a sufficient proxy for the swap-table direction.")
    print("Absolute counts may differ on Claude's exact tokenizer; rank order does not.")
elif disagree_count < len(HIERO_OPS) * 0.1:
    print(f"\n[GAP 3 RESULT] Swap recommendations are MOSTLY STABLE ({disagree_count} disagreements).")
    print("Review the disagreeing ops; cl100k_base proxy is good for the rest.")
else:
    print(f"\n[GAP 3 RESULT] Significant BPE divergence ({disagree_count} disagreements).")
    print("Need direct Claude API token-count to validate.")
