import cv2
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add parent dir to sys path
import numpy as np

from grid import *
from shape import *

imgs = []
s = 0.3

a1, b1, c1 = np.random.rand(3)
a2, b2, c2 = np.random.rand(3)

frames = 700
low, high = 0.1, 10
for idx, i in enumerate(np.linspace(0.1, 10, num = frames)):
    sys.stdout.write('\rCreating frame ' + str(idx+1) + ' of ' + str(frames))
    sys.stdout.flush()
    tico = dodecahedron(name = 'tico', center = (s*499, s*499, s*100),
                        rad = (math.sin(i))**2*s*1500, shade = 1)
    mygrid = grid(shapes = [tico], dim = (round(s*1000), round(s*1000)))
    mygrid.rotate_shape3d(name = 'tico', axis = [a1, b1, c1], angle = i*math.pi/5)
    mygrid.rotate_shape3d(name = 'tico', axis = [a2, b2, c2], angle = i*math.pi/5)
    mygrid.paint_canvas(paint = 'gradient')
    mygrid.draw_shapes()
    cmap = rgb_to_cmap(colors = [[205,92,92], [0,128,128], [221,160,221]], penlow = [0,255,127], penhigh = [205,133,63])
    mygrid.plot_grid('pic.png', cmap = cmap, dpi = 200)
    imgs.append(cv2.imread('pic.png'))
    os.remove('pic.png')
print('\n')
np.save('anim.npy', imgs)

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
video=cv2.VideoWriter('dodecahedron.mp4', fourcc, 50, (1000, 1000)) # img dims must meet or exceed resolution determined by dpi above

n = len(imgs)
m = len(str(n))
for idx, image in enumerate(imgs):
    if idx % 10 == 0:
        sys.stdout.write('\rAdding frame: ' + str(idx+1) + (m-len(str(idx+1)))*' ' + ' to video ')
        sys.stdout.flush()
    video.write(image)
for idx, image in enumerate(reversed(imgs)):
    if idx % 10 == 0:
        sys.stdout.write('\rAdding frame ' + str(n-1-idx) + (m-len(str(n-1-idx)))*' ' + ' to video ')
        sys.stdout.flush()
    video.write(image)
for idx, image in enumerate(imgs):
    if idx % 10 == 0:
        sys.stdout.write('\rAdding frame ' + str(idx) + (m-len(str(idx+1)))*' ' + ' to video ')
        sys.stdout.flush()
    video.write(image)
for idx, image in enumerate(reversed(imgs)):
    if idx % 10 == 0:
        sys.stdout.write('\rAdding frame ' + str(n-1-idx) + (m-len(str(n-1-idx)))*' ' + ' to video ')
        sys.stdout.flush()
    video.write(image)
print('\n')

cv2.destroyAllWindows()
video.release()
