#coding:UTF-8

"""
# Name    : _gen_mesh.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Two-dimensional mesh generation program
"""

import numpy as np
from ._gen_mesh_T3 import gen_mesh_T3
from ._gen_mesh_T6 import gen_mesh_T6
from ._gen_mesh_Q4 import gen_mesh_Q4
from ._gen_mesh_Q8 import gen_mesh_Q8

#-----------------------------------------------------------------------------#
def gen_mesh(mesh_info):
    """
    This function generate mesh and return node data (nodes)
    and element data(elems).
    This function can be generate 'T3', 'T6', 'Q4' and 'Q8'
    mesh

    Parameters
    ----------
    mesh_info : dict
        mesh_info include bellow parameters

        elem_type (str, element type 'T3', 'T6', 'Q4', 'Q8')

        lx (float, length of the model in the x direction)

        ly (float, length of the model in the y direction)

        ex (int, number of element in the x direction)

        ey (int, number of element in the y direction)

    Returns
    -------
    nodes : ndarray, 2-D
        node data
    elems : ndarray, 2-D
        element data
    """

    if mesh_info['elem_type'] == 'T3':
        return gen_mesh_T3(mesh_info)

    elif mesh_info['elem_type'] == 'T6':
        return gen_mesh_T6(mesh_info)

    elif mesh_info['elem_type'] == 'Q4':
        return gen_mesh_Q4(mesh_info)

    elif mesh_info['elem_type'] == 'Q8':
        return gen_mesh_Q8(mesh_info)

    else:
        print('Element type error.')
        print('Element type is "T3, T6, Q4, Q8"')
        exit()

#-----------------------------------------------------------------------------#
