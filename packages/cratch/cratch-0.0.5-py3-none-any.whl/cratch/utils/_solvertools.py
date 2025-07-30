#coding:UTF-8

"""
# Name    : _solvertools.py
# Autohr  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : finite element method tool program
"""

import numpy as np
import matplotlib.pyplot as plt
import ctypes
import copy

import time
from ._shapefunctions import shape_function
from ._matrixtools import (
    get_elem,
    force_symmetric,
    make_b_matrix,
    make_element_stiffness_matrix
)

from ._ptrtools import get_ctypestools

#-----------------------------------------------------------------------------#
def load_local_library(lib_path, lib_name):
    """
    This function returns local c library.

    Parameters
    ----------
    lib_path : str
        Local library path
    lib_name : str
        Local library name

    Returns
    -------
    ctypes.cdll[libpath] : library object
        A ctypes library object
    """
    import os
    import inspect
    assert os.path.exists(lib_path+lib_name),\
        '[Error] The local library was not found.'

    return np.ctypeslib.load_library(lib_name, lib_path)

#-----------------------------------------------------------------------------#
def load_local_solver(lib, method):
    """
    This function returns local c solver.

    Parameters
    ----------
    lib : library object
        Loaded local c library object
    method : str
        'GE' : Gaussian elimination solver (DS)
        'LU' : LU solver (DS)
        'GS' : Gauss seidel solver (IS)
        'JACOBI' : Jacobi solver (IS)
        'SOR' : SOR solver (IS)
        'CG' : Conjugate gradient solver (IS)
        'ICCG' : I.C. Conjugate gradient solver (IS)
        [DS: Direct solver, IS: Iterative solver]
    Returns
    -------
    solver
    """

    ndpointer, c_int, c_int_p, c_int_pp,\
    c_double, c_double_p, c_double_pp = get_ctypestools()

    if method == 'GE':
        solver = lib.GaussianElimination
    elif method == 'GS':
        solver = lib.GSSolver
    elif method == 'LU':
        solver = lib.LUSolver
    elif method == 'JACOBI':
        solver = lib.JacobiSolver
    elif method == 'SOR':
        solver = lib.SORSolver
    elif method == 'CG':
        solver = lib.CGSolver
    elif method == 'ICCG':
        solver = lib.ICCGSolver
    else:
        print('[Error] Please check method.')
        exit()

    solver.argtypes = [c_int, c_double_pp, c_double_p, c_double_p]
    solver.restype = None
    return solver

#-----------------------------------------------------------------------------#
'''
def get_ctypestools():
    """
    This function return ctypes pointer tools
    """

    ndpointer = np.ctypeslib.ndpointer
    c_int = ctypes.c_int
    c_int_p = ctypes.POINTER(c_int)
    c_int_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')
    c_double = ctypes.c_double
    c_double_p = ctypes.POINTER(c_double)
    c_double_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')

    return ndpointer, c_int, c_int_p, c_int_pp,\
           c_double, c_double_p, c_double_pp
'''
#-----------------------------------------------------------------------------#
def convert_pointer(arr):
    """
    This function convert nparray to pointer of c langeuage

    Parameters
    ----------
    arr : ndarray(2D)

    Returns
    -------
    pointer
    """
    if len(arr.shape) == 1: # 1D array
        v_type = type(arr[0])
        if v_type == np.float64:
            p_type = ctypes.POINTER(ctypes.c_double)
        elif v_type == np.int32:
            p_type = ctypes.POINTER(ctypes.c_int)
        pointer = arr.ctypes.data_as(p_type)
    elif len(arr.shape) == 2: # 2D array
        pointer = (arr.__array_interface__['data'][0]\
                  + np.arange(arr.shape[0])*arr.strides[0]).astype(np.uintp)
    else:
        print('array dimensional error.')
        exit()
    return pointer

#-----------------------------------------------------------------------------#
def check_matrix(A):
    if A.shape[0] != A.shape[1]:
        print('Error :matrix A must be square.')
        exit()
    if not np.array_equal(A,A.T):
        print('Error :matrix A must be symmetric.')
        exit()
    if not np.all(np.linalg.eigvals(A) > 0):
        print('Error :matrix A is at least not positive definite.')
        exit()


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def fem_solver_test():
    lib_name = 'fem_solver.so'
    lib_path = './femtools/fem_solver/lib/'
    lib = np.ctypeslib.load_library(lib_name, lib_path)

    row = 2
    col = 5
    n = 4.5
    matrix1 = np.random.rand(col)
    matrix2 = np.random.rand(row, col)

    matrix3 = np.array([1,2,3,4,5], dtype=np.int32)
    matrix4 = np.array([[1,2,3,4,5],[6,7,8,9,0]], dtype=np.int32)

    ndpointer = np.ctypeslib.ndpointer
    c_int = ctypes.c_int
    c_int_p = ctypes.POINTER(c_int)
    c_int_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')
    c_double = ctypes.c_double
    c_double_p = ctypes.POINTER(c_double)
    c_double_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')

    n = c_double(n)
    row = c_int(row)
    col = c_int(col)

    ite = 1
    #ite = c_int(ite)
    ite_p = ctypes.pointer(c_int(ite))
    #print(ite_p)
    #exit()

    #>> 引数の型指定(argtypes)と戻り値の型指定(restype)

    lib.test1d_double.argtypes = [c_double_p, c_int, c_double]
    lib.test1d_double.restype = None
    pnt = convert_pointer(matrix1)
    print('before:\n', matrix1)
    lib.test1d_double(pnt, col, n)
    print('after:\n', matrix1)

    lib.test2d_double.argtypes = [c_double_pp, c_int, c_int, c_double]
    lib.test2d_double.restype = None
    pnt = convert_pointer(matrix2)
    print('before:\n', matrix2)
    lib.test2d_double(pnt, row, col, n)
    print('after:\n', matrix2)

    lib.test1d_int.argtypes = [c_int_p, c_int]
    lib.test1d_int.restype = None
    pnt = convert_pointer(matrix3)
    print('before:\n', matrix3)
    lib.test1d_int(pnt, col)
    print('after:\n', matrix3)

    lib.test2d_int.argtypes = [c_int_pp, c_int, c_int, c_int_p]
    lib.test2d_int.restype = None
    pnt = convert_pointer(matrix4)
    print('before:\n', matrix4)
    lib.test2d_int(pnt, row, col, ite_p)
    print('after:\n', matrix4)

    print( np.int32(ite_p.contents))
    exit()

