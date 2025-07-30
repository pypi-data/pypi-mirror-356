#coding:UTF-8

"""
# Name    : _mlstools.py
# Autohr  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Oct. 02 2023
# Note    : Moveing least square tools program
"""

import numpy as np

#-----------------------------------------------------------------------------#
def mls_basis(mls_type, x0, pts, support_size):
    """
    This functionr returns the moving least square interpolant
    basis and its gradients w.r.t the parent coordinate system.

    Parameters
    ----------
    mls_type : str
        moving least square type
    x0 : ndarray, 1-D
        pioints
    pts : ndarray, 2-D
        points
    support_size : float
        support size
    """
    nn = len(pts)

    #>> Judge MLS type
    if mls_type[0:3] == 'MLS':
        interpolation = 1
    else:
        interpolation = 0
        print('Interpolation %s is not supported.' % mls_type[0:3])
        N = []; dNdxi = []

    #>> Judge MLS dimension
    if mls_type[3:5] == '1D': num_dim = 1
    elif mls_type[3:5] == '2D': num_dim = 2
    elif mls_type[3:5] == '3D': num_dim = 3
    else:
        num_dim = 0
        print('Dimension %s is not supported.' % mls_type[3:5])
        N = []; dNdxi = []

    #>> Judge MLS order
    if mls_type[5] == '1':
        num_order = 1
    elif mls_type[5] == '2':
        num_order = 2
    elif mls_type[5] == '3':
        num_order = 3
    else:
        num_order = 0
        print('Order %s is not supported.' % mls_type[5])
        N = []; dNdxi = []
    if pts.shape[1] != num_dim:
        print('Error %d coordinates needed for the MLS' % num_dim)
    if nn < num_order:
        print('Error minimum %d points needed for the MLS' % num_order)

    if interpolation == 1:
        if num_dim == 1: # one dimensional interpolation
            xi = np.zeros((nn, num_dim), dtype=float)
            ri = np.zeros(nn, dtype=float)
            xi = pts - x0
            ri = np.sqrt(xi**2)
            wt, dwdr = weight('SPLINE4', ri, support_size)

            if num_order == 1:
                # P[n, b] = [p[xi]]
                # B[b, n] = P'W
                P = np.ones((nn, xi.shape[1] + 1), dtype=float)
                B = np.ones((xi.shape[1] + 1, wt.shape[0]), dtype=float)
                P[:, 1] = xi[:, 0]
                B = P.T*wt
                B[0] = P[:, 0]*wt
                B[1] = P[:, 1]*wt
            elif num_order == 2:
                P = np.ones((nn, xi.shape[1] + 2), dtype=float)
                B = np.ones((xi.shape[0] + 2, wt.shape[0]), dtype=float)
                P[:, 1] = xi[:, 0]
                P[:, 2] = xi[:, 0]**2
                B = P.T*wt
            elif num_order == 3:
                P = np.ones((nn, xi.shape[1] + 3), dtype=float)
                B = np.ones((xi.shape[0] + 3, wt.shape[0]), dtype=float)
                P[:, 1] = xi[:, 0]
                P[:, 2] = xi[:, 0]**2
                P[:, 3] = xi[:, 0]**3
                B = P.T*wt

        elif num_dim == 2:
            xi = np.zeros((nn, num_dim), dtype=float)
            ri = np.zeros(nn, dtype=float)
            xi = pts - x0
            ri = np.sqrt(xi[:, 0]**2 + xi[:, 1]**2)
            wt, dwdr = weight('SPLINE4', ri, support_size)

            if num_order == 1:
                P = np.ones((nn, xi.shape[1] + 1), dtype=float)
                B = np.zeros((xi.shape[1] + 1, wt.shape[0]), dtype=float)
                P[:, 1] = xi[:, 0]
                P[:, 2] = xi[:, 1]
                B = P.T*wt
            elif num_order == 2:
                P = np.ones((nn, xi.shape[1]**2 + 2), dtype=float)
                B = np.zeros((xi.shape[1]**2 + 2, wt.shape[0]), dtype=float)
                P[:, 1] = xi[:, 0]
                P[:, 2] = xi[:, 1]
                P[:, 3] = xi[:, 0]**2
                P[:, 4] = xi[:, 0]*xi[:, 1]
                P[:, 5] = xi[:, 1]**2
                B = P.T*wt
            else:
                print('This order is not implemeted')
                exit()
        elif num_dim == 3:
            xi = np.zeros((nn, num_dim), dtype=float)
            ri = np.zeros(nn, dtype=float)
            xi = pts - x0
            ri = np.sqrt(xi[:, 0]**2 + xi[:, 1]**2 + xi[:, 2]**2)
            wt, dwdr = weight('SPLINE4', ri, support_size)

            if num_order == 1:
                P = np.ones((nn, xi.shape[1] + 1), dtype=float)
                B = np.zeros((xi.shape[1] + 1, wt.shape[0]), dtype=float)
                P[:, 1] = xi[:, 0]
                P[:, 2] = xi[:, 1]
                P[:, 3] = xi[:, 2]
                B = P.T*wt
            elif num_order == 2:
                print('This order is not implemeted')
                exit()
                '''
                P = np.ones((nn, xi.shape[1]**2 + 2), dtype=float)
                B = np.zeros((xi.shape[1]**2 + 2, wt.shape[0]), dtype=float)
                P[:, 1] = xi[:, 0]
                P[:, 2] = xi[:, 1]
                P[:, 3] = xi[:, 2]
                P[:, 4] = xi[:, 0]**2
                P[:, 5] = xi[:, 0]*xi[:, 1]
                P[:, 6] = xi[:, 1]**2
                P[:, 7] = xi[:, 0]*xi[:, 2]
                P[:, 8] = xi[:, 1]*xi[:, 2]
                P[:, 9] = xi[:, 2]**2
                P[:,10] = xi[:, 0]
                P[:,11] = xi[:, 1]
                P[:,12] = xi[:, 2]
                '''
        A = np.dot(B, P) # A[b, b] = P'WP = BP
        A1 = np.linalg.inv(A) # A^(-1)
        A1B = np.dot(A1, B)

        Nv = A1B[0, :] # N'[n] = p'A^(-1) B = P'A1B
        IPA1B = np.eye(nn) - np.dot(P, A1B) # IPA1B[n][n] = A^(-1)P'
        A1P = np.dot(A1, P.T) # A1P[m,n] = A^(-1)P'

        pA1Pdwdr = A1P[0]*dwdr # pA1Pdwdr = p'A^(-1)P'dwdr = A^(-1)P'[0,:]dwdr

        dNdxi01 = np.zeros_like(xi, dtype=float)
        for i in range(xi.shape[1]):
            dNdxi01[:, i] = pA1Pdwdr*xi[:, i]
        # ((A^-1) B)' p, k
        # dw/dx = -dw/dr *dr/dx because xi = |pts-x|
        # W, k = dw/dr * dr/dx
        dNdxi = A1B[1:3, :].T - IPA1B.T.dot(dNdxi01)
    return Nv, dNdxi

#-----------------------------------------------------------------------------#
def weight(ip_type, ri, support_size):
    """
    This function returns the weight of point for mls

    """
    if support_size <= 0:
        print('Error support_size shoud not be greater than zero')
    wt = np.zeros(ri.shape[0], dtype=float)
    nr = np.zeros(ri.shape[0], dtype=float)
    dwdr = np.zeros(ri.shape[0], dtype=float)

    if ip_type == 'SPLINE4':
        # Spline 4 : Quadric spline
        # wt = 1 - 6d^2 + 8d^3 - 3d^4 = 1+(-6+(8-3d)d)d^2
        # dw = -12d + 24d^2 - 12d^3 = (-12+(24-12d)d)d
        nr = ri / support_size # normalize
        wx = 1.0 + (-6.0 + (8.0 - 3.0*nr)*nr)*nr**2
        dwx = (-12.0+(24.0 - 12.0*nr)*nr)*nr
    else:
        print('Weight %s is not supported.' % ip_type)
    return wx, dwx

#-----------------------------------------------------------------------------#
