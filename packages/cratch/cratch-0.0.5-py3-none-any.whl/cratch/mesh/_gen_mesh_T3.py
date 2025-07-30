#coding:UTF-8

"""
# Name    : _gen_mesh_T3.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Two-dimensional T3 mesh generation program
"""

import numpy as np
import copy

#-----------------------------------------------------------------------------#
def gen_mesh_T3(mesh_info):
    """
    Generate 1st order triangular mesh.
    """
    lx = mesh_info['lx']; ly = mesh_info['ly']
    ex = mesh_info['ex']; ey = mesh_info['ey']
    nx = ex + 1; ny = ey + 1
    dx = lx / ex; dy = ly / ey
    nodes = np.zeros((nx*ny, 2), dtype=float)
    elems = np.zeros((ex*ey*2, 3), dtype=int)
    for j in range(ey):
        for i in range(ex):
            k = i + ex*j
            n0 = (ex + 1)*j + i
            n1 = n0 + 1
            n2 = (ex + 1)*(j + 1) + i
            n3 = n2 + 1
            nodes[n0, :] = np.array([dx*(i  ), dy*(j  )])
            nodes[n1, :] = np.array([dx*(i+1), dy*(j  )])
            nodes[n2, :] = np.array([dx*(i  ), dy*(j+1)])
            nodes[n3, :] = np.array([dx*(i+1), dy*(j+1)])
            elems[k*2, :] = np.array([n0, n1, n3])
            elems[k*2+1, :] = np.array([n0, n3, n2])
    return nodes, elems
    '''
    # matplotlib版簡易メッシュ生成T3
    x = np.linspace(0, mesh_info['lx'], mesh_info['ex'] + 1)
    y = np.linspace(0, mesh_info['ly'], mesh_info['ey'] + 1)
    xx, yy = np.meshgrid(x, y)
    xx = xx.reshape(-1)
    yy = yy.reshape(-1)
    nodes = np.vstack((xx, yy)).T
    import matplotlib.tri as tri
    elems = tri.Triangulation(nodes[:, 0], nodes[:, 1]).triangles
    return nodes, elems
    '''
#-----------------------------------------------------------------------------#
