#!/usr/bin/env python3
"""Handoff chain: the coarse, human-walkable layer over the fine block chain.

Will (2026-08-12): "each handoff should be chained to the past one ... the
chain's strength isn't 'all memory at once', it is that you can walk back the
chain ... that way you're connected to every bit of your past ... we need auto
backup ... at least 2 nodes ... can your protocols/primitives be baked into it?"

Each handoff becomes a BLOCK linked to its predecessor by hash (like the fine
`blocks/block-*.json` chain, but at session granularity so a human can walk it).

Block record (stored in handoff-chain/chain.jsonl, append-only):
  seq        : monotonic index (0 = genesis)
  ts         : iso timestamp (passed in; wall-clock not read here)
  file       : handoff filename (copied into the repo, durable)
  hash       : sha256 of the handoff bytes
  prev       : predecessor filename (None at genesis)   <- the LINK
  prev_hash  : predecessor hash (None at genesis)        <- tamper-evident link
  fine_head  : hash of the newest fine-chain block at seal time (anchor to detail)
  self_root  : fingerprint of the identity layer (which "me" wrote it)

The handoff file is COPIED into handoff-chain/handoffs/ (the git-backed repo) and
stamped in-place with a <!-- CHAIN ... --> header, so the durable copy is
self-describing and the Desktop drop-zone stays a working area.

Idempotent: re-sealing the same newest handoff is a no-op (dedupe by hash).

This module is import-safe and CLI-testable:
  python handoff-chain.py --seal --ts <iso>     # seal the newest handoff
  python handoff-chain.py --status              # print HEAD + walk-back preview
  python handoff-chain.py --walk                # print the full chain, newest->genesis
"""
import glob
import hashlib
import json
import os
import shutil
import sys

HOME = os.path.expanduser("~")
CHAIN_DIR = os.path.join(HOME, ".claude", "session-chain", "handoff-chain")
HANDOFFS_DIR = os.path.join(CHAIN_DIR, "handoffs")
CHAIN_LOG = os.path.join(CHAIN_DIR, "chain.jsonl")
HEAD_PTR = os.path.join(CHAIN_DIR, "HEAD.json")
MEMORY_DIR = os.path.join(HOME, ".claude", "projects", "C--Users-Will", "memory")
FINE_BLOCKS = os.path.join(HOME, ".claude", "session-chain", "blocks")

HANDOFF_GLOBS = [
    os.path.join(HOME, "Desktop", "SESSION-HANDOFF-*.md"),
    os.path.join(HOME, "Desktop", "Session-Handoffs", "SESSION-HANDOFF-*.md"),
]
STAMP_START = "<!-- CHAIN"
STAMP_END = "-->"


def _sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def _sha256_file(path):
    with open(path, "rb") as f:
        return _sha256_bytes(f.read())


def newest_handoff():
    cands = []
    for g in HANDOFF_GLOBS:
        cands.extend(glob.glob(g))
    if not cands:
        return None
    return max(cands, key=lambda p: os.path.getmtime(p))


def fine_chain_head():
    """Hash of the newest fine-grained block -- the anchor into turn-level detail."""
    try:
        blocks = glob.glob(os.path.join(FINE_BLOCKS, "block-*.json"))
        if not blocks:
            return None
        newest = max(blocks, key=lambda p: os.path.getmtime(p))
        with open(newest, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f).get("hash")
    except Exception:
        return None


def self_root():
    """Fingerprint of the identity layer: which version of the primitives/protocols
    corpus produced this block. Deterministic digest over memory file names + sizes.
    Baking the protocols into the chain (Will's ask) = every block records its self."""
    try:
        names = sorted(
            f for f in os.listdir(MEMORY_DIR) if f.endswith(".md")
        )
        h = hashlib.sha256()
        for n in names:
            p = os.path.join(MEMORY_DIR, n)
            h.update(n.encode())
            h.update(str(os.path.getsize(p)).encode())
        return h.hexdigest()[:16]
    except Exception:
        return None


