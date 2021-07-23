import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add parent dir to sys path

from grid import *
from shape import *

if not os.path.isdir('tests/test-output'):
    os.makedirs('tests/test-output')

# PLOT A SHAPE - DEBUG HERE:

s = 1
# Replace shape-generating function here:
testshp = dodecahedron(name = 'test', center = (s*499, s*499, s*100), rad = s*300, rand = True)

# Add shape to grid:
mygrid = grid(shapes = [testshp], dim = (round(s*1000), round(s*1000)))
mygrid.draw_shapes(['test'])

# Create colormap:
cmap = rgb_to_cmap(colors = [[176,224,230]], penlow = None, penhigh = [160,0,0])

# Plot canvas and shape
mygrid.plot_grid('tests/test-output/testimg.png', cmap = cmap)
