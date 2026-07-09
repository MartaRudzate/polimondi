"""Task 5: assemble families_report.md from families.json + n=48 grep confirmation."""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from core import transition_matrix
from family import generate

HERE = os.path.dirname(__file__)
DBDIR = os.path.join(HERE, '..', 'docs', 'obtuse_new')


def load():
    with open(os.path.join(HERE, 'families.json')) as f:
        return json.load(f)


def load_found48():
    path = os.path.join(HERE, 'found48.txt')
    if not os.path.exists(path):
        return set()
    with open(path) as f:
        return set(line.strip() for line in f if line.strip())


def fmt_matrix(T):
    return '\n'.join('    [' + '  '.join(f'{x:2d}' for x in row) + ']' for row in T)


def main():
    data = load()
    fams = data['families']
    found48 = load_found48()
    pred48 = {idx: w for idx, w in data['pred48']}

    # fold n=48 confirmation into corrob_sizes
    for idx, fam in enumerate(fams):
        w48 = pred48.get(idx)
        if w48 is not None and w48 in found48:
            if 48 not in fam['corrob_sizes']:
                fam['corrob_sizes'] = sorted(fam['corrob_sizes'] + [48])

    # rank by number of distinct corroborated sizes desc, then by n0 asc
    fams.sort(key=lambda f: (-len(f['corrob_sizes']), f['n0'], f['seed']))
    top = fams[:20]

    L = 12
    T = transition_matrix(L)
    lines = []
    lines.append('# Infinite PCL-grammar families of obtuse polyiamonds\n')
    lines.append('Serial 120-degree isogons; strings over {A,B,C,D,E,F} with side lengths '
                 'decreasing n, n-1, ..., 1.\n')
    lines.append('Directions: A=(1,0,-1) B=(1,-1,0) C=(0,-1,1) D=(-1,0,1) E=(-1,1,0) F=(0,1,-1). '
                 'Closure: (n+1)*p(w) - M(w) = 0.\n')
    lines.append(f'\n## Summary\n')
    lines.append(f'- Mechanism found: **C1 multi-site** families. No balanced tandem repeat '
                 f'(p(X)=0, |X|<=12, repeated) exists in the database, so no pure C2 single-block '
                 f'family manifests as a literal repeat; instead families insert several '
                 f'individually-unbalanced length-2/4 blocks whose plain-sums **cancel** '
                 f'(sum_j p(B_j) = 0).')
    lines.append(f'- Step **L = {L}** (divisible by 6); size formula **n = n0 + {L}*k**. '
                 f'Families connect DB sizes spaced by 12: {{12,24,36,48}} or {{18,30,42}}.')
    lines.append(f'- L=6 cross-linking yields **no** edges (checked); the minimal DB-aligned step is 12.')
    lines.append(f'- Total unique families with k=0..3 closed & simple: **{len(fams)}**. '
                 f'Top 20 by number of corroborating DB sizes below.\n')

    lines.append('## Shared transition matrix T on state (D, M)\n')
    lines.append('One family step inserts total balanced length L=12, so D is invariant and '
                 'M shifts by L*D:  D\' = D,  M\' = M + 12*D. In basis (D0,D1,D2,M0,M1,M2):\n')
    lines.append('```')
    lines.append(fmt_matrix(T))
    lines.append('```')
    lines.append('T is unipotent: (T - I)^2 = 0 with rank(T - I) = 3. **Jordan type: three '
                 'Jordan blocks of size 2, all eigenvalue 1** (J = 3 x J_2(1)).\n')

    lines.append('## Top families\n')
    for rank, fam in enumerate(top, 1):
        sizes = fam['corrob_sizes']
        c2 = 'yes (C2)' if fam['blocks_each_balanced'] else 'no (C1: combined cancellation)'
        lines.append(f'### {rank}. seed n0={fam["n0"]}  — corroborated at DB sizes {sizes} '
                     f'({len(sizes)} sizes)')
        lines.append('')
        lines.append(f'- closed form: `{fam["closed_form"]}`')
        lines.append(f'- seed (k=0): `{fam["seed"]}`')
        lines.append(f'- step L = {fam["L"]},  n = {fam["n0"]} + {fam["L"]}*k')
        lines.append(f'- per-step inserted blocks (pos in seed, block): '
                     f'{[(p, b) for p, b in fam["specs"]]}')
        lines.append(f'- inserted plain-sum (C1): {tuple(fam["inserted_psum"])}; '
                     f'each block balanced? {c2}')
        tv = ', '.join(f'k={t["k"]}(n={t["n"]}:{"OK" if t["closed"] and t["simple"] else "FAIL"})'
                       for t in fam['terms'])
        lines.append(f'- verification k=0..3: {tv}')
        # show k=0,1,2 strings explicitly
        s0 = fam['seed']
        lines.append(f'- terms: k0=`{generate(s0,[tuple(x) for x in fam["specs"]],0)}`')
        lines.append(f'         k1=`{generate(s0,[tuple(x) for x in fam["specs"]],1)}`')
        lines.append(f'         k2=`{generate(s0,[tuple(x) for x in fam["specs"]],2)}`')
        lines.append('')

    report = '\n'.join(lines) + '\n'
    with open(os.path.join(DBDIR, 'families_report.md'), 'w') as f:
        f.write(report)
    print(f"wrote families_report.md  (top {len(top)} of {len(fams)} families)")
    # short chat summary stats
    by_sizes = {}
    for fam in fams:
        c = len(fam['corrob_sizes'])
        by_sizes[c] = by_sizes.get(c, 0) + 1
    print("families by #corroborated sizes:", dict(sorted(by_sizes.items(), reverse=True)))
    print("top family corrob sizes:", [f['corrob_sizes'] for f in top[:8]])


if __name__ == '__main__':
    main()
