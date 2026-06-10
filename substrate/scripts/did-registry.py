#!/usr/bin/env python3
"""DID-based memory registry for Jarvis Mind Network.

Each memory gets a stable DID: did:jarvis:<type>:<sha256_8chars>
Registry maps DIDs -> file paths + metadata + cross-references.
Shards resolve DIDs instead of passing raw context -- infinite scaling.

Usage:
    python did-registry.py init          # Build registry from existing files
    python did-registry.py register <f>  # Register a single file
    python did-registry.py lookup <did>  # Resolve DID or alias to metadata
    python did-registry.py list [opts]   # List entries (--type, --tier, --tag)
    python did-registry.py verify [did]  # Check content integrity
    python did-registry.py refs <did>    # Show incoming + outgoing refs
    python did-registry.py graph         # Export reference graph (DOT)
    python did-registry.py search <q>    # Search titles, descriptions, tags
    python did-registry.py stats         # Registry statistics
    python did-registry.py orphans       # Files not in registry
    python did-registry.py dangling      # Broken DID references
    python did-registry.py export        # Export compact registry for TG bot shards
    python did-registry.py shapley       # Calculate Shapley values across memory graph
    python did-registry.py access <did>  # Record access (increment count + timestamp)
"""

import hashlib
import itertools
import json
import math
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ============ Constants ============

MEMORY_DIR = Path(__file__).resolve().parent.parent / "projects" / "C--Users-Will" / "memory"
REGISTRY_PATH = MEMORY_DIR / "registry.json"
HASH_TRUNCATION = 8
VALID_TYPES = {"project", "user", "feedback", "reference", "index", "system"}

# Default Shapley attribution field for each registry entry
DEFAULT_SHAPLEY = {
    "contributors": ["will", "jarvis"],
    "marginal_value": 0.0,
    "coalition_weight": 1.0,
    "last_accessed": None,
    "access_count": 0,
}

# Bot export path — TG shards read this
BOT_EXPORT_PATH = Path(__file__).resolve().parent.parent.parent / "vibeswap" / "jarvis-bot" / "data" / "did-registry.json"

STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "must", "and", "or",
    "but", "if", "then", "else", "when", "at", "by", "for", "with", "about",
    "into", "from", "up", "out", "on", "off", "over", "under", "to", "in",
    "of", "not", "no", "so", "too", "very", "just", "also", "than", "that",
    "this", "these", "those", "it", "its", "all", "each", "every", "both",
    "few", "more", "most", "other", "some", "such", "only", "own", "same",
}

# Type inference from filename patterns
REFERENCE_FILES = {
    "solidity-patterns", "testing-patterns", "defi-math", "frontend-patterns",
    "deployment-patterns", "contracts-catalogue", "build-recommendations",
}

FEEDBACK_PREFIX = "feedback_"

# ============ DID Generation ============


def generate_did(filename_stem: str, memory_type: str) -> str:
    raw = hashlib.sha256(filename_stem.encode("utf-8")).hexdigest()
    short = raw[:HASH_TRUNCATION]
    return f"did:jarvis:{memory_type}:{short}"


def compute_content_hash(filepath: Path) -> str:
    return "sha256:" + hashlib.sha256(filepath.read_bytes()).hexdigest()


# ============ Frontmatter ============


def parse_frontmatter(text: str) -> tuple:
    """Returns (metadata_dict or None, body_text)."""
    if not text.startswith("---"):
        return None, text
    end = text.find("---", 3)
    if end == -1:
        return None, text
    fm_text = text[3:end].strip()
    meta = {}
    current_key = None
    current_list = None
    for line in fm_text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("- ") and current_key and current_list is not None:
            current_list.append(stripped[2:].strip())
            continue
        if ":" in stripped:
            if current_key and current_list is not None:
                meta[current_key] = current_list
                current_list = None
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "":
                current_key = key
                current_list = []
            else:
                meta[key] = val
                current_key = key
                current_list = None
        elif stripped == "" and current_key and current_list is not None:
            meta[current_key] = current_list
            current_key = None
            current_list = None
    if current_key and current_list is not None:
        meta[current_key] = current_list
    body = text[end + 3:].strip()
    return meta, body


