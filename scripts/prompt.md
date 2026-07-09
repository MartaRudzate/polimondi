We have a database of perfect obtuse polyiamonds ("serial 120-degree isogons") in
docs/obtuse_new/. Each is a string over {A,B,C,D,E,F} encoding side directions; the
i-th letter is the direction of the side of length n-i+1, so side lengths decrease
n, n-1, ..., 1. All valid obtuse polyiamonds are listed for n = 12,18,24,30,36,42,48
(several million strings at n=48). Do NOT load the whole database into your context —
process it with scripts and only surface short summaries and final results.

GOAL: find database strings that can serve as the FIRST element of an infinite PCL-grammar
family of obtuse polyiamonds — sequences where the same fixed direction-blocks are inserted
at fixed positions k times each, giving n = n_0 + L*k for some step L divisible by 6 —
and emit closed-form expressions like  A(BABAFEDC)^k C D ... (X)^k ...  for each family found.

MATHEMATICAL BACKGROUND (encode this in your scripts):

Represent the six directions as integer triples:
  A=(1,0,-1) B=(1,-1,0) C=(0,-1,1) D=(-1,0,1) E=(-1,1,0) F=(0,1,-1)
For a string w, define two vector statistics:
  p(w) = sum of direction triples              ("plain sum" / drift D)
  M(w) = sum of i * (direction triple of i-th letter)   ("positional moment", i 1-indexed)
A string of length n is a CLOSED polyiamond iff  (n+1)*p(w) - M(w) = 0.

Inserting blocks turns the (D,M) state into a unipotent linear map. A pair (w, w') —
where w has length n, w' has length n'=n+L, and w' is w with blocks B_1..B_c inserted —
extends to an infinite closed family iff:
  C1 (drift invariance): the total inserted plain sum is zero,  sum_j p(B_j) = 0;
  C2 (moment shift, sufficient form): EACH inserted block is individually balanced,
     p(B_j) = 0, which forces M to shift by exactly L*p(w) — the additive-shift mechanism
     that makes the closure equation propagate from level k to level k+1 automatically.
Simplicity (non-self-intersection) is NOT automatic and must be checked separately.

TASKS:

1. Write a script that loads docs/obtuse_new/, groups strings by n, and reports counts.
   Never print more than a few sample strings.

2. For the largest sizes, detect TANDEM REPEATS: substrings X with 1<=|X|<=12 that occur
   contiguously as X^r with r>=2. Keep only repeats where the period X is BALANCED
   (p(X) = (0,0,0)). These are families "showing themselves" — the inserted block is X.

3. For each balanced tandem repeat X^r found in a string w' of length n', de-periodize:
   remove one copy of X to get a shorter string, and check whether it appears in the
   database at size n'-|X|. Cross-link matches across n, n-6, n-12, ... to assemble
   candidate families. Allow MULTIPLE simultaneous repeat sites (the c insertion points):
   a family may insert X at site 1, Y at site 2, etc., as long as the combined inserted
   material satisfies C1, and prefer the C2 (each-block-balanced) case.

4. For every candidate family, take the inferred seed and insertion rule and GENERATE the
   next 2-3 terms symbolically. Verify each generated term is:
     (a) closed:  (n+1)*p - M = 0 ;
     (b) simple:  build the polygon on the triangular lattice (use the integer-triple
         coordinates, sum prefixes with decreasing lengths n,n-1,...,1) and check no two
         non-adjacent sides intersect and no vertex is revisited.
   Discard any family whose generated terms fail either check.

5. Output ONLY the survivors, as a concise report: for each family give the closed-form
   expression with explicit repeated blocks marked (...)^k, the step L, the size formula
   n = n_0 + L*k, the seed string, and confirmation that terms k=0,1,2,3 are valid.
   Also emit, for each family, the 6x6 unipotent transition matrix T on the (D,M) state
   and note its Jordan type. Write the full report to docs/obtuse_new/families_report.md.

Keep all heavy data on disk; put scripts in a scripts/ directory; summarize findings in
chat in under ~30 lines. If the tandem-repeat search surfaces too many candidates, rank
them by (number of distinct sizes the family is corroborated at) descending and report
the top 20.
