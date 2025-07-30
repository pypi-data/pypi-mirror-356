#coding:UTF-8

import numpy as np

#from cratch.utils._quadtools import quadrature
#from cratch.utils._shapefunctions import shape_function

#-----------------------------------------------------------------------------#
def import_fast(fname):
    """
    This function returns node and element data
    from ``FAST`` mesh.

    Parameter
    ---------
    fname : str
        File name of ``FAST`` mesh.

    Returns
    -------
    nodes : ndarray, 2D
        Node data.
    elems : ndarray, 2D
        Element data.
    bcext : class
        Boundary conditions and extra data class for ``FAST`` mesh.
        This class contains
        ``bc_dist_load`` (Distributed load B.C.),
        ``bc_con_force`` (Concentrated force B.C.),
        ``bc_disp`` (Displacement B.C.),
        ``extra`` (Extra data),
        ``E`` (Young's modulus [MPa]),
        ``nu`` (Poisson's ratio).
    """

    with open(fname, 'r') as file:
        contents = [s.rstrip() for s in file.readlines()]

    for i, data in enumerate(contents):
        data = data.split(' ')
        #>> Read mesh information
        if i == 0:
            num_nodes, num_elems, num_nline = read_meshinfo(data)
        #>> Get nodes and elems array
        elif i == 1:
            nodes, elems = get_arrays(data, num_nodes, num_elems)
        #>> Get element data
        elif 1 < i <= num_elems:
            elems[i-1] = np.array(data).astype(int)
        else:
            break

    elems -= 1 # Element index -1

    #>> Get nodes data
    start_idx = num_elems + 1
    if elems.shape[1] == 8: # 2d fast mesh
        read_node2d(nodes, contents, start_idx, num_nline)
    elif elems.shape[1] == 20: # 3d fast mesh
        read_node3d(nodes, contents, start_idx, num_nline)
        lst = [0,1,13,12,3,2,14,15,4,9,16,8,6,10,18,11,7,5,17,19]
        elems = elems[:, lst]

    #>> Rearrange contents (exclude node and element data)
    if elems.shape[1] == 8: # 2d fast mesh
        start_index = num_elems + 1 + num_nline*2
    elif elems.shape[1] == 20: # 3d fast mesh
        start_index = num_elems + 1 + num_nline*3
    contents = contents[start_index:]

    #>> Read boundary condition and extra data
    bce = read_bc_extra(contents)

    return nodes, elems, bce

#-----------------------------------------------------------------------------#
def read_meshinfo(data):
    """
    This function returns number of elements, nodes
    and node lines.

    Parameter
    ---------
    data : list
        The first line data of FAST mesh.

    Returns
    -------
    num_nodes : int
        The number of nodes.
    num_elems : int
        The number of elements.
    num_nline : int
        The number of node lines.
    """

    #>> get number of elements and nodes
    if len(data) == 5: # 2d fast mesh
        num_elems = int(data[1])
        num_nodes = int(data[2])
    elif len(data) == 4: # 3d fast mesh
        num_elems = int(data[0])
        num_nodes = int(data[1])

    #>> get number of node lines
    if num_nodes %5 == 0:
        num_nline = int(num_nodes / 5)
    else:
        num_nline = int(num_nodes / 5) + 1

    return num_nodes, num_elems, num_nline

#-----------------------------------------------------------------------------#
def get_arrays(data, num_nodes, num_elems):
    """
    This function retuns node and element array.

    Parameters
    ----------
    data : list
        The second line data of FAST mesh.
    num_nodes : int
        The number of nodes.
    num_elems : int
        The number of elements.

    Returns
    -------
    nodes : ndarray, 2D
        Nodes data.
    elems : ndarray, 2D
        Element data.
    """
    if len(data) == 8: # 2d fast mesh
        nodes = np.zeros((num_nodes, 2), dtype=float)
        elems = np.zeros((num_elems, 8), dtype=int)
    elif len(data) == 20: # 3d fast mesh
        nodes = np.zeros((num_nodes, 3), dtype=float)
        elems = np.zeros((num_elems,20), dtype=int)
    else:
        print('Is this FAST mesh?')
        exit()
    elems[0] = np.array(data).astype(int)

    return nodes, elems

#-----------------------------------------------------------------------------#
def read_node2d(nodes, contents, start_idx, num_nline):
    """
    This function returns node data from ``FAST`` mesh. (2d)

    Parameters
    ----------
    nodes : ndarray, 2D
        Nodes data.
    contents : list
        ``FAST`` data contents.
    start_idx : int
        Start index of file read.
    num_nline : int
        The number of read lines.

    Return
    ------
    nodes : ndarray, 2D
        Nodes data.
    """

    node_idx = 0
    for i in range(num_nline):
        coord_x = contents[i + start_idx]
        coord_y = contents[i + start_idx + num_nline]

        coord_x = np.array(coord_x.split(' ')).astype(float)
        coord_y = np.array(coord_y.split(' ')).astype(float)

        for j in range(coord_x.shape[0]):
            nodes[node_idx, 0] = coord_x[j]
            nodes[node_idx, 1] = coord_y[j]
            node_idx += 1
    return nodes

