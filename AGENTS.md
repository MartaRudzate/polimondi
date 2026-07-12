# How to run Python code

## 1. How to activate the virtual environment:

```bash
source venv_poli/bin/activate
```

## For Lean4-related updates

lean4/README.md is the running log of results about perfect polyiamonds
and MUST be kept current: whenever you prove, restate, or restructure
anything under lean4/, append a new dated entry to lean4/README.md as part
of the same task, before finishing. Follow the format of the existing
entries:

- heading `## Entry N: <short title>` (N = next number; the file is
  append-only — never rewrite or delete earlier entries);
- `**Date:**` (today's date);
- `**Results.**` — the theorems/lemmas proved or restated, by their Lean
  names, noting which previous `sorry`s were removed;
- `**Methods / decisions.**` — proof strategy, design choices, pitfalls
  worth remembering;
- close with the up-to-date list of remaining `sorry`s.