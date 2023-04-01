from itertools import product
import math
import networkx as nx
import numpy as np

from Shape import Shape
from shape_utils import center_of_mass


def tetrahedron_nx(center, rad):
    """Create tetrahedron nx.Graph."""
    a, b, c, d = 1/3, np.sqrt(8/9), np.sqrt(2/9), np.sqrt(2/3)
    center = np.asarray(center)
    vertices = [
        np.array([0, 0, 1]) + center,
        np.array([-c, d, -a]) + center,
        np.array([-c, -d, -a]) + center,
        np.array([b, 0, -a]) + center
    ]
    graph = nx.Graph()
    graph.add_nodes_from([
        (0, {"pos": vertices[0]}),
        (1, {"pos": vertices[1]}),
        (2, {"pos": vertices[2]}),
        (3, {"pos": vertices[3]})
    ])
    graph.add_edges_from([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
    return graph

def tetrahedron(name, center, rad, shade=1, rand=False):
    """Create tetrahedron Shape object."""
    cfg = {
        "name":name,
        "shade":shade,
        "dims":3,
        "graph":tetrahedron_nx(center, rad)
    }
    shp = Shape.from_nx(**cfg)
    com = center_of_mass(shp, dims=3)
    factor = rad / np.linalg.norm(shp.nodes[0]["pos"] - com)
    shp.scale(factor)

    if rand:
        shp.rotate_3d(axis=np.random.rand(3), angle=2*math.pi*np.random.rand())
    return shp

def cube_nx(center, rad):
    """Create cube nx.Graph."""
    center = np.asarray(center)
    vertices = [
        np.array([ 1, 1, 1]) + center,
        np.array([ 1, 1, -1]) + center,
        np.array([ 1, -1, 1]) + center,
        np.array([ 1, -1, -1]) + center,
        np.array([-1, 1, 1]) + center,
        np.array([-1, 1, -1]) + center,
        np.array([-1, -1, 1]) + center,
        np.array([-1, -1, -1]) + center
    ]
    graph = nx.Graph()
    graph.add_nodes_from([
        (0, {"pos": vertices[0]}),
        (1, {"pos": vertices[1]}),
        (2, {"pos": vertices[2]}),
        (3, {"pos": vertices[3]}),
        (4, {"pos": vertices[4]}),
        (5, {"pos": vertices[5]}),
        (6, {"pos": vertices[6]}),
        (7, {"pos": vertices[7]})
    ])
    graph.add_edges_from([
        (0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
        (2, 6), (3, 7), (4, 6), (4, 5), (5, 7), (6, 7)
    ])
    return graph

def cube(name, center, rad, shade=1, rand=False):
    """Create cube Shape object."""
    cfg = {
        "name":name,
        "shade":shade,
        "dims":3,
        "graph":cube_nx(center, rad)
    }
    shp = Shape.from_nx(**cfg)
    com = center_of_mass(shp, dims=3)
    factor = rad / np.linalg.norm(shp.nodes[0]["pos"] - com)
    shp.scale(factor)

    if rand:
        shp.rotate_3d(axis=np.random.rand(3), angle=2*math.pi*np.random.rand())
    return shp

def octahedron_nx(center, rad, isosceles=False):
    """Create octahedron nx.Graph."""
    center = np.asarray(center)
    vertices = [
        np.array([ 1, 1, 0]) + center,
        np.array([ 1, -1, 0]) + center,
        np.array([-1, 1, 0]) + center,
        np.array([-1, -1, 0]) + center
    ]

    z = 1/np.sqrt(2) if isosceles else np.sqrt(2)
    vertices += [np.array([0, 0, z]) + center, np.array([0, 0, -z]) + center]

    graph = nx.Graph()
    graph.add_nodes_from([
        (0, {"pos": vertices[0]}),
        (1, {"pos": vertices[1]}),
        (2, {"pos": vertices[2]}),
        (3, {"pos": vertices[3]}),
        (4, {"pos": vertices[4]}),
        (5, {"pos": vertices[5]})
    ])
    graph.add_edges_from([
        (0, 1), (0, 2), (0, 4), (0, 5), (1, 3), (1, 4),
        (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5)
    ])
    return graph

def octahedron(name, center, rad, shade=1, rand=False, isosceles=False):
    """Create octahedron Shape object."""
    cfg = {
        "name":name,
        "shade":shade,
        "dims":3,
        "graph":octahedron_nx(center, rad, isosceles)
    }
    shp = Shape.from_nx(**cfg)
    factor = rad / np.linalg.norm(shp.nodes[0]["pos"] - shp.get_com())
    shp.scale(factor)

    if rand:
        shp.rotate_3d(axis=np.random.rand(3), angle=2*math.pi*np.random.rand())
    return shp

def dodecahedron_nx(center, rad):
    """Create dodecahedron nx.Graph."""
    c = 2/(1 + np.sqrt(5))
    n = np.sqrt(1 + c*c)
    ico_nodes = {
        0:np.array([ 0, c, -1]) / n,
        1:np.array([ c, 1, 0]) / n,
        2:np.array([-c, 1, 0]) / n,
        3:np.array([ 0, c, 1]) / n,
        4:np.array([ 0, -c, 1]) / n,
        5:np.array([-1, 0, c]) / n,
        6:np.array([ 0, -c, -1]) / n,
        7:np.array([ 1, 0, -c]) / n,
        8:np.array([ 1, 0, c]) / n,
        9:np.array([-1, 0, -c]) / n,
        10:np.array([ c, -1, 0]) / n,
        11:np.array([-c, -1, 0]) / n
    }
    graph = nx.Graph()
    faces = [
        [0, 1, 2],
        [0, 1, 7],
        [0, 2, 9],
        [0, 6, 7],
        [0, 6, 9],
        [1, 2, 3],
        [1, 3, 8],
        [1, 7, 8],
        [2, 3, 5],
        [2, 5, 9],
        [3, 4, 5],
        [3, 4, 8],
        [4, 5, 11],
        [4, 8, 10],
        [4, 10, 11],
        [5, 9, 11],
        [6, 7, 10],
        [6, 9, 11],
        [6, 10, 11],
        [7, 8, 10]
    ]
    n_faces = len(faces)

    centers_of_mass = [
        np.array(
            [np.mean([ico_nodes[j][k] for j in faces[i]]) for k in range(3)]
        )
        for i in range(n_faces)
    ]

    dodec_nodes = [node/np.linalg.norm(node) for node in centers_of_mass]
    duals = {i:faces[i] for i in range(n_faces)}
    graph.add_nodes_from([(i, {"pos":dodec_nodes[i]}) for i in range(n_faces)])

    for i, j in product(duals, duals):
        if len(set(duals[i]) & set(duals[j])) == 2:
            graph.add_edge(i, j)

    return graph

def dodecahedron(name, center, rad, shade=1, rand=False):
    """Create dodecahedron Shape object."""
    cfg = {
        "name":name,
        "shade":shade,
        "dims":3,
        "graph":dodecahedron_nx(center, rad)
    }
    shp = Shape.from_nx(**cfg)

    center = np.asarray(center)
    shp.translate(direction=center)
    com = center_of_mass(shp, dims=3)
    factor = rad / np.linalg.norm(shp.nodes[0]["pos"] - com)
    shp.scale(factor)

    if rand:
        shp.rotate_3d(axis=np.random.rand(3), angle=2*math.pi*np.random.rand())
    return shp

def icosahedron_nx(center, rad):
    """Create icosahedron nx.Graph."""
    center = np.asarray(center)
    c = 2 / (1 + np.sqrt(5))
    n = np.sqrt(1 + c*c)
    vertices = [
        np.array([ 0, c, -1]) / n + center,
        np.array([ c, 1, 0]) / n + center,
        np.array([-c, 1, 0]) / n + center,
        np.array([ 0, c, 1]) / n + center,
        np.array([ 0, -c, 1]) / n + center,
        np.array([-1, 0, c]) / n + center,
        np.array([ 0, -c, -1]) / n + center,
        np.array([ 1, 0, -c]) / n + center,
        np.array([ 1, 0, c]) / n + center,
        np.array([-1, 0, -c]) / n + center,
        np.array([ c, -1, 0]) / n + center,
        np.array([-c, -1, 0]) / n + center
    ]

    graph = nx.Graph()
    graph.add_nodes_from([
        (0, {"pos": vertices[0]}),
        (1, {"pos": vertices[1]}),
        (2, {"pos": vertices[2]}),
        (3, {"pos": vertices[3]}),
        (4, {"pos": vertices[4]}),
        (5, {"pos": vertices[5]}),
        (6, {"pos": vertices[6]}),
        (7, {"pos": vertices[7]}),
        (8, {"pos": vertices[8]}),
        (9, {"pos": vertices[9]}),
        (10, {"pos": vertices[10]}),
        (11, {"pos": vertices[11]})
    ])
    graph.add_edges_from([
        (0, 1), (0, 2), (0, 6), (0, 7), (0, 9), (1, 2),
        (1, 3), (1, 7), (1, 8), (2, 3), (2, 5), (2, 9),
        (3, 4), (3, 5), (3, 8), (4, 5), (4, 8), (4, 10),
        (4, 11), (5, 9), (5, 11), (6, 7), (6, 9), (6, 10),
        (6, 11), (7, 8), (7, 10), (8, 10), (9, 11), (10, 11)
    ])

    return graph

def icosahedron(name, center, rad, shade=1, rand=False):
    """Create icosahedron Shape object."""
    cfg = {
        "name":name,
        "shade":shade,
        "dims":3,
        "graph":icosahedron_nx(center, rad)
    }
    shp = Shape.from_nx(**cfg)
    com = center_of_mass(shp, dims=3)
    factor = rad / np.linalg.norm(shp.nodes[0]["pos"] - com)
    shp.scale(factor)

    if rand:
        shp.rotate_3d(axis=np.random.rand(3), angle=2*math.pi*np.random.rand())
    return shp

def triambic_icosahedron_nx(center, rad, keep_edges=False):
    """Create icosahedron nx.Graph. If keep_edges, then edges of regular
    icosahedron are retained."""
    c = 2 / (1 + np.sqrt(5))
    n = np.sqrt(1 + c*c)
    vertices = [
        np.array([ 0, c, -1]) / n,
        np.array([ c, 1, 0]) / n,
        np.array([-c, 1, 0]) / n,
        np.array([ 0, c, 1]) / n,
        np.array([ 0, -c, 1]) / n,
        np.array([-1, 0, c]) / n,
        np.array([ 0, -c, -1]) / n,
        np.array([ 1, 0, -c]) / n,
        np.array([ 1, 0, c]) / n,
        np.array([-1, 0, -c]) / n,
        np.array([ c, -1, 0]) / n,
        np.array([-c, -1, 0]) / n
    ]

    graph = nx.Graph()
    graph.add_nodes_from([
        (0, {"pos": vertices[0]}),
        (1, {"pos": vertices[1]}),
        (2, {"pos": vertices[2]}),
        (3, {"pos": vertices[3]}),
        (4, {"pos": vertices[4]}),
        (5, {"pos": vertices[5]}),
        (6, {"pos": vertices[6]}),
        (7, {"pos": vertices[7]}),
        (8, {"pos": vertices[8]}),
        (9, {"pos": vertices[9]}),
        (10, {"pos": vertices[10]}),
        (11, {"pos": vertices[11]})
    ])
    faces = [
        [0, 1, 2],
        [0, 1, 7],
        [0, 2, 9],
        [0, 6, 7],
        [0, 6, 9],
        [1, 2, 3],
        [1, 3, 8],
        [1, 7, 8],
        [2, 3, 5],
        [2, 5, 9],
        [3, 4, 5],
        [3, 4, 8],
        [4, 5, 11],
        [4, 8, 10],
        [4, 10, 11],
        [5, 9, 11],
        [6, 7, 10],
        [6, 9, 11],
        [6, 10, 11],
        [7, 8, 10]
    ]

    for idx, face in enumerate(faces):
        com = np.asarray([
            np.mean([graph.nodes[pt]["pos"][i] for pt in face])
            for i in range(3)
        ])
        new_node = (1 + 2 / np.linalg.norm(com)) * com
        graph.add_nodes_from([(idx + 12, {"pos":new_node})])
        graph.add_edges_from([(idx + 12, pt) for pt in face])

    if keep_edges:
        graph.add_edges_from([
            (0, 1), (0, 2), (0, 6), (0, 7), (0, 9),
            (1, 2), (1, 3), (1, 7), (1, 8), (2, 3),
            (2, 5), (2, 9), (3, 4), (3, 5), (3, 8),
            (4, 5), (4, 8), (4, 10), (4, 11), (5, 9),
            (5, 11), (6, 7), (6, 9), (6, 10), (6, 11),
            (7, 8), (7, 10), (8, 10), (9, 11), (10, 11)
        ])

    return graph

def triambic_icosahedron(
    name,
    center,
    rad,
    shade=1,
    rand=False,
    keep_edges=False
):
    """Create icosahedron Shape object. If keep_edges, then edges of regular
    icosahedron are retained."""
    cfg = {
        "name":name,
        "shade":shade,
        "dims":3,
        "graph":triambic_icosahedron_nx(center, rad, keep_edges)
    }
    shp = Shape.from_nx(**cfg)
    center = np.asarray(center)
    shp.translate(direction=center)
    com = center_of_mass(shp, dims=3)
    factor = rad / 3
    shp.scale(factor)

    if rand:
        shp.rotate_3d(axis=np.random.rand(3), angle=2*math.pi*np.random.rand())
    return shp
