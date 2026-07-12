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
  `Lean4.PerfectPolyiamonds`), is the cubic polynomial

    `P(k) = 144k³ + 232k² + 124k + 19`

  (`area_wordF`, proved for every `k` with `k` symbolic: the `csum` shoelace
  machinery of `Lean4.PerfectPolyiamonds` splits the boundary along the four
  blocks of `wordF`, the periodic blocks get polynomial closed forms
  `csum_rep_bdfd`/`csum_rep_afab` by induction on `k`, and the pieces sum to
  `−P(k)`, the boundary being traced clockwise); the instances `P(0) = 19`
  and `P(1) = 519` are also certified by `decide`.
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

/-! ### The area polynomial

The area is computed by the `csum` machinery of `Lean4.PerfectPolyiamonds`:
`shoelace_trace_perfectSides` turns `area` into the weighted shoelace sum
`csum n 0 (wordF k)` with `n = 8k + 5`, `csum_append` splits it along the
four blocks of `wordF`, and the two periodic blocks are evaluated by the
closed forms below (proved by induction on `k`, with `n` and the starting
point `p` symbolic; the induction step peels one period off the front and
closes with `ring`). -/

open Dir in
/-- Closed form of the shoelace sum along the block `(bdfd)^k`, with the
start weight `n` and the start point `p` symbolic. -/
lemma csum_rep_bdfd (k : ℕ) (n : ℤ) (p : Pt) :
    csum n p (rep [b, d, f, d] k)
      = -4 * (k : ℤ) ^ 3 + 4 * (k : ℤ) ^ 2 * n + 8 * (k : ℤ) ^ 2
          - (k : ℤ) * n ^ 2 - 4 * (k : ℤ) * n - 2 * (k : ℤ) * p.1
          + (-2 * (k : ℤ) ^ 2 + (k : ℤ) * n - 2 * (k : ℤ)) * p.2.1 := by
  induction k generalizing n p with
  | zero => norm_num [rep]
  | succ k ih =>
    simp only [rep]
    rw [csum_append, ih]
    simp only [csum_cons, csum_nil, wsum_cons, wsum_nil, List.length_cons,
      List.length_nil, Dir.vec, cross, Prod.smul_mk, smul_eq_mul,
      Prod.mk_add_mk, Prod.fst_add, Prod.snd_add, Prod.fst_zero, Prod.snd_zero,
      add_zero, zero_add]
    push_cast
    ring

open Dir in
/-- Closed form of the shoelace sum along the block `(afab)^k`, with the
start weight `n` and the start point `p` symbolic. -/
lemma csum_rep_afab (k : ℕ) (n : ℤ) (p : Pt) :
    csum n p (rep [a, f, a, b] k)
      = -12 * (k : ℤ) ^ 3 + 12 * (k : ℤ) ^ 2 * n - 4 * (k : ℤ) ^ 2
          - 3 * (k : ℤ) * n ^ 2 + 2 * (k : ℤ) * n + 5 * (k : ℤ)
          + 2 * (k : ℤ) * p.1
          + (6 * (k : ℤ) ^ 2 - 3 * (k : ℤ) * n - (k : ℤ)) * p.2.1 := by
  induction k generalizing n p with
  | zero => norm_num [rep]
  | succ k ih =>
    simp only [rep]
    rw [csum_append, ih]
    simp only [csum_cons, csum_nil, wsum_cons, wsum_nil, List.length_cons,
      List.length_nil, Dir.vec, cross, Prod.smul_mk, smul_eq_mul,
      Prod.mk_add_mk, Prod.fst_add, Prod.snd_add, Prod.fst_zero, Prod.snd_zero,
      add_zero, zero_add]
    push_cast
    ring

/-- **The area polynomial**: the area of the perfect polyiamond `wordF k`,
measured in unit triangles, is the cubic polynomial
`P(k) = 144k³ + 232k² + 124k + 19`, for every `k`.  The boundary is traced
clockwise, so its shoelace sum is `−P(k)`; the area is `|−P(k)| = P(k)`. -/
theorem area_wordF (k : ℕ) :
    area (perfectSides (wordF k))
      = 144 * (k : ℤ) ^ 3 + 232 * (k : ℤ) ^ 2 + 124 * (k : ℤ) + 19 := by
  have hs : shoelace (trace (perfectSides (wordF k)))
      = -(144 * (k : ℤ) ^ 3 + 232 * (k : ℤ) ^ 2 + 124 * (k : ℤ) + 19) := by
    rw [shoelace_trace_perfectSides, wordF_length]
    simp only [wordF, csum_append, csum_rep_bdfd, csum_rep_afab, csum_cons,
      csum_nil, wsum_append, wsum_rep_quad, wsum_cons, wsum_nil, rep_length,
      List.length_append, List.length_cons, List.length_nil, Dir.vec, cross,
      Prod.smul_mk, smul_eq_mul, Prod.mk_add_mk, Prod.fst_add, Prod.snd_add,
      Prod.fst_zero, Prod.snd_zero, add_zero, zero_add]
    push_cast
    ring
  have hP : (0 : ℤ)
      ≤ 144 * (k : ℤ) ^ 3 + 232 * (k : ℤ) ^ 2 + 124 * (k : ℤ) + 19 := by
    positivity
  rw [area, hs, abs_neg, abs_of_nonneg hP]

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
