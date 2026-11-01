#!/usr/bin/env python3
"""SessionStart witness: surface experience-chain health at boot.

So chain integrity is visible every window rather than discovered on failure.
Reports HEAD (seq/file), walk-link integrity (does prev_hash chain to genesis with
no gap?), and whether a remote backup is still pending. Fail-loud per
[[boot-hook-fail-loud]]: a missing HEAD or a broken link is shouted, not swallowed.

Cheap + deterministic: reads chain.jsonl + HEAD.json + the pending flag only. No
network, no MCP. Emits one concise additionalContext block (or nothing if silent
and healthy is not worth the boot budget -- but a broken chain always speaks).
"""
import json
import os
import sys

HOME = os.path.expanduser("~")
CHAIN = os.path.join(HOME, ".claude", "session-chain", "handoff-chain")
CHAINLOG = os.path.join(CHAIN, "chain.jsonl")
HEAD = os.path.join(CHAIN, "HEAD.json")
PENDING = os.path.join(CHAIN, ".backup-pending")


def check():
    if not os.path.exists(HEAD):
        return "loud", "[CHAIN-HEALTH] WARN: no HEAD.json -- experience chain not initialized or lost."
    try:
        head = json.load(open(HEAD, encoding="utf-8"))
        blocks = []
        with open(CHAINLOG, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    blocks.append(json.loads(line))
    except Exception as e:
        return "loud", f"[CHAIN-HEALTH] WARN: chain unreadable: {e}"

    by_hash = {b["hash"]: b for b in blocks}
    # walk from HEAD back via prev_hash; count hops, detect break
    cur, seen, hops = head, set(), 0
    broken = None
    while cur is not None:
        hops += 1
        ph = cur.get("prev_hash")
        if ph is None:
            break  # genesis
        if ph in seen or ph not in by_hash:
            broken = cur.get("file")
            break
        seen.add(cur["hash"])
        cur = by_hash.get(ph)

    n = len(blocks)
    pending = os.path.exists(PENDING)
    expected = head.get("seq", -1) + 1

    if broken:
        return "loud", (f"[CHAIN-HEALTH] WARN: broken link at {broken} "
                        f"(walked {hops}/{n}). prev_hash does not resolve -- investigate.")
    if hops != n or n != expected:
        return "loud", (f"[CHAIN-HEALTH] WARN: length mismatch (walk {hops}, log {n}, "
                        f"expected {expected}). Chain may have gaps.")

    msg = (f"[CHAIN-HEALTH] OK: {n} blocks, HEAD seq {head['seq']} "
           f"({head['file']}), walk-back clean to genesis.")
    if pending:
        return "loud", msg + " | BACKUP PENDING (sub-quorum last close; next backup retries)."
    return "quiet", msg


def main():
    hook_mode = not sys.stdin.isatty()
    if hook_mode:
        try:
            json.load(sys.stdin)
        except Exception:
            pass
    level, msg = check()
    # healthy-quiet still prints one short line (chain visibility is the point,
    # and it's a single line -- cheap); broken always prints.
    if hook_mode:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": msg,
            }
        }))
    else:
        print(f"[{level}] {msg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
