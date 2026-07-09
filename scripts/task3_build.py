"""Tasks 3-5 orchestration: build L=12 edges over DB sizes <=42, minimize seeds,
dedupe families, score corroboration, verify generated terms, and persist results.

n=48 membership is verified later via a single batched grep (see run_all.sh),
not by streaming the 7.5M-line file here.
"""
import os, sys, json, itertools
sys.path.insert(0, os.path.dirname(__file__))
from crosslink import load_set, find_edges, DB
from family import (generate, minimize_seed, verify_family, closed_form,
                    step_L, total_inserted_psum)
from core import is_balanced

SIZES = [12, 18, 24, 30, 36, 42]
L = 12


def main():
    sets = {n: load_set(n) for n in SIZES}
    # build edges for each (child, parent=child-12) pair within <=42
    all_edges = []
    for child in [24, 30, 36, 42]:
        edges, total, nwp = find_edges(child, sets[child - L], L)
        print(f"edges {child}->{child-L}: {len(edges)} (of {total} children)", file=sys.stderr)
        all_edges.extend(edges)

    # minimize each edge to a canonical (seed, specs) family key
    families = {}
    for (par, ch, rule, specs) in all_edges:
        seed, sspecs = minimize_seed(par, specs)
        key = (seed, sspecs)
        families.setdefault(key, 0)
        families[key] += 1

    results = []
    pred48 = []  # (family_index, predicted_48_string)
    for (seed, sspecs) in families:
        v = verify_family(seed, sspecs, 3)
        if not v['ok']:
            continue  # discard families failing closed/simple for k=0..3
        n0 = len(seed)
        # corroboration: which DB sizes 12..48 does the family hit & are confirmed?
        corrob = []
        idx = len(results)
        k = 0
        while True:
            nk = n0 + L * k
            if nk > 48:
                break
            w = generate(seed, sspecs, k)
            if nk <= 42:
                if w in sets.get(nk, set()):
                    corrob.append(nk)
            elif nk == 48:
                pred48.append((idx, w))   # confirm later by grep
            k += 1
        results.append({
            'seed': seed,
            'n0': n0,
            'specs': [[p, b] for (p, b) in sspecs],
            'L': step_L(sspecs),
            'inserted_psum': list(total_inserted_psum(sspecs)),
            'blocks_each_balanced': all(is_balanced(b) for _, b in sspecs),
            'closed_form': closed_form(seed, sspecs),
            'terms': [{'k': t['k'], 'n': t['n'], 'closed': t['closed'],
                       'simple': t['simple']} for t in v['terms']],
            'corrob_sizes': corrob,   # 48 appended after grep
        })

    out = {'families': results, 'pred48': pred48}
    with open(os.path.join(os.path.dirname(__file__), 'families.json'), 'w') as f:
        json.dump(out, f)
    print(f"unique families (k0..3 valid): {len(results)}", file=sys.stderr)
    # write predicted 48-strings for batched grep
    with open(os.path.join(os.path.dirname(__file__), 'pred48.txt'), 'w') as f:
        for idx, w in pred48:
            f.write(f"{idx}\t{w}\n")


if __name__ == '__main__':
    main()
