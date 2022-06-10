import cv2
import math
import numpy as np
import os, sys

# add src to sys path
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "src"
    )
)

from Animation import Animation
from Grid import Grid
from grid_utils import *
from Shape import Shape
from shape_lib import *
from shape_utils import *


a1, b1, c1 = np.random.rand(3)
a2, b2, c2 = np.random.rand(3)

def frame_func(idx, t, frames):
    s = (math.sin(t))**2 * 0.4 + 0.005
    tico = icosahedron(
        name = "tico",
        center = (s*499, s*499, s*100),
        rad = s*400,
        shade = 1
    )
    mygrid = Grid(shapes=[tico], dim=(500, 500))
    mygrid.rotate_shape_3d(
        name = "tico",
        axis = [a1, math.cos(t)*b1, math.sin(t)*c1],
        angle = t*math.pi/5
    )
    mygrid.rotate_shape_3d(
        name = "tico", axis = [a2, b2, c2], angle = t*math.pi/5
    )
    mygrid.paint_canvas(paint="gradient")
    mygrid.draw_shapes()
    cmap = rgb_to_cmap(
        colors = [[255,0,0], [255,255,255], [0,0,255]],
        penlow = [0,255,127],
        penhigh = [255,165,0]
    )
    mygrid.plot_grid("pic.png", cmap=cmap, dpi=200)
    frames.append(cv2.imread("pic.png"))
    os.remove("pic.png")

animation = Animation(
    time=np.linspace(0.1, 10, num=600),
    frame_func=frame_func,
    fps=30,
    n_cycles=2,
    frame_size=(1000, 1000),
    animation_fname="anim0.mp4"
)
animation.process_frames()
animation.write_video()
