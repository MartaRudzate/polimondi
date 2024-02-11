import math
from .point_tg import PointTg
from .point_tg import DIRECTIONS
from .point_tg import AA,BB,CC,DD,EE,FF
from .geom_utilities import *
from .inductive_splits import InductiveSplits

from shapely.geometry import Point, Polygon, LineString
# from shapely.ops import rotate
from shapely import affinity
from scipy.spatial import ConvexHull
import numpy as np
import copy as cp



#DIRECTIONS = {'A': PointTg(1,0,-1), 'B': PointTg(1,-1,0), 'C': PointTg(0,-1,1),
#        'D': PointTg(-1,0,1), 'E': PointTg(-1,1,0),'F': PointTg(0,1,-1)}

DESCARTES = {'A': (1.0, 0.0), 'B': (0.5, 1.0), 'C': (-0.5, 1.0), 'D': (-1.0, 0.0), 'E': (-0.5, -1.0), 'F': (0.5, -1.0) }

unit_triangle_height = math.sqrt(3) / 2
unit_triangle_area = math.sqrt(3) / 4

class Polyiamond:
    # "sides" is a list of tuples for a polyiamond
    # such as [(5,'A'), (4,'C'), (3,'E'), (2,'D'), (1,'F')].
    # It does not need to be perfect or even magic, so the side lengths can be any integers.
    # Side directions are always one of the following: 'A', 'B', 'C', 'D', 'E', 'F'.
    def __init__(self, sides):
        self.compact_sides = sides
        if isinstance(sides, str):
            sides = list(zip(range(len(sides), 0, -1), list(sides)))
        self.sides = sides
        if not self.is_valid():
            print(f"WARNING: Polyiamond {self.compact_sides} is not valid - line segments do not close!")
            pass
            # raise ValueError("Polyiamond {} cannot exist".format(sides))
        else:
            self.setup()

    # The 1st check: The last side should return back to (0,0,0)
    # The 2nd check: The line segments must not cross themselves (not implemented)
    def is_valid(self):
        self.get_vertices()
        (side_length, direction) = self.sides[-1]
        new_vertex = self.vertices[-1] + side_length * PointTg.get_direction(direction)
        check1 = (new_vertex == PointTg(0,0,0))

        currVertex = PointTg(0,0,0)
        check2 = True  # assume the sides do not intersect
        points = set()
        for (sidelen,dir) in self.sides:
            for i in range(1, sidelen+1):
                currPoint = currVertex + i*DIRECTIONS[dir]
                if currPoint in points:
                    # print('Intersecting STUFF!')
                    check2 = False
                else:
                    points.add(currPoint)
            nextSide = sidelen*DIRECTIONS[dir]
            currVertex = currVertex + nextSide
        return check1 and check2

    # This method will do custom initializations
    def setup(self):
        self.get_mod_descartes()
        self.get_descartes()
        self.get_signed_area()
        self.get_area()
        self.get_perimeter()
        self.get_bounding_hexagon()
        self.get_bounding_sizes()


    def __str__(self):
        return 'PolyGeometry({})'.format(self.sides)

    def __repr__(self):
        result = "sides = {}".format(self.sides) + ", " + "signed_area = {}".format(self.signed_area)
        return result

    # All vertices in triangle coordinates.
    def get_vertices(self):
        if not hasattr(self, 'vertices'):
            self.vertices = [PointTg(0, 0, 0)]
            for (side_length, direction) in self.sides:
                new_vertex = self.vertices[-1] + side_length * PointTg.get_direction(direction)
                if len(self.vertices) < len(self.sides):
                    self.vertices.append(new_vertex)
        return self.vertices

    # Get vertex coordinates (but assume that triangle height is 1 unit; not sqrt(3)/2).
    def get_mod_descartes(self):
        if not hasattr(self, 'mod_descartes'):
            vectors = [(L*DESCARTES[D][0], L*DESCARTES[D][1]) for (L, D) in self.sides]

            self.mod_descartes = [(0.0, 0.0)]
            for i in range(0, len(self.sides)-1):
                new_pair = (self.mod_descartes[-1][0] + vectors[i][0], self.mod_descartes[-1][1] + vectors[i][1])
                self.mod_descartes.append(new_pair)
        return self.mod_descartes

    # Get regular (x,y) coordinates of vertices
    def get_descartes(self):
        if not hasattr(self, 'descartes'):
            self.get_mod_descartes()
            self.descartes = [(x, unit_triangle_height*y) for (x,y) in self.mod_descartes]
        return self.descartes

    def get_rect_box(self):
        if not hasattr(self, 'descartes'):
            self.get_mod_descartes()
        min_x = min([uu[0] for uu in self.mod_descartes])
        max_x = max([uu[0] for uu in self.mod_descartes])
        min_y = min([uu[1] for uu in self.mod_descartes])
        max_y = max([uu[1] for uu in self.mod_descartes])
        return (min_x, max_x, min_y, max_y)

    def get_signed_area(self):
        if not hasattr(self, 'signed_area'):
            self.get_descartes()
            N = len(self.descartes)
            area = 0
            for i in range(0, N - 1):
                area += self.descartes[i][0]*self.descartes[i+1][1] - self.descartes[i][1]*self.descartes[i+1][0]
            area += self.descartes[N-1][0]*self.descartes[0][1] - self.descartes[N-1][1]*self.descartes[0][0]
            # convert from square units into the small triangle units
            result = (area/2)/unit_triangle_area
            self.signed_area = int(round(result))
        return self.signed_area

    def get_area(self):
        if not hasattr(self, 'area'):
            self.get_signed_area()
            self.area = abs(self.signed_area)
        return self.area

    def get_perimeter(self):
        if not hasattr(self, 'perimeter'):
            self.perimeter = sum([L for (L, D) in self.sides])
        return self.perimeter

    def get_bounding_hexagon(self):
        if not hasattr(self, 'bounding_hexagon'):
            self.get_vertices()
            a_min = min([p.y for p in self.vertices])
            a_max = max([p.y for p in self.vertices])

            b_min = min([p.z for p in self.vertices])
            b_max = max([p.z for p in self.vertices])

            c_min = min([p.x for p in self.vertices])
            c_max = max([p.x for p in self.vertices])
            self.bounding_hexagon = (a_min, a_max, b_min, b_max, c_min, c_max)

        return self.bounding_hexagon

    def get_bounding_sizes(self):
        if not hasattr(self, 'bounding_sizes'):
            (a_min, a_max, b_min, b_max, c_min, c_max) = self.get_bounding_hexagon()
            self.bounding_sizes = (a_max - a_min, b_max - b_min, c_max - c_min)
        return self.bounding_sizes

    # Return (a,b,c) showing the length totals for the polyiamond's sides in all 3 directions.
    def get_direction_counts(self):
        if not hasattr(self, 'direction_counts'):
            aa, bb, cc = 0, 0, 0
            for (L, D) in self.sides:
                if D in ['A','D']:
                    aa += L
                elif D in ['B', 'E']:
                    bb += L
                else:
                    cc += L
            self.direction_counts = (aa,bb,cc)
        return self.direction_counts

    # Do not store perimeter with the object
    def list_perimeter(self):
        curr_point = PointTg(0,0,0)
        result = []
        for (L, D) in self.sides:
            vect = PointTg.get_direction(D)
            for i in range(L):
                curr_point += vect
                result.append(curr_point)
        return result

    # Ray casting algorithm to check, if "pt" is
    # inside the polygon represented by "self".
    # def is_inside1(self, pt):
    #     # self.get_vertices()
    #     vertices = [vv.get_xy() for vv in self.vertices]
    #     (x, y) = pt.get_xy()
    #     print('vertices = {}'.format(vertices))
    #     print('pt = {},{}'.format(x,y))
    #     count = 0
    #     p1x, p1y = vertices[0]
    #     for i in range(1, len(vertices) + 1):
    #         p2x, p2y = vertices[i % len(vertices)]
    #         if y > min(p1y, p2y):
    #             if y <= max(p1y, p2y):
    #                 if x <= max(p1x, p2x):
    #                     if p1y != p2y:
    #                         xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
    #                     if p1x == p2x or x <= xinters:
    #                         count += 1
    #         p1x, p1y = p2x, p2y
    #     if count % 2 == 0:
    #         return False
    #     else:
    #         return True

    def winding_number(self, pt):
        vertices = [vv.get_xy() for vv in self.vertices]
        (x, y) = pt.get_xy()
        sum_angle = 0.0

        for i in range(len(vertices)):
            dx1, dy1 = vertices[i][0] - x, vertices[i][1] - y
            dx2, dy2 = vertices[(i + 1) % len(vertices)][0] - x, vertices[(i + 1) % len(vertices)][1] - y
            angle1 = math.atan2(dy1, dx1)
            angle2 = math.atan2(dy2, dx2)
            da = angle1 - angle2
            if da <= -math.pi:
                da += 2 * math.pi
            elif da > math.pi:
                da -= 2 * math.pi
            sum_angle += da
        return round(sum_angle / (2 * math.pi))


    # Winding-number based algorithm to find out, if "pt" is
    # inside the polygon represented by "self".
    # def is_inside2(self, pt):
    #     winding_number = self.winding_number(pt)
    #     return winding_number != 0


    def is_inside(self, pt):
        vertices = [vv.get_xy() for vv in self.vertices]
        (x, y) = pt.get_xy()
        pp = Point(x, y)
        poly = Polygon(vertices)
        cond1 = poly.contains(pp)
        cond2 = True
        for i in range(len(vertices)):
            v1 = vertices[i]
            v2 = vertices[(i+1)%len(vertices)]
            line = LineString([v1, v2])
            if pp.distance(line) < 1e-07:
                cond2 = False
                break
        return cond1 and cond2

    # Return triplet (diam, i_max, j_max) - the diameter for a set of points and where it was achieved
    def diameter(self):
        vertices = [vv.get_xy() for vv in self.vertices]
        diam, i_max, j_max = 0, -1, -1
        for i in range(len(vertices)):
            for j in range(i+1, len(vertices)):
                dist = L2_dist(vertices[i], vertices[j])
                if dist > diam:
                    diam = dist
                    i_max, j_max = i, j
        return (diam, i_max, j_max)

    # Returns the minimum width: The closest possible distance between two parallel lines
    # such that all vertices are between these parallel lines (or on these lines).
    def min_width(self):
        vertices = [vv.get_xy() for vv in self.vertices]
        hull = ConvexHull(vertices)
        convex_vertices = [vertices[i] for i in hull.vertices]
        pol = Polygon(convex_vertices)

        # the rotating calipers algorithm needs the vertices ordered by angle
        sorted_vertices = sorted(pol.exterior.coords[:-1])
        # initialize min_width variable as infinity
        min_width = float('inf')
        seg_min_width = [0, 0]

        n = len(sorted_vertices)
        for i in range(n):
            # Create a LineString from a pair of vertices
            line = LineString([sorted_vertices[i], sorted_vertices[(i + 1) % n]])

            # 180 deg rotation to compute parallel line through opposite vertex
            # rotated_line = rotate(line, 180, sorted_vertices[i])
            rotated_line = affinity.rotate(line, 180, sorted_vertices[i])

            # Find the closest point on the rotated line to the opposite vertex
            closest_point = rotated_line.interpolate(rotated_line.project(Point(sorted_vertices[(i + n // 2) % n])))

            # Compute the distance between the vertex and its closest point on the rotated line
            width = Point(sorted_vertices[i]).distance(closest_point)

            # Update min_width and seg_min_width if the width is smaller than min_width
            if width < min_width:
                min_width = width
                seg_min_width = [sorted_vertices[i], (closest_point.x, closest_point.y)]

        return min_width, seg_min_width

    def width(self):
        vertices = [vv.get_xy() for vv in self.vertices]
        vertice_lists = [[x,y] for (x,y) in vertices]
        return minimum_width(np.array(vertice_lists))

    # Return all internal+perimeter points as [PointTg, PointTg, ...]
    def list_inside(self):
        # Cache answers to avoid computing anything twice
        black_points = set()
        bad_points = set()
        gray_points = cp.copy(self.list_perimeter())
        while len(gray_points) > 0:
            current = gray_points.pop(0)
            # print('current = {}; len(gray_points) = {}'.format(current, len(gray_points)))
            for v in [AA,BB,CC,DD,EE,FF]:
                new_point = current + v
                if (new_point not in gray_points) and (new_point not in bad_points) and (new_point not in black_points):
                    if self.is_inside(new_point):
                        gray_points.append(new_point)
                    else:
                        bad_points.add(new_point)
            black_points.add(current)
        return sorted(black_points)




    # Return all contained triangles as list of triplets:
    # [(PointTg, PointTg, PointTg), (PointTg, PointTg, PointTg), ...]
    def list_triangles(self):
        inside_points = self.list_inside()
        queue = cp.copy(inside_points)
        result = set()
        while len(queue) > 0:
            curr0 = queue.pop(0)
            curr1 = curr0 + FF
            curr2 = curr0 + AA
            if curr1 in inside_points and curr2 in inside_points:
                result.add((curr0, curr1, curr2))
            curr3 = curr0 + BB
            if curr2 in inside_points and curr3 in inside_points:
                result.add((curr0, curr3, curr2))
        return sorted(result)


    # Assuming that polyiamond is 2-colored (usual parity coloring),
    # Return pair (black, white) -- the count of black and white triangles.
    # The following equality should be satisfied: black+white == area.
    # TODO: Should use list_trianles()
    def black_white(self):
        return (0,0)

    # Return a quadruplet (a,b,c,d) representing the
    # counts of internal angles by their size. They can be 60 or 120 degrees;
    # as well as -120 or -60 degrees (for vertices where polyiamond is not convex).
    def internal_angles(self):
        (a60, a120, a240, a300) = (0,0,0,0)
        signed_area = self.get_signed_area()
        orientation = int(abs(signed_area)/signed_area)
        for i in range(0, len(self.sides)):
            side1 = self.sides[i][1]
            side2 = self.sides[(i+1) % len(self.sides)][1]
            signed_angle = orientation*PointTg.ANGLES[(side1, side2)]
            if signed_angle == 60:
                a60 += 1
            elif signed_angle == 120:
                a120 += 1
            elif signed_angle == -120:
                a240 += 1
            else:
                a300 += 1
        return (a60, a120, a240, a300)

    @staticmethod
    def find_fragments_cfg(sides):
        n = len(sides)
        D = dict()
        result = []
        for i in range(n, 0, -1):
            for j in range(i-1, -1, -1):
                x = sides[j:i]
                # result.append(x)
                px = InductiveSplits.p(x)

                # skip zero-sequences
                if (px == PointTg(0,0,0)):
                    continue
                # skip sequences that cannot concatenate as polyiamonds:
                if x[0] == x[-1]:
                    continue
                if DIRECTIONS[x[0]] + DIRECTIONS[x[-1]] == PointTg(0,0,0):
                    continue

                x_px = abs(i-j)*px
                if x_px in D:
                    D[x_px].append((x,j,i))
                else:
                    D[x_px] = [(x, i, j)]
                pv = px
                for xlen in range(1, n):
                    searchkey = (-2*xlen - abs(i-j))*px
                    if not searchkey in D:
                        continue
                    for (x2, j2, i2) in D[searchkey]:
                        if xlen == (i2-j2) and j2 >= i:
                            u2 = sides[0:j]
                            v2 = x
                            w2 = sides[i:j2]
                            y2 = sides[i2:]

                            AA = InductiveSplits.g(y2) + InductiveSplits.g(w2) + InductiveSplits.g(u2)
                            AA += len(y2)*InductiveSplits.p(w2)
                            AA += (len(y2) + len(w2))*InductiveSplits.p(u2)
                            # (A) g(y) + g(w) + g(u) + |y| * p(w) + (|y|+|w|) * p(u) = (0,0,0)
                            BB = InductiveSplits.g(x2)  +  InductiveSplits.g(v2)
                            BB += len(y2)*InductiveSplits.p(x2)
                            BB += len(x2)*InductiveSplits.p(w2)
                            BB += (len(y2) + len(x2) + len(w2))*InductiveSplits.p(v2)
                            BB += (len(x2) + len(v2))*InductiveSplits.p(u2)
                            # (B) g(x) + g(v) + | y | *p(x) + | x |*p(w) + (| y | + | x | + | w |) * p(v) + (| x | + | v |) * p(u) = (0, 0, 0)
                            if AA == PointTg(0,0,0) and BB == PointTg(0,0,0):
                                result.append((u2, v2, w2, x2, y2))
        return result




# A function that returns those polygons which have minimal-size bounding hexagons from polylist.
def get_minimal_bounding_sizes(polylist):
    min_item = min(polylist, key=lambda ai: ai.get_bounding_sizes())
    f_list = [ai for ai in polylist if ai.get_bounding_sizes() == min_item.get_bounding_sizes()]
    return f_list