#coding:UTF-8

"""
# Name    : _gen_mesh_Q4.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Two-dimensional Q4 mesh generation program
"""

import numpy as np

#-----------------------------------------------------------------------------#
def gen_mesh_Q4(mesh_info):
    """
    Generate 1st order quadrilateral mesh.
    """
    lx = mesh_info['lx']; ly = mesh_info['ly']
    ex = mesh_info['ex']; ey = mesh_info['ey']
    nx = ex + 1; ny = ey + 1
    dx = lx / ex; dy = ly / ey
    nodes = np.zeros((nx*ny, 2), dtype=float)
    elems = np.zeros((ex*ey, 4), dtype=int)
    k = 0
    for j, y in enumerate(np.linspace(0.0, ly, ny)):
        for i, x in enumerate(np.linspace(0.0, lx, nx)):
            n = i + nx*j
            nodes[n, 0] = x; nodes[n, 1] = y
            if i < ex and j < ey:
                elems[k, 0] = n
                elems[k, 1] = n + 1
                elems[k, 2] = n + nx + 1
                elems[k, 3] = n + nx
                k += 1
    return nodes, elems

#-----------------------------------------------------------------------------#
