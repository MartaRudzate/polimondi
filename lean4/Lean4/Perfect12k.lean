/-
  Perfect obtuse polyiamonds: the two `12k`-families
  ==================================================

  The sufficient condition for the existence of perfect obtuse polyiamonds
  ("serial isogons with 120-degree angles"): two explicit infinite families
  of boundary words,

  * `wordA k` of length `n = 12k + 12` (i.e. `n = 12, 24, 36, …`), and
  * `wordB k` of length `n = 12k + 18` (i.e. `n = 18, 30, 42, …`),

  the two arithmetic progressions of the source (`Apgalvojums` in
  `kursadarbs.tex`).  Together they cover every `n ≥ 12` divisible by `6`,
  which with the necessity theorems of `Lean4.PerfectPolyiamonds` gives the
  full characterization `exists_obtuse_iff`.

  Proved so far: the closure of both families for every `k` (via the
  `wsum`/`rep` machinery of `Lean4.PerfectPolyiamonds`), and the concrete
  instance of the smallest `12`-gon `abcdedefafab`, certified by `decide`.
  The full family theorems (simplicity being the open part) and the
  characterization are still left as `sorry`.
-/
import Lean4.PerfectPolyiamonds

namespace Polyiamond

open Dir in
/-- The first family, `n = 12k + 12` (i.e. `n = 12, 24, 36, …`):
`(ab)^k · abc · (de)^k · de · (dc)^k · de · (fa)^k · fa · (fe)^k · fa · (bc)^k · b`.
For `k = 0` this is `abcdedefafab`, the unique smallest serial `120°` isogon. -/
def wordA (k : ℕ) : List Dir :=
  rep [a, b] k ++ [a, b, c] ++
  rep [d, e] k ++ [d, e] ++
  rep [d, c] k ++ [d, e] ++
  rep [f, a] k ++ [f, a] ++
  rep [f, e] k ++ [f, a] ++
  rep [b, c] k ++ [b]

open Dir in
/-- The second family, `n = 12k + 18` (i.e. `n = 18, 30, 42, …`):
`(ab)^k · abaf · (ed)^k · eded · (ef)^k · ed · (cb)^k · cbcb · (cd)^k · cb · (af)^k · ab`. -/
def wordB (k : ℕ) : List Dir :=
  rep [a, b] k ++ [a, b, a, f] ++
  rep [e, d] k ++ [e, d, e, d] ++
  rep [e, f] k ++ [e, d] ++
  rep [c, b] k ++ [c, b, c, b] ++
  rep [c, d] k ++ [c, b] ++
  rep [a, f] k ++ [a, b]

@[simp] lemma wordA_length (k : ℕ) : (wordA k).length = 12 * k + 12 := by
  simp only [wordA, List.length_append, rep_length, List.length_cons,
    List.length_nil]
  omega

@[simp] lemma wordB_length (k : ℕ) : (wordB k).length = 12 * k + 18 := by
  simp only [wordB, List.length_append, rep_length, List.length_cons,
    List.length_nil]
  omega

/-- The boundary of `wordA k` closes, for every `k`: the word splits into six
`rep`-segments and six short joints, each evaluated by `wsum_append` /
`wsum_rep_pair`, and the resulting linear combination of the six direction
vectors cancels — checked componentwise by `ring`, with `k` symbolic. -/
theorem closes_wordA (k : ℕ) :
    ((unitSteps (perfectSides (wordA k))).map Dir.vec).sum = 0 := by
  rw [sum_map_vec_unitSteps_eq_wsum, wordA_length]
  simp only [wordA, wsum_append, wsum_rep_pair, wsum_cons, wsum_nil,
    rep_length, List.length_append, List.length_cons, List.length_nil]
  simp only [Dir.vec, Prod.smul_mk, smul_eq_mul, Prod.ext_iff, Prod.fst_add,
    Prod.snd_add, Prod.fst_zero, Prod.snd_zero]
  push_cast
  refine ⟨by ring, by ring, by ring⟩

