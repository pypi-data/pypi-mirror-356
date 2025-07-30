#coding:UTF-8

"""
# Name    : _model_init.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Jan. 07 2025
# Date    : Mar. 20 2023
# Note    : Neural netrwork tool for model initialization.
"""

import numpy as np
import torch
import torch.nn as nn

#-----------------------------------------------------------------------------#
def model_init(model, init_type=None, bias=None, option=None):
    """
    This function initializes neural network model parameters.

    Parameters
    ----------
    model: class
        Neural network model.
    init_type: str
        Initialization type.
        "xavier_normal", "xavier_uniform",
        "kaiming_normal", "kaiming_uniform",
        "trunc_normal".
    bias: float
        Initialized bias value.
    option: list
        Truncated nomal distribution option.
        ['default'], ['xavier', mean(faloat)]
        or ['custom', mean, std, a, b](mean, std, a, b are float
        and a < mean < b).
    """

    for name, param in model.named_parameters():
        if 'weight' in name:
            model_init_weight(model, name, param, init_type, option)

        if 'bias' in name:
            model_init_bias(model, name, param, bias)

#-----------------------------------------------------------------------------#
def model_init_weight(model, name, param, init_type, option):
    """
    Model weight initialization.
    """
    shape = param.shape
    inits = torch.empty(shape)
    if init_type == None:
        pass

    else:
        if param.dim() != 1:
            if init_type == 'xavier_normal':
                inits = nn.init.xavier_normal_(inits)

            elif init_type == 'xavier_uniform':
                inits = nn.init.xavier_uniform_(inits)

            elif init_type == 'kaiming_normal':
                inits = nn.init.kaiming_normal_(inits)

            elif init_type == 'kaiming_uniform':
                inits = nn.init.kaiming_uniform_(inits)

            elif init_type == 'trunc_normal':
                num_params = np.sum(shape)
                if option == None or option[0] == 'default':
                    '''
                    Default truncated normal distribution
                    mean = 0.0, std = 1.0, a = -2.0, b = 2.0
                    '''
                    inits = nn.init.trunc_normal_(inits)
                elif option[0] == 'xavier':
                    std = np.sqrt(2.0 / num_params)
                    b = 2.0*std
                    a = -1.0*b
                    inits = nn.init.trunc_normal_(inits,\
                        mean=option[1], std=std, a=a, b=b)
                elif option[0] == 'custom':
                    '''
                    Customized truncated normal distribution
                    '''
                    inits = nn.init.trunc_normal_(inits,\
                        mean=option[1], std=option[2],\
                        a=option[3], b=option[4])
            else:
                error_weight_init()

            model.state_dict()[name][:] = inits
    del inits

#-----------------------------------------------------------------------------#
def error_weight_init():
    print('[Error: model_init] Please check "init_type"')
    print('Please use bellow:')
    print('  "xavier_normal", "xavier_uniform",')
    print('  "kaiming_normal", "kaiming_uniform",')
    print('  "trunc_normal"')
    exit()

#-----------------------------------------------------------------------------#
def model_init_bias(model, name, param, bias):
    """
    Model bias initialization.
    """
    if bias == None:
        inits = torch.empty(1)
        pass
    elif bias == 0.0:
        inits = torch.zeros(param.shape)
        model.state_dict()[name][:] = inits
    elif bias == 1.0:
        inits = torch.ones(param.shape)
        model.state_dict()[name][:] = inits
    else:
        inits = torch.ones(param.shape)*bias
        model.state_dict()[name][:] = inits
    del inits

#-----------------------------------------------------------------------------#
