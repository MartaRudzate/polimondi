# Infinite PCL-grammar families of obtuse polyiamonds

Serial 120-degree isogons; strings over {A,B,C,D,E,F} with side lengths decreasing n, n-1, ..., 1.

Directions: A=(1,0,-1) B=(1,-1,0) C=(0,-1,1) D=(-1,0,1) E=(-1,1,0) F=(0,1,-1). Closure: (n+1)*p(w) - M(w) = 0.


## Summary

- Mechanism found: **C1 multi-site** families. No balanced tandem repeat (p(X)=0, |X|<=12, repeated) exists in the database, so no pure C2 single-block family manifests as a literal repeat; instead families insert several individually-unbalanced length-2/4 blocks whose plain-sums **cancel** (sum_j p(B_j) = 0).
- Step **L = 12** (divisible by 6); size formula **n = n0 + 12*k**. Families connect DB sizes spaced by 12: {12,24,36,48} or {18,30,42}.
- L=6 cross-linking yields **no** edges (checked); the minimal DB-aligned step is 12.
- Total unique families with k=0..3 closed & simple: **44**. Top 20 by number of corroborating DB sizes below.

## Shared transition matrix T on state (D, M)

One family step inserts total balanced length L=12, so D is invariant and M shifts by L*D:  D' = D,  M' = M + 12*D. In basis (D0,D1,D2,M0,M1,M2):

```
    [ 1   0   0   0   0   0]
    [ 0   1   0   0   0   0]
    [ 0   0   1   0   0   0]
    [12   0   0   1   0   0]
    [ 0  12   0   0   1   0]
    [ 0   0  12   0   0   1]
```
T is unipotent: (T - I)^2 = 0 with rank(T - I) = 3. **Jordan type: three Jordan blocks of size 2, all eigenvalue 1** (J = 3 x J_2(1)).

## Top families

### 1. seed n0=12  — corroborated at DB sizes [12, 24, 36, 48] (4 sizes)

- closed form: `(AB)^kABC(DE)^kDE(DC)^kDE(FA)^kFA(FE)^kFA(BC)^kB`
- seed (k=0): `ABCDEDEFAFAB`
- step L = 12,  n = 12 + 12*k
- per-step inserted blocks (pos in seed, block): [(0, 'AB'), (3, 'DE'), (5, 'DC'), (7, 'FA'), (9, 'FE'), (11, 'BC')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=12:OK), k=1(n=24:OK), k=2(n=36:OK), k=3(n=48:OK)
- terms: k0=`ABCDEDEFAFAB`
         k1=`ABABCDEDEDCDEFAFAFEFABCB`
         k2=`ABABABCDEDEDEDCDCDEFAFAFAFEFEFABCBCB`

### 2. seed n0=18  — corroborated at DB sizes [18, 30, 42] (3 sizes)

- closed form: `(AB)^kABAF(ED)^kEDED(EF)^kED(CB)^kCBCB(CD)^kCB(AF)^kAB`
- seed (k=0): `ABAFEDEDEDCBCBCBAB`
- step L = 12,  n = 18 + 12*k
- per-step inserted blocks (pos in seed, block): [(0, 'AB'), (4, 'ED'), (8, 'EF'), (10, 'CB'), (14, 'CD'), (16, 'AF')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=18:OK), k=1(n=30:OK), k=2(n=42:OK), k=3(n=54:OK)
- terms: k0=`ABAFEDEDEDCBCBCBAB`
         k1=`ABABAFEDEDEDEFEDCBCBCBCDCBAFAB`
         k2=`ABABABAFEDEDEDEDEFEFEDCBCBCBCBCDCDCBAFAFAB`

### 3. seed n0=18  — corroborated at DB sizes [18, 30, 42] (3 sizes)

- closed form: `(AB)^kABAF(ED)^kED(EF)^kEDED(CB)^kCB(CD)^kCBCBAB(AF)^k`
- seed (k=0): `ABAFEDEDEDCBCBCBAB`
- step L = 12,  n = 18 + 12*k
- per-step inserted blocks (pos in seed, block): [(0, 'AB'), (4, 'ED'), (6, 'EF'), (10, 'CB'), (12, 'CD'), (18, 'AF')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=18:OK), k=1(n=30:OK), k=2(n=42:OK), k=3(n=54:OK)
- terms: k0=`ABAFEDEDEDCBCBCBAB`
         k1=`ABABAFEDEDEFEDEDCBCBCDCBCBABAF`
         k2=`ABABABAFEDEDEDEFEFEDEDCBCBCBCDCDCBCBABAFAF`

