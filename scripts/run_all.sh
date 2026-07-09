#!/bin/bash
# Reproduce the obtuse-polyiamond family analysis end to end.
# Heavy data stays on disk; only short summaries print.
set -e
cd "$(dirname "$0")/.."

echo "== Task 1: counts =="
python3 scripts/task1_counts.py

echo "== Task 2: balanced tandem repeats (none exist; families are C1 multi-site) =="
python3 scripts/task2_repeats.py docs/obtuse_new/obtuse_42.txt 12 | head -4

echo "== Task 3/4: build L=12 families over DB sizes <=42, minimize seeds, verify =="
python3 scripts/task3_build.py

echo "== Confirm predicted n=48 members in DB[48] via one grep pass =="
cut -f2 scripts/pred48.txt > scripts/pred48_strings.txt
grep -Fxf scripts/pred48_strings.txt docs/obtuse_new/obtuse_48.txt > scripts/found48.txt || true
echo "matched $(wc -l < scripts/found48.txt) / $(wc -l < scripts/pred48.txt) predicted n=48 members"

echo "== Task 5: write report =="
python3 scripts/task5_report.py
