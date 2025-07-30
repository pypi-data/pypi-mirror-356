#coding:UTF-8

"""
# Name    : _format_vtk.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Feb. 03 2017
# Note    : VTK class defenition and export program for paraview
"""

import numpy as np
import codecs

#-----------------------------------------------------------------------------#
class VTK:
    """
    vtk data class
    """
    def __init__(self, fname, nodes=None, elems=None,\
                 disp=None, stress=None, strain=None):
        self.fname = fname
        if nodes is not None:
            self.nodes = nodes
        if elems is not None:
            self.elems = elems
        if disp is not None:
            self.disp = disp
        if stress is not None:
            self.stress = stress
        if strain is not None:
            self.strain = strain

#-----------------------------------------------------------------------------#
def export_vtk(fname, nodes=None, elems=None,\
               disp=None, stress=None, strain=None):
    """
    This function export .vtk format file.

    Parameters
    ----------
    fname : str
        vtk file name
    nodes : ndarray, 2-D
        node data
    elems : ndarray, 2-D
        element data
    disp : ndarray, 2-D, optional
        nodal displacement data
    stress : ndarray, 2-D, optional
        nodal stress data
    strain : ndarray, 2-D, optional
        nodal stress data
    """

    vtk = VTK(fname, nodes, elems, disp, stress, strain)

    variables = vars(vtk)
    if not 'nodes' in variables.keys():
        print('Please set nodes (ex. vtk.nodes = nodes)')
        exit()
    if not 'elems' in variables.keys():
        print('Please set elems (ex. vtk.elems = elems)')
        exit()

    vtk.num_nodes = vtk.nodes.shape[0]
    vtk.dof_nodes = vtk.nodes.shape[1]
    vtk.num_elems = vtk.elems.shape[0]
    vtk.num_nnelm = vtk.elems.shape[1]

    #>> Check element type
    check_element_type(vtk)

    #>> Generate unstrucured grid data
    generate_ugrid(vtk)

    # Assign nodes
    assign_nodes(vtk)

    # Assigh elems
    assign_elems(vtk)

    # Assign PointData
    if 'disp' in variables.keys():
        vtk.ugrid.append('POINT_DATA %d' % vtk.num_nodes)
        assign_displacement(vtk)

        if 'stress' in variables.keys():
            assign_stress(vtk)
        if 'stress' in variables.keys():
            assign_strain(vtk)

        #######################################
        # if you use cell data, use bellow
        #vtk.ugrid.append('CELL_DATA %d' % NumData )

    with codecs.open(vtk.fname, 'w', encoding='utf-8') as f:
        f.write('\n'.join(vtk.ugrid))

#-----------------------------------------------------------------------------#
def check_element_type(vtk):
    if vtk.dof_nodes == 2:          # 2-dimensional case
        if vtk.num_nnelm == 3:      # 1st order triangle
            vtk.etype = 5
        elif vtk.num_nnelm == 4:    # quadrilateral
            vtk.etype = 9
        elif vtk.num_nnelm == 6:    # Quadratic triangle
            vtk.etype = 22
        elif vtk.num_nnelm == 8:    # Quadratic quad
            vtk.etype = 23
        else:
            print('This element type is not yet implemented.')
            exit()
    elif vtk.dof_nodes == 3:        # 3-dimensional case
        if vtk.num_nnelm == 4:      # Tetra
            vtk.etype = 10
        elif vtk.num_nnelm == 8:    # Hexahedron
            vtk.etype = 12
        elif vtk.num_nnelm == 10:   # Quadratic tetra
            vtk.etype = 24
        elif vtk.num_nnelm == 20:   # Quadratic hexahedron
            vtk.etype = 25
        else:
            print('This element type is not yet implemented.')
            exit()
    elementDict = {
        'VERTEX'               :1,
        'PLOY_VERTEX'          :2,
        'LINE'                 :3,
        'PLOY_LINE'            :4,
        'TRIANGLE'             :5,
        'TRIANGLE_STRIP'       :6,
        'PLOYGON'              :7,
        'PIXEL'                :8,
        'QUAD'                 :9,
        'TETRA'                :10,
        'VOXEL'                :11,
        'HEXAHEDRON'           :12,
        'WEDGE'                :13,
        'PYRAMID'              :14,
        'QUADRATIC_EDGE'       :21,
        'QUADRATIC_TRIANGLE'   :22,
        'QUADRATIC_QUAD'       :23,
        'QUADRATIC_TETRA'      :24,
        'QUADRATIC_HEXAHEDRON' :25 }

