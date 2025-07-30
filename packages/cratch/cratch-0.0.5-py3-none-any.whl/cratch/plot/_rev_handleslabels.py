#coding:UTF-8

import matplotlib.pyplot as plt

#-----------------------------------------------------------------------------#
def rev_handleslabels(ncol=1):
    """
    This function reverse handles and labels. Please use after ``plt.legend()``.

    Parameters
    ----------
    ncol : int, optional
        Number of columns.

    Example
    -------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> import cratch
    >>> a = np.arange(10)
    >>> b = np.ones((3, 10))
    >>> b[1] += 1
    >>> b[2] += 2
    >>> plt.plot(a, b[0], label='0')
    >>> plt.plot(a, b[1], label='1')
    >>> plt.plot(a, b[2], label='2')
    >>> plt.legend()
    >>> cratch.plot.rev_handleslabels()
    >>> plt.show()
    """

    h = plt.legend().get_lines()
    plt.legend(handles=h[::-1], ncol=ncol)

#-----------------------------------------------------------------------------#
