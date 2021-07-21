import math
import networkx as nx
import numpy as np

def center_of_mass(shp, dims = 2):
    """
    Returns dims-dimensional center of mass of vertices in shape
    """
    com = [np.mean([shp.nodes[pt]["pos"][i] for pt in list(shp.nodes)]) \
           for i in range(dims)]
    com = np.asarray(com)
    return com

def tetrahedron(name, center, rad, shade = 1, rand = False):
    """
    Returns (possibly randomly oriented) tetrahedron shape object
    centered at 'center' with radius 'rad'.
    """
    a = 1/3
    b = np.sqrt(8/9)
    c = np.sqrt(2/9)
    d = np.sqrt(2/3)
    center = np.asarray(center)
    v0 = np.array([0,   0,  1]) + center
    v1 = np.array([-c,  d, -a]) + center
    v2 = np.array([-c, -d, -a]) + center
    v3 = np.array([b,   0, -a]) + center
    shp = shape(name = name, shade = shade, dims = 3)
    shp.add_nodes_from([(0, {'pos': v0}), (1, {'pos': v1}),
                        (2, {'pos': v2}), (3, {'pos': v3})])
    shp.add_edges_from([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
    com = center_of_mass(shp, dims = 3)
    factor = rad / np.linalg.norm(v0 - com)
    shp.scale(factor)
    if rand:
        shp.rotate3d(axis = np.random.rand(3), angle = 2*math.pi*np.random.rand())
    return shp

def cube(name, center, rad, shade = 1, rand = False):
    """
    Returns (possibly randomly oriented) cube shape object
    centered at 'center' with radius 'rad'.
    """
    center = np.asarray(center)
    v0 = np.array([ 1,  1,  1]) + center
    v1 = np.array([ 1,  1, -1]) + center
    v2 = np.array([ 1, -1,  1]) + center
    v3 = np.array([ 1, -1, -1]) + center
    v4 = np.array([-1,  1,  1]) + center
    v5 = np.array([-1,  1, -1]) + center
    v6 = np.array([-1, -1,  1]) + center
    v7 = np.array([-1, -1, -1]) + center
    shp = shape(name = name, shade = shade, dims = 3)
    shp.add_nodes_from([(0, {'pos': v0}), (1, {'pos': v1}),
                        (2, {'pos': v2}), (3, {'pos': v3}),
                        (4, {'pos': v4}), (5, {'pos': v5}),
                        (6, {'pos': v6}), (7, {'pos': v7})])
    shp.add_edges_from([(0, 1), (0, 2), (0, 4), (1, 3),
                        (1, 5), (2, 3), (2, 6), (3, 7),
                        (4, 6), (4, 5), (5, 7), (6, 7)])
    com = center_of_mass(shp, dims = 3)
    factor = rad / np.linalg.norm(v0 - com)
    shp.scale(factor)
    if rand:
        shp.rotate3d(axis = np.random.rand(3), angle = 2*math.pi*np.random.rand())
    return shp

def octahedron(name, center, rad, shade = 1, rand = False, isosceles = False):
    """
    Returns (possibly randomly oriented) octahedron shape object
    centered at 'center' with radius 'rad'.
    """
    center = np.asarray(center)
    v0 = np.array([ 1,  1, 0]) + center
    v1 = np.array([ 1, -1, 0]) + center
    v2 = np.array([-1,  1, 0]) + center
    v3 = np.array([-1, -1, 0]) + center
    if isosceles:
        v4 = np.array([0, 0,  1/np.sqrt(2)]) + center
        v5 = np.array([0, 0, -1/np.sqrt(2)]) + center
    else:
        v4 = np.array([0, 0, np.sqrt(2)]) + center
        v5 = np.array([0, 0, -np.sqrt(2)]) + center
    shp = shape(name = name, shade = shade, dims = 3)
    shp.add_nodes_from([(0, {'pos': v0}), (1, {'pos': v1}),
                        (2, {'pos': v2}), (3, {'pos': v3}),
                        (4, {'pos': v4}), (5, {'pos': v5})])
    shp.add_edges_from([(0, 1), (0, 2), (1, 3), (2, 3),
                        (0, 4), (1, 4), (2, 4), (3, 4),
                        (0, 5), (1, 5), (2, 5), (3, 5)])
    factor = rad / np.linalg.norm(v4 - shp.get_com())
    shp.scale(factor)
    if rand:
        shp.rotate3d(axis = np.random.rand(3), angle = 2*math.pi*np.random.rand())
    return shp

def icosahedron(name, center, rad, shade = 1, rand = False):
    center = np.asarray(center)
    c = 2 / (1 + np.sqrt(5))
    n = np.sqrt(1 + c**2)
    v1 =  np.array([ 0,  c, -1]) / n + center
    v2 =  np.array([ c,  1,  0]) / n + center
    v3 =  np.array([-c,  1,  0]) / n + center
    v4 =  np.array([ 0,  c,  1]) / n + center
    v5 =  np.array([ 0, -c,  1]) / n + center
    v6 =  np.array([-1,  0,  c]) / n + center
    v7 =  np.array([ 0, -c, -1]) / n + center
    v8 =  np.array([ 1,  0, -c]) / n + center
    v9 =  np.array([ 1,  0,  c]) / n + center
    v10 = np.array([-1,  0, -c]) / n + center
    v11 = np.array([ c, -1,  0]) / n + center
    v12 = np.array([-c, -1,  0]) / n + center
    shp = shape(name = name, shade = shade, dims = 3)
    shp.add_nodes_from([(1,  {'pos': v1}),  (2,  {'pos': v2}),
                        (3,  {'pos': v3}),  (4,  {'pos': v4}),
                        (5,  {'pos': v5}),  (6,  {'pos': v6}),
                        (7,  {'pos': v7}),  (8,  {'pos': v8}),
                        (9,  {'pos': v9}),  (10, {'pos': v10}),
                        (11, {'pos': v11}), (12, {'pos': v12})])
    shp.add_edges_from([(1, 2),  (1, 3),  (1, 7),  (1, 8),   (1, 10),
                        (2, 3),  (2, 4),  (2, 8),  (2, 9),   (3, 4),
                        (3, 6),  (3, 10), (4, 5),  (4, 6),   (4, 9),
                        (5, 6),  (5, 9),  (5, 11), (5, 12),  (6, 10),
                        (6, 12), (7, 8),  (7, 10), (7, 11),  (7, 12),
                        (8, 9),  (8, 11), (9, 11), (10, 12), (11, 12)])
    com = center_of_mass(shp, dims = 3)
    factor = rad / np.linalg.norm(v1 - com)
    shp.scale(factor)
    if rand:
        shp.rotate3d(axis = np.random.rand(3), angle = 2*math.pi*np.random.rand())
    return shp

def triambic_icosahedron(name, center, rad, shade = 1, retain_edges = False, rand = False):
    """
    If retain_edges is True then edges from regular icosahedron are retained.
    """
    c = 2 / (1 + np.sqrt(5))
    n = np.sqrt(1 + c**2)
    v1 =  np.array([ 0,  c, -1]) / n
    v2 =  np.array([ c,  1,  0]) / n
    v3 =  np.array([-c,  1,  0]) / n
    v4 =  np.array([ 0,  c,  1]) / n
    v5 =  np.array([ 0, -c,  1]) / n
    v6 =  np.array([-1,  0,  c]) / n
    v7 =  np.array([ 0, -c, -1]) / n
    v8 =  np.array([ 1,  0, -c]) / n
    v9 =  np.array([ 1,  0,  c]) / n
    v10 = np.array([-1,  0, -c]) / n
    v11 = np.array([ c, -1,  0]) / n
    v12 = np.array([-c, -1,  0]) / n
    shp = shape(name = name, shade = shade, dims = 3)
    shp.add_nodes_from([(1,  {'pos': v1}),  (2,  {'pos': v2}),
                        (3,  {'pos': v3}),  (4,  {'pos': v4}),
                        (5,  {'pos': v5}),  (6,  {'pos': v6}),
                        (7,  {'pos': v7}),  (8,  {'pos': v8}),
                        (9,  {'pos': v9}),  (10, {'pos': v10}),
                        (11, {'pos': v11}), (12, {'pos': v12})])
    faces = [[3, 2, 1],   [2, 3, 4],   [6, 5, 4],   [5, 9, 4],
             [8, 7, 1],   [7, 10, 1],  [12, 11, 5], [11, 12, 7],
             [10, 6, 3],  [6, 10, 12], [9, 8, 2],   [8, 9, 11],
             [3, 6, 4],   [9, 2, 4],   [10, 3, 1],  [2, 8, 1],
             [12, 10, 7], [8, 11, 7],  [6, 12, 5],  [11, 9, 5]]
    for idx, face in enumerate(faces):
        com = np.asarray([np.mean([shp.nodes[pt]["pos"][i] for pt in face]) for i in range(3)])
        new_node = (1 + 2 / np.linalg.norm(com)) * com
        shp.add_nodes_from([(idx + 13, {'pos':new_node})])
        shp.add_edges_from([(idx + 13, pt) for pt in face])
    if retain_edges:
        shp.add_edges_from([(1, 2),  (1, 3),  (1, 7),  (1, 8),   (1, 10),
                            (2, 3),  (2, 4),  (2, 8),  (2, 9),   (3, 4),
                            (3, 6),  (3, 10), (4, 5),  (4, 6),   (4, 9),
                            (5, 6),  (5, 9),  (5, 11), (5, 12),  (6, 10),
                            (6, 12), (7, 8),  (7, 10), (7, 11),  (7, 12),
                            (8, 9),  (8, 11), (9, 11), (10, 12), (11, 12)])
    center = np.asarray(center)
    shp.translate(direction = center)
    com = center_of_mass(shp, dims = 3)
    factor = rad / 3
    shp.scale(factor)
    if rand:
        shp.rotate3d(axis = np.random.rand(3), angle = 2*math.pi*np.random.rand())
    return shp

class shape(nx.Graph):
    
    def __init__(self, name, shade = 1, dims = 2, circles = None):
        super().__init__()
        self.name = name
        self.shade = shade
        self.dims = dims
        self.com = None
        self.circles = circles

    def set_shade(self, shade):
        self.shade = shade
        
    def translate(self, direction):
        for node in list(self.nodes):
            direction = np.array(direction)
            point = np.array(self.nodes[node]["pos"])
            self.nodes[node]["pos"] = point + direction
    
    def scale(self, factor, center = 'com'):
        if factor < 0:
            raise ValueError("factor must be non-negative")
        center = center_of_mass(self, dims = self.dims) \
                 if center == 'com' else np.asarray(center)
        for node in list(self.nodes):
            point = np.array(self.nodes[node]["pos"])
            outward_radial = point - center
            self.nodes[node]["pos"] = center + factor * outward_radial
    
    def rotate2d(self, origin, angle):
        
        def rotate_point(origin, point, angle):
            ox, oy = origin
            px, py = point
            qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
            qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
            return np.array([qx, qy])
        
        for node in list(self.nodes):
            self.nodes[node]["pos"] = rotate_point(origin = origin,
                                                   point = self.nodes[node]["pos"],
                                                   angle = angle)
        return self
            
    def rotate3d(self, axis, angle, center = 'com'):
        
        def rotation_matrix(axis, angle):
            """
            Euler-Rodrigues formula for rotation about an axis in 3D.
            """
            axis = np.asarray(axis)
            axis = axis / math.sqrt(np.dot(axis, axis))
            a = math.cos(angle / 2.0)
            b, c, d = -axis * math.sin(angle / 2.0)
            aa, bb, cc, dd = a * a, b * b, c * c, d * d
            bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
            return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                             [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                             [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])
        
        center = center_of_mass(self, dims = self.dims) \
                 if center == 'com' else np.asarray(center)
        rot = rotation_matrix(axis, angle)
        for node in list(self.nodes):
            point = np.array(self.nodes[node]["pos"])
            trans_pt = point - center
            self.nodes[node]["pos"] = np.dot(rot, trans_pt) + center
    
    def get_com(self):
        """
        Returns self.dims-dimensional center of mass of vertices in self
        """
        com = np.array([np.mean([self.nodes[pt]["pos"][i]     \
                                 for pt in list(self.nodes)]) \
                        for i in range(self.dims)])
        return com
