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
"""For modelling coherent lens aberrations and phase deviations.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For general array handling.
import numpy as np

# For validating and converting objects.
import czekitout.check
import czekitout.convert

# For defining classes that support enforced validation, updatability,
# pre-serialization, and de-serialization.
import fancytypes



# For calculating electron beam wavelengths.
import embeam



##################################
## Define classes and functions ##
##################################

# List of public objects in package.
__all__ = ["Aberration",
           "PhaseDeviation"]



def _check_and_convert_m(params):
    obj_name = "m"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    m = czekitout.convert.to_nonnegative_int(**kwargs)

    return m



def _pre_serialize_m(m):
    obj_to_pre_serialize = m
    serializable_rep = obj_to_pre_serialize
    
    return serializable_rep



def _de_pre_serialize_m(serializable_rep):
    m = serializable_rep

    return m



def _check_and_convert_n(params):
    obj_name = "n"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    n = czekitout.convert.to_nonnegative_int(**kwargs)

    return n



def _pre_serialize_n(n):
    obj_to_pre_serialize = n
    serializable_rep = obj_to_pre_serialize
    
    return serializable_rep



def _de_pre_serialize_n(serializable_rep):
    n = serializable_rep

    return n



def _check_and_convert_C_mag(params):
    obj_name = "C_mag"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    C_mag = czekitout.convert.to_float(**kwargs)

    return C_mag



def _pre_serialize_C_mag(C_mag):
    obj_to_pre_serialize = C_mag
    serializable_rep = obj_to_pre_serialize
    
    return serializable_rep



def _de_pre_serialize_C_mag(serializable_rep):
    C_mag = serializable_rep

    return C_mag



def _check_and_convert_C_ang(params):
    obj_name = "C_ang"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    C_ang = czekitout.convert.to_float(**kwargs)

    return C_ang



def _pre_serialize_C_ang(C_ang):
    obj_to_pre_serialize = C_ang
    serializable_rep = obj_to_pre_serialize
    
    return serializable_rep



def _de_pre_serialize_C_ang(serializable_rep):
    C_ang = serializable_rep

    return C_ang



_module_alias = \
    embeam.gun
_default_m = \
    0
_default_n = \
    0
_default_C_mag = \
    0
_default_C_ang = \
    0
_default_skip_validation_and_conversion = \
    _module_alias._default_skip_validation_and_conversion



class Aberration(fancytypes.PreSerializableAndUpdatable):
    r"""A coherent lens aberration.

    As discussed in greater detail in e.g. Ref. [Kirkland1]_, an important
    quantity that characterizes how coherent lens aberrations affect an electron
    beam is the phase deviation:

    .. math ::
        \chi\left(k_{x},k_{y};\delta_f\right)&=\sum_{m=0}^{\infty}
        \sum_{n=0}^{\infty}\left(\lambda k_{xy}\right)^{m}
        \left(C_{m,n}^{\text{mag}}
        +\delta_{m,2}\delta_{n,0}\pi\delta_f/\lambda\right)\\
        &\hphantom{=\sum_{m=0}^{\infty}\sum_{n=0}^{\infty}}\mathop{\times}
        \left\{ \cos\left[nC_{m,n}^{\text{ang}}\right]\cos\left[n
        \text{atan2}\left(k_{x},k_{y}\right)\right]\right.\\
        &\hphantom{=\sum_{m=0}^{\infty}\sum_{n=0}^{\infty}\mathop{\times}\quad}
        \left.\mathop{+}\sin\left[nC_{m,n}^{\text{ang}}\right]\sin\left[n
        \text{atan2}\left(k_{x},k_{y}\right)\right]\right\},
        :label: chi_in_coherent_aberration__1

    where :math:`k_{x}` and :math:`k_{y}` are the Fourier coordinates; 

    .. math ::
        k_{xy}=\sqrt{k_{x}^{2}+k_{y}^{2}};
        :label: k_xy_in_coherent_aberration__1

    .. math ::
        k_{xy,\max}=\frac{\alpha_{\max}}{\lambda},
        :label: k_xy_max_in_coherent_aberration__1

    with :math:`\alpha_{\max}` being the convergence semiangle, and
    :math:`\lambda` being the electron beam wavelength [given by
    Eq. :eq:`electron_beam_wavelength__1`]; :math:`C_{m,n}^{\text{mag}}` and
    :math:`C_{m,n}^{\text{ang}}` are dimensionless coefficients describing the
    magnitude and azimuthal phase of an aberration of radial order :math:`m` and
    azimuthal order :math:`n`; :math:`\delta_f` is an offset to
    :math:`C_{2,0}^{\text{mag}}`, expressed in units of length; and atan2 is the
    2-argument arctangent function which returns the polar angle of
    :math:`\left(k_{x},k_{y}\right)` in the correct quadrant. Note that
    :math:`m` and :math:`n` are integers, whereas :math:`C_{m,n}^{\text{mag}}`
    and :math:`C_{m,n}^{\text{ang}}` are real numbers.

    The quantity :math:`\delta_f` was introduced to conveniently describe
    temporally incoherent beams. We refer to this quantity as the "defocal
    offset" throughout the documentation.

    Parameters
    ----------
    m : `int`, optional
        The radial order of the aberration, :math:`m`. Must be non-negative.
    n : `int`, optional
        The azimuthal order of the aberration, :math:`n`. Must be non-negative.
    C_mag : `float`, optional
        The dimensionless coefficient :math:`C_{m,n}^{\text{mag}}`.
    C_ang : `float`, optional
        The dimensionless coefficient :math:`C_{m,n}^{\text{ang}}`.
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
    ctor_param_names = ("m",
                        "n",
                        "C_mag",
                        "C_ang")
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
                 m=\
                 _default_m,
                 n=\
                 _default_n,
                 C_mag=\
                 _default_C_mag,
                 C_ang=\
                 _default_C_ang,
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
        self._update_is_azimuthally_symmetric()

        return None



    def _update_is_azimuthally_symmetric(self):
        self_core_attrs = self.get_core_attrs(deep_copy=False)

        n = self_core_attrs["n"]
        C_mag = self_core_attrs["C_mag"]
        C_ang = self_core_attrs["C_ang"]
        self._is_azimuthally_symmetric = (n*C_mag*C_ang == 0)

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



    @property
    def is_azimuthally_symmetric(self):
        r"""`bool`: A boolean variable indicating whether the aberration is
        azimuthally symmetric.

        See the summary documentation of the class
        :class:`embeam.coherent.Aberration` for additional context.

        A coherent aberration is azimuthally symmetric if :math:`n
        C_{m,n}^{\text{mag}} C_{m,n}^{\text{ang}} = 0`.

        If ``is_azimuthally_symmetric`` is set to ``True``, then the aberration
        is azimuthally symmetric. Otherwise, the aberration is not azimuthally
        symmetric.

        Note that ``is_azimuthally_symmetric`` should be considered
        **read-only**.

        """
        result = self._is_azimuthally_symmetric
        
        return result