#-----------------------------------------------------------------------------#
def read_node3d(nodes, contents, start_idx, num_nline):
    """
    This function returns node data from ``FAST`` mesh. (3d)

    Parameters
    ----------
    nodes : ndarray, 2D
        Nodes data.
    contents : list
        ``FAST`` data contents.
    start_idx : int
        Start index of file read.
    num_nline : int
        The number of read lines.

    Return
    ------
    nodes : ndarray, 2D
        Nodes data.
    """

    node_idx = 0
    for i in range(num_line):
        coord_x = contents[i + start_idx]
        coord_y = contents[i + start_idx + num_line]
        coord_z = contents[i + start_idx + num_line*2]

        coord_x = np.array(coord_x.split(' ')).astype(float)
        coord_y = np.array(coord_y.split(' ')).astype(float)
        coord_z = np.array(coord_z.split(' ')).astype(float)

        for j in range(coord_x.shape[0]):
            nodes[node_idx, 0] = coord_x[j]
            nodes[node_idx, 1] = coord_y[j]
            nodes[node_idx, 2] = coord_z[j]
            node_idx += 1
    return nodes

#-----------------------------------------------------------------------------#
def read_bc_extra(contents):
    """
    This function returns boundary condition and
    extra data (include material constrints).

    Parameter
    ---------
    contents : list
        ``FAST`` data without node and element data.

    Returns
    -------
    bcext : class
        Boundary conditions and extra data class for ``FAST`` mesh.
        This class contains
        ``bc_dist_load`` (Distributed load B.C.),
        ``bc_con_force`` (Concentrated force B.C.),
        ``bc_disp`` (Displacement B.C.),
        ``extra`` (Extra data),
        ``E`` (Young's modulus [MPa]),
        ``nu`` (Poisson's ratio).
    """

    bce = BCE()

    num_separator = 0 # Number of separator
    for i, data in enumerate(contents):
        data = data.split(' ')
        #print(data)
        if data[0] == '-1':
            num_separator += 1
        elif num_separator == 0:
            bce.bc_dist_load.append(data)
        elif num_separator == 1:
            bce.bc_con_force.append(data)
        elif num_separator == 2:
            bce.bc_disp.append(data)
        elif num_separator == 3:
            bce.E = float(data[0])
            bce.nu = float(data[1])
        else:
            bce.extra.append(data)

    return bce

#-----------------------------------------------------------------------------#
class BCE():
    """
    Boundary conditions and extra data class for ``FAST`` mesh.
    """
    def __init__(self):
        self.bc_dist_load = []  # Distributed load B.C.
        self.bc_con_force = []  # Concentrated force B.C.
        self.bc_disp = []       # Displacement B.C.
        self.extra = []         # Extra data
        self.E = 0.0            # Young's modulus [MPa]
        self.nu = 0.0           # Poisson's ratio

    def show(self):
        """
        This function shows the contents of
        boundary conditions and extra data class.
        """
        cfmt = '\033[1;36m{}\033[0m'
        print('Contains:')
        print(cfmt.format('  `bc_dist_load`'), end='')
        if self.bc_dist_load:
            print(cfmt.format(': Distributed load B.C.'))
        else:
            print(': Distributed load B.C.')
        print(cfmt.format('  `bc_con_force`'), end='')
        if self.bc_con_force:
            print(cfmt.format(': Concentrated force B.C.'))
        else:
            print(': Concentrated force B.C.')
        print(cfmt.format('  `bc_disp`'), end='')
        if self.bc_disp:
            print(cfmt.format('     : Displacement B.C.'))
        else:
            print('     : Displacement B.C.')
        print(cfmt.format('  `extra`'), end='')
        if self.extra:
            print(cfmt.format('       : Extra data'))
        else:
            print('       : Extra data')
        print(cfmt.format('  `E`'), end='')
        if self.E != 0.0:
            print(cfmt.format('           : Young\'s modulus [MPa]'))
        else:
            print('           : Young\'s modulus [MPa]')
        print(cfmt.format('  `nu`'), end='')
        if self.nu != 0.0:
            print(cfmt.format('          : Poisson\'s ratio'))
        else:
            print('          : Poisson\'s ratio')

    def show_all(self):
        """
        This function shows the all contents of
        boundary conditions and extra data class.
        """
        self.show()
        cfmt = '\033[1;36m{}\033[0m:'
        print('')
        print('Contains all:')
        for key, val in vars(self).items():
            print(cfmt.format(key), val)

#-----------------------------------------------------------------------------#
#def export_fast(filename, nodes, elems, disp, force, 





