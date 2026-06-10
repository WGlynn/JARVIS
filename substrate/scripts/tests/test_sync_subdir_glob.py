"""Per #9 audit suggestion: lock in the subdirectory rglob fix to prevent regression.

Original bug: sync_hooks() used flat `*.py` glob, missed hooks/layer8-audit/*.py.
Fixed 2026-06-10 to use rglob with relative_to preserving subdir structure.
This test asserts the behavior so a future flat-glob regression breaks CI.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "sync-public-substrate.py"


@pytest.fixture
def sync_sandbox(tmp_path: Path):
    """Build a fake HOME with hooks/ and hooks/subdir/ structure + a fake monorepo."""
    home = tmp_path / "home"
    monorepo = tmp_path / "jarvis-monorepo"
    home.mkdir()
    monorepo.mkdir()

    hooks_dir = home / ".claude" / "hooks"
    hooks_dir.mkdir(parents=True)
    (hooks_dir / "top-level-hook.py").write_text("# top level\nprint('top')\n")

    subdir = hooks_dir / "audit-tool"
    subdir.mkdir()
    (subdir / "nested-hook.py").write_text("# nested\nprint('nested')\n")

    # Empty memory + scripts + cron-prompts + session-chain to satisfy sync script
    (home / ".claude" / "projects" / "C--Users-Will" / "memory").mkdir(parents=True)
    (home / ".claude" / "session-chain").mkdir()
    (home / ".claude" / "cron-prompts").mkdir()
    (home / ".claude" / "scripts").mkdir()

    monorepo_substrate = monorepo / "substrate"
    monorepo_substrate.mkdir()
    subprocess.run(["git", "init"], cwd=monorepo, check=False, capture_output=True)

    return home, monorepo


def test_subdir_hook_is_mirrored(sync_sandbox, monkeypatch):
    home, monorepo = sync_sandbox
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--apply", "--no-push"],
        env={**__import__('os').environ, "HOME": str(home), "USERPROFILE": str(home)},
        capture_output=True,
        text=True,
        cwd=str(monorepo.parent),
    )

    mirrored = monorepo / "substrate" / "hooks"
    assert (mirrored / "top-level-hook.py").exists(), f"top-level not mirrored: {result.stdout}{result.stderr}"
    assert (mirrored / "audit-tool" / "nested-hook.py").exists(), \
        f"NESTED hook missing — flat glob regression detected. stdout={result.stdout[:500]}"