### 4. seed n0=24  — corroborated at DB sizes [24, 36, 48] (3 sizes)

- closed form: `(AB)^kABAB(CD)^kCDCD(EF)^kEF(ED)^kEDEDE(FA)^kFAFAFA(BC)^kBCB`
- seed (k=0): `ABABCDCDEFEDEDEFAFAFABCB`
- step L = 12,  n = 24 + 12*k
- per-step inserted blocks (pos in seed, block): [(0, 'AB'), (4, 'CD'), (8, 'EF'), (10, 'ED'), (15, 'FA'), (21, 'BC')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=24:OK), k=1(n=36:OK), k=2(n=48:OK), k=3(n=60:OK)
- terms: k0=`ABABCDCDEFEDEDEFAFAFABCB`
         k1=`ABABABCDCDCDEFEFEDEDEDEFAFAFAFABCBCB`
         k2=`ABABABABCDCDCDCDEFEFEFEDEDEDEDEFAFAFAFAFABCBCBCB`

### 5. seed n0=30  — corroborated at DB sizes [30, 42] (2 sizes)

- closed form: `(AB)^kABABAFED(EF)^kEFE(DC)^kDC(DE)^kDEDEDCBCBCBA(BC)^kBCB(AF)^kAF`
- seed (k=0): `ABABAFEDEFEDCDEDEDCBCBCBABCBAF`
- step L = 12,  n = 30 + 12*k
- per-step inserted blocks (pos in seed, block): [(0, 'AB'), (8, 'EF'), (11, 'DC'), (13, 'DE'), (25, 'BC'), (28, 'AF')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=30:OK), k=1(n=42:OK), k=2(n=54:OK), k=3(n=66:OK)
- terms: k0=`ABABAFEDEFEDCDEDEDCBCBCBABCBAF`
         k1=`ABABABAFEDEFEFEDCDCDEDEDEDCBCBCBABCBCBAFAF`
         k2=`ABABABABAFEDEFEFEFEDCDCDCDEDEDEDEDCBCBCBABCBCBCBAFAFAF`

### 6. seed n0=30  — corroborated at DB sizes [30, 42] (2 sizes)

- closed form: `(AB)^kABABA(FE)^kFEDEFE(DC)^kDC(DE)^kDEDED(CB)^kCBCBCBABCB(AF)^kAF`
- seed (k=0): `ABABAFEDEFEDCDEDEDCBCBCBABCBAF`
- step L = 12,  n = 30 + 12*k
- per-step inserted blocks (pos in seed, block): [(0, 'AB'), (5, 'FE'), (11, 'DC'), (13, 'DE'), (18, 'CB'), (28, 'AF')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=30:OK), k=1(n=42:OK), k=2(n=54:OK), k=3(n=66:OK)
- terms: k0=`ABABAFEDEFEDCDEDEDCBCBCBABCBAF`
         k1=`ABABABAFEFEDEFEDCDCDEDEDEDCBCBCBCBABCBAFAF`
         k2=`ABABABABAFEFEFEDEFEDCDCDCDEDEDEDEDCBCBCBCBCBABCBAFAFAF`

### 7. seed n0=30  — corroborated at DB sizes [30, 42] (2 sizes)

- closed form: `(AB)^kABABA(FE)^kFEFE(DC)^kDC(DE)^kDEDEDED(CB)^kCBCBCBCB(AF)^kAFAB`
- seed (k=0): `ABABAFEFEDCDEDEDEDCBCBCBCBAFAB`
- step L = 12,  n = 30 + 12*k
- per-step inserted blocks (pos in seed, block): [(0, 'AB'), (5, 'FE'), (9, 'DC'), (11, 'DE'), (18, 'CB'), (26, 'AF')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=30:OK), k=1(n=42:OK), k=2(n=54:OK), k=3(n=66:OK)
- terms: k0=`ABABAFEFEDCDEDEDEDCBCBCBCBAFAB`
         k1=`ABABABAFEFEFEDCDCDEDEDEDEDCBCBCBCBCBAFAFAB`
         k2=`ABABABABAFEFEFEFEDCDCDCDEDEDEDEDEDCBCBCBCBCBCBAFAFAFAB`

### 8. seed n0=30  — corroborated at DB sizes [30, 42] (2 sizes)

