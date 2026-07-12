/-
  Perfect polyiamonds: the `8k + 5` family and its area polynomial
  ================================================================

  The infinite family of boundary words

    `E(k) = ac · (bdfd)^k · edf · (afab)^k`

  over `Σ = {a, …, f}` (here `wordF k`, to avoid clashing with the `wordE`
  of `Lean4.Perfect8k_8`), of length `n = 8k + 5` (i.e. `n = 5, 13, 21, …`).
  For `k = 0` this is the word `acedf`, a perfect pentagon of area `19`.

  Every `wordF k` encodes a perfect `(8k + 5)`-polyiamond: the boundary
  closes (`closes_wordF`, proved for every `k` with `k` symbolic — the
  directions `a, b, c, d, e, f` collect the weights `4k² + 10k + 5`,
  `8k² + 4k`, `8k + 4`, `12k² + 10k + 2`, `4k + 3`, `8k² + 8k + 1`, whose
  vector sum cancels), and the `k = 0` instance is certified by `decide`.
  The full family theorem `isPerfect_wordF` (simplicity being the open
  part, as for the other families) is left as `sorry`.

  The area of these polyiamonds, measured in unit triangles (`area` in
  `Lean4.PerfectPolyiamonds`), is claimed to be the cubic polynomial

    `P(k) = 144k³ + 232k² + 124k + 19`

  (`area_wordF`, left as `sorry`); the instances `P(0) = 19` and
  `P(1) = 519` are certified by `decide`.
-/
import Lean4.PerfectPolyiamonds

namespace Polyiamond

/-! ### The words `E(k)` -/

open Dir in
/-- The `8k + 5` family (i.e. `n = 5, 13, 21, …`):
`E(k) = ac · (bdfd)^k · edf · (afab)^k`.
For `k = 0` this is `acedf` (see `wordF_zero`). -/
def wordF (k : ℕ) : List Dir :=
  [a, c] ++ rep [b, d, f, d] k ++ [e, d, f] ++ rep [a, f, a, b] k

open Dir in
/-- `wordF 0` spelled out: the word `acedf`. -/
lemma wordF_zero : wordF 0 = [a, c, e, d, f] := rfl

@[simp] lemma wordF_length (k : ℕ) : (wordF k).length = 8 * k + 5 := by
  simp only [wordF, List.length_append, rep_length, List.length_cons,
    List.length_nil]
  omega

/-! ### Closure -/

/-- The boundary of `wordF k` closes, for every `k`: the two periodic blocks
are evaluated by `wsum_rep_quad`, the joints `ac` and `edf` by `wsum_cons`,
and the resulting linear combination of the six direction vectors cancels —
checked componentwise by `ring`, with `k` symbolic. -/
theorem closes_wordF (k : ℕ) :
    ((unitSteps (perfectSides (wordF k))).map Dir.vec).sum = 0 := by
  rw [sum_map_vec_unitSteps_eq_wsum, wordF_length]
  simp only [wordF, wsum_append, wsum_rep_quad, wsum_cons, wsum_nil,
    rep_length, List.length_append, List.length_cons, List.length_nil]
  simp only [Dir.vec, Prod.smul_mk, smul_eq_mul, Prod.ext_iff, Prod.fst_add,
    Prod.snd_add, Prod.fst_zero, Prod.snd_zero]
  push_cast
  refine ⟨by ring, by ring, by ring⟩

/-! ### The family theorems -/

/-- The infinite family: every `wordF k` encodes a perfect
`(8k + 5)`-polyiamond.  (Closure is `closes_wordF`; the positivity and
corner conditions are routine; simplicity is the open part, as for the
families of `Lean4.Perfect12k` and `Lean4.Perfect8k_8`.) -/
theorem isPerfect_wordF (k : ℕ) : IsPerfectPolyiamond (wordF k) := by
  sorry

/-- **The area polynomial**: the area of the perfect polyiamond `wordF k`,
measured in unit triangles, is the cubic polynomial
`P(k) = 144k³ + 232k² + 124k + 19`.  (The instances `k = 0` and `k = 1`
are certified by `decide` below.) -/
theorem area_wordF (k : ℕ) :
    area (perfectSides (wordF k))
      = 144 * (k : ℤ) ^ 3 + 232 * (k : ℤ) ^ 2 + 124 * (k : ℤ) + 19 := by
  sorry

/-! ### Sanity checks -/

/-- The smallest member of the family, `acedf` (5 sides): a perfect
`5`-polyiamond, certified by the kernel via `decide`. -/
example : IsPerfectPolyiamond (wordF 0) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · decide  -- `3 ≤ 5`: at least three sides
  · decide  -- all sides have positive length
  · decide  -- consecutive sides meet in genuine vertices
  · decide  -- the boundary closes: the side vectors sum to `0`
  · decide +kernel  -- simplicity: the visited grid points are pairwise distinct

/-- `P(0) = 19`: the pentagon `acedf` encloses `19` unit triangles. -/
example : area (perfectSides (wordF 0)) = 19 := by decide

/-- `P(1) = 144 + 232 + 124 + 19 = 519`: the `13`-gon `acbdfdedfafab`
encloses `519` unit triangles. -/
example : area (perfectSides (wordF 1)) = 519 := by decide +kernel

end Polyiamond
