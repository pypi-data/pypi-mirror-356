#coding:UTF-8

import numpy as np

#-----------------------------------------------------------------------------#
def cmap2list(cmap, num):
    """
    This function returns pickupd cmap value at 256 steps.

    Parameters
    ----------
    cmap : class
        Matplotlib color map instance name.
    num : int
        Number of items.

    Returns
    -------
    cmaplist : list
        Discritized color list.

    Example
    -------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> import cratch
    >>> a = np.arange(10)
    >>> cmaplist = cratch.plot.cmap2list(plt.cm.jet, 10)
    >>> for i in range(10):
    ...     plt.plot(a[i], a[i], 'o', color=cmaplist[i])
    ...
    >>> plt.show()
    """
    colors = [cmap(i) for i in range(cmap.N)]
    cmapidx = np.linspace(0, 255, num, dtype=int)
    cmaplist = [colors[i] for i in cmapidx]
    return cmaplist

#-----------------------------------------------------------------------------#