def inject_did_frontmatter(filepath: Path, did: str, name: str, desc: str, mtype: str, refs: list) -> None:
    text = filepath.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    refs_block = ""
    if refs:
        refs_lines = "\n".join(f"  - {r}" for r in refs)
        refs_block = f"\nrefs:\n{refs_lines}"

    if meta:
        # Has frontmatter — inject did at top
        if "did" in meta:
            return  # Already has DID
        # Rebuild frontmatter with did first
        new_fm = f"---\ndid: {did}\n"
        for k, v in meta.items():
            if isinstance(v, list):
                new_fm += f"{k}:\n"
                for item in v:
                    new_fm += f"  - {item}\n"
            else:
                new_fm += f"{k}: {v}\n"
        if refs and "refs" not in meta:
            new_fm += f"refs:\n"
            for r in refs:
                new_fm += f"  - {r}\n"
        new_fm += "---\n\n"
        filepath.write_text(new_fm + body, encoding="utf-8")
    else:
        # No frontmatter — create one
        new_fm = f"---\ndid: {did}\nname: {name}\ndescription: {desc}\ntype: {mtype}{refs_block}\n---\n\n"
        filepath.write_text(new_fm + text, encoding="utf-8")


# ============ Inference ============


def infer_type(filename: str, meta: dict | None) -> str:
    if meta and meta.get("type") in VALID_TYPES:
        return meta["type"]
    stem = Path(filename).stem
    if stem == "MEMORY":
        return "index"
    if stem.startswith(FEEDBACK_PREFIX.rstrip("_")) or stem.startswith("feedback"):
        return "feedback"
    if stem in REFERENCE_FILES:
        return "reference"
    return "project"


def infer_tier(filename_stem: str, memory_md: str) -> str:
    # Find which section of MEMORY.md references this file
    lines = memory_md.split("\n")
    current_tier = "COLD"
    for line in lines:
        if line.startswith("## [HOT]"):
            current_tier = "HOT"
        elif line.startswith("## [WARM]"):
            current_tier = "WARM"
        elif line.startswith("## [COLD]"):
            current_tier = "COLD"
        if filename_stem in line:
            return current_tier
    return "COLD"


def extract_title(meta: dict | None, body: str, filename: str) -> str:
    if meta and meta.get("name"):
        return meta["name"]
    for line in body.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return Path(filename).stem.replace("-", " ").replace("_", " ").title()


def extract_description(meta: dict | None, body: str) -> str:
    if meta and meta.get("description"):
        return meta["description"]
    for line in body.split("\n"):
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("-") and not line.startswith(">"):
            return line[:120]
    return ""


def extract_refs(body: str, registry_entries: dict) -> list:
    refs = set()
    for match in re.finditer(r"memory/([a-zA-Z0-9_.-]+\.md)", body):
        ref_file = match.group(1)
        for did, entry in registry_entries.items():
            if entry["filename"] == ref_file:
                refs.add(did)
    for match in re.finditer(r"did:jarvis:[a-z]+:[a-f0-9]{8,}", body):
        refs.add(match.group(0))
    return sorted(refs)


def generate_tags(filename_stem: str, title: str, description: str) -> list:
    words = set()
    for text in [filename_stem.replace("-", " ").replace("_", " "), title, description]:
        for word in re.findall(r"[a-zA-Z]{3,}", text.lower()):
            if word not in STOP_WORDS:
                words.add(word)
    return sorted(words)[:10]


# ============ Registry Operations ============


def load_registry() -> dict:
    if REGISTRY_PATH.exists():
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return {
        "version": 1,
        "method": "did:jarvis",
        "created": datetime.now(timezone.utc).isoformat(),
        "updated": datetime.now(timezone.utc).isoformat(),
        "hash_algorithm": "sha256",
        "hash_truncation": HASH_TRUNCATION,
        "entries": {},
        "aliases": {},
    }


def save_registry(reg: dict) -> None:
    reg["updated"] = datetime.now(timezone.utc).isoformat()
    tmp = REGISTRY_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(REGISTRY_PATH)


