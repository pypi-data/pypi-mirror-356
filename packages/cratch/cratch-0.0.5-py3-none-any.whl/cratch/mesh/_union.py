#coding:UTF-8

"""
# Name    : _union.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Two-dimensional mesh unite program
"""

import numpy as np

#-----------------------------------------------------------------------------#
def union(nodes1, elems1, nodes2, elems2):
    """
    This function unite two meshes.

    Parameters
    ----------
    nodes1 : ndarray, 2-D
        node data 1
    elems1 : ndarray, 2-D
        element data 1
    nodes2 : ndarray, 2-D
        node data 2
    elems2 : ndarray, 2-D
        element data 2

    Returns
    -------
    nodes : ndarray, 2-D
        United node data
    elems : ndarray, 2-D
        United element data
    """
    #>> Get overlap node index
    overlap_idx = [] #[idx 1, idx 2]
    for i, node in enumerate(nodes2):
        rr = nodes1 - node
        r = np.sqrt(rr[:,0]**2 + rr[:,1]**2)
        idx = np.where(r < 1e-8)[0]
        #print(idx)
        if idx.shape[0] != 0:
            overlap_idx.append([idx[0],i])
    overlap_idx = np.array(overlap_idx)

    #>> Union node data
    nodes22 = np.delete(nodes2, overlap_idx[:,1], axis=0)
    nodes = np.vstack((nodes1, nodes22))

    #>> Get switch node index (only overlap nodes)
    elems2_flat = elems2.ravel()
    switch_list = []
    for i in range(overlap_idx.shape[0]):
        idx = np.where(elems2_flat == overlap_idx[i,1])[0]
        switch_list.append(idx)

    #>> Get look up table (exclude overlap nodes)
    idx1 = []; idx2 = []
    for i, node in enumerate(nodes22):
        rr = nodes - node
        r  = np.sqrt(rr[:, 0]**2 + rr[:,1]**2)
        idx = np.where(r < 1e-8)[0]
        if idx.shape[0] != 0:
            idx1.append(idx[0])
            idxx = np.where((nodes2[:,0] == nodes[idx[0],0])\
                           &(nodes2[:,1] == nodes[idx[0],1]))[0][0]
            idx2.append(idxx)

    #>> Update element data (exclude overlap node)
    for i in range(len(idx2)-1, -1, -1):
        idx = np.where(elems2_flat == idx2[i])[0]
        elems2_flat[idx] = idx1[i]

    #>> Update element data (only overlap node)
    for i in range(len(switch_list)):
        elems2_flat[switch_list[i]] = overlap_idx[i,0]

    #>> Union element data
    elems3 = elems2_flat.reshape(elems2.shape)
    elems = np.vstack((elems1, elems3))
    return nodes, elems

#-----------------------------------------------------------------------------#
#def mesh_union_old(nodes1, elems1, nodes2, elems2):
    '''
    # nodes1, elems1: 結合もと
    # nodes2, elems2: 結合データ
    #>> 節点の重複チェック
    overlap_idx = []
    for i, node in enumerate(nodes2):
        rr = nodes1 - node
        r = np.sqrt(rr[:,0]**2 + rr[:,1]**2)
        idx = np.where(r < 1e-8)[0]
        if idx.shape[0] != 0:
            overlap_idx.append(i)
    nodes22 = np.delete(nodes2, overlap_idx, axis=0) #重複の取り除かれたnode2
    nodes = np.vstack((nodes1, nodes22))

    #>> 修正する節点番号のindexを取得
    index1 = []; index2 = []
    for i, node in enumerate(nodes2):
        rr = nodes - node
        r = np.sqrt(rr[:, 0]**2 + rr[:, 1]**2)
        idx = np.where(r < 1e-8)[0]
        if idx.shape[0] != 0:
            index1.append(idx[0])
            index2.append(i)

    #>> elems2の節点番号の修正
    elems2_flat = elems2.flatten()
    for i in range(len(index2)-1, -1, -1):
        idx = np.where(elems2_flat == index2[i])[0]
        elems2_flat[idx] = index1[i]
    elems3 = elems2_flat.reshape(elems2.shape)
    elems = np.vstack((elems1, elems3))

    return nodes, elems
    '''

#-----------------------------------------------------------------------------#
