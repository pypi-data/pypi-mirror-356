#coding:UTF-8

"""
# Name    : _matrixtools.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : finite element method tool program
"""

import numpy as np
from ._shapefunctions import shape_function
from ._mlstools import mls_basis

#-----------------------------------------------------------------------------#
def delta2disp(fem, delta):
    """
    This function returns node displacement with fixed nodes.

    Parameters
    ----------
    fem : class
        FEM class
    delta : ndarray, 2-D
        displacement data without fixed nodes.

    Returns
    -------
    disp : ndarry
        node displacement with fixed nodes.
    """
    disp = np.zeros_like((fem.num_nodes, fem.dof_nodes), dtype=float)
    disp = delta[fem.freenode_idx.reshape(-1, 1)].reshape(-1, fem.dof_nodes)
    index = np.where(fem.freenode_idx == -1)
    disp[index] = 0.0
    return disp

#-----------------------------------------------------------------------------#
def disp2delta(fem, disp):
    """
    This function returns node displacement without fixed nodes.

    Parameters
    ----------
    fem : class
        FEM class
    disp : ndarray, 2D
        node displacement with fixed nodes.

    Returns
    -------
    delta : ndarray, 2D
        node displacement without fixed nodes.
    """
    index = np.where(fem.freenode_idx != -1)
    delta = disp[index].reshape(-1, 1)
    return delta

#-----------------------------------------------------------------------------#
def get_elem(fem, ipt, nodes, elems):
    """
    This function returns the coordinates of the nodes
    of element ipt and its steeering vector

    Parameters
    ----------
    fem : class
        FEM2D class
    ipt : int
        element number
    nodes : ndarray, 2-D
        nodes data
    elems : ndarray, 2-D
        element data

    Returns
    -------
    coordinates : ndarray, 2-D
        coordinates of element node
    nodes_index : ndarray, 1-D
        k matrix index array
    """

    #for i in range(fem.num_nnelm):
    #    for j in range(fem.dof_nodes):
    #        l = i*fem.dof_nodes + j
    #        fem.elemnode_coord[i, j] = nodes[elems[ipt, i], j]
    #        fem.elemnode_index[l] = fem.freenode_idx[elems[ipt, i], j]
    #return fem.elemnode_coord, fem.elemnode_index
    coordinates = nodes[elems[ipt]]
    nodes_index = fem.freenode_idx[elems[ipt]].ravel()
    return coordinates, nodes_index

#-----------------------------------------------------------------------------#
def make_b_matrix(fem, deriv):
    """
    This function make 'B' matrix.

    Parameters
    ----------
    fem : class
        FEM2D class
    deriv : ndarray, 2-D

    Returns
    -------
    b_matrix : ndarray, 2-D
        Calculated 'B' matrix
    """
    fem.b_matrix.fill(0.0)
    if fem.dof_nodes == 2:
        fem.b_matrix[0, 0::2] = deriv[0,:]
        fem.b_matrix[1, 1::2] = deriv[1,:]
        fem.b_matrix[2, 0::2] = deriv[1,:]
        fem.b_matrix[2, 1::2] = deriv[0,:]

    elif fem.dof_nodes == 3:
        fem.b_matrix[0, 0::3] = deriv[0,:]
        fem.b_matrix[1, 1::3] = deriv[1,:]
        fem.b_matrix[2, 2::3] = deriv[2,:]
        fem.b_matrix[3, 0::3] = deriv[1,:]
        fem.b_matrix[3, 1::3] = deriv[0,:]
        fem.b_matrix[4, 0::3] = deriv[2,:]
        fem.b_matrix[4, 2::3] = deriv[0,:]
        fem.b_matrix[5, 1::3] = deriv[2,:]
        fem.b_matrix[5, 2::3] = deriv[1,:]
    return fem.b_matrix

