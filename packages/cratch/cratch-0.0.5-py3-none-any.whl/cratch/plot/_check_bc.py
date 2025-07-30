#coding:UTF-8

import numpy as np
import matplotlib.pyplot as plt

from ._wireframe import mesh

#-----------------------------------------------------------------------------#
def check_bc(nodes, elems, force, fix, rx=False, ry=False,\
             xlabel='', ylabel='', showornot=True, saveornot=False):
    """
    This function shows boundary conditions.

    Parameters
    ----------
    nodes : ndarray, 2-D
        Node data.
    elems : ndarray, 2-D
        Element data.
    force : ndarray, 2-D
        Force data. (Equivalent nodal force)
    fix : ndarray, 2-D
        Fix data.
    rx : bool (optional)
        [False] (default)
        [True] : reverse x-direction marker.
    ry : bool (optional)
        [False] (default)
        [True] : reverse y-direction marker.
    xlabel : str
        The label text for the x-axis.
    ylabel : str
        The label text for the y-axis.
    showornot : bool (optional)
        [False] : 
        [True] (default)
    saveornot : bool (optional)
        [False]
        [True] : 
    """

    plt.subplot().set_aspect('equal')
    #poly_mesh(nodes, elems)
    mesh(nodes, elems)
    check_bc_force(nodes, force)
    check_bc_fix(nodes, fix, rx=rx, ry=ry)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if saveornot:
        figname = 'boundary_condition.png'
        plt.savefig(figname)
        print('Boundary condition figure was saved. [%s]' % figname)
        plt.close()
        showornot=False
    if showornot:
        plt.show()
        plt.close()

#-----------------------------------------------------------------------------#
def check_bc_force(nodes, force):
    """
    This function plots force boundary condition.
    """

    idx = np.where(force != 0.0)[0]
    scale_y = (np.max(force[:,1]) - np.min(force[:,1]))\
            / (np.max(nodes[:,1]) - np.min(nodes[:,1])) * 10.0
    scale_x = (np.max(force[:,0]) - np.min(force[:,0]))\
            / (np.max(nodes[:,0]) - np.min(nodes[:,0])) * 10.0
    scale = np.sqrt(scale_x**2 + scale_y**2)
    ext_xm = np.min(force[:, 0])/scale * 1.5
    ext_xp = np.max(force[:, 0])/scale * 1.5
    ext_ym = np.min(force[:, 1])/scale * 1.5
    ext_yp = np.max(force[:, 1])/scale * 1.5
    xmin = np.min(nodes[:, 0])
    xmax = np.max(nodes[:, 0])
    ymin = np.min(nodes[:, 1])
    ymax = np.max(nodes[:, 1])

    plt.quiver(nodes[idx, 0], nodes[idx, 1],\
               force[idx, 0], force[idx, 1],\
               scale_units='xy', width=0.01,\
               scale=scale, color='r', alpha=0.8)
    plt.xlim(xmin+ext_xm-3, xmax+ext_xp+3)
    plt.ylim(ymin+ext_ym-3, ymax+ext_yp+3)

#-----------------------------------------------------------------------------#
def fix_trig_x(nodes, fix_idx, trih):
    """
    This function plots triangle marker on fixed nodes (x-direction).
    """

    triw = 1.0 *0.5
    for idx in fix_idx[0]:
        tri = np.array([\
        [nodes[idx,0], nodes[idx,1]],\
        [nodes[idx,0]-trih, nodes[idx,1]-triw],\
        [nodes[idx,0]-trih, nodes[idx,1]+triw] ])
        t1 = plt.Polygon(tri, fc='b', ec='b', alpha=0.5)
        plt.gca().add_patch(t1)

#-----------------------------------------------------------------------------#
def fix_trig_y(nodes, fix_idx, trih):
    """
    This function plots triangle marker on fixed nodes (y-direction).
    """

    triw = 1.0 *0.5
    for idx in fix_idx[0]:
        tri = np.array([\
        [nodes[idx,0], nodes[idx,1]],\
        [nodes[idx,0]-triw, nodes[idx,1]-trih],\
        [nodes[idx,0]+triw, nodes[idx,1]-trih] ])
        t1 = plt.Polygon(tri, fc='b', ec='b', alpha=0.5)
        plt.gca().add_patch(t1)

#-----------------------------------------------------------------------------#
def check_bc_fix(nodes, fix, rx=False, ry=False):
    """
    This function plots triangle marker on fixed nodes.
    """

    fix_idx = np.where(fix[:,0] == 0)
    fix_idy = np.where(fix[:,1] == 0)
    trih = np.sqrt(2) *0.5

    if rx == True:
        fix_trig_x(nodes, fix_idx, trih*(-1.0))
    else:
        fix_trig_x(nodes, fix_idx, trih)
    if ry == True:
        fix_trig_y(nodes, fix_idy, trih*(-1.0))
    else:
        fix_trig_y(nodes, fix_idy, trih)

#-----------------------------------------------------------------------------#
