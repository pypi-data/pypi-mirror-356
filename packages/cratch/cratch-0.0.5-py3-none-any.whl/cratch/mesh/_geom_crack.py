#coding:UTF-8

"""
# Name    : _geom_crack.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Two-dimensional crack geometry generation program
"""

import numpy as np

#-----------------------------------------------------------------------------#
def geom_crack(crack_r, length_rect, ligament_r):
    """
    This function generate crack geometry.

    Parameters
    ----------
    crack_r : float
        crack radius. (0.0 < crack_r < 0.5)
    length_rect : float
        Rectangular length.
    ligament_r : float
        ligament ratio. (0.1 ~ 0.9)
    """

    geometry = dict()
    c_1 = 0.853553390593274
    c_2 = 0.603553390593274
    c_3 = 0.353553390593274

    rx = crack_r
    ry = crack_r
    lx = length_rect
    ly = length_rect
    lr = ligament_r

    geometry['length_rect'] = length_rect
    geometry['degrees_u'] = 2
    geometry['degrees_v'] = 1
    geometry['ctrlpts_u'] = 7
    geometry['ctrlpts_v'] = 2
    geometry['ctrlpts'] = [\
        [      1.0*rx,    0.0, 0.0], [                  lr*lx+rx,    0.0, 0.0],\
        [      c_1*rx, c_3*ry, 0.0], [                  lr*lx+rx, 0.5*ly, 0.0],\
        [      c_2*rx, c_2*ry, 0.0], [                  lr*lx+rx, 1.0*ly, 0.0],\
        [      c_3*rx, c_1*ry, 0.0], [    (lr-0.5)*0.5+0.5*lr+rx, 1.0*ly, 0.0],
        [         0.0, 1.0*ry, 0.0], [      (lr-(1-lr))*0.5 + rx, 1.0*ly, 0.0],
        [     -rx*0.5, 1.0*ry, 0.0], [0.5*((lr-1.0)+(lr-0.5))+rx, 1.0*ly, 0.0],
        [-(1.0-lr)+rx, 1.0*ry, 0.0], [              -(1.0-lr)+rx, 1.0*ly, 0.0],
        ]

    geometry['weights'] = [1.0, 1.0,\
                           c_1, 1.0,\
                           c_1, 1.0,\
                           c_1, 1.0,\
                           1.0, 1.0,\
                           1.0, 1.0,\
                           1.0, 1.0,\
                           ]
    coeff = 1.0/((geometry['ctrlpts_u'] - 1)/2.0)
    geometry['knotvec_u'] = [0.00, 0.00, 0.00,\
                             coeff, coeff,\
                             coeff*2, coeff*2,\
                             1.0, 1.0, 1.00]
    geometry['knotvec_v'] = [0.0,0.0,1.0,1.0]
    return geometry

#-----------------------------------------------------------------------------#
