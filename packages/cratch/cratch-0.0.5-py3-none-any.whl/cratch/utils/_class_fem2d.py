#coding:UTF-8

import numpy as np
from ._quadtools import quadrature

#-----------------------------------------------------------------------------#
class FEM2D():
    """
    Two dimensional Finite Element Method class
    """
    def __init__(self, nodes=None, elems=None):
        self.stress_state = ''  # 'plane_stress' or plane_strain
        self.E = 210000.0       # Young's modulus [MPa]
        self.nu = 0.3           # Poisson's ratio
        self.type_data = float
        self.num_nodes = 0  # number of nodes
        self.num_elems = 0  # number of elements
        self.num_nnelm = 0  # number of nodes in an element
        self.dof_nodes = 2  # degrees of freedom of node
        self.dof_elems = 0  # degrees of freedom of element
        self.mesh_type = None   # degrees of freedom of element

        if (nodes is not None) and (elems is not None):
            self.num_nodes = nodes.shape[0]
            self.num_elems = elems.shape[0]
            self.num_nnelm = elems.shape[1]
            self.dof_elems = self.num_nnelm*self.dof_nodes
            self.b_matrix = np.zeros((3, self.dof_elems), dtype=float)
            self.elem_type = self.get_elem_type(nodes)
            #>> Set default gaussian weight & point
            self.W, self.Q = self.set_gauss_default()

    def make_d_matrix(self):
        """
        This function make 'D' matrix using E and nu.

        Examples
        --------
        >>> import cratch.utils
        >>> fem = cratch.utils.FEM2D()
        >>> fem.stress_state = 'plane_stress'
        >>> fem.E = 210000
        >>> fem.nu = 0.3
        >>> fem.make_d_matrix()
        >>> fem.d_matrix
        array([[230769.23076923,  69230.76923077,      0.        ],
               [ 69230.76923077, 230769.23076923,      0.        ],
               [     0.        ,      0.        ,  80769.23076923]])

        """
        E = self.E; nu = self.nu
        if E == 0.0:
            print('Please set E')
            exit()

        self.d_matrix = np.zeros((3, 3), dtype=float)

        if self.stress_state == 'plane_stress':
            c11 = E / (1.0 - nu*nu)
            c12 = E*nu / (1.0 - nu*nu)
            c33 = 0.5*E*(1.0 - nu) / (1.0 - nu*nu)
            self.d_matrix[0, 0] = c11
            self.d_matrix[0, 1] = c12
            self.d_matrix[1, 0] = c12
            self.d_matrix[1, 1] = c11
            self.d_matrix[2, 2] = c33
        elif self.stress_state == 'plane_strain':
            c11 = E*(1.0 - nu) / ((1.0 + nu)*(1.0 - 2.0*nu))
            c12 = E*nu / ((1.0 + nu)*(1.0 - 2.0*nu))
            c33 = E / (2.0*(1.0 + nu))
            self.d_matrix[0, 0] = c11
            self.d_matrix[0, 1] = c12
            self.d_matrix[1, 0] = c12
            self.d_matrix[1, 1] = c11
            self.d_matrix[2, 2] = c33
        else:
            print('Please check stress_state!')
            exit()

    def get_elem_type(self, nodes):
        if nodes.shape[1] != 2:
            print('nodes shape error...')
            exit()
        else:
            if self.num_nnelm == 3:
                elem_type = 'T3'
            elif self.num_nnelm == 4:
                elem_type = 'Q4'
            elif self.num_nnelm == 6:
                elem_type = 'T6'
            elif self.num_nnelm == 8:
                elem_type = 'Q8'
            else:
                print('elems shape error...')
                exit()
        return elem_type

    def set_gauss_default(self):
        quadorder = 3
        sdim = self.dof_nodes
        if self.elem_type == 'T3' or self.elem_type == 'T6':
            qt = 'TRIANGULAR'
        else:
            qt = 'GAUSS'
        if self.elem_type == 'T3':
            sdim = 1; quadorder = 1
        return quadrature(quadorder, qt, sdim)

#-----------------------------------------------------------------------------#




















