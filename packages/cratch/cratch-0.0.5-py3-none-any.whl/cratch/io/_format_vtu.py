#coding:UTF-8

"""
# Name    : _format_vtu.py
# Autohr  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : VTU class defenition and export program for paraview
"""

import numpy as np
import codecs

#-----------------------------------------------------------------------------#
def export_pvd(fname, vtulist):
    """
    Make pvd file for continuous vtu file

    Parameters
    ----------
    fname : str
        pvd file name
    vtulist : list
        vtu file name list
    """

    pvd = []
    pvd_line = '<VTKFile byte_order="LittleEndian" '
    pvd_line += 'type="Collection" version="0.1">'
    pvd.append(pvd_line)
    pvd.append('<Collection>')
    for i, fname in enumerate(vtulist):
        pvd.append('<DataSet file="%s" groups="" part="0" timestep="%d"/>'\
                   % (fname, i))
    pvd.append('</Collection>')
    pvd.append('</VTKFile>')

    with codecs.open(fname, 'w', encoding='utf-8') as f:
        f.write('\n'.join(pvd))

#-----------------------------------------------------------------------------#
class VTU:
    """
    vtu file class
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
def export_vtu(fname, nodes=None, elems=None,\
               disp=None, stress=None, strain=None):
    """
    This function export .vtu format file.

    Parameters
    ----------
    fname : str
        vtu file name
    nodes : ndarray, 2-D
        nodes data
    elems : ndarray, 2-D
        element data
    disp : ndarray, 2-D, optional
        nodal displacement data
    stress : ndarray, 2-D, optional
        nodal stress data
    strain : ndarray, 2-D, optional
        nodal strain data
    """

    vtu = VTU(fname, nodes, elems, disp, stress, strain)

    variables = vars(vtu)
    if not 'nodes' in variables.keys():
        print('Please set nodes (ex. vtu.nodes = nodes)')
        exit()
    if not 'elems' in variables.keys():
        print('Please set elems (ex. vtu.elems = elems)')
        exit()

    vtu.num_nodes = vtu.nodes.shape[0]
    vtu.dof_nodes = vtu.nodes.shape[1]
    vtu.num_elems = vtu.elems.shape[0]
    vtu.num_nnelm = vtu.elems.shape[1]

    #>> Check element type
    check_element_type(vtu)

    #>> Generate unstructured grid data
    generate_ugrid(vtu)

    #>> Assign nodes
    assign_nodes(vtu)

    #>> Assign element
    assign_elems(vtu)

    #>> Assign PointData
    if 'disp' in variables.keys():
        vtu.ugrid.append('<PointData>')
        assign_displacement(vtu)

        if 'stress' in variables.keys():
            assign_stress(vtu)

        if 'strain' in variables.keys():
            assign_strain(vtu)

        vtu.ugrid.append('</PointData>')

    #>> Finalize unstructured grid data
    finalize_ugrid(vtu)

    with codecs.open(vtu.fname, 'w', encoding='utf-8') as f:
        f.write('\n'.join(vtu.ugrid))

#-----------------------------------------------------------------------------#
def check_element_type(vtu):
    if vtu.dof_nodes == 2:          # 2-dimensional case
        if vtu.num_nnelm == 3:      # 1st order triangle
            vtu.etype = 5
        elif vtu.num_nnelm == 4:    # quadrilateral
            vtu.etype = 9
        elif vtu.num_nnelm == 6:    # Quadratic triangle
            vtu.etype = 22
        elif vtu.num_nnelm == 8:    # Quadratic quad
            vtu.etype = 23
        else:
            print('This element type is not yet implemented.')
            exit()
    elif vtu.dof_nodes == 3:        # 3-dimensional case
        if vtu.num_nnelm == 4:      # Tetra
            vtu.etype = 10
        elif vtu.num_nnelm == 8:    # Hexahedron
            vtu.etype = 12
        elif vtu.num_nnelm == 10:   # Quadratic tetra
            vtu.etype = 24
        elif vtu.num_nnelm == 20:   # Quadratic hexahedron
            vtu.etype = 25
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
def generate_ugrid(vtu):
    vtu.ugrid = []
    vtu.ugrid.append('<?xml version="1.0" encoding="UTF-8"?>')
    vtu.ugrid_line = '<VTKFile xmlns="VTK" byte_order="LittleEndian" '\
                   + 'version="0.1" type="UnstructuredGrid">'
    vtu.ugrid.append(vtu.ugrid_line)
    vtu.ugrid.append('<UnstructuredGrid>')
    vtu.ugrid_line = '<Piece NumberOfPoints="%d" ' % vtu.nodes.shape[0]\
                   + 'NumberOfCells="%d">' % vtu.elems.shape[0]
    vtu.ugrid.append(vtu.ugrid_line)

#-----------------------------------------------------------------------------#
def finalize_ugrid(vtu):
    vtu.ugrid.append('</Piece>')
    vtu.ugrid.append('</UnstructuredGrid>')
    vtu.ugrid.append('</VTKFile>')

#-----------------------------------------------------------------------------#
def assign_nodes(vtu):
    vtu.ugrid.append('<Points>')
    if vtu.dof_nodes == 2:
        vtu.ugrid_line = '<DataArray NumberOfComponents="%d" '% \
                         (vtu.dof_nodes+1)
    elif vtu.dof_nodes == 3:
        vtu.ugrid_line = '<DataArray NumberOfComponents="%d" ' % \
                         vtu.dof_nodes
    vtu.ugrid_line += 'type="Float32" Name="coordinate" format="ascii">'
    vtu.ugrid.append(vtu.ugrid_line)

    for i in range(vtu.num_nodes):
        coord = ''
        for j in range(vtu.dof_nodes):
            if j == (vtu.dof_nodes - 1):
                if vtu.dof_nodes == 2:
                    coord += '%e 0.0' % vtu.nodes[i][j]
                else:
                    coord += '%e' % vtu.nodes[i][j]
            else:
                coord += '%e ' % vtu.nodes[i][j]
        vtu.ugrid.append(coord)
    vtu.ugrid.append('</DataArray>')
    vtu.ugrid.append('</Points>')

#-----------------------------------------------------------------------------#
def assign_elems(vtu):
    vtu.ugrid.append('<Cells>')
    vtu.ugrid_line = '<DataArray type="Int32" '\
                   + 'Name="connectivity" format="ascii">'
    vtu.ugrid.append(vtu.ugrid_line)

    for i in range(vtu.num_elems):
        connect = ''
        for j in range(vtu.num_nnelm):
            if j == (vtu.num_nnelm - 1):
                connect += '%d' % vtu.elems[i][j]
            else:
                connect += '%d ' % vtu.elems[i][j]
        vtu.ugrid.append(connect)
    vtu.ugrid.append('</DataArray>')

    #>> Insert offset data
    vtu.ugrid_line = '<DataArray type="Int32" '\
                   + 'Name="offsets" format="ascii">'
    vtu.ugrid.append(vtu.ugrid_line)

    offset_line = ''
    for i in range(vtu.num_elems):
        if ((i + 1) % 10 == 0) or (i == (vtu.num_elems - 1)):
            offset_line += '%d' % (vtu.num_nnelm*(i + 1))
            vtu.ugrid.append(offset_line)
            offset_line = ''
        else:
            offset_line += '%d ' % (vtu.num_nnelm*(i + 1))
    vtu.ugrid.append('</DataArray>')

    #>> Insert element type id
    vtu.ugrid_line = '<DataArray type="UInt8" '\
                   + 'Name="types" format="ascii">'
    vtu.ugrid.append(vtu.ugrid_line)

    etype_line = ''
    for i in range(vtu.num_elems):
        if ((i + 1) % 20 == 0) or (i == (vtu.num_elems - 1)):
            etype_line += '%d' % vtu.etype
            vtu.ugrid.append(etype_line)
            etype_line = ''
        else:
            etype_line += '%d ' % vtu.etype
    vtu.ugrid.append('</DataArray>')
    vtu.ugrid.append('</Cells>')

#-----------------------------------------------------------------------------#
def assign_displacement(vtu):
    num_comps = vtu.disp.shape[1]

    comp = ['x-direction', 'y-direction', 'z-direction']

    if num_comps == 2:
        vtu.ugrid_line = '<DataArray NumberOfComponents="%d" ' % \
                         (num_comps+1)
    elif num_comps == 3:
        vtu.ugrid_line = '<DataArray NumberOfComponents="%d" ' % \
                         (num_comps)

    vtu.ugrid_line += 'type="Float32" Name="Displacement" '
    for i in range(len(comp)):
        vtu.ugrid_line += 'ComponentName%d="%s" ' % (i, comp[i])
    vtu.ugrid_line += 'format="ascii">'
    vtu.ugrid.append(vtu.ugrid_line)

    emitted_warning_types = {'Inf':0, 'NaN':0}

    for i in range(vtu.num_nodes):
        line = ''
        for j in range(num_comps):
            if j == (num_comps - 1):
                if num_comps == 2:
                    line += '%e 0.0' % (vtu.disp[i][j])
                elif num_comps == 3:
                    line += '%e' % (vtu.disp[i][j])
            else:
                line += '%e ' % (vtu.disp[i][j])
        vtu.ugrid.append(line)
    vtu.ugrid.append('</DataArray>')

#-----------------------------------------------------------------------------#
def assign_stress(vtu):
    num_comps = vtu.stress.shape[1]

    if num_comps == 3:
        comps = ['xx component', 'yy component', 'xy component']
    elif num_comps == 5:
        comps = ['xx component', 'yy component', 'xy component',\
                    'max', 'min']
    elif num_comps == 6:
        comps = ['xx component', 'yy component', 'zz component',\
                    'xy component', 'xz component', 'yz component']
    elif num_comps == 9:
        comps = ['xx component', 'yy component', 'zz component',\
                    'xy component', 'xz component', 'yz component',\
                    'minor principal', 'intermediate principal',\
                    'major principal']

    vtu.ugrid_line = '<DataArray NumberOfComponents="%d" ' % (len(comps))
    vtu.ugrid_line += 'type="Float32" Name="Stress" '
    for i in range(len(comps)):
        vtu.ugrid_line += 'ComponentName%d="%s" ' % (i, comps[i])
    vtu.ugrid_line += 'format="ascii">'
    vtu.ugrid.append(vtu.ugrid_line)

    for i in range(vtu.num_nodes):
        line = ''
        for j in range(num_comps):
            if j == (num_comps - 1):
                line += '%e' % vtu.stress[i][j]
            else:
                line += '%e ' % vtu.stress[i][j]
        vtu.ugrid.append(line)
    vtu.ugrid.append('</DataArray>')

#-----------------------------------------------------------------------------#
def assign_strain(vtu):
    num_comps = vtu.strain.shape[1]

    if num_comps == 3:
        comps = ['xx component', 'yy component', 'xy component']
    elif num_comps == 6:
        comps = ['xx component', 'yy component', 'zz component',\
                    'xy component', 'xz component', 'yz component']

    vtu.ugrid_line = '<DataArray NumberOfComponents="%d" ' % (len(comps))
    vtu.ugrid_line += 'type="Float32" Name="Strain" '
    for i in range(len(comps)):
        vtu.ugrid_line += 'ComponentName%d="%s" ' % (i, comps[i])
    vtu.ugrid_line += 'format="ascii">'
    vtu.ugrid.append(vtu.ugrid_line)

    for i in range(vtu.num_nodes):
        line = ''
        for j in range(num_comps):
            if j == (num_comps - 1):
                line += '%e' % vtu.strain[i][j]
            else:
                line += '%e ' % vtu.strain[i][j]
        vtu.ugrid.append(line)
    vtu.ugrid.append('</DataArray>')

#-----------------------------------------------------------------------------#
