#coding:UTF-8

import numpy as np
import matplotlib.pyplot as plt

from ._cmap2list import cmap2list

#-----------------------------------------------------------------------------#
def cmap2dashedlines(num):
    """
    This function returns dashed line list.
    Please set ``linestyle`` in plt.plot.

    Parameters
    ----------
    num : int
        The number of items.

    Returns
    -------
    dashedlist : list
        Dashed lines list.

    Example
    -------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> import cratch
    >>> a = np.arange(10)
    >>> b = np.ones((3, 10))
    >>> b[1] += 1
    >>> b[2] += 2
    >>> dashed_lines = cratch.plot.cmap2dashedlines(3)
    >>> plt.plot(a, b[0], linestyle=dashed_lines[0])
    >>> plt.plot(a, b[1], linestyle=dashed_lines[1])
    >>> plt.plot(a, b[2], linestyle=dashed_lines[2])
    >>> plt.show()
    """

    cmaplist = cmap2list(plt.cm.gist_yarg, num)
    dashedlist = []
    for i in range(num):
        tmp = np.array(cmaplist[num-1-i])[::-1]*(i+1) + 0.0001
        #tmp = (tmp[0], tuple(tmp[1:]))
        dashedlist.append((tmp[0], tuple(tmp[1:])))
        #dashedlist.append(tmp)
    return dashedlist[::-1]

#-----------------------------------------------------------------------------#
