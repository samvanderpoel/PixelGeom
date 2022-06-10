import cv2
import math
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add parent dir to sys path
import numpy as np

from grid import *
from shape import *

imgs = []

frames = 600
low, high = 0.1, 10
interval = (high - low) / (frames - 1)
for idx, i in enumerate(np.linspace(0.1, 10, num = frames)):
    sys.stdout.write('\rCreating frame ' + str(idx+1) + ' of ' + str(frames))
    sys.stdout.flush()
    mygrid = grid(shapes = [], dim = (25, 25))
    mygrid.paint_canvas(paint = 'gradient')
    j = high - i
    cmap = rgb_to_cmap(
        colors = [
            [(255/interval)*i, (255/interval)*j**2, (255/interval)*i**3],
            [(255/interval)*j, (255/interval)*i**(1/2), (255/interval)*j**(1/3)]
        ],
        penlow = None,
        penhigh = None
    )
    mygrid.plot_grid('pic.png', cmap = cmap, dpi = 200)
    imgs.append(cv2.imread('pic.png'))
    os.remove('pic.png')
print('\n')
np.save('anim.npy', imgs)

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
video=cv2.VideoWriter('changing-cmap.mp4', fourcc, 30, (1000, 1000)) # img dims must meet or exceed resolution determined by dpi above

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
