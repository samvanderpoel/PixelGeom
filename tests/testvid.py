import cv2
import math
import numpy as np
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add parent dir to sys path

from grid import *
from shape import *

if not os.path.isdir('tests/test-output'):
    os.makedirs('tests/test-output')

# CREATE VID OF SHAPE ROTATION - DEBUG HERE:

s = 0.5   # param to tune granularity/resolution of frames
imgs = [] # where frames are stored

# Replace shape-generating function here:
testshp = triambic_icosahedron(name = 'test', center = (s*499, s*499, s*100), rad = s*400, shade = 1)
mygrid = grid(shapes = [testshp], dim = (round(s*1000), round(s*1000)))

frames = 100
low, high = 0.1, 10
interval = (high - low) / (frames - 1)
for idx, i in enumerate(np.linspace(0.1, 10, num = frames)):
    sys.stdout.write('\rCreating frame ' + str(idx+1) + ' of ' + str(frames))
    sys.stdout.flush()
    mygrid.rotate_shape3d(name = 'test', axis = [0, math.cos(i), math.sin(i)], angle = interval * math.pi/5)
    mygrid.rotate_shape3d(name = 'test', axis = [1, 0, 0], angle = interval * math.pi/5)
    mygrid.draw_shapes()
    cmap = rgb_to_cmap(colors = [[176,224,230]], penlow = None, penhigh = [160,0,0])
    mygrid.plot_grid('pic.png', cmap = cmap, dpi = 200)
    imgs.append(cv2.imread('pic.png'))
    os.remove('pic.png')
print('\n')
np.save('tests/test-output/test-vid-data.npy', imgs)

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
video=cv2.VideoWriter('tests/test-output/test-vid.mp4', fourcc, 15, (1000, 1000))
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
