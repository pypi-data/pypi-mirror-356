
from ._class_fem2d import FEM2D

#from ._plottools import (
#    plot_wireframe,
#    plot_nodalvalue,
#)

from ._quadtools import (
    quadrature,
    dunavant_rule,
)


from ._shapefunctions import (
    shape_function
)


from ._matrixtools import (
    delta2disp,
    disp2delta,
    get_elem,
    make_b_matrix,
    make_global_force_vector,
    make_global_stiffness_matrix,
    assemble_k_matrix,
    calculate_stress_strain,
)


from ._exactsolutions import (
    getexact_circularhole,
)


from ._solvertools import (
    load_local_library,
    load_local_solver,
    #load_solver,
    #femsolver,
    #use_femsolver,
    #conjugate_gradients,
    #cg_solver,
    #ichol,
    #mumpssolver,
)

from ._ptrtools import (
    get_ctypestools,
    convert_pointer,
)

from ._bctools import (
    get_fixarray,
    set_fix,
    set_load_oneside2D,
)

from ._conv_fast_bc import (
    conv_fast_bc,
)

__all__ = [
    'FEM2D',
    #'plot_wireframe',
    #'plot_nodalvalue',
    'quadrature',
    'dunavant_rule',
    'shape_function',
    'delta2disp',
    'disp2delta',
    'get_elem',
    'make_b_matrix',
    'make_global_force_vector',
    'make_global_stiffness_matrix',
    'assemble_k_matrix',
    'calculate_stress_strain',
    'getexact_circularhole',
    #----- _solvertools import -----,
    'load_local_library',
    'load_local_solver',
    #'load_solver',
    #'femsolver',
    #'use_femsolver',
    #'conjugate_gradients',
    #'cg_solver',
    #'ichol',
    #'mumpssolver',
    'get_ctypestools',
    'convert_pointer',
    'get_fixarray',
    'set_fix',
    'set_load_oneside2D',
    'conv_fast_bc',
]