def register_file(filepath: Path, reg: dict, memory_md: str, update_frontmatter: bool = True) -> str:
    stem = filepath.stem
    text = filepath.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    mtype = infer_type(filepath.name, meta)
    did = generate_did(stem, mtype)

    # Collision check
    if did in reg["entries"] and reg["entries"][did]["filename"] != filepath.name:
        did = f"did:jarvis:{mtype}:{hashlib.sha256(stem.encode()).hexdigest()[:10]}"

    title = extract_title(meta, body, filepath.name)
    desc = extract_description(meta, body)
    tags = generate_tags(stem, title, desc)
    tier = infer_tier(stem, memory_md)
    refs = extract_refs(body, reg["entries"])
    stat = filepath.stat()

    # Preserve existing Shapley data if re-registering
    existing_shapley = None
    if did in reg["entries"] and "shapley" in reg["entries"][did]:
        existing_shapley = reg["entries"][did]["shapley"]

    reg["entries"][did] = {
        "title": title,
        "filename": filepath.name,
        "path": f"memory/{filepath.name}",
        "type": mtype,
        "tier": tier,
        "created": datetime.fromtimestamp(stat.st_ctime, tz=timezone.utc).isoformat(),
        "modified": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
        "content_hash": compute_content_hash(filepath),
        "size_bytes": stat.st_size,
        "tags": tags,
        "refs": refs,
        "description": desc[:200],
        "shapley": existing_shapley if existing_shapley else dict(DEFAULT_SHAPLEY),
    }

    # Alias = filename stem
    alias = stem.replace("_", "-").lower()
    reg["aliases"][alias] = did

    if update_frontmatter and filepath.name != "MEMORY.md":
        inject_did_frontmatter(filepath, did, title, desc, mtype, refs)

    return did


# ============ Commands ============


def cmd_init():
    reg = load_registry()
    memory_md = (MEMORY_DIR / "MEMORY.md").read_text(encoding="utf-8") if (MEMORY_DIR / "MEMORY.md").exists() else ""

    files = sorted(MEMORY_DIR.glob("*.md"))
    count = 0
    for f in files:
        if f.name == "registry.json":
            continue
        did = register_file(f, reg, memory_md, update_frontmatter=False)
        count += 1
        print(f"  {did} <- {f.name}")

    # Second pass: resolve cross-refs now that all entries exist
    for f in files:
        if f.name == "registry.json":
            continue
        text = f.read_text(encoding="utf-8")
        _, body = parse_frontmatter(text)
        stem = f.stem
        mtype = infer_type(f.name, parse_frontmatter(text)[0])
        did = generate_did(stem, mtype)
        if did in reg["entries"]:
            reg["entries"][did]["refs"] = extract_refs(body, reg["entries"])

    save_registry(reg)
    print(f"\nRegistered {count} memories. Registry: {REGISTRY_PATH}")
    print(f"Total entries: {len(reg['entries'])}, aliases: {len(reg['aliases'])}")


def cmd_register(filepath_str: str):
    filepath = Path(filepath_str).resolve()
    if not filepath.exists():
        filepath = MEMORY_DIR / filepath_str
    if not filepath.exists():
        print(f"File not found: {filepath_str}")
        sys.exit(1)
    reg = load_registry()
    memory_md = (MEMORY_DIR / "MEMORY.md").read_text(encoding="utf-8") if (MEMORY_DIR / "MEMORY.md").exists() else ""
    did = register_file(filepath, reg, memory_md)
    save_registry(reg)
    print(f"Registered: {did} <- {filepath.name}")


def cmd_lookup(query: str):
    reg = load_registry()
    did = query
    if not query.startswith("did:"):
        did = reg["aliases"].get(query.lower().replace("_", "-"), None)
        if not did:
            # Fuzzy search aliases
            matches = [a for a in reg["aliases"] if query.lower() in a]
            if matches:
                did = reg["aliases"][matches[0]]
                print(f"(matched alias: {matches[0]})")
            else:
                print(f"Not found: {query}")
                return
    entry = reg["entries"].get(did)
    if not entry:
        print(f"DID not in registry: {did}")
        return
    print(f"DID:         {did}")
    print(f"Title:       {entry['title']}")
    print(f"File:        {entry['path']}")
    print(f"Type:        {entry['type']}")
    print(f"Tier:        {entry['tier']}")
    print(f"Tags:        {', '.join(entry['tags'])}")
    print(f"Size:        {entry['size_bytes']} bytes")
    print(f"Description: {entry['description']}")
    shapley = entry.get("shapley", {})
    if shapley:
        print(f"Contributors:{', '.join(shapley.get('contributors', []))}")
        print(f"Access count:{shapley.get('access_count', 0)}")
        print(f"Last access: {shapley.get('last_accessed', 'never')}")
        print(f"Marginal val:{shapley.get('marginal_value', 0.0):.2f}")
        print(f"Coalition wt:{shapley.get('coalition_weight', 1.0):.2f}")
    if entry["refs"]:
        print(f"Refs out:    {len(entry['refs'])}")
        for r in entry["refs"]:
            ref_entry = reg["entries"].get(r, {})
            print(f"  -> {r} ({ref_entry.get('title', '?')})")


