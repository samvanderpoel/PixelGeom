import copy
import cv2
import math
import os
import numpy as np

from grid import *
from shape import *

imgs = []
s = 0.25

first_shape = icosahedron(name = 'ico', center = (s*749, s*749, s*100), rad = s*150, shade = 0)
shape_list = [first_shape]

a, b, c = np.random.rand(3)
num_shapes = 5

for i in np.linspace(0.1, 10, num=500):
    print('Working on i = ' + str(i))

    new_shape = copy.deepcopy(shape_list[0])
    new_shape.rotate3d(axis = [0, 0, 1], angle = math.pi/50, center = (s*499 + 30*math.cos(i), s*499 + 30*math.sin(i), s*100))
    if len(shape_list) >= 5:
        shape_list.pop()
        shape_list.insert(0, new_shape)
    else:
        shape_list.insert(0, new_shape)
    for idx, shp in enumerate(shape_list):
        shp.name = 'ico' + str(idx + 1)
        shp.shade = idx/(idx + 1)

    mygrid = grid(shapes = shape_list, dim = (round(s*1000), round(s*1000)))
    mygrid.paint_canvas('radial')
    mygrid.draw_shapes()
    mygrid.plot_grid('pic.png', dpi=200)
    imgs.append(cv2.imread('pic.png'))
    os.remove('pic.png')

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
video=cv2.VideoWriter('platotetra.mp4', fourcc, 20, (1000, 1000)) # img dims must match resolution determined by dpi above

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