def _check_and_convert_beam_energy(params):
    module_alias = embeam
    func_alias = module_alias._check_and_convert_beam_energy
    beam_energy = func_alias(params)

    return beam_energy



def _pre_serialize_beam_energy(beam_energy):
    obj_to_pre_serialize = beam_energy
    serializable_rep = obj_to_pre_serialize
    
    return serializable_rep



def _de_pre_serialize_beam_energy(serializable_rep):
    beam_energy = serializable_rep

    return beam_energy



def _check_and_convert_coherent_aberrations(params):
    obj_name = "coherent_aberrations"
    obj = params[obj_name]

    current_func_name = "_check_and_convert_coherent_aberrations"

    try:
        coherent_aberrations = tuple()
        mn_pairs = tuple()

        for coherent_aberration in obj:
            accepted_types = (Aberration,)
    
            kwargs = {"obj": coherent_aberration,
                      "obj_name": "coherent_aberration",
                      "accepted_types": accepted_types}
            czekitout.check.if_instance_of_any_accepted_types(**kwargs)

            kwargs = coherent_aberration.get_core_attrs(deep_copy=False)
            coherent_aberration = accepted_types[0](**kwargs)

            coherent_aberration_core_attrs = \
                coherent_aberration.get_core_attrs(deep_copy=False)

            mn_pair = (coherent_aberration_core_attrs["m"],
                       coherent_aberration_core_attrs["n"])

            if mn_pair in mn_pairs:
                unformatted_err_msg = globals()[current_func_name+"_err_msg_1"]
                err_msg = unformatted_err_msg.format(*mn_pair)
                raise ValueError(err_msg)
            
            mn_pairs += (mn_pair,)
            coherent_aberrations += (coherent_aberration,)
    except:
        err_msg = globals()[current_func_name+"_err_msg_2"]
        raise ValueError(err_msg)

    return coherent_aberrations