- closed form: `(AB)^kABABA(FE)^kFEFEDE(DC)^kDC(DE)^kDEDED(CB)^kCBCBCBCBAB(AF)^kAF`
- seed (k=0): `ABABAFEFEDEDCDEDEDCBCBCBCBABAF`
- step L = 12,  n = 30 + 12*k
- per-step inserted blocks (pos in seed, block): [(0, 'AB'), (5, 'FE'), (11, 'DC'), (13, 'DE'), (18, 'CB'), (28, 'AF')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=30:OK), k=1(n=42:OK), k=2(n=54:OK), k=3(n=66:OK)
- terms: k0=`ABABAFEFEDEDCDEDEDCBCBCBCBABAF`
         k1=`ABABABAFEFEFEDEDCDCDEDEDEDCBCBCBCBCBABAFAF`
         k2=`ABABABABAFEFEFEFEDEDCDCDCDEDEDEDEDCBCBCBCBCBCBABAFAFAF`

### 9. seed n0=30  — corroborated at DB sizes [30, 42] (2 sizes)

- closed form: `(AB)^kABABCB(CD)^kCDCDEFEFEFA(FE)^kFE(DE)^kDEDEDE(FA)^kFA(BC)^kBCB`
- seed (k=0): `ABABCBCDCDEFEFEFAFEDEDEDEFABCB`
- step L = 12,  n = 30 + 12*k
- per-step inserted blocks (pos in seed, block): [(0, 'AB'), (6, 'CD'), (17, 'FE'), (19, 'DE'), (25, 'FA'), (27, 'BC')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=30:OK), k=1(n=42:OK), k=2(n=54:OK), k=3(n=66:OK)
- terms: k0=`ABABCBCDCDEFEFEFAFEDEDEDEFABCB`
         k1=`ABABABCBCDCDCDEFEFEFAFEFEDEDEDEDEFAFABCBCB`
         k2=`ABABABABCBCDCDCDCDEFEFEFAFEFEFEDEDEDEDEDEFAFAFABCBCBCB`

### 10. seed n0=30  — corroborated at DB sizes [30, 42] (2 sizes)

- closed form: `(AB)^kABABCDCB(CD)^kCDEFEFA(FE)^kFEFE(DE)^kDEDEDE(FA)^kFA(BC)^kBCB`
- seed (k=0): `ABABCDCBCDEFEFAFEFEDEDEDEFABCB`
- step L = 12,  n = 30 + 12*k
- per-step inserted blocks (pos in seed, block): [(0, 'AB'), (8, 'CD'), (15, 'FE'), (19, 'DE'), (25, 'FA'), (27, 'BC')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=30:OK), k=1(n=42:OK), k=2(n=54:OK), k=3(n=66:OK)
- terms: k0=`ABABCDCBCDEFEFAFEFEDEDEDEFABCB`
         k1=`ABABABCDCBCDCDEFEFAFEFEFEDEDEDEDEFAFABCBCB`
         k2=`ABABABABCDCBCDCDCDEFEFAFEFEFEFEDEDEDEDEDEFAFAFABCBCBCB`

### 11. seed n0=30  — corroborated at DB sizes [30, 42] (2 sizes)

- closed form: `(AB)^kABAB(CD)^kCDCD(EF)^kEFEFEDC(DE)^kDE(FA)^kFAFAFA(BC)^kBCBCDCB`
- seed (k=0): `ABABCDCDEFEFEDCDEFAFAFABCBCDCB`
- step L = 12,  n = 30 + 12*k
- per-step inserted blocks (pos in seed, block): [(0, 'AB'), (4, 'CD'), (8, 'EF'), (15, 'DE'), (17, 'FA'), (23, 'BC')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=30:OK), k=1(n=42:OK), k=2(n=54:OK), k=3(n=66:OK)
- terms: k0=`ABABCDCDEFEFEDCDEFAFAFABCBCDCB`
         k1=`ABABABCDCDCDEFEFEFEDCDEDEFAFAFAFABCBCBCDCB`
         k2=`ABABABABCDCDCDCDEFEFEFEFEDCDEDEDEFAFAFAFAFABCBCBCBCDCB`

### 12. seed n0=30  — corroborated at DB sizes [30, 42] (2 sizes)

- closed form: `(AB)^kABABC(DE)^kDE(DC)^kDCDEDE(FA)^kFABA(FE)^kFEDEFAFA(BC)^kBCBAF`
- seed (k=0): `ABABCDEDCDEDEFABAFEDEFAFABCBAF`
- step L = 12,  n = 30 + 12*k
- per-step inserted blocks (pos in seed, block): [(0, 'AB'), (5, 'DE'), (7, 'DC'), (13, 'FA'), (17, 'FE'), (25, 'BC')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=30:OK), k=1(n=42:OK), k=2(n=54:OK), k=3(n=66:OK)
- terms: k0=`ABABCDEDCDEDEFABAFEDEFAFABCBAF`
         k1=`ABABABCDEDEDCDCDEDEFAFABAFEFEDEFAFABCBCBAF`
         k2=`ABABABABCDEDEDEDCDCDCDEDEFAFAFABAFEFEFEDEFAFABCBCBCBAF`

