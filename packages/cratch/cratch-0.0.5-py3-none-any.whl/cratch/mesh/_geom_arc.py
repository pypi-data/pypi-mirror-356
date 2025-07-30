#coding:UTF-8

"""
# Name    : _geom_arc.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Two-dimensional arc geometry generation program
"""

import numpy as np

#-----------------------------------------------------------------------------#
def geom_arc(radius_hole, length_rect):
    #>> Geometry settings
    geometry = dict()
    c_1 = 0.853553390593274
    c_2 = 0.603553390593274
    c_3 = 0.353553390593274

    rx = radius_hole
    ry = radius_hole
    lx = length_rect
    ly = length_rect

    geometry['length_rect'] = length_rect
    geometry['degrees_u'] = 2
    geometry['degrees_v'] = 1
    geometry['ctrlpts_u'] = 5
    geometry['ctrlpts_v'] = 2
    geometry['ctrlpts'] = [\
        [1.0*rx,    0.0, 0.0], [1.0*lx,    0.0, 0.0],
        [c_1*rx, c_3*ry, 0.0], [c_1*lx, c_3*ly, 0.0],
        [c_2*rx, c_2*ry, 0.0], [c_2*lx, c_2*ly, 0.0],
        [c_3*rx, c_1*ry, 0.0], [c_3*lx, c_1*ly, 0.0],
        [   0.0, 1.0*ry, 0.0], [   0.0, 1.0*ly, 0.0],
        ]

    geometry['weights'] = [1.0, 1.0,\
                           c_1, c_1,\
                           c_1, c_1,\
                           c_1, c_1,\
                           1.0, 1.0 ]
    geometry['knotvec_u'] = [0.0,0.0,0.0,0.5,0.5,1.0,1.0,1.0]
    geometry['knotvec_v'] = [0.0,0.0,1.0,1.0]

    return geometry

#-----------------------------------------------------------------------------#
