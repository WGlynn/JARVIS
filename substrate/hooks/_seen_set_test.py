"""pytest for _seen_set: seen-set roundtrip + deep-context signal + housekeeping.

Run:  python -m pytest hooks/_seen_set_test.py -q
"""
import importlib.util
import os
import time
from pathlib import Path

_MOD = Path(__file__).with_name("_seen_set.py")
_spec = importlib.util.spec_from_file_location("_seen_set", _MOD)
ss = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ss)


def test_load_empty(tmp_path):
    assert ss.load_seen("s1", tmp_path) == set()
    assert ss.has_seen("s1", "x.md", tmp_path) is False


def test_mark_and_has(tmp_path):
    ss.mark_seen("s1", "a.md", tmp_path)
    assert ss.has_seen("s1", "a.md", tmp_path)
    assert not ss.has_seen("s1", "b.md", tmp_path)


def test_mark_list_and_persist(tmp_path):
    ss.mark_seen("s1", ["a.md", "b.md"], tmp_path)
    # fresh call re-reads from disk -> proves persistence
    assert ss.load_seen("s1", tmp_path) == {"a.md", "b.md"}


def test_sessions_isolated(tmp_path):
    ss.mark_seen("s1", "a.md", tmp_path)
    assert ss.load_seen("s2", tmp_path) == set()


def test_idempotent_mark(tmp_path):
    ss.mark_seen("s1", "a.md", tmp_path)
    ss.mark_seen("s1", "a.md", tmp_path)
    assert ss.load_seen("s1", tmp_path) == {"a.md"}


def test_mark_accumulates(tmp_path):
    ss.mark_seen("s1", "a.md", tmp_path)
    ss.mark_seen("s1", ["b.md", "c.md"], tmp_path)
    assert ss.load_seen("s1", tmp_path) == {"a.md", "b.md", "c.md"}


def test_is_deep_context_false_without_sentinel(tmp_path):
    assert ss.is_deep_context("s1", tmp_path) is False
    assert ss.is_deep_context("", tmp_path) is False


def test_is_deep_context_true_with_sentinel(tmp_path):
    (tmp_path / "s1.c1").write_text("654309")
    assert ss.is_deep_context("s1", tmp_path) is True
    # a different session without a sentinel is still normal-mode
    assert ss.is_deep_context("s2", tmp_path) is False


def test_clear(tmp_path):
    ss.mark_seen("s1", "a.md", tmp_path)
    ss.clear("s1", tmp_path)
    assert ss.load_seen("s1", tmp_path) == set()


def test_prune(tmp_path):
    old = tmp_path / "old.seen-set.json"
    old.write_text('{"seen":["a.md"]}')
    stamp = time.time() - 30 * 86400
    os.utime(old, (stamp, stamp))
    fresh = tmp_path / "new.seen-set.json"
    fresh.write_text('{"seen":["b.md"]}')
    removed = ss.prune(days=7, hd=tmp_path)
    assert removed == 1
    assert not old.exists()
    assert fresh.exists()


def test_corrupt_file_is_failopen(tmp_path):
    (tmp_path / "s1.seen-set.json").write_text("{not valid json")
    assert ss.load_seen("s1", tmp_path) == set()
