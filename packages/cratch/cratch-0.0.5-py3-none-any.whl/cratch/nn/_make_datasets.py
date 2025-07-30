#coding:UTF-8

"""
# Name    : _make_dataset.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Neural netrwork tool for making dataset.
"""

import numpy as np
import random

#-----------------------------------------------------------------------------#
def make_datasets(inp, out, valid_size):
    """
    This function returns learning datasets for training and validation.

    Parameters
    ----------
    inp : ndarray, 2-D
        input data
    out : ndarray, 2-D
        output data
    valid_size : float
        0.1 ~ 0.9

    Returns
    -------
    trainset : list
        [input data(ndarray,2-D) and output data (ndarray, 2-D)]
    validset : list
        [input data(ndarray,2-D) and output data (ndarray, 2-D)]
    """
    num_data = inp.shape[0]
    all_index = list(np.arange(num_data, dtype=int))
    num_valid = int(num_data*valid_size)
    valid_idx = np.sort(random.sample(all_index, num_valid))
    idx = np.zeros(num_data, dtype=bool)
    idx[valid_idx] = True
    trainset = [inp[~idx], out[~idx]]
    validset = [inp[idx], out[idx]]

    return trainset, validset

#-----------------------------------------------------------------------------#
