import functools
import matplotlib.pyplot as plt
import numpy as np

from grid_utils import *
from Shape import Shape
from shape_utils import center_of_mass


class Grid:

    def __init__(self, shapes, dim, zerobottomleft=True):
        assert isinstance(shapes, list), "shapes must be in a list"
        assert isinstance(dim, tuple), "dim must be tuple of length >= 2"

        self.shapes = {shape.name:shape for shape in shapes}
        self.dim = np.array(dim)
        self.canvas = np.zeros(dim)
        self.gridarr = np.zeros(dim)
        self.gridcur = "white"
        self.zerobottomleft = zerobottomleft
    
    def add_shape(self, shp):
        self.shapes[shp.name] = shp
    
    def del_shape(self, shp):
        del self.shapes[shp.name]
        
    def scale_shape(self, name, factor):
        self.shapes[name].scale(factor=factor)
    
    def rotate_shape_2d(self, name, origin, angle):
        self.shapes[name].rotate_2d(origin=origin, angle=angle)
        
    def rotate_shape_3d(self, name, axis, angle, center="com"):
        self.shapes[name].rotate_3d(center=center, axis=axis, angle=angle)
        
    def translate_shape(self, name, direction):
        self.shapes[name].translate(direction=direction)
    
    def paint_canvas(self, paint="white"):
        try:
            if paint < 0 or paint > 1:
                Warning(
                    "Uniform shade should be between 0 and 1."
                    "Plot may not appear as intended."
                )
            enum = map(
                functools.partial(uniform_shade, shade=paint),
                np.ndenumerate(self.canvas)
            )
        except:
            paint_types = {
                "gradient":gradient,
                "radial":radial,
                "white":white,
                "black":black
            }
            func = paint_types[paint]
            enum = map(
                functools.partial(func, dim=self.dim),
                np.ndenumerate(self.canvas)
            )

        for idx, val in enum:
            val = 0.005 if val < 0.005 else val
            val = 0.995 if val > 0.995 else val
            self.canvas[idx] = val

        self.gridcur = paint
        
    def draw_shapes(self, shapes="all", proj="persp"):
        shapes = [name for name in self.shapes] if shapes=="all" else shapes
        gridout = np.array(self.canvas)

        for name in shapes:
            shp = self.shapes[name]
            if shp.dims == 2:
                edges = [
                    (shp.nodes[edge[0]]["pos"], shp.nodes[edge[1]]["pos"])
                    for edge in list(shp.edges)
                ]
            elif shp.dims == 3:
                edges = [
                    (
                        projection(shp, edge[0], griddim=self.dim, proj=proj),
                        projection(shp, edge[1], griddim=self.dim, proj=proj)
                    )
                    for edge in list(shp.edges)
                ]

            for edge in edges:
                p1, p2 = edge
                gridout = draw_edge(gridout, p1, p2, dim=self.dim, shade=shp.shade)

        self.gridarr = gridout

    def plot_grid(self, filename=None, cmap="Greys", dpi=500):
        gridout = np.rot90(self.gridarr) if self.zerobottomleft else self.gridarr
        fig, ax = plt.subplots(1, figsize=(5, 5), dpi=dpi)
        ax.imshow(gridout, cmap=cmap, interpolation="None", vmin=0, vmax=1)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        ax.axis("off")
        fig.subplots_adjust(right=1.00, left=0.00, bottom=0.00, top=1.00)

        if filename is not None:
            fig.savefig(filename, dpi=dpi)
        plt.close()