/-- The boundary of `wordB k` closes, for every `k` (same method as
`closes_wordA`). -/
theorem closes_wordB (k : ℕ) :
    ((unitSteps (perfectSides (wordB k))).map Dir.vec).sum = 0 := by
  rw [sum_map_vec_unitSteps_eq_wsum, wordB_length]
  simp only [wordB, wsum_append, wsum_rep_pair, wsum_cons, wsum_nil,
    rep_length, List.length_append, List.length_cons, List.length_nil]
  simp only [Dir.vec, Prod.smul_mk, smul_eq_mul, Prod.ext_iff, Prod.fst_add,
    Prod.snd_add, Prod.fst_zero, Prod.snd_zero]
  push_cast
  refine ⟨by ring, by ring, by ring⟩

/-- The first infinite family: every `wordA k` encodes a perfect obtuse
`(12k + 12)`-polyiamond.  (Closure is `closes_wordA`; the positivity, corner
and obtuse-turn conditions are routine; simplicity is the open part.) -/
theorem isPerfectObtuse_wordA (k : ℕ) : IsPerfectObtusePolyiamond (wordA k) := by
  sorry

/-- The second infinite family: every `wordB k` encodes a perfect obtuse
`(12k + 18)`-polyiamond.  (Closure is `closes_wordB`.) -/
theorem isPerfectObtuse_wordB (k : ℕ) : IsPerfectObtusePolyiamond (wordB k) := by
  sorry

/-- **Sufficiency**: for every `n ≥ 12` divisible by `6` there is a perfect
obtuse `n`-polyiamond.  (From the two families: if `n ≡ 0 (mod 12)` then
`n = 12k + 12` for some `k`, and if `n ≡ 6 (mod 12)` with `n ≥ 12` then
`n ≥ 18`, so `n = 12k + 18` for some `k`.) -/
theorem exists_obtuse_of_six_dvd {n : ℕ} (h₆ : 6 ∣ n) (h₁₂ : 12 ≤ n) :
    ∃ w : List Dir, w.length = n ∧ IsPerfectObtusePolyiamond w := by
  sorry

/-- **Full characterization**: a perfect obtuse `n`-polyiamond exists *iff*
`6 ∣ n` and `12 ≤ n`.  (The forward direction combines
`six_dvd_of_exists_obtuse`, `not_exists_obtuse_six`, and `IsPolyiamond.three_le`
which rules out `n = 0`.) -/
theorem exists_obtuse_iff (n : ℕ) :
    (∃ w : List Dir, w.length = n ∧ IsPerfectObtusePolyiamond w) ↔
      6 ∣ n ∧ 12 ≤ n := by
  sorry

/-! ### Sanity checks

Larger instances can be explored with

* `#eval decide (IsPerfectObtusePolyiamond (wordA 2))`
* `#eval trace (perfectSides (wordA 0))`   -- the 78 boundary points + origin
-/

open Dir in
/-- `wordA 0` spelled out: the word `abcdedefafab`. -/
lemma wordA_zero : wordA 0 = [a, b, c, d, e, d, e, f, a, f, a, b] := rfl

/-- The smallest perfect obtuse polyiamond, `abcdedefafab` (12 sides).
Each field is a finite check, certified by the kernel via `decide`:
the word `abcdedefafab` (see `wordA_zero`) has 12 letters, all
cyclically consecutive letters differ by one step of `±60°` rotation,
the weighted direction vectors sum to `0`, and the `78` boundary points
(a 12-gon with sides `12, 11, …, 1`) are pairwise distinct. -/
example : IsPerfectObtusePolyiamond (wordA 0) := by
  refine ⟨⟨?_, ?_, ?_, ?_, ?_⟩, ?_⟩
  · decide  -- `3 ≤ 12`: at least three sides
  · decide  -- all sides have positive length
  · decide  -- consecutive sides meet in genuine vertices
  · decide  -- the boundary closes: the side vectors sum to `0`
  · decide +kernel  -- simplicity: the visited grid points are pairwise distinct
  · decide  -- every turn is `±60°`, i.e. every angle is `120°` or `240°`

end Polyiamond
