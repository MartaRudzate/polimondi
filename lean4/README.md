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

## Entry 2: closure of both families for every `k`; no perfect obtuse hexagon

**Date:** 2026-07-12

**Results.**

* `closes_wordA` / `closes_wordB`: the boundary of `wordA k` (resp.
  `wordB k`) closes — the side vectors sum to the null vector — for **every**
  `k`, with `k` symbolic.  This is the closure field of
  `isPerfectObtuse_wordA` / `isPerfectObtuse_wordB`.
* `not_exists_obtuse_six` (previously a `sorry`): no perfect obtuse hexagon
  exists, via the new kernel-checked lemma `no_obtuse_closed_six`.
* New infrastructure: the weighted vector sum `wsum : ℤ → List Dir → Pt`
  with `wsum n w = n • vec w₀ + (n − 1) • vec w₁ + ⋯`, the splitting lemma
  `wsum_append`, the arithmetic-progression formula `wsum_rep_pair`, and the
  bridge `sum_map_vec_unitSteps_eq_wsum` from the unit-step form of closure.

**Methods / decisions.**

* `wsum` takes an *integer* first argument even though side lengths are
  natural numbers: subword weights like `n − 2k − 3` then never truncate, so
  `wsum_append` and inductions over `k` need no side conditions.
* `wsum_rep_pair` is the "arithmetic progression formula" of the plan: in
  `(xy)^k` traced with weights `n, n − 1, …`, letter `x` collects
  `n + (n−2) + ⋯ = k(n−k+1)` and letter `y` collects `k(n−k)`.  Proof by
  induction on `k` (generalizing `n`); the algebraic step is closed by
  Mathlib's `module` tactic after `push_cast`.
* `closes_wordA`/`closes_wordB` then evaluate the word segment by segment
  (`simp only [wsum_append, wsum_rep_pair, …]`), reduce the resulting
  linear combination of the six direction vectors to components of
  `ℤ × ℤ × ℤ`, and finish with one `ring` per coordinate — the coefficient
  polynomials in `k` cancel identically.  No grid points are enumerated, and
  the proof works for all `k` uniformly.
* For the hexagon, a numeric experiment (Python, see below) showed that of
  the 132 cyclically obtuse 6-words **none** is closed.  So simplicity — and
  with it the classical total-turning/rotation-index argument, which is not
  available in Mathlib — is not needed at all: `no_obtuse_closed_six` refutes
  `obtuse ∧ closes` for all `6^6` letter tuples by `decide +kernel` (≈ 30 s;
  stated with six separate `∀ dᵢ : Dir` quantifiers rather than
  `∀ v : Fin 6 → Dir`, which halves the kernel time by avoiding the pi-type
  `Fintype` enumeration).  `not_exists_obtuse_six` reduces the existential
  over the infinite type `List Dir` to that finite check by writing the
  length-6 word as `List.ofFn v` and expanding its six letters.
* Sanity checks (side-vector sums for `k = 0..7`, the `k(n−k+1)`/`k(n−k)`
  coefficients against random `n, k`, and the closed-hexagon enumeration)
  were run in plain Python before formalizing.

Remaining `sorry`s: the necessity direction (`6 ∣ n`), the full family
theorems `isPerfectObtuse_wordA` / `isPerfectObtuse_wordB` (corner, obtuse
and positivity fields are routine; **simplicity** of the boundary for
symbolic `k` is the substantial open part), and the two combination results
`exists_obtuse_of_six_dvd` / `exists_obtuse_iff`.