def cmd_list(args: list):
    reg = load_registry()
    type_filter = tier_filter = tag_filter = None
    i = 0
    while i < len(args):
        if args[i] == "--type" and i + 1 < len(args):
            type_filter = args[i + 1]
            i += 2
        elif args[i] == "--tier" and i + 1 < len(args):
            tier_filter = args[i + 1].upper()
            i += 2
        elif args[i] == "--tag" and i + 1 < len(args):
            tag_filter = args[i + 1].lower()
            i += 2
        else:
            i += 1

    for did, entry in sorted(reg["entries"].items(), key=lambda x: x[1]["tier"]):
        if type_filter and entry["type"] != type_filter:
            continue
        if tier_filter and entry["tier"] != tier_filter:
            continue
        if tag_filter and tag_filter not in entry["tags"]:
            continue
        print(f"[{entry['tier']:4}] {did}  {entry['title'][:50]}")


def cmd_verify(target: str | None):
    reg = load_registry()
    entries = reg["entries"]
    if target and target.startswith("did:"):
        entries = {target: entries[target]} if target in entries else {}

    ok = fail = missing = 0
    for did, entry in entries.items():
        fpath = MEMORY_DIR / entry["filename"]
        if not fpath.exists():
            print(f"MISSING  {did} -> {entry['filename']}")
            missing += 1
            continue
        current = compute_content_hash(fpath)
        if current == entry["content_hash"]:
            ok += 1
        else:
            print(f"CHANGED  {did} -> {entry['filename']}")
            entry["content_hash"] = current
            fail += 1

    if fail:
        save_registry(reg)
    print(f"\nVerified: {ok} ok, {fail} changed, {missing} missing")


def cmd_refs(did: str):
    reg = load_registry()
    if did not in reg["entries"]:
        # Try alias
        did = reg["aliases"].get(did.lower().replace("_", "-"), did)
    entry = reg["entries"].get(did)
    if not entry:
        print(f"Not found: {did}")
        return

    print(f"=== {entry['title']} ({did}) ===\n")
    print("Outgoing refs:")
    for r in entry.get("refs", []):
        re_entry = reg["entries"].get(r, {})
        print(f"  -> {r} ({re_entry.get('title', '?')})")

    print("\nIncoming refs:")
    for other_did, other_entry in reg["entries"].items():
        if did in other_entry.get("refs", []):
            print(f"  <- {other_did} ({other_entry['title']})")


def cmd_graph():
    reg = load_registry()
    print("digraph jarvis_memory {")
    print('  rankdir=LR;')
    print('  node [shape=box, style=filled];')
    colors = {"HOT": "#ff6b6b", "WARM": "#ffd93d", "COLD": "#6bcbff"}
    for did, entry in reg["entries"].items():
        label = entry["title"][:30].replace('"', '\\"')
        color = colors.get(entry["tier"], "#cccccc")
        print(f'  "{did}" [label="{label}", fillcolor="{color}"];')
    for did, entry in reg["entries"].items():
        for ref in entry.get("refs", []):
            if ref in reg["entries"]:
                print(f'  "{did}" -> "{ref}";')
    print("}")


def cmd_search(query: str):
    reg = load_registry()
    q = query.lower()
    results = []
    for did, entry in reg["entries"].items():
        score = 0
        if q in entry["title"].lower():
            score += 3
        if q in entry["description"].lower():
            score += 2
        if q in entry["tags"]:
            score += 2
        if q in entry["filename"].lower():
            score += 1
        if q in did:
            score += 5
        if score > 0:
            results.append((score, did, entry))
    results.sort(key=lambda x: -x[0])
    for score, did, entry in results[:10]:
        print(f"[{score}] {did}  {entry['title'][:60]}")


