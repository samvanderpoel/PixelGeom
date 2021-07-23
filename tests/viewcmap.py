import functools
import matplotlib.pyplot as plt
import numpy as np
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add parent dir to sys path

from grid import rgb_to_cmap

if not os.path.isdir('tests/test-output'):
    os.makedirs('tests/test-output')

# Specify cmap here:
mycmap = rgb_to_cmap([[255,127,80], [189,183,107], [123,104,238], [0,128,128]])

def gradient(x, dim):
    idx, val = x
    temp_val = 1-idx[0]/(dim[0]-1)-idx[1]/(dim[1]-1)
    return [idx, (temp_val+1)/2]

dim = (8, 8)
canvas = np.zeros(dim)
enum = map(functools.partial(gradient, dim=dim), np.ndenumerate(canvas))
for idx, val in enum:
    canvas[idx] = val

dpi = 300
fig, ax = plt.subplots(1, figsize=(3, 3), dpi = dpi)
ax.imshow(canvas, cmap = mycmap, interpolation = 'None', vmin = 0, vmax = 1)
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)
ax.axis('off')
fig.subplots_adjust(right=1.00, left=0.00, bottom=0.00, top=1.00)
fig.savefig('tests/test-output/test-cmap.png', dpi = dpi)
plt.close()