#-----------------------------------------------------------------------------#
def symmetric_sor(A, x0, b):
    force_symmetric(A, 1e-8)
    omega = 1.1
    eps = 1e-8
    residual = 1.0
    ite = 1
    check_matrix(A)

    C = np.triu(A)
    #print('C'); print(C)
    #print(C.shape)
    size_a = np.zeros(C.shape[0], dtype=int) # after
    size_b = np.zeros(C.shape[0], dtype=int) # before
    for i in range(C.shape[0]):
        size_a[i] = np.where(C[i,:] != 0)[0][-1]
        size_b[i] = np.where(C[:,i] != 0)[0][0]
    size_a = size_a - np.arange(C.shape[0])
    #print('before',size_b)
    #print('after ',size_a)
    #exit()
    x1 = np.copy(x0)
    while residual > eps:
        tmp = np.copy(x1)
        for i in range(x1.shape[0]):
            before = 0.0
            for j in range(size_b[i], i):
                before += C[j,i] * x1[j,0]
                #print('before j, i :', j, i, before, C[j,i], x1[j,0])
            after = 0.0
            for j in range(size_a[i]):
                after += C[i,i+j+1] * x1[i+j+1,0]
                #print('after  i, j :', i, i+j+1)
            #print('C',C[i,i], before, after)
            x1[i][0] = (omega / C[i,i])*(b[i][0] - before - after) + (1.0-omega)*x1[i][0]
            #print('before', i, before)
            #print('after', after)
        #print(x1)
        residual = np.linalg.norm(x1 - tmp)
        print(f'\r\033[Kite:%6d, residual: %.6e' %(ite, residual), end='')
        #print(f'\r\033[K[OK] Allocate memory')
        ite += 1

    #print(x1)
    print('ite:%6d, residual: %.6e' %(ite, residual))
    #x = np.linalg.solve(A, b)
    #print(x)
    #exit()
    return x1

#-----------------------------------------------------------------------------#
def solver_sor(A, b, tol):
    xOld = np.zeros_like(b)
    residual = 1e12
    D = np.diag(np.diag(A))
    L = np.tril(A, -1)
    U = A - L - D
    Mj = np.dot(np.linalg.inv(D), -(L+U))
    rho_Mj = max(abs(np.linalg.eigvals(Mj)))
    w = 2.0/(1.0+np.sqrt(1.0 - rho_Mj**2))

    T = np.linalg.inv(D+w*L)
    Lw = np.dot(T, -w*U+(1-w)*D)
    c = np.dot(T, w*b)
    while residual > tol:
        x = np.dot(Lw, xOld) + c
        residual = np.linalg.norm(x - xOld)/np.linalg.norm(x)
        xOld = x
    return x

#-----------------------------------------------------------------------------#
def solver_sor1(A, b, tol):
    tol = 1e-9
    np.random.seed(314)
    omega = 1.1
    D = np.diag(A)
    R = A - np.diag(D)
    #x = np.random.random(b.shape[0]).reshape(b.shape)
    x = np.zeros_like(b)-1.0
    #x = np.random.random(len(b))
    residual = 1e20
    
    while residual > tol:
        x0 = x.copy()
        for i in range(x.shape[0]):
            aa = (1.0 - omega)*x0[i]
            bb = omega*(b[i] - R[i]@x)/D[i]
            x[i] = aa + bb
        residual = np.linalg.norm((x - x0)) / np.linalg.norm(x)
        print(residual)
        #print(residual, np.linalg.norm(x))
        #residual = np.sum(np.sqrt((x - x0)**2)) / np.sum(np.sqrt(x**2))
        #print(residual)
        #exit()

        #print( (x - x_old)**2 )
        #print(x_old)
        #exit()
        #residual = np.slinalg.norm(x - x_old) / np.linalg.norm(x)
        #print(residual)
        #x_old = x
        #exit()
    #print(x)
    #exit()
    return x

