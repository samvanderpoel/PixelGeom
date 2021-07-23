import functools
import math
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from shape import *

def gradient(x, dim):
    # Used in paint_canvas method
    idx, val = x
    temp_val = 1-idx[0]/(dim[0]-1)-idx[1]/(dim[1]-1)
    return [idx, (temp_val+1)/2]

def radial(x, dim):
    # Used in paint_canvas method
    idx, val = x
    return [idx, 1 - abs(0.50-idx[0]/(dim[0]-1)) - abs(0.50-idx[1]/(dim[1]-1))]

def white(x, dim):
    # Used in paint_canvas method
    idx, val = x
    return [idx, 0]

def black(x, dim):
    # Used in paint_canvas method
    idx, val = x
    return [idx, 1]

def uniform_shade(x, shade):
    # Used in paint_canvas method
    idx, val = x
    return [idx, shade]

def draw_edge(arr, v1, v2, dim, shade = 1):
    """
    Detects and replaces entries in array 'arr' that are pieced by the
    segment (v1, v2) with the quantity 'shade'. 'dim' is used to
    determine how finely to search for pieced entries.

    Used in draw_shapes method.
    """
    v1, v2 = np.array(v1), np.array(v2)
    for i in np.linspace(0, 1, num = max(dim)):
        u = v1 + i*(v2-v1)
        if round(u[0]) < 0 or math.ceil(u[1]) < 0 or math.floor(u[1]) < 0:
            continue
        try:
            if all([d > 200 for d in dim]):
                arr[round(u[0]), int(math.ceil(u[1]))] = shade
                arr[round(u[0]), int(math.floor(u[1]))] = shade
            else:
                arr[round(u[0]), round(u[1])] = shade
        except:
            continue
    return arr

def projection(shp, node, griddim, proj = 'persp'):
    """
    Perspective projection or orthographic projection of the point
    'node' onto the x-y plane. Camera position (xc, yc) is taken to
    be the center of mass of the shape.

    Used in draw_shapes method.
    """
    x, y, z = np.array(shp.nodes[node]["pos"])
    if proj == 'persp':
        xc, yc, zc = center_of_mass(shp, dims = shp.dims)
        xp = (max(griddim)/(max(griddim)+2*abs(zc))) * (x-xc) + xc
        yp = (max(griddim)/(max(griddim)+2*abs(zc))) * (y-yc) + yc
        return (xp, yp)
    elif proj == 'ortho':
        return (x, y)

def rgb_to_cmap(colors, penlow = None, penhigh = None):
    """
    Returns a matplotlib.cm object that evenly spaces colors in 'colors' (which
    should be a list of RGB-denoted colors) and specifies pen colors 'penlow'
    (corresponding with shade 0.0) and 'penhigh' (corresponding with shade 1.0).

    Use optionally in development.
    """
    colors = np.asarray(colors) / 255
    penlow = np.asarray(penlow) / 255 if penlow is not None else None
    penhigh = np.asarray(penhigh) / 255 if penhigh is not None else None
    red, green, blue = [], [], []
    low = 0 if penlow is None else 0.001
    high = 1 if penhigh is None else 0.999
    incrs = np.linspace(low, high, num = 2*len(colors)-1)
    for idx, color in enumerate(colors):
        red.append(  [incrs[2*idx], color[0], color[0]])
        green.append([incrs[2*idx], color[1], color[1]])
        blue.append( [incrs[2*idx], color[2], color[2]])
        if idx is not len(colors)-1:
            red.append(  [incrs[2*idx+1], (color[0]+colors[idx+1][0])/2, (color[0]+colors[idx+1][0])/2])
            green.append([incrs[2*idx+1], (color[1]+colors[idx+1][1])/2, (color[1]+colors[idx+1][1])/2])
            blue.append( [incrs[2*idx+1], (color[2]+colors[idx+1][2])/2, (color[2]+colors[idx+1][2])/2])
    if penlow is not None:
        red.insert(0, [0.0, penlow[0], penlow[0]])
        green.insert(0, [0.0, penlow[1], penlow[1]])
        blue.insert(0, [0.0, penlow[2], penlow[2]])
    if penhigh is not None:
        red.append([1.0, penhigh[0], penhigh[0]])
        green.append([1.0, penhigh[1], penhigh[1]])
        blue.append([1.0, penhigh[2], penhigh[2]])
    cdict = {'red':tuple(tuple(x) for x in red),
             'green':tuple(tuple(x) for x in green),
             'blue':tuple(tuple(x) for x in blue)}
    return LinearSegmentedColormap('custom', cdict)

