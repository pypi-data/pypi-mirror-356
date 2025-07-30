#coding:UTF-8

"""
# Name    : _shape_functions.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Finite element method tool program get shape function
"""

import numpy as np

#-----------------------------------------------------------------------------#
def shape_function(elem_type):
    """
    This function returns the vectors of the shape function
    and their derivatives with respect to xi and eta.

    Parameters
    ----------
    elem_type : str
        element type

    Returns
    -------
    N : ndarray, 2-D
        shape function
    dNdxi : ndarray, 2-D
        derived shape function

    """
    if elem_type == 'L2':
        return shape_func_L2
    elif elem_type == 'L3':
        return shape_func_L3
    elif elem_type == 'T3':
        return shape_func_T3
    elif elem_type == 'T4':
        return shape_func_T4
    elif elem_type == 'T6':
        return shape_func_T6
    elif elem_type == 'Q4':
        return shape_func_Q4
    elif elem_type == 'Q8':
        return shape_func_Q8
    elif elem_type == 'Q9':
        return shape_func_Q9
    elif elem_type == 'H4':
        return shape_func_H4
    elif elem_type == 'H10':
        return shape_func_H10
    elif elem_type == 'B8':
        return shape_func_B8
    elif elem_type == 'B20':
        return shape_func_B20
    else:
        print('%s element is not supported' % elem_type)
        exit()

#-----------------------------------------------------------------------------#
def shape_func_L2(pt):
    r"""
        L2 : Two node line element
            >>>
            1-------2
    """
    if pt.shape[0] < 1:
        print('Element error: coordinate needed for L2 element')
        exit()
    else:
        xi = pt[0]
        N = np.array([[1.0 - xi], \
                      [1.0 + xi]])*0.5
        dNdxi = np.array([[-1.0],[1.0]])*0.5
        return N, dNdxi

#-----------------------------------------------------------------------------#
def shape_func_L3(pt):
    r"""
        L3 : Three node line element
            >>>
            1---2---3
    """
    if pt.shape[0] < 1:
        print('Element error: coordinate needed for L3 element')
        exit()
    else:
        xi = pt[0]
        N = np.array([\
            [0.5*xi*(xi - 1.0)],\
            [(1.0 - xi)*(1.0 + xi)],\
            [0.5*xi*(xi + 1.0)]
            ])
        dNdxi = np.array([\
            [0.5*(2.0*xi - 1.0)],\
            [-2.0*xi],\
            [0.5*(2.0*xi + 1.0)]])
        return N, dNdxi

#-----------------------------------------------------------------------------#
def shape_func_T3(pt):
    r"""
        T3 : Three node triangular element
            >>>
                3
               / \
              /   \
             /     \
            1-------2
    """
    if pt.shape[0] < 2:
        print('Element error: two coordinate needed for T3 element')
        exit()
    else:
        xi = pt[0]
        eta = pt[1]
        N = np.array([\
            [(1.0 - xi - eta)],
            [xi],\
            [eta] ])
        dNdxi = np.array([\
            [-1.0, -1.0],\
            [ 1.0,  0.0],\
            [ 0.0,  1.0]])
        return N, dNdxi

#-----------------------------------------------------------------------------#
def shape_func_T4(pt):
    r"""
        T4 : Four node triangular element
            >>>
                3
               / \
              / 4 \
             /     \
            1-------2
    """
    if pt.shape[0] < 2:
        print('Element error: two coordinate needed for T4 element')
        exit()
    else:
        xi = pt[0]
        eta = pt[1]
        N = np.array([\
            [1.0 - xi - eta - 3.0*xi*eta],\
            [xi * (1.0 - 3.0*eta)],\
            [eta * (1.0 - 3.0*xi)],\
            [9.0 * xi * eta]])
        dNdxi = np.array([\
            [-1.0 - 3.0*eta, -1.0 - 3.0*xi],\
            [ 1.0 - 3.0*eta, -3.0*xi],\
            [-3.0*eta,        1.0 - 3.0*xi],\
            [ 9.0*eta,        9.0*xi]])
        return N, dNdxi