#-----------------------------------------------------------------------------#
def make_global_force_vector(fem, force):
    global_force = np.zeros((fem.num_freedof, 1), dtype=float)
    for i in range(fem.num_nodes):
        if fem.freenode_idx[i, 0] != -1:
            global_force[fem.freenode_idx[i, 0]] = force[i, 0]
        if fem.freenode_idx[i, 1] != -1:
            global_force[fem.freenode_idx[i, 1]] = force[i, 1]
    return global_force

#-----------------------------------------------------------------------------#
def make_global_stiffness_matrix(fem, nodes, elems):
    #>> Numerical integration and assembly of the global stiffness matrix
    ke = np.zeros((fem.dof_elems, fem.dof_elems), dtype=float)
    kg = np.zeros((fem.num_freedof, fem.num_freedof), dtype=float)
    shape_func = shape_function(fem.elem_type)
    for i in range(fem.num_elems):
        coord, g = get_elem(fem, i, nodes, elems)
        #>> Calculate element stiffness matrix
        make_element_stiffness_matrix(fem, coord, ke, shape_func)
        #>> Assemble global stiffness matrix
        assemble_k_matrix(fem, kg, ke, g)
    ### End of assembly ###
    return kg

#-----------------------------------------------------------------------------#
def make_element_stiffness_matrix(fem, coord, ke, shape_func):
    #>> Calculate element stiffness matrix
    ke.fill(0.0)
    for j in range(fem.W.shape[0]):
        weight = fem.W[j, 0]
        pt = fem.Q[j]
        N, dNdxi = shape_func(pt)
        jacob = np.dot(coord.T, dNdxi)
        jacob_inv = np.linalg.inv(jacob)
        jacob_det = np.linalg.det(jacob)
        deriv = np.dot(dNdxi, jacob_inv)
        b_matrix = make_b_matrix(fem, deriv.T)

        #>> Integrate stiffness matrix
        if fem.stress_state == 'plane_stress':
            ke += jacob_det*weight*fem.thick\
                *np.dot(np.dot(b_matrix.T, fem.d_matrix), b_matrix)
        elif fem.stress_state == 'plane_strain':
            ke += jacob_det*weight\
                *np.dot(np.dot(b_matrix.T, fem.d_matrix), b_matrix)


#-----------------------------------------------------------------------------#
def assemble_k_matrix(fem, kk, ke, g):
    """
    This function assemble the global stiffness matrix.

    Parameters
    ----------
    fem : class
        FEM2D class
    kk : ndarray, 2-D
        Global stiffness matrix
    ke : ndarray, 2-D
        Element sfiffness matrix
    g : ndarray, 1-D
        Index of global stiffness matrix
    """
    for i in range(fem.dof_elems):
        if g[i] != -1:
            for j in range(fem.dof_elems):
                if g[j] != -1:
                    kk[g[i], g[j]] += ke[i, j]

#-----------------------------------------------------------------------------#
def force_symmetric(A, eps=1e-10):
    """
    This function convert force symmetirc matrix
    強制的に対称行列に修正

    Parameters
    ----------
    A : ndarray(2D)
    eps : float
    """
    for i in range(A.shape[0]):
        for j in range((i+1), A.shape[1]):
            if np.abs(A[i, j] - A[j, i]) < eps:
                A[j, i] = A[i, j]


