#!/usr/bin/env python3
"""Search for new perfect polyiamond sequences with Step=8.

Strategy:
  For each valid n-polyiamond S (n=5..12) and each valid (n+8)-polyiamond T,
  find all ways T can be obtained from S by inserting fixed groups at positions
  according to the patterns (4,4), (2,4,2), (2,2,2,2).
  A candidate is kept if the k=2 AND k=3 members are also geometrically valid.

Deduplication:
  Two different expressions can produce identical strings for all k (e.g.
  ``ab(ab)^k X`` and ``(ab)^k ab X`` are the same sequence).  We deduplicate
  by the fingerprint tuple (k0, k1, k2, k3) of member strings rather than by
  the expression text.

Output: scripts/sequences/out/new_sequences.csv
"""

import os
import csv
import re
import sys

# ── Direction vectors in triangular grid (x,y,z) where x+y+z=0 ──────────────
DIRS = {
    'A': (1, 0, -1), 'B': (1, -1, 0), 'C': (0, -1, 1),
    'D': (-1, 0, 1), 'E': (-1, 1, 0), 'F': (0, 1, -1),
}


def check_valid(s: str) -> bool:
    """Return True iff side-string s is a valid (closed, simple) polyiamond."""
    s = s.upper()
    sides = list(zip(range(len(s), 0, -1), s))
    cx, cy, cz = 0, 0, 0
    visited: set = set()  # empty — closing step adds (0,0,0) last
    simple = True
    for length, d in sides:
        dx, dy, dz = DIRS[d]
        for i in range(1, length + 1):
            pt = (cx + i * dx, cy + i * dy, cz + i * dz)
            if pt in visited:
                simple = False
            else:
                visited.add(pt)
        cx += length * dx
        cy += length * dy
        cz += length * dz
    return (cx == 0 and cy == 0 and cz == 0) and simple


# ── Database loading ──────────────────────────────────────────────────────────

def load_poly_db(max_n: int = 20) -> dict[int, set[str]]:
    """Load perfect polyiamonds for n=5..max_n from docs/polimondi/."""
    here = os.path.dirname(os.path.abspath(__file__))
    docs = os.path.normpath(os.path.join(here, '..', '..', 'docs', 'polimondi'))
    db: dict[int, set[str]] = {}
    for n in range(5, max_n + 1):
        path = os.path.join(docs, f'perfect_{n}.txt')
        if not os.path.exists(path):
            continue
        with open(path) as f:
            strings = set(line.strip().upper() for line in f if line.strip())
        db[n] = strings
        print(f"  loaded perfect_{n}: {len(strings):>7,} strings", file=sys.stderr)
    return db


# ── Sequence construction helpers ─────────────────────────────────────────────

def build_k_string(S: str, positions: list[int], groups: list[str], k: int) -> str:
    """Return the k-th member of the sequence defined by (S, positions, groups)."""
    parts: list[str] = []
    prev = 0
    for p, g in zip(positions, groups):
        parts.append(S[prev:p])
        parts.append(g * k)
        prev = p
    parts.append(S[prev:])
    return ''.join(parts)


def build_expression(S: str, positions: list[int], groups: list[str]) -> str:
    """Return the CSV-style expression string, e.g. ``(ab)^k ace(dede)^k dfb(ab)^k``."""
    parts: list[str] = []
    prev = 0
    for p, g in zip(positions, groups):
        if p > prev:
            parts.append(S[prev:p].lower())
        parts.append(f'({g.lower()})^k')
        prev = p
    if prev < len(S):
        parts.append(S[prev:].lower())
    return ' '.join(parts)


def fingerprint(S: str, positions: list[int], groups: list[str]) -> tuple[str, ...]:
    """Return (k0, k1, k2, k3) member strings — used for deduplication."""
    return tuple(build_k_string(S, positions, groups, k) for k in range(4))


# ── Alignment search ──────────────────────────────────────────────────────────

def find_alignments(S: str, T: str, pattern: tuple[int, ...]) -> list[tuple]:
    """Find all (positions, groups) such that T == build_k_string(S, positions, groups, 1).

    Uses early termination: once a character mismatch is found, larger insertion
    points at the same depth are skipped.
    """
    n = len(S)
    m = len(pattern)
    results: list[tuple] = []
    pos_acc: list[int] = []
    grp_acc: list[str] = []

    def search(s_pos: int, t_pos: int, depth: int) -> None:
        if depth == m:
            if S[s_pos:] == T[t_pos:]:
                results.append((pos_acc[:], grp_acc[:]))
            return
        l = pattern[depth]
        offset = 0
        while s_pos + offset <= n:
            p = s_pos + offset
            if offset > 0 and S[p - 1] != T[t_pos + offset - 1]:
                break  # mismatch → larger insertion points can't match either
            t_end = t_pos + offset + l
            if t_end <= len(T):
                pos_acc.append(p)
                grp_acc.append(T[t_pos + offset: t_end])
                search(p, t_end, depth + 1)
                pos_acc.pop()
                grp_acc.pop()
            offset += 1

    search(0, 0, 0)
    return results


