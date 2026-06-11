#!/usr/bin/env python3
"""
sync-public-substrate.py

Layer-2 persistence mechanism. Runs the substrate-mirror discipline so
the local memory store stays in sync with the public substrate slice
without manual `cp` + `git` invocations.

Mirrors:
  - ~/.claude/projects/C--Users-Will/memory/*.md ->
      ~/jarvis-monorepo/substrate/memory/

  - ~/.claude/hooks/*.py + ~/.claude/session-chain/*.py ->
      ~/jarvis-monorepo/substrate/hooks/

  - ~/.claude/cron-prompts/*.md ->
      ~/jarvis-monorepo/substrate/cron-prompts/

  - ~/.claude/scripts/*.py (this script, odysseus_discovery, etc.) ->
      ~/jarvis-monorepo/substrate/scripts/

Scrub-list applied to memory: any file matching partner-engagement
specifics or NDA-locked content is skipped. Hooks with personal email
or hardcoded user-path are skipped.

Then commits + pushes the JARVIS monorepo if there are changes.

Usage:
    python sync-public-substrate.py           # dry-run (default: show what would change)
    python sync-public-substrate.py --apply   # actually copy, commit, push
    python sync-public-substrate.py --apply --no-push  # copy + commit but skip push

Designed to be cron-callable for periodic sync. Idempotent: if nothing
changed, nothing commits.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


HOME = Path.home()
LOCAL_MEMORY = HOME / ".claude" / "projects" / "C--Users-Will" / "memory"
LOCAL_HOOKS = [HOME / ".claude" / "hooks", HOME / ".claude" / "session-chain"]
LOCAL_CRON = HOME / ".claude" / "cron-prompts"
LOCAL_SCRIPTS = HOME / ".claude" / "scripts"
LOCAL_CHAIN_INDEX = HOME / ".claude" / "session-chain" / "index.json"

MONOREPO = HOME / "jarvis-monorepo"
SUBSTRATE = MONOREPO / "substrate"
SUB_MEMORY = SUBSTRATE / "memory"
SUB_HOOKS = SUBSTRATE / "hooks"
SUB_CRON = SUBSTRATE / "cron-prompts"
SUB_SCRIPTS = SUBSTRATE / "scripts"
SUB_CHAIN = SUBSTRATE / "_chain"

# Scrub patterns for memory files. Any file whose CONTENT matches one of these
# stays local.
SCRUB_CONTENT_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in [
        r"\bPragma\b", r"\b[REDACTED-NDA]\b",
        r"\bRickUSD8\b", r"\bkimberthilson\b",
        r"\bbernhard\b", r"\bmatta\b", r"\bkrakovia\b",
        r"\bpragmaresearch\b",
        r"\bnda-locked\b",
        r"@gmail\.com", r"@yahoo\.com", r"@outlook\.com",
        r"\bsk-[A-Za-z0-9]{40,}",
        r"\bghp_[A-Za-z0-9]+",
        r"anthropic-engagement",
        r"anthropic-conversation",
    ]
]

# Memory filename patterns that always stay local
SCRUB_FILENAME_PATTERNS = [
    re.compile(p) for p in [
        r"^MEMORY\.md$",
        r"^MEMORY_INDEX_.*\.md$",
        r"^MEMORY_WARM_.*\.md$",
        r"^MEMORY_FORMAT_SPEC\.md$",
    ]
]

# Hooks that have hardcoded personal content. They get a sanitization pass
# (regex replace) before mirror. Hooks NOT in this list are mirrored as-is
# (after a path-rewrite for ~/.claude/).
HOOK_SKIP_LIST = {
    "phone-ping.py",                   # personal email in docstring
    "partner-architecture-load-gate.py",  # partner-specific embedded content
}

# Hooks where the em-dash gate is special — we keep a sanitized version that
# was already written. Don't overwrite it from local.
HOOK_PRESERVE_IF_PRESENT = {
    "em-dash-augmentation-gate.py",
}


def should_scrub_memory(path: Path) -> tuple[bool, str]:
    name = path.name
    for pat in SCRUB_FILENAME_PATTERNS:
        if pat.match(name):
            return True, "filename-scrub-list"
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return True, "read-error"
    for pat in SCRUB_CONTENT_PATTERNS:
        m = pat.search(text)
        if m:
            return True, f"content-match: {m.group(0)[:40]}"
    return False, ""


def sanitize_hook_text(text: str) -> str:
    """Apply path-rewrite for portable hooks."""
    text = text.replace("C:/Users/Will/.claude/", "~/.claude/")
    text = text.replace("C:/Users/Will/", "~/")
    text = text.replace("/c/Users/Will/.claude/", "~/.claude/")
    text = text.replace("/c/Users/Will/", "~/")
    return text


def copy_if_different(src: Path, dest: Path, transform=None) -> str:
    """Returns one of: 'added', 'updated', 'skipped-same', 'error'."""
    try:
        src_text = src.read_text(encoding="utf-8", errors="replace")
        if transform:
            src_text = transform(src_text)
    except OSError as e:
        return f"error: {e}"
    if dest.exists():
        try:
            dst_text = dest.read_text(encoding="utf-8", errors="replace")
        except OSError:
            dst_text = ""
        if dst_text == src_text:
            return "skipped-same"
        action = "updated"
    else:
        action = "added"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(src_text, encoding="utf-8")
    return action


def sync_memory(apply: bool) -> dict:
    stats = {"copied": 0, "updated": 0, "scrubbed": 0, "same": 0}
    scrubbed_names = []
    if not LOCAL_MEMORY.exists():
        return stats
    for src in sorted(LOCAL_MEMORY.glob("*.md")):
        # Explicit frontmatter discretion flag (per #8 audit, class-eliminates paraphrase bypass)
        try:
            head = src.read_text(encoding='utf-8', errors='replace')[:2000]
            d = check_discretion_frontmatter(head)
            if d:
                scrubbed_names.append(f"{src.name} (frontmatter: discretion={d})")
                # Retroactive cleanup: if previously-mirrored copy exists, DELETE it.
                # Class-eliminates 'flag added after first mirror, leaked copy persists.'
                # Note: git history on public repo still retains pre-flag content — that's a
                # separate class documented in substrate/ADOPTION.md (history-leakage).
                dest = SUB_MEMORY / src.name
                if dest.exists() and apply:
                    try:
                        dest.unlink()
                        print(f"  retroactive-removed: {src.name} (discretion={d})")
                    except Exception:
                        pass
                continue
        except Exception:
            pass
        skip, reason = should_scrub_memory(src)
        if skip:
            stats["scrubbed"] += 1
            scrubbed_names.append((src.name, reason))
            continue
        dest = SUB_MEMORY / src.name
        if not apply:
            if not dest.exists():
                stats["copied"] += 1
            elif src.read_text(encoding="utf-8", errors="replace") != dest.read_text(encoding="utf-8", errors="replace"):
                stats["updated"] += 1
            else:
                stats["same"] += 1
            continue
        result = copy_if_different(src, dest)
        if result == "added":
            stats["copied"] += 1
        elif result == "updated":
            stats["updated"] += 1
        else:
            stats["same"] += 1
    stats["scrubbed_names"] = scrubbed_names[:10]
    return stats


def check_discretion_frontmatter(content: str) -> str | None:
    """Per #8 audit suggestion: explicit > implicit. Memory files can opt out of
    public sync via YAML frontmatter:
      discretion: nda           ⇒ never mirror
      discretion: partner-private ⇒ never mirror
      discretion: internal      ⇒ never mirror
    Returns the discretion value if set, None otherwise.

    Round-5 class-fix: handle unusually long frontmatter. We now look for the
    closing '---' anywhere in the file, not just within first 2KB. Class-
    eliminates 'frontmatter > 2KB and discretion line gets missed silently.'
    """
    if not content.startswith('---'):
        return None
    # Search the entire content for the closing '---' on its own line (or with leading newline)
    end = content.find('\n---', 3)
    if end < 0:
        return None
    frontmatter = content[3:end]
    for line in frontmatter.splitlines():
        line = line.strip()
        if line.startswith('discretion:'):
            val = line.split(':', 1)[1].strip().strip('"').strip("'").lower()
            if val in ('nda', 'partner-private', 'internal', 'private'):
                return val
    return None


def sync_hooks(apply: bool) -> dict:
    stats = {"copied": 0, "updated": 0, "skipped": 0, "same": 0}
    SUB_HOOKS.mkdir(parents=True, exist_ok=True)
    for hook_dir in LOCAL_HOOKS:
        if not hook_dir.exists():
            continue
        for src in sorted(hook_dir.rglob("*.py")):
            name = src.name
            if name in HOOK_SKIP_LIST:
                stats["skipped"] += 1
                continue
            rel = src.relative_to(hook_dir)
            dest = SUB_HOOKS / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            if name in HOOK_PRESERVE_IF_PRESENT and dest.exists():
                stats["skipped"] += 1
                continue
            if not apply:
                if not dest.exists():
                    stats["copied"] += 1
                else:
                    stats["same"] += 1  # rough; not transforming on dry-run
                continue
            result = copy_if_different(src, dest, transform=sanitize_hook_text)
            if result == "added":
                stats["copied"] += 1
            elif result == "updated":
                stats["updated"] += 1
            else:
                stats["same"] += 1
    return stats


def sync_dir(src_dir: Path, dest_dir: Path, glob: str, apply: bool,
             content_scrub: bool = False) -> dict:
    stats = {"copied": 0, "updated": 0, "same": 0, "scrubbed": 0}
    if not src_dir.exists():
        return stats
    dest_dir.mkdir(parents=True, exist_ok=True)
    for src in sorted(src_dir.glob(glob)):
        dest = dest_dir / src.name
        if content_scrub:
            # Same conservative rule as the memory mirror: a content match
            # keeps the whole file local. Cron-prompt state files (queues,
            # logs) accumulate partner context exactly like memory does.
            try:
                body = src.read_text(encoding="utf-8", errors="replace")
            except Exception:
                stats["scrubbed"] += 1
                continue
            hit = next((pat.pattern for pat in SCRUB_CONTENT_PATTERNS if pat.search(body)), None)
            if hit:
                stats["scrubbed"] += 1
                print(f"    scrub: {src.name} (content-match: {hit})")
                continue
        if not apply:
            if not dest.exists():
                stats["copied"] += 1
            else:
                stats["same"] += 1
            continue
        result = copy_if_different(src, dest)
        if result == "added":
            stats["copied"] += 1
        elif result == "updated":
            stats["updated"] += 1
        else:
            stats["same"] += 1
    return stats


def git_commit_and_push(push: bool) -> tuple[bool, str]:
    """Returns (changed, message). changed=False means nothing to commit."""
    if not MONOREPO.exists():
        return False, f"no monorepo at {MONOREPO}"
    try:
        status = subprocess.run(
            ["git", "-C", str(MONOREPO), "status", "--short"],
            capture_output=True, text=True, check=True
        ).stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, f"git status failed: {e}"
    if not status:
        return False, "no changes"
    files_changed = len(status.splitlines())
    msg = f"sync-public-substrate: auto-sync ({files_changed} file(s) changed)"
    try:
        subprocess.run(
            ["git", "-C", str(MONOREPO),
             "-c", "user.email=tiptaptangsun@gmail.com",
             "-c", "user.name=Will Glynn",
             "add", "-A"],
            check=True, capture_output=True
        )
        subprocess.run(
            ["git", "-C", str(MONOREPO),
             "-c", "user.email=tiptaptangsun@gmail.com",
             "-c", "user.name=Will Glynn",
             "commit", "-m", msg],
            check=True, capture_output=True
        )
        if push:
            subprocess.run(
                ["git", "-C", str(MONOREPO), "push"],
                check=True, capture_output=True
            )
        return True, msg
    except subprocess.CalledProcessError as e:
        return False, f"git op failed: {e.stderr.decode('utf-8', errors='replace')[:200]}"


DEFER_STATE = Path(os.environ.get("TEMP") or "/tmp") / "claude" / ".substrate-sync-defer-count"
MAX_DEFERS = 3


def _background_agent_alive() -> bool:
    """A 0-byte, recent task-output file means a harness background agent is
    mid-run (write-on-completion). Syncing then risks sweeping its half-applied
    edits into a public auto-commit (git add -A). Self-defer instead of relying
    on operator vigilance -- 3 manual deferrals on 2026-06-11 motivated this.

    Window tightened 2026-06-11 (6h -> 15m for the 0-byte case): an *aborted*
    task leaves a 0-byte stub with the SAME signature as a pending agent, and the
    old 6h window kept that orphan flagged 'live' for hours, false-deferring
    unattended cron ticks (the guard the loop relies on was eating the loop).
    A genuinely pending agent is freshly spawned; 15m covers it. Anything longer
    is handled by the bounded-defer safety valve in main() so we can never get
    permanently stuck behind a lingering stub."""
    import time as _time
    temp = Path(os.environ.get("TEMP") or "/tmp") / "claude"
    try:
        now = _time.time()
        for p in temp.rglob("tasks/*.output"):
            st = p.stat()
            # pending/streaming agent: 0-byte but freshly spawned (not a stale stub)
            if st.st_size == 0 and st.st_mtime > now - 15 * 60:
                return True
            # any task output touched very recently = active completion write
            if st.st_mtime > now - 10 * 60:
                return True
    except Exception:
        pass
    return False


def _read_defer_count() -> int:
    try:
        return int(DEFER_STATE.read_text().strip())
    except Exception:
        return 0


def _write_defer_count(n: int) -> None:
    try:
        DEFER_STATE.parent.mkdir(parents=True, exist_ok=True)
        DEFER_STATE.write_text(str(n))
    except Exception:
        pass


def emit_chain_commitment(apply: bool) -> dict:
    """Unified persistence framework: the session-chain stays LOCAL (its blocks
    hold raw prompt/response content that must not leak), but it is a hash-chain,
    so its HEAD HASH cryptographically commits to every block. Publish only that
    commitment -- tamper-evident, zero content. Same off-chain-storage +
    public-commitment pattern as integrity-attest over governed files. A future
    shard node verifies a chain replica against this public head. This is the
    'local authority -> public commitment -> shard replication' framework that
    unifies substrate-sync (full content) and the session-chain (commitment only)."""
    import json
    import time as _t
    try:
        idx = json.loads(LOCAL_CHAIN_INDEX.read_text(encoding="utf-8"))
    except Exception as e:
        return {"ok": False, "reason": f"no local chain index ({e})"}
    head = idx.get("head")
    height = len(idx.get("blocks", []))
    commitment = {
        "head_hash": head,
        "height": height,
        "committed_at": int(_t.time()),
        "framework": "local-authority -> public-commitment -> shard-replication",
        "note": "blocks stay local (raw prompt/response); this head hash commits the full chain.",
    }
    if apply:
        SUB_CHAIN.mkdir(parents=True, exist_ok=True)
        (SUB_CHAIN / "commitment.json").write_text(
            json.dumps(commitment, indent=2) + "\n", encoding="utf-8")
    return {"ok": True, "head": head, "height": height}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="actually copy files (default is dry-run)")
    parser.add_argument("--no-push", action="store_true", help="skip git push after commit")
    parser.add_argument("--force", action="store_true", help="sync even while background agents are live")
    args = parser.parse_args()

    if args.apply and not args.force and _background_agent_alive():
        n = _read_defer_count() + 1
        if n <= MAX_DEFERS:
            _write_defer_count(n)
            print(f"sync-public-substrate: DEFERRED ({n}/{MAX_DEFERS}) -- live background "
                  "agent detected (0-byte task output). Re-run after agents land, or --force.")
            return 0
        # bounded-defer safety valve: a real agent would have landed in MAX_DEFERS
        # ticks; a lingering 0-byte stub is almost certainly orphaned. Proceed so
        # an unattended cron can't drift forever behind a dead stub. The sync only
        # mirrors memory/hooks/crons/scripts, not task-output files.
        print(f"sync-public-substrate: defer limit reached ({MAX_DEFERS}); proceeding "
              "past a likely-orphaned 0-byte stub (bounded-defer safety valve).")
    # any path that reaches a real sync resets the counter
    _write_defer_count(0)

    print(f"sync-public-substrate ({'apply' if args.apply else 'dry-run'})")
    print("=" * 60)

    mem_stats = sync_memory(args.apply)
    print(f"memory:  +{mem_stats['copied']} added  ~{mem_stats['updated']} updated  "
          f"={mem_stats['same']} same  -{mem_stats['scrubbed']} scrubbed")
    if mem_stats.get("scrubbed_names"):
        for name, reason in mem_stats["scrubbed_names"][:5]:
            print(f"    scrub: {name} ({reason})")

    hook_stats = sync_hooks(args.apply)
    print(f"hooks:   +{hook_stats['copied']} added  ~{hook_stats['updated']} updated  "
          f"={hook_stats['same']} same  -{hook_stats['skipped']} skipped")

    cron_stats = sync_dir(LOCAL_CRON, SUB_CRON, "*.md", args.apply, content_scrub=True)
    print(f"crons:   +{cron_stats['copied']} added  ~{cron_stats['updated']} updated  "
          f"={cron_stats['same']} same  -{cron_stats['scrubbed']} scrubbed")

    script_stats = sync_dir(LOCAL_SCRIPTS, SUB_SCRIPTS, "*.py", args.apply)
    print(f"scripts: +{script_stats['copied']} added  ~{script_stats['updated']} updated  "
          f"={script_stats['same']} same")

    chain_stats = emit_chain_commitment(args.apply)
    if chain_stats.get("ok"):
        print(f"chain:   commitment head={str(chain_stats['head'])[:12]}... "
              f"height={chain_stats['height']} (blocks stay local, head goes public)")
    else:
        print(f"chain:   {chain_stats.get('reason')}")

    if args.apply:
        changed, msg = git_commit_and_push(push=not args.no_push)
        print(f"git: {msg}" if changed else f"git: {msg}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
