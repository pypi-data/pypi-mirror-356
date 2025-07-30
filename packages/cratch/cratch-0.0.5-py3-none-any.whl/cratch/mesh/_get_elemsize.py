#coding:UTF-8

"""
# Name    : _get_elemsize.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Two-dimensional element size calculation program
"""

import numpy as np

#-----------------------------------------------------------------------------#
def get_elemsize(nodes, elems):
    """
    Get min and max element size.

    Parameters
    ----------
    nodes : ndarray, 2-D
        Node data.
    elems : ndarray, 2-D
        Element data.

    Returns
    -------
    min_leng : float
        Minimum element size.
    max_leng : float
        Maximum element size.
    minidx : list
        Minimum element size node pare.
    maxidx : list
        Maximum element size node pare.
    """
    for j, el in enumerate(elems):
        edge1 = np.arange(el.shape[0])-1
        edge2 = np.arange(el.shape[0])
        for i in range(edge1.shape[0]):
            nid1 = el[edge1[i]]
            nid2 = el[edge2[i]]
            length = (nodes[nid1,0] - nodes[nid2,0])**2\
                   + (nodes[nid1,1] - nodes[nid2,1])**2
            length = np.sqrt(length)
            if j == 0 and i == 0:
                min_leng = length
                min_idxs = [nid1, nid2]
                max_leng = length
                max_idxs = [nid1, nid2]
            else:
                if min_leng > length:
                    min_leng = length
                    print(min_leng)
                    min_idxs = [nid1, nid2]
                if max_leng < length:
                    max_leng = length
                    max_idxs = [nid1, nid2]
            #print(length)
    return min_leng, max_leng, min_idxs, max_idxs

#-----------------------------------------------------------------------------#