#-----------------------------------------------------------------------------#
def solver_cg(A, b, k):
    """ 3x3 matrix only """
    if A.shape[0] != 3:
        print('solver_cg is 3x3 matrix only')
        #A = np.array([[1,0,0],[0,2,0],[0,0,1]])
        #b = np.array([[4],[5],[6]])
        exit()
    alpha = 0.0
    x = np.zeros_like(b)
    m = A.T*(A*x-b)
    t = -(np.tensordot(m, A.T*(A*x-b)))/(np.tensordot(m, A.T*A*m))
    x = x + t*m
    eps = 1e-8
    residual = 1.0
    while residual > eps:
        tmp = x.copy()
        alpha = -(np.tensordot(m, A.T*A*A.T*(A*x-b)))/(np.tensordot(m, A.T*A*m))
        m = A.T * (A*x - b) + alpha*m
        t = -(np.tensordot(m, A.T*(A*x-b)))/(np.tensordot(m, A.T*A*m))
        x = x + t*m
        residual = np.linalg.norm(x-tmp)
        print(residual)
    return np.diag(x).reshape(b.shape)
    #return np.diag(x).reshape(b.shape)

#-----------------------------------------------------------------------------#
def ichol(A):
    print(f'\r\033[Kpreconditioning ...')
    AA = np.copy(A)
    n = AA.shape[1]
    for k in range(n):
        AA[k,k] = np.sqrt(AA[k,k])
        idx = np.where(AA[k+1:, k] != 0.0)[0] + (k+1)
        AA[idx, k] /= AA[k, k]

        for j in range(k+1, n):
            for i in range(j, n):
                if AA[i,j] != 0:
                    AA[i,j] -= AA[i,k] * AA[j,k]

    for i in range(n):
        AA[i, i+1:] = 0.0

    #plt.imshow(AA, cmap=plt.cm.jet)
    #plt.colorbar()
    #plt.show()
    #exit()
    print(f'\r\033[Fpreconditioning END')
    print('')
    return AA




#def iccg_solver(A, x, b):
    

#-----------------------------------------------------------------------------#
def conjugate_gradients(A, x, b):
    """
    不完全コレスキー分解付き共役勾配法ソルバー
    ICCG(Incomplete Cholesky Conjugate Gradient method)
    """
    #http://www.grimnes.no/algorithms/preconditioned-conjugate-gradients-method-matrices/
    print('[  ] Solve matrix. [iccg_solver]')
    residual = b - np.dot(A, x)
    preconditioner = np.linalg.inv(ichol(A))
    z = np.dot(preconditioner, residual)
    d = z
    error = np.dot(residual.T, residual)

    iterate = 0
    while error > 1e-8:
    #while error > 1e-6:
        q = np.dot(A,d)
        a = np.dot(residual.T, z) / np.dot(d.T, q)

        phi = np.dot(z.T, residual)
        old_res = residual

        x = x + a*d
        residual = residual - a*q

        z = np.dot(preconditioner, residual)
        beta = np.dot(z.T, (residual - old_res))/phi
        d = z + beta * d
        error = np.dot(residual.T, residual)[0][0]
        iterate += 1
        #print('ite, error', iterate, error)
        print(f'\r\033[Kite:%6d, residual: %.6e' %(iterate, error), end='')
    residual = error
    print(f'\r\033[F[OK] Solve matrix.')
    print(f'\r     ite: %5d, residual: %.4e' % (iterate, residual))
    return x

#-----------------------------------------------------------------------------#
def cg_solver(A, x, b):
    """
    共役勾配法ソルバー
    """
    print('[  ] Solve matrix. [cg_solver]')
    residual = b - np.dot(A, x)
    d = residual
    g_new = np.dot(residual.T, residual)
    max_ite = 1e4
    max_err = 1e-8
    iteration = 0
    while iteration < max_ite and g_new > max_err**2:
        q = np.dot(A, d)
        a = g_new / np.dot(d.T, q)
        x = x + a*d
        residual = residual - a*q

        g_old = g_new
        g_new = np.dot(residual.T, residual)

        beta = g_new / g_old
        d = residual + beta*d
        iteration += 1
        error = np.dot(residual.T, residual)[0][0]
        print(f'\r\033[Kite:%6d, residual: %.6e' %(iteration, error), end='')

    if iteration > max_ite:
        print('Convergence failed. [iteration over]')
        exit()
    residual = error
    print(f'\r\033[F[OK] Solve matrix.')
    print(f'\r     ite: %5d, residual: %.4e' % (iteration, residual))

    return x

#-----------------------------------------------------------------------------#
def set_direchlet_bc(info):
    for iNode in range(info.num_nodes):
        indexi = info.start_index[iNode]
        bc0 = 1.0
        bc1 = 1.0

        if info.eq_bc[2*iNode + 0] < 0.5:
            info.eq_a[indexi + 0] = 1.0
            info.eq_a[indexi + 1] = 0.0
            info.eq_a[indexi + 2] = 0.0
            bc0 = 0.0
        if info.eq_bc[2*iNode + 1] < 0.5:
            info.eq_a[indexi + 1] = 0.0
            info.eq_a[indexi + 2] = 0.0
            info.eq_a[indexi + 3] = 1.0
            bc1 = 0.0

        for jNode, nodeIDj in enumerate(info.nodeID[iNode][1:], 1):
            #nodeIDj = info.nodeID[iNode][jNode]

            info.eq_a[indexi + 4*jNode + 0] *= bc0
            info.eq_a[indexi + 4*jNode + 1] *= bc0
            info.eq_a[indexi + 4*jNode + 2] *= bc1
            info.eq_a[indexi + 4*jNode + 3] *= bc1
            if info.eq_bc[2*nodeIDj + 0] < 0.5:
                info.eq_a[indexi + 4*jNode + 0] = 0.0
                info.eq_a[indexi + 4*jNode + 2] = 0.0
            if info.eq_bc[2*nodeIDj + 1] < 0.5:
                info.eq_a[indexi + 4*jNode + 1] = 0.0
                info.eq_a[indexi + 4*jNode + 3] = 0.0

