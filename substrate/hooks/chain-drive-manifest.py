#!/usr/bin/env python3
"""Generate the Node-3 (Google Drive) tip-attestation manifest, deterministically.

Node 3 is AGENT-DRIVEN: the Google Drive MCP tools are only available to a live
Jarvis turn, never to the headless Stop hook. So the headless backup can't push to
Drive -- but it CAN regenerate this tiny manifest on disk, and a live agent (or the
autopilot cron) uploads it via mcp__..._Google_Drive__create_file into folder
DRIVE_FOLDER_ID, overwriting the prior manifest.

The manifest is a ~800-byte tip attestation: HEAD + a sha256 of the whole
chain.jsonl + block count + the full-content GitHub node URLs. It proves the chain
tip and lets anyone detect divergence; the full walkable log lives 2x on GitHub.

Usage:
  python chain-drive-manifest.py            # write manifest to OUT, print it
  python chain-drive-manifest.py --ts <iso> # stamp a specific generated-time
"""
import hashlib
import json
import os
import sys

HOME = os.path.expanduser("~")
CHAIN = os.path.join(HOME, ".claude", "session-chain", "handoff-chain")
CHAINLOG = os.path.join(CHAIN, "chain.jsonl")
HEAD = os.path.join(CHAIN, "HEAD.json")
OUT = os.path.join(CHAIN, "drive-manifest.json")
DRIVE_FILE_TITLE = "chain-manifest.json"


def _canonical_folder_id():
    """Single-source the Drive folder id from chain-backup.py so the two files can
    never drift (a concurrent autopilot turn once created a duplicate folder --
    this makes that class impossible)."""
    import importlib.util
    cb = os.path.join(HOME, ".claude", "session-chain", "chain-backup.py")
    try:
        spec = importlib.util.spec_from_file_location("_cb_fid", cb)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.GDRIVE_FOLDER_ID
    except Exception:
        return "1lZ25dbnB0FXDtNY6aaJ8mcQoxOjg68lL"  # canonical fallback


DRIVE_FOLDER_ID = _canonical_folder_id()


def build(ts="unknown"):
    with open(CHAINLOG, "rb") as f:
        chain = f.read()
    head = json.load(open(HEAD, encoding="utf-8"))
    return {
        "kind": "jarvis-chain tip-attestation (Node 3 / Google Drive)",
        "generated": ts,
        "head_seq": head["seq"],
        "head_file": head["file"],
        "head_hash": head["hash"],
        "chainlog_sha256": hashlib.sha256(chain).hexdigest(),
        "block_count": chain.decode("utf-8", "replace").strip().count("\n") + 1,
        "genesis": "SESSION-HANDOFF-2026-06-20.md",
        "full_content_nodes": [
            "github.com/WGlynn/jarvis-chain (private)",
            "github.com/WGlynn/claude-memory-backup (private)",
        ],
        "drive_folder_id": DRIVE_FOLDER_ID,
        "drive_file_title": DRIVE_FILE_TITLE,
        "verify": ("clone a full node, run: python session-chain/handoff-chain.py "
                   "--walk; sha256(chain.jsonl) must equal chainlog_sha256 above"),
        "note": ("Node 3 is agent-driven (MCP is not available to the headless Stop "
                 "hook). A live agent uploads this file to drive_folder_id."),
    }


def stage(ts="unknown"):
    """Write the manifest to disk (atomic). Returns (path, manifest_dict)."""
    m = build(ts)
    tmp = OUT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(m, f, indent=2)
    os.replace(tmp, OUT)
    return OUT, m


if __name__ == "__main__":
    ts = "unknown"
    if "--ts" in sys.argv:
        ts = sys.argv[sys.argv.index("--ts") + 1]
    path, m = stage(ts)
    print(f"staged -> {path}")
    print(json.dumps(m, indent=2))
