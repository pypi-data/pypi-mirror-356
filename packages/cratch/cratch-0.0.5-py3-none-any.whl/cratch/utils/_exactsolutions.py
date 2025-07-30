#coding:UTF-8

"""
# Name    : _exactsolutions.py
# Author  : Takuya TOYOSHI
# Version : 1.1.0
# Updata  : Dec. 04 2024
# Date    : Mar. 20 2023
# Note    : finite element method tool program
"""

import numpy as np

#-----------------------------------------------------------------------------#
def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return rho, phi

#-----------------------------------------------------------------------------#
def getexact_circularhole(x, y, force, E, nu, sstate, thickness, R):
    """
    This function returns circular hole (1/4 model) exact solution in polar coordinate.

    [Displacement field]

    .. math::
       :nowrap:

        \\begin{eqnarray}
        {u_x}\\left( r\\operatorname{,}\\theta \\right) &=&\\frac{\\left( \\kappa -3\\right)  \\cos{\\left( \\theta \\right) } T {{r}^{4}}+\\left( \\left( -2 \\kappa +2\\right)  \\cos{\\left( \\theta \\right) }-2 \\cos{\\left( 3 \\theta \\right) }\\right)  {{a}^{2}} T {{r}^{2}}+2 \\cos{\\left( 3 \\theta \\right) } {{a}^{4}} T}{8 \\mu  {{r}^{3}}} \\\\

        {u_y}\\left( r\\operatorname{,}\\theta \\right) &=&\\frac{\\left( \\kappa +1\\right)  \\sin{\\left( \\theta \\right) } T {{r}^{4}}+\\left( \\left( 2 \\kappa +2\\right)  \\sin{\\left( \\theta \\right) }-2 \\sin{\\left( 3 \\theta \\right) }\\right)  {{a}^{2}} T {{r}^{2}}+2 \\sin{\\left( 3 \\theta \\right) } {{a}^{4}} T}{8 \\mu  {{r}^{3}}}
        \\end{eqnarray}

    where

    .. math::
        \\mu = \\frac{{E}}{2 \\left(1 + \\nu\\right)}, \\kappa = \\frac{3 - \\nu}{1 + \\nu}

    [Stress field : plane stress]

    .. math::
       :nowrap:

        \\begin{eqnarray}
        {{\\sigma }_{xx}}\\left( r\\operatorname{,}\\theta \\right) &=&-\\frac{3 \\cos{\\left( 4 \\theta \\right) } T {{a}^{4}}+\\left( -2 \\cos{\\left( 4 \\theta \\right) }-\\cos{\\left( 2 \\theta \\right) }\\right)  {{r}^{2}} T {{a}^{2}}}{2 {{r}^{4}}} \\\\

        {{\\sigma }_{yy}}\\left( r\\operatorname{,}\\theta \\right) &=&\\frac{3 \\cos{\\left( 4 \\theta \\right) } T {{a}^{4}}+\\left( -2 \\cos{\\left( 4 \\theta \\right) }+3 \\cos{\\left( 2 \\theta \\right) }\\right)  {{r}^{2}} T {{a}^{2}}+2 {{r}^{4}} T}{2 {{r}^{4}}} \\\\

        {{\\sigma }_{xy}}\\left( r\\operatorname{,}\\theta \\right) &=&-\\frac{3 \\sin{\\left( 4 \\theta \\right) } T {{a}^{4}}+\\left( -2 \\sin{\\left( 4 \\theta \\right) }+\\sin{\\left( 2 \\theta \\right) }\\right)  {{r}^{2}} T {{a}^{2}}}{2 {{r}^{4}}}

        \\end{eqnarray}

    [Strain field : plane stress]

    .. math::
       :nowrap:

        \\begin{eqnarray}
        {{\\varepsilon}_{xx}} \\left( r, \\theta \\right) &=& -\\frac{\\left( 3 \\cos{\\left( 4 \\theta \\right) } \\nu +3 \\cos{\\left( 4 \\theta \\right) }\\right)  T {{a}^{4}}+\\left( \\left( -2 \\cos{\\left( 4 \\theta \\right) }+3 \\cos{\\left( 2 \\theta \\right) }\\right)  \\nu -2 \\cos{\\left( 4 \\theta \\right) }-\\cos{\\left( 2 \\theta \\right) }\\right)  {{r}^{2}} T {{a}^{2}}+2 \\nu  {{r}^{4}} T}{2 E {{r}^{4}}} \\\\

        {{\\varepsilon}_{yy}} \\left( r, \\theta \\right) &=& \\frac{\\left( 3 \\cos{\\left( 4 \\theta \\right) } \\nu +3 \\cos{\\left( 4 \\theta \\right) }\\right)  T {{a}^{4}}+\\left( \\left( -2 \\cos{\\left( 4 \\theta \\right) }-\\cos{\\left( 2 \\theta \\right) }\\right)  \\nu -2 \\cos{\\left( 4 \\theta \\right) }+3 \\cos{\\left( 2 \\theta \\right) }\\right)  {{r}^{2}} T {{a}^{2}}+2 {{r}^{4}} T}{2 E {{r}^{4}}} \\\\

        {{\\gamma}_{xy}} \\left( r, \\theta \\right) &=& -\\frac{\\left( 3 \\sin{\\left( 4 \\theta \\right) } \\nu +3 \\sin{\\left( 4 \\theta \\right) }\\right)  T {{a}^{4}}+\\left( \\left( -2 \\sin{\\left( 4 \\theta \\right) }+\\sin{\\left( 2 \\theta \\right) }\\right)  \\nu -2 \\sin{\\left( 4 \\theta \\right) }+\\sin{\\left( 2 \\theta \\right) }\\right)  {{r}^{2}} T {{a}^{2}}}{E {{r}^{4}}}

        \\end{eqnarray}

    Parameters
    ----------
    x : ndarray, 1-D
        coordinate x (cartecian coordinate).
    y : ndarray, 1-D
        coordinate y (cartecian coordinate).
    force : float
        Traction force [N]
    E : float
        Young's Modulous [MPa]
    nu : float
        Poisson's ratio
    sstate : str
        Stress state 'plane_strain' or 'plane_stress'
    thickness : float
        Plate thickness [mm]. 'plane_stress' is needed.
    R : float
        Circular hole radius.

    Returns
    -------
    u : ndarray, 1-D
        Exact solution of :math:`u`.
    v : ndarray, 1-D
        Exact solution of :math:`v`.
    sig_xx : ndarray, 1-D
        Exact solution of :math:`\\sigma_{xx}`.
    sig_yy : ndarray, 1-D
        Exact solution of :math:`\\sigma_{yy}`.
    sig_xy : ndarray, 1-D
        Exact solution of :math:`\\sigma_{xy}`.
    eps_xx : ndarray, 1-D
        Exact solution of :math:`\\varepsilon_{xx}`.
    eps_yy : ndarray, 1-D
        Exact solution of :math:`\\varepsilon_{yy}`.
    gamma_xy : ndarray, 1-D
        Exact solution of :math:`\\gamma_{xy}`.
    """
    r, theta = cart2pol(x, y)
    tx = force

    width = np.max(x) - np.min(x)
    area = width*thickness
    sigma = tx/area

    a = R
    if sstate == 'plane_stress':
        mu = E/(2.0*(1.0 + nu)) # 'plane_stress'
        k = (3.0 - nu)/(1.0 + nu) # 'plane_stress'
    elif sstate == 'plane_stress':
        mu = E/(1-2*nu) # 'plane_strain'
        k = (3-4*nu) # 'plane_strain'
    else:
        print('Check sstate'); exit()

    cos = np.cos
    sin = np.sin
    u = ((k-3)*cos(theta)*sigma*r**4\
      + ((-2*k+2)*cos(theta) - 2*cos(3*theta))*a**2*sigma*r**2\
      + 2*cos(3*theta)*a**4*sigma)/(8*mu*r**3)
    v = ((k+1)*sin(theta)*sigma*r**4\
      + (( 2*k+2)*sin(theta) - 2*sin(3*theta))*a**2*sigma*r**2\
      + 2*sin(3*theta)*a**4*sigma)/(8*mu*r**3)

    sig_xx = -(3*cos(4*theta)*sigma*a**4+(-2*cos(4*theta)\
               -cos(2*theta))*r**2*sigma*a**2)/(2*r**4)
    sig_yy =  (3*cos(4*theta)*sigma*a**4+(-2*cos(4*theta)\
               +3*cos(2*theta))*r**2*sigma*a**2+2*r**4*sigma)/(2*r**4)
    sig_xy = -(3*sin(4*theta)*sigma*a**4+(-2*sin(4*theta)\
               +sin(2*theta))*r**2*sigma*a**2)/(2*r**4)

    eps_xx = -((3*cos(4*theta)*nu+3*cos(4*theta))*sigma*a**4\
           + ((-2*cos(4*theta)+3*cos(2*theta))*nu-2*cos(4*theta)\
           - cos(2*theta))*r**2*sigma*a**2+2*nu*r**4*sigma)/(2*E*r**4)

    eps_yy = ((3*cos(4*theta)*nu+3*cos(4*theta))*sigma*a**4\
           + ((-2*cos(4*theta)-cos(2*theta))*nu-2*cos(4*theta)\
           + 3*cos(2*theta))*r**2*sigma*a**2+2*r**4*sigma)/(2*E*r**4)

    eps_xy = -((3*sin(4*theta)*nu+3*sin(4*theta))*sigma*a**4\
           + ((-2*sin(4*theta)+sin(2*theta))*nu-2*sin(4*theta)\
           + sin(2*theta))*r**2*sigma*a**2)/(E*r**4)


    return u, v, sig_xx, sig_yy, sig_xy, eps_xx, eps_yy, eps_xy

#-----------------------------------------------------------------------------#
