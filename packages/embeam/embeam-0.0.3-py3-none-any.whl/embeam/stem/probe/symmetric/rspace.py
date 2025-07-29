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
r"""Contains classes representing real-space functions of probes that are
azimuthally symmetric.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For using special math functions and constants.
import numpy as np

# For special math functions and numerical integration.
import scipy.integrate
import scipy.special

# For defining classes that support enforced validation, updatability,
# pre-serialization, and de-serialization.
import fancytypes



# For calculating the electron beam wavelength; validating, pre-serializing, and
# de-pre-serializing instances of :class:`embeam.stem.probe.ModelParams`;
# extracting parameters from the probe model parameters; constructing instances
# of :class:`embeam.stem.probe.kspace.Wavefunction`; and temporarily disabling
# chromatic aberrations.
import embeam



##################################
## Define classes and functions ##
##################################

# List of public objects in objects.
__all__ = ["Wavefunction",
           "Intensity"]



def _check_and_convert_symmetric_coherent_probe_model_params(params):
    module_alias = \
        embeam.stem.probe
    func_alias = \
        module_alias._check_and_convert_symmetric_coherent_probe_model_params
    probe_model_params = \
        func_alias(params)

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
_default_x = \
    _module_alias._default_k_x
_default_y = \
    _module_alias._default_k_y
_default_skip_validation_and_conversion = \
    _module_alias._default_skip_validation_and_conversion



class Wavefunction(fancytypes.PreSerializableAndUpdatable):
    r"""The real-space wavefunction of an azimuthally symmetric and coherent 
    probe.

    The real-space wavefunction of a coherent probe is well-described by the
    model given by Eq. :eq:`coherent_psi_probe_in_stem_probe_model_params__1`.
    If the coherent probe is also azimuthally symmetric, then the
    right-hand-side of
    Eq. :eq:`coherent_psi_probe_in_stem_probe_model_params__1` simplifies to:

    .. math ::
        \psi_{\text{probe}}^{\text{symmetric}}\left(x,y;\delta_{f}\right)
        =\left(2\pi\right)
        \int_{0}^{k_{xy,\max}}dk_{xy}\,k_{xy}\Phi_{\text{probe}}\left(k_{xy},0;
        \delta_{f}\right)J_{0}\left(2\pi k_{xy}r_{xy}\right),
        :label: coherent_psi_probe_in_stem_probe_symmetric_rspace__1

    where :math:`x` and :math:`y` are the real-space coordinates; 

    .. math ::
        r_{xy}=\sqrt{x^{2}+y^{2}};
        :label: r_xy__1

    .. math ::
        k_{xy,\max}=\frac{\alpha_{\max}}{\lambda},
        :label: k_xy_max__10

    with :math:`\alpha_{\max}` being the convergence semiangle, and
    :math:`\lambda` being the electron beam wavelength; :math:`\delta_f` is the
    defocal offset; :math:`\Phi_{\text{probe}}\left(k_{xy},0;\delta_f\right)` is
    the :math:`k`-space wavefunction, given by
    Eq. :eq:`coherent_Phi_probe_in_stem_probe_model_params__1`; and
    :math:`J_{0}\left(u\right)` is the zeroth order Bessel function of the first
    kind.

    See the documentation for the class :class:`embeam.stem.probe.ModelParams`
    for further discussion on probe modelling.

    Parameters
    ----------
    probe_model_params : :class:`embeam.stem.probe.ModelParams` | `None`, optional
        The model parameters of the coherent probe. If ``probe_model_params`` is
        set to ``None`` [i.e. the default value], then the parameter will be
        reassigned to the value ``embeam.stem.probe.ModelParams()``. An
        exception is raised if the model parameters specify a probe that is
        either incoherent or azimuthally asymmetric.
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
        {"probe_model_params": \
         _check_and_convert_symmetric_coherent_probe_model_params}
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
        kwargs = \
            self.get_core_attrs(deep_copy=False)
        kwargs["skip_validation_and_conversion"] = \
            True
        self._kspace_wavefunction = \
            embeam.stem.probe.kspace.Wavefunction(**kwargs)

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
             x=\
             _default_x,
             y=\
             _default_y,
             skip_validation_and_conversion=\
             _default_skip_validation_and_conversion):
        r"""Evaluate the real-space wavefunction of the azimuthally symmetric 
        and coherent probe.

        This method evaluates
        Eq. :eq:`coherent_psi_probe_in_stem_probe_symmetric_rspace__1`.

        Parameters
        ----------
        x : `array_like` (`float`), optional
            The horizontal real-space coordinates, in units of Å, of the
            real-space coordinate pairs at which to evaluate the wavefunction.
        y : `array_like` (`float`, shape=``x.shape``), optional
            The vertical real-space coordinates, in units of Å, of the
            real-space coordinate pairs at which to evaluate the wavefunction.
        skip_validation_and_conversion : `bool`, optional
            If ``skip_validation_and_conversion`` is set to ``False``, then
            validations and conversions are performed on the above parameters.

            Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
            no validations and conversions are performed on the above
            parameters. This option is desired primarily when the user wants to
            avoid potentially expensive validation and/or conversion operations.

        Returns
        -------
        result : `array_like` (`complex`, shape=``x.shape``)
            The values of the wavefunction at the real-space coordinate pairs
            specified by ``x`` and ``y``. For every tuple of nonnegative
            integers ``indices`` that does not raise an ``IndexError`` exception
            upon calling ``result[indices]``, ``result[indices]`` is the value
            of the wavefunction for the real-space coordinate pair
            ``(x[indices], y[indices])``.

        """
        params = {key: val
                  for key, val in locals().items()
                  if (key not in ("self", "__class__"))}

        func_alias = _check_and_convert_skip_validation_and_conversion
        skip_validation_and_conversion = func_alias(params)

        if (skip_validation_and_conversion == False):
            params = {"cartesian_coords": (x, y), "units": "Å"}
            x, y = _check_and_convert_cartesian_coords(params)

        result = self._eval(x, y)

        return result



    def _eval(self, x, y):
        r_xy = np.sqrt(x*x + y*y)
        k_xy_max = self._kspace_wavefunction._k_xy_max

        result = np.zeros_like(x, dtype=complex)
        
        result_shape = result.shape
        num_coord_pairs = int(np.prod(result_shape))

        for coord_pair_idx in range(num_coord_pairs):
            array_indices = np.unravel_index(coord_pair_idx, result_shape)
            
            r_xy_elem = r_xy[array_indices]
            
            N_max = self._max_num_integration_subintervals(r_xy_elem)

            integrand_1d = (lambda k_xy_elem:
                            self._integrand_real_part(r_xy_elem, k_xy_elem))
            real_part = scipy.integrate.quad(integrand_1d, 
                                             a=0, 
                                             b=k_xy_max, 
                                             limit=N_max)[0]

            integrand_1d = (lambda k_xy_elem:
                            self._integrand_imag_part(r_xy_elem, k_xy_elem))
            imag_part = scipy.integrate.quad(integrand_1d, 
                                             a=0, 
                                             b=k_xy_max, 
                                             limit=N_max)[0]
        
            result[array_indices] = real_part + 1j*imag_part

        return result



    def _max_num_integration_subintervals(self, r_xy_elem):
        k_xy_max = self._kspace_wavefunction._k_xy_max
        phase_deviation = self._kspace_wavefunction._phase_deviation
        N = 50

        kwargs = {"k_x": k_xy_max, "k_y": 0}
        temp = N*np.ceil(phase_deviation._eval(**kwargs)/2/np.pi)
        
        max_num_integration_subintervals = \
            N*np.ceil(k_xy_max*r_xy_elem)
        max_num_integration_subintervals = \
            np.maximum(max_num_integration_subintervals, temp)
        max_num_integration_subintervals = \
            np.maximum(max_num_integration_subintervals, N).astype(int)
        
        return max_num_integration_subintervals



    def _integrand_real_part(self, r_xy_elem, k_xy_elem):
        result = np.real(self._integrand(r_xy_elem, k_xy_elem))
    
        return result
    
    
    
    def _integrand_imag_part(self, r_xy_elem, k_xy_elem):
        result = np.imag(self._integrand(r_xy_elem, k_xy_elem))
    
        return result



    def _integrand(self, r_xy_elem, k_xy_elem):
        kwargs = {"k_x": k_xy_elem, "k_y": 0}
        result = ((2*np.pi) * k_xy_elem
                  * self._kspace_wavefunction._eval_with_heaviside(**kwargs)
                  * scipy.special.jv(0, 2*np.pi*k_xy_elem*r_xy_elem))
    
        return result