#-----------------------------------------------------------------------------#
def convert_nodeID(nodeID): # to 2d int array
    #>> nodeIDは長さの異なる2dリストなので
    #   2d array に変換し，各節点に関係のある節点数も共に返す
    numIDs = np.array([len(ids) for ids in nodeID], dtype=np.int32)
    nodeID_arr = np.zeros((numIDs.shape[0], np.max(numIDs)), dtype=np.int32)
    for i in range(len(nodeID)):
        for j in range(len(nodeID[i])):
            nodeID_arr[i,j] = nodeID[i][j]

    return numIDs, nodeID_arr

#-----------------------------------------------------------------------------#
def fem_solver_ssor_type_c(info):
    print('[  ] Solve matrix.')
    #lib_name = 'fem_solver.so'
    #lib_path = './femtools/fem_solver/lib/'
    #lib = np.ctypeslib.load_library(lib_name, lib_path)
    import os
    import inspect
    lib_name = 'fem_solver.so'
    lib_path = os.path.dirname(inspect.stack()[0].filename)+'/lib/'
    lib = np.ctypeslib.load_library(lib_name, lib_path)

    #>> type_c settings
    ndpointer, c_int, c_int_p, c_int_pp,\
    c_double, c_double_p, c_double_pp = get_ctypestools()
    #ndpointer = np.ctypeslib.ndpointer
    #c_int = ctypes.c_int
    #c_int_p = ctypes.POINTER(c_int)
    #c_int_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')
    #c_double = ctypes.c_double
    #c_double_p = ctypes.POINTER(c_double)
    #c_double_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')

    #>> use parameters
    A = info.eq_a   # 1d array
    x0 = info.eq_x  # 1d array
    b = info.eq_b   # 1d array
    num_nodes = info.num_nodes # int
    start_index = info.start_index.astype(np.int32) # 1d array
    nodeID = info.nodeID #  2d int list
    x = np.zeros_like(x0, dtype=np.float64)
    tmp = np.zeros_like(x0, dtype=np.float64)
    numIDs, nodeID = convert_nodeID(nodeID) # to 2d int array
    iterate = 0
    residual = 1.0

    #>> convert to pointers
    A_pt = convert_pointer(A)
    x0_pt = convert_pointer(x0)
    b_pt = convert_pointer(b)
    num_nodes = c_int(num_nodes)
    start_index_pt = convert_pointer(start_index)
    x_pt = convert_pointer(x)
    tmp_pt = convert_pointer(tmp)
    numIDs_pt = convert_pointer(numIDs)
    nodeID_pt = convert_pointer(nodeID)
    iterate = ctypes.pointer(c_int(iterate))
    residual = ctypes.pointer(c_double(residual))

    #>> solver settings
    lib.fem_solver_ssor_c.argtypes\
        = [c_double_p, c_double_p, c_double_p,\
           c_int, c_int_p, c_double_p, c_double_p,\
           c_int_p, c_int_pp, c_int_p, c_double_p]
    lib.fem_solver_ssor_c.restype = None

    #>> solve equation
    lib.fem_solver_ssor_c(A_pt, x0_pt, b_pt, num_nodes, start_index_pt,\
                          x_pt, tmp_pt, numIDs_pt, nodeID_pt, iterate, residual)

    iterate = np.int32(iterate.contents)
    residual = np.float64(residual.contents)
    print(f'\r\033[F[OK] Solve matrix.')
    print(f'\r     ite: %5d, residual: %.4e' % (iterate, residual))
    #print('type_c')
    #exit()
    return x

#-----------------------------------------------------------------------------#
def ssor_index_plot(fem):
    test = np.zeros((fem.num_nodes, fem.num_nodes))
    ii = 0
    for i in range(fem.num_nodes*2):
        iNode = i//2
        ii += 1
        #>> after
        for jNode, jnodeID in enumerate(fem.nodeID[iNode][1:], 1):
            test[iNode, jnodeID] = ii
        #>> before
        for jj in range(iNode):
            if iNode in fem.nodeID[jj]:
                test[iNode, jj] = ii
                #test[iNode, jj] = 0

        #>> self
        test[iNode, iNode] = 21

    plt.imshow(test, cmap=plt.cm.jet)
    plt.show()
    exit()

