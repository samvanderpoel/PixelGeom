import math
import numpy as np


def center_of_mass(shp, dims=2):
    """Get dims-dimensional center of mass of vertices in an nx.Graph"""
    com = np.asarray([
        np.mean([shp.nodes[pt]["pos"][i] for pt in list(shp.nodes)])
        for i in range(dims)
    ])
    return com

def rotate_point_2d(origin, point, angle):
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(angle)*(px - ox) - math.sin(angle)*(py - oy)
    qy = oy + math.sin(angle)*(px - ox) + math.cos(angle)*(py - oy)
    return np.array([qx, qy])

def rotation_matrix(axis, angle):
    """Euler-Rodrigues formula for rotation about axis in 3D."""
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(angle/2)
    b, c, d = -axis * math.sin(angle/2)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d

    return np.array([
        [aa + bb - cc - dd, 2*(bc + ad), 2*(bd - ac)],
        [2*(bc - ad), aa + cc - bb - dd, 2*(cd + ab)],
        [2*(bd + ac), 2*(cd - ab), aa + dd - bb - cc]
    ])
