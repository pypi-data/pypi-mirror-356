"""Tetrahedral High-Order Finite-Element Data Creation

In this example, two tetrahedrons with grid order 2 (Tet-10's) are created by
defining the nodes the associated element to node mapping (nodemap). The nodes
in each element of the nodemap follow a specific order that starts with the
corners followed by the edge nodes then face nodes then nodes interior to the
volume of the cell.

http://cgns.github.io/CGNS_docs_current/sids/conv.html#unst_3d
"""
import itertools as it

import tecplot as tp
from tecplot.constant import *

import numpy as np

# Run this script with "-c" to connect to Tecplot 360 on port 7600
# To enable connections in Tecplot 360, click on:
#   "Scripting..." -> "PyTecplot Connections..." -> "Accept connections"
import sys
if '-c' in sys.argv:
    tp.session.connect()

# Locations (x,y,z) of the nodes
nodes = ((0, 0, 0),
         (2, 0, 0),
         (0, 2, 0),
         (0, 0, 2),
         (1, 0, 0),
         (1, 1, 0),
         (0, 1, 0),
         (0, 0, 1),
         (1, 0, 1),
         (0, 1, 1),
         (0, 0,-2),
         (0, 0,-1),
         (1, 0,-1),
         (0, 1,-1),)

nodemap = ((0, 1, 2,  3, 4, 5, 6,  7,  8,  9),
           (0, 1, 2, 10, 4, 5, 6, 11, 12, 13))

# Scalar value at the nodes
scalar_data = (0, 4, 4, 4, 0, 1, 0, 0, 1, 1, 0, 0, -1, -1)

sections = (
    (2, FECellShape.Tetrahedron, 2),  # 2 elements of Tet-10s (grid order: 2)
)

# Setup dataset and zone
# Make sure to set the connectivity before any plot or style change.
ds = tp.active_frame().create_dataset('Data', ['x','y','z','s'])

z = ds.add_fe_mixed_zone(name='FE Tetrahedron-10 Float (20, 2)',
                         num_points=len(nodes),
                         sections=sections)

# Fill in node locations
z.values('x')[:] = [n[0] for n in nodes]
z.values('y')[:] = [n[1] for n in nodes]
z.values('z')[:] = [n[2] for n in nodes]

# Set the scalar data
z.values('s')[:] = scalar_data

z.nodemap.section(0)[:] = nodemap

### Now we setup a nice view of the data
plot = tp.active_frame().plot(PlotType.Cartesian3D)
plot.activate()

plot.contour(0).colormap_name = 'Sequential - Yellow/Green/Blue'
plot.contour(0).variable = ds.variable('s')
plot.contour(0).levels.reset_levels([0, 1, 2, 3, 4])

for ax in plot.axes:
    ax.show = True

iso = plot.isosurface(0)
iso.isosurface_selection = IsoSurfaceSelection.AllContourLevels
iso.show = True

plot.show_isosurfaces = True

tp.export.save_png('fe_tetrahedrons_highorder1.png', 600, supersample=3)