#-----------------------------------------------------------------------------#
def ssor_py(info):
    omega = 1.1
    A = info.eq_a
    x0 = info.eq_x
    b = info.eq_b
    #fem_solver_test()
    #print('test')
    #exit()

    eps = 1e-6
    ite = 1
    residual = 1.0
    x1 = np.copy(x0)
    #>> before
    before = 0.0
    num_before = np.zeros(info.num_nodes, dtype=np.int32)
    before_idx = []
    for iNode in range(info.num_nodes):
        before_idx.append([])
        for jj in range(iNode):
            if iNode in info.nodeID[jj]:
                num_before[iNode] += 1
                idx_eq = info.nodeID[jj].index(iNode)
                index0 = info.start_index[jj]
                before_idx[iNode].append(jj)
                before_idx[iNode].append(idx_eq)
                #print(iNode, jj,  idx_eq, info.nodeID[jj])

    max_ncol = max([len(data) for data in before_idx])
    before_idx_eq = np.zeros((info.num_nodes, max_ncol), dtype=np.int32)

    for iNode in range(info.num_nodes):
        for j in range(len(before_idx[iNode])):
            before_idx_eq[iNode,j] = before_idx[iNode][j]
        #print(iNode, num_before[iNode], before_idx_eq[iNode])



    time_st = time.time()
    while residual > eps:
        tmp = np.copy(x1)
        for i in range(info.num_nodes):
            iNode = i
            index0 = info.start_index[iNode]
            #>> after
            after0 = 0.0; after1 = 0.0
            for jNode, jnodeID in enumerate(info.nodeID[iNode][1:], 1):
                aj00 = A[index0 + jNode*4 + 0]
                aj01 = A[index0 + jNode*4 + 1]
                aj10 = A[index0 + jNode*4 + 2]
                aj11 = A[index0 + jNode*4 + 3]
                after0 += aj00*x1[jnodeID*2+0] + aj01*x1[jnodeID*2+1]
                after1 += aj10*x1[jnodeID*2+0] + aj11*x1[jnodeID*2+1]
            #>> before
            before0 = 0.0; before1 = 0.0
            for j in range(num_before[iNode]):
                jnodeID = before_idx_eq[iNode][j*2]
                idx_eq = before_idx_eq[iNode][j*2+1]
                index0 = info.start_index[jnodeID]
                aj00 = A[index0 + idx_eq*4 + 0]
                aj01 = A[index0 + idx_eq*4 + 1]
                aj10 = A[index0 + idx_eq*4 + 2]
                aj11 = A[index0 + idx_eq*4 + 3]
                before0 += aj00*x1[jnodeID*2+0] + aj10*x1[jnodeID*2+1]
                before1 += aj01*x1[jnodeID*2+0] + aj11*x1[jnodeID*2+1]
            #>> self
            #test[iNode, iNode] = 21
            index0 = info.start_index[iNode]
            a00 = A[index0 + 0]; a01 = A[index0 + 1]
            a10 = A[index0 + 2]; a11 = A[index0 + 3]
            #if flg == 0:
            after0 += a01*x1[i*2+1]
            x1[i*2+0] = (omega / a00)*(b[i*2+0] - before0 - after0) + (1.0-omega)*x1[i*2+0]
            #elif flg == 1:
            before1 += a10*x1[i*2+1-1]
            x1[i*2+1] = (omega / a11)*(b[i*2+1] - before1 - after1) + (1.0-omega)*x1[i*2+1]
        residual = np.linalg.norm(x1 - tmp)
        print(f'\r\033[Kite:%6d, residual: %.6e' %(ite, residual), end='')
        ite += 1
    print('')
    print('TIME :',time.time() - time_st)

    return x1

#-----------------------------------------------------------------------------#
def ssor(info):
    omega = 1.1
    A = info.eq_a
    x0 = info.eq_x
    b = info.eq_b
    #fem_solver_test()
    #print('test')
    #exit()

    eps = 1e-6
    ite = 1
    residual = 1.0

    x1 = np.copy(x0)
    while residual > eps:
        tmp = np.copy(x1)
        for i in range(info.num_nodes):
            iNode = i
            #>> after
            index0 = info.start_index[iNode]
            after0 = 0.0; after1 = 0.0
            for jNode, jnodeID in enumerate(info.nodeID[iNode][1:], 1):
                aj00 = A[index0 + jNode*4 + 0]
                aj01 = A[index0 + jNode*4 + 1]
                aj10 = A[index0 + jNode*4 + 2]
                aj11 = A[index0 + jNode*4 + 3]
                after0 += aj00*x1[jnodeID*2+0] + aj01*x1[jnodeID*2+1]
                after1 += aj10*x1[jnodeID*2+0] + aj11*x1[jnodeID*2+1]

            #>> before
            before0 = 0.0; before1 = 0.0
            for jj in range(iNode):
                if iNode in info.nodeID[jj]:
                    idx_eq = info.nodeID[jj].index(iNode)
                    index0 = info.start_index[jj]
                    aj00 = A[index0 + idx_eq*4 + 0]
                    aj01 = A[index0 + idx_eq*4 + 1]
                    aj10 = A[index0 + idx_eq*4 + 2]
                    aj11 = A[index0 + idx_eq*4 + 3]
                    before0 += aj00*x1[jj*2+0] + aj10*x1[jj*2+1]
                    before1 += aj01*x1[jj*2+0] + aj11*x1[jj*2+1]
            #>> self
            index0 = info.start_index[iNode]
            a00 = A[index0 + 0]; a01 = A[index0 + 1]
            a10 = A[index0 + 2]; a11 = A[index0 + 3]
            #if flg == 0:
            after0 += a01*x1[i*2+0+1]
            x1[i*2+0] = (omega / a00)*(b[i*2+0] - before0 - after0) + (1.0-omega)*x1[i*2+0]
            #elif flg == 1:
            before1 += a10*x1[i*2+1-1]
            x1[i*2+1] = (omega / a11)*(b[i*2+1] - before1 - after1) + (1.0-omega)*x1[i*2+1]

        residual = np.linalg.norm(x1 - tmp)
        print(f'\r\033[Kite:%6d, residual: %.6e' %(ite, residual), end='')
        ite += 1
    print('')

    return x1


