"""Core math for obtuse polyiamonds (serial 120-degree isogons).

A string w over {A,B,C,D,E,F} encodes side directions; the i-th letter (1-indexed)
is the direction of the side of length n-i+1, so side lengths decrease n,n-1,...,1.

Directions as cube-coordinate unit vectors (components sum to 0):
  A=(1,0,-1) B=(1,-1,0) C=(0,-1,1) D=(-1,0,1) E=(-1,1,0) F=(0,1,-1)
Note A=-D, B=-E, C=-F.

Statistics for a string w of length n:
  p(w) = sum of direction triples                 ("plain sum" / drift D)
  M(w) = sum of i * (direction triple of i-th)     ("positional moment", i 1-indexed)
Closure:  (n+1)*p(w) - M(w) = 0    <=>  sum_i (n-i+1)*d_i = 0.
"""

DIRS = {
    'A': (1, 0, -1),
    'B': (1, -1, 0),
    'C': (0, -1, 1),
    'D': (-1, 0, 1),
    'E': (-1, 1, 0),
    'F': (0, 1, -1),
}


def vadd(u, v):
    return (u[0] + v[0], u[1] + v[1], u[2] + v[2])


def vscale(s, u):
    return (s * u[0], s * u[1], s * u[2])


def p_sum(w):
    """Plain sum / drift D = sum of direction triples."""
    x = y = z = 0
    for ch in w:
        dx, dy, dz = DIRS[ch]
        x += dx; y += dy; z += dz
    return (x, y, z)


def m_moment(w):
    """Positional moment M = sum_i i*d_i (i 1-indexed)."""
    x = y = z = 0
    for i, ch in enumerate(w, start=1):
        dx, dy, dz = DIRS[ch]
        x += i * dx; y += i * dy; z += i * dz
    return (x, y, z)


def is_balanced(block):
    """p(block) == (0,0,0)."""
    return p_sum(block) == (0, 0, 0)


def is_closed(w):
    """(n+1)*p(w) - M(w) == 0."""
    n = len(w)
    p = p_sum(w)
    m = m_moment(w)
    return all((n + 1) * p[k] - m[k] == 0 for k in range(3))


# ---- geometry / simplicity on the triangular lattice ----------------------

def vertices(w):
    """Polygon vertices v_0..v_n in cube coords.
    Edge i (1-indexed) has direction d_i and length n-i+1.
    Returns list of (x,y,z) tuples, length n+1 (v_0 == origin)."""
    n = len(w)
    verts = [(0, 0, 0)]
    cur = (0, 0, 0)
    for i, ch in enumerate(w, start=1):
        length = n - i + 1
        cur = vadd(cur, vscale(length, DIRS[ch]))
        verts.append(cur)
    return verts


def _on_segment_collinear(a, b, c):
    """Given a,b,c are collinear (a->b is an axis-aligned cube step direction),
    is c strictly between a and b (inclusive endpoints handled by caller)?"""
    # project onto the dominant coordinate
    for k in range(3):
        if a[k] != b[k]:
            lo, hi = (a[k], b[k]) if a[k] < b[k] else (b[k], a[k])
            return lo <= c[k] <= hi
    return False


def _seg_dir(a, b):
    """Unit step direction of segment a->b (one of the 6 dirs)."""
    d = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    g = max(abs(d[0]), abs(d[1]), abs(d[2]))
    if g == 0:
        return (0, 0, 0)
    return (d[0] // g, d[1] // g, d[2] // g)


def _segments_intersect(p1, p2, p3, p4):
    """Do segments p1p2 and p3p4 (lattice, along the 6 dirs) share any point?
    Works in cube coords using a 2D embedding (x,y) since z=-x-y is redundant."""
    def to2d(pt):
        return (pt[0], pt[1])
    a, b, c, d = to2d(p1), to2d(p2), to2d(p3), to2d(p4)

    def cross(o, u, v):
        return (u[0] - o[0]) * (v[1] - o[1]) - (u[1] - o[1]) * (v[0] - o[0])

    def on_seg(o, u, q):  # q collinear with o-u; is it within bbox?
        return (min(o[0], u[0]) <= q[0] <= max(o[0], u[0]) and
                min(o[1], u[1]) <= q[1] <= max(o[1], u[1]))

    d1 = cross(c, d, a)
    d2 = cross(c, d, b)
    d3 = cross(a, b, c)
    d4 = cross(a, b, d)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    if d1 == 0 and on_seg(c, d, a):
        return True
    if d2 == 0 and on_seg(c, d, b):
        return True
    if d3 == 0 and on_seg(a, b, c):
        return True
    if d4 == 0 and on_seg(a, b, d):
        return True
    return False


def is_simple(w):
    """True iff the closed polygon is simple: no vertex revisited (except v_0==v_n)
    and no two non-adjacent edges intersect.  Assumes/also checks closure."""
    verts = vertices(w)
    n = len(w)
    # must be closed
    if verts[-1] != (0, 0, 0):
        return False
    # vertices v_0..v_{n-1} must be distinct (v_n == v_0)
    seen = set()
    for v in verts[:-1]:
        if v in seen:
            return False
        seen.add(v)
    # edges: edge i connects verts[i-1]->verts[i], for i=1..n
    edges = [(verts[i], verts[i + 1]) for i in range(n)]
    m = len(edges)
    for i in range(m):
        a1, a2 = edges[i]
        for j in range(i + 1, m):
            # skip adjacent edges (share a vertex) including wrap-around
            if j == i + 1:
                continue
            if i == 0 and j == m - 1:
                continue
            b1, b2 = edges[j]
            if _segments_intersect(a1, a2, b1, b2):
                return False
    return True


# ---- insertion / family transition ---------------------------------------

def transition_matrix(L):
    """6x6 unipotent map on state (D, M) (each in R^3) for one family step
    that inserts total balanced length L.  D' = D, M' = M + L*D.
    Returns list of 6 rows (columns/rows ordered D0,D1,D2,M0,M1,M2)."""
    T = [[1 if i == j else 0 for j in range(6)] for i in range(6)]
    for k in range(3):
        T[3 + k][k] = L  # M_k' = M_k + L*D_k
    return T
