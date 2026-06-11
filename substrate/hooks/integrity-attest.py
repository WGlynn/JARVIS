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

# ── Tamper-RESISTANCE (standard tier): Ed25519 signature over the Merkle root. ──
# Merkle alone is tamper-EVIDENT (you can detect a change) but an attacker can
# re-run `commit` to re-baseline and silence the drift. Signing the root makes
# `commit` require a key held OUTSIDE the governed tree, so the drift cannot be
# silenced without the secret. Standard primitive (ssh-keygen Ed25519 sigs), no
# new deps. Honest boundary: the key is on-disk here (tier 1) -- a local-root
# attacker who reads it can still re-sign; tier 2 = passphrase + OS-keychain/TPM/
# YubiKey so the key cannot be exfiltrated. Verify needs only the PUBLIC key, so
# the automated boot path never touches a secret.
KEYDIR = os.path.join(HOME, ".claude", "keys")
SIGN_KEY = os.path.join(KEYDIR, "jarvis-attest")
ALLOWED_SIGNERS = os.path.join(KEYDIR, "allowed_signers")
SIG_NS = "jarvis-attest"
SIG_IDENTITY = "jarvis@local"


def _sign_root(root: str):
    """Sign the root string with the Ed25519 attestation key. Returns sig dict or None."""
    if not os.path.exists(SIGN_KEY):
        return None
    import subprocess
    import tempfile
    try:
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "root")
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(root)
            r = subprocess.run(["ssh-keygen", "-Y", "sign", "-f", SIGN_KEY, "-n", SIG_NS, p],
                               capture_output=True, text=True)
            if r.returncode != 0:
                return None
            sig = open(p + ".sig", encoding="utf-8").read()
        return {"signature": sig, "signer": SIG_IDENTITY, "namespace": SIG_NS,
                "scheme": "ssh-ed25519"}
    except Exception:
        return None


def _verify_root_sig(root: str, m: dict):
    """Verify the manifest's signature over `root`. Returns (ok, detail)."""
    sig = m.get("signature")
    if not sig:
        return (None, "unsigned manifest (tamper-evident only; run commit with a key to enable resistance)")
    if not os.path.exists(ALLOWED_SIGNERS):
        return (False, "no allowed_signers file -- cannot verify")
    import subprocess
    import tempfile
    try:
        with tempfile.TemporaryDirectory() as td:
            sp = os.path.join(td, "root.sig")
            with open(sp, "w", encoding="utf-8", newline="") as f:
                f.write(sig)
            r = subprocess.run(
                ["ssh-keygen", "-Y", "verify", "-f", ALLOWED_SIGNERS,
                 "-I", m.get("signer", SIG_IDENTITY), "-n", m.get("namespace", SIG_NS),
                 "-s", sp],
                input=root, capture_output=True, text=True)
        return (r.returncode == 0, (r.stderr or r.stdout).strip())
    except Exception as e:
        return (False, f"verify error: {e}")


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
        if m.get("merkle_root") != root:
            print(_j.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                "additionalContext": f"[INTEGRITY DRIFT] root {root[:12]} != attested {str(m.get('merkle_root'))[:12]}. A gate or primitive changed since last attestation -- if sanctioned re-attest (integrity-attest.py commit), else investigate tampering BEFORE work."}}))
            return 0
        ok, detail = _verify_root_sig(root, m)
        if ok is False:
            # root matches but signature is invalid/missing-with-allowed-signers ->
            # the manifest itself was altered (re-baselined without the key). Strong tamper signal.
            print(_j.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                "additionalContext": f"[INTEGRITY ALERT — SIGNATURE INVALID] root matches but the attestation signature does not verify ({detail}). The manifest was re-baselined WITHOUT the attestation key. Treat as tampering BEFORE work."}}))
        elif ok is None:
            print(_j.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                "additionalContext": f"[INTEGRITY OK — unsigned] {len(leaves)} files match root {root[:12]} (tamper-evident; sign with integrity-attest.py commit to add resistance)."}}))
        else:
            print(_j.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                "additionalContext": f"[INTEGRITY OK — SIGNED] {len(leaves)} governed files match attested root {root[:12]}, Ed25519 signature verified."}}))
        return 0

    mode_dispatch_done = False

    if mode == "commit":
        os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
        manifest = {
            "merkle_root": root,
            "leaf_count": len(leaves),
            "by_dir": counts,
            "attested_at_unix": int(time.time()),
            "note": "recompute with `python integrity-attest.py verify`; root is "
                    "committed to public git as tamper-evidence, and signed (Ed25519) "
                    "as tamper-resistance -- the signature cannot be forged without the "
                    "attestation key held outside the governed tree",
        }
        sig = _sign_root(root)
        if sig:
            manifest.update(sig)
        json.dump(manifest, open(MANIFEST, "w", encoding="utf-8", newline="\n"), indent=2)
        sig_state = "SIGNED" if sig else "UNSIGNED (no key -- evidence only)"
        print(f"ATTESTED [{sig_state}] root={root[:16]}... over {len(leaves)} governed files {counts}")
        return 0

    # verify
    try:
        m = json.load(open(MANIFEST, encoding="utf-8"))
    except Exception:
        print("integrity: no manifest yet -- run `commit` to establish baseline")
        return 0
    if m.get("merkle_root") == root:
        ok, detail = _verify_root_sig(root, m)
        if ok is True:
            print(f"INTEGRITY OK [SIGNED] root={root[:16]}... {len(leaves)} files match + Ed25519 signature verified")
            return 0
        if ok is None:
            print(f"INTEGRITY OK [UNSIGNED] root={root[:16]}... {len(leaves)} files match (tamper-evident only; run commit with a key for resistance)")
            return 0
        print(f"⚠ INTEGRITY ALERT — root matches but SIGNATURE INVALID ({detail}). "
              "Manifest re-baselined without the attestation key = tampering.")
        return 1
    # drift: find which files changed vs a stored leaf snapshot if present
    print(f"⚠ INTEGRITY DRIFT — root {root[:16]}... != attested {str(m.get('merkle_root'))[:16]}...")
    print(f"  governed now: {len(leaves)} files {counts}")
    print(f"  attested:     {m.get('leaf_count')} files {m.get('by_dir')}")
    print("  a gate or primitive changed since last attestation. If sanctioned, "
          "run `commit` to re-attest; if not, you just caught tampering.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
