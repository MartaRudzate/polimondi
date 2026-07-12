/-
  Perfect polyiamonds on the triangular grid
  ==========================================

  A Lean 4 / Mathlib formalization of the definitions of polyiamonds,
  perfect polyiamonds and perfect obtuse/acute polyiamonds, and of the
  statements

  * (necessity)   a perfect obtuse `n`-polyiamond exists → `6 ∣ n`;
  * (sufficiency) `6 ∣ n` and `12 ≤ n` → a perfect obtuse `n`-polyiamond exists,

  following `kombinatorikas_uzdevums.pdf` and `perfect_polyiamonds2024.tex`
  (K. Apsītis, M. Rudzāte).  Perfect obtuse polyiamonds are the
  "serial isogons with 120-degree angles" of
  Sallows–Gardner–Guy–Knuth, *Serial isogons of 90 degrees*,
  Math. Mag. 64 (1991) 315–324.

  Design notes
  ------------
  Mathlib currently has no library for polyforms, lattice polygons, or simple
  polygons (there is no polygonal Jordan curve theorem, and `Polytope`/convexity
  files do not apply to non-convex boundaries).  We therefore formalize a
  polyiamond through its *boundary word*, which is also the point of view taken
  in the source texts ("perfect polyiamonds as formal languages"):

  * a candidate boundary is a cyclic list of sides `(length, direction)`,
    where the six unit directions `a…f` of the triangular grid are written in
    the cube coordinates `{(x, y, z) ∈ ℤ³ ∣ x + y + z = 0}` of the source:
    `a = (1,0,−1)`, `b = (1,−1,0)`, `c = (0,−1,1)`, `d = −a`, `e = −b`, `f = −c`;

  * "simple polygon" becomes: the lattice points visited by the unit-step walk
    along the boundary are pairwise distinct (except for the final return to
    the starting point).  This is equivalent to geometric simplicity because
    on the triangular grid any two grid lines of different directions meet in
    a lattice point, unit segments contain no lattice points in their
    interiors, and hence two distinct unit grid segments intersect in at most
    one common lattice point;

  * "all interior angles are `120°` or `240°`" becomes: cyclically consecutive
    side directions differ by exactly one step of `±60°` rotation
    (for a counterclockwise traversal a `+60°` turn is an interior angle of
    `120°` and a `−60°` turn is `240°`; a clockwise traversal swaps the two
    interpretations, so the predicate is orientation-independent).
    Likewise `60°/300°` becomes a `±120°` rotation.

  This file contains the *general* definitions and the family-independent
  results (the weighted-sum form of the closure condition, the `wsum`/`rep`
  machinery for evaluating boundary sums of periodic words, the necessity
  theorems — still `sorry` — and the `n = 6` non-existence).  The explicit
  infinite families live in separate files that import this one:

  * `Lean4.Perfect12k`   — the perfect *obtuse* families `wordA k`
    (`n = 12k + 12`) and `wordB k` (`n = 12k + 18`), and the sufficiency /
    characterization statements built from them;
  * `Lean4.Perfect8k_8`  — the perfect (but *not* obtuse: it has two `60°`
    angles) family `wordE k` (`n = 8k + 8`),
    `E(k) = ab(ab)^k dede(dede)^k ab(ab)^k`;
  * `Lean4.Perfect8k_5`  — the perfect family `wordF k` (`n = 8k + 5`),
    `E(k) = ac(bdfd)^k edf(afab)^k`, together with the claim that its area
    in unit triangles is the cubic polynomial `144k³ + 232k² + 124k + 19`.
-/
import Mathlib

namespace Polyiamond

/-- A lattice point of the triangular grid, in cube coordinates.
(Every point reachable from the origin satisfies `x + y + z = 0`; we do not
bake this invariant into the type — it is provable for all traced vertices.) -/
abbrev Pt : Type := ℤ × ℤ × ℤ

/-! ### Directions -/

/-- The six unit directions of the triangular grid, in counterclockwise order
(each successive direction is the previous one rotated by `+60°`). -/
inductive Dir : Type
  | a | b | c | d | e | f
  deriving DecidableEq, Repr, Fintype

namespace Dir

/-- Cube coordinates of the unit directions:
`a = (1,0,−1)`, `b = (1,−1,0)`, `c = (0,−1,1)`, `d = −a`, `e = −b`, `f = −c`. -/
def vec : Dir → Pt
  | .a => (1, 0, -1)
  | .b => (1, -1, 0)
  | .c => (0, -1, 1)
  | .d => (-1, 0, 1)
  | .e => (-1, 1, 0)
  | .f => (0, 1, -1)

