"""Task 3 engine: de-periodize tandem repeats and cross-link to smaller DB sizes.

For a string at size n', enumerate ways to remove copies from its tandem-repeat
sites so the removed material has total length L_step and total plain-sum p == 0
(condition C1).  Construct the shorter string and test membership in DB[n'-L_step].
"""
import os, sys, itertools
sys.path.insert(0, os.path.dirname(__file__))
from core import p_sum, DIRS
from task2_repeats import tandem_sites

DB = os.path.join(os.path.dirname(__file__), '..', 'docs', 'obtuse_new')


def load_set(n):
    path = os.path.join(DB, f'obtuse_{n}.txt')
    with open(path) as f:
        return set(line.strip() for line in f if line.strip())


def vsum(ps):
    x = y = z = 0
    for p in ps:
        x += p[0]; y += p[1]; z += p[2]
    return (x, y, z)


def deperiodize_options(s, L_step=6, maxp=12):
    """Yield (parent_string, rule) where rule = tuple of (start,len,block,copies_removed)
    for removing copies at tandem sites with total removed length L_step and p-sum 0."""
    sites = [(i, d, r, X, p_sum(X)) for (i, d, r, X) in tandem_sites(s, maxp) if r >= 2]
    if not sites:
        return
    nsites = len(sites)
    # DFS over sites choosing copies c_k in 0..min(r-1, remaining_len//d); prune by length.
    combos = []
    cur = [0] * nsites

    def dfs(k, rem_len, px, py, pz):
        if rem_len == 0:
            if (px, py, pz) == (0, 0, 0) and any(cur):
                combos.append(tuple(cur))
            return
        if k == nsites:
            return
        i, d, r, X, p = sites[k]
        hi = min(r - 1, rem_len // d, 2)
        for c in range(hi + 1):
            cur[k] = c
            dfs(k + 1, rem_len - c * d, px + c * p[0], py + c * p[1], pz + c * p[2])
        cur[k] = 0

    dfs(0, L_step, 0, 0, 0)
    seen_parents = set()
    for combo in combos:
        # build parent by deleting copies, right-to-left
        chosen = [(sites[k][0], sites[k][1], c, sites[k][3]) for k, c in enumerate(combo) if c > 0]
        chosen.sort(key=lambda t: t[0], reverse=True)
        t = s
        for (start, d, c, X) in chosen:
            t = t[:start] + t[start + c * d:]
        if t in seen_parents:
            continue
        seen_parents.add(t)
        # parent-coordinate insertion specs: per-step block = X*c at pos (parent coords)
        specs = []
        asc = sorted(chosen, key=lambda t: t[0])  # by child start ascending
        left_del = 0
        for (start, d, c, X) in asc:
            pos = start - left_del
            specs.append((pos, X * c))
            left_del += c * d
        rule = tuple(sorted((start, d, X, c) for (start, d, c, X) in chosen))
        yield (t, rule, tuple(specs))


def find_edges(child_size, parent_set, L_step=6, limit=None, sample_print=0):
    """Stream the child-size file; yield edges (parent, child, rule) where parent in parent_set."""
    path = os.path.join(DB, f'obtuse_{child_size}.txt')
    edges = []
    n_with_parent = 0
    total = 0
    with open(path) as f:
        for line in f:
            child = line.strip()
            if not child:
                continue
            total += 1
            if limit and total > limit:
                break
            found = False
            for parent, rule, specs in deperiodize_options(child, L_step):
                if parent in parent_set:
                    edges.append((parent, child, rule, specs))
                    found = True
            if found:
                n_with_parent += 1
    return edges, total, n_with_parent


if __name__ == '__main__':
    # probe: do +6 p=0 parent edges exist from 42 -> 36?
    child_size = int(sys.argv[1]) if len(sys.argv) > 1 else 42
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    pset = load_set(child_size - 6)
    edges, total, nwp = find_edges(child_size, pset, 6, limit=limit)
    print(f"probe {child_size}->{child_size-6}: scanned {total} children, {nwp} have a +6 p=0 DB parent, {len(edges)} edges")
    for (par, ch, rule, specs) in edges[:6]:
        print("  parent:", par)
        print("  child :", ch)
        print("  specs :", specs)
        print()
