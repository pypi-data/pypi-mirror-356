#coding:UTF-8

"""
# Name    : _get_boundnodes.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Two-dimensional bound nodes pickup program
"""

import numpy as np

#-----------------------------------------------------------------------------#
def get_boundnodes(elems, mesh_info):
    """
    Get boundary nodes.

    Parameters
    ----------
    elems : ndarray, 2-D
        Element data.
    mesh_info : dict
        mesh_info include bellow parameters

    Returns
    -------
    bound_nodes : ndarray, 2-D
        boundary nodes data
    """

    #>> Make array for node count
    node_all0 = elems.ravel()
    node_idx0 = np.unique(node_all0)
    node_cnt0 = np.zeros((node_idx0.shape[0], 2), dtype=int)
    node_cnt0[:,0] = node_idx0

    #>> For T3, Q4 element
    for i, idx in enumerate(node_idx0):
        node_cnt0[i,1] = np.where(node_all0==idx)[0].shape[0]
    connect_max = np.max(node_cnt0[:,1])
    bound_nodes = np.where(node_cnt0[:,1]!=connect_max)[0]

    #>> For T6, Q8 element
    if mesh_info['elem_type'] == 'T6' or\
        mesh_info['elem_type'] == 'Q8':
        if mesh_info['elem_type'] == 'T6':
            node_all1 = elems[:,:3]
        if mesh_info['elem_type'] == 'Q8':
            node_all1 = elems[:,:4]

        node_all1 = node_all1.ravel()
        node_idx1 = np.unique(node_all1)
        node_cnt1 = np.zeros((node_idx1.shape[0], 2), dtype=int)
        node_cnt1[:,0] = node_idx1
        for i, idx in enumerate(node_idx1):
            node_cnt1[i,1] = np.where(node_all1==idx)[0].shape[0]
        connect_max = np.max(node_cnt1[:,1])
        bound_node1 = node_cnt1[np.where(node_cnt1[:,1]!=connect_max)[0],0]
        # Use T3 or Q4 boundary node data
        bound_nodes = np.where(node_cnt0[:,1]==1)[0]
        bound_nodes = np.unique(np.hstack((bound_node1, bound_nodes)))
    #print(bound_nodes)
    return bound_nodes

#-----------------------------------------------------------------------------#
