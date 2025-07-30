#coding:UTF-8

"""
# Name    : _geom_ch.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Two-dimensional circular hole geometry generation program
"""

import numpy as np

#-----------------------------------------------------------------------------#
def geom_ch(radius_hole, length_rect):
    """
    This function generate circular hole geometry.

    Parameters
    ----------
    radius_hole : float
        Radius hole size.
    length_rect : float
        Rectangular length.

    Returns
    -------
    geometry : dict
        Geometry data.
    """
    #>> Geometry settings
    geometry = dict()
    c_1 = 0.853553390593274
    c_2 = 0.603553390593274
    c_3 = 0.353553390593274

    rx = radius_hole
    ry = radius_hole
    #ry = 0.01
    lx = length_rect
    ly = length_rect

    geometry['length_rect'] = length_rect
    geometry['degrees_u'] = 2
    geometry['degrees_v'] = 1
    geometry['ctrlpts_u'] = 5
    geometry['ctrlpts_v'] = 2
    geometry['ctrlpts'] = [\
        [1.0*rx,    0.0, 0.0],\
        [1.0*lx,    0.0, 0.0],\
        [c_1*rx, c_3*ry, 0.0],\
        [1.0*lx, 0.5*ly, 0.0],\
        [c_2*rx, c_2*ry, 0.0],\
        [1.0*lx, 1.0*ly, 0.0],\
        [c_3*rx, c_1*ry, 0.0],\
        [0.5*lx, 1.0*ly, 0.0],\
        [   0.0, 1.0*ry, 0.0],\
        [   0.0, 1.0*ly, 0.0] ]

    geometry['weights'] = [1.0, 1.0,\
                           c_1, 1.0,\
                           c_1, 1.0,\
                           c_1, 1.0,\
                           1.0, 1.0 ]
    geometry['knotvec_u'] = [0.0,0.0,0.0,0.5,0.5,1.0,1.0,1.0]
    geometry['knotvec_v'] = [0.0,0.0,1.0,1.0]
    return geometry

#-----------------------------------------------------------------------------#
