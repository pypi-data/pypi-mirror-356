#coding:UTF-8

import numpy as np

from ._quadtools import quadrature
from ._shapefunctions import shape_function

#-----------------------------------------------------------------------------#
def conv_fast_bc(fem, nodes, elems, bce):
    """
    This function converts ``FAST`` boundary condition data.

    Parameters
    ----------
    fem : class
        cratch fem class.
    nodes : ndarray, 2-D
        Node data.
    elems : ndarray, 2-D
        Element data.
    bce : class
        ``FAST`` boundary condition data class.

    Returns
    -------
    disp : ndarray, 2-D
        Displacement data.
    fix : ndarry, 2-D
        Fix data. (fix:0, unfix:1)
    force : ndarray, 2-D
        Force data.
    """
    disp = np.zeros_like(nodes, dtype=float)
    fix = np.ones_like(nodes, dtype=int)
    force = np.zeros_like(nodes, dtype=float)
    disp[:,:] = np.nan

    if bce.bc_dist_load:
        if nodes.shape[1] == 2:
            conv_fast_dist_load_2d(nodes, elems, force, bce.bc_dist_load)
        else:
            print('Sorry... 2d only...')
            exit()
    if bce.bc_con_force:
        conv_fast_con_force(force, bce.bc_con_force)
    if bce.bc_disp:
        conv_fast_disp_fix(nodes, disp, fix, bce.bc_disp)

    #>> Update fem class (set fix)
    fem.bc = fix
    fem.num_freedof = np.sum(fem.bc)
    idx = np.where(fem.bc == 1)
    fem.freenode_idx = np.zeros_like(nodes, dtype=int)
    fem.freenode_idx[idx]  = np.arange(fem.num_freedof) + 1
    fem.freenode_idx -= 1

    return disp, fix, force

#-----------------------------------------------------------------------------#
def conv_fast_dist_load_2d(nodes, elems, force, bc_dist_load):
    """
    This function returns converted distributed load data
    from ``FAST`` data to Equivalent nodal force.

    Parameters
    ----------
    nodes : ndarray, 2-D
        Node data.
    elems : ndarray, 2-D
        Element data.
    force : ndarray, 2-D
        Force data.
    bc_dist_load : list

    Returns
    -------
    force : ndarray, 2-D
        Converted force data.
    """
    shape_func = shape_function('L3')
    quadorder = 2; qt = 'GAUSS'; sdim = 1
    gauss_W, gauss_Q = quadrature(quadorder, qt, sdim)

    node_type = [[0,4,1], [1,5,2], [2,6,3], [3,7,0]]
    num_linenodes = 3
    for data in bc_dist_load:
        elem_id = int(data[0]) - 1
        type_id = int(data[1]) - 1
        direction = int(data[2]) - 1
        value = float(data[3])
        node_id = elems[elem_id][node_type[type_id]]
        for ix in range(quadorder):
            dxdu = np.zeros(2)
            N, dNdxi = shape_func(gauss_Q[ix])
            for dim in range(2):
                v = 0.0
                for inode in range(num_linenodes):
                    v += dNdxi[inode, 0]*nodes[node_id[inode], dim]
                dxdu[dim] = v
            jacobian = np.sqrt(dxdu[0]**2 + dxdu[1]**2)
            for inode in range(num_linenodes):
                force[node_id[inode], direction]\
                += N[inode, 0]*value*gauss_W[ix, 0]*jacobian
    return force

#-----------------------------------------------------------------------------#
def conv_fast_con_force(force, bc_con_force):
    """
    This function returns force data.

    Parameters
    ----------
    force : ndarray, 2-D
        Force data.
    bc_con_force
        Concentrated force data.

    Return
    ------
    force : ndarray, 2-D
        Force data.
    """

    for data in bc_con_force:
        node_id = int(data[0]) - 1
        direction = int(data[1]) - 1
        value = float(data[2])
        force[node_id, direction] = value
    return force

#-----------------------------------------------------------------------------#
def conv_fast_disp_fix(nodes, disp, fix, bc_disp):
    """
    This function convert dicpacement condition from ``FAST`` data
    to disp and fix array.

    Parameters
    ----------
    nodes : ndarray, 2-D
        Node data.
    disp : ndarray, 2-D
        Displacement data.
    fix : ndarray, 2-D
        Fix data.
    bc_disp : list
        Displacement boundary condition data.

    Returns
    -------
    disp : ndarray, 2-D
        Displacement data.
    fix : ndarray, 2-D
        Fix data.
    """

    for data in bc_disp:
        node_id = int(data[0]) - 1
        direction = int(data[1]) - 1
        value = float(data[2])
        if value == 0.0:
            fix[node_id, direction] = 0
        disp[node_id, direction] = value
    #idx = np.where(np.isnan(disp)==False)

    return disp, fix

#-----------------------------------------------------------------------------#