### 13. seed n0=30  — corroborated at DB sizes [30, 42] (2 sizes)

- closed form: `(AB)^kABAB(CD)^kCDEDCDEFA(FE)^kFE(DE)^kDEDE(FA)^kFABABA(BC)^kBCBAB`
- seed (k=0): `ABABCDEDCDEFAFEDEDEFABABABCBAB`
- step L = 12,  n = 30 + 12*k
- per-step inserted blocks (pos in seed, block): [(0, 'AB'), (4, 'CD'), (13, 'FE'), (15, 'DE'), (19, 'FA'), (25, 'BC')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=30:OK), k=1(n=42:OK), k=2(n=54:OK), k=3(n=66:OK)
- terms: k0=`ABABCDEDCDEFAFEDEDEFABABABCBAB`
         k1=`ABABABCDCDEDCDEFAFEFEDEDEDEFAFABABABCBCBAB`
         k2=`ABABABABCDCDCDEDCDEFAFEFEFEDEDEDEDEFAFAFABABABCBCBCBAB`

### 14. seed n0=30  — corroborated at DB sizes [30, 42] (2 sizes)

- closed form: `(AB)^kABABC(DE)^kDE(DC)^kDCDE(FA)^kFAFEDED(EF)^kEFABABAB(CB)^kCBAB`
- seed (k=0): `ABABCDEDCDEFAFEDEDEFABABABCBAB`
- step L = 12,  n = 30 + 12*k
- per-step inserted blocks (pos in seed, block): [(0, 'AB'), (5, 'DE'), (7, 'DC'), (11, 'FA'), (18, 'EF'), (26, 'CB')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=30:OK), k=1(n=42:OK), k=2(n=54:OK), k=3(n=66:OK)
- terms: k0=`ABABCDEDCDEFAFEDEDEFABABABCBAB`
         k1=`ABABABCDEDEDCDCDEFAFAFEDEDEFEFABABABCBCBAB`
         k2=`ABABABABCDEDEDEDCDCDCDEFAFAFAFEDEDEFEFEFABABABCBCBCBAB`

### 15. seed n0=30  — corroborated at DB sizes [30, 42] (2 sizes)

- closed form: `(AB)^kABAFABA(FE)^kFEDEDE(DC)^kDC(DE)^kDEDCDCDC(BC)^kBCBCB(AF)^kAF`
- seed (k=0): `ABAFABAFEDEDEDCDEDCDCDCBCBCBAF`
- step L = 12,  n = 30 + 12*k
- per-step inserted blocks (pos in seed, block): [(0, 'AB'), (7, 'FE'), (13, 'DC'), (15, 'DE'), (23, 'BC'), (28, 'AF')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=30:OK), k=1(n=42:OK), k=2(n=54:OK), k=3(n=66:OK)
- terms: k0=`ABAFABAFEDEDEDCDEDCDCDCBCBCBAF`
         k1=`ABABAFABAFEFEDEDEDCDCDEDEDCDCDCBCBCBCBAFAF`
         k2=`ABABABAFABAFEFEFEDEDEDCDCDCDEDEDEDCDCDCBCBCBCBCBAFAFAF`

### 16. seed n0=30  — corroborated at DB sizes [30, 42] (2 sizes)

- closed form: `AB(AF)^kAFAFA(BC)^kBCDCDC(DE)^kDEDE(DC)^kDCDEDE(FE)^kFEFEF(AB)^kAB`
- seed (k=0): `ABAFAFABCDCDCDEDEDCDEDEFEFEFAB`
- step L = 12,  n = 30 + 12*k
- per-step inserted blocks (pos in seed, block): [(2, 'AF'), (7, 'BC'), (13, 'DE'), (17, 'DC'), (23, 'FE'), (28, 'AB')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=30:OK), k=1(n=42:OK), k=2(n=54:OK), k=3(n=66:OK)
- terms: k0=`ABAFAFABCDCDCDEDEDCDEDEFEFEFAB`
         k1=`ABAFAFAFABCBCDCDCDEDEDEDCDCDEDEFEFEFEFABAB`
         k2=`ABAFAFAFAFABCBCBCDCDCDEDEDEDEDCDCDCDEDEFEFEFEFEFABABAB`