def _pre_serialize_coherent_aberrations(coherent_aberrations):
    obj_to_pre_serialize = coherent_aberrations

    serializable_rep = tuple()
    for elem_of_obj_to_pre_serialize in obj_to_pre_serialize:
        serializable_rep += (elem_of_obj_to_pre_serialize.pre_serialize(),)
    
    return serializable_rep



def _de_pre_serialize_coherent_aberrations(serializable_rep):
    coherent_aberrations = \
        tuple()
    for elem_of_serializable_rep in serializable_rep:
        coherent_aberrations += \
            (Aberration.de_pre_serialize(elem_of_serializable_rep),)

    return coherent_aberrations



def _check_and_convert_defocal_offset(params):
    obj_name = "defocal_offset"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    defocal_offset = czekitout.convert.to_float(**kwargs)

    return defocal_offset



def _pre_serialize_defocal_offset(defocal_offset):
    obj_to_pre_serialize = defocal_offset
    serializable_rep = obj_to_pre_serialize
    
    return serializable_rep



def _de_pre_serialize_defocal_offset(serializable_rep):
    defocal_offset = serializable_rep

    return defocal_offset



def _check_and_convert_skip_validation_and_conversion(params):
    module_alias = embeam
    func_alias = module_alias._check_and_convert_skip_validation_and_conversion
    skip_validation_and_conversion = func_alias(params)

    return skip_validation_and_conversion



def _check_and_convert_cartesian_coords(params):
    units = params["units"]

    obj_name = "cartesian_coords"
    obj = params[obj_name]

    if units == "Å":
        x, y = obj

        params["real_numpy_array"] = x
        params["name_of_alias_of_real_numpy_array"] = "x"
        x = _check_and_convert_real_numpy_array(params)

        params["real_numpy_array"] = y
        params["name_of_alias_of_real_numpy_array"] = "y"
        y = _check_and_convert_real_numpy_array(params)

        cartesian_coords = (x, y)
    else:
        k_x, k_y = obj

        params["real_numpy_array"] = k_x
        params["name_of_alias_of_real_numpy_array"] = "k_x"
        k_x = _check_and_convert_real_numpy_array(params)

        params["real_numpy_array"] = k_y
        params["name_of_alias_of_real_numpy_array"] = "k_y"
        k_y = _check_and_convert_real_numpy_array(params)

        cartesian_coords = (k_x, k_y)

    del params["real_numpy_array"]
    del params["name_of_alias_of_real_numpy_array"]

    current_func_name = "_check_and_convert_cartesian_coords"

    if cartesian_coords[0].shape != cartesian_coords[1].shape:
        unformatted_err_msg = globals()[current_func_name+"_err_msg_1"]
        args = ("x", "y") if (units == "Å") else ("k_x", "k_y")
        err_msg = unformatted_err_msg.format(*args)
        raise ValueError(err_msg)

    return cartesian_coords



def _check_and_convert_real_numpy_array(params):
    obj_name = "real_numpy_array"
    obj = params[obj_name]
    
    name_of_alias_of_real_numpy_array = \
        params["name_of_alias_of_real_numpy_array"]

    current_func_name = "_check_and_convert_real_numpy_array"

    try:
        kwargs = {"obj": obj,
                  "obj_name": name_of_alias_of_real_numpy_array}
        real_numpy_array = czekitout.convert.to_real_numpy_array(**kwargs)
    except:
        unformatted_err_msg = globals()[current_func_name+"_err_msg_1"]
        err_msg = unformatted_err_msg.format(name_of_alias_of_real_numpy_array)
        raise TypeError(err_msg)

    return real_numpy_array