#-----------------------------------------------------------------------------#
def calculate_gp_stress_strain(fem, nodes, elems, delta):
    """
    This function calculate coordinate of gauss point and
    stress and stress of each gauss point

    Parameters
    ----------
    fem : class
        FEM2D class
    nodes : ndarray, 2-D
        Nodes data
    elems : ndarray, 2-D
        Element data
    delta : ndarray, 2-D
        Displacement

    Returns
    -------
    coords_gp : ndarray, 2-D
        Coordinate of gauss points
    stress_gp : ndarray, 2-D
        Stress at each gauss points
    strain_gp : ndarray, 2-D
        Strain at each gauss points
    """
    num_gp = fem.W.shape[0]
    coords_gp = np.zeros((fem.num_elems*num_gp, 2), dtype=float)
    stress_gp = np.zeros((fem.num_elems*num_gp, 3), dtype=float)
    strain_gp = np.zeros((fem.num_elems*num_gp, 3), dtype=float)
    elem_disp = np.zeros((fem.dof_elems, 1), dtype=float)

    shape_func = shape_function(fem.elem_type)
    for i in range(fem.num_elems):
        coord, g = get_elem(fem, i, nodes, elems)
        index = np.where(g != -1)
        elem_disp.fill(0.0)
        elem_disp[index] = delta[g[index]]

        for j in range(num_gp):
            idx = i*num_gp + j
            pt = fem.Q[j]
            N, dNdxi = shape_func(pt)
            jacob = np.dot(coord.T, dNdxi)
            jacob_inv = np.linalg.inv(jacob)
            deriv = np.dot(dNdxi, jacob_inv)
            b_matrix = make_b_matrix(fem, deriv.T)
            eps = np.dot(b_matrix, elem_disp)
            sigma = np.dot(fem.d_matrix, eps)
            coords_gp[idx, :] = np.dot(coord.T, N).T[0]
            stress_gp[idx, :] = sigma.T
            strain_gp[idx, :] = eps.T
    return coords_gp, stress_gp, strain_gp

#-----------------------------------------------------------------------------#
def calculate_elementalvalue(fem, stress_gp, strain_gp):
    """
    This function calculate elemental value of stress and strain.
    ガウス点の平均値を要素の値として返す

    Parameters
    ----------
    fem : class
        FEM2D class
    stress_gp : ndarray, 2-D
        Stress at each gauss points
    strain_gp : ndarray, 2-D
        Strain at each gauss points
    """
    num_gp = fem.W.shape[0]
    #>> Elemental value
    stress_e = np.zeros((fem.num_elems, 3), dtype=float)
    strain_e = np.zeros((fem.num_elems, 3), dtype=float)
    for i in range(fem.num_elems):
        idx_s = (i + 0)*num_gp
        idx_e = (i + 1)*num_gp
        stress_e[i] = np.mean(stress_gp[idx_s:idx_e, :], axis=0)
        strain_e[i] = np.mean(strain_gp[idx_s:idx_e, :], axis=0)
    return stress_e, strain_e

#-----------------------------------------------------------------------------#
def calculate_nodalvalue(fem, value, nodes, elems, val_type):
    """
    This function averages nodal value.
    周辺要素の値の平均値を節点解として返す

    Parameters
    ----------
    fem : class
        FEM2D class
    value : ndarray, 2-D
        Stress or strain array
    nodes : ndarray, 2-D
        node data
    elems : ndarray, 2-D
        element data
    val_type : str
        'stress' or 'strain'

    Returns
    -------
    values : ndarray, 2-D
        calculated nodal value
    """

    if fem.dof_nodes == 2: # 2D
        value_n = np.zeros((fem.num_nodes, 3), dtype=float)
    elif fem.dof_nodes == 3: # 3D
        value_n = np.zeros((fem.num_nodes, 6), dtype=float)
    for i in range(fem.num_nodes):
        index = np.where(elems == i)[0]
        value_n[i] = np.mean(value[index], axis=0)
    return value_n

#-----------------------------------------------------------------------------#
def calculate_nodalvalue2(fem, value, nodes, elems):
    """
    主応力の計算
    value : nodal value
    """

    if fem.dof_nodes == 2: # 2D
        values = np.zeros((fem.num_nodes, 2), dtype=float)
    elif fem.dof_nodes == 3: # 3D
        values = np.zeros((fem.num_nodes, 3), dtype=float)

    if fem.dof_nodes == 2: # 2D
        for i in range(fem.num_nodes):
            xx = value[i, 0]
            yy = value[i, 1]
            xy = value[i, 2]

            sqrt_value = np.sqrt(((xx + yy) / 2)**2 + xy**2)
            values[i, 0] = ((xx + yy) / 2 + sqrt_value)
            values[i, 1] = ((xx + yy) / 2 - sqrt_value)

    elif fem.dof_nodes == 3: #3D
        for i in range(fem.num_nodes):
            xx = value[i, 0]; yy = value[i, 1]
            zz = value[i, 2]; xy = value[i, 3]
            xz = value[i, 4]; yz = value[i, 5]
            tensor = np.array([\
                [xx, xy, xz],\
                [xy, yy, yz],\
                [xz, yz, zz]])
            values[i, :] = np.linalg.eigvals(tensor)

    return values

