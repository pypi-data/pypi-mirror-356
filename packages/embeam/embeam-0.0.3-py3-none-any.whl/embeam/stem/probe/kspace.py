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
r"""Contains classes representing :math:`k`-space functions of probes.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For using special math functions and constants.
import numpy as np

# For defining classes that support enforced validation, updatability,
# pre-serialization, and de-serialization.
import fancytypes



# For calculating the electron beam wavelength; validating, pre-serializing, and
# de-pre-serializing instances of :class:`embeam.stem.probe.ModelParams`;
# temporarily disabling chromatic aberrations; and constructing instances of the
# class :class:`embeam.coherent.PhaseDeviation`.
import embeam



##################################
## Define classes and functions ##
##################################

# List of public objects in objects.
__all__ = ["Wavefunction",
           "Intensity"]



def _check_and_convert_coherent_probe_model_params(params):
    module_alias = embeam.stem.probe
    func_alias = module_alias._check_and_convert_coherent_probe_model_params
    probe_model_params = func_alias(params)

    return probe_model_params



def _pre_serialize_probe_model_params(probe_model_params):
    obj_to_pre_serialize = probe_model_params
    module_alias = embeam.stem.probe
    func_alias = module_alias._pre_serialize_probe_model_params
    serializable_rep = func_alias(obj_to_pre_serialize)

    return serializable_rep



def _de_pre_serialize_probe_model_params(serializable_rep):
    module_alias = embeam.stem.probe
    func_alias = module_alias._de_pre_serialize_probe_model_params
    probe_model_params = func_alias(serializable_rep)

    return probe_model_params



def _check_and_convert_cartesian_coords(params):
    module_alias = embeam.coherent
    func_alias = module_alias._check_and_convert_cartesian_coords
    cartesian_coords = func_alias(params)

    return cartesian_coords



def _check_and_convert_skip_validation_and_conversion(params):
    module_alias = embeam
    func_alias = module_alias._check_and_convert_skip_validation_and_conversion
    skip_validation_and_conversion = func_alias(params)

    return skip_validation_and_conversion



_module_alias = \
    embeam.coherent
_default_probe_model_params = \
    None
_default_k_x = \
    _module_alias._default_k_x
_default_k_y = \
    _module_alias._default_k_y
_default_skip_validation_and_conversion = \
    _module_alias._default_skip_validation_and_conversion



class Wavefunction(fancytypes.PreSerializableAndUpdatable):
    r"""The :math:`k`-space wavefunction of a coherent probe.

    The :math:`k`-space wavefunction of a coherent probe is well-described by
    the model given by
    Eq. :eq:`coherent_Phi_probe_in_stem_probe_model_params__1`. 

    See the documentation for the class :class:`embeam.stem.probe.ModelParams`
    for further discussion on probe modelling.

    Parameters
    ----------
    probe_model_params : :class:`embeam.stem.probe.ModelParams` | `None`, optional
        The model parameters of the coherent probe. If ``probe_model_params`` is
        set to ``None`` [i.e. the default value], then the parameter will be
        reassigned to the value ``embeam.stem.probe.ModelParams()``.
    skip_validation_and_conversion : `bool`, optional
        Let ``validation_and_conversion_funcs`` and ``core_attrs`` denote the
        attributes :attr:`~fancytypes.Checkable.validation_and_conversion_funcs`
        and :attr:`~fancytypes.Checkable.core_attrs` respectively, both of which
        being `dict` objects.

        Let ``params_to_be_mapped_to_core_attrs`` denote the `dict`
        representation of the constructor parameters excluding the parameter
        ``skip_validation_and_conversion``, where each `dict` key ``key`` is a
        different constructor parameter name, excluding the name
        ``"skip_validation_and_conversion"``, and
        ``params_to_be_mapped_to_core_attrs[key]`` would yield the value of the
        constructor parameter with the name given by ``key``.

        If ``skip_validation_and_conversion`` is set to ``False``, then for each
        key ``key`` in ``params_to_be_mapped_to_core_attrs``,
        ``core_attrs[key]`` is set to ``validation_and_conversion_funcs[key]
        (params_to_be_mapped_to_core_attrs)``.

        Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
        then ``core_attrs`` is set to
        ``params_to_be_mapped_to_core_attrs.copy()``. This option is desired
        primarily when the user wants to avoid potentially expensive deep copies
        and/or conversions of the `dict` values of
        ``params_to_be_mapped_to_core_attrs``, as it is guaranteed that no
        copies or conversions are made in this case.

    """
    ctor_param_names = ("probe_model_params",)
    kwargs = {"namespace_as_dict": globals(),
              "ctor_param_names": ctor_param_names}

    _validation_and_conversion_funcs_ = \
        {"probe_model_params": _check_and_convert_coherent_probe_model_params}
    _pre_serialization_funcs_ = \
        fancytypes.return_pre_serialization_funcs(**kwargs)
    _de_pre_serialization_funcs_ = \
        fancytypes.return_de_pre_serialization_funcs(**kwargs)

    del ctor_param_names, kwargs

    

    def __init__(self,
                 probe_model_params=\
                 _default_probe_model_params,
                 skip_validation_and_conversion=\
                 _default_skip_validation_and_conversion):
        ctor_params = {key: val
                       for key, val in locals().items()
                       if (key not in ("self", "__class__"))}
        kwargs = ctor_params
        kwargs["skip_cls_tests"] = True
        fancytypes.PreSerializableAndUpdatable.__init__(self, **kwargs)

        self.execute_post_core_attrs_update_actions()

        return None



    def execute_post_core_attrs_update_actions(self):
        self_core_attrs = self.get_core_attrs(deep_copy=False)

        probe_model_params = \
            self_core_attrs["probe_model_params"]
        probe_model_params_core_attrs = \
            probe_model_params.get_core_attrs(deep_copy=False)
        
        convergence_semiangle = \
            probe_model_params_core_attrs["convergence_semiangle"]
        lens_model_params = \
            probe_model_params_core_attrs["lens_model_params"]
        gun_model_params = \
            probe_model_params_core_attrs["gun_model_params"]

        lens_model_params_core_attrs = \
            lens_model_params.get_core_attrs(deep_copy=False)
        coherent_aberrations = \
            lens_model_params_core_attrs["coherent_aberrations"]

        gun_model_params_core_attrs = \
            gun_model_params.get_core_attrs(deep_copy=False)
        beam_energy = \
            gun_model_params_core_attrs["mean_beam_energy"]
        
        kwargs = {"beam_energy": beam_energy,
                  "coherent_aberrations": coherent_aberrations,
                  "defocal_offset": 0,
                  "skip_validation_and_conversion": True}
        phase_deviation = embeam.coherent.PhaseDeviation(**kwargs)

        del kwargs["coherent_aberrations"]
        del kwargs["defocal_offset"]
        wavelength = embeam.wavelength(**kwargs)
        
        self._k_xy_max = (convergence_semiangle / 1000) / wavelength
        self._C = 1 / np.sqrt(np.pi * self._k_xy_max**2)

        is_azimuthally_symmetric = phase_deviation.is_azimuthally_symmetric
        
        self._phase_deviation = phase_deviation
        self._is_azimuthally_symmetric = is_azimuthally_symmetric

        return None



    @classmethod
    def get_validation_and_conversion_funcs(cls):
        validation_and_conversion_funcs = \
            cls._validation_and_conversion_funcs_.copy()

        return validation_and_conversion_funcs


    
    @classmethod
    def get_pre_serialization_funcs(cls):
        pre_serialization_funcs = \
            cls._pre_serialization_funcs_.copy()

        return pre_serialization_funcs


    
    @classmethod
    def get_de_pre_serialization_funcs(cls):
        de_pre_serialization_funcs = \
            cls._de_pre_serialization_funcs_.copy()

        return de_pre_serialization_funcs



    def update(self,
               new_core_attr_subset_candidate,
               skip_validation_and_conversion=\
               _default_skip_validation_and_conversion):
        super().update(new_core_attr_subset_candidate,
                       skip_validation_and_conversion)
        self.execute_post_core_attrs_update_actions()

        return None



    def eval(self,
             k_x=\
             _default_k_x,
             k_y=\
             _default_k_y,
             skip_validation_and_conversion=\
             _default_skip_validation_and_conversion):
        r"""Evaluate the :math:`k`-space wavefunction of the coherent probe.

        This method evaluates
        Eq. :eq:`coherent_Phi_probe_in_stem_probe_model_params__1`.

        Parameters
        ----------
        k_x : `array_like` (`float`), optional
            The horizontal Fourier coordinates, in units of 1/Å, of the Fourier
            coordinate pairs at which to evaluate the wavefunction.
        k_y : `array_like` (`float`, shape=``k_x.shape``), optional
            The vertical Fourier coordinates, in units of 1/Å, of the Fourier
            coordinate pairs at which to evaluate the wavefunction.
        skip_validation_and_conversion : `bool`, optional
            If ``skip_validation_and_conversion`` is set to ``False``, then
            validations and conversions are performed on the above parameters.

            Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
            no validations and conversions are performed on the above
            parameters. This option is desired primarily when the user wants to
            avoid potentially expensive validation and/or conversion operations.

        Returns
        -------
        result : `array_like` (`complex`, shape=``k_x.shape``)
            The values of the wavefunction at the Fourier coordinate pairs
            specified by ``k_x`` and ``k_y``. For every tuple of nonnegative
            integers ``indices`` that does not raise an ``IndexError`` exception
            upon calling ``result[indices]``, ``result[indices]`` is the value
            of the wavefunction for the Fourier coordinate pair ``(k_x[indices],
            k_y[indices])``.

        """
        params = {key: val
                  for key, val in locals().items()
                  if (key not in ("self", "__class__"))}

        func_alias = _check_and_convert_skip_validation_and_conversion
        skip_validation_and_conversion = func_alias(params)

        if (skip_validation_and_conversion == False):
            params = {"cartesian_coords": (k_x, k_y), "units": "1/Å"}
            k_x, k_y = _check_and_convert_cartesian_coords(params)

        result = self._eval_with_heaviside(k_x, k_y)

        return result



    def _eval_with_heaviside(self, k_x, k_y):
        k_xy = np.sqrt(k_x*k_x + k_y*k_y)
        Theta = np.heaviside(self._k_xy_max - k_xy, 1)
        result = Theta * self._eval_without_heaviside(k_x, k_y)

        return result



    def _eval_without_heaviside(self, k_x, k_y):
        chi = self._phase_deviation._eval(k_x, k_y)
        result = self._C * np.exp(-1j * chi)

        return result



    @property
    def is_azimuthally_symmetric(self):
        r"""`bool`: A boolean variable indicating whether the probe model is 
        azimuthally symmetric.

        See the summary documentation of the classes
        :class:`embeam.coherent.PhaseDeviation`,
        :class:`embeam.coherent.Aberration`, and
        :class:`embeam.stem.probe.ModelParams` for additional context.

        A probe model is azimuthally symmetric if the coherent aberrations of
        the probe-forming lens are azimuthally symmetric, i.e. if if
        :math:`\sum_{m=0}^{\infty}\sum_{n=0}^{\infty} n
        \left(C_{m,n}^{\text{mag}} C_{m,n}^{\text{ang}}\right)^2=0`.

        Note that ``is_azimuthally_symmetric`` should be considered
        **read-only**.

        """
        result = self._is_azimuthally_symmetric
        
        return result



def _check_and_convert_probe_model_params(params):
    module_alias = embeam.stem.probe
    func_alias = module_alias._check_and_convert_probe_model_params
    probe_model_params = func_alias(params)

    return probe_model_params



class Intensity(fancytypes.PreSerializableAndUpdatable):
    r"""The :math:`k`-space fractional intensity of a probe.

    In scenarios where the fluctuations over time in the electron beam energy
    are either small or non-existent, the :math:`k`-space fractional intensity
    of the probe is well-described by
    Eq. :eq:`incoherent_k_space_p_probe_in_stem_probe_model_params__1`. 

    See the documentation for the class :class:`embeam.stem.probe.ModelParams`
    for further discussion on probe modelling.

    Parameters
    ----------
    probe_model_params : :class:`embeam.stem.probe.ModelParams` | `None`, optional
        The model parameters of the probe. If ``probe_model_params`` is set to
        ``None`` [i.e. the default value], then the parameter will be
        reassigned to the value ``embeam.stem.probe.ModelParams()``.
    skip_validation_and_conversion : `bool`, optional
        Let ``validation_and_conversion_funcs`` and ``core_attrs`` denote the
        attributes :attr:`~fancytypes.Checkable.validation_and_conversion_funcs`
        and :attr:`~fancytypes.Checkable.core_attrs` respectively, both of which
        being `dict` objects.

        Let ``params_to_be_mapped_to_core_attrs`` denote the `dict`
        representation of the constructor parameters excluding the parameter
        ``skip_validation_and_conversion``, where each `dict` key ``key`` is a
        different constructor parameter name, excluding the name
        ``"skip_validation_and_conversion"``, and
        ``params_to_be_mapped_to_core_attrs[key]`` would yield the value of the
        constructor parameter with the name given by ``key``.

        If ``skip_validation_and_conversion`` is set to ``False``, then for each
        key ``key`` in ``params_to_be_mapped_to_core_attrs``,
        ``core_attrs[key]`` is set to ``validation_and_conversion_funcs[key]
        (params_to_be_mapped_to_core_attrs)``.

        Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
        then ``core_attrs`` is set to
        ``params_to_be_mapped_to_core_attrs.copy()``. This option is desired
        primarily when the user wants to avoid potentially expensive deep copies
        and/or conversions of the `dict` values of
        ``params_to_be_mapped_to_core_attrs``, as it is guaranteed that no
        copies or conversions are made in this case.

    """
    ctor_param_names = ("probe_model_params",)
    kwargs = {"namespace_as_dict": globals(),
              "ctor_param_names": ctor_param_names}

    _validation_and_conversion_funcs_ = \
        fancytypes.return_validation_and_conversion_funcs(**kwargs)
    _pre_serialization_funcs_ = \
        fancytypes.return_pre_serialization_funcs(**kwargs)
    _de_pre_serialization_funcs_ = \
        fancytypes.return_de_pre_serialization_funcs(**kwargs)

    del ctor_param_names, kwargs

    

    def __init__(self,
                 probe_model_params=\
                 _default_probe_model_params,
                 skip_validation_and_conversion=\
                 _default_skip_validation_and_conversion):
        ctor_params = {key: val
                       for key, val in locals().items()
                       if (key not in ("self", "__class__"))}
        kwargs = ctor_params
        kwargs["skip_cls_tests"] = True
        fancytypes.PreSerializableAndUpdatable.__init__(self, **kwargs)

        self.execute_post_core_attrs_update_actions()

        return None



    def execute_post_core_attrs_update_actions(self):
        self_core_attrs = self.core_attrs
        probe_model_params = self_core_attrs["probe_model_params"]

        is_azimuthally_symmetric = probe_model_params.is_azimuthally_symmetric
        is_coherent = probe_model_params.is_coherent

        self._is_azimuthally_symmetric = is_azimuthally_symmetric
        self._is_coherent = is_coherent

        kwargs = self_core_attrs
        embeam.stem.probe._disable_chromatic_aberrations(**kwargs)

        kwargs["skip_validation_and_conversion"] = True
        self._kspace_wavefunction = Wavefunction(**kwargs)
        
        return None



    @classmethod
    def get_validation_and_conversion_funcs(cls):
        validation_and_conversion_funcs = \
            cls._validation_and_conversion_funcs_.copy()

        return validation_and_conversion_funcs


    
    @classmethod
    def get_pre_serialization_funcs(cls):
        pre_serialization_funcs = \
            cls._pre_serialization_funcs_.copy()

        return pre_serialization_funcs


    
    @classmethod
    def get_de_pre_serialization_funcs(cls):
        de_pre_serialization_funcs = \
            cls._de_pre_serialization_funcs_.copy()

        return de_pre_serialization_funcs



    def update(self,
               new_core_attr_subset_candidate,
               skip_validation_and_conversion=\
               _default_skip_validation_and_conversion):
        super().update(new_core_attr_subset_candidate,
                       skip_validation_and_conversion)
        self.execute_post_core_attrs_update_actions()

        return None



    def eval(self,
             k_x=\
             _default_k_x,
             k_y=\
             _default_k_y,
             skip_validation_and_conversion=\
             _default_skip_validation_and_conversion):
        r"""Evaluate the :math:`k`-space fractional intensity of the probe.

        This method evaluates
        Eq. :eq:`incoherent_k_space_p_probe_in_stem_probe_model_params__1`.

        Parameters
        ----------
        k_x : `array_like` (`float`), optional
            The horizontal Fourier coordinates, in units of 1/Å, of the Fourier
            coordinate pairs at which to evaluate the fractional intensity.
        k_y : `array_like` (`float`, shape=``k_x.shape``), optional
            The vertical Fourier coordinates, in units of 1/Å, of the Fourier
            coordinate pairs at which to evaluate the fractional intensity.
        skip_validation_and_conversion : `bool`, optional
            If ``skip_validation_and_conversion`` is set to ``False``, then
            validations and conversions are performed on the above parameters.

            Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
            no validations and conversions are performed on the above
            parameters. This option is desired primarily when the user wants to
            avoid potentially expensive validation and/or conversion operations.

        Returns
        -------
        result : `array_like` (`float`, shape=``k_x.shape``)
            The values of the fractional intensity at the Fourier coordinate
            pairs specified by ``k_x`` and ``k_y``. For every tuple of
            nonnegative integers ``indices`` that does not raise an
            ``IndexError`` exception upon calling ``result[indices]``,
            ``result[indices]`` is the value of the fractional intensity for the
            Fourier coordinate pair ``(k_x[indices], k_y[indices])``.

        """
        params = {key: val
                  for key, val in locals().items()
                  if (key not in ("self", "__class__"))}

        func_alias = _check_and_convert_skip_validation_and_conversion
        skip_validation_and_conversion = func_alias(params)

        if (skip_validation_and_conversion == False):
            params = {"cartesian_coords": (k_x, k_y), "units": "1/Å"}
            k_x, k_y = _check_and_convert_cartesian_coords(params)

        result = self._eval_with_heaviside(k_x, k_y)

        return result



    def _eval_with_heaviside(self, k_x, k_y):
        kspace_wavefunction = self._kspace_wavefunction
        temp = np.abs(kspace_wavefunction._eval_with_heaviside(k_x, k_y))
        result = temp * temp
        
        return result



    @property
    def is_azimuthally_symmetric(self):
        r"""`bool`: A boolean variable indicating whether the probe model is 
        azimuthally symmetric.

        See the summary documentation of the classes
        :class:`embeam.coherent.PhaseDeviation`,
        :class:`embeam.coherent.Aberration`, and
        :class:`embeam.stem.probe.ModelParams` for additional context.

        A probe model is azimuthally symmetric if the coherent aberrations of
        the probe-forming lens are azimuthally symmetric, i.e. if if
        :math:`\sum_{m=0}^{\infty}\sum_{n=0}^{\infty} n
        \left(C_{m,n}^{\text{mag}} C_{m,n}^{\text{ang}}\right)^2=0`.

        Note that ``is_azimuthally_symmetric`` should be considered
        **read-only**.

        """
        result = self._is_azimuthally_symmetric
        
        return result



    @property
    def is_coherent(self):
        r"""`bool`: A boolean variable indicating whether the probe model is 
        coherent.

        See the summary documentation of the class
        :class:`embeam.stem.probe.ModelParams` for additional context.

        If ``is_coherent`` is set to ``True``, then the probe model is
        coherent. Otherwise, the probe model is not coherent.

        Note that ``is_coherent`` should be considered **read-only**.

        """
        result = self._is_coherent
        
        return result



###########################
## Define error messages ##
###########################