### 17. seed n0=30  — corroborated at DB sizes [30, 42] (2 sizes)

- closed form: `(AB)^kABA(FE)^kFEDE(DC)^kDCDCDE(DC)^kDCBABAFABAFAF(EF)^kEF(AB)^kAB`
- seed (k=0): `ABAFEDEDCDCDEDCBABAFABAFAFEFAB`
- step L = 12,  n = 30 + 12*k
- per-step inserted blocks (pos in seed, block): [(0, 'AB'), (3, 'FE'), (7, 'DC'), (13, 'DC'), (26, 'EF'), (28, 'AB')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=30:OK), k=1(n=42:OK), k=2(n=54:OK), k=3(n=66:OK)
- terms: k0=`ABAFEDEDCDCDEDCBABAFABAFAFEFAB`
         k1=`ABABAFEFEDEDCDCDCDEDCDCBABAFABAFAFEFEFABAB`
         k2=`ABABABAFEFEFEDEDCDCDCDCDEDCDCDCBABAFABAFAFEFEFEFABABAB`

### 18. seed n0=30  — corroborated at DB sizes [30, 42] (2 sizes)

- closed form: `(AB)^kABA(FE)^kFEDE(DC)^kDC(DE)^kDEDCBABA(BC)^kBCB(AF)^kAFEFEDEFEF`
- seed (k=0): `ABAFEDEDCDEDCBABABCBAFEFEDEFEF`
- step L = 12,  n = 30 + 12*k
- per-step inserted blocks (pos in seed, block): [(0, 'AB'), (3, 'FE'), (7, 'DC'), (9, 'DE'), (17, 'BC'), (20, 'AF')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=30:OK), k=1(n=42:OK), k=2(n=54:OK), k=3(n=66:OK)
- terms: k0=`ABAFEDEDCDEDCBABABCBAFEFEDEFEF`
         k1=`ABABAFEFEDEDCDCDEDEDCBABABCBCBAFAFEFEDEFEF`
         k2=`ABABABAFEFEFEDEDCDCDCDEDEDEDCBABABCBCBCBAFAFAFEFEDEFEF`

### 19. seed n0=30  — corroborated at DB sizes [30, 42] (2 sizes)

- closed form: `ABA(FE)^kFEDEDCDE(DC)^kDC(BA)^kBABA(BC)^kBCB(AF)^kAFEF(ED)^kEDEFEF`
- seed (k=0): `ABAFEDEDCDEDCBABABCBAFEFEDEFEF`
- step L = 12,  n = 30 + 12*k
- per-step inserted blocks (pos in seed, block): [(3, 'FE'), (11, 'DC'), (13, 'BA'), (17, 'BC'), (20, 'AF'), (24, 'ED')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=30:OK), k=1(n=42:OK), k=2(n=54:OK), k=3(n=66:OK)
- terms: k0=`ABAFEDEDCDEDCBABABCBAFEFEDEFEF`
         k1=`ABAFEFEDEDCDEDCDCBABABABCBCBAFAFEFEDEDEFEF`
         k2=`ABAFEFEFEDEDCDEDCDCDCBABABABABCBCBCBAFAFAFEFEDEDEDEFEF`

### 20. seed n0=30  — corroborated at DB sizes [30, 42] (2 sizes)

- closed form: `(AB)^kABA(FE)^kFEDE(DC)^kDCDE(DC)^kDCDCBABABAFAFA(FE)^kFEF(AB)^kAB`
- seed (k=0): `ABAFEDEDCDEDCDCBABABAFAFAFEFAB`
- step L = 12,  n = 30 + 12*k
- per-step inserted blocks (pos in seed, block): [(0, 'AB'), (3, 'FE'), (7, 'DC'), (11, 'DC'), (25, 'FE'), (28, 'AB')]
- inserted plain-sum (C1): (0, 0, 0); each block balanced? no (C1: combined cancellation)
- verification k=0..3: k=0(n=30:OK), k=1(n=42:OK), k=2(n=54:OK), k=3(n=66:OK)
- terms: k0=`ABAFEDEDCDEDCDCBABABAFAFAFEFAB`
         k1=`ABABAFEFEDEDCDCDEDCDCDCBABABAFAFAFEFEFABAB`
         k2=`ABABABAFEFEFEDEDCDCDCDEDCDCDCDCBABABAFAFAFEFEFEFABABAB`

