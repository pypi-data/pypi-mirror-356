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
"""``embeam`` is a Python library for for modelling beams and lenses in electron
microscopy.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For general array handling.
import numpy as np

# For validating and converting objects.
import czekitout.convert



# Import child modules and packages of current package.
import embeam.constants
import embeam.gun
import embeam.lens
import embeam.coherent
import embeam.stem

# Get version of current package.
from embeam.version import __version__



##################################
## Define classes and functions ##
##################################

# List of public objects in package.
__all__ = ["wavelength"]



def _check_and_convert_beam_energy(params):
    obj_name = "beam_energy"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    beam_energy = czekitout.convert.to_positive_float(**kwargs)

    return beam_energy



def _check_and_convert_skip_validation_and_conversion(params):
    obj_name = "skip_validation_and_conversion"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    skip_validation_and_conversion = czekitout.convert.to_bool(**kwargs)

    return skip_validation_and_conversion



_default_beam_energy = 80
_default_skip_validation_and_conversion = False



def wavelength(beam_energy=\
               _default_beam_energy,
               skip_validation_and_conversion=\
               _default_skip_validation_and_conversion):
    r"""Determine the relativistic electron beam wavelength from the energy of a
    coherent beam.

    The relativistic electron beam wavelength of a coherent beam is calculated
    by:

    .. math ::
        \lambda=\frac{h}{\sqrt{2m_{e}E\left(1+\frac{E}{2m_{e}c^{2}}\right)}},
        :label: electron_beam_wavelength__1

    where :math:`h` is Planck's constant, :math:`m_e` is the rest mass of an
    electron, :math:`e` is the elementary charge, :math:`c` is the speed of 
    light, and :math:`E` is the beam energy.

    Parameters
    ----------
    beam_energy : `float`, optional
        The beam energy, :math:`E`, in units of keV. Must be positive.
    skip_validation_and_conversion : `bool`, optional
        If ``skip_validation_and_conversion`` is set to ``False``, then
        validations and conversions are performed on the above
        parameters. 

        Otherwise, if ``skip_validation_and_conversion`` is set to ``True``, no
        validations and conversions are performed on the above parameters. This
        option is desired primarily when the user wants to avoid potentially
        expensive validation and/or conversion operations.

    Returns
    -------
    wavelength : `float`
        The relativistic electron beam wavelength in units of Å.

    """
    params = locals()

    func_alias = _check_and_convert_skip_validation_and_conversion
    skip_validation_and_conversion = func_alias(params)

    if (skip_validation_and_conversion == False):
        global_symbol_table = globals()
        for param_name in params:
            if param_name == "skip_validation_and_conversion":
                continue
            func_name = "_check_and_convert_" + param_name
            func_alias = global_symbol_table[func_name]
            params[param_name] = func_alias(params)

    kwargs = params
    del kwargs["skip_validation_and_conversion"]
    result = _wavelength(**kwargs)

    return result



def _wavelength(beam_energy):
    V = beam_energy * 1000  # Applied beam voltage, in units of volts.
    m_e = embeam.constants.m_e()
    e = embeam.constants.e()
    c = embeam.constants.c()
    h = embeam.constants.h()

    result = (h
              / np.sqrt(1 + e * V / 2 / m_e / c / c)
              / np.sqrt(2 * m_e * e * V)
              * 1.0e10)

    return result



###########################
## Define error messages ##
###########################
