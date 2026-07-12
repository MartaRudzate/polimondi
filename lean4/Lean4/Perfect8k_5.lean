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
  The family theorem `isPerfect_wordF` is assembled from `closes_wordF`,
  the positivity of the side lengths (`pos_perfectSides`), the cyclic
  corner condition (`cyclicChain_dirStep_wordF`, proved for every `k` by
  induction over the periodic blocks), and the simplicity of the boundary —
  the one remaining open condition, isolated as `nodup_trace_wordF`
  (`sorry`, with a documented geometric proof plan).  From it,
  `exists_isPerfectPolyiamond_of_mod_eight` derives a perfect
  `n`-polyiamond for every `n ≡ 5 (mod 8)`.

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

/-! ### The corner condition -/

open Dir in
/-- Chains through the block `(bdfd)^k`: whenever `e :: l` is a
`DirStep`-chain and `x` may precede both `b` and `e`, the word
`x · (bdfd)^k · e · l` is a `DirStep`-chain.  (The quantifier over `x` feeds
the induction: inside the block each period is preceded by the letter `d`.) -/
lemma isChain_dirStep_rep_bdfd (k : ℕ) {l : List Dir}
    (h : List.IsChain DirStep (e :: l)) :
    ∀ x : Dir, DirStep x b → DirStep x e →
      List.IsChain DirStep (x :: (rep [b, d, f, d] k ++ e :: l)) := by
  induction k with
  | zero =>
    intro x _ hxe
    simpa [rep] using List.isChain_cons_cons.mpr ⟨hxe, h⟩
  | succ k ih =>
    intro x hxb _
    simp only [rep, List.cons_append, List.nil_append, List.append_assoc]
    refine List.isChain_cons_cons.mpr ⟨hxb, ?_⟩
    refine List.isChain_cons_cons.mpr ⟨by decide, ?_⟩
    refine List.isChain_cons_cons.mpr ⟨by decide, ?_⟩
    refine List.isChain_cons_cons.mpr ⟨by decide, ?_⟩
    exact ih d (by decide) (by decide)

open Dir in
/-- Chains through the block `(afab)^k`: whenever `a :: l` is a
`DirStep`-chain and `x` may precede `a`, the word `x · (afab)^k · a · l` is a
`DirStep`-chain.  (Inside the block each period is preceded by `b`.) -/
lemma isChain_dirStep_rep_afab (k : ℕ) {l : List Dir}
    (h : List.IsChain DirStep (a :: l)) :
    ∀ x : Dir, DirStep x a →
      List.IsChain DirStep (x :: (rep [a, f, a, b] k ++ a :: l)) := by
  induction k with
  | zero =>
    intro x hxa
    simpa [rep] using List.isChain_cons_cons.mpr ⟨hxa, h⟩
  | succ k ih =>
    intro x hxa
    simp only [rep, List.cons_append, List.nil_append, List.append_assoc]
    refine List.isChain_cons_cons.mpr ⟨hxa, ?_⟩
    refine List.isChain_cons_cons.mpr ⟨by decide, ?_⟩
    refine List.isChain_cons_cons.mpr ⟨by decide, ?_⟩
    refine List.isChain_cons_cons.mpr ⟨by decide, ?_⟩
    exact ih b (by decide)

open Dir in
/-- The corner condition of `wordF k`, at the level of the direction word:
cyclically consecutive letters never repeat and never reverse. -/
lemma cyclicChain_dirStep_wordF (k : ℕ) : CyclicChain' DirStep (wordF k) := by
  have htake : (wordF k).take 1 = [a] := rfl
  unfold CyclicChain'
  rw [htake]
  simp only [wordF, List.append_assoc, List.cons_append, List.nil_append]
  refine List.isChain_cons_cons.mpr ⟨by decide, ?_⟩
  refine isChain_dirStep_rep_bdfd k ?_ c (by decide) (by decide)
  refine List.isChain_cons_cons.mpr ⟨by decide, ?_⟩
  refine List.isChain_cons_cons.mpr ⟨by decide, ?_⟩
  exact isChain_dirStep_rep_afab k (List.isChain_singleton a) f (by decide)

/-! ### The family theorems -/

/-- Simplicity of the family boundary (the one open condition): the walk
along `perfectSides (wordF k)` visits no grid point twice.

Geometric picture (planar coordinates `(x, y) := (p.1, p.2.1)`, `n = 8k+5`):
the boundary consists of five chains —
* side `a` of length `n` along `y = 0`, `0 ≤ x ≤ n`;
* side `c` down the right edge `x = n`, `-(n−1) ≤ y ≤ 0`;
* the comb `(bdfd)^k`: `k` downward teeth in the band `-16k−7 ≤ y ≤ -8k−4`,
  tooth `j` lying between the diagonals `x + y = u_{j+1}` and `x + y = u_j`,
  where `u_j` is strictly decreasing in `j` with gaps `≥ 4k+1` (adjacent
  teeth overlap only in a width-2 diagonal strip, where they are separated
  by `y`);
* the connector `edf` with `x ≤ -6k²+3k+2`, `-10k−4 ≤ y ≤ -2k`;
* the comb `(afab)^k` in the band `-2k ≤ y ≤ 2k−1`, with `x < 0` except at
  its final point `(0,0)` (the closing vertex, dropped by `dropLast`);
  along this chain `(x + y, x)` increases lexicographically at every unit
  step, which yields its simplicity at once.
The five chains lie in pairwise disjoint regions (up to the junction
vertices, each visited once), and each chain is itself simple.  A
formalization can split the walk into the five chunks, prove per-chain
`Nodup` and region containment by induction on the number of periods
(tracking positions by recursively defined coordinates, so that every
induction step is linear integer arithmetic), and discharge the pairwise
region checks; this remains to be done. -/
theorem nodup_trace_wordF (k : ℕ) :
    (trace (perfectSides (wordF k))).dropLast.Nodup := by
  sorry

/-- The infinite family: every `wordF k` encodes a perfect
`(8k + 5)`-polyiamond.  Closure is `closes_wordF`, positivity of the side
lengths is `pos_perfectSides`, the corner condition is
`cyclicChain_dirStep_wordF` (via the transfer lemma
`cyclicChain_cornerStep_iff`), and simplicity is `nodup_trace_wordF` —
the one remaining `sorry`. -/
theorem isPerfect_wordF (k : ℕ) : IsPerfectPolyiamond (wordF k) := by
  refine ⟨?_, pos_perfectSides _, ?_, closes_wordF k, nodup_trace_wordF k⟩
  · rw [perfectSides_length, wordF_length]; omega
  · exact (cyclicChain_cornerStep_iff _).mpr (cyclicChain_dirStep_wordF k)

/-- **Existence**: for every `n ≡ 5 (mod 8)` there is a perfect
`n`-polyiamond, namely `wordF (n / 8)`.  (With `n = 5` the smallest length
for which perfect polyiamonds exist at all.) -/
theorem exists_isPerfectPolyiamond_of_mod_eight {n : ℕ} (h : n % 8 = 5) :
    ∃ w : List Dir, w.length = n ∧ IsPerfectPolyiamond w :=
  ⟨wordF (n / 8), by rw [wordF_length]; omega, isPerfect_wordF _⟩

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
