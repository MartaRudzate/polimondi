# lean4 Activity

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

## Entry 3: the area polynomial of the `8k + 5` family, for every `k`

**Date:** 2026-07-12

**Results.**

* `area_wordF` (previously a `sorry`): the area of the perfect polyiamond
  `wordF k`, measured in unit triangles, is
  `P(k) = 144k³ + 232k² + 124k + 19`, for **every** `k` with `k` symbolic.
  Axiom check: only `propext`, `Classical.choice`, `Quot.sound` — no
  `sorry` anywhere in its proof.
* New shoelace machinery in `Lean4.PerfectPolyiamonds`, the area counterpart
  of the `wsum` closure machinery: bilinearity lemmas for `cross`;
  `crossSum p ds` (the shoelace sum of a unit-step walk) with
  `shoelace_scanl` / `shoelace_trace` / `crossSum_append` /
  `crossSum_replicate`; the weighted, side-by-side shoelace sum
  `csum : ℤ → Pt → List Dir → ℤ` with the bridge
  `shoelace_trace_perfectSides : shoelace (trace (perfectSides w)) =
  csum w.length 0 w`, the splitting lemma `csum_append`, and the
  translation lemma `csum_eq_cross_wsum_add_csum : csum n p w =
  cross p (wsum n w) + csum n 0 w` (the start-point dependence of a
  shoelace sum enters only through the boundary vector sum).
* Family closed forms `csum_rep_bdfd` / `csum_rep_afab` in
  `Lean4.Perfect8k_5`: cubic polynomials (in `k`, the start weight `n` and
  the start point `p`, all symbolic) for the shoelace sums along the
  periodic blocks `(bdfd)^k` and `(afab)^k`.

**Methods / decisions.**

* `csum` mirrors the design of `wsum` (integer weights, evaluation side by
  side), so subword sums compose and inductions over `k` need no side
  conditions.  A side of length `ℓ` from `q` in direction `d` contributes
  `ℓ · cross q (vec d)` because `cross` kills the direction of motion —
  this is `crossSum_replicate`.
* The closed forms were first derived numerically (sympy: exact
  interpolation in `k` from `k = 0..5`, validated at `k = 6..9` and against
  a direct shoelace-over-trace computation), then certified in Lean by
  induction on `k` (generalizing `n` and `p`): the step peels one period
  off the front and closes with `push_cast; ring`.
* `area_wordF` assembles the four blocks of `wordF k` with `csum_append`,
  substitutes the closed forms and `wsum_rep_quad`, and reduces to one
  `ring` identity.  The boundary is traced **clockwise**, so the shoelace
  sum is `−P(k)`; the absolute value in `area` is removed by `abs_neg` and
  `positivity` (`P(k) ≥ 19 > 0`).
* Pitfall: `shoelace` recurses on `p :: q :: l` and is not `rfl`-reducible
  through `List.scanl`, so `shoelace_scanl` unfolds via equation lemmas
  (`simp only [..., shoelace]`) rather than `rfl`.
* The instances `P(0) = 19` and `P(1) = 519` remain as independent
  `decide` spot-checks of the polynomial.

Remaining `sorry`s: unchanged except that `Lean4.Perfect8k_5` now has only
`isPerfect_wordF` open (see Entry 4).

## Entry 4: `isPerfect_wordF` reduced to simplicity; existence for `n ≡ 5 (mod 8)`

**Date:** 2026-07-12

**Results.**

* `isPerfect_wordF` is no longer a monolithic `sorry`: four of its five
  fields are now proved for every `k` —
  side count (`8k + 5 ≥ 3`), positive side lengths (new general lemma
  `pos_perfectSides`), the cyclic corner condition
  (`cyclicChain_dirStep_wordF`, axiom check: `propext` only), and closure
  (`closes_wordF`, Entry for the family).  The one remaining open field is
  **simplicity**, isolated as `nodup_trace_wordF` (the only `sorry` in
  `Lean4.Perfect8k_5`).
* New word-level corner machinery: the relation `DirStep p q :=
  q ≠ p ∧ q ≠ p.opp` in `Lean4.PerfectPolyiamonds`, the transfer lemma
  `cyclicChain_cornerStep_iff : CyclicChain' CornerStep (perfectSides w) ↔
  CyclicChain' DirStep w` (via `map_snd_perfectSides` and
  `List.isChain_map`), and the block lemmas `isChain_dirStep_rep_bdfd` /
  `isChain_dirStep_rep_afab` in `Lean4.Perfect8k_5`.
* `exists_isPerfectPolyiamond_of_mod_eight`: for every `n ≡ 5 (mod 8)`
  there is a perfect `n`-polyiamond, namely `wordF (n / 8)` — with `n = 5`
  the smallest length for which perfect polyiamonds exist at all.  (The
  statement inherits the `sorry` of `nodup_trace_wordF` and becomes
  axiom-clean the moment simplicity lands.)

**Methods / decisions.**

* The corner condition is proved at the level of the direction word and
  transferred to the sides: `CornerStep` only inspects the second
  components, so `(perfectSides w).map Prod.snd = w` plus
  `List.isChain_map` gives the equivalence.
* The block lemmas quantify over the **preceding letter** `x` (with the
  hypotheses `DirStep x b` / `DirStep x e`, resp. `DirStep x a`): the first
  period of `(bdfd)^k` is preceded by `c` but later periods by `d`
  (resp. `f` and then `b` for `(afab)^k`), and the `∀ x` form feeds the
  induction directly.  Individual letter pairs are discharged by `decide`.
* Simplicity is not proved, but the geometric analysis is done and recorded
  in the docstring of `nodup_trace_wordF` (planar coordinates
  `(x, y) = (p.1, p.2.1)`, `u := x + y`): the boundary splits into five
  chains in essentially disjoint regions — side `a` on `y = 0`; side `c` on
  `x = n`; the comb `(bdfd)^k` in the band `−16k−7 ≤ y ≤ −8k−4` with tooth
  `j` confined between the diagonals `u_{j+1}` and `u_j`; the connector
  `edf`; and the comb `(afab)^k` in the band `−2k ≤ y ≤ 2k−1`.  Two
  findings make a formalization tractable: along `(afab)^k` the pair
  `(x + y, x)` increases lexicographically at **every** unit step (letters
  `a, f, b` all lex-increase), so that chain's simplicity is a pure
  monotonicity argument; and tracking chain positions by recursively
  defined start points (instead of the closed forms, which are quadratic in
  `j`) keeps every induction step inside `omega`-friendly linear
  arithmetic.  Estimated effort: walk-splitting `Nodup` infrastructure,
  a five-conjunct band invariant for the `bdfd` comb, and ten pairwise
  region checks — roughly 900 lines.

Remaining `sorry`s: `nodup_trace_wordF` (simplicity of the `8k + 5`
family), the necessity direction (`6 ∣ n`) with its colouring scaffolding,
the `Perfect12k` family theorems and combination results, and the
`Perfect8k_8` family theorem.
