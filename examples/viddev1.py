import cv2
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add parent dir to sys path
import numpy as np

from grid import *
from shape import *

imgs = []
s = 0.12

a1, b1, c1 = np.random.rand(3)
a2, b2, c2 = np.random.rand(3)

tetra = tetrahedron(name = 'tetra', center = (s*499, s*499, s*100), rad = s*(600*(math.sin(i))**2), shade = 0)
mygrid = grid(shapes = [tetra], dim = (round(s*1000), round(s*1000)))

frames = 500
low, high = 0.1, 10
interval = (high - low) / (frames - 1)
for idx, i in enumerate(np.linspace(0.1, 10, num = frames)):
    sys.stdout.write('\rCreating frame ' + str(idx+1) + ' of ' + str(frames))
    sys.stdout.flush()
    mygrid.rotate_shape3d(name = 'tetra', axis = [a1, 4*math.cos(i)*b1, 4*math.sin(i)*c1], angle = interval * math.pi/5)
    for idx, node in enumerate(list(tetra.nodes())):
        node_pos = np.array(tetra.nodes[node]["pos"])
        mygrid.add_shape(cube(name = 'ico' + str(idx), center = node_pos, rad = s*(300*(math.sin(i))**2), shade = 1))
        mygrid.rotate_shape3d(name = 'ico' + str(idx), axis = [a2, b2, 2*math.sin(i)*c2], angle = i*math.pi)
    mygrid.paint_canvas(paint = 0.5)
    mygrid.draw_shapes()
    cmap = rgb_to_cmap(colors = [[178,34,34], [72,209,204], [221,160,221]], penlow = [255,215,0], penhigh = [0,255,127])
    mygrid.plot_grid('pic.png', cmap = cmap, dpi = 200)
    imgs.append(cv2.imread('pic.png'))
    os.remove('pic.png')
print('\n')
np.save('anim.npy', imgs)

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
video=cv2.VideoWriter('platotetra.mp4', fourcc, 14, (1000, 1000)) # img dims must meet or exceed resolution determined by dpi above

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