/-- Rotation by `+60°` (counterclockwise): `a ↦ b ↦ c ↦ d ↦ e ↦ f ↦ a`. -/
def rotCCW : Dir → Dir
  | .a => .b | .b => .c | .c => .d | .d => .e | .e => .f | .f => .a

/-- Rotation by `−60°` (clockwise). -/
def rotCW : Dir → Dir
  | .a => .f | .b => .a | .c => .b | .d => .c | .e => .d | .f => .e

/-- The opposite direction (rotation by `180°`). -/
def opp : Dir → Dir
  | .a => .d | .b => .e | .c => .f | .d => .a | .e => .b | .f => .c

@[simp] lemma vec_opp (d : Dir) : d.opp.vec = -d.vec := by
  cases d <;> decide

@[simp] lemma rotCW_rotCCW (d : Dir) : d.rotCCW.rotCW = d := by cases d <;> rfl

@[simp] lemma rotCCW_rotCW (d : Dir) : d.rotCW.rotCCW = d := by cases d <;> rfl

end Dir

/-! ### Boundaries of grid polygons -/

/-- A candidate polygon boundary: the cyclic list of its sides, each given by a
length and a grid direction (the last side is cyclically followed by the first). -/
abbrev Sides : Type := List (ℕ × Dir)

/-- The boundary as a sequence of unit steps: a side `(ℓ, d)` contributes
`ℓ` consecutive copies of `d`. -/
def unitSteps : Sides → List Dir
  | [] => []
  | (ℓ, d) :: s => List.replicate ℓ d ++ unitSteps s

/-- All grid points visited while tracing the boundary from the origin, one
unit step at a time.  The origin comes first; for a closed boundary the final
entry is the origin again. -/
def trace (s : Sides) : List Pt :=
  (unitSteps s).scanl (fun p d => p + d.vec) (0 : Pt)

/-- `CyclicChain' R l`: the relation `R` holds between all *cyclically*
consecutive entries of `l` (including between the last and the first). -/
def CyclicChain' {α : Type*} (R : α → α → Prop) (l : List α) : Prop :=
  List.IsChain R (l ++ l.take 1)

