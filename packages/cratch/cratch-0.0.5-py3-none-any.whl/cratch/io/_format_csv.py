#coding:UTF-8

"""
# Name    : _format_csv.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 12 2024
# Note    : Export csv data program
"""

import numpy as np
import pandas as pd

#-----------------------------------------------------------------------------#
def export_csv(fname, nodes, disp=None,\
               stress=None, strain=None):
    """
    This function export csv file for analysis result.

    Parameters
    ----------
    fname : str
        csv file name
    nodes : ndarray, 2-D
        node data
    disp : ndarray, 2-D, optional
        nodal displacement data
    stress : ndarray, 2-D, optional
        nodal stress data
    strain : ndarray, 2-D, optional
        nodal strain data
    """
    dof_nodes = nodes.shape[1]

    if dof_nodes == 2:
        all_result = np.hstack((nodes, disp,\
                                stress[:, 0:3],\
                                strain[:, 0:3]))
        header = ['x', 'y', 'disp_x', 'disp_y',\
                  'sigma_xx', 'sigma_yy', 'sigma_xy',\
                  'eps_xx', 'eps_yy', 'eps_xy']
        dframe = pd.DataFrame(data = all_result)
        dframe.to_csv(fname, header=header, index=False)

#-----------------------------------------------------------------------------#
