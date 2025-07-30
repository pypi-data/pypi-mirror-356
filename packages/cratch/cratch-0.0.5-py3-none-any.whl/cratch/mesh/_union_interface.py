#coding:UTF-8

"""
# Name    : _union_interface.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Two-dimensional mesh unite only interface program
"""

import numpy as np
import copy

#-----------------------------------------------------------------------------#
def union_interface(nodes1, elems1, nodes2, elems2):
    # nodes1, elems1: 結合もと
    # nodes2, elems2: 結合データ
    # Q4 mesh only
    overlap_idx = np.empty((0, 2), dtype=int)
    for i, node in enumerate(nodes2):
        r = nodes1 - node
        rr = np.sqrt(r[:,0]**2 + r[:, 1]**2)
        idx = np.where(rr < 1e-8)[0]
        if idx.shape[0] != 0:
            # node1のidxとnode2のidx
            overlap_idx = np.append(overlap_idx, np.array([[idx[0], i]]), 0)

    nodes = np.vstack((nodes1, nodes2))
    # get line element
    elems_id = np.where(np.sum(np.isin(elems2, overlap_idx[:,1]), axis=1) > 1)[0]
    elems_l = elems2[elems_id]
    lines = elems_l[np.isin(elems_l, overlap_idx[:, 1])].reshape(elems_id.shape[0], -1)
    #print(lines)

    num_lines = lines.shape[0]
    num_nodes1 = nodes1.shape[0]
    faces = np.zeros((num_lines, 4), dtype=int)

    for i in range(num_lines):
        n1 = np.where(overlap_idx[:,1] == lines[i, 0])[0][0]
        n1 = overlap_idx[n1, 0]
        n2 = np.where(overlap_idx[:,1] == lines[i, 1])[0][0]
        n2 = overlap_idx[n2, 0]
        n3 = lines[i, 0] + num_nodes1
        n4 = lines[i, 1] + num_nodes1
        faces[i] = np.array([n1, n2, n3, n4])

    elems = np.vstack((elems1, elems2+num_nodes1))

    return nodes, elems, faces

#-----------------------------------------------------------------------------#