#-----------------------------------------------------------------------------#
def global_force2solver(fem, global_force):
    """
    Parameters
    ----------
    fem : class
    global_force : ndarray(1D)

    Returns
    -------
    gf : ndarray(1D)
        converted global force

    global force vectorをsolver用に変換
    """
    #gf = np.zeros_like(fem.bc, dtype=float)
    gf = np.zeros((fem.num_nodes, fem.dof_nodes), dtype=float)
    for i in range(fem.num_nodes):
        for j in range(fem.dof_nodes):
            if fem.freenode_idx[i,j] == -1:
                gf[i,j] = 0.0
            else:
                idx = fem.freenode_idx[i,j]
                gf[i,j] = global_force[idx][0]
    return gf

#-----------------------------------------------------------------------------#
def get_solver_index(fem, elems):
    """
    Parameters
    ----------
    fem : class
    elems : ndarray(2D)

    全体剛性行列のindex情報の取得(関連のある節点の調査)
    """
    fem.related_nodes = [] # 関連のある節点番号
    #>> 先頭を自身の節点番号とする
    for i in range(fem.num_nodes):
        fem.related_nodes.append([i])
    for i in range(fem.num_elems):
        elemnodes = elems[i]
        for inode in elemnodes:
            for jnode in elemnodes:
                if (inode < jnode) and (jnode not in fem.related_nodes[inode]):
                    fem.related_nodes[inode].append(jnode)
    for i in range(fem.num_nodes):
        fem.related_nodes[i].sort()

#-----------------------------------------------------------------------------#
def load_solver():
    import os
    import inspect
    lib_name = 'fem_solver.so'
    lib_path = os.path.dirname(inspect.stack()[0].filename)+'/lib/'
    lib = np.ctypeslib.load_library(lib_name, lib_path)
    print('femsolver loaded')
    return lib

#-----------------------------------------------------------------------------#
def mumpssolver(A, b, x, n, nnz, sym, irn, jcn, lib):
    """
    MUMPS solver.
    """
    from mpi4py import MPI

    #>> Get ctypes pointer tools
    ndpointer, c_int, c_int_p, c_int_pp,\
    c_double, c_double_p, c_double_pp = get_ctypestools()

    #>> Convert pointer
    A_pt = convert_pointer(A)
    b_pt = convert_pointer(b)
    x_pt = convert_pointer(x)
    n = c_int(n)
    nnz = c_int(nnz)
    sym = c_int(sym)
    irn = irn.ctypes.data_as(c_int_p)
    jcn = jcn.ctypes.data_as(c_int_p)

    #>> Set MPI communication parameter
    if MPI._sizeof(MPI.Comm) == ctypes.sizeof(ctypes.c_int):
        MPI_Comm = ctypes.c_int
    else:
        MPI_Comm = ctypes.c_void_p
    comm_ptr = MPI._addressof(MPI.COMM_WORLD)
    comm_val = MPI_Comm.from_address(comm_ptr)

    #>> Solver setting
    solver = lib.mumps_solver
    solver.restype = None
    solver.argtypes = [MPI_Comm, c_int, c_int, c_int, c_int_p, c_int_p,\
                       c_double_p, c_double_p, c_double_p]
    solver(comm_val, sym, n, nnz, irn, jcn, A_pt, b_pt, x_pt)

    #if rank == 0:
    x = copy.deepcopy(b)
    return x

#-----------------------------------------------------------------------------#
def femsolver(fem, nodes, elems, k_global, global_force, solver, lib):

    #>> Get ctypes pointer tools
    ndpointer, c_int, c_int_p, c_int_pp,\
    c_double, c_double_p, c_double_pp = get_ctypestools()


    delta = np.zeros_like(global_force.ravel())
    n = delta.shape[0]
    epsilon = 1e-8
    maxit = 2*n*n
    numit = 0
    kg = copy.deepcopy(k_global)
    gf = copy.deepcopy(global_force)

    A = convert_pointer(kg)
    b = convert_pointer(gf.ravel())
    x = convert_pointer(delta)
    n = c_int(n)
    eps = c_double(epsilon)
    maxit = c_int(maxit)
    numit_pt = ctypes.pointer(c_int(numit))


    #>> Direct solver [Triangle]
    if solver == 'solve_triang':
        solve_triang(lib, n, A, x, b)
    #>> Direct solver [LU solver]
    elif solver == 'solve_lu':
        solve_lu(lib, n, A, x, b)

    #>> Iterative solver [jacobi]
    elif solver == 'solve_jacobi':
        solve_jacobi(lib, n, A, x, b)

    #>> Iterative solver [gauss-seidel]
    elif solver == 'solve_gs':
        solve_gs(lib, n, A, x, b)

    #>> Iterative solver [gauss-seidel omp]
    elif solver == 'solve_gs_omp':
        solve_gs_omp(lib, n, A, x, b)

    #>> Iterative solver [sor]
    elif solver == 'solve_sor':
        solve_sor(lib, n, A, x, b)

    #>> Iterative solver [cg]
    elif solver == 'solve_cg':
        solve_cg(lib, n, A, x, b)

    #>> Iterative solver [iccg]
    elif solver == 'solve_iccg':
        solve_iccg(lib, n, A, x, b)

    delta = delta.reshape(-1,1)
    return delta

#-----------------------------------------------------------------------------#
def solve_triang(lib, n, A, x, b):
    ndpointer, c_int, c_int_p, c_int_pp,\
    c_double, c_double_p, c_double_pp = get_ctypestools()
    lower = False
    lower = c_int(lower)
    #>> Direct solver [Triangle]
    solver = lib.GaussianElimination
    solver.argtypes = [c_int, c_double_pp, c_double_p]
    solver.restype = None
    solver(n, A, b)

    solver = lib.solve_triangular
    solver.argtypes = [c_int, c_double_pp, c_double_p, c_double_p, c_int]
    solver.restype = None
    solver(n, A, b, x, lower)

