# SPDX-FileCopyrightText: 2025-present Takuya TOYOSHI
#
# SPDX-License-Identifier: MIT

from cratch import plot
from cratch import mesh

def whatis():
    print('\
    ##############################################\n\
    #                         ##          ##     #\n\
    #                         ##          ##     #\n\
    #  ####  ## ##  ####    ######  ####  #####  #\n\
    # ##     ###   ##  ##     ##   ##     ##  ## #\n\
    # ##     ##    ##  ###    ##   ##     ##  ## #\n\
    #  ####  ##     #### ##   ##    ####  ##  ## #\n\
    # ------------------------------------------ #\n\
    # Computational mechanics and Neural network #\n\
    # =                              ==          #\n\
    # tool using Torch library.                  #\n\
    # =             ==                           #\n\
    ##############################################')

# Automatic graph-stype update only "import cratch"
import matplotlib.pyplot as plt
params = {
    'font.family'           : 'serif',
    'font.serif'            : ['Times New Roman']+plt.rcParams['font.serif'],
    'savefig.dpi'           : 300,
    'pdf.fonttype'          : 42,
    'axes.labelsize'        : 22,
    'legend.fontsize'       : 14,
    'legend.labelspacing'   : 0.05,
    'xtick.labelsize'       : 20,
    'ytick.labelsize'       : 20,
    'mathtext.fontset'      : 'cm',
    'mathtext.default'      : 'it',
    'xtick.direction'       : 'in',
    'ytick.direction'       : 'in',
    'figure.figsize'        : [6.4, 4.8], # 640x480 pixel x3(300dpi)
    'figure.autolayout'     : True, # Automatic layout set
    'grid.linestyle'        : '-',
    'grid.alpha'            : '0.5',
    'text.usetex'           : False,
    'lines.linewidth'       : 1,
    #'zticks.labelsize'      : 20,
    #'axes.axisbelow'        : True, # True : background grid
    #'backend'               : 'cairo',
}
plt.rcParams.update(params)
