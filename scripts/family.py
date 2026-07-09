"""Family generation and verification (Task 4).

A family is a seed w0 plus insertion specs [(pos, block)] in w0-coordinates:
  w_k = w0 with block*k spliced in at each pos (positions are w0-relative).
n_k = |w0| + k*L,  L = sum(len(block) for pos,block in specs).
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from core import is_closed, is_simple, p_sum, is_balanced


def generate(w0, specs, k):
    res = w0
    for pos, block in sorted(specs, key=lambda x: -x[0]):
        res = res[:pos] + block * k + res[pos:]
    return res


def step_L(specs):
    return sum(len(b) for _, b in specs)


def verify_family(w0, specs, kmax=3):
    """Return dict with per-k (n, closed, simple) and overall ok for k=0..kmax."""
    out = {'terms': [], 'ok': True}
    for k in range(kmax + 1):
        w = generate(w0, specs, k)
        c = is_closed(w)
        s = is_simple(w) if c else False
        out['terms'].append({'k': k, 'n': len(w), 'closed': c, 'simple': s, 'w': w})
        if not (c and s):
            out['ok'] = False
    return out


def decrement(w0, specs):
    """Remove one copy of each block at its spec position (the inverse of one step).
    Returns (smaller_string, new_specs) in the smaller string's coords, or None if
    the blocks are not present (i.e. cannot de-periodize further)."""
    asc = sorted(specs)
    res = w0
    shift = 0
    new_specs = []
    for (pos, block) in asc:
        p = pos - shift
        l = len(block)
        if res[p:p + l] != block:
            return None
        res = res[:p] + res[p + l:]
        new_specs.append((p, block))
        shift += l
    new_specs = tuple(new_specs)
    if generate(res, new_specs, 1) != w0:   # consistency guard
        return None
    return res, new_specs


def minimize_seed(w0, specs):
    """De-periodize downward while terms stay closed & simple; return minimal (seed, specs)."""
    cur_w, cur_specs = w0, tuple(specs)
    while True:
        dec = decrement(cur_w, cur_specs)
        if dec is None:
            break
        w2, specs2 = dec
        if not (is_closed(w2) and is_simple(w2)):
            break
        cur_w, cur_specs = w2, specs2
    return cur_w, cur_specs


def total_inserted_psum(specs):
    x = y = z = 0
    for _, b in specs:
        p = p_sum(b)
        x += p[0]; y += p[1]; z += p[2]
    return (x, y, z)


def closed_form(w0, specs):
    """Render seed split by insertion points into  S0 (B1)^k S1 (B2)^k ... form."""
    pts = sorted(specs, key=lambda x: x[0])
    parts = []
    prev = 0
    for pos, block in pts:
        parts.append(w0[prev:pos])
        parts.append(f"({block})^k")
        prev = pos
    parts.append(w0[prev:])
    # drop empty segments but keep structure readable
    return ''.join(p for p in parts if p != '')