def cmd_stats():
    reg = load_registry()
    entries = reg["entries"]
    types = {}
    tiers = {}
    total_refs = 0
    total_size = 0
    for entry in entries.values():
        types[entry["type"]] = types.get(entry["type"], 0) + 1
        tiers[entry["tier"]] = tiers.get(entry["tier"], 0) + 1
        total_refs += len(entry.get("refs", []))
        total_size += entry.get("size_bytes", 0)

    # Shapley stats
    total_accesses = 0
    all_contributors = set()
    for entry in entries.values():
        shapley = entry.get("shapley", {})
        total_accesses += shapley.get("access_count", 0)
        for c in shapley.get("contributors", []):
            all_contributors.add(c)

    print(f"Registry v{reg['version']} | {len(entries)} memories | {len(reg['aliases'])} aliases")
    print(f"Total size: {total_size:,} bytes | {total_refs} cross-references")
    print(f"Total accesses: {total_accesses} | Contributors: {', '.join(sorted(all_contributors)) or 'none'}")
    print(f"\nBy type:  {', '.join(f'{k}: {v}' for k, v in sorted(types.items()))}")
    print(f"By tier:  {', '.join(f'{k}: {v}' for k, v in sorted(tiers.items()))}")


def cmd_orphans():
    reg = load_registry()
    registered = {e["filename"] for e in reg["entries"].values()}
    for f in sorted(MEMORY_DIR.glob("*.md")):
        if f.name not in registered and f.name != "registry.json":
            print(f"ORPHAN  {f.name}")


def cmd_dangling():
    reg = load_registry()
    for did, entry in reg["entries"].items():
        for ref in entry.get("refs", []):
            if ref not in reg["entries"]:
                print(f"DANGLING  {did} -> {ref}")


