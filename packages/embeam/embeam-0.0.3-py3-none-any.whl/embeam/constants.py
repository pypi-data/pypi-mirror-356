# -*- coding: utf-8 -*-
# Copyright 2024 Matthew Fitzpatrick.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
"""A module that stores the values of a set of physical constants that are used 
for modelling.

"""



#####################################
## Load libraries/packages/modules ##
#####################################



##################################
## Define classes and functions ##
##################################

# List of public objects in package.
__all__ = ["h",
           "m_e",
           "e",
           "c"]



def h():
    r"""Return the value of Plank's constant :math:`h` in SI units.

    Returns
    -------
    result : `float`
        The value of Plank's constant :math:`h` in SI units.

    """
    result = 6.62607e-34

    return result



def m_e():
    r"""Return the value of the rest mass of an electron :math:`m_e` in SI 
    units.

    Returns
    -------
    result : `float`
        The value of the rest mass of an electron :math:`m_e` in SI units.

    """
    result = 9.109383e-31

    return result



def e():
    r"""Return the value of the elementary charge :math:`e` in SI 
    units.

    Returns
    -------
    result : `float`
        The value of the elementary charge :math:`e` in SI units.

    """
    result = 1.602177e-19

    return result



def c():
    r"""Return the value of the speed of light :math:`c` in SI units.

    Returns
    -------
    result : `float`
        The value of the speed of light :math:`c` in SI units.

    """
    result = 299792458.

    return result



###########################
## Define error messages ##
###########################
