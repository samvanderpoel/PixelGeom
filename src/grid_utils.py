import math
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

from shape_utils import center_of_mass


def rgb_to_cmap(colors, penlow=None, penhigh=None):
    """Returns a matplotlib.cm object that evenly spaces `colors` and includes
    optional 'pen' colors at shades [0,0.001) and (0.999, 1] of the cmap.

    Args:
        colors: a list of colors in RGB format, i.e. from 0-255
        penlow: an RGB color specifying the color of 'pen' at shade 0
        penlow: an RGB color specifying the color of 'pen' at shade 1
    """
    colors = np.asarray(colors) / 255
    penlow = np.asarray(penlow) / 255 if penlow is not None else None
    penhigh = np.asarray(penhigh) / 255 if penhigh is not None else None
    red, green, blue = [], [], []
    low = 0 if penlow is None else 0.001
    high = 1 if penhigh is None else 0.999
    incrs = np.linspace(low, high, num = 2*len(colors)-1)

    for idx, color in enumerate(colors):
        red.append([incrs[2*idx], color[0], color[0]])
        green.append([incrs[2*idx], color[1], color[1]])
        blue.append([incrs[2*idx], color[2], color[2]])
        
        if idx is not len(colors)-1:
            red.append([
                incrs[2*idx+1],
                (color[0]+colors[idx+1][0])/2,
                (color[0]+colors[idx+1][0])/2
            ])
            green.append([
                incrs[2*idx+1],
                (color[1]+colors[idx+1][1])/2,
                (color[1]+colors[idx+1][1])/2
            ])
            blue.append([
                incrs[2*idx+1],
                (color[2]+colors[idx+1][2])/2,
                (color[2]+colors[idx+1][2])/2
            ])

    if penlow is not None:
        red.insert(0, [0.0, penlow[0], penlow[0]])
        green.insert(0, [0.0, penlow[1], penlow[1]])
        blue.insert(0, [0.0, penlow[2], penlow[2]])

    if penhigh is not None:
        red.append([1.0, penhigh[0], penhigh[0]])
        green.append([1.0, penhigh[1], penhigh[1]])
        blue.append([1.0, penhigh[2], penhigh[2]])

    cdict = {
        "red":tuple(tuple(x) for x in red),
        "green":tuple(tuple(x) for x in green),
        "blue":tuple(tuple(x) for x in blue)
    }
    return LinearSegmentedColormap("custom", cdict)

def draw_edge(arr, v1, v2, dim, shade=1):
    """Detects and replaces entries in array "arr" that are pierced by the
    segment (v1, v2) with the quantity "shade". "dim" is used to determine how
    finely to search for pieced entries."""
    v1, v2 = np.array(v1), np.array(v2)

    for i in np.linspace(0, 1, num=max(dim)):
        u = v1 + i*(v2-v1)
        if u[0]<0 or u[1]<0 or u[0]>dim[0]-1 or u[1]>dim[1]-1:
            continue
        if all([d > 200 for d in dim]):
            arr[round(u[0]), int(math.ceil(u[1]))] = shade
            arr[round(u[0]), int(math.floor(u[1]))] = shade
        else:
            arr[round(u[0]), round(u[1])] = shade

    return arr

def draw_face(arr, face, dim, shade):
    """Draws face on 2D array given the corresponding vertices and shade. For
    3D drawings, only projected vertices must be passed."""
    pass

def projection(shp, node, griddim, proj="persp"):
    """Orthographic projection followed by a scaling of the point "node" onto
    the x-y plane. Camera position (xc, yc) is taken to be the center of mass
    of the shape. Used in draw_shapes method."""
    x, y, z = np.array(shp.nodes[node]["pos"])

    if proj == "persp":
        xc, yc, zc = center_of_mass(shp, dims = shp.dims)
        xp = (max(griddim)/(max(griddim)+2*abs(zc))) * (x-xc) + xc
        yp = (max(griddim)/(max(griddim)+2*abs(zc))) * (y-yc) + yc
        return (xp, yp)
    elif proj == "ortho":
        return (x, y)

def gradient(x, dim):
    idx, val = x
    temp_val = 1-idx[0]/(dim[0]-1)-idx[1]/(dim[1]-1)
    return [idx, (temp_val+1)/2]

def radial(x, dim):
    idx, val = x
    return [idx, 1 - abs(0.50-idx[0]/(dim[0]-1)) - abs(0.50-idx[1]/(dim[1]-1))]

def white(x, dim):
    idx, val = x
    return [idx, 0]

def black(x, dim):
    idx, val = x
    return [idx, 1]

def uniform_shade(x, shade):
    idx, val = x
    return [idx, shade]