#-----------------------------------------------------------------------------#
def shape_func_T6(pt):
    r"""
        T6 : Six node triangular element
            >>>
                3
               / \
              6   5
             /     \
            1---4---2
    """
    if pt.shape[0] < 2:
        print('Element error: two coordinate needed for T6 element')
        exit()
    else:
        xi = pt[0]
        eta = pt[1]
        N = np.array([\
            [1.0 - 3.0*(xi+eta) + 4.0*xi*eta + 2*(xi**2 + eta**2)],\
            [xi*(2*xi - 1.0)],\
            [eta*(2*eta - 1.0)],\
            [4.0*xi*(1.0 - xi - eta)],\
            [4.0*xi*eta],\
            [4.0*eta*(1.0 - xi - eta)]])
        dNdxi = np.array([\
            [ 4.0*(xi + eta) - 3.0,      4.0*(xi + eta) - 3.0],\
            [ 4.0*xi - 1.0,              0.0],\
            [ 0.0,                       4.0*eta - 1.0],\
            [ 4.0*(1.0 - eta - 2.0*xi), -4.0*xi],\
            [ 4.0*eta,                   4.0*xi],\
            [-4.0*eta,                   4.0*(1.0 - xi - 2.0*eta)] ])
        return N, dNdxi

#-----------------------------------------------------------------------------#
def shape_func_Q4(pt):
    r"""
        Q4 : Four node quadrilateral element
            >>>
            4-------3
            |       |
            |       |
            |       |
            1-------2
    """
    if pt.shape[0] < 2:
        print('Element error: two coordinate needed for Q4 element')
        exit()
    else:
        xi = pt[0]
        eta = pt[1]
        N = np.array([\
            [(1.0 - xi)*(1.0 - eta)],\
            [(1.0 + xi)*(1.0 - eta)],\
            [(1.0 + xi)*(1.0 + eta)],\
            [(1.0 - xi)*(1.0 + eta)] ]) * 0.25
        dNdxi = np.array([\
            [-(1.0 - eta), -(1.0 - xi)],\
            [ (1.0 - eta), -(1.0 + xi)],\
            [ (1.0 + eta),  (1.0 + xi)],\
            [-(1.0 + eta),  (1.0 - xi)] ]) *  0.25
        return N, dNdxi

#-----------------------------------------------------------------------------#
def shape_func_Q8(pt):
    r"""
        Q8 : Eight node quadrilateral element
            >>>
            4---7---3
            |       |
            8       6
            |       |
            1---5---2
    """
    if pt.shape[0] < 2:
        print('Element error: two coordinate needed for Q8 element')
        exit()
    else:
        xi = pt[0]
        eta = pt[1]
        etam = 1.0 - eta
        etap = 1.0 + eta
        xim = 1.0 - xi
        xip = 1.0 + xi

        N = np.array([\
            [-1.0*xim*etam*(1.0 + xi + eta)],\
            [-1.0*xip*etam*(1.0 - xi + eta)],\
            [-1.0*xip*etap*(1.0 - xi - eta)],\
            [-1.0*xim*etap*(1.0 + xi - eta)],\
            [ 2.0*(1.0 - xi*xi)*etam],\
            [ 2.0*(1.0 - eta*eta)*xip],\
            [ 2.0*(1.0 - xi*xi)*etap],\
            [ 2.0*(1.0 - eta*eta)*xim] ])*0.25

        dNdxi = np.array([\
            [1.0*etam*(2.0*xi + eta),  1.0*xim*(xi + 2.0*eta)],\
            [1.0*etam*(2.0*xi - eta), -1.0*xip*(xi - 2.0*eta)],\
            [1.0*etap*(2.0*xi + eta),  1.0*xip*(xi + 2.0*eta)],\
            [1.0*etap*(2.0*xi - eta), -1.0*xim*(xi - 2.0*eta)],\
            [           -4.0*etam*xi,      -2.0*(1.0 - xi**2)],\
            [     2.0*(1.0 - eta**2),            -4.0*xip*eta],\
            [           -4.0*etap*xi,       2.0*(1.0 - xi**2)],\
            [    -2.0*(1.0 - eta**2),            -4.0*xim*eta]])*0.25
        return N, dNdxi

