#coding:UTF-8

"""
# Name    : _plottools.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Two dimensional fem result plot program
"""

import numpy as np
import matplotlib.pyplot as plt

#-----------------------------------------------------------------------------#
def get_reshapesize(mesh_info):
    """
    This function return reshape array size for contour plot

    Parameters
    ----------
    mesh_info : dict.
        mesh information dictionary

    Returns
    -------
    rs_size : list
        reshape size
    """
    elem_type = mesh_info['elem_type']
    if elem_type == 'T3' or elem_type == 'Q4' or elem_type == 'Q8':
        rs_size = [mesh_info['ey'] + 1, mesh_info['ex'] + 1]
    elif elem_type == 'T6':
        rs_size = [mesh_info['ey']*2 + 1, mesh_info['ex']*2 + 1]
    return rs_size

#-----------------------------------------------------------------------------#
def plot_wireframe(nodes, elems, showornot=False, saveornot=False):
    """
    This function plot wire frame of finite element.

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
    if saveornot == True:
        plt.subplot().set_aspect('equal')
        figname = 'wireframe.png'
        plt.savefig(figname)
        print('Wire frame figure was saved. [%s]' % figname)
        plt.close()
    if showornot == True:
        plt.subplot().set_aspect('equal')
        plt.show()
        plt.close()

#-----------------------------------------------------------------------------#
def plot_patches(nodes, elems, value, div, component, option):
    """
    Two-dimensional patch plot for triangular element (T3)

    Parameters
    ----------
    nodes : ndarray, 2-D
        node data
    elems : ndarray, 2-D
        element data
    value : ndarray, 1-D
        value array for plot
    div : int
        divided number of colorbar
    component : str
        component name
    showornot : bool
        True(default) : not plt.show() and save figure
        Flase : only plt.show()
    """

    vertices = []
    values = []
    for node in elems:
        vertices.append(tuple([tuple(nodes[n]) for n in node]))
    import matplotlib as mpl
    collection = mpl.collections.PolyCollection(\
                 vertices, edgecolors='face',\
                 linewidth=1.0, antialiased=1)
    cmap = plt.cm.jet
    bounds = np.linspace(np.min(value), np.max(value), div+1)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    collection.set_array(value)
    collection.set_cmap(cmap)
    ax = plt.figure().gca()
    ax.add_collection(collection)
    ax.set_aspect('equal')
    plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
    plt.xlabel('$x$ [mm]')
    plt.ylabel('$y$ [mm]')
    if option['with_wireframe']:
        disp = option['displacement']
        magnitude = option['magnitude']
        plot_wireframe(nodes, elems, False)
        plot_wireframe(nodes + disp*magnitude, elems, False)
    else:
        ax.set_xlim(np.min(nodes[:,0]), np.max(nodes[:,0]))
        ax.set_ylim(np.min(nodes[:,1]), np.max(nodes[:,1]))

    if option['saveornot'] == True:
        figname = 'T3_patch_' + component + '.png'
        plt.savefig(figname)
    else:
        plt.show()
    plt.close()


#-----------------------------------------------------------------------------#
#def plot_nodalvalue(nodes, elems, mesh_info, value1, value2, component, option):
def plot_nodalvalue(nodes, elems, mesh_info, value, component, option):
    """
    This function make nodal value contour graph.

    Parameters
    ----------
    nodes : ndarray, 2-D
        node data
    elems : ndarray, 2-D
        element data
    mesh_info : dict.
        mesh information dictionary
    value : ndarray, 2-D
        contour data
    component : str
        data component
    option : dict.
        plot option dictionay
    """

    #>> Get reshape size
    rs_size = get_reshapesize(mesh_info)

    magnitude = option['magnitude']
    if magnitude is None: magnitude = 1.0
    disp = option['displacement']
    if disp is None: disp = np.zeros_like(nodes)

    #>> Plot wireframe option
    if option['with_wireframe']:
        if mesh_info['elem_type'] == 'Q8':
            elems = elems[:, :4]
        elif mesh_info['elem_type'] == 'T6':
            elems = elems[:, :3]

        #plot_wireframe(nodes, elems, False)
        plot_wireframe(nodes + disp*magnitude, elems, False)

    #>> Reshaped contour data
    X = (nodes[:,0] + disp[:,0]*magnitude).reshape(rs_size)
    Y = (nodes[:,1] + disp[:,1]*magnitude).reshape(rs_size)
    #V1 = value1.reshape(rs_size)
    #V2 = value2.reshape(rs_size)
    V = value.reshape(rs_size)

    #>> Plot contour
    #plt.contourf(X+V1*500, Y+V2*500, V1, 15, cmap=plt.cm.jet)
    #plt.contourf(X+V1, Y+V2, V1, 15, cmap=plt.cm.jet)
    plt.contourf(X, Y, V, 15, cmap=plt.cm.jet)
    plt.subplot().set_aspect('equal')
    plt.xlabel('$x$ [mm]')
    plt.ylabel('$y$ [mm]')
    plt.grid()
    plt.colorbar()

    #>> Save option
    if option['saveornot'] == True:
        figname = mesh_info['elem_type'] + '_' + component + '.png'
        plt.savefig(figname)
    else:
        plt.show()
    plt.close()

#-----------------------------------------------------------------------------#
def plot_nodalvalue_multi(nodes_list, elems_list, mesh_infos,\
                          value_list, column_index, component, option):

    plt.subplot().set_aspect('equal')
    #>> Plot wireframe optoin
    if option['with_wireframe']:
        disp_list = option['displacement']
        magnitude = option['magnitude']
        for i in range(len(mesh_infos)):
            if mesh_infos[i]['elem_type'] == 'Q8':
                elems_list[i] = elems_list[i][:, :4]
            elif mesh_infos[i]['elem_type'] == 'T6':
                elems_list[i] = elems_list[i][:, :3]
            plot_wireframe(nodes_list[i], elems_list[i], False)
            plot_wireframe(nodes_list[i] + disp_list[i]*magnitude,\
                           elems_list[i], False)

    #>> Get all value and set contour level
    for i in range(len(mesh_infos)):
        if i == 0:
            v_all = value_list[i][:, column_index]
        else:
            v_all = np.hstack((v_all, value_list[i][:, column_index]))
    v_min = np.min(v_all)
    v_max = np.max(v_all)
    levs = np.linspace(v_min, v_max, 15)

    #>> Multiple cotour plot
    for i in range(len(mesh_infos)):
        rs_size = get_reshapesize(mesh_infos[i])
        X = nodes_list[i][:, 0].reshape(rs_size)
        Y = nodes_list[i][:, 1].reshape(rs_size)
        V = value_list[i][:, column_index].reshape(rs_size)
        cont = plt.contourf(X, Y, V, levs, cmap=plt.cm.jet)
    cbar = plt.colorbar(cont)
    plt.xlabel('$x$ [mm]')
    plt.ylabel('$y$ [mm]')
    plt.grid()

    if option['saveornot'] == True:
        figname = mesh_infos[0]['elem_type'] + '_' + component + '.png'
        plt.savefig(figname)
    else:
        plt.show()
    plt.close()

#-----------------------------------------------------------------------------#
