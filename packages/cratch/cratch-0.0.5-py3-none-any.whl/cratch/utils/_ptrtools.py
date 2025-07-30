import numpy as np
import ctypes

#-----------------------------------------------------------------------------#
def get_ctypestools():
    """
    This function returns ctypes pointer tools
    
    Examples
    --------
    >>> import cratch.utils
    >>> ndpointer, c_int, c_int_p, c_int_pp,\
 c_double, c_double_p, c_double_pp = cratch.utils.get_ctypestools()
    """

    ndpointer = np.ctypeslib.ndpointer
    c_int = ctypes.c_int
    c_int_p = ctypes.POINTER(c_int)
    c_int_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')
    c_double = ctypes.c_double
    c_double_p = ctypes.POINTER(c_double)
    c_double_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')

    return ndpointer, c_int, c_int_p, c_int_pp,\
           c_double, c_double_p, c_double_pp

#-----------------------------------------------------------------------------#
def convert_pointer(arr):
    """
    This function converts nparray to pointer of c langeuage

    Parameters
    ----------
    arr : ndarray(2D)

    Returns
    -------
    pointer
    """
    if len(arr.shape) == 1: # 1D array
        v_type = type(arr[0])
        if v_type == np.float64:
            p_type = ctypes.POINTER(ctypes.c_double)
        elif v_type == np.int32:
            p_type = ctypes.POINTER(ctypes.c_int)
        pointer = arr.ctypes.data_as(p_type)
    elif len(arr.shape) == 2: # 2D array
        pointer = (arr.__array_interface__['data'][0]\
                  + np.arange(arr.shape[0])*arr.strides[0]).astype(np.uintp)
    else:
        print('array dimensional error.')
        exit()
    return pointer

#-----------------------------------------------------------------------------#