#-----------------------------------------------------------------------------#
def shape_func_Q9(pt):
    r"""
        Q9 : Nine node quadrilateral element
            >>>
            4---7---3
            |       |
            8   9   6
            |       |
            1---5---2
    """
    if pt.shape[0] < 2:
        print('Element error: two coordinate needed for Q9 element')
        exit()
    else:
        xi = pt[0]
        eta = pt[1]
        N = np.array([\
            [  xi*eta*(xi - 1.0)*(eta - 1.0)],\
            [  xi*eta*(xi + 1.0)*(eta - 1.0)],\
            [  xi*eta*(xi + 1.0)*(eta + 1.0)],\
            [  xi*eta*(xi - 1.0)*(eta + 1.0)],\
            [-2.0*eta*(xi + 1.0)*(xi  - 1.0)*(eta - 1.0)],\
            [ -2.0*xi*(xi + 1.0)*(eta + 1.0)*(eta - 1.0)],\
            [-2.0*eta*(xi - 1.0)*(xi  + 1.0)*(eta + 1.0)],\
            [ -2.0*xi*(xi - 1.0)*(eta - 1.0)*(eta + 1.0)],\
            [4.0*(xi + 1.0)*(xi - 1.0)*(eta + 1.0)*(eta - 1.0)]])*0.25
        dNdxi = np.array([\
            [eta*(2.0*xi-1.0)*(eta-1.0), xi*(xi-1.0)*(2.0*eta-1.0)],\
            [eta*(2.0*xi+1.0)*(eta-1.0), xi*(xi+1.0)*(2.0*eta-1.0)],\
            [eta*(2.0*xi+1.0)*(eta+1.0), xi*(xi+1.0)*(2.0*eta+1.0)],\
            [eta*(2.0*xi-1.0)*(eta+1.0), xi*(xi-1.0)*(2.0*eta+1.0)],\
            [-4.0*xi*eta*(eta-1.0), -2.0*(xi+1.0)*(xi-1.0)*(2*eta-1.0)],\
            [-2.0*(eta+1.0)*(eta-1.0)*(2*xi+1.0), -4.0*xi*eta*(xi+1.0)],\
            [-4.0*xi*eta*(eta+1.0), -2.0*(xi+1.0)*(xi-1.0)*(2*eta+1.0)],\
            [-2.0*(eta+1.0)*(eta-1.0)*(2*xi-1.0), -4.0*xi*eta*(xi-1.0)],\
            [8.0*xi*(eta*eta-1.0), 8.0*eta*(xi*xi-1.0)]])*0.25
        return N, dNdxi

#-----------------------------------------------------------------------------#
def shape_func_H4(pt):
    r"""
        H4 : Four node tetrahedral element
            >>>
                4
               /|\
              / | \
             /  |  \
            1---+---3
             `  |  `
              ` | `
               `2`
    """
    if pt.shape[0] < 3:
        print('Element error: three coordinate needed for H4 element')
        exit()
    else:
        xi = pt[0]
        eta = pt[1]
        zeta = pt[2]
        N = np.array([\
            [1.0-xi-eta-zeta],
            [xi],
            [eta],
            [zeta]])
        dNdxi = np.array([\
            [-1.0, -1.0, -1.0],\
            [ 1.0,  0.0,  0.0],\
            [ 0.0,  1.0,  0.0],\
            [ 0.0,  0.0,  1.0]])
        return N, dNdxi

