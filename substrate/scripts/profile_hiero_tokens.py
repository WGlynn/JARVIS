#!/usr/bin/env python3
"""HIERO operator token-cost profile vs ASCII alternatives.
cl100k_base BPE (GPT-4 family) as proxy for Claude tokenizer.
Path 5: find multi-token Unicode ops, propose 1-token swaps."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

try:
    import tiktoken
except ImportError:
    print("pip install tiktoken", file=sys.stderr)
    sys.exit(1)

enc = tiktoken.get_encoding("cl100k_base")

HIERO_OPS = [
    ("forall", "∀", "ALL"),
    ("exists", "∃", "EXI"),
    ("implies", "⇒", "->"),
    ("rev_impl", "⇐", "<-"),
    ("iff", "⇔", "<->"),
    ("and", "∧", "&"),
    ("or", "∨", "|"),
    ("not", "¬", "!"),
    ("xor", "⊕", "^"),
    ("equiv", "≡", "=="),
    ("approx", "≈", "~="),
    ("neq", "≠", "!="),
    ("leq", "≤", "<="),
    ("geq", "≥", ">="),
    ("in", "∈", "in"),
    ("nin", "∉", "!in"),
    ("subset", "⊂", "sub"),
    ("superset", "⊃", "sup"),
    ("union", "∪", "U"),
    ("intersect", "∩", "N"),
    ("orthogonal", "⊥", "_|_"),
    ("parallel", "∥", "||"),
    ("therefore", "∴", ":."),
    ("because", "∵", ".:"),
    ("arrow", "→", "->"),
    ("uparrow", "↑", "^"),
    ("downarrow", "↓", "v"),
    ("check", "✓", "OK"),
    ("cross", "✗", "NO"),
    ("dagger", "†", "+"),
    ("bullet", "•", "*"),
    ("dot", "·", "."),
    ("times", "×", "x"),
    ("divide", "÷", "/"),
    ("plusminus", "±", "+-"),
    ("delta", "Δ", "D"),
    ("phi", "φ", "phi"),
    ("infinity", "∞", "inf"),
    ("ellipsis", "…", "..."),
    ("nabla", "∇", "grad"),
]

def cost(s):
    toks = enc.encode(s)
    return len(toks), toks

print(f"{'OP':<12} {'UNI':<6} {'tok':<4} {'ASCII':<6} {'tok':<4} {'win':<5} {'note'}")
print("-" * 70)

total_uni = 0
total_ascii = 0
wins = []
losses = []
ties = []

for name, uni, ascii_alt in HIERO_OPS:
    u_n, _ = cost(uni)
    a_n, _ = cost(ascii_alt)
    total_uni += u_n
    total_ascii += a_n
    diff = u_n - a_n
    if diff > 0:
        wins.append((name, uni, u_n, ascii_alt, a_n, diff))
        marker = f"SAVE{diff}"
    elif diff < 0:
        losses.append((name, uni, u_n, ascii_alt, a_n, -diff))
        marker = f"LOSE{-diff}"
    else:
        ties.append((name, uni, u_n))
        marker = "tie"
    print(f"{name:<12} {uni:<6} {u_n:<4} {ascii_alt:<6} {a_n:<4} {marker:<5}")

print("-" * 70)
print(f"TOTAL unicode tokens : {total_uni}")
print(f"TOTAL ascii tokens   : {total_ascii}")
print(f"Net savings if swap  : {total_uni - total_ascii}")
print(f"Wins (swap)          : {len(wins)}")
print(f"Losses (keep uni)    : {len(losses)}")
print(f"Ties                 : {len(ties)}")

print("\n=== SWAP RECOMMENDATIONS (HIERO++ candidates) ===")
for name, uni, u_n, ascii_alt, a_n, diff in sorted(wins, key=lambda x: -x[5]):
    print(f"  {uni} ({u_n}t) -> {ascii_alt} ({a_n}t)  saves {diff}/use   [{name}]")

print("\n=== KEEP UNICODE (already 1-token or cheaper) ===")
for name, uni, u_n, ascii_alt, a_n, diff in losses:
    print(f"  {uni} ({u_n}t) beats {ascii_alt} ({a_n}t)  [{name}]")
for name, uni, n in ties:
    print(f"  {uni} ({n}t) ties ASCII  [{name}]")
