from math import sqrt
from scipy.spatial import ConvexHull, distance_matrix
import numpy as np
from difflib import SequenceMatcher

##########################################################
## This contains some real-valued 2D geometry utilities.
## No references to PointTg or any triangle geometry here.
#############################################################

# Measure the Euclidean (L2) distance between points p1 = (x1,y1) and p2 = (x2, y2)
def L2_dist(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Compute the diameter of a set of points
def set_diameter(pt_set):
    # create a convex hull object
    hull = ConvexHull(pt_set)

    # get the vertices of the convex hull
    convex_vertices = pt_set[hull.vertices]

    # compute all pairwise distances in convex_vertices
    dist_mat = distance_matrix(convex_vertices, convex_vertices)

    # return the maximum pairwise distance
    return np.max(dist_mat)


# Levenstein distance
def longest_common_subsequence(str1, str2):
    match = SequenceMatcher(None, str1, str2).find_longest_match(0, len(str1), 0, len(str2))
    return str1[match.a: match.a + match.size]




def point_line_distance(point, line_point1, line_point2):
    return np.abs(np.cross(line_point2 - line_point1, point - line_point1)) / np.linalg.norm(line_point2 - line_point1)


def minimum_width(points):
    # Compute the convex hull of the set of points
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]

    min_width = float('inf')

    # Rotating Calipers: Iterate over hull edges to find minimum width
    for i in range(len(hull_points)):
        # Define the edge points
        p1 = hull_points[i]
        p2 = hull_points[(i + 1) % len(hull_points)]

        # Store max distance for the current edge
        max_distance = 0
        # Find the point farthest from the current edge
        for j in range(len(hull_points)):
            if j != i and j != (i + 1) % len(hull_points):
                max_distance = max(max_distance, point_line_distance(hull_points[j], p1, p2))

        # Update the minimum width found so far
        min_width = min(min_width, max_distance)

    return min_width

