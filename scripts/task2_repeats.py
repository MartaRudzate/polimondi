"""Task 2: detect tandem repeats X^r (r>=2, 1<=|X|<=12) and keep balanced periods.

Aggregates across a file: which balanced period-strings X occur, with what period
length, and in how many database strings.  Prints only short summaries.
Usage: python3 task2_repeats.py <file> [maxperiod]
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from core import is_balanced


def tandem_sites(s, maxp=12):
    """Yield (start, period_len, reps, period_str) for maximal tandem repeats.
    A site is maximal: not extendable left by one full period."""
    n = len(s)
    for d in range(1, maxp + 1):
        i = 0
        while i + 2 * d <= n:
            if s[i:i + d] == s[i + d:i + 2 * d]:
                # maximal-left check
                if i - d >= 0 and s[i - d:i] == s[i:i + d]:
                    i += 1
                    continue
                # count reps
                r = 2
                while i + (r + 1) * d <= n and s[i + r * d:i + (r + 1) * d] == s[i:i + d]:
                    r += 1
                yield (i, d, r, s[i:i + d])
                i += r * d
            else:
                i += 1


def scan_file(path, maxp=12, only_balanced=True):
    # counts[(d, X)] = number of strings containing >=1 such balanced site
    counts = collections.Counter()
    total = 0
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            total += 1
            seen = set()
            for (i, d, r, X) in tandem_sites(s, maxp):
                if only_balanced and not is_balanced(X):
                    continue
                seen.add((d, X))
            for key in seen:
                counts[key] += 1
    return total, counts


if __name__ == '__main__':
    path = sys.argv[1]
    maxp = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    total, counts = scan_file(path, maxp)
    print(f"file={os.path.basename(path)} strings={total} distinct balanced periods={len(counts)}")
    # group by period length
    bylen = collections.Counter()
    for (d, X), c in counts.items():
        bylen[d] += 1
    print("balanced-period count by |X|:", dict(sorted(bylen.items())))
    print("top balanced periods (|X|, X, #strings):")
    for (d, X), c in counts.most_common(25):
        print(f"  |X|={d:2d}  X={X:<13} in {c} strings")
