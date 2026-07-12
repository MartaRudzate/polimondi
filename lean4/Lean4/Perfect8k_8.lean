/-
  Perfect polyiamonds: the `8k + 8` family `E(k)`
  ===============================================

  The infinite family of boundary words

    `E(k) = ab · (ab)^k · dede · (dede)^k · ab · (ab)^k`

  over `Σ = {a, …, f}` (here `wordE k`), of length `n = 8k + 8`
  (i.e. `n = 8, 16, 24, …`).  For `k = 0` this is the word `abdedeab`.

  Every `wordE k` encodes a perfect `(8k + 8)`-polyiamond: the boundary
  closes (`closes_wordE`, proved for every `k` with `k` symbolic, via the
  `wsum`/`rep` machinery of `Lean4.PerfectPolyiamonds`), and the `k = 0`
  instance is certified by `decide`.

  **Warning — this family is *not* obtuse.**  The two block junctions
  `…ab·de…` and `…de·ab…` are turns by `±120°`, i.e. interior angles of
  `60°`, so `wordE k` fails `CyclicChain' ObtuseStep` at those two
  vertices (all remaining angles are `120°` or `240°`).  This is proved
  below for *every* `k` (`not_obtuse_wordE`), so the family satisfies
  `IsPerfectPolyiamond` but never `IsPerfectObtusePolyiamond`.  That is
  consistent with the necessity theorem `six_dvd_length_of_obtuse`: a
  perfect obtuse `n`-polyiamond needs `6 ∣ n`, while `8k + 8` is divisible
  by `6` only for `k ≡ 2 (mod 3)` — and even for those lengths the two
  `60°` angles remain, which is why the direct proof matters.
-/
import Lean4.PerfectPolyiamonds

namespace Polyiamond

/-! ### The words `E(k)` -/

open Dir in
/-- The `8k + 8` family (i.e. `n = 8, 16, 24, …`):
`E(k) = ab · (ab)^k · dede · (dede)^k · ab · (ab)^k`.
For `k = 0` this is `abdedeab` (see `wordE_zero`). -/
def wordE (k : ℕ) : List Dir :=
  [a, b] ++ rep [a, b] k ++
  [d, e, d, e] ++ rep [d, e, d, e] k ++
  [a, b] ++ rep [a, b] k

open Dir in
/-- `wordE 0` spelled out: the word `abdedeab`. -/
lemma wordE_zero : wordE 0 = [a, b, d, e, d, e, a, b] := rfl

@[simp] lemma wordE_length (k : ℕ) : (wordE k).length = 8 * k + 8 := by
  simp only [wordE, List.length_append, rep_length, List.length_cons,
    List.length_nil]
  omega

/-! ### Two `rep` normal forms

`wordE` is spelled exactly as the source expression `E(k)`; for the closure
computation and the junction analysis it is more convenient to regroup it
into three maximal periodic blocks of two-letter periods,
`(ab)^{k+1} · (de)^{2k+2} · (ab)^{k+1}`. -/

/-- A four-letter period of the form `xyxy` is a doubled two-letter period. -/
lemma rep_pair_pair (x y : Dir) (k : ℕ) :
    rep [x, y, x, y] k = rep [x, y] (2 * k) := by
  induction k with
  | zero => rfl
  | succ k ih =>
    have h : rep [x, y, x, y] (k + 1) = [x, y, x, y] ++ rep [x, y, x, y] k := rfl
    have h2 : 2 * (k + 1) = 2 * k + 1 + 1 := by ring
    have h3 : rep [x, y] (2 * k + 1 + 1) = [x, y] ++ rep [x, y] (2 * k + 1) := rfl
    have h4 : rep [x, y] (2 * k + 1) = [x, y] ++ rep [x, y] (2 * k) := rfl
    rw [h, ih, h2, h3, h4]
    simp