_module_alias = embeam.gun
_default_beam_energy = _module_alias._default_mean_beam_energy
_default_coherent_aberrations = tuple()
_default_defocal_offset = 0
_default_k_x = np.zeros((1, 1))
_default_k_y = np.zeros((1, 1))



class PhaseDeviation(fancytypes.PreSerializableAndUpdatable):
    r"""The phase deviation due to a set of coherent lens aberrations.

    The phase deviation :math:`\chi\left(k_{x},k_{y}; \delta_f \right)` is
    defined in Eq. :eq:`chi_in_coherent_aberration__1`.

    Parameters
    ----------
    beam_energy : `float`, optional
        The electron beam energy :math:`E` in units of keV. Must be positive.
    coherent_aberrations : `array_like` (:class:`embeam.coherent.Aberration`, ndim=1), optional
        The set of coherent lens aberrations. No coherent lens aberration should
        be specified more than once.
    defocal_offset : `float`, optional
        The defocal offset :math:`\delta_f`, in units of Å.
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
    ctor_param_names = ("beam_energy",
                        "coherent_aberrations",
                        "defocal_offset")
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
                 beam_energy=\
                 _default_beam_energy,
                 coherent_aberrations=\
                 _default_coherent_aberrations,
                 defocal_offset=\
                 _default_defocal_offset,
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

        self._update_is_azimuthally_symmetric()
        self._update_wavelength()
        self._update_coherent_aberrations_as_matrix()
        self._update_eval_implementation()
        self._delta_f = self_core_attrs["defocal_offset"]

        return None



    def _update_is_azimuthally_symmetric(self):
        self_core_attrs = self.get_core_attrs(deep_copy=False)
        
        coherent_aberrations = self_core_attrs["coherent_aberrations"]
        
        is_azimuthally_symmetric = \
            True
        for coherent_aberration in coherent_aberrations:
            is_azimuthally_symmetric = \
                (is_azimuthally_symmetric
                 and coherent_aberration.is_azimuthally_symmetric)
            
        self._is_azimuthally_symmetric = is_azimuthally_symmetric

        return None



    def _update_wavelength(self):
        self_core_attrs = self.get_core_attrs(deep_copy=False)

        beam_energy = self_core_attrs["beam_energy"]
        self._wavelength = embeam._wavelength(beam_energy)

        return None



    def _update_coherent_aberrations_as_matrix(self):
        self_core_attrs = self.get_core_attrs(deep_copy=False)

        coherent_aberrations = self_core_attrs["coherent_aberrations"]
        
        self._coherent_aberrations_as_matrix = \
            tuple()
        for coherent_aberration in coherent_aberrations:
            coherent_aberration_core_attrs = \
                coherent_aberration.get_core_attrs(deep_copy=False)
            m = \
                coherent_aberration_core_attrs["m"]
            n = \
                coherent_aberration_core_attrs["n"]
            C_mag = \
                coherent_aberration_core_attrs["C_mag"]
            C_ang = \
                coherent_aberration_core_attrs["C_ang"]
            
            self._coherent_aberrations_as_matrix += ((m, n, C_mag, C_ang),)

        return None



    def _update_eval_implementation(self):
        if self._is_azimuthally_symmetric:
            self._eval = self._eval_for_azimuthally_symmetric_case
        else:
            self._eval = self._eval_for_azimuthally_asymmetric_case

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
        r"""Evaluate the phase deviation.

        This method evaluates Eq. :eq:`chi_in_coherent_aberration__1`.

        Parameters
        ----------
        k_x : `array_like` (`float`), optional
            The horizontal Fourier coordinates, in units of 1/Å, of the Fourier
            coordinate pairs at which to evaluate the phase deviation.
        k_y : `array_like` (`float`, shape=``k_x.shape``), optional
            The vertical Fourier coordinates, in units of 1/Å, of the Fourier
            coordinate pairs at which to evaluate the phase deviation.
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
            The values of the phase deviation at the Fourier coordinate pairs
            specified by ``k_x`` and ``k_y``. For every tuple of nonnegative
            integers ``indices`` that does not raise an ``IndexError`` exception
            upon calling ``result[indices]``, ``result[indices]`` is the value
            of the phase deviation for the Fourier coordinate pair
            ``(k_x[indices], k_y[indices])``.

        """
        params = {key: val
                  for key, val in locals().items()
                  if (key not in ("self", "__class__"))}

        func_alias = _check_and_convert_skip_validation_and_conversion
        skip_validation_and_conversion = func_alias(params)

        if (skip_validation_and_conversion == False):
            params = {"cartesian_coords": (k_x, k_y), "units": "1/Å"}
            k_x, k_y = _check_and_convert_cartesian_coords(params)

        result = self._eval(k_x, k_y)

        return result



    def _eval_for_azimuthally_symmetric_case(self, k_x, k_y):
        k_xy = np.sqrt(k_x*k_x + k_y*k_y)
        lambda_k_xy = self._wavelength * k_xy
        wavelength = self._wavelength
        delta_f = self._delta_f

        result = 0
        for m, n, C_mag, C_ang in self._coherent_aberrations_as_matrix:
            temp = np.ones(lambda_k_xy.shape)
            for _ in range(m):
                temp *= lambda_k_xy                
            result += temp * C_mag
        result += np.pi * lambda_k_xy * lambda_k_xy * delta_f / wavelength

        return result



    def _eval_for_azimuthally_asymmetric_case(self, k_x, k_y):
        k_xy = np.sqrt(k_x*k_x + k_y*k_y)
        lambda_k_xy = self._wavelength * k_xy
        arctan2_ky_kx = np.arctan2(k_y, k_x)
        wavelength = self._wavelength
        delta_f = self._delta_f

        result = 0
        for m, n, C_mag, C_ang in self._coherent_aberrations_as_matrix:
            temp = np.ones(lambda_k_xy.shape)
            for _ in range(m):
                temp *= lambda_k_xy

            result += (temp * C_mag
                       * (np.cos(n*C_ang) * np.cos(n*arctan2_ky_kx) 
                          + np.sin(n*C_ang) * np.sin(n*arctan2_ky_kx)))

        result += np.pi * lambda_k_xy * lambda_k_xy * delta_f / wavelength

        return result



    @property
    def is_azimuthally_symmetric(self):
        r"""`bool`: A boolean variable indicating whether the phase deviation is
        azimuthally symmetric.

        See the summary documentation of the class
        :class:`embeam.coherent.PhaseDeviation` for additional context.

        A phase deviation is azimuthally symmetric if
        :math:`\sum_{m=0}^{\infty}\sum_{n=0}^{\infty} n
        \left(C_{m,n}^{\text{mag}} C_{m,n}^{\text{ang}}\right)^2=0`.

        If ``is_azimuthally_symmetric`` is set to ``True``, then the phase
        deviation is azimuthally symmetric. Otherwise, the phase deviation is
        not azimuthally symmetric.

        Note that ``is_azimuthally_symmetric`` should be considered
        **read-only**.

        """
        result = self._is_azimuthally_symmetric
        
        return result



###########################
## Define error messages ##
###########################

_check_and_convert_coherent_aberrations_err_msg_1 = \
    ("The object ``coherent_aberrations`` specifies a coherent lens aberration "
     "of radial order {} and azimuthal order {} at least more than once. No "
     "coherent lens aberration should be specified more than once.")
_check_and_convert_coherent_aberrations_err_msg_2 = \
    ("The object ``coherent_aberrations`` must specify a sequence of instances "
     "of the class `embeam.coherent.Aberration`, where each instance specifies "
     "a coherent lens aberration. Moreover, for each specified coherent lens "
     "aberration, the pair formed by its radial order and azimuthal order must "
     "be unique.")

_check_and_convert_cartesian_coords_err_msg_1 = \
    ("The objects ``{}`` and ``{}`` must be real-valued arrays of the same "
     "shape.")

_check_and_convert_real_numpy_array_err_msg_1 = \
    ("The object ``{}`` must be a real-valued number or array.")
