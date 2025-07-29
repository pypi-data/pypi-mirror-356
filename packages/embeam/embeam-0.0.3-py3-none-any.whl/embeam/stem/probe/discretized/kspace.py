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
r"""Contains classes representing discretized :math:`k`-space wavefunctions and
fractional intensities of probes.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For performing deep copies.
import copy



# For general array handling.
import numpy as np

# For validating and converting objects.
import czekitout.check
import czekitout.convert

# For defining classes that support enforced validation, updatability,
# pre-serialization, and de-serialization.
import fancytypes

# For creating hyperspy signals.
import hyperspy.signals

# For calculating the modulus squared of hyperspy signals.
import empix



# For calculating the electron beam wavelength; validating, pre-serializing,
# de-pre-serializing, and generating objects used to construct instances of
# :class:`embeam.stem.probe.discretized.kspace.Wavefunction` and
# :class:`embeam.stem.probe.discretized.kspace.Intensity`; and temporarily
# disabling chromatic aberrations.
import embeam



##################################
## Define classes and functions ##
##################################

# List of public objects in objects.
__all__ = ["Wavefunction",
           "Intensity"]



class _SoftAperture():
    def __init__(self, discretized_obj_core_attrs):
        self._d_k_xy_vec = np.array(discretized_obj_core_attrs["pixel_size"])

        probe_model_params = \
            discretized_obj_core_attrs["probe_model_params"]

        probe_model_params_core_attrs = \
            probe_model_params.get_core_attrs(deep_copy=False)
        convergence_semiangle = \
            probe_model_params_core_attrs["convergence_semiangle"]
        gun_model_params = \
            probe_model_params_core_attrs["gun_model_params"]

        gun_model_params_core_attrs = \
            gun_model_params.get_core_attrs(deep_copy=False)
        beam_energy = \
            gun_model_params_core_attrs["mean_beam_energy"]
        
        wavelength = embeam.wavelength(beam_energy)
        
        self._k_xy_max = (convergence_semiangle / 1000) / wavelength

        return None



    def _eval(self, k_x, k_y):
        temp_1 = k_x*k_x
        temp_2 = k_y*k_y
        temp_3 = temp_1 + temp_2
        temp_4 = np.sqrt(temp_3)
        temp_5 = self._k_xy_max * temp_4 - temp_3 + 1.0e-14
        temp_6 = (((self._d_k_xy_vec[0] * self._d_k_xy_vec[0]) * temp_1
                   + (self._d_k_xy_vec[1] * self._d_k_xy_vec[1]) * temp_2)
                  + 1.0e-14)
        temp_7 = temp_5/temp_6 + 0.5
        result = np.minimum(np.maximum(temp_7, 0), 1)

        return result



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



def _check_and_convert_pixel_size(params):
    module_alias = embeam.stem.probe.discretized
    func_alias = module_alias._check_and_convert_pixel_size
    pixel_size = func_alias(params)

    return pixel_size



def _pre_serialize_pixel_size(pixel_size):
    obj_to_pre_serialize = pixel_size
    module_alias = embeam.stem.probe.discretized
    func_alias = module_alias._pre_serialize_pixel_size
    serializable_rep = func_alias(obj_to_pre_serialize)

    return serializable_rep



def _de_pre_serialize_pixel_size(serializable_rep):
    module_alias = embeam.stem.probe.discretized
    pixel_size = module_alias._de_pre_serialize_pixel_size(serializable_rep)

    return pixel_size



def _check_and_convert_viewer_dims_in_pixels(params):
    module_alias = embeam.stem.probe.discretized
    func_alias = module_alias._check_and_convert_viewer_dims_in_pixels
    viewer_dims_in_pixels = func_alias(params)

    return viewer_dims_in_pixels



def _pre_serialize_viewer_dims_in_pixels(viewer_dims_in_pixels):
    obj_to_pre_serialize = viewer_dims_in_pixels
    module_alias = embeam.stem.probe.discretized
    func_alias = module_alias._pre_serialize_viewer_dims_in_pixels
    serializable_rep = func_alias(obj_to_pre_serialize)

    return serializable_rep



def _de_pre_serialize_viewer_dims_in_pixels(serializable_rep):
    module_alias = \
        embeam.stem.probe.discretized
    viewer_dims_in_pixels = \
        module_alias._de_pre_serialize_viewer_dims_in_pixels(serializable_rep)

    return viewer_dims_in_pixels



def _check_and_convert_deep_copy(params):
    obj_name = "deep_copy"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    deep_copy = czekitout.convert.to_bool(**kwargs)

    return deep_copy



_module_alias = \
    embeam.coherent
_default_probe_model_params = \
    None
_default_pixel_size = \
    2*(0.01,)
_default_viewer_dims_in_pixels = \
    2*(512,)
_default_skip_validation_and_conversion = \
    _module_alias._default_skip_validation_and_conversion
_default_deep_copy = \
    True



class Wavefunction(fancytypes.PreSerializableAndUpdatable):
    r"""The discretized :math:`k`-space wavefunction of a coherent probe.

    The discretized :math:`k`-space wavefunction of a coherent probe is defined
    as

    .. math ::
        \Phi_{\text{probe};n_{1},n_{2}}\left(\delta_f\right)=
        \frac{1}{\sqrt{\pi k_{xy,\max}^{2}}}
        A\left(k_{x;n_{2}},k_{y;n_{1}}\right)
        e^{-i\chi\left(k_{x;n_{2}},k_{y;n_{1}};\delta_f\right)},
        :label: Phi_probe_n_1_n_2_in_stem_probe_discretized_kspace__1

    where :math:`\chi\left(k_{x},k_{y};\delta_f\right)` is given by
    Eq. :eq:`chi_in_coherent_aberration__1`; :math:`\delta_f` is the defocal
    offset; :math:`n_{1}` and :math:`n_{2}` are the row and column indices of
    the discretized object respectively;

    .. math ::
        k_{x;n}=
        \Delta k_{x}\left\{ -\left\lfloor N_{x}/2\right\rfloor +n\right\},
        :label: k_x_n_in_stem_probe_discretized_kspace__1

    with :math:`\Delta k_{x}` being the :math:`k_x`-dimension of each pixel, and
    :math:`N_{x}` being the total number of columns; and

    .. math ::
        k_{y;n}=\Delta k_{y}
        \left\{ \left\lfloor \left(N_{y}-1\right)/2\right\rfloor -n\right\},
        :label: k_y_n_in_stem_probe_discretized_kspace__1

    with :math:`\Delta k_{y}` being the :math:`k_y`-dimension of each pixel, and
    :math:`N_{y}` being the total number of rows;

    .. math ::
        A\left(k_{x},k_{y}\right)=
        \min\left[\max\left(\frac{k_{xy,\max}k_{xy}
        -k_{xy}^{2}}{\left\Vert \mathbf{k}_{xy}\odot\Delta\mathbf{k}_{xy}
        \right\Vert _{2}}+\frac{1}{2},0\right),1\right],
        :label: soft_aperture_function_in_stem_probe_discretized_kspace__1

    with :math:`k_{xy}` being given by
    Eq. :eq:`k_xy_in_stem_probe_model_params__1`, :math:`k_{xy,\max}` being
    given by Eq. :eq:`k_xy_max_in_stem_probe_model_params__1`,

    .. math ::
        \mathbf{k}_{xy}=k_{x}\hat{\mathbf{x}}+k_{y}\hat{\mathbf{y}},
        :label: k_xy_vec_in_stem_probe_discretized_kspace__1

    .. math ::
        \Delta \mathbf{k}_{xy}=
        \Delta k_{x}\hat{\mathbf{x}}+\Delta k_{y}\hat{\mathbf{y}},
        :label: Delta_k_xy_vec_in_stem_probe_discretized_kspace__1

    :math:`\odot` being the Hadamard [element-wise] product, and
    :math:`\left\Vert \cdots\right\Vert _{2}` being the 2-norm. We refer to
    :math:`A\left(k_{x;n_{2}},k_{y;n_{1}}\right)` as a “soft” aperture function
    and opt for such an aperture function [following Ref. [DaCosta1]_] rather
    than a hard [i.e. step-function-like] aperture to minimize mathematical
    artifacts that emerge in the calculation of the discretized periodic
    :math:`r`-space wavefunction
    [Eq. :eq:`psi_probe_n_1_n_2_periodic_in_stem_probe_discretized_periodic_rspace__1`]
    of the same coherent probe, which involves taking a fast Fourier transform
    of :math:`\Phi_{\text{probe};n_{1},n_{2}}\left(\delta_f\right)`.

    Note that
    
    .. math ::
        \lim_{\Delta k_{x},\Delta k_{y}\to0}\lim_{N_{x},N_{y}\to\infty}
        \Phi_{\text{probe};n_{1},n_{2}}\left(\delta_f\right)=
        \Phi_{\text{probe}}\left(k_{x;n_{2}},k_{y;n_{1}};\delta_f\right),
        :label: limit_of_Phi_probe_n_1_n_2_in_stem_probe_discretized_kspace__1

    where :math:`\Phi_{\text{probe}}\left(k_{x},k_{y};\delta_f\right)` is given
    by Eq. :eq:`coherent_Phi_probe_in_stem_probe_model_params__1`. In other
    words, in the above sequence of limits,
    :math:`\Phi_{\text{probe};n_{1},n_{2}}\left(\delta f\right)` samples
    :math:`\Phi_{\text{probe}}\left(k_{x},k_{y};\delta_f\right)`, which is the
    :math:`k`-space wavefunction of the coherent probe.

    See the documentation for the class :class:`embeam.stem.probe.ModelParams`
    for further discussion on probe modelling.

    Parameters
    ----------
    probe_model_params : :class:`embeam.stem.probe.ModelParams` | `None`, optional
        The model parameters of the coherent probe. If ``probe_model_params`` is
        set to ``None`` [i.e. the default value], then the parameter will be
        reassigned to the value ``embeam.stem.probe.ModelParams()``. An
        exception is raised if the model parameters specify an incoherent probe.
    pixel_size : `array_like` (`float`, shape=(``2``,)), optional
        ``pixel_size[0]`` and ``pixel_size[1]`` are :math:`\Delta k_x` and
        :math:`\Delta k_y` respectively, in units of 1/Å. Both ``pixel_size[0]``
        and ``pixel_size[1]`` must be positive.
    viewer_dims_in_pixels : `array_like` (`int`, shape=(``2``,)), optional
        ``viewer_dims_in_pixels[0]`` and ``viewer_dims_in_pixels[1]`` are
        :math:`N_x` and :math:`N_y` respectively. Both
        ``viewer_dims_in_pixels[0]`` and ``viewer_dims_in_pixels[1]`` must be
        positive.
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
    ctor_param_names = ("probe_model_params",
                        "pixel_size",
                        "viewer_dims_in_pixels")
    kwargs = {"namespace_as_dict": globals(),
              "ctor_param_names": ctor_param_names}

    _validation_and_conversion_funcs_ = \
        {"probe_model_params": _check_and_convert_coherent_probe_model_params,
         "pixel_size": _check_and_convert_pixel_size,
         "viewer_dims_in_pixels": _check_and_convert_viewer_dims_in_pixels}
    _pre_serialization_funcs_ = \
        fancytypes.return_pre_serialization_funcs(**kwargs)
    _de_pre_serialization_funcs_ = \
        fancytypes.return_de_pre_serialization_funcs(**kwargs)

    del ctor_param_names, kwargs

    

    def __init__(self,
                 probe_model_params=\
                 _default_probe_model_params,
                 pixel_size=\
                 _default_pixel_size,
                 viewer_dims_in_pixels=\
                 _default_viewer_dims_in_pixels,
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
        probe_model_params = self_core_attrs["probe_model_params"]

        is_azimuthally_symmetric = probe_model_params.is_azimuthally_symmetric
        self._is_azimuthally_symmetric = is_azimuthally_symmetric

        self._signal = None

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



    def get_signal(self, deep_copy=_default_deep_copy):
        r"""Return the hyperspy signal representation of the discretized 
        :math:`k`-space wavefunction.

        Parameters
        ----------
        deep_copy : `bool`, optional
            Let ``signal`` denote the attribute
            :attr:`embeam.stem.probe.discretized.kspace.Wavefunction.signal`.

            If ``deep_copy`` is set to ``True``, then a deep copy of ``signal``
            is returned.  Otherwise, a reference to ``signal`` is returned.

        Returns
        -------
        signal : :class:`hyperspy._signals.signal2d.ComplexSignal2D`
            The attribute
            :attr:`embeam.stem.probe.discretized.kspace.Wavefunction.signal`.

        """
        params = {"deep_copy": deep_copy}
        deep_copy = _check_and_convert_deep_copy(params)

        if self._signal is None:
            self._signal = self._calc_signal()

        signal = (copy.deepcopy(self._signal)
                  if (deep_copy == True)
                  else self._signal)

        return signal



    def _calc_signal(self):
        self_core_attrs = self.get_core_attrs(deep_copy=False)

        metadata = {"General": {"title": "k-Space Probe Wavefunction"}, 
                    "Signal": dict()}
        
        signal = hyperspy.signals.ComplexSignal2D(data=self._calc_signal_data(),
                                                  metadata=metadata)

        module_alias = embeam.stem.probe.discretized
        kwargs = {"signal": signal,
                  "discretized_obj_core_attrs": self_core_attrs}
        module_alias._update_kspace_signal_axes(**kwargs)

        return signal



    def _calc_signal_data(self):
        self_core_attrs = self.get_core_attrs(deep_copy=False)
        
        N_x, N_y = self_core_attrs["viewer_dims_in_pixels"]

        kwargs = {"discretized_obj_core_attrs": self_core_attrs}        
        soft_aperture = _SoftAperture(**kwargs)
        
        d_k_x, d_k_y = self_core_attrs["pixel_size"]
        k_xy_max = soft_aperture._k_xy_max
        k_xy_upper_limit = k_xy_max + 0.5*np.sqrt(d_k_x*d_k_x + d_k_y*d_k_y)

        n_x_i = min(int(np.floor((N_x//2)-k_xy_upper_limit/d_k_x)), 0)
        n_x_f = max(int(np.ceil((N_x//2)+k_xy_upper_limit/d_k_x)+1), N_x)
        n_y_i = min(int(np.floor((N_y-1)//2-k_xy_upper_limit/d_k_y)), 0)
        n_y_f = max(int(np.ceil((N_y-1)//2+k_xy_upper_limit/d_k_y)+1), N_y)

        k_x_vec = embeam.stem.probe.discretized._k_x_vec(**kwargs)
        k_y_vec = embeam.stem.probe.discretized._k_y_vec(**kwargs)
        
        pair_of_1d_coord_arrays = (k_x_vec[n_x_i:n_x_f], k_y_vec[n_y_i:n_y_f])
        k_x_subgrid, k_y_subgrid = np.meshgrid(*pair_of_1d_coord_arrays,
                                               indexing="xy")

        probe_model_params = \
            self_core_attrs["probe_model_params"]
        kspace_wavefunction = \
            embeam.stem.probe.kspace.Wavefunction(probe_model_params)

        kwargs = \
            {"k_x": k_x_subgrid, "k_y": k_y_subgrid}
        signal_data = \
            np.zeros((N_y, N_x), dtype=complex)
        signal_data[n_y_i:n_y_f, n_x_i:n_x_f] = \
            (kspace_wavefunction._eval_without_heaviside(**kwargs)
             * soft_aperture._eval(**kwargs))
        
        return signal_data


    
    @property
    def signal(self):
        r"""`hyperspy._signals.signal2d.Signal2D`: The hyperspy signal
        representation of the discretized :math:`k`-space wavefunction.

        Note that ``signal`` should be considered **read-only**.

        """
        result = self.get_signal(deep_copy=True)
        
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
    r"""The discretized :math:`k`-space fractional intensity of a probe.

    The discretized :math:`k`-space fractional intensity of a probe is defined
    as

    .. math ::
        p_{\text{probe};\mathbf{K};n_{1},n_{2}}=
        \left|\Phi_{\text{probe};n_{1},n_{2}}\left(
        \delta_{f}=0\right)\right|^{2},
        :label: p_probe_K_n_1_n_2_in_stem_probe_discretized_kspace__1

    where :math:`\Phi_{\text{probe};n_{1},n_{2}}\left(\delta_{f}=0\right)` is
    given by Eq. :eq:`Phi_probe_n_1_n_2_in_stem_probe_discretized_kspace__1`;
    :math:`\delta_f` is the defocal offset; and :math:`n_{1}` and :math:`n_{2}`
    are the row and column indices of the discretized object respectively.

    Note that
    
    .. math ::
        \lim_{\Delta k_{x},\Delta k_{y}\to0}\lim_{N_{x},N_{y}\to\infty}
        p_{\text{probe};\mathbf{K};n_{1},n_{2}}=
        p_{\text{probe}}\left(\left.K_{x}=k_{x}\right|K_{y}=k_{y}\right),
        :label: limit_of_discretized_kspace_wavefunction__2

    where
    :math:`p_{\text{probe}}\left(\left.K_{x}=k_{x}\right|K_{y}=k_{y}\right)` is
    given by Eq. :eq:`incoherent_k_space_p_probe_in_stem_probe_model_params__1`;
    :math:`N_{x}` is the total number of columns; :math:`N_{y}` is the total
    number of rows; :math:`\Delta k_{x}` is the :math:`k_x`-dimension of each
    pixel; and :math:`\Delta k_{y}` is the :math:`k_y`-dimension of each
    pixel. In other words, in the above sequence of limits,
    :math:`p_{\text{probe};\mathbf{K};n_{1},n_{2}}` samples
    :math:`p_{\text{probe}}\left(\left.K_{x}=k_{x}\right|K_{y}=k_{y}\right)`,
    which is the :math:`k`-space fractional intensity of the probe.

    See the documentation for the class :class:`embeam.stem.probe.ModelParams`
    for further discussion on probe modelling.

    Parameters
    ----------
    probe_model_params : :class:`embeam.stem.probe.ModelParams` | `None`, optional
        The model parameters of the probe. If ``probe_model_params`` is set to
        ``None`` [i.e. the default value], then the parameter will be
        reassigned to the value ``embeam.stem.probe.ModelParams()``.
    pixel_size : `array_like` (`float`, shape=(``2``,)), optional
        ``pixel_size[0]`` and ``pixel_size[1]`` are :math:`\Delta k_x` and
        :math:`\Delta k_y` respectively, in units of 1/Å. Both ``pixel_size[0]``
        and ``pixel_size[1]`` must be positive.
    viewer_dims_in_pixels : `array_like` (`int`, shape=(``2``,)), optional
        ``viewer_dims_in_pixels[0]`` and ``viewer_dims_in_pixels[1]`` are
        :math:`N_x` and :math:`N_y` respectively. Both
        ``viewer_dims_in_pixels[0]`` and ``viewer_dims_in_pixels[1]`` must be
        positive.
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
    ctor_param_names = ("probe_model_params",
                        "pixel_size",
                        "viewer_dims_in_pixels")
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
                 pixel_size=\
                 _default_pixel_size,
                 viewer_dims_in_pixels=\
                 _default_viewer_dims_in_pixels,
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

        probe_model_params = self_core_attrs["probe_model_params"]

        is_azimuthally_symmetric = probe_model_params.is_azimuthally_symmetric
        is_coherent = probe_model_params.is_coherent

        self._is_azimuthally_symmetric = is_azimuthally_symmetric
        self._is_coherent = is_coherent

        self._signal = None

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



    def get_signal(self, deep_copy=_default_deep_copy):
        r"""Return the hyperspy signal representation of the discretized 
        :math:`k`-space fractional intensity.

        Parameters
        ----------
        deep_copy : `bool`, optional
            Let ``signal`` denote the attribute
            :attr:`embeam.stem.probe.discretized.kspace.Intensity.signal`.

            If ``deep_copy`` is set to ``True``, then a deep copy of ``signal``
            is returned.  Otherwise, a reference to ``signal`` is returned.

        Returns
        -------
        signal : :class:`hyperspy._signals.signal2d.Signal2D`
            The attribute
            :attr:`embeam.stem.probe.discretized.kspace.Intensity.signal`.

        """
        params = {"deep_copy": deep_copy}
        deep_copy = _check_and_convert_deep_copy(params)

        if self._signal is None:
            self._signal = self._calc_signal()

        signal = (copy.deepcopy(self._signal)
                  if (deep_copy == True)
                  else self._signal)

        return signal



    def _calc_signal(self):
        self_core_attrs = self.core_attrs

        probe_model_params = self_core_attrs["probe_model_params"]
        pixel_size = self_core_attrs["pixel_size"]
        viewer_dims_in_pixels = self_core_attrs["viewer_dims_in_pixels"]

        module_alias = embeam.stem.probe
        module_alias._disable_chromatic_aberrations(probe_model_params)

        kwargs = {"probe_model_params": probe_model_params,
                  "pixel_size": pixel_size,
                  "viewer_dims_in_pixels": viewer_dims_in_pixels,
                  "skip_validation_and_conversion": True}
        discretized_kspace_wavefunction = Wavefunction(**kwargs)

        discretized_kspace_wavefunction_signal = \
            discretized_kspace_wavefunction.get_signal(deep_copy=False)

        kwargs = {"input_signal": discretized_kspace_wavefunction_signal,
                  "title": "k-Space Probe Fractional Intensity"}
        signal = empix.abs_sq(**kwargs)

        return signal



    @property
    def signal(self):
        r"""`hyperspy._signals.signal2d.Signal2D`: The hyperspy signal
        representation of the discretized :math:`k`-space fractional intensity.

        Note that ``signal`` should be considered **read-only**.

        """
        result = self.get_signal(deep_copy=True)
        
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



    @classmethod
    def construct_from_discretized_wavefunction(cls, discretized_wavefunction):
        r"""Construct the discretized :math:`k`-space fractional intensity 
        corresponding to a given discretized :math:`k`-space wavefunction of 
        some coherent probe.

        See the documentation for the class
        :class:`embeam.stem.probe.discretized.kspace.Wavefunction` for a
        discussion on discretized :math:`k`-space wavefunctions of coherent
        probes.

        Parameters
        ----------
        discretized_wavefunction : :class:`embeam.stem.probe.discretized.kspace.Wavefunction`
            The discretized :math:`k`-space wavefunction of the coherent probe
            of interest, from which to construct the discretized :math:`k`-space
            fractional intensity.

        Returns
        -------
        discretized_intensity : :class:`embeam.stem.probe.discretized.kspace.Intensity`
            The discretized :math:`k`-space fractional intensity corresponding
            to the given discretized :math:`k`-space wavefunction of the
            coherent probe of interest.

        """
        kwargs = {"obj": discretized_wavefunction,
                  "obj_name": "discretized_wavefunction",
                  "accepted_types": (Wavefunction,)}
        czekitout.check.if_instance_of_any_accepted_types(**kwargs)

        kwargs = discretized_wavefunction.core_attrs
        kwargs["skip_validation_and_conversion"] = True
        discretized_intensity = cls(**kwargs)

        return discretized_intensity



###########################
## Define error messages ##
###########################
