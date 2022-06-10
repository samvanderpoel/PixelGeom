import cv2
import math
import numpy as np
import os, sys

# add src to sys path
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"
    )
)

from Animation import Animation
from Grid import Grid
from grid_utils import *
from Shape import Shape
from shape_lib import *
from shape_utils import *


if __name__ == "__main__":
    a1, b1, c1 = np.random.rand(3)
    a2, b2, c2 = np.random.rand(3)
    scale = 5
    time = np.linspace(0.1, 10, num=200)

    def frame_func(idx, t, frames):
        s = (math.sin(t))**2 * 0.95 + 0.005
        dodec = dodecahedron(
            name="dodec",
            center=(scale*49, scale*49, 10),
            rad=scale*48,
            shade = 1
        )
        mygrid = Grid(shapes=[dodec], dim=(scale*100, scale*100))
        mygrid.rotate_shape_3d(
            name="dodec", axis=[a2, b2, c2], angle=t*math.pi/max(time/2)
        )
        mygrid.draw_shapes()
        cmap = rgb_to_cmap(colors=[[0, 48, 87]], penhigh=[179, 163, 105])
        mygrid.plot_grid("pic.png", cmap=cmap, dpi=200)
        frames.append(cv2.imread("pic.png"))
        os.remove("pic.png")

    animation = Animation(
        time=time,
        frame_func=frame_func,
        fps=10,
        n_cycles=2,
        frame_size=(1000, 1000),
        animation_fname="anim1.mp4"
    )
    animation.process_frames()
    animation.write_video()
