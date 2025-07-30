#coding:UTF-8

"""
# Name    : _duplicate.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Two-dimensional mesh duplication program
"""

import numpy as np
import copy
from ._union import union

#-----------------------------------------------------------------------------#
def dup_hstack(nodes, elems, t=0.0):
    """
    Node and element arrays in sequence horizontally.

    Parameters
    ----------
    nodes : ndarray, 2-D
        Node data.
    elems : ndarray, 2-D
        Element data.
    t : float, optional
        Angle of rotation (0 to 360 degrees, default:0.0).

    Returns
    -------
    stacked_n : ndarray, 2-D
        Stacked node data.
    stacked_e : ndarray, 2-D
        Stacked element data.
    """
    nodes2 = copy.deepcopy(nodes)
    elems2 = copy.deepcopy(elems)
    t = np.radians(t)
    rmat = np.array([[np.cos(t), -np.sin(t)],[np.sin(t), np.cos(t)]] )
    nodes2 = np.dot(nodes2, rmat)
    nodes2[:,0] *= -1.0
    nodes2[:,0] += np.max(nodes[:,0])*2.0
    stacked_n, stacked_e = union(nodes, elems, nodes2, elems2)
    return stacked_n, stacked_e

#-----------------------------------------------------------------------------#
def dup_vstack(nodes, elems, t=0.0):
    """
    Node and element arrays in sequence vertically.

    Parameters
    ----------
    nodes : ndarray, 2-D
        Node data.
    elems : ndarray, 2-D
        Element data.
    t : float, optional
        Angle of rotation (0 to 360 degrees, default:0.0).

    Returns
    -------
    stacked_n : ndarray, 2-D
        Stacked node data.
    stacked_e : ndarray, 2-D
        Stacked element data.
    """
    nodes2 = copy.deepcopy(nodes)
    elems2 = copy.deepcopy(elems)
    t = np.radians(t)
    rmat = np.array([[np.cos(t), -np.sin(t)],[np.sin(t), np.cos(t)]] )
    nodes2 = np.dot(nodes2, rmat)
    nodes2[:,1] += np.max(nodes[:,1])*2
    nodes2[:,0] += np.max(nodes[:,0])
    stacked_n, stacked_e = union(nodes, elems, nodes2, elems2)
    return stacked_n, stacked_e

#-----------------------------------------------------------------------------#
