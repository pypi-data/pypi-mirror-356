#coding:UTF-8

"""
# Name    : _class_lcloss.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 20 2023
# Note    : Neural netrwork tool Log-Cosh program.
"""

import torch
import torch.nn as nn

#-----------------------------------------------------------------------------#
class LCLoss(nn.Module):
    """
    Create criterion that measures the Log-Cosh error between each element
    in the input :math:`x` and target :math:`y`.

    The unreduced loss can be descrived as:

    .. math::
        \ell(x, y) = L = \{l_1,\dots,l_N\}^T, \quad
        l_n = \log\left(\cosh\left(x_n - y_n \\right)\\right)

    where :math:`N` is the batch size. If :attr:`reduction` is not 
    ``'none'`` (default ``'mean'``), then:

    .. math::
        \ell(x, y) = \operatorname{mean}(L)

    :math:`x` and :math:`y` are tensors of arbitrary shapes with a total
    of :math:`n` elements each.

    Examples
    --------
    >>> import torch
    >>> import cratch
    >>> loss = cratch.nn.LCLoss()
    >>> input = torch.randn(3, 5, requires_grad=True)
    >>> target = torch.randn(3, 5)
    >>> output = loss(input, target)
    >>> output.backward()
    """

    def __init__(self):
        super().__init__()
    def log_cosh_loss(self, y_pred, y_true):
        def _log_cosh(x):
            log2 = torch.log(torch.tensor(2.0))
            return x + nn.functional.softplus(-2.0*x) - log2
        return torch.mean(_log_cosh(y_pred - y_true))
    def forward(self, y_pred, y_true):
        return self.log_cosh_loss(y_pred, y_true)

#-----------------------------------------------------------------------------#
