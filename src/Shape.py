import networkx as nx
import numpy as np

from shape_utils import center_of_mass, rotate_point_2d, rotation_matrix


class Shape(nx.Graph):

    def __init__(self, name, shade=1, dims=2):
        super().__init__()
        self.name = name
        self.shade = shade
        self.dims = dims
        self.com = None

    @classmethod
    def from_nx(cls, graph, **kwargs):
        shape = cls(**kwargs)
        shape.add_nodes_from([(i, graph.nodes[i]) for i in graph.nodes])
        shape.add_edges_from(list(graph.edges))
        return shape

    def set_shade(self, shade):
        self.shade = shade
        
    def translate(self, direction):
        for node in list(self.nodes):
            direction = np.array(direction)
            point = np.array(self.nodes[node]["pos"])
            self.nodes[node]["pos"] = point + direction
    
    def scale(self, factor, center = "com"):
        assert factor >= 0, "factor must be non-negative"

        center = (
            center_of_mass(self, dims=self.dims)
            if center == "com"
            else np.asarray(center)
        )
        for node in list(self.nodes):
            point = np.array(self.nodes[node]["pos"])
            outward_radial = point - center
            self.nodes[node]["pos"] = center + factor * outward_radial
    
    def rotate_2d(self, origin, angle):
        for node in list(self.nodes):
            self.nodes[node]["pos"] = rotate_point_2d(
                origin = origin,
                point = self.nodes[node]["pos"],
                angle = angle
            )
        return self
            
    def rotate_3d(self, axis, angle, center="com"):
        center = (
            center_of_mass(self, dims=self.dims)
            if center == "com"
            else np.asarray(center)
        )
        rot = rotation_matrix(axis, angle)
        for node in list(self.nodes):
            point = np.array(self.nodes[node]["pos"])
            trans_pt = point - center
            self.nodes[node]["pos"] = np.dot(rot, trans_pt) + center
    
    def get_com(self):
        """Get dims-dimensional center of mass of vertices in self"""
        return center_of_mass(self, self.dims)