#-----------------------------------------------------------------------------#
def calculate_stress_strain(fem, nodes, elems, delta, option=None):
    """
    Calculate stress and strain

    Parameters
    ----------
    """
    coords_gp, stress_gp, strain_gp\
     = calculate_gp_stress_strain(fem, nodes, elems, delta)

    if option == None:
        out_type = 'nodal'
        mls_type = 'MLS2D1'
        mls_size = 1.1
    else:
        out_type = option['out_type']
        mls_type = option['mls_type']
        mls_size = option['mls_size']


    if out_type == 'element':
        # 要素の値を取得
        if fem.elem_type == 'T3':
            return stress_gp, strain_gp
        else:
            # ガウス点の平均値を要素の値として返す
            stress, strain = calculate_elementalvalue(fem, stress_gp, strain_gp)
    else:
        # 節点の値を取得
        if fem.elem_type == 'T3':
            # 三角形1次要素の場合は，周辺要素の平均値を節点の値として返す
            stress = calculate_nodalvalue(fem, stress_gp, nodes, elems, 'stress')
            strain = calculate_nodalvalue(fem, strain_gp, nodes, elems, 'strain')
        else:
            # それ以外は移動最小二乗法による補間で節点の値を返す
            stress, strain\
            = calculate_nodalstressstrain_mls(fem, nodes, elems,\
                                              coords_gp, stress_gp, strain_gp,\
                                              mls_type, mls_size)

    return stress, strain


#-----------------------------------------------------------------------------#
def calculate_nodalstressstrain_mls(fem, nodes, elems,\
                                    coords_gp, stress_gp, strain_gp,\
                                    mls_type, mls_size):
    """
    Calculate nodal stress and strain using mls
    """
    num_gp = fem.W.shape[0]
    #mls_type = 'MLS2D1'
    stress_n = np.zeros((fem.num_nodes, 3), dtype=float)
    strain_n = np.zeros((fem.num_nodes, 3), dtype=float)
    for i in range(fem.num_nodes):
        elem_idx = np.where(elems == i)[0]
        length = get_length(nodes, elems, elem_idx)
        support_size = length*mls_size
        gp_idx = np.zeros(elem_idx.shape[0]*num_gp, dtype=int)
        for j in range(elem_idx.shape[0]):
            idx_st = elem_idx[j]*num_gp
            idxs = idx_st + np.arange(num_gp)
            gp_idx[j*num_gp:(j+1)*num_gp] = idxs
            coords = coords_gp[gp_idx]
            stress = stress_gp[gp_idx]
            strain = strain_gp[gp_idx]
        xn = nodes[i]
        pts = coords
        N, dNdxi = mls_basis(mls_type, xn, pts, support_size)
        stress_n[i] = np.dot(N, stress)
        strain_n[i] = np.dot(N, strain)

    return stress_n, strain_n

#-----------------------------------------------------------------------------#

def get_length(nodes, elems, elem_idx):
    for i, eidx in enumerate(elem_idx):
        coords = nodes[elems[eidx]]
        size_x = np.max(coords[:,0]) - np.min(coords[:,0])
        size_y = np.max(coords[:,1]) - np.min(coords[:,1])
        tmplen = np.sqrt(size_x**2 + size_y**2)
        if i == 0:
            length = tmplen
        else:
            if length < tmplen:
                length = tmplen
    return length














