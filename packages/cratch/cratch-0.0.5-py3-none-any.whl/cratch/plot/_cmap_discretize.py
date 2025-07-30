#coding:UTF-8
import numpy as np
import matplotlib
def cmap_discretize(cmap, num):
    """
    This function retuns a discretized colormap from the continuous
    color map.

    Parameters
    ----------
    cmap : class
        Colormap instance.
    num : int
        The number of steps.

    Returns
    -------
    x : class
        Discretized colormap.

    Example
    -------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> import cratch
    >>> a = np.resize(np.arange(100), (5, 100))
    >>> jet_d = cratch.plot.cmap_discretize(plt.cm.jet, 10)
    >>> plt.imshow(a, cmap=jet_d)
    >>> plt.show()
    """
    colors_i = np.concatenate((np.linspace(0, 1, num),\
                              (0.0, 0.0, 0.0, 0.0, 0.0)))
    colors_rgba = cmap(colors_i)
    indices = np.linspace(0, 1, num+1)
    cdict = {}
    for ki, key in enumerate(('red', 'green', 'blue')):
        cdict[key] = [(indices[i], colors_rgba[i-1, ki],\
                       colors_rgba[i, ki])\
                      for i in range(num+1)]
    return matplotlib.colors.LinearSegmentedColormap(\
            cmap.name+'%d' % num, cdict, 1024)