/-- Splitting the first letter and the last letter off a repeated pair:
`(xy)^{k+1} = x · (yx)^k · y`. -/
lemma rep_pair_snoc (x y : Dir) (k : ℕ) :
    rep [x, y] (k + 1) = x :: (rep [y, x] k ++ [y]) := by
  induction k with
  | zero => rfl
  | succ k ih =>
    have h : rep [x, y] (k + 1 + 1) = [x, y] ++ rep [x, y] (k + 1) := rfl
    have h' : rep [y, x] (k + 1) = [y, x] ++ rep [y, x] k := rfl
    rw [h, ih, h']
    simp

open Dir in
/-- `E(k)` regrouped into its three maximal periodic blocks:
`E(k) = (ab)^{k+1} · (de)^{2k+2} · (ab)^{k+1}`. -/
lemma wordE_eq (k : ℕ) :
    wordE k = rep [a, b] (k + 1) ++ rep [d, e] (2 * k + 2) ++ rep [a, b] (k + 1) := by
  have h1 : rep [a, b] (k + 1) = [a, b] ++ rep [a, b] k := rfl
  have h2 : 2 * k + 2 = 2 * (k + 1) := by ring
  have h3 : rep [d, e, d, e] (k + 1) = [d, e, d, e] ++ rep [d, e, d, e] k := rfl
  rw [h2, ← rep_pair_pair, h3, h1, wordE]
  simp [List.append_assoc]

/-! ### Closure -/

/-- The boundary of `wordE k` closes, for every `k`: in the block form
`(ab)^{k+1} · (de)^{2k+2} · (ab)^{k+1}` the directions `a` and `b` collect
(by `wsum_rep_pair`) the total weights `2(k+1)(4k+5)` and `8(k+1)²`, which
are exactly cancelled by `d = −a` and `e = −b` — checked componentwise by
`ring`, with `k` symbolic. -/
theorem closes_wordE (k : ℕ) :
    ((unitSteps (perfectSides (wordE k))).map Dir.vec).sum = 0 := by
  rw [sum_map_vec_unitSteps_eq_wsum, wordE_length, wordE_eq]
  simp only [wsum_append, wsum_rep_pair,
    rep_length, List.length_append, List.length_cons, List.length_nil]
  simp only [Dir.vec, Prod.smul_mk, smul_eq_mul, Prod.ext_iff, Prod.fst_add,
    Prod.snd_add, Prod.fst_zero, Prod.snd_zero]
  push_cast
  refine ⟨by ring, by ring, by ring⟩

/-! ### The family theorems -/

/-- The infinite family: every `wordE k` encodes a perfect
`(8k + 8)`-polyiamond.  (Closure is `closes_wordE`; the positivity and
corner conditions are routine; simplicity is the open part, as for
`wordA`/`wordB` in `Lean4.Perfect12k`.)

N.B. these polyiamonds are perfect but *not* obtuse: each has exactly two
interior angles of `60°`, at the junctions `…ab·de…` and `…de·ab…` — see
`not_obtuse_wordE`. -/
theorem isPerfect_wordE (k : ℕ) : IsPerfectPolyiamond (wordE k) := by
  sorry

open Dir in
/-- No member of the family is a perfect *obtuse* polyiamond: at the block
junction `…ab·de…` the boundary turns by `+120°` (an interior angle of
`60°`), i.e. the letters `b, d` are cyclically adjacent in `wordE k` and
`ObtuseStep b d` fails.  (Proved for every `k`; note that the "cheap"
argument via `six_dvd_length_of_obtuse` would only cover `k ≢ 2 (mod 3)`.) -/
theorem not_obtuse_wordE (k : ℕ) : ¬ IsPerfectObtusePolyiamond (wordE k) := by
  intro h
  have h0 : List.IsChain ObtuseStep (wordE k ++ (wordE k).take 1) := h.obtuse
  have htake : (wordE k).take 1 = [a] := rfl
  have hsucc : 2 * k + 2 = 2 * k + 1 + 1 := by omega
  have hde : rep [d, e] (2 * k + 1 + 1) = [d, e] ++ rep [d, e] (2 * k + 1) := rfl
  rw [htake, wordE_eq, rep_pair_snoc, hsucc, hde] at h0
  -- Regroup so that the offending pair `b, d` is exposed as
  -- `l₁ ++ b :: d :: l₂`, then extract `ObtuseStep b d` and refute it.
  have key : List.IsChain ObtuseStep
      ((a :: rep [b, a] k) ++
        b :: d :: ((e :: rep [d, e] (2 * k + 1)) ++
          ((a :: (rep [b, a] k ++ [b])) ++ [a]))) := by
    simpa [List.append_assoc] using h0
  exact absurd (List.isChain_append_cons_cons.mp key).2.1 (by decide)

/-! ### Sanity checks -/

/-- The smallest member of the family, `abdedeab` (8 sides): a perfect
`8`-polyiamond, certified by the kernel via `decide` (the boundary visits
`8·9/2 = 36` pairwise distinct grid points before returning to the origin). -/
example : IsPerfectPolyiamond (wordE 0) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · decide  -- `3 ≤ 8`: at least three sides
  · decide  -- all sides have positive length
  · decide  -- consecutive sides meet in genuine vertices
  · decide  -- the boundary closes: the side vectors sum to `0`
  · decide +kernel  -- simplicity: the visited grid points are pairwise distinct

/-- …and it is not obtuse (two of its angles are `60°`), by computation —
the general statement is `not_obtuse_wordE`. -/
example : ¬ CyclicChain' ObtuseStep (wordE 0) := by decide

end Polyiamond
