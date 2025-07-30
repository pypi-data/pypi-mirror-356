#coding:UTF-8

"""
# Name    : _wireframe.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Jan. 27 2025
# Date    : Mar. 20 2023
# Note    : Two dimensional fem result plot program
"""

import numpy as np
import matplotlib.pyplot as plt

#-----------------------------------------------------------------------------#
def wireframe(nodes, elems, showornot=False, saveornot=False):
    """
    This function plots wire frame of finite element.

    Parameters
    ----------
    nodes : ndarray, 2-D
        node data
    elems : ndarray, 2-D
        element data
    showornot : bool
        [False] (default) : not plt.show()
        [True] : plt.show()
    saveornot : bool
        [False] (default) : not save figure
        [True] : save figure
    """

    if elems.shape[1] == 6:     # T6 mesh
        elems = elems[:, :3]
    elif elems.shape[1] == 8:   # Q8 mesh
        elems = elems[:, :4]
    connectivity = np.arange(elems.shape[1] + 1)
    connectivity[-1] = 0
    for i in range(elems.shape[0]):
        plt.plot(nodes[elems[i, connectivity], 0],\
                 nodes[elems[i, connectivity], 1], 'k-', lw=0.5)

    message = 'Wire frame figure was saved.'
    figname = 'wireframe.png'
    show_save(showornot, saveornot, message, figname)

#-----------------------------------------------------------------------------#
def mesh(nodes, elems, showornot=False, saveornot=False):
    """
    This function plots polygon mesh.
    """
    plt.plot(0,0,'r.', alpha=0.0)
    if elems.shape[1] == 6:     # T6 mesh
        elems = elems[:, :3]
    elif elems.shape[1] == 8:   # Q8 mesh
        elems = elems[:, :4]
    for elem in elems:
        poly = plt.Polygon(nodes[elem], fc='c', ec='k', lw=0.5)
        plt.gca().add_patch(poly)

    message = 'Mesh figure was saved.'
    figname = 'mesh_fig.png'
    show_save(showornot, saveornot, message, figname)

#-----------------------------------------------------------------------------#
def show_save(showornot, saveornot, message, figname):
    plt.subplot().set_aspect('equal')
    if saveornot == True:
        plt.savefig(figname)
        print('%s [%s]' % (message, figname))
        plt.close()
    if showornot == True:
        plt.show()
        plt.close()

#-----------------------------------------------------------------------------#










