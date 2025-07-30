#coding:UTF-8

"""
# Name    : _gen_mesh_Q8.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Two-dimensional Q8 mesh generation program
"""

import numpy as np
from ._gen_mesh_Q4 import gen_mesh_Q4
from ._conv_highordermesh import conv_highordermesh

#-----------------------------------------------------------------------------#
def gen_mesh_Q8(mesh_info):
    """
    Generate 2nd order quadrilateral mesh.
    """
    nodes, elems = gen_mesh_Q4(mesh_info)
    nodes, elems = conv_highordermesh(nodes, elems)
    return nodes, elems

#-----------------------------------------------------------------------------#

