#coding:UTF-8

"""
# Name    : _format_off.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 12 2024
# Note    : Export off data program
"""

import numpy as np

#-----------------------------------------------------------------------------#
def export_off(fname, nodes, elems):
    """
    This function export .off format file.

    Parameters
    ----------
    fname : str
        off file name
    nodes : ndarray, 2-D
        node data
    elems : ndarray, 2-D
        element data

    Notes
    -----
    off format file is easy mesh file. This format can use only
    'T3' or 'Q4' which is first order element. If you use high order
    mesh, vtu format use.
    """

    if elems.shape[1] != 3 and elems.shape[1] != 4:
        print('[export_off]')
        print('This element is not supported...')
        exit()

    outfile = open(fname, 'w')
    outfile.write('OFF\n')
    num_nodes = nodes.shape[0]
    num_elems = elems.shape[0]
    outfile.write('%d %d 0\n' % (num_nodes, num_elems))

    #>> Write node data
    if nodes.shape[1] == 2: # 2D
        for i in range(num_nodes):
            outfile.write('%18.16f %18.16f 0.0\n' %\
                (nodes[i][0], nodes[i][1]))

    elif nodes.shape[1] == 3:   # 3D
        for i in range(num_nodes):
            outfile.write('%18.16f %18.16f %18.16f\n' %\
                (nodes[i][0], nodes[i][1], nodes[i][2]))

    #>> Write element data
    if elems.shape[1] == 3: # Triangular element (T3)
        for i in range(num_elems):
            outfile.write('3 %d %d %d\n' %\
                (elems[i][0], elems[i][1], elems[i][2]))
    elif elems.shape[1] == 4: # Quadrangular element (Q4)
        for i in range(num_elems):
            outfile.write('4 %d %d %d %d\n' %\
                (elems[i][0], elems[i][1],\
                 elems[i][2], elems[i][3]))

    outfile.close()

#-----------------------------------------------------------------------------#
def import_off(fname):
    """
    This function import .off format file.

    Parameters
    ----------
    fname : str
        off file name
    """

    for i, line in enumerate(open(fname)):
        items = line.split()
        if i == 0:
            continue
        elif i == 1:
            num_nodes = int(items[0])
            num_elems = int(items[1])
            nodes = np.zeros((num_nodes, 3), dtype=float)
            print(num_nodes, num_elems)
        elif 1 < i <= (num_nodes + 1):
            idx = i - 2
            nodes[idx][0] = items[0]
            nodes[idx][1] = items[1]
            nodes[idx][2] = items[2]
        elif (num_nodes + 1) < i <= (num_nodes + num_elems + 1):
            idx = i - (num_nodes + 2)
            if i == (num_nodes + 2):
                num_nnelm = int(items[0])
                elems = np.zeros((num_elems, num_nnelm), dtype=int)
            for j in range(num_nnelm):
                elems[idx][j] = int(items[j+1])

    if np.all(nodes[:,-1] == 0.0):  # 2D file
        nodes = nodes[:,0:2]

    return nodes, elems

#-----------------------------------------------------------------------------#
