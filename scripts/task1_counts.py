"""Task 1: load docs/obtuse_new/, group by n, report counts. Streams; no full load."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from core import is_closed

DB = os.path.join(os.path.dirname(__file__), '..', 'docs', 'obtuse_new')
SIZES = [12, 18, 24, 30, 36, 42, 48]


def count_file(path):
    n = 0
    sample = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            n += 1
            if len(sample) < 2:
                sample.append(line)
    return n, sample


if __name__ == '__main__':
    print(f"{'n':>4} {'count':>10}  sample")
    for s in SIZES:
        path = os.path.join(DB, f'obtuse_{s}.txt')
        if not os.path.exists(path):
            continue
        cnt, sample = count_file(path)
        # length sanity + closure check on first sample
        ok = all(len(x) == s for x in sample) and (not sample or is_closed(sample[0]))
        print(f"{s:>4} {cnt:>10}  len_ok={ok}  e.g. {sample[0] if sample else ''}")
