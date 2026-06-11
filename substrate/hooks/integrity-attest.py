#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""JARVIS integrity attestation — the tamper-EVIDENT answer to "it's just files".

Computes a Merkle root over the governed substrate (every gate hook + every
memory primitive). The root is committed to public git: anyone can re-run this,
recompute the root, and check it against the committed manifest. Files stay
files (inspectable); cryptography proves they weren't modified outside the
sanctioned flow. This is the CKB primitive -- off-chain storage + on-chain
commitment -- applied to JARVIS's own body. Stdlib only.

  verify : recompute, compare to manifest, exit 1 + report drift on mismatch
  commit : recompute, write manifest (the new attested baseline)
"""
import hashlib
import json
import os
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HOME = os.path.expanduser("~")
MEM = os.path.join(HOME, ".claude", "projects", "C--Users-Will", "memory")
GOVERNED = [
    (os.path.join(HOME, ".claude", "hooks"), ".py"),
    (os.path.join(HOME, ".claude", "session-chain"), ".py"),
    (os.path.join(HOME, ".claude", "bin"), ".py"),
    (MEM, ".md"),
]
MANIFEST = os.path.join(MEM, "_system", "integrity_manifest.json")


def _leaves() -> list[tuple[str, str]]:
    out = []
    for root, ext in GOVERNED:
        if not os.path.isdir(root):
            continue
        for fn in sorted(os.listdir(root)):
            if not fn.endswith(ext):
                continue
            p = os.path.join(root, fn)
            try:
                h = hashlib.sha256(open(p, "rb").read()).hexdigest()
            except Exception:
                continue
            rel = os.path.relpath(p, HOME).replace("\\", "/")
            out.append((rel, h))
    return sorted(out)


def _merkle(leaves: list[str]) -> str:
    if not leaves:
        return hashlib.sha256(b"").hexdigest()
    layer = [bytes.fromhex(x) for x in leaves]
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            a = layer[i]
            b = layer[i + 1] if i + 1 < len(layer) else layer[i]
            nxt.append(hashlib.sha256(a + b).digest())
        layer = nxt
    return layer[0].hex()


def _root(leaves):
    return _merkle([h for _, h in leaves])


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "verify"
    _BOOT_INLINE = True
    leaves = _leaves()
    root = _root(leaves)
    counts = {}
    for rel, _ in leaves:
        d = rel.split("/")[-2] if "/" in rel else "."
        counts[d] = counts.get(d, 0) + 1

    if mode == "boot":
        # SessionStart: verify silently, scream via additionalContext on drift
        import json as _j
        try:
            m = json.load(open(MANIFEST, encoding="utf-8"))
        except Exception:
            print(_j.dumps({})); return 0
        if m.get("merkle_root") == root:
            print(_j.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                "additionalContext": f"[INTEGRITY OK] {len(leaves)} governed files match attested root {root[:12]}."}}))
        else:
            print(_j.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                "additionalContext": f"[INTEGRITY DRIFT] root {root[:12]} != attested {str(m.get('merkle_root'))[:12]}. A gate or primitive changed since last attestation -- if sanctioned re-attest (integrity-attest.py commit), else investigate tampering BEFORE work."}}))
        return 0

    mode_dispatch_done = False

    if mode == "commit":
        os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
        json.dump({
            "merkle_root": root,
            "leaf_count": len(leaves),
            "by_dir": counts,
            "attested_at_unix": int(time.time()),
            "note": "recompute with `python integrity-attest.py verify`; "
                    "root is committed to public git as tamper-evidence",
        }, open(MANIFEST, "w", encoding="utf-8", newline="\n"), indent=2)
        print(f"ATTESTED root={root[:16]}... over {len(leaves)} governed files {counts}")
        return 0

    # verify
    try:
        m = json.load(open(MANIFEST, encoding="utf-8"))
    except Exception:
        print("integrity: no manifest yet -- run `commit` to establish baseline")
        return 0
    if m.get("merkle_root") == root:
        print(f"INTEGRITY OK root={root[:16]}... {len(leaves)} files match attestation")
        return 0
    # drift: find which files changed vs a stored leaf snapshot if present
    print(f"⚠ INTEGRITY DRIFT — root {root[:16]}... != attested {str(m.get('merkle_root'))[:16]}...")
    print(f"  governed now: {len(leaves)} files {counts}")
    print(f"  attested:     {m.get('leaf_count')} files {m.get('by_dir')}")
    print("  a gate or primitive changed since last attestation. If sanctioned, "
          "run `commit` to re-attest; if not, you just caught tampering.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