#-----------------------------------------------------------------------------#
def generate_ugrid(vtk):
    vtk.ugrid = []
    vtk.ugrid.append('# vtk DataFile Version 2.0')
    vtk.ugrid.append('outdata')
    vtk.ugrid.append('ASCII')
    vtk.ugrid.append('DATASET UNSTRUCTURED_GRID')

#-----------------------------------------------------------------------------#
def assign_nodes(vtk):
    vtk.ugrid.append('POINTS %d float' % vtk.num_nodes)
    for i in range(vtk.num_nodes):
        coord = ''
        for j in range(vtk.dof_nodes):
            if j == (vtk.dof_nodes - 1):
                if vtk.dof_nodes == 2:
                    coord += '%18.16lf 0.0' % vtk.nodes[i][j]
                else:
                    coord += '%18.16lf' % vtk.nodes[i][j]
            else:
                coord += '%18.16lf ' % vtk.nodes[i][j]
        vtk.ugrid.append(coord)

#-----------------------------------------------------------------------------#
def assign_elems(vtk):
    vtk.ugrid.append('CELLS %d %d' % \
        (vtk.num_elems, vtk.num_elems*(vtk.num_nnelm + 1)))
    for i in range(vtk.num_elems):
        connect = '%d ' % vtk.num_nnelm
        for j in range(vtk.num_nnelm):
            if j == (vtk.num_nnelm - 1):
                connect += '%d' % vtk.elems[i][j]
            else:
                connect += '%d ' % vtk.elems[i][j]
        vtk.ugrid.append(connect)

    vtk.ugrid.append('CELL_TYPES %d' % vtk.num_elems)
    for i in range(vtk.num_elems):
        vtk.ugrid.append('%d' % vtk.etype)

#-----------------------------------------------------------------------------#
def assign_displacement(vtk):
    num_comps = vtk.disp.shape[1]

    if num_comps == 2:
        vtk.ugrid.append('SCALARS %s float %d' %\
            ('displacement', (num_comps+1)))
    elif num_comps == 3:
        vtk.ugrid.append('SCALARS %s float %d' %\
            ('displacement', num_comps))

    vtk.ugrid.append('LOOKUP_TABLE default')

    for i in range(vtk.num_nodes):
        line = ''
        for j in range(num_comps):
            if j == (num_comps - 1):
                if num_comps == 2:
                    line += '%e 0.0' % (vtk.disp[i][j])
                elif num_comps == 3:
                    line += '%e' % (vtk.disp[i][j])
            else:
                line += '%e ' % (vtk.disp[i][j])
        vtk.ugrid.append(line)

#-----------------------------------------------------------------------------#
def assign_stress(vtk):
    num_comps = vtk.stress.shape[1]

    if num_comps == 3:
        comps = ['xx_component', 'yy_component', 'xy_component']
    elif num_comps == 5:
        comps = ['xx_component', 'yy_component', 'xy_component',\
                    'max', 'min']
    elif num_comps == 6:
        comps = ['xx_component', 'yy_component', 'zz_component',\
                     'xy_component', 'xz_component', 'yz_component']
    elif num_comps == 9:
        comps = ['xx_component', 'yy_component', 'zz_component',\
                'xy_component', 'xz_component', 'yz_component',\
                'minor principal','intermediate principal'\
                'major principal']
    for i in range(num_comps):
        vtk.ugrid.append('SCALARS sig_%s float 1' % comps[i])
        vtk.ugrid.append('LOOKUP_TABLE default')
        for j in range(num_nodes):
            vtk.ugrid.append('%e' % vtk.stress[i][j])

#-----------------------------------------------------------------------------#
def assign_strain(vtk):
    num_comps = vtk.strain.shape[1]

    if num_comps == 3:
        comps = ['xx_component', 'yy_component', 'xy_component']
    elif num_comps == 5:
        comps = ['xx_component', 'yy_component', 'xy_component',\
                    'max', 'min']
    elif num_comps == 6:
        comps = ['xx_component', 'yy_component', 'zz_component',\
                'xy_component', 'xz_component', 'yz_component']
    elif num_comps == 9:
        comps = ['xx_component', 'yy_component', 'zz_component',\
                'xy_component', 'xz_component', 'yz_component',\
                'minor principal','intermediate principal'\
                'major principal']
    for i in range(num_comps):
        vtk.ugrid.append('SCALARS eps_%s float 1' % comps[i])
        vtk.ugrid.append('LOOKUP_TABLE default')
        for j in range(num_nodes):
            vtk.ugrid.append('%e' % vtk.strain[i][j])

#-----------------------------------------------------------------------------#
