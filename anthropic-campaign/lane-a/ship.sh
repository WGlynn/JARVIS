#!/usr/bin/env bash
# Turnkey shipper for the retroactive-rule-audit cookbook PR.
#
# Does the whole Lane-A PR in one command: forks anthropics/claude-cookbooks,
# drops the notebook into misc/, adds the authors.yaml + registry.yaml entries,
# executes the notebook to capture the committed outputs their repo expects,
# lints, commits, pushes a branch, and opens the PR.
#
# Prereqs (all yours, all one-time):
#   - gh authed as WGlynn         (already true)
#   - ANTHROPIC_API_KEY exported  (your key; used ONCE to run the notebook)
#   - python3 available
#
# Usage:
#   export ANTHROPIC_API_KEY=sk-ant-...
#   bash ship.sh
#
# It never force-pushes and opens a normal PR you can close if anything looks off.
set -euo pipefail

STAGE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NB="retroactive_rule_audit.ipynb"
UPSTREAM="anthropics/claude-cookbooks"
BRANCH="cookbook-retroactive-rule-audit"
WORK="${TMPDIR:-/tmp}/claude-cookbooks-ship"

command -v gh >/dev/null || { echo "need gh CLI"; exit 1; }
[ -f "$STAGE/$NB" ] || { echo "missing $NB in $STAGE"; exit 1; }

echo "==> fork $UPSTREAM (idempotent)"
gh repo fork "$UPSTREAM" --clone=false >/dev/null 2>&1 || true

echo "==> shallow-clone your fork"
rm -rf "$WORK"
gh repo clone "WGlynn/claude-cookbooks" "$WORK" -- --depth 1 >/dev/null 2>&1 \
  || git clone --depth 1 "https://github.com/WGlynn/claude-cookbooks.git" "$WORK"
cd "$WORK"
git checkout -b "$BRANCH"

echo "==> place notebook in misc/"
cp "$STAGE/$NB" "misc/$NB"

echo "==> add authors.yaml + registry.yaml entries (append if absent)"
python3 - "$STAGE" <<'PYEOF'
import sys
from pathlib import Path

# authors.yaml: append the WGlynn block if not already present.
authors = Path("authors.yaml")
a = authors.read_text(encoding="utf-8")
if "\nWGlynn:" not in a and not a.startswith("WGlynn:"):
    a = a.rstrip() + (
        "\nWGlynn:\n"
        "  name: Will Glynn\n"
        "  website: https://github.com/WGlynn\n"
        "  avatar: https://avatars.githubusercontent.com/u/41205327?v=4\n"
    )
    authors.write_text(a, encoding="utf-8")
    print("   authors.yaml: added WGlynn")
else:
    print("   authors.yaml: WGlynn already present")

# registry.yaml: append the notebook entry if the path is not already listed.
registry = Path("registry.yaml")
r = registry.read_text(encoding="utf-8")
if "misc/retroactive_rule_audit.ipynb" not in r:
    entry = (
        "- title: 'Catch the rule you already broke: retroactive audits with Claude as judge'\n"
        "  description: A cheap keyword sweep shortlists rules that might apply to\n"
        "    finished work, then Claude acts as a judge that keeps only the rules the\n"
        "    work actually broke. Retrieve widely, judge narrowly.\n"
        "  path: misc/retroactive_rule_audit.ipynb\n"
        "  authors:\n"
        "  - WGlynn\n"
        "  date: '2026-07-05'\n"
        "  categories:\n"
        "  - Patterns\n"
        "  - Tool use\n"
    )
    registry.write_text(r.rstrip() + "\n" + entry, encoding="utf-8")
    print("   registry.yaml: added entry")
else:
    print("   registry.yaml: entry already present")
PYEOF

if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
  echo "==> execute notebook to capture outputs (uses your key once)"
  if command -v uv >/dev/null; then
    uv run --with nbconvert --with ipykernel --with anthropic \
      jupyter nbconvert --to notebook --execute --inplace "misc/$NB"
  else
    python3 -m pip install --quiet nbconvert ipykernel anthropic
    python3 -m nbconvert --to notebook --execute --inplace "misc/$NB"
  fi
  echo "   outputs captured."
else
  echo "!! ANTHROPIC_API_KEY not set: submitting with outputs CLEARED."
  echo "   (their CI executes notebooks, but committing real outputs is preferred;"
  echo "    re-run with the key exported for the cleaner PR.)"
fi

echo "==> lint (ruff, if available)"
if command -v ruff >/dev/null; then ruff check "misc/$NB" || true; fi

echo "==> commit + push"
git add "misc/$NB" authors.yaml registry.yaml
git -c user.name="Will Glynn" -c user.email="tiptaptangsun@gmail.com" \
  commit -q -m "feat(misc): retroactive rule audit with recall + LLM judge"
git push -u origin "$BRANCH"

echo "==> open PR"
gh pr create --repo "$UPSTREAM" \
  --title "feat(misc): retroactive rule audit with recall + LLM judge" \
  --body-file "$STAGE/PR_BODY.md" \
  --head "WGlynn:$BRANCH"

echo ""
echo "Done. Review the PR link above. To undo: gh pr close <n> and delete the branch."
