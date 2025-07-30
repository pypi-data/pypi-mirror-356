#coding:UTF-8

"""
# Name    : _format_svg.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 03 2024
# Date    : Mar. 12 2024
# Note    : Export svg data program
"""

import numpy as np

#-----------------------------------------------------------------------------#
def export_svg(fname, nodes, elems):
    """
    This function export .svg format file.

    Parameters
    ----------
    fname : str
        svg file name
    nodes : ndarray, 2-D
        node data
    elems : ndarray, 2-D
        element data
    """

    im_w = 480
    im_h = 640

    sides = get_sides(nodes, elems)
    outfile = open(fname ,'w')
    text = '<?xml version="1.0" encoding="utf-8"?>\n'
    text += '<!-- Generator: Adobe Illustrator 15.1.0, '
    text += 'SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->\n'
    text += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" '
    text += '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
    text += '<svg version="1.1" id="Layer_1" '
    text += 'xmlns="http://www.w3.org/2000/svg" '
    text += 'xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" '
    text += 'width="%dpx" height="%dpx" ' % (im_w, im_h)
    text += 'viewBox="0 0 %d %d" ' % (im_w, im_h)
    text += 'enable-background="new 0 0 %d %d"\n' % (im_w, im_h)
    text += 'xml:space="preserve">\n'
    text += '<style type="text/css">\n'
    text += '<![CDATA[\n'
    text += '.st0{fill:none;stroke:#000000;stroke-miterlimit:10;}\n'
    text += ']]>\n'
    text += '</style>\n'

    for i in range(sides.shape[0]):
        text += '<line class="st0" x1="%lf" y1="%lf" x2="%lf" y2="%lf"/>\n' %\
            (nodes[sides[i][0] ][0], im_h - nodes[sides[i][0]][1],\
             nodes[sides[i][1] ][0], im_h - nodes[sides[i][1]][1])

    text += '</svg>\n'
    outfile.write(text)
    outfile.close()

#-----------------------------------------------------------------------------#
def get_sides(nodes, elems):
    """
    This function retuns mesh sides data.

    Parameters
    ----------
    nodes : ndarray, 2-D
        node data
    elems : ndarray, 2-D
        element data

    Returns
    -------
    sides : ndarray, 2-D
        mesh sides data
    """

    num_nodes = nodes.shape[0]
    num_elems = elems.shape[0]
    num_nnelm = elems.shape[1]
    sides = []

    for i in range(num_elems):
        for j in range(num_nnelm):
            n1 = elems[i][j]
            if (j + 1) < num_nnelm:
                n2 = elems[i][j+1]
                if n2 < n1:
                    n2 = n1
                    n1 = elems[i][j+1]
                sides.append((n1, n2))
            else:
                n2 = elems[i][0]
                if n2 < n1:
                    n2 = n1
                    n1 = elems[i][0]
                sides.append((n1, n2))
    sides = np.array(list(set(sides)))

    return sides

#-----------------------------------------------------------------------------#
