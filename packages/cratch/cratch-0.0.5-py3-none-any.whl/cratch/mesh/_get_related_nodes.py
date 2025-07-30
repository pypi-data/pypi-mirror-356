#coding:UTF-8

"""
# Name    : _get_related_nodes.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Jan. 08 2025
# Date    : Mar. 20 2023
# Note    : Get related nodes from mesh program
"""

import numpy as np

#-----------------------------------------------------------------------------#
def get_related_nodes(nodes, elems):
    """
    This function returns a related nodes list.

    Parameters
    ----------
    nodes : ndarray, 2-D
        Node data.
    elems : ndarray, 2-D
        Element data.

    Return
    ------
    related_nodes : list, 2-D
        Related nodes list.
    """
    num_nodes = nodes.shape[0]
    num_elems = elems.shape[0]
    #>> 先頭を自身の節点番号とするリストの生成
    related_nodes = [[x] for x in range(num_nodes)]

    for i in range(num_elems):
        elemnodes = elems[i]
        for inode in elemnodes:
            for jnode in elemnodes:
                if (inode < jnode) and (jnode not in related_nodes[inode]):
                    related_nodes[inode].append(jnode)
    for i in range(num_nodes):
        related_nodes[i].sort()
    return related_nodes

#-----------------------------------------------------------------------------#
