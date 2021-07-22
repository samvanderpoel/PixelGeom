import copy
import cv2
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np

from grid import *
from shape import *

imgs = []
s = 0.3

a1, b1, c1 = np.random.rand(3)
a2, b2, c2 = np.random.rand(3)

for i in np.linspace(0.1, 10, num=300):
    print('Working on i = ' + str(i))

    tico = dodecahedron(name = 'tico', center = (s*499, s*499, s*100),
                        rad = s*400, shade = 1)
    mygrid = grid(shapes = [tico], dim = (round(s*1000), round(s*1000)))
    mygrid.rotate_shape3d(name = 'tico', axis = [a1, b1, c1], angle = i*math.pi/5)
    mygrid.rotate_shape3d(name = 'tico', axis = [a2, b2, c2], angle = i*math.pi/5)
    mygrid.paint_canvas(paint = 'gradient')
    mygrid.draw_shapes()
    cmap = rgb_to_cmap(colors = [[255,0,0], [255,255,255], [0,0,255]], penlow = [0,255,127], penhigh = [255,165,0])
    mygrid.plot_grid('pic.png', cmap = cmap, dpi = 200)
    imgs.append(cv2.imread('pic.png'))
    os.remove('pic.png')

np.save('anim.npy', imgs)

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
video=cv2.VideoWriter('triambic_icosahedron.mp4', fourcc, 50, (1000, 1000)) # img dims must meet or exceed resolution determined by dpi above

n = len(imgs)
for idx, image in enumerate(imgs):
    if idx % 10 == 0: print('Working on image ' + str(idx))
    video.write(image)
for idx, image in enumerate(reversed(imgs)):
    if idx % 10 == 0: print('Working on image ' + str(n-1-idx))
    video.write(image)
for idx, image in enumerate(imgs):
    if idx % 10 == 0: print('Working on image ' + str(idx))
    video.write(image)
for idx, image in enumerate(reversed(imgs)):
    if idx % 10 == 0: print('Working on image ' + str(n-1-idx))
    video.write(image)

cv2.destroyAllWindows()
video.release()