#-----------------------------------------------------------------------------#
def shape_func_H10(pt):
    r"""
        H10 : Ten node tetrahedral element
            >>>
                4
               /|\
              8 | 10
             /  |9 \
            1---+---3
             `  |7 `
              5 | 6
               `2`
    """
    if pt.shape[0] < 3:
        print('Element error: three coordinate needed for H10 element')
        exit()
    else:
        xi = pt[0]
        eta = pt[1]
        zeta = pt[2]
        L0 = 1.0-xi-eta-zeta
        L1 = xi
        L2 = eta
        L3 = zeta
        N = np.array([
            [L0*(2*L0 - 1.0)],\
            [L1*(2*L1 - 1.0)],\
            [L2*(2*L2 - 1.0)],\
            [L3*(2*L3 - 1.0)],\
            [4.0*L0*L1],\
            [4.0*L1*L2],\
            [4.0*L0*L2],\
            [4.0*L0*L3],\
            [4.0*L1*L3],\
            [4.0*L2*L3] ])
        dNdxi = np.array([\
            [1.0 - 4.0*L0, 1.0 - 4.0*L0, 1.0 - 4.0*L0],
            [  4.0*L1-1.0,          0.0,          0.0],
            [         0.0, 4.0*L2 - 1.0,          0.0],
            [         0.0,          0.0,   4.0*L3-1.0],
            [ 4.0*(L0-L1),      -4.0*L1,      -4.0*L1],
            [      4.0*L2,       4.0*L1,          0.0],
            [     -4.0*L2,  4.0*(L0-L2),      -4.0*L2],
            [     -4.0*L3,      -4.0*L3,  4.0*(L0-L3)],
            [      4.0*L3,          0.0,       4.0*L1],
            [         0.0,       4.0*L3,       4.0*L2] ])
        return N, dNdxi

#-----------------------------------------------------------------------------#
def shape_func_B8(pt):
    r"""
        B8 : Eight node brick element
            >>>
               8_______7
              /|      /|
             / |     / |
            5--+----6  |
            |  4----+--3
            | /     | /
            |/      |/
            1-------2
    """
    if pt.shape[0] < 3:
        print('Element error: three coordinate needed for B8 element')
        exit()
    else:
        xi = pt[0]
        eta = pt[1]
        zeta = pt[2]
        I1 = 1/2 - pt/2
        I2 = 1/2 + pt/2
        N = np.array([\
            [I1[0]*I1[1]*I1[2]],\
            [I2[0]*I1[1]*I1[2]],\
            [I2[0]*I2[1]*I1[2]],\
            [I1[0]*I2[1]*I1[2]],\
            [I1[0]*I1[1]*I2[2]],\
            [I2[0]*I1[1]*I2[2]],\
            [I2[0]*I2[1]*I2[2]],\
            [I1[0]*I2[1]*I2[2]]])
        dNdxi = np.array([\
            [-1.0+eta+zeta-eta*zeta, -1.0+xi+zeta-xi*zeta, -1.0+xi+eta-xi*eta],\
            [ 1.0-eta-zeta+eta*zeta, -1.0-xi+zeta+xi*zeta, -1.0-xi+eta+xi*eta],\
            [ 1.0+eta-zeta-eta*zeta,  1.0+xi-zeta-xi*zeta, -1.0-xi-eta-xi*eta],\
            [-1.0-eta+zeta+eta*zeta,  1.0-xi-zeta+xi*zeta, -1.0+xi-eta+xi*eta],\
            [-1.0+eta-zeta+eta*zeta, -1.0+xi-zeta+xi*zeta,  1.0-xi-eta+xi*eta],\
            [ 1.0-eta+zeta-eta*zeta, -1.0-xi-zeta-xi*zeta,  1.0+xi-eta-xi*eta],\
            [ 1.0+eta+zeta+eta*zeta,  1.0+xi+zeta+xi*zeta,  1.0+xi+eta+xi*eta],\
            [-1.0-eta-zeta-eta*zeta,  1.0-xi+zeta-xi*zeta,  1.0-xi+eta-xi*eta]])/8.0
        N = np.array([\
            [(1.0 - xi)*(1.0 - eta)*(1.0 - zeta)],\
            [(1.0 + xi)*(1.0 - eta)*(1.0 - zeta)],\
            [(1.0 + xi)*(1.0 + eta)*(1.0 - zeta)],\
            [(1.0 - xi)*(1.0 + eta)*(1.0 - zeta)],\
            [(1.0 - xi)*(1.0 - eta)*(1.0 + zeta)],\
            [(1.0 + xi)*(1.0 - eta)*(1.0 + zeta)],\
            [(1.0 + xi)*(1.0 + eta)*(1.0 + zeta)],\
            [(1.0 - xi)*(1.0 + eta)*(1.0 + zeta)]])*0.125
        dNdxi = np.array([\
            [-(1.0 - eta)*(1.0 - zeta), -(1.0 - xi)*(1.0 - zeta), -(1.0 - xi)*(1.0 - eta)],\
            [ (1.0 - eta)*(1.0 - zeta), -(1.0 + xi)*(1.0 - zeta), -(1.0 + xi)*(1.0 - eta)],\
            [ (1.0 + eta)*(1.0 - zeta),  (1.0 + xi)*(1.0 - zeta), -(1.0 + xi)*(1.0 + eta)],\
            [-(1.0 + eta)*(1.0 - zeta),  (1.0 - xi)*(1.0 - zeta), -(1.0 - xi)*(1.0 + eta)],\
            [-(1.0 - eta)*(1.0 + zeta), -(1.0 - xi)*(1.0 + zeta),  (1.0 - xi)*(1.0 - eta)],\
            [ (1.0 - eta)*(1.0 + zeta), -(1.0 + xi)*(1.0 + zeta),  (1.0 + xi)*(1.0 - eta)],\
            [ (1.0 + eta)*(1.0 + zeta),  (1.0 + xi)*(1.0 + zeta),  (1.0 + xi)*(1.0 + eta)],\
            [-(1.0 + eta)*(1.0 + zeta),  (1.0 - xi)*(1.0 + zeta),  (1.0 - xi)*(1.0 + eta)]\
            ])*0.125
        return N, dNdxi