def _check_and_convert_symmetric_probe_model_params(params):
    module_alias = embeam.stem.probe
    func_alias = module_alias._check_and_convert_symmetric_probe_model_params
    probe_model_params = func_alias(params)

    return probe_model_params



class Intensity(fancytypes.PreSerializableAndUpdatable):
    r"""The real-space fractional intensity of an azimuthally symmetric probe.

    In scenarios where the fluctuations over time in the electron beam energy
    are either small or non-existent, the real-space fractional intensity of the
    probe is well-described by
    Eq. :eq:`incoherent_r_space_p_probe_in_stem_probe_model_params__2`. If the
    probe is also azimuthally symmetric, then the right-hand-side of
    Eq. :eq:`incoherent_r_space_p_probe_in_stem_probe_model_params__2`
    simplifies to:

    .. math ::
        p_{\text{probe}}^{\text{symmetric}}\left(\left.X=x\right|Y=y\right)
        \approx\frac{1}{\sqrt{\pi}}\sum_{l=1}^{N_{f}}w_{f;l}
        p_{\text{probe}}^{\text{symmetric}}\left(\left.X=x\right|Y=y;
        \delta_{f}=\sqrt{2}\sigma_{f}x_{f;l}\right),
        :label: symmetric_r_space_p_probe_in_stem_probe_symmetric_rspace__1

    where the :math:`w_{f;l}` are given by Eq
    :eq:`normalized_gauss_hermite_weights_in_stem_probe_model_params__1`;
    :math:`N_{f}` is the number of points used in the Gauss-Hermite quadrature
    scheme of
    Eq. :eq:`incoherent_r_space_p_probe_in_stem_probe_model_params__2`;
    :math:`\sigma_{f}` is given by
    Eq. :eq:`sigma_f_in_stem_probe_model_params__1`; :math:`x_{f;l}` is the
    :math:`l^{\text{th}}` root of the Physicists' version of the
    :math:`N_{f}^{\text{th}}` Hermite polynomial
    :math:`H_{N_{f}}\left(x\right)`; and

    .. math ::
        p_{\text{probe}}^{\text{symmetric}}\left(\left.X=x\right|Y=y;
        \delta_{f}=\sqrt{2}\sigma_{f}x_{f;l}\right)
        =\left|\psi_{\text{probe}}^{\text{symmetric}}\left(x,y;
        \delta_{f}=\sqrt{2}\sigma_{f}x_{f;l}\right)\right|^{2},
        :label: symmetric_coherent_r_space_p_probe_in_stem_probe_symmetric_rspace__1

    with
    :math:`\psi_{\text{probe}}^{\text{symmetric}}\left(x,y;\delta_{f}=\sqrt{2}
    \sigma_{f}x_{f;l}\right)` being given by
    Eq. :eq:`coherent_psi_probe_in_stem_probe_symmetric_rspace__1`.

    See the documentation for the class :class:`embeam.stem.probe.ModelParams`
    for further discussion on probe modelling.

    Parameters
    ----------
    probe_model_params : :class:`embeam.stem.probe.ModelParams` | `None`, optional
        The model parameters of the probe. If ``probe_model_params`` is set to
        ``None`` [i.e. the default value], then the parameter will be reassigned
        to the value ``embeam.stem.probe.ModelParams()``. An exception is raised
        if the probe model specified is not azimuthally symmetric.
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
        {"probe_model_params": _check_and_convert_symmetric_probe_model_params}
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
        
        is_coherent = probe_model_params.is_coherent
        self._is_coherent = is_coherent
        
        func_alias = embeam.stem.probe._get_C_2_0_mag_from_probe_model_params
        kwargs = self_core_attrs
        old_C_2_0_mag = func_alias(**kwargs)

        sigma_f = probe_model_params._sigma_f
        gauss_hermite_points = probe_model_params._gauss_hermite_points
        self._gauss_hermite_weights = probe_model_params._gauss_hermite_weights

        probe_model_params_core_attrs = \
            probe_model_params.get_core_attrs(deep_copy=False)
        gun_model_params = \
            probe_model_params_core_attrs["gun_model_params"]

        gun_model_params_core_attrs = \
            gun_model_params.get_core_attrs(deep_copy=False)
        beam_energy = \
            gun_model_params.core_attrs["mean_beam_energy"]
        
        wavelength = embeam.wavelength(beam_energy)

        embeam.stem.probe._disable_chromatic_aberrations(**kwargs)

        self._rspace_wavefunctions = tuple()
        for x_f_l in gauss_hermite_points:
            delta_f = np.sqrt(2)*sigma_f*x_f_l
            new_C_2_0_mag = old_C_2_0_mag + np.pi*delta_f/wavelength
            
            module_alias = embeam.stem.probe
            func_alias = module_alias._update_C_2_0_mag_in_probe_model_params
            kwargs["C_2_0_mag"] = new_C_2_0_mag
            func_alias(**kwargs)
            
            rspace_wavefunction = Wavefunction(probe_model_params)
            self._rspace_wavefunctions += (rspace_wavefunction,)
        
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
             x=\
             _default_x,
             y=\
             _default_y,
             skip_validation_and_conversion=\
             _default_skip_validation_and_conversion):
        r"""Evaluate the real-space fractional intensity of the azimuthally 
        symmetric probe.

        This method evaluates
        Eq. :eq:`symmetric_r_space_p_probe_in_stem_probe_symmetric_rspace__1`.

        Parameters
        ----------
        x : `array_like` (`float`), optional
            The horizontal real-space coordinates, in units of Å, of the
            real-space coordinate pairs at which to evaluate the fractional
            intensity.
        y : `array_like` (`float`, shape=``x.shape``), optional
            The vertical real-space coordinates, in units of Å, of the
            real-space coordinate pairs at which to evaluate the fractional
            intensity.
        skip_validation_and_conversion : `bool`, optional
            If ``skip_validation_and_conversion`` is set to ``False``, then
            validations and conversions are performed on the above parameters.

            Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
            no validations and conversions are performed on the above
            parameters. This option is desired primarily when the user wants to
            avoid potentially expensive validation and/or conversion operations.

        Returns
        -------
        result : `array_like` (`float`, shape=``x.shape``)
            The values of the fractional intensity at the real-space coordinate
            pairs specified by ``x`` and ``y``. For every tuple of nonnegative
            integers ``indices`` that does not raise an ``IndexError`` exception
            upon calling ``result[indices]``, ``result[indices]`` is the value
            of the fractional intensity for the real-space coordinate pair
            ``(x[indices], y[indices])``.

        """
        params = {key: val
                  for key, val in locals().items()
                  if (key not in ("self", "__class__"))}

        func_alias = _check_and_convert_skip_validation_and_conversion
        skip_validation_and_conversion = func_alias(params)

        if (skip_validation_and_conversion == False):
            params = {"cartesian_coords": (x, y), "units": "Å"}
            x, y = _check_and_convert_cartesian_coords(params)

        result = self._eval(x, y)

        return result



    def _eval(self, x, y):
        zip_obj = zip(self._gauss_hermite_weights, self._rspace_wavefunctions)

        result = np.zeros_like(x).astype(float)
        for w_f_l, rspace_wavefunction in zip_obj:
            kwargs = {"x": x, "y": y}
            temp = np.abs(rspace_wavefunction._eval(**kwargs)).astype(float)
            result += w_f_l*temp*temp
        result /= np.sqrt(np.pi)

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