#-----------------------------------------------------------------------------#
def solve_lu(lib, n, A, x, b):
    ndpointer, c_int, c_int_p, c_int_pp,\
    c_double, c_double_p, c_double_pp = get_ctypestools()
    #>> Direct solver [LU solver]
    solver = lib.lu_solver
    solver.argtypes = [c_int, c_double_pp, c_double_p, c_double_p]
    solver.restype = None
    solver(n, A, x, b)

#-----------------------------------------------------------------------------#
def solve_jacobi(lib, n, A, x, b):
    ndpointer, c_int, c_int_p, c_int_pp,\
    c_double, c_double_p, c_double_pp = get_ctypestools()
    #>> Iterative solver
    solver = lib.jacobi_solver
    solver.argtypes = [c_int, c_double_pp, c_double_p, c_double_p]
    solver.restype = None
    solver(n, A, x, b)

#-----------------------------------------------------------------------------#
def solve_gs(lib, n, A, x, b):
    ndpointer, c_int, c_int_p, c_int_pp,\
    c_double, c_double_p, c_double_pp = get_ctypestools()
    #>> Iterative solver
    solver = lib.gs_solver
    solver.argtypes = [c_int, c_double_pp, c_double_p, c_double_p]
    solver.restype = None
    solver(n, A, x, b)

#-----------------------------------------------------------------------------#
def solve_gs_omp(lib, n, A, x, b):
    ndpointer, c_int, c_int_p, c_int_pp,\
    c_double, c_double_p, c_double_pp = get_ctypestools()
    #>> Iterative solver [parallel]
    solver = lib.gs_solver_omp
    p = 1 # number of threads
    p = c_int(p)
    solver.argtypes = [c_int, c_int, c_double_pp, c_double_p, c_double_p]
    solver.restype = None
    solver(n, p, A, x, b)

#-----------------------------------------------------------------------------#
def solve_sor(lib, n, A, x, b):
    ndpointer, c_int, c_int_p, c_int_pp,\
    c_double, c_double_p, c_double_pp = get_ctypestools()
    #>> Iterative solver
    solver = lib.sor_solver
    solver.argtypes = [c_int, c_double_pp, c_double_p, c_double_p]
    solver.restype = None
    solver(n, A, x, b)

#-----------------------------------------------------------------------------#
def solve_cg(lib, n, A, x, b):
    ndpointer, c_int, c_int_p, c_int_pp,\
    c_double, c_double_p, c_double_pp = get_ctypestools()
    #>> Iterative solver
    solver = lib.cg_solver
    solver.argtypes = [c_int, c_double_pp, c_double_p, c_double_p]
    solver.restype = None
    solver(n, A, x, b)

#-----------------------------------------------------------------------------#
def solve_iccg(lib, n, A, x, b):
    ndpointer, c_int, c_int_p, c_int_pp,\
    c_double, c_double_p, c_double_pp = get_ctypestools()
    #>> Iterative solver
    solver = lib.iccg_solver
    solver.argtypes = [c_int, c_double_pp, c_double_p, c_double_p]
    solver.restype = None
    solver(n, A, x, b)

#-----------------------------------------------------------------------------#
def plot_fem2d_kglobal(fem, A):
    test = np.zeros((fem.num_nodes*2, fem.num_nodes*2))
    A = fem.eq_a
    for iNode in range(fem.num_nodes):
        index0 = fem.start_index[iNode]
        for jNode, jnodeID in enumerate(fem.nodeID[iNode]):
            a00 = A[index0 + jNode*4 + 0]
            a01 = A[index0 + jNode*4 + 1]
            a10 = A[index0 + jNode*4 + 2]
            a11 = A[index0 + jNode*4 + 3]
            test[iNode*2+0, jnodeID*2+0] = a00
            test[iNode*2+1, jnodeID*2+0] = a01
            test[iNode*2+0, jnodeID*2+1] = a10
            test[iNode*2+1, jnodeID*2+1] = a11
            test[jnodeID*2+0, iNode*2+0] = a00
            test[jnodeID*2+1, iNode*2+0] = a10
            test[jnodeID*2+0, iNode*2+1] = a01
            test[jnodeID*2+1, iNode*2+1] = a11

    plt.imshow(test, cmap=plt.cm.jet)
    plt.show()
    exit()