# ── Known-sequence fingerprints ───────────────────────────────────────────────

_CSV_GROUP_RE = re.compile(r"\(([a-fA-F]+)\)\^k", re.IGNORECASE)


def _expand(expression: str, k: int) -> str:
    compact = re.sub(r"\s+", "", expression)
    return _CSV_GROUP_RE.sub(lambda m: m.group(1) * k, compact).upper()


def load_known_fingerprints(csv_path: str) -> set[tuple[str, ...]]:
    """Build (k0,k1,k2,k3) fingerprints for all known step-8 sequences."""
    fps: set[tuple[str, ...]] = set()
    if not os.path.exists(csv_path):
        return fps
    with open(csv_path, newline='') as f:
        for row in csv.DictReader(f):
            if int(row.get('Step', 0)) != 8:
                continue
            try:
                fp = tuple(_expand(row['Expression'], k) for k in range(4))
                fps.add(fp)
            except Exception:
                pass
    return fps


# ── Main search ───────────────────────────────────────────────────────────────

# Insertion patterns summing to 8.
PATTERNS: list[tuple[int, ...]] = [
    (4, 4),         # 2 locations × 4 letters
    (2, 4, 2),      # 3 locations: 2+4+2
    (2, 2, 2, 2),   # 4 locations × 2 letters
]


def search_all(poly_db: dict, known_fps: set) -> list[dict]:
    results: list[dict] = []
    seen_fps: set[tuple] = set(known_fps)

    for n in range(5, 13):
        if n not in poly_db:
            continue
        tn = n + 8
        if tn not in poly_db:
            continue

        base_list = sorted(poly_db[n])
        target_set = poly_db[tn]

        print(f"\nn={n}: {len(base_list)} bases, {len(target_set):,} targets …",
              file=sys.stderr, flush=True)
        found_n = 0
        pairs_done = 0

        for S in base_list:
            for T in target_set:
                pairs_done += 1
                for pat in PATTERNS:
                    for positions, groups in find_alignments(S, T, pat):
                        # Geometric verification for k=2 and k=3
                        k2 = build_k_string(S, positions, groups, 2)
                        if not check_valid(k2):
                            continue
                        k3 = build_k_string(S, positions, groups, 3)
                        if not check_valid(k3):
                            continue

                        # Deduplicate by full fingerprint (handles shift equivalence)
                        fp = (build_k_string(S, positions, groups, 0), k2[:0] or
                              build_k_string(S, positions, groups, 1), k2, k3)
                        # Re-use already-computed strings
                        fp = (
                            build_k_string(S, positions, groups, 0),
                            build_k_string(S, positions, groups, 1),
                            k2,
                            k3,
                        )
                        if fp in seen_fps:
                            continue
                        seen_fps.add(fp)

                        expr = build_expression(S, positions, groups)
                        entry = {
                            'SeqName': f'NEW_n{n}_{len(results) + 1}',
                            'Expression': expr,
                            'InitialValue': n,
                            'Step': 8,
                            'Locations': len(positions),
                        }
                        results.append(entry)
                        found_n += 1

            # Progress tick per base string
            print(f"  {S}: +{found_n} so far", file=sys.stderr, flush=True)

        print(f"  → {found_n} new sequences for n={n}", file=sys.stderr)

    return results


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(here, 'perfect_polyiamond_sequences.csv')
    out_path = os.path.join(here, 'out', 'new_sequences.csv')

    print("Loading databases …", file=sys.stderr)
    poly_db = load_poly_db(max_n=20)

    known_fps = load_known_fingerprints(csv_path)
    print(f"\nKnown step-8 fingerprints: {len(known_fps)}", file=sys.stderr)

    print("\nSearching …", file=sys.stderr)
    results = search_all(poly_db, known_fps)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fieldnames = ['SeqName', 'Expression', 'InitialValue', 'Step', 'Locations']
    with open(out_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nDone. Found {len(results)} new sequences -> {out_path}")


if __name__ == '__main__':
    main()
