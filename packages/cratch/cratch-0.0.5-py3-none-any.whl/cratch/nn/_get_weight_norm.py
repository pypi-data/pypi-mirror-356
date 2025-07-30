#coding:UTF-8

"""
# Name    : _get_weight_norm.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Neural netrwork tool for regularization.
"""

import torch

#-----------------------------------------------------------------------------#
def get_weight_norm(model, reg_type='L2'):
    """
    This function returns weight norm for regularization.

    Parameters
    ----------
    model : class
        neural network model.
    reg_type : str
        'L1' is Lasso regression. 'L2' is Ridge regression (default).

    Returns
    -------
    norm_w : tensor
        weight norm.
    """
    norm_w = torch.tensor(0.0, requires_grad=True)
    for name, param in model.named_parameters():
        if 'weight' in name:
            if reg_type == 'L2': # Ridge L2 norm
                norm_w = norm_w + torch.linalg.norm(param)**2
            elif reg_type == 'L1': # Lasso L1 norm
                norm_w = norm_w + torch.linalg.norm(param,1)
    return norm_w

#-----------------------------------------------------------------------------#