def read_head():
    try:
        with open(HEAD_PTR, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None  # genesis state


def read_chain():
    out = []
    try:
        with open(CHAIN_LOG, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    out.append(json.loads(line))
    except FileNotFoundError:
        pass
    return out


def _strip_existing_stamp(text):
    if text.startswith(STAMP_START):
        end = text.find(STAMP_END)
        if end != -1:
            return text[end + len(STAMP_END):].lstrip("\n")
    return text


def _stamp_header(block):
    return (
        f"{STAMP_START}\n"
        f"  seq:        {block['seq']}\n"
        f"  ts:         {block['ts']}\n"
        f"  file:       {block['file']}\n"
        f"  hash:       {block['hash']}\n"
        f"  prev:       {block['prev']}\n"
        f"  prev_hash:  {block['prev_hash']}\n"
        f"  fine_head:  {block['fine_head']}\n"
        f"  self_root:  {block['self_root']}\n"
        f"{STAMP_END}\n\n"
    )


import re as _re


def _filename_date(path):
    """Sort key: the YYYY-MM-DD in the handoff filename (chronological genesis).
    Falls back to mtime-derived ordering only if no date is present."""
    m = _re.search(r"(\d{4})-(\d{2})-(\d{2})", os.path.basename(path))
    if m:
        return m.group(0)
    return "0000-00-00"


def all_handoffs_chrono():
    """Every handoff, oldest -> newest by filename date (mtime as tiebreak).
    De-dupes by basename (same handoff can exist in Desktop + Session-Handoffs/)."""
    seen, uniq = {}, []
    cands = []
    for g in HANDOFF_GLOBS:
        cands.extend(glob.glob(g))
    for p in cands:
        b = os.path.basename(p)
        # prefer the copy in Session-Handoffs/ (the archive) if duplicated
        if b not in seen or "Session-Handoffs" in p:
            seen[b] = p
    uniq = list(seen.values())
    uniq.sort(key=lambda p: (_filename_date(p), os.path.getmtime(p)))
    return uniq


def reset_chain():
    """Wipe chain state (log, HEAD, durable copies) for a clean rebuild."""
    for p in (CHAIN_LOG, HEAD_PTR):
        try:
            os.remove(p)
        except FileNotFoundError:
            pass
    if os.path.isdir(HANDOFFS_DIR):
        for f in glob.glob(os.path.join(HANDOFFS_DIR, "*.md")):
            os.remove(f)


def backfill(ts):
    """Rebuild the chain from scratch, sealing every handoff oldest->newest so
    seq 0 = the earliest handoff (genesis) and HEAD = the latest. Idempotent by
    virtue of reset+replay."""
    reset_chain()
    n = 0
    for src in all_handoffs_chrono():
        status, _ = _seal_path(src, ts)
        if status == "sealed":
            n += 1
    return n


SEAL_LOCK = os.path.join(CHAIN_DIR, ".seal.lock")


def _acquire_seal_lock(timeout=10.0, stale=60.0):
    """Cross-process lock so two simultaneous session-Stops can't interleave the
    read-head -> append -> advance-HEAD critical section (which would fork the chain
    / duplicate a seq). O_CREAT|O_EXCL is the atomic primitive; a lock older than
    `stale` seconds is treated as crashed and reclaimed. Returns True on acquire.
    Deterministic-safe: uses os.stat mtime, not a forbidden clock call, for staleness
    and busy-waits a bounded number of short sleeps."""
    import time
    os.makedirs(CHAIN_DIR, exist_ok=True)
    deadline = time.time() + timeout
    while True:
        try:
            fd = os.open(SEAL_LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            return True
        except FileExistsError:
            # reclaim a crashed lock
            try:
                age = time.time() - os.path.getmtime(SEAL_LOCK)
                if age > stale:
                    os.remove(SEAL_LOCK)
                    continue
            except FileNotFoundError:
                continue
            if time.time() >= deadline:
                raise TimeoutError("seal lock busy")
            time.sleep(0.1)


def _release_seal_lock():
    try:
        os.remove(SEAL_LOCK)
    except FileNotFoundError:
        pass


def _seal_path(src, ts):
    """Seal a SPECIFIC handoff file as the next block. Idempotent (dedupe by hash
    vs current HEAD). Serialized by a cross-process lock so concurrent Stops cannot
    fork the chain. Returns (status, block_or_reason)."""
    if not src or not os.path.exists(src):
        return "empty", "handoff path missing"

    os.makedirs(HANDOFFS_DIR, exist_ok=True)
    src_hash = _sha256_file(src)
    fname = os.path.basename(src)

    _acquire_seal_lock()
    try:
        head = read_head()
        if head and head.get("hash") == src_hash:
            return "noop", f"already sealed (seq {head.get('seq')}, hash {src_hash[:12]})"

        seq = 0 if not head else head.get("seq", -1) + 1
        prev = None if not head else head.get("file")
        prev_hash = None if not head else head.get("hash")

        block = {
            "seq": seq,
            "ts": ts,
            "file": fname,
            "hash": src_hash,
            "prev": prev,
            "prev_hash": prev_hash,
            "fine_head": fine_chain_head(),
            "self_root": self_root(),
        }

        # copy into the durable repo dir, stamped with the chain header
        with open(src, "r", encoding="utf-8", errors="replace") as f:
            body = _strip_existing_stamp(f.read())
        stamped = _stamp_header(block) + body
        dst = os.path.join(HANDOFFS_DIR, fname)
        tmp = dst + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(stamped)
        os.replace(tmp, dst)

        # append to the chain log (single write, under lock)
        with open(CHAIN_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(block) + "\n")

        # advance HEAD atomically
        htmp = HEAD_PTR + ".tmp"
        with open(htmp, "w", encoding="utf-8") as f:
            json.dump(block, f, indent=2)
        os.replace(htmp, HEAD_PTR)

        return "sealed", block
    finally:
        _release_seal_lock()


def seal(ts):
    """Seal the newest handoff as the next block (the live session-end path)."""
    return _seal_path(newest_handoff(), ts)


def walk():
    """Return the chain newest -> genesis by following prev_hash. Verifies links."""
    chain = {b["hash"]: b for b in read_chain()}
    head = read_head()
    if not head:
        return []
    ordered = []
    cur = head
    seen = set()
    while cur is not None:
        ordered.append(cur)
        ph = cur.get("prev_hash")
        if ph is None or ph in seen:
            break
        seen.add(cur["hash"])
        cur = chain.get(ph)  # None => broken link, loop ends (detectable gap)
    return ordered


def _cli():
    ts = "1970-01-01T00:00:00+00:00"
    if "--ts" in sys.argv:
        ts = sys.argv[sys.argv.index("--ts") + 1]
    if "--backfill" in sys.argv:
        n = backfill(ts)
        print(f"[backfill] sealed {n} handoff(s) oldest->newest")
        return 0
    if "--seal" in sys.argv:
        status, res = seal(ts)
        print(f"[{status}] {res if isinstance(res, str) else json.dumps(res, indent=2)}")
        return 0
    if "--walk" in sys.argv:
        chain = walk()
        print(f"chain length: {len(chain)} (newest -> genesis)")
        for b in chain:
            link = "GENESIS" if b["prev"] is None else f"prev={b['prev']}"
            print(f"  seq {b['seq']:>4}  {b['file']}  [{link}]")
        return 0
    # default: status
    head = read_head()
    n = len(read_chain())
    if not head:
        print("chain: EMPTY (no blocks sealed yet)")
    else:
        print(f"chain: {n} block(s). HEAD seq {head['seq']} = {head['file']}")
        print(f"       hash {head['hash'][:16]}  fine_head {head.get('fine_head')}  self_root {head.get('self_root')}")
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
