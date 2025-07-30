#coding:UTF-8

"""
# Name    : _conv_highordermesh.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Two-dimensional mesh generation program
"""

import numpy as np

#-----------------------------------------------------------------------------#
def conv_highordermesh(nodes, elems):
    """
    Convert high order mesh. T3->T6, Q4->Q8.

    Parameters
    ----------
    nodes : ndarray, 2-D
        Node data.
    elems : ndarray, 2-D
        Element data.

    Returns
    -------
    nodes : ndarray, 2-D
        Converted node data.
    elems : ndarray, 2-D
        Converted element data.
    """
    new_nodes = np.zeros((1,2), dtype=float)
    new_elems = np.zeros((elems.shape[0], elems.shape[1]*2), dtype=int)
    new_elems[:,:elems.shape[1]] = elems[:]
    connectivity = np.arange(elems.shape[1] + 1)
    connectivity[-1] = connectivity[0]
    num_newnode = 0
    pairid = 0
    startidx_elem = elems.shape[1]
    startidx_node = np.max(elems) + 1
    for i in range(elems.shape[0]):
        for j in range(elems.shape[1]):
            line = j
            coordinate_x = (nodes[elems[i, connectivity[j  ]], 0]
                          + nodes[elems[i, connectivity[j+1]], 0])*0.5
            coordinate_y = (nodes[elems[i, connectivity[j  ]], 1]
                          + nodes[elems[i, connectivity[j+1]], 1])*0.5
            new_node = np.array([coordinate_x, coordinate_y])

            if num_newnode == 0:
                new_nodes[0,:] = new_node
                new_elems[i, startidx_elem + j] = startidx_node\
                                                + num_newnode
                num_newnode += 1
            else:
                add_flag = 0
                for k in range(num_newnode):
                    if new_nodes[k, 0] == new_node[0] and \
                       new_nodes[k, 1] == new_node[1]:
                        add_flag = 1
                        pairid = k
                if add_flag == 0:
                    new_nodes = np.vstack((new_nodes, new_node))
                    new_elems[i, startidx_elem + j] = startidx_node\
                                                    + num_newnode
                    num_newnode += 1
                else:
                    new_elems[i, startidx_elem + j] = startidx_node\
                                                    + pairid

    #>> add new nodes
    new_nodes = np.vstack((nodes, new_nodes))
    return new_nodes, new_elems

#-----------------------------------------------------------------------------#
