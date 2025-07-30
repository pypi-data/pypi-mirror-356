#coding:UTF-8

"""
# Name    : _bctools.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 04 2024
# Date    : Mar. 20 2023
# Note    : finite element method tool program
"""

import numpy as np
from ._shapefunctions import shape_function
from ._quadtools import quadrature

#-----------------------------------------------------------------------------#
def get_fixarray(fem, idx, fix_type):
    """
    This function returns fix array.

    Parameters
    ----------
    fem : class
        FEM class.
    idx : ndarray, 1-D
        Fix node ID.
    fix_type : str
        Fix type (fix direction). In 2-d ('x', 'y', 'xy').
        In 3-d ('x', 'y', 'z', 'yz(zy)', 'zx(xz)', 'xy(yx)', 'xyz'.)

    Returns
    -------
    fix : ndarray, 2-D
        Fix array.
    """

    fix = np.zeros((idx.shape[0], fem.dof_nodes), dtype=int)
    if fem.dof_nodes == 2: # in 2D
        if fix_type == 'x':
            fix[:, 1] = 1
        elif fix_type == 'y':
            fix[:, 0] = 1
        elif fix_type == 'xy':
            return fix
        else:
            print('Please check "fix_type"')
            exit()
    elif fem.dof_nodes == 3: # in 3D
        if fix_type == 'x': # [fix] only x dirextion
            fix[:, 1] = 1
            fix[:, 2] = 1
        elif fix_type == 'y': # [fix] only y dirextion
            fix[:, 0] = 1
            fix[:, 2] = 1
        elif fix_type == 'z': # [fix] only z dirextion
            fix[:, 0] = 1
            fix[:, 1] = 1
        elif fix_type == 'yz' or fix_type == 'zy':
            # [fix] only yz dirextion
            fix[:, 0] = 1
        elif fix_type == 'xz' or fix_type == 'zx':
            # [fix] only xz dirextion
            fix[:, 1] = 1
        elif fix_type == 'xy' or fix_type == 'yx':
            # [fix] only xy dirextion
            fix[:, 2] = 1
        elif fix_type == 'xyz': # [fix] all dirextion
            return fix
        else:
            print('Please check "fix_type"')
            exit()
    return fix

#-----------------------------------------------------------------------------#
def set_fix(fem, idx, fix):
    """
    This function set fix nodes and get free node index [fem.freenode_idx].

    Parameters
    ----------
    fem : class
        FEM class
    idx : ndarray, 1-D
        Fix nodes ID.
    fix : ndarray, 2-D
        Fix type array ("0" fix, "1" not fix).
    """
    shape = (fem.num_nodes, fem.dof_nodes)
    fem.bc = np.ones(shape, dtype=int)
    for i in range(idx.shape[0]):
        fem.bc[idx[i], :] = fix[i]
    fem.num_freedof = np.sum(fem.bc)
    idx = np.where(fem.bc == 1)
    fem.freenode_idx = np.zeros(shape, dtype=int)
    fem.freenode_idx[idx] = np.arange(fem.num_freedof) + 1
    fem.freenode_idx -= 1

#-----------------------------------------------------------------------------#
def set_load_oneside2D(nodes, elems, mesh_info, idx, P, direction):
    force = np.zeros_like(nodes)
    force_nodes = nodes[idx]
    # get line element
    elems_idx = np.where(np.sum(np.isin(elems, idx), axis=1) > 1)[0]
    elems_l = elems[elems_idx]
    lines = elems_l[np.isin(elems_l, idx)].reshape(elems_idx.shape[0], -1)
    # 積分点の位置と重みの取得
    quadorder = 2; qt = 'GAUSS'; sdim = 1
    gauss_W, gauss_Q = quadrature(quadorder, qt, sdim)
    # 線分情報の取得
    if mesh_info['elem_type'] == 'T3' or mesh_info['elem_type'] == 'Q4':
        num_linenodes = 2
    elif mesh_info['elem_type'] == 'T6' or mesh_info['elem_type'] == 'Q8':
        num_linenodes = 3
        lines = lines[:, [0,2,1]]

    if num_linenodes == 2:
        shape_func = shape_function('L2')
    elif num_linenodes == 3:
        shape_func = shape_function('L3')

    for l in range(lines.shape[0]):
        for ix in range(quadorder):
            dxdu = np.zeros(2)
            N, dNdxi = shape_func(gauss_Q[ix])
            for dim in range(2):
                v = 0.0
                for inode in range(num_linenodes):
                    v += dNdxi[inode, 0]*nodes[lines[l, inode], dim]
                dxdu[dim] = v
            jacobian = np.sqrt(dxdu[0]**2 + dxdu[1]**2)
            for inode in range(num_linenodes):
                force[lines[l, inode], direction]\
                += N[inode, 0]*P*gauss_W[ix, 0]*jacobian
    return force

#-----------------------------------------------------------------------------#
