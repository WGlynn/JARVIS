#!/usr/bin/env python3
"""registry-drift-check.py -- Layer 1 self-checking invariant.

The gate registry (01-hooks/gate-registry.md) is only trustworthy while it stays
in sync with the live hook config (~/.claude/settings.json). A silently drifting
registry fakes confidence in the audit surface every layer above assumes holds
(the 1-to-all dependency: gates fire orthogonal to context, everything above
trusts that the enumerated set IS the live set).

This tool is read-only. It parses the hook scripts registered in settings.json
and the .py filenames named in gate-registry.md, then reports drift:
  - scripts registered in settings.json but not named in the registry
  - names in the registry not registered in settings.json

Note: some gates are named by FUNCTION in the registry on purpose (discretion:
a codename in a filename is an attack surface). Those show up here as
"registered but not named by filename", which is expected, not a defect -- the
report surfaces the delta for a human, it does not judge intent.

Exit code 0 always (report tool). Promote to a boot/CI gate later if wanted.
"""
import json
import os
import re
import sys

HOME = os.path.expanduser("~")
SETTINGS = os.path.join(HOME, ".claude", "settings.json")
HERE = os.path.dirname(os.path.abspath(__file__))
REGISTRY = os.path.join(HERE, "gate-registry.md")

PY = re.compile(r"([A-Za-z0-9_\-]+\.py)")


def registered_scripts(settings_path):
    with open(settings_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    scripts = set()
    for _event, groups in cfg.get("hooks", {}).items():
        for group in groups:
            for h in group.get("hooks", []):
                for m in PY.findall(h.get("command", "")):
                    scripts.add(os.path.basename(m))
    return scripts


def registry_scripts(registry_path):
    with open(registry_path, "r", encoding="utf-8") as f:
        text = f.read()
    return {os.path.basename(m) for m in PY.findall(text)}


def main():
    for path, label in ((SETTINGS, "settings.json"), (REGISTRY, "gate-registry.md")):
        if not os.path.exists(path):
            print(f"[drift] {label} not found at {path}", file=sys.stderr)
            return 0

    reg = registered_scripts(SETTINGS)
    doc = registry_scripts(REGISTRY)
    missing_from_doc = sorted(reg - doc)
    stale_in_doc = sorted(doc - reg)

    print("=== gate-registry drift check ===")
    print(f"registered .py in settings.json : {len(reg)}")
    print(f".py named in gate-registry.md   : {len(doc)}")
    print()

    if missing_from_doc:
        print(f"[DRIFT] {len(missing_from_doc)} registered script(s) not named by filename in the registry")
        print("        (function-named-on-purpose gates are expected here):")
        for s in missing_from_doc:
            print(f"  - {s}")
    else:
        print("[ok] every registered script is named in the registry")
    print()

    if stale_in_doc:
        print(f"[DRIFT] {len(stale_in_doc)} registry .py name(s) not registered in settings.json")
        print("        (renamed or removed since the doc was written):")
        for s in stale_in_doc:
            print(f"  - {s}")
    else:
        print("[ok] every registry .py name is still registered")
    return 0


if __name__ == "__main__":
    sys.exit(main())