#-----------------------------------------------------------------------------#
def use_femsolver(fem, nodes, elems, global_force):
    #>> solver用gloval_forceの変換
    gf = global_force2solver(fem, global_force)

    get_solver_index(fem, elems)

    fem.nodeID = fem.related_nodes


    shape_kmat_e = (fem.dof_elems, fem.dof_elems)
    ke = np.zeros(shape_kmat_e, dtype=float) # Element stiffness mat

    #>> indexの取得
    dims = fem.dof_nodes
    fem.start_index = np.zeros(fem.num_nodes, dtype=int)
    for i in range(1, fem.num_nodes):
        fem.start_index[i] = fem.start_index[i - 1]\
                           + dims*dims*len(fem.related_nodes[i - 1])

    num_eq = dims*dims*(sum([len(x) for x in fem.related_nodes]))
    fem.eq_a = np.zeros(num_eq, dtype=float)
    fem.eq_x = np.zeros(dims*fem.num_nodes, dtype=float)
    fem.eq_bc = fem.bc.ravel().astype(float)
    ### index end ###
    shape_func = shape_function(fem.elem_type)

    #>> Stiffness matrix
    #>> 右辺ベクトルの初期化(問題なし)
    fem.eq_b = gf.ravel()
    for iElement in range(fem.num_elems):
        coord, element = get_elem(fem, iElement, nodes, elems)
        element = elems[iElement]
        #>> Element stiffness matrix
        #   要素剛性行列の作成
        make_element_stiffness_matrix(fem, coord, ke, shape_func)
        force_symmetric(ke)

        A = fem.eq_a

        for iNode, inodeID in enumerate(element):
            start_index = fem.start_index[inodeID]
            for jNode, jnodeID in enumerate(element):
                if jnodeID in fem.nodeID[inodeID]:
                    idx_k = np.where(fem.nodeID[inodeID]==jnodeID)[0][0]
                    #A[start_index + 4*idx_k + 0] += ke[2*iNode + 0][2*jNode + 0]
                    #A[start_index + 4*idx_k + 1] += ke[2*iNode + 0][2*jNode + 1]
                    #A[start_index + 4*idx_k + 2] += ke[2*iNode + 1][2*jNode + 0]
                    #A[start_index + 4*idx_k + 3] += ke[2*iNode + 1][2*jNode + 1]
                    #print(ke[2*iNode + 0][2*jNode + 0])
                    #print(ke[2*iNode + 0][2*jNode + 1])
                    #print(ke[2*iNode + 1][2*jNode + 0])
                    #print(ke[2*iNode + 1][2*jNode + 1])
                    #print(ke[2*iNode:2*iNode+2, 2*jNode:2*jNode+2].ravel())
                    idx = start_index + 4*idx_k
                    #print(A[idx:idx+4])
                    values = ke[2*iNode:2*iNode+2, 2*jNode:2*jNode+2].ravel()
                    A[idx:idx+4] += values


    #>> 初期値（変位境界条件の値を与える）(問題なし)
    for iNode in range(fem.num_nodes):
        for iDim in range(2):
            fem.eq_x[2*iNode + iDim] = 0.0

    set_direchlet_bc(fem)

    #>> check diagonal (対角項の整理)
    for iNode in range(fem.num_nodes):
        index0 = fem.start_index[iNode]
        if np.abs(fem.eq_a[index0 + 0]) < 1.0e-12:
            fem.eq_a[index0 + 0] = 1.0
        if np.abs(fem.eq_a[index0 + 3]) < 1.0e-12:
            fem.eq_a[index0 + 3] = 1.0


    #plot_fem2d_kglobal(fem, A)

    eq_x = np.array([fem.eq_x]).T
    eq_b = np.array([fem.eq_b]).T
    #print(eq_b)
    #exit()
    #xx1 = conjugate_gradients(test, eq_x, eq_b)
    #print(xx1.T[0])
    #exit()
    #test

    #'''
    #ssor_index_plot(fem)
    #exit()
    time_st = time.time()
    xx1 = fem_solver_ssor_type_c(fem)
    print('solver  time : ', time.time() - time_st)
    #time_st = time.time()
    #xx1 = ssor(fem)
    #print('ssor    time : ', time.time() - time_st)
    #print(xx1)
    #time_st = time.time()
    #xx1 = ssor_py(fem)
    #print(xx1)
    #print('ssor_py time : ', time.time() - time_st)
    #exit()
    #'''
    #print('xx1\n', xx1)
    #print('dddisp\n', fem.dddisp)
    #print('error', np.linalg.norm(xx1 - fem.dddisp))
    #exit()

    '''
    xx = np.zeros_like(fem.eq_x)
    b = fem.eq_b
    xx = xx.reshape(-1,1)
    b = b.reshape(-1,1)
    xx2 = symmetric_sor(test, xx, b)
    '''
    '''
    A = np.array([[4,  3,  2],\
                  [3, -1,  2],\
                  [2,  2,  6]])

    b = np.array([[4, 2, 3]]).T
    AA = np.eye(5)
    AA[1:4, 1:4] = A
    bb = np.zeros((5, 1))
    bb[1:4] = b
    '''
    '''
    A = np.array([\
        [ 7.0, -1.0,  0.0,  0.0, 0.0],\
        [-1.0,  9.0, -2.0,  1.0, 0.0],\
        [ 0.0, -2.0,  8.0, -3.0, 0.0],\
        [ 0.0,  1.0, -3.0, 10.0, 2.0],\
        [ 0.0,   0.0,  0.0,  2.0, 3.0]], dtype=float)
    b = np.array([[-5, 15, -10, 20, 2]], dtype=float).T
    xx = np.zeros_like(b)
    xx2 = symmetric_sor(A, xx, b)


    print(xx2)
    #print('error', np.linalg.norm(xx1 - xx2))
    exit()
    #'''
    '''
    xx3 = np.linalg.solve(test, b)


    print('xx1\n', xx1)
    xx2 = xx2.ravel()
    xx3 = xx3.ravel()
    print('xx2\n', xx2)
    print('xx3\n', xx3)
    print('xx2-xx1',np.linalg.norm(xx2-xx1))
    print('xx2-xx3',np.linalg.norm(xx2-xx3))
    exit()
    '''


    return xx1.reshape(fem.num_nodes, fem.dof_nodes)

#-----------------------------------------------------------------------------#