instance {α : Type*} (R : α → α → Prop) [DecidableRel R] (l : List α) :
    Decidable (CyclicChain' R l) :=
  inferInstanceAs (Decidable (List.IsChain R (l ++ l.take 1)))

/-- Two cyclically consecutive sides make a genuine polygon vertex: the
direction changes, and does not simply reverse.  (Reversal is in fact already
excluded by simplicity of the boundary; it is included here so that the
polygon notion is self-contained.) -/
def CornerStep (p q : ℕ × Dir) : Prop := q.2 ≠ p.2 ∧ q.2 ≠ p.2.opp

instance : DecidableRel CornerStep := fun p q =>
  inferInstanceAs (Decidable (q.2 ≠ p.2 ∧ q.2 ≠ p.2.opp))

/-- The word-level corner condition: the next direction differs from the
previous one and is not its opposite (`CornerStep` on the directions alone). -/
def DirStep (p q : Dir) : Prop := q ≠ p ∧ q ≠ p.opp

instance : DecidableRel DirStep := fun p q =>
  inferInstanceAs (Decidable (q ≠ p ∧ q ≠ p.opp))

/-- `IsPolyiamond s`: the side list `s` traces the boundary of a polyiamond,
i.e. of a simple polygon whose sides run along the triangular grid.
(The region bounded by such a curve is automatically a union of unit
triangles, so this matches the "figure made of unit triangles" definition.) -/
structure IsPolyiamond (s : Sides) : Prop where
  /-- A polygon has at least three sides. -/
  three_le : 3 ≤ s.length
  /-- Every side has positive length. -/
  pos : ∀ p ∈ s, 0 < p.1
  /-- Cyclically consecutive sides meet in genuine vertices. -/
  corner : CyclicChain' CornerStep s
  /-- The boundary returns to its starting point. -/
  closes : ((unitSteps s).map Dir.vec).sum = 0
  /-- Simplicity: the visited grid points are pairwise distinct, the final
  return to the origin excepted.  On the triangular grid this is equivalent
  to the polygon being simple (see the design notes in the file header). -/
  simple : (trace s).dropLast.Nodup

instance (s : Sides) : Decidable (IsPolyiamond s) :=
  decidable_of_iff
    (3 ≤ s.length ∧ (∀ p ∈ s, 0 < p.1) ∧ CyclicChain' CornerStep s ∧
      ((unitSteps s).map Dir.vec).sum = 0 ∧ (trace s).dropLast.Nodup)
    ⟨fun ⟨h1, h2, h3, h4, h5⟩ => ⟨h1, h2, h3, h4, h5⟩,
     fun ⟨h1, h2, h3, h4, h5⟩ => ⟨h1, h2, h3, h4, h5⟩⟩

/-! ### Perfect polyiamonds

A perfect `n`-polyiamond has sides of lengths `n, n−1, …, 1` *in this order*,
so it is determined by the word `w ∈ {a,…,f}*` of its side directions:
the `i`-th letter (0-indexed) is the direction of the side of length `n − i`,
where `n = w.length`. -/

/-- The side list of the perfect polyiamond encoded by the direction word `w`. -/
def perfectSides : List Dir → Sides
  | [] => []
  | d :: w => (w.length + 1, d) :: perfectSides w

@[simp] lemma perfectSides_length (w : List Dir) :
    (perfectSides w).length = w.length := by
  induction w with
  | nil => rfl
  | cons d w ih => simp [perfectSides, ih]

/-- `w` encodes a perfect `n`-polyiamond (`n = w.length`). -/
def IsPerfectPolyiamond (w : List Dir) : Prop :=
  IsPolyiamond (perfectSides w)

instance (w : List Dir) : Decidable (IsPerfectPolyiamond w) :=
  inferInstanceAs (Decidable (IsPolyiamond (perfectSides w)))

/-- Every side of a perfect polyiamond has positive length. -/
lemma pos_perfectSides (w : List Dir) : ∀ p ∈ perfectSides w, 0 < p.1 := by
  induction w with
  | nil => simp [perfectSides]
  | cons d w ih =>
    intro p hp
    simp only [perfectSides, List.mem_cons] at hp
    rcases hp with h | h
    · subst h; simp
    · exact ih p h

lemma map_snd_perfectSides (w : List Dir) : (perfectSides w).map Prod.snd = w := by
  induction w with
  | nil => rfl
  | cons d w ih => simp [perfectSides, ih]

/-- The corner condition of a perfect polyiamond depends only on its
direction word. -/
lemma cyclicChain_cornerStep_iff (w : List Dir) :
    CyclicChain' CornerStep (perfectSides w) ↔ CyclicChain' DirStep w := by
  unfold CyclicChain'
  conv_rhs => rw [← map_snd_perfectSides w]
  rw [← List.map_take, ← List.map_append, List.isChain_map]
  rfl

/-- The unit-step form of the boundary vector sum of a perfect polyiamond
equals its weighted form: side `i` (of length `n − i`, where `n = w.length`)
contributes `(n − i) • vec wᵢ`. -/
lemma sum_unitSteps_perfectSides (w : List Dir) :
    ((unitSteps (perfectSides w)).map Dir.vec).sum =
      ∑ i : Fin w.length, (w.length - i.val) • (w.get i).vec := by
  induction w with
  | nil => simp [perfectSides, unitSteps]
  | cons d w ih => simp [perfectSides, unitSteps, Fin.sum_univ_succ, ih]

/-- The closure condition of a perfect polyiamond in the weighted-sum form
used in the source text: `∑_{i<n} (n − i) · vec wᵢ = 0`
(the `i`-th letter carries the side length `n − i`; reading the word from its
short end instead gives the equivalent form `∑ (i+1) · vec (w.reverse)ᵢ = 0`). -/
theorem isPerfect_closes_iff_weightedSum (w : List Dir) :
    ((unitSteps (perfectSides w)).map Dir.vec).sum = 0 ↔
      ∑ i : Fin w.length, ((w.length : ℤ) - (i.val : ℤ)) • (w.get i).vec = 0 := by
  have h : ∀ i : Fin w.length, ((w.length : ℤ) - (i.val : ℤ)) • (w.get i).vec
      = (w.length - i.val) • (w.get i).vec := fun i => by
    rw [← natCast_zsmul]
    congr 1
    have := i.isLt
    omega
  rw [sum_unitSteps_perfectSides, Finset.sum_congr rfl fun i _ => h i]

/-! #### Weighted vector sums

`wsum` is the workhorse for closure computations: it evaluates the boundary
vector sum of consecutive sides of lengths `n, n − 1, …` side by side, so that
sums over subwords compose (`wsum_append`) and sums over periodic subwords
have arithmetic-progression closed forms (`wsum_rep_pair` below). -/

/-- `wsum n w` is the boundary vector sum of consecutive sides of lengths
`n, n − 1, …` in directions `w₀, w₁, …`, i.e.
`n • vec w₀ + (n − 1) • vec w₁ + ⋯`.  The weight is an integer so that sums
of subwords can be manipulated without truncated subtraction. -/
def wsum : ℤ → List Dir → Pt
  | _, [] => 0
  | n, d :: w => n • d.vec + wsum (n - 1) w

@[simp] lemma wsum_nil (n : ℤ) : wsum n [] = 0 := rfl

@[simp] lemma wsum_cons (n : ℤ) (d : Dir) (w : List Dir) :
    wsum n (d :: w) = n • d.vec + wsum (n - 1) w := rfl

lemma wsum_append (u v : List Dir) (n : ℤ) :
    wsum n (u ++ v) = wsum n u + wsum (n - u.length) v := by
  induction u generalizing n with
  | nil => simp
  | cons d u ih =>
    have h : n - 1 - (u.length : ℤ) = n - ((u.length : ℤ) + 1) := by ring
    simp [ih, h, add_assoc]

/-- The unit-step boundary sum of a perfect polyiamond in `wsum` form. -/
lemma sum_map_vec_unitSteps_eq_wsum (w : List Dir) :
    ((unitSteps (perfectSides w)).map Dir.vec).sum = wsum w.length w := by
  induction w with
  | nil => simp [perfectSides, unitSteps]
  | cons d w ih => simp [perfectSides, unitSteps, ih, ← natCast_zsmul]

/-! ### Angle conditions -/

/-- One *obtuse* step: the next side direction is obtained from the previous
one by a `±60°` rotation — the combinatorial form of "the interior angle at
this vertex is `120°` or `240°`". -/
def ObtuseStep (p q : Dir) : Prop := q = p.rotCCW ∨ q = p.rotCW

/-- One *acute* step: a `±120°` rotation — interior angle `60°` or `300°`. -/
def AcuteStep (p q : Dir) : Prop := q = p.rotCCW.rotCCW ∨ q = p.rotCW.rotCW

instance : DecidableRel ObtuseStep := fun p q =>
  inferInstanceAs (Decidable (q = p.rotCCW ∨ q = p.rotCW))

instance : DecidableRel AcuteStep := fun p q =>
  inferInstanceAs (Decidable (q = p.rotCCW.rotCCW ∨ q = p.rotCW.rotCW))

/-- Perfect *obtuse* polyiamond — all interior angles `120°` or `240°`
(a "serial isogon with 120-degree angles"). -/
structure IsPerfectObtusePolyiamond (w : List Dir) : Prop where
  perfect : IsPerfectPolyiamond w
  obtuse : CyclicChain' ObtuseStep w

/-- Perfect *acute* polyiamond — all interior angles `60°` or `300°`
(a "serial isogon with 60-degree angles"). -/
structure IsPerfectAcutePolyiamond (w : List Dir) : Prop where
  perfect : IsPerfectPolyiamond w
  acute : CyclicChain' AcuteStep w

instance (w : List Dir) : Decidable (IsPerfectObtusePolyiamond w) :=
  decidable_of_iff (IsPerfectPolyiamond w ∧ CyclicChain' ObtuseStep w)
    ⟨fun ⟨h1, h2⟩ => ⟨h1, h2⟩, fun ⟨h1, h2⟩ => ⟨h1, h2⟩⟩

instance (w : List Dir) : Decidable (IsPerfectAcutePolyiamond w) :=
  decidable_of_iff (IsPerfectPolyiamond w ∧ CyclicChain' AcuteStep w)
    ⟨fun ⟨h1, h2⟩ => ⟨h1, h2⟩, fun ⟨h1, h2⟩ => ⟨h1, h2⟩⟩

/-- The languages of perfect / perfect obtuse / perfect acute polyiamonds over
`Σ = {a,…,f}`, in the sense of `Mathlib.Computability.Language`.  (Mathlib's
`DFA.pumping_lemma` etc. are available for statements about (non-)regularity
of these languages.) -/
def perfectLang : Language Dir := {w | IsPerfectPolyiamond w}

def obtuseLang : Language Dir := {w | IsPerfectObtusePolyiamond w}

def acuteLang : Language Dir := {w | IsPerfectAcutePolyiamond w}

/-! ### The necessary condition: `6 ∣ n` -/

/-- **Necessity** (Theorem): if a perfect obtuse `n`-polyiamond exists,
then `n ≡ 0 (mod 6)`. -/
theorem six_dvd_length_of_obtuse {w : List Dir}
    (h : IsPerfectObtusePolyiamond w) : 6 ∣ w.length := by
  sorry

/-- Existence form of the necessity theorem. -/
theorem six_dvd_of_exists_obtuse {n : ℕ}
    (h : ∃ w : List Dir, w.length = n ∧ IsPerfectObtusePolyiamond w) :
    6 ∣ n := by
  sorry

/-- Step (1) of the necessity proof: the number of sides is even
(count of `120°` vs `240°` angles against the angle sum `(n − 2)·180°`;
combinatorially: the total turning of a simple closed boundary is `±360°`). -/
theorem even_length_of_obtuse {w : List Dir}
    (h : IsPerfectObtusePolyiamond w) : Even w.length := by
  sorry

/-- Step (2) of the necessity proof: the number of sides is divisible by `3`
(mod-3 colouring argument, see `colour_pair_step` below). -/
theorem three_dvd_length_of_obtuse {w : List Dir}
    (h : IsPerfectObtusePolyiamond w) : 3 ∣ w.length := by
  sorry

/-! #### Scaffolding for the mod-3 colouring argument -/

/-- The 3-colouring `(x, y, z) ↦ x − y (mod 3)` of the triangular grid. -/
def colour (p : Pt) : ZMod 3 := ((p.1 - p.2.1 : ℤ) : ZMod 3)

/-- The vertex of the perfect polyiamond reached after tracing its first `i`
sides, starting from the origin. -/
def vertexAfter (w : List Dir) (i : ℕ) : Pt :=
  ((unitSteps ((perfectSides w).take i)).map Dir.vec).sum

/-- Colouring invariant, per **pair** of sides: tracing two consecutive sides
of a perfect obtuse polyiamond — of lengths `2m` and `2m − 1` — adds `1`
(mod 3) to the colour of the current vertex.  Summing over the `n / 2` pairs
and using that the boundary closes forces `3 ∣ n / 2`, hence `6 ∣ n`.

N.B.  This per-pair statement is the sound form of the invariant (Lemma 3 of
`kombinatorikas_uzdevums.pdf`).  The colour change along a *single* side of
length `ℓ` equals `ℓ (mod 3)` for the "red" directions `a, c, e` and
`2ℓ (mod 3)` for the "blue" directions `b, d, f`, which is *not* constant;
only the sum over a red–blue pair, `2m · 1 + (2m − 1) · 2 ≡ 1 (mod 3)`, is. -/
theorem colour_pair_step {w : List Dir} (h : IsPerfectObtusePolyiamond w)
    {i : ℕ} (hi : 2 * i + 2 ≤ w.length) :
    colour (vertexAfter w (2 * i + 2)) = colour (vertexAfter w (2 * i)) + 1 := by
  sorry

/-! ### Repeated subwords

The explicit infinite families (`wordA`/`wordB` in `Lean4.Perfect12k`,
`wordE` in `Lean4.Perfect8k_8`) are all built from periodically repeated
two-letter blocks; `rep` and the arithmetic-progression formula
`wsum_rep_pair` are the shared machinery for evaluating their boundary
sums with the parameter `k` symbolic. -/

/-- `rep u k` is the word `u` repeated `k` times (`u^k` in string notation). -/
def rep (u : List Dir) : ℕ → List Dir
  | 0 => []
  | k + 1 => u ++ rep u k

@[simp] lemma rep_length (u : List Dir) (k : ℕ) :
    (rep u k).length = k * u.length := by
  induction k with
  | zero => simp [rep]
  | succ k ih => simp only [rep, List.length_append, ih]; ring

/-- Arithmetic-progression formula: in `(xy)^k` traced with weights
`n, n − 1, …, n − 2k + 1`, the letter `x` collects the weights
`n, n − 2, …` summing to `k(n − k + 1)`, and `y` the weights
`n − 1, n − 3, …` summing to `k(n − k)`. -/
lemma wsum_rep_pair (x y : Dir) (k : ℕ) (n : ℤ) :
    wsum n (rep [x, y] k)
      = ((k : ℤ) * (n - k + 1)) • x.vec + ((k : ℤ) * (n - k)) • y.vec := by
  induction k generalizing n with
  | zero => simp [rep]
  | succ k ih =>
    have h : rep [x, y] (k + 1) = x :: y :: rep [x, y] k := rfl
    rw [h, wsum_cons, wsum_cons, ih]
    push_cast
    module

/-- The four-letter analogue of `wsum_rep_pair`: in `(xyzw)^k` traced with
weights `n, n − 1, …, n − 4k + 1`, the letter `x` collects the weights
`n, n − 4, …` summing to `k(n − 2k + 2)`, and `y`, `z`, `w` likewise the
sums `k(n − 2k + 1)`, `k(n − 2k)`, `k(n − 2k − 1)`. -/
lemma wsum_rep_quad (x y z w : Dir) (k : ℕ) (n : ℤ) :
    wsum n (rep [x, y, z, w] k)
      = ((k : ℤ) * (n - 2 * k + 2)) • x.vec + ((k : ℤ) * (n - 2 * k + 1)) • y.vec
        + ((k : ℤ) * (n - 2 * k)) • z.vec + ((k : ℤ) * (n - 2 * k - 1)) • w.vec := by
  induction k generalizing n with
  | zero => simp [rep]
  | succ k ih =>
    have h : rep [x, y, z, w] (k + 1) = x :: y :: z :: w :: rep [x, y, z, w] k := rfl
    rw [h, wsum_cons, wsum_cons, wsum_cons, wsum_cons, ih]
    push_cast
    module

/-- No word of length 6 is both cyclically obtuse and closed: a finite check
over the `6^6` candidates, certified by the kernel.  (Simplicity is not needed
for the contradiction: *no* hexagonal boundary with only `120°`/`240°` angles
and sides `6, 5, 4, 3, 2, 1` returns to its starting point.  This is stronger
than the classical argument via the total turning of a simple closed curve,
which would only reduce the candidates to the equiangular words
`x · x±60° · x±120° · ⋯` and still needs closure to fail for those.) -/
lemma no_obtuse_closed_six : ∀ d₁ d₂ d₃ d₄ d₅ d₆ : Dir,
    ¬ (CyclicChain' ObtuseStep [d₁, d₂, d₃, d₄, d₅, d₆] ∧
       wsum 6 [d₁, d₂, d₃, d₄, d₅, d₆] = 0) := by
  decide +kernel

/-- No perfect obtuse hexagon exists: writing the word as its six letters,
`no_obtuse_closed_six` contradicts the obtuse-turn and closure conditions. -/
theorem not_exists_obtuse_six :
    ¬ ∃ w : List Dir, w.length = 6 ∧ IsPerfectObtusePolyiamond w := by
  rintro ⟨w, hlen, h⟩
  obtain ⟨v, rfl⟩ : ∃ v : Fin 6 → Dir, w = List.ofFn v := by
    refine ⟨fun i => w[(i : ℕ)]'(by rw [hlen]; exact i.isLt), ?_⟩
    exact List.ext_getElem (by simp [hlen]) (fun i h1 h2 => (List.getElem_ofFn h2).symm)
  have e : List.ofFn v = [v 0, v 1, v 2, v 3, v 4, v 5] := by simp [List.ofFn_succ]
  rw [e] at h
  refine no_obtuse_closed_six (v 0) (v 1) (v 2) (v 3) (v 4) (v 5) ⟨h.obtuse, ?_⟩
  have hc := h.perfect.closes
  rw [sum_map_vec_unitSteps_eq_wsum] at hc
  simpa using hc

/-! ### Optional bridge to Euclidean geometry

Should a fully geometric statement ever be wanted, the grid plane embeds into
`ℝ²` by the map below, which sends the six unit directions to the six unit
vectors at angles `0°, −60°, …` (it is injective on the sublattice
`x + y + z = 0`, where `z` is determined by `x` and `y`).  The angle
conditions could then be re-expressed with `EuclideanGeometry.oangle`, and
`ObtuseStep`/`AcuteStep` proved equivalent to them — but note that Mathlib has
no simple-polygon machinery, so the combinatorial development above remains
the workable formalization. -/

/-- `(x, y, z) ↦ (x + y/2, −(√3/2)·y)`; e.g. `vec a ↦ (1, 0)`,
`vec b ↦ (1/2, √3/2)`. -/
noncomputable def toPlane (p : Pt) : ℝ × ℝ :=
  ((p.1 : ℝ) + (p.2.1 : ℝ) / 2, -(Real.sqrt 3 / 2) * (p.2.1 : ℝ))

/-! ### Area

The area of a polyiamond, measured in *unit triangles* (not the Euclidean
area).  Under the embedding `toPlane`, `u = x + y/2` and `v = −(√3/2)·y`,
so each term of the Euclidean shoelace formula transforms as
`uᵢ·vⱼ − uⱼ·vᵢ = (√3/2)·(xⱼ·yᵢ − xᵢ·yⱼ)`, giving Euclidean area
`½·|Σᵢ (uᵢ·vᵢ₊₁ − uᵢ₊₁·vᵢ)| = (√3/4)·|Σᵢ (xᵢ·yᵢ₊₁ − xᵢ₊₁·yᵢ)|`.
A unit grid triangle has Euclidean area exactly `√3/4`, so the integer
`|Σᵢ (xᵢ·yᵢ₊₁ − xᵢ₊₁·yᵢ)|`, computed from the cube coordinates of the
boundary vertices, *is* the number of unit triangles enclosed. -/

/-- The cross-product term `x_p·y_q − x_q·y_p` of the shoelace formula, in
the first two cube coordinates. -/
def cross (p q : Pt) : ℤ := p.1 * q.2.1 - q.1 * p.2.1

/-- The shoelace sum `Σᵢ cross Pᵢ Pᵢ₊₁` over consecutive points of a list. -/
def shoelace : List Pt → ℤ
  | p :: q :: l => cross p q + shoelace (q :: l)
  | _ => 0

/-- The area of the region enclosed by the boundary `s`, measured in unit
triangles.  (`trace s` of a closed boundary begins *and ends* at the origin,
so the shoelace sum over its consecutive points is already the full cyclic
sum.)  For a genuine polyiamond this is a positive integer; the absolute
value makes the definition independent of the traversal orientation. -/
def area (s : Sides) : ℤ := |shoelace (trace s)|

open Dir in
/-- The area of a single unit triangle is `1`. -/
example : area [(1, a), (1, c), (1, e)] = 1 := by decide

/-! #### Shoelace sums of perfect boundaries

`crossSum`/`csum` are the area counterparts of the `wsum` machinery above:
they evaluate the shoelace sum of a boundary walk side by side, so that sums
over subwords compose (`csum_append`), a translation of the starting point
enters only through `cross` and the boundary vector sum
(`csum_eq_cross_wsum_add_csum`), and periodic subwords get polynomial closed
forms (see `Lean4.Perfect8k_5`, where this machinery proves the area
polynomial `area_wordF` for every `k`). -/

@[simp] lemma cross_zero_left (q : Pt) : cross 0 q = 0 := by
  simp [cross]

@[simp] lemma cross_zero_right (p : Pt) : cross p 0 = 0 := by
  simp [cross]

@[simp] lemma cross_self (p : Pt) : cross p p = 0 := by
  simp [cross]

lemma cross_add_left (p q r : Pt) : cross (p + q) r = cross p r + cross q r := by
  simp only [cross, Prod.fst_add, Prod.snd_add]; ring

lemma cross_add_right (p q r : Pt) : cross p (q + r) = cross p q + cross p r := by
  simp only [cross, Prod.fst_add, Prod.snd_add]; ring

lemma cross_zsmul_left (n : ℤ) (p q : Pt) : cross (n • p) q = n * cross p q := by
  simp only [cross, Prod.smul_fst, Prod.smul_snd, smul_eq_mul]; ring

lemma cross_zsmul_right (n : ℤ) (p q : Pt) : cross p (n • q) = n * cross p q := by
  simp only [cross, Prod.smul_fst, Prod.smul_snd, smul_eq_mul]; ring

/-- The shoelace sum of the unit-step walk that starts at `p` and follows the
directions `ds`: the step from `q` in direction `d` contributes
`cross q (q + vec d) = cross q (vec d)`. -/
def crossSum : Pt → List Dir → ℤ
  | _, [] => 0
  | p, d :: ds => cross p d.vec + crossSum (p + d.vec) ds

@[simp] lemma crossSum_nil (p : Pt) : crossSum p [] = 0 := rfl

@[simp] lemma crossSum_cons (p : Pt) (d : Dir) (ds : List Dir) :
    crossSum p (d :: ds) = cross p d.vec + crossSum (p + d.vec) ds := rfl

/-- Prepending a point to a unit-step walk adds one shoelace term
(`scanl` is never empty, so `shoelace` always sees the first edge). -/
private lemma shoelace_cons_scanl (p q : Pt) (ds : List Dir) :
    shoelace (p :: ds.scanl (fun r d => r + d.vec) q)
      = cross p q + shoelace (ds.scanl (fun r d => r + d.vec) q) := by
  cases ds <;> simp only [List.scanl_nil, List.scanl_cons, shoelace]

/-- The shoelace sum of the unit-step walk from `p` along `ds` is
`crossSum p ds`. -/
lemma shoelace_scanl (ds : List Dir) (p : Pt) :
    shoelace (ds.scanl (fun q d => q + d.vec) p) = crossSum p ds := by
  induction ds generalizing p with
  | nil => rfl
  | cons d ds ih =>
    simp only [List.scanl_cons]
    rw [shoelace_cons_scanl, ih, crossSum_cons, cross_add_right, cross_self,
      zero_add]

/-- The shoelace sum of the trace of a boundary, one unit step at a time. -/
lemma shoelace_trace (s : Sides) :
    shoelace (trace s) = crossSum 0 (unitSteps s) :=
  shoelace_scanl _ _

lemma crossSum_append (u v : List Dir) (p : Pt) :
    crossSum p (u ++ v)
      = crossSum p u + crossSum (p + (u.map Dir.vec).sum) v := by
  induction u generalizing p with
  | nil => simp
  | cons d u ih => simp [ih, add_assoc]

/-- A straight run of `ℓ` unit steps in direction `d` — one side of length
`ℓ` — contributes `ℓ · cross p (vec d)` to the shoelace sum. -/
lemma crossSum_replicate (ℓ : ℕ) (d : Dir) (p : Pt) :
    crossSum p (List.replicate ℓ d) = ℓ * cross p d.vec := by
  induction ℓ generalizing p with
  | zero => simp
  | succ ℓ ih =>
    rw [List.replicate_succ, crossSum_cons, ih, cross_add_left, cross_self]
    push_cast
    ring

/-- `csum n p w`: the shoelace sum of the boundary walk that starts at `p` and
traces consecutive sides of lengths `n, n − 1, …` in directions `w₀, w₁, …`
(the side from `q` of length `ℓ` in direction `d` contributes
`ℓ · cross q (vec d)` and moves the current point to `q + ℓ • vec d`).
This is the area counterpart of `wsum`. -/
def csum : ℤ → Pt → List Dir → ℤ
  | _, _, [] => 0
  | n, p, d :: w => n * cross p d.vec + csum (n - 1) (p + n • d.vec) w

@[simp] lemma csum_nil (n : ℤ) (p : Pt) : csum n p [] = 0 := rfl

@[simp] lemma csum_cons (n : ℤ) (p : Pt) (d : Dir) (w : List Dir) :
    csum n p (d :: w) = n * cross p d.vec + csum (n - 1) (p + n • d.vec) w := rfl

lemma csum_append (u v : List Dir) (n : ℤ) (p : Pt) :
    csum n p (u ++ v)
      = csum n p u + csum (n - u.length) (p + wsum n u) v := by
  induction u generalizing n p with
  | nil => simp
  | cons d u ih =>
    have h : n - 1 - (u.length : ℤ) = n - ((u.length : ℤ) + 1) := by ring
    simp [ih, h, add_assoc]

/-- Translating the starting point of a boundary walk changes its shoelace
sum by the cross product with the total boundary vector: the `p`-dependence
of `csum` is entirely captured by `cross p (wsum n w)`. -/
lemma csum_eq_cross_wsum_add_csum (w : List Dir) (n : ℤ) (p : Pt) :
    csum n p w = cross p (wsum n w) + csum n 0 w := by
  induction w generalizing n p with
  | nil => simp
  | cons d w ih =>
    have h1 := ih (n - 1) (p + n • d.vec)
    have h2 := ih (n - 1) ((0 : Pt) + n • d.vec)
    rw [csum_cons, csum_cons, wsum_cons, h1, h2]
    simp only [cross_add_right, cross_add_left, cross_zsmul_left,
      cross_zsmul_right, cross_zero_left, zero_add]
    ring

/-- The shoelace sum of the boundary of a perfect polyiamond, in `csum` form
(the area counterpart of `sum_map_vec_unitSteps_eq_wsum`). -/
lemma crossSum_unitSteps_perfectSides (w : List Dir) (p : Pt) :
    crossSum p (unitSteps (perfectSides w)) = csum w.length p w := by
  induction w generalizing p with
  | nil => rfl
  | cons d w ih =>
    simp only [perfectSides, unitSteps]
    rw [crossSum_append, crossSum_replicate, ih]
    simp only [List.map_replicate, List.sum_replicate, List.length_cons,
      csum_cons, Nat.cast_add, Nat.cast_one, add_sub_cancel_right,
      ← natCast_zsmul]

/-- The shoelace sum of the trace of a perfect polyiamond: `area` reduces to
the weighted shoelace sum `csum` of its direction word. -/
lemma shoelace_trace_perfectSides (w : List Dir) :
    shoelace (trace (perfectSides w)) = csum w.length 0 w := by
  rw [shoelace_trace, crossSum_unitSteps_perfectSides]

/-! ### Sanity checks

All predicates above are decidable, so concrete instances can be certified by
computation; see the `k = 0` instances in `Lean4.Perfect12k` (the smallest
serial `120°` isogon `abcdedefafab`) and `Lean4.Perfect8k_8` (the smallest
member `abdedeab` of the `8k + 8` family).

(The boundary of an `n`-gon visits `n(n+1)/2` points and the `Nodup` check is
quadratic in that; for `n = 12` the kernel handles it — `decide +kernel`, the
plain `decide` elaborator hits its recursion limit — but for larger instances
`native_decide` is recommended.)

The `n = 6` non-existence is *not* syntactically decidable in the form
`¬ ∃ w : List Dir, …` (the existential ranges over the infinite type
`List Dir`); `not_exists_obtuse_six` above therefore goes through the
decidable reformulation over the six letters of the word
(`no_obtuse_closed_six`). -/

end Polyiamond
