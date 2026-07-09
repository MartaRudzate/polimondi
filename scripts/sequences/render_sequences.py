#!/usr/bin/env python3
"""Render the perfect-polyiamond sequences listed in
``perfect_polyiamond_sequences.csv`` as SVG pictures.

Each CSV row describes an infinite family of perfect polyiamonds
parametrised by ``k = 0, 1, 2, ...``.  The ``Expression`` column uses the
shorthand ``(group)^k`` to denote a ``group`` repeated ``k`` times, so the
k-th member is obtained by substituting ``k`` and dropping the parentheses.
For example::

    acec(ecea)^k eceaeafabcb(abcb)^k db

expands (k=1) to ``acececeaeceaeafabcbabcbdb``.

A *perfect* polyiamond of ``n`` sides uses the six unit directions
``A..F`` (60-degree steps) with strictly decreasing side lengths
``[n, n-1, ..., 1]``.  For a member to be a valid (simple) polygon two
conditions must hold:

1. drawing all the side vectors returns to the origin, and
2. the boundary does not touch or cross itself.

For every sequence this script checks the first ``NUM_MEMBERS`` members,
prints a warning for any member that is malformed / does not return /
self-intersects, and writes the valid members side by side into
``out/<SeqName>.svg``.

Run from anywhere::

    python scripts/sequences/render_sequences.py
"""

import csv
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")  # head-less SVG rendering, no display needed
import matplotlib.pyplot as plt

from polyforms.point_tg import PointTg, DIRECTIONS
from polyforms.polyiamond import Polyiamond
from polyforms.draw_scene import DrawScene, Align

# How many members (k = 0, 1, ..., NUM_MEMBERS-1) of each sequence to check
# and draw.  k=3 is included so that "intersects for k=3" style problems show.
NUM_MEMBERS = 7

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "out")

# Substitutes a single ``(group)^k`` occurrence; whitespace is stripped first.
_GROUP_RE = re.compile(r"\(([a-fA-F]+)\)\^k")


def expand(expression, k):
    """Expand a sequence ``Expression`` for a given ``k`` into the bare side
    string (upper-case, no spaces, no parentheses)."""
    compact = re.sub(r"\s+", "", expression)
    expanded = _GROUP_RE.sub(lambda m: m.group(1) * k, compact)
    return expanded.upper()


def check_member(side_string):
    """Validate a single perfect-polyiamond side string.

    Returns ``(closes, simple)`` where ``closes`` is True when the side
    vectors return to the origin and ``simple`` is True when the boundary
    never revisits a lattice point (i.e. the polygon does not self-touch or
    self-cross).  Mirrors ``Polyiamond.is_valid`` but reports the two
    conditions separately so we can emit a precise warning.
    """
    sides = list(zip(range(len(side_string), 0, -1), side_string))
    current = PointTg(0, 0, 0)
    visited = set()
    simple = True
    for length, direction in sides:
        step = DIRECTIONS[direction]
        for i in range(1, length + 1):
            point = current + i * step
            if point in visited:
                simple = False
            else:
                visited.add(point)
        current = current + length * step
    closes = current == PointTg(0, 0, 0)
    return closes, simple


def render_sequence(name, expression, initial_value, step):
    """Check the first ``NUM_MEMBERS`` members of one sequence and draw the
    valid ones into ``out/<name>.svg``.  Returns the list of valid k values."""
    polys = []
    valid_ks = []
    for k in range(NUM_MEMBERS):
        side_string = expand(expression, k)
        actual_len = len(side_string)
        expected_len = initial_value + k * step

        if actual_len != expected_len:
            print(
                f"WARNING: {name}: member k={k} has {actual_len} sides, "
                f"but InitialValue+k*Step = {expected_len} "
                f"(malformed expression?)"
            )
            continue

        closes, simple = check_member(side_string)
        if not closes:
            print(f"WARNING: {name}: the sequence for k={k} does not return to the origin")
            continue
        if not simple:
            print(f"WARNING: {name}: the side sequence for k={k} intersects itself")
            # continue

        polys.append(Polyiamond(side_string))
        valid_ks.append(k)

    if not polys:
        print(f"WARNING: {name}: no valid members in k=0..{NUM_MEMBERS - 1}; no SVG written")
        return valid_ks

    scene = DrawScene(Align.BASELINE)
    for k, poly in zip(valid_ks, polys):
        scene.add_polyiamond(f"k{k}", poly)
    scene.pack()
    scene.set_size_in(max(6.0, scene.width * 0.12), max(3.0, scene.height * 0.3))
    scene.fig.suptitle(f"{name}   (k = {', '.join(str(k) for k in valid_ks)})", fontsize=10)

    out_path = os.path.join(OUT_DIR, f"{name}.svg")
    scene.fig.savefig(out_path, format="svg", bbox_inches="tight", pad_inches=0.1)
    plt.close("all")  # DrawScene() opens a stray figure besides scene.fig
    print(f"wrote {os.path.relpath(out_path, HERE)}  ({len(valid_ks)} members)")
    return valid_ks


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <sequences.csv>")
        sys.exit(1)
    os.makedirs(OUT_DIR, exist_ok=True)
    CSV_PATH = os.path.join(HERE, sys.argv[1])
    with open(CSV_PATH, newline="") as f:
        rows = list(csv.DictReader(f))

    print(f"Processing {len(rows)} sequences from {os.path.basename(CSV_PATH)}\n")
    for row in rows:
        render_sequence(
            row["SeqName"],
            row["Expression"],
            int(row["InitialValue"]),
            int(row["Step"]),
        )


if __name__ == "__main__":
    main()
