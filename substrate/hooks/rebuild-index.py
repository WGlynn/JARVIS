#!/usr/bin/env python3
"""
Rebuild session-chain index.json from the block files (recovery, 2026-08-07).

index.json was truncated to 0 bytes on ~2026-07-31, silently halting the chain
(append_block computes next id from len(index['blocks']), so an empty index would
restart at id 0 and overwrite block-0000). The block files themselves are intact.

This scans blocks/, reconstructs the index in the exact schema chain.py expects
({blocks:[{id,hash,timestamp,prompt}], head, created}), verifies hash-link
continuity (parent[i] == hash[i-1]), and writes index.json. Backs up any existing
index first. Idempotent + re-runnable.

Uses os.scandir (bash `ls` on this dir hangs on ~43.5k files).
"""

import os, json, re
from datetime import datetime, timezone
from pathlib import Path

CHAIN = Path("~/.claude/session-chain")
BLOCKS = CHAIN / "blocks"
INDEX = CHAIN / "index.json"
PAT = re.compile(r"block-(\d+)\.json$")


def main():
    # 1. Collect block ids via scandir (fast; no hang).
    ids = []
    with os.scandir(BLOCKS) as it:
        for e in it:
            m = PAT.search(e.name)
            if m:
                ids.append(int(m.group(1)))
    ids.sort()
    if not ids:
        print("No block files found -- nothing to rebuild.")
        return
    print(f"Found {len(ids)} blocks, ids {ids[0]}..{ids[-1]}")

    # 2. Read each block, build the index entries + verify the hash chain.
    #    CRITICAL invariant: chain.py computes the next block id as
    #    len(index['blocks']), so the list MUST be dense (entry[i].id == i) or the
    #    next finalize() collides with an existing block. Corrupted/unreadable
    #    blocks therefore get a PLACEHOLDER entry (hash recovered from raw bytes
    #    where possible) so no hole shortens the list.
    max_id = ids[-1]
    hash_re = re.compile(rb'"hash"\s*:\s*"([0-9a-f]+)"')
    parent_re = re.compile(rb'"parent"\s*:\s*"([0-9a-f]+)"')
    by_id = {}
    breaks = []
    created = None
    for i in ids:
        f = BLOCKS / f"block-{i:04d}.json"
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            ts = d.get("timestamp")
            if created is None and ts:
                created = ts
            by_id[i] = {
                "id": d.get("id", i),
                "hash": d.get("hash"),
                "parent": d.get("parent"),
                "timestamp": ts,
                "prompt": (d.get("prompt") or "")[:80],
            }
        except Exception as ex:
            # Recover hash/parent from raw bytes so the chain link survives even
            # though the JSON body is corrupt.
            raw = b""
            try:
                raw = f.read_bytes()
            except Exception:
                pass
            hm = hash_re.search(raw)
            pm = parent_re.search(raw)
            breaks.append((i, f"unreadable: {type(ex).__name__} (placeholder; hash {'recovered' if hm else 'LOST'})"))
            by_id[i] = {
                "id": i,
                "hash": hm.group(1).decode() if hm else None,
                "parent": pm.group(1).decode() if pm else None,
                "timestamp": None,
                "prompt": "[corrupt block - placeholder to keep index dense]",
            }

    # Emit a DENSE list over 0..max_id; verify parent==prev hash in id order.
    blocks = []
    prev_hash = None
    for i in range(0, max_id + 1):
        e = by_id.get(i)
        if e is None:
            # id genuinely absent from disk (should not happen: contiguous) --
            # still emit a placeholder to preserve density.
            breaks.append((i, "missing file (placeholder)"))
            e = {"id": i, "hash": None, "parent": None, "timestamp": None,
                 "prompt": "[missing block - placeholder to keep index dense]"}
        if prev_hash is not None and e.get("parent") not in (prev_hash, None):
            breaks.append((i, f"parent {str(e.get('parent'))[:12]} != prev hash {str(prev_hash)[:12]}"))
        prev_hash = e.get("hash") if e.get("hash") is not None else prev_hash
        # index entry schema chain.py expects: {id, hash, timestamp, prompt}
        blocks.append({k: e[k] for k in ("id", "hash", "timestamp", "prompt")})

    head = blocks[-1]["hash"] if blocks else None
    print(f"Reconstructed {len(blocks)} index entries; head = {str(head)[:12]}")
    print(f"hash-link breaks: {len(breaks)}")
    for i, why in breaks[:10]:
        print(f"  block {i}: {why}")
    if len(breaks) > 10:
        print(f"  ... +{len(breaks)-10} more")

    # 3. Back up any existing index (the 0-byte corpse) then write.
    if INDEX.exists():
        bak = CHAIN / f"index.json.corrupt-bak"
        try:
            bak.write_bytes(INDEX.read_bytes())
            print(f"Backed up existing index -> {bak.name} ({INDEX.stat().st_size} bytes)")
        except Exception as ex:
            print(f"Backup warning: {ex}")

    index = {
        "blocks": blocks,
        "head": head,
        "created": created or datetime.now(timezone.utc).isoformat(),
        "_rebuilt": datetime.now(timezone.utc).isoformat(),
        "_rebuilt_from": f"{len(blocks)} block files",
    }
    # Atomic write: tmp + strict-JSON verify + os.replace, so a crash mid-write can
    # never re-zero the very index this recovery tool exists to rebuild.
    _text = json.dumps(index, indent=2)
    _tmp = INDEX.with_suffix(".json.tmp")
    _tmp.write_text(_text, encoding="utf-8")
    json.loads(_tmp.read_text(encoding="utf-8"))  # verify well-formed before swap
    os.replace(_tmp, INDEX)
    size = INDEX.stat().st_size
    print(f"Wrote index.json ({size} bytes). Next append id = {len(blocks)} -> block-{len(blocks):04d}.json (no collision with tip {ids[-1]}).")
    if breaks:
        print("NOTE: hash-link breaks recorded above -- chain is usable but not fully continuous.")
    else:
        print("Hash-link continuity: CLEAN (every parent matches prior hash).")


if __name__ == "__main__":
    main()