class grid:
    
    # initialize grid object
    def __init__(self, shapes, dim, zerobottomleft = True):
        if not isinstance(shapes, list):
            raise TypeError("shapes must be supplied in a list")
        if not isinstance(dim, tuple):
            raise TypeError("dim must be a tuple of length at least 2")
        self.shapes = {shape.name:shape for shape in shapes}
        self.dim = np.array(dim)
        self.canvas = np.zeros(dim)
        self.gridarr = np.zeros(dim)
        self.gridcur = 'white'
        self.zerobottomleft = zerobottomleft
    
    def add_shape(self, shp):
        self.shapes[shp.name] = shp
    
    def del_shape(self, shp):
        del self.shapes[shp.name]
        
    def scale_shape(self, name, factor):
        self.shapes[name].scale(factor = factor)
    
    def rotate_shape2d(self, name, origin, angle):
        self.shapes[name].rotate2d(origin = origin, angle = angle)
        
    def rotate_shape3d(self, name, axis, angle, center = 'com'):
        self.shapes[name].rotate3d(center = center, axis = axis, angle = angle)
        
    def translate_shape(self, name, direction):
        self.shapes[name].translate(direction = direction)
    
    def paint_canvas(self, paint = 'white'):
        try:
            if paint < 0 or paint > 1:
                Warning("Uniform shade should be between 0 and 1. Plot may not appear as intended.")
            enum = map(functools.partial(uniform_shade, shade = paint), np.ndenumerate(self.canvas))
        except:
            paint_types = {'gradient':gradient, 'radial':radial, 'white':white, 'black':black}
            func = paint_types[paint]
            enum = map(functools.partial(func, dim=self.dim), np.ndenumerate(self.canvas))
        for idx, val in enum:
            val = 0.005 if val < 0.005 else val
            val = 0.995 if val > 0.995 else val
            self.canvas[idx] = val
        self.gridcur = paint
        
    def draw_shapes(self, shapes = 'all', proj = 'persp'):
        shapes = [name for name in self.shapes] if shapes=='all' else shapes
        gridout = np.array(self.canvas)
        for name in shapes:
            shp = self.shapes[name]
            if shp.dims == 2:
                edges = [(shp.nodes[edge[0]]["pos"], shp.nodes[edge[1]]["pos"]) \
                         for edge in list(shp.edges)]
            elif shp.dims == 3:
                if proj == 'persp':
                    edges = [(projection(shp, edge[0], griddim = self.dim, proj = 'persp'), \
                              projection(shp, edge[1], griddim = self.dim, proj = 'persp')) \
                             for edge in list(shp.edges)]
                elif proj == 'ortho':
                    edges = [(projection(shp, edge[0], griddim = self.dim, proj = 'ortho'), \
                              projection(shp, edge[1], griddim = self.dim, proj = 'ortho')) \
                             for edge in list(shp.edges)]
            for edge in edges:
                p1, p2 = edge
                gridout = draw_edge(gridout, p1, p2, dim=self.dim, shade = shp.shade)
        self.gridarr = gridout

    def plot_grid(self, filename = None, cmap = 'Greys', dpi = 500):
        gridout = np.rot90(self.gridarr) if self.zerobottomleft else self.gridarr
        fig, ax = plt.subplots(1, figsize=(5, 5), dpi=dpi)
        ax.imshow(gridout, cmap=cmap, interpolation='None', vmin=0, vmax=1)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        ax.axis('off')
        fig.subplots_adjust(right=1.00, left=0.00, bottom=0.00, top=1.00)
        if filename is not None:
            fig.savefig(filename, dpi=dpi)
        plt.close()
