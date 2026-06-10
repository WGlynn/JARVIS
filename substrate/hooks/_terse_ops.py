"""L3 — APL-style terse hot-path ops.
1-char names + minimal-token-cost helpers for hook internals.
Read by devs at debug-time only; runtime callers don't care about readability.

Naming convention (APL/J/K inspired):
    a  any                e  every (all)             c  count
    S  sum                 P  product                M  max
    m  min                 d  dedup (set)            f  filter (truthy)
    Z  zip                 W  window (sliding)       k  keys-of
    R  range               H  head N                 T  tail N
    s  split               j  join                   B  bytes-len
    N  now (wall sec)      D  delta-now-vs(ts)       J  json-loads

Each op is < 4 source-tokens. Hook scoring math compresses 3-5x vs
descriptive-name Python while staying valid CPython. Cost: one
import line; benefit: every gate-fire pays less.
"""
from __future__ import annotations
import json as _j
import time as _t
from typing import Any, Iterable

a = any
e = all
c = len
S = sum
P = lambda xs: __import__('math').prod(xs)
M = max
m = min
d = lambda xs: list(dict.fromkeys(xs))
f = lambda xs: [x for x in xs if x]
Z = zip
W = lambda xs, n: [xs[i:i+n] for i in range(len(xs)-n+1)]
k = lambda obj: list(obj.keys()) if hasattr(obj, 'keys') else []
R = range
H = lambda xs, n: xs[:n]
T = lambda xs, n: xs[-n:] if n else []
s = lambda x, sep=None: x.split(sep) if sep else x.split()
j = lambda xs, sep='': sep.join(map(str, xs))
B = lambda x: len(x.encode('utf-8')) if isinstance(x, str) else len(x)
N = _t.time
D = lambda ts: _t.time() - ts
J = _j.loads


def score(weights: dict, hits: dict) -> float:
    """w·h dot product. score({'a':2,'b':1}, {'a':3,'b':5}) -> 11."""
    return S(weights.get(k_, 0) * v for k_, v in hits.items())


def conf(s: float, lo: float, hi: float) -> float:
    """Clamp+normalize score to [0,1] confidence."""
    return 0.0 if s <= lo else 1.0 if s >= hi else (s - lo) / (hi - lo)


def recent(ts_list: Iterable[float], window_s: float) -> int:
    """Count timestamps within last window_s seconds."""
    cut = N() - window_s
    return c(f(t >= cut for t in ts_list))