#-----------------------------------------------------------------------------#
def shape_func_B20(pt):
    r"""
        B20 : Twenty node brick element
            >>>
               8_______7
              /|      /|
             / |     / |
            5--+----6  |
            |  4----+--3
            | /     | /
            |/      |/
            1-------2
    """
    if pt.shape[0] < 3:
        print('Element error: three coordinate needed for B8 element')
        exit()
    else:
        xi = pt[0]
        eta = pt[1]
        zeta = pt[2]

        N = np.array([
            [ 0.125*(xi-1.0)*(eta-1.0)*(zeta-1.0)*(zeta+eta+xi+2.0)],\
            [-0.125*(xi+1.0)*(eta-1.0)*(zeta-1.0)*(zeta+eta-xi+2.0)],\
            [ 0.125*(xi+1.0)*(eta+1.0)*(zeta-1.0)*(zeta-eta-xi+2.0)],\
            [-0.125*(xi-1.0)*(eta+1.0)*(zeta-1.0)*(zeta-eta+xi+2.0)],\
            [ 0.125*(xi-1.0)*(eta-1.0)*(zeta+1.0)*(zeta-eta-xi-2.0)],\
            [-0.125*(xi+1.0)*(eta-1.0)*(zeta+1.0)*(zeta-eta+xi-2.0)],\
            [ 0.125*(xi+1.0)*(eta+1.0)*(zeta+1.0)*(zeta+eta+xi-2.0)],\
            [-0.125*(xi-1.0)*(eta+1.0)*(zeta+1.0)*(zeta+eta-xi-2.0)],\
            [ -0.25*(xi-1.0)*(xi+1.0)*(eta-1.0)*(zeta-1.0)],\
            [  0.25*(xi+1.0)*(eta-1.0)*(eta+1.0)*(zeta-1.0)],\
            [  0.25*(xi-1.0)*(xi+1.0)*(eta+1.0)*(zeta-1.0)],\
            [ -0.25*(xi-1.0)*(eta-1.0)*(eta+1.0)*(zeta-1.0)],\
            [  0.25*(xi-1.0)*(xi+1.0)*(eta-1.0)*(zeta+1.0)],\
            [ -0.25*(xi+1.0)*(eta-1.0)*(eta+1.0)*(zeta+1.0)],\
            [ -0.25*(xi-1.0)*(xi+1.0)*(eta+1.0)*(zeta+1.0)],\
            [  0.25*(xi-1.0)*(eta-1.0)*(eta+1.0)*(zeta+1.0)],\
            [ -0.25*(xi-1.0)*(eta-1.0)*(zeta-1.0)*(zeta+1.0)],\
            [  0.25*(xi+1.0)*(eta-1.0)*(zeta-1.0)*(zeta+1.0)],\
            [ -0.25*(xi+1.0)*(eta+1.0)*(zeta-1.0)*(zeta+1.0)],\
            [  0.25*(xi-1.0)*(eta+1.0)*(zeta-1.0)*(zeta+1.0)]])

        dNdxi = np.zeros((20,3), dtype=float)
        dNdxi[0, 0] = 0.125*(zeta-1.0)*(eta-1.0)*(2.0*xi+eta+zeta+1.0)
        dNdxi[1, 0] = 0.125*(zeta-1.0)*(eta-1.0)*(2.0*xi-eta-zeta-1.0)
        dNdxi[2, 0] =-0.125*(zeta-1.0)*(eta+1.0)*(2.0*xi+eta-zeta-1.0)
        dNdxi[3, 0] =-0.125*(zeta-1.0)*(eta+1.0)*(2.0*xi-eta+zeta+1.0)
        dNdxi[4, 0] =-0.125*(zeta+1.0)*(eta-1.0)*(2.0*xi+eta-zeta+1.0)
        dNdxi[5, 0] =-0.125*(zeta+1.0)*(eta-1.0)*(2.0*xi-eta+zeta-1.0)
        dNdxi[6, 0] = 0.125*(zeta+1.0)*(eta+1.0)*(2.0*xi+eta+zeta-1.0)
        dNdxi[7, 0] = 0.125*(zeta+1.0)*(eta+1.0)*(2.0*xi-eta-zeta+1.0)
        dNdxi[8, 0] =  -0.5*(zeta-1.0)*(eta-1.0)*xi
        dNdxi[9, 0] =  0.25*(zeta-1.0)*(eta-1.0)*(eta+1.0)
        dNdxi[10,0] =   0.5*(zeta-1.0)*(eta+1.0)*xi
        dNdxi[11,0] = -0.25*(zeta-1.0)*(eta-1.0)*(eta+1.0)
        dNdxi[12,0] =   0.5*(zeta+1.0)*(eta-1.0)*xi
        dNdxi[13,0] = -0.25*(zeta+1.0)*(eta-1.0)*(eta+1.0)
        dNdxi[14,0] =  -0.5*(zeta+1.0)*(eta+1.0)*xi
        dNdxi[15,0] =  0.25*(zeta+1.0)*(eta-1.0)*(eta+1.0)
        dNdxi[16,0] = -0.25*(zeta-1.0)*(zeta+1.0)*(eta-1.0)
        dNdxi[17,0] =  0.25*(zeta-1.0)*(zeta+1.0)*(eta-1.0)
        dNdxi[18,0] = -0.25*(zeta-1.0)*(zeta+1.0)*(eta+1.0)
        dNdxi[19,0] =  0.25*(zeta-1.0)*(zeta+1.0)*(eta+1.0)

        dNdxi[0, 1] = 0.125*(zeta-1.0)*(xi-1.0)*(xi+2.0*eta+zeta+1.0)
        dNdxi[1, 1] = 0.125*(zeta-1.0)*(xi+1.0)*(xi-2.0*eta-zeta-1.0)
        dNdxi[2, 1] =-0.125*(zeta-1.0)*(xi+1.0)*(xi+2.0*eta-zeta-1.0)
        dNdxi[3, 1] =-0.125*(zeta-1.0)*(xi-1.0)*(xi-2.0*eta+zeta+1.0)
        dNdxi[4, 1] =-0.125*(zeta+1.0)*(xi-1.0)*(xi+2.0*eta-zeta+1.0)
        dNdxi[5, 1] =-0.125*(zeta+1.0)*(xi+1.0)*(xi-2.0*eta+zeta-1.0)
        dNdxi[6, 1] = 0.125*(zeta+1.0)*(xi+1.0)*(xi+2.0*eta+zeta-1.0)
        dNdxi[7, 1] = 0.125*(zeta+1.0)*(xi-1.0)*(xi-2.0*eta-zeta+1.0)
        dNdxi[8, 1] = -0.25*(zeta-1.0)*(xi-1.0)*(xi+1.0)
        dNdxi[9, 1] =   0.5*(zeta-1.0)*eta*(xi+1.0)
        dNdxi[10,1] =  0.25*(zeta-1.0)*(xi-1.0)*(xi+1.0)
        dNdxi[11,1] =  -0.5*(zeta-1.0)*eta*(xi-1.0)
        dNdxi[12,1] =  0.25*(zeta+1.0)*(xi-1.0)*(xi+1.0)
        dNdxi[13,1] =  -0.5*(zeta+1.0)*eta*(xi+1.0)
        dNdxi[14,1] = -0.25*(zeta+1.0)*(xi-1.0)*(xi+1.0)
        dNdxi[15,1] =   0.5*(zeta+1.0)*eta*(xi-1.0)
        dNdxi[16,1] = -0.25*(zeta-1.0)*(zeta+1.0)*(xi-1.0)
        dNdxi[17,1] =  0.25*(zeta-1.0)*(zeta+1.0)*(xi+1.0)
        dNdxi[18,1] = -0.25*(zeta-1.0)*(zeta+1.0)*(xi+1.0)
        dNdxi[19,1] =  0.25*(zeta-1.0)*(zeta+1.0)*(xi-1.0)

        dNdxi[0, 2] = 0.125*(eta-1.0)*(xi-1.0)*(xi+eta+2.0*zeta+1.0)
        dNdxi[1, 2] = 0.125*(eta-1.0)*(xi+1.0)*(xi-eta-2.0*zeta-1.0)
        dNdxi[2, 2] =-0.125*(eta+1.0)*(xi+1.0)*(xi+eta-2.0*zeta-1.0)
        dNdxi[3, 2] =-0.125*(eta+1.0)*(xi-1.0)*(xi-eta+2.0*zeta+1.0)
        dNdxi[4, 2] =-0.125*(eta-1.0)*(xi-1.0)*(xi+eta-2.0*zeta+1.0)
        dNdxi[5, 2] =-0.125*(eta-1.0)*(xi+1.0)*(xi-eta+2.0*zeta-1.0)
        dNdxi[6, 2] = 0.125*(eta+1.0)*(xi+1.0)*(xi+eta+2.0*zeta-1.0)
        dNdxi[7, 2] = 0.125*(eta+1.0)*(xi-1.0)*(xi-eta-2.0*zeta+1.0)
        dNdxi[8, 2] = -0.25*(eta-1.0)*(xi-1.0)*(xi+1.0)
        dNdxi[9, 2] =  0.25*(eta-1.0)*(eta+1.0)*(xi+1.0)
        dNdxi[10,2] =  0.25*(eta+1.0)*(xi-1.0)*(xi+1.0)
        dNdxi[11,2] = -0.25*(eta-1.0)*(eta+1.0)*(xi-1.0)
        dNdxi[12,2] =  0.25*(eta-1.0)*(xi-1.0)*(xi+1.0)
        dNdxi[13,2] = -0.25*(eta-1.0)*(eta+1.0)*(xi+1.0)
        dNdxi[14,2] = -0.25*(eta+1.0)*(xi-1.0)*(xi+1.0)
        dNdxi[15,2] =  0.25*(eta-1.0)*(eta+1.0)*(xi-1.0)
        dNdxi[16,2] =  -0.5*zeta*(eta-1.0)*(xi-1.0)
        dNdxi[17,2] =   0.5*zeta*(eta-1.0)*(xi+1.0)
        dNdxi[18,2] =  -0.5*zeta*(eta+1.0)*(xi+1.0)
        dNdxi[19,2] =   0.5*zeta*(eta+1.0)*(xi-1.0)

        return N, dNdxi

#-----------------------------------------------------------------------------#
