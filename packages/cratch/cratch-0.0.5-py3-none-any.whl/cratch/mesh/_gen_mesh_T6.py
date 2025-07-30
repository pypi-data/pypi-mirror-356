#coding:UTF-8

"""
# Name    : _gen_mesh_T6.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Two-dimensional T6 mesh generation program
"""

import numpy as np

#-----------------------------------------------------------------------------#
def gen_mesh_T6(mesh_info):
    """
    Generate 2nd order triangular mesh.
    """
    lx = mesh_info['lx']; ly = mesh_info['ly']
    ex = mesh_info['ex']; ey = mesh_info['ey']
    nx = ex + 1; ny = ey + 1
    dx = lx / ex; dy = ly / ey
    nodes = np.zeros(((ex*2 + 1)*(ey*2 + 1), 2), dtype=float)
    elems = np.zeros((ex*ey*2, 6), dtype=int)
    k = 0
    for j in range(ey):
        for i in range(ex):
            n1 = (2*i) + (2*ex + 1)*(2*j)
            n4 = (2*i) + (2*ex + 1)*(2*j + 1)
            n7 = (2*i) + (2*ex + 1)*(2*j + 2)
            n2 = n1 + 1; n3 = n1 + 2
            n5 = n4 + 1; n6 = n4 + 2
            n8 = n7 + 1; n9 = n7 + 2
            c1 = i; c2 = (2*i + 1) / 2; c3 = i + 1
            c4 = j; c5 = (2*j + 1) / 2; c6 = j + 1
            nodes[n1, :] = np.array([dx*c1, dy*c4])
            nodes[n2, :] = np.array([dx*c2, dy*c4])
            nodes[n3, :] = np.array([dx*c3, dy*c4])
            nodes[n4, :] = np.array([dx*c1, dy*c5])
            nodes[n5, :] = np.array([dx*c2, dy*c5])
            nodes[n6, :] = np.array([dx*c3, dy*c5])
            nodes[n7, :] = np.array([dx*c1, dy*c6])
            nodes[n8, :] = np.array([dx*c2, dy*c6])
            nodes[n9, :] = np.array([dx*c3, dy*c6])
            elems[2*k, :] = np.array([n1, n3, n9, n2, n6, n5])
            elems[2*k+1, :] = np.array([n1, n9, n7, n5, n8, n4])
            k += 1
    return nodes, elems

#-----------------------------------------------------------------------------#
