#coding:UTF-8

"""
# Name    : _gen_geommesh.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Two-dimensional geometry mesh generation program
"""

import numpy as np
import copy

#-----------------------------------------------------------------------------#
def gen_geommesh(geometry, ex, ey, shift_x=0.0, shift_y=0.0):
    """
    This function generate mesh using geometry data. Output mesh type is "Q4".

    Parameters
    ----------
    geometry : dict
        Geometry data.
    ex : int
        Number of element (x-direction).
    ey : int
        Number of element (y-direction).
    shiftx : float
        shift x direction.
    shifty : float
        shift y direction.

    Returns
    -------
    nodes : ndarray, 2-D
        Node data.
    elems : ndarray, 2-D
        Element data.
    """
    #>> Make mapping target nodes
    nx = ex + 1; ny = ey + 1
    edge_u = np.linspace(0.0, geometry['length_rect'], nx)
    edge_v = np.linspace(0.0, geometry['length_rect'], ny)

    #print('edge_u\n', edge_u)

    #>> 円孔メッシュ不等分割(疎密ありメッシュ)
    #   ガウス分布による疎密(重み付きlinspace)
    x_min = 1.0
    x_max = 2.0 # 2.5 - 4.15 (default 3.0)
    mu = 0.0
    scale = 0.87 # 0.87 - 1.86 (default 1.0)
    num_pts = ny
    edge_v1 = gauss_weighted_linspace(x_min, x_max, mu, scale, num_pts)
    #edge_v = edge_v1

    node_u, node_v = np.meshgrid(edge_u, edge_v)
    node_u = node_u.flatten()
    node_v = node_v.flatten()

    mapTarget = np.array([node_u, node_v]).T
    mapTarget = tuple(map(tuple, mapTarget))

    #>> Node mapping by NURBS
    from geomdl import NURBS
    surf = NURBS.Surface()
    surf.degree_u = geometry['degrees_u']
    surf.degree_v = geometry['degrees_v']
    surf.ctrlpts_size_u = geometry['ctrlpts_u']
    surf.ctrlpts_size_v = geometry['ctrlpts_v']

    num_ctrlpts = np.shape(geometry['ctrlpts'])[0]
    ctrlPts = np.zeros_like(geometry['ctrlpts'])
    for i in range(ctrlPts.shape[0]):
        for j in range(ctrlPts.shape[1]):
            ctrlPts[i,j] = geometry['ctrlpts'][i][j]/geometry['weights'][i]
    surf.ctrlpts = ctrlPts.tolist()
    surf.weights = geometry['weights']
    surf.knotvector_u = geometry['knotvec_u']
    surf.knotvector_v = geometry['knotvec_v']

    mappedNodes = np.array(surf.evaluate_list(mapTarget))
    nodes = mappedNodes[:,:2]

    #>> Meke element
    elems = np.zeros((ex*ey, 4), dtype=int)
    k = 0
    for j in range(ny):
        for i in range(nx):
            n = i + nx*j
            if i < (nx-1) and j < (ny-1):
                elems[k,0] = n
                elems[k,1] = n + nx
                elems[k,2] = n + nx + 1
                elems[k,3] = n + 1
                k += 1
    #>> Shift nodes
    nodes[:, 0] += shift_x
    nodes[:, 1] += shift_y
    return nodes, elems

#-----------------------------------------------------------------------------#
def gauss_weighted_linspace(x_min, x_max, mu, scale, num_pts):
    import matplotlib.pyplot as plt
    sigma = scale
    x = np.linspace( 0, x_max, num_pts)
    fx = prob_dist(x, mu, sigma)
    xx = (x - mu) / (np.sqrt(2.0)*sigma)
    cdf = 0.5*(1.0 + error_func(xx))
    bounds = np.array([cdf[0], cdf[-1]])
    pp1 = np.linspace(*bounds, num=num_pts)
    err2 = error_func_i((2.0*pp1 - 1.0))
    ppf = mu + sigma*np.sqrt(2)*err2

    c = 1.0 / x_max
    ppf = ppf*c

    #print(ppf)

    #dist = sum_gaussian_gen()
    #bounds = dist.cdf([0, 3])
    #pp = np.linspace(*bounds, num=21)
    #vals = dist.ppf(pp)
    #print('vals', vals)
    #print('ppf', ppf)
    #plt.plot(vals, [0.5]*vals.size, 'o')
    #plt.plot(ppf, [0.51]*ppf.size, 's')
    #xs = np.linspace(0,3,500)
    #plt.plot(xs, dist.pdf(xs), 'r-', lw=2)
    #plt.plot(x, fx, 'b--', lw=2)
    #plt.show()
    #exit()
    return ppf

#-----------------------------------------------------------------------------#
from scipy import stats
class sum_gaussian_gen(stats.rv_continuous):
    def _pdf(self, x):
        return (stats.norm.pdf(x, loc=0, scale=3))

#-----------------------------------------------------------------------------#
def prob_dist(x, mu, sigma):
    ca = 1.0 / np.sqrt(2.0*np.pi*sigma**2)
    fx = ca*np.exp(-(x - mu)**2 / (2.0*sigma**2))
    return fx

#-----------------------------------------------------------------------------#
def error_func(x):
    """
    Error function
    """
    pi = np.pi
    a = -(8.0*(pi - 3.0)) / (3.0*pi*(pi - 4.0))
    erf2 = 1.0 - np.exp(-x**2 * (4.0/pi + a*x**2) / (1.0 + a*x**2))
    erf = np.sqrt(erf2)
    idx = np.where(x < 0.0)[0]
    erf[idx] *= -1.0
    return erf


#-----------------------------------------------------------------------------#
def error_func_i(x):
    """
    Inverse of error function
    """
    pi = np.pi
    a = -(8.0*(pi - 3.0)) / (3.0*pi*(pi - 4.0))
    A = ((2.0 / (pi*a)) + (np.log(1.0 - x**2) / 2.0))**2
    B = np.log(1.0 - x**2) / a
    C = (2.0 / (pi*a)) + (np.log(1.0 - x**2) / 2.0)
    ierf = np.sqrt(np.sqrt(A - B) - C)
    idx = np.where(x < 0.0)[0]
    ierf[idx] *= -1.0
    return ierf

#-----------------------------------------------------------------------------#
