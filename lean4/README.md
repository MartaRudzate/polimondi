# lean4

The log of decisions when proving results from PerfectPolyiamonds.lean. 
Please record the date, the result achieved and methods/decisions taken 
to prove something.

## Entry 1: `wordA 0` is a perfect obtuse polyiamond; weighted-sum form of closure

**Date:** 2026-07-12

**Results.**

* `example : IsPerfectObtusePolyiamond (wordA 0)` — the smallest serial 120°
  isogon, the 12-gon `abcdedefafab` with sides `12, 11, …, 1` (the word is
  spelled out in the new lemma `wordA_zero`).
* `isPerfect_closes_iff_weightedSum` (previously a `sorry`), via the new
  lemma `sum_unitSteps_perfectSides`: the unit-step boundary sum of a perfect
  polyiamond equals the weighted sum `∑_{i<n} (n − i) · vec wᵢ` of its
  direction vectors.
* Prerequisite fix: `CyclicChain'` now uses `List.IsChain` instead of the
  deprecated `List.Chain'`, whose `Decidable` instance no longer exists in
  the pinned Mathlib (`v4.31.0`) — without this the file did not compile.

**Methods / decisions.**

* Every field of `IsPerfectObtusePolyiamond (wordA 0)` is a finite check, so
  the proof discharges each field by `decide` — a computation certified by
  the Lean kernel, with no `native_decide` and hence no trust in the
  compiler.  The fields are proved one by one (rather than by a single
  opaque `decide` on the whole predicate) so a reader sees exactly which
  finite facts are being checked: side count, positive lengths, genuine
  corners, closure, simplicity, and ±60° turns.
* The one expensive field is simplicity: the boundary visits
  `12·13/2 = 78` lattice points and `Nodup` compares all `~78²/2` pairs,
  which exceeds the recursion limit of the `decide` elaborator.
  `decide +kernel` (evaluation delegated directly to the kernel) handles it
  in a few seconds.  For larger members of the families (`wordA k`, `k ≥ 1`)
  `native_decide` remains the practical per-instance certificate; the
  uniform statement `isPerfectObtuse_wordA` still awaits a symbolic proof.
* `sum_unitSteps_perfectSides` is stated with natural-number weights
  `(w.length − i) • vec wᵢ`, which makes the induction on the word a plain
  `simp` with `Fin.sum_univ_succ` (each side `(ℓ, d)` contributes
  `ℓ • vec d`, by `List.sum_replicate`) — no integer-cast bookkeeping inside
  the induction.  The integer-weighted `iff` of
  `isPerfect_closes_iff_weightedSum` then follows by `natCast_zsmul` and
  `omega` (using `i < w.length`, so the ℕ-subtraction is not truncated).
  This equality — not just the `iff` — is the intended entry point for
  proving closure ("the side vectors sum to the null vector") of the general
  families `wordA k` / `wordB k` symbolically.

Remaining `sorry`s: the necessity direction (`6 ∣ n`, via the total-turning
and mod-3 colouring arguments), the general families
`isPerfectObtuse_wordA` / `isPerfectObtuse_wordB`, the `n = 6`
non-existence, and the resulting characterization `exists_obtuse_iff`.