def cmd_export():
    """Export compact registry for TG bot shards."""
    reg = load_registry()
    compact = {
        "version": reg["version"],
        "method": reg["method"],
        "updated": reg["updated"],
        "entries": {},
        "aliases": reg["aliases"],
    }
    for did, entry in reg["entries"].items():
        compact["entries"][did] = {
            "title": entry["title"],
            "type": entry["type"],
            "tier": entry["tier"],
            "tags": entry["tags"],
            "refs": entry.get("refs", []),
            "description": entry["description"][:100],
        }
    BOT_EXPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    BOT_EXPORT_PATH.write_text(json.dumps(compact, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Exported {len(compact['entries'])} entries to {BOT_EXPORT_PATH}")
    print(f"Size: {BOT_EXPORT_PATH.stat().st_size:,} bytes")


# ============ Shapley Attribution ============


def _compute_incoming_refs(entries: dict) -> dict:
    """Build map of did -> count of other entries that reference it."""
    incoming = {did: 0 for did in entries}
    for did, entry in entries.items():
        for ref in entry.get("refs", []):
            if ref in incoming:
                incoming[ref] += 1
    return incoming


def _memory_value(entry: dict, incoming_count: int) -> float:
    """A memory's value = access_count * (1 + number of incoming refs).

    Memories that are never accessed have zero value.
    Memories referenced by many others are amplified.
    """
    access_count = entry.get("shapley", {}).get("access_count", 0)
    return access_count * (1 + incoming_count)


def _shapley_values(entries: dict) -> dict:
    """Calculate Shapley values across the memory graph.

    For each contributor, their Shapley value is the sum of their
    marginal contributions across all memories they contributed to.

    Marginal contribution for a memory = memory_value / |contributors|
    weighted by coalition_weight. This is the symmetric Shapley
    allocation (equal split when all contributors are symmetric).

    For the full combinatorial Shapley (2^N coalitions), we use the
    formula: phi_i = sum over S not containing i of
      |S|!(n-|S|-1)!/n! * [v(S union {i}) - v(S)]

    With the simplifying assumption that a memory's value only exists
    when ALL its listed contributors are in the coalition (joint
    production), this reduces to: phi_i = v(N) / n for each memory.
    """
    incoming = _compute_incoming_refs(entries)
    contributor_values: dict[str, float] = {}

    for did, entry in entries.items():
        shapley = entry.get("shapley", {})
        contributors = shapley.get("contributors", ["will", "jarvis"])
        coalition_weight = shapley.get("coalition_weight", 1.0)
        value = _memory_value(entry, incoming.get(did, 0)) * coalition_weight

        if not contributors or value == 0:
            continue

        # Shapley equal split for joint production
        share = value / len(contributors)
        for contributor in contributors:
            contributor_values[contributor] = contributor_values.get(contributor, 0.0) + share

        # Store marginal value back on the entry
        entry["shapley"]["marginal_value"] = value

    return contributor_values


def cmd_shapley():
    """Calculate and display Shapley values across the memory graph."""
    reg = load_registry()
    entries = reg["entries"]

    if not entries:
        print("Registry is empty. Run 'init' first.")
        return

    # Ensure all entries have shapley fields
    for did, entry in entries.items():
        if "shapley" not in entry:
            entry["shapley"] = dict(DEFAULT_SHAPLEY)

    contributor_values = _shapley_values(entries)
    incoming = _compute_incoming_refs(entries)

    # Save updated marginal values
    save_registry(reg)

    # Summary stats
    total_value = sum(contributor_values.values())
    total_accesses = sum(
        e.get("shapley", {}).get("access_count", 0) for e in entries.values()
    )

    print("=" * 60)
    print("  SHAPLEY VALUE ATTRIBUTION — Jarvis Memory Graph")
    print("=" * 60)
    print(f"\n  Total memories:  {len(entries)}")
    print(f"  Total accesses:  {total_accesses}")
    print(f"  Total value:     {total_value:.2f}")
    print()

    # Ranked contributor table
    ranked = sorted(contributor_values.items(), key=lambda x: -x[1])
    print(f"  {'Contributor':<20} {'Shapley Value':>14} {'Share':>8}")
    print(f"  {'-' * 20} {'-' * 14} {'-' * 8}")
    for contributor, value in ranked:
        pct = (value / total_value * 100) if total_value > 0 else 0
        print(f"  {contributor:<20} {value:>14.2f} {pct:>7.1f}%")

    # Top accessed memories
    print(f"\n  {'Top Accessed Memories':<50}")
    print(f"  {'-' * 50}")
    by_access = sorted(
        entries.items(),
        key=lambda x: x[1].get("shapley", {}).get("access_count", 0),
        reverse=True,
    )
    for did, entry in by_access[:10]:
        shapley = entry.get("shapley", {})
        ac = shapley.get("access_count", 0)
        inc = incoming.get(did, 0)
        mv = shapley.get("marginal_value", 0)
        if ac == 0:
            continue
        title = entry["title"][:35]
        print(f"  {title:<35} acc={ac:<4} refs={inc:<3} val={mv:.1f}")

    print()


def cmd_access(did_or_alias: str):
    """Record an access event for a DID — increments count + timestamp."""
    reg = load_registry()

    # Resolve alias to DID
    did = did_or_alias
    if not did_or_alias.startswith("did:"):
        did = reg["aliases"].get(did_or_alias.lower().replace("_", "-"), None)
        if not did:
            # Fuzzy match
            matches = [a for a in reg["aliases"] if did_or_alias.lower() in a]
            if matches:
                did = reg["aliases"][matches[0]]
                print(f"(matched alias: {matches[0]})")
            else:
                print(f"Not found: {did_or_alias}")
                sys.exit(1)

    entry = reg["entries"].get(did)
    if not entry:
        print(f"DID not in registry: {did}")
        sys.exit(1)

    # Ensure shapley field exists
    if "shapley" not in entry:
        entry["shapley"] = dict(DEFAULT_SHAPLEY)

    entry["shapley"]["access_count"] += 1
    entry["shapley"]["last_accessed"] = datetime.now(timezone.utc).isoformat()

    save_registry(reg)

    ac = entry["shapley"]["access_count"]
    print(f"Accessed: {did}")
    print(f"  Title:        {entry['title']}")
    print(f"  Access count: {ac}")
    print(f"  Last access:  {entry['shapley']['last_accessed']}")


# ============ Main ============


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "init":
        cmd_init()
    elif cmd == "register":
        if len(sys.argv) < 3:
            print("Usage: did-registry.py register <file>")
            sys.exit(1)
        cmd_register(sys.argv[2])
    elif cmd == "lookup":
        if len(sys.argv) < 3:
            print("Usage: did-registry.py lookup <did|alias>")
            sys.exit(1)
        cmd_lookup(sys.argv[2])
    elif cmd == "list":
        cmd_list(sys.argv[2:])
    elif cmd == "verify":
        cmd_verify(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "refs":
        if len(sys.argv) < 3:
            print("Usage: did-registry.py refs <did>")
            sys.exit(1)
        cmd_refs(sys.argv[2])
    elif cmd == "graph":
        cmd_graph()
    elif cmd == "search":
        cmd_search(" ".join(sys.argv[2:]))
    elif cmd == "stats":
        cmd_stats()
    elif cmd == "orphans":
        cmd_orphans()
    elif cmd == "dangling":
        cmd_dangling()
    elif cmd == "export":
        cmd_export()
    elif cmd == "shapley":
        cmd_shapley()
    elif cmd == "access":
        if len(sys.argv) < 3:
            print("Usage: did-registry.py access <did|alias>")
            sys.exit(1)
        cmd_access(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
