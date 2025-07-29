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
r"""Contains class representing discretized periodic real-space wavefunctions 
and fractional intensities of probes.

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
# :class:`embeam.stem.probe.discretized.periodic.rspace.Wavefunction` and
# :class:`embeam.stem.probe.discretized.periodic.rspace.Intensity`; temporarily
# disabling chromatic aberrations; and constructing instances of
# :class:`embeam.stem.probe.discretized.kspace.Wavefunction`.
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
    module_alias = embeam.stem.probe.discretized.kspace
    func_alias = module_alias._check_and_convert_deep_copy
    deep_copy = func_alias(params)

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
    r"""The discretized periodic real-space wavefunction of a coherent probe.

    The discretized periodic real-space wavefunction of a coherent probe is
    defined as
    
    .. math ::
        \psi_{\text{probe};n_{1},n_{2}}^{\text{periodic}}\left(\delta_f\right)=
        \sum_{m_{1}=0}^{N_{y}-1}\sum_{m_{2}=0}^{N_{x}-1}
        \Phi_{\text{probe};m_{1},m_{2}}\left(\delta_f\right)
        e^{2\pi ik_{x;m_{2}}x_{n_{2}}+2\pi ik_{y;m_{1}}y_{n_{1}}},
        :label: psi_probe_n_1_n_2_periodic_in_stem_probe_discretized_periodic_rspace__1

    where :math:`\Phi_{\text{probe};m_{1},m_{2}}\left(\delta_{f}\right)` is
    given by Eq. :eq:`Phi_probe_n_1_n_2_in_stem_probe_discretized_kspace__1`;
    :math:`\delta_f` is the defocal offset; :math:`n_{1}` and :math:`n_{2}` are
    respectively the row and column indices of the discretized periodic
    real-space wavefunction of the coherent probe;

    .. math ::
        x_{n}=\Delta x
        \left\{ -\left\lfloor N_{x}/2\right\rfloor +n\right\} ,
        :label: x_n_in_stem_probe_discretized_periodic_rspace__1

    with :math:`\Delta x` being the :math:`x`-dimension of each real-space
    pixel, and :math:`N_{x}` being the total number of columns;

    .. math ::
        y_{n}=\Delta y\left\{ \left\lfloor 
        \left(N_{y}-1\right)/2\right\rfloor -n\right\} ,
        :label: y_n_in_stem_probe_discretized_periodic_rspace__1

    with :math:`\Delta y` being the :math:`y`-dimension of each real-space
    pixel, and :math:`N_{y}` being the total number of rows;

    .. math ::
        k_{x;m}=\frac{1}{N_{x}\Delta x}
        \left\{ -\left\lfloor N_{x}/2\right\rfloor +m\right\};
        :label: k_x_m_in_stem_probe_discretized_periodic_rspace__1

    and

    .. math ::
        k_{y;m}=\frac{1}{N_{y}\Delta y}
        \left\{ \left\lfloor \left(N_{y}-1\right)/2\right\rfloor -m\right\}.
        :label: k_y_m_in_stem_probe_discretized_periodic_rspace__1

    Note that by imposing periodic boundary conditions to the discretized
    periodic real-space wavefunction, we are introducing unphysical artifacts in
    our estimation and visualization of the corresponding real-space
    wavefunction :math:`\psi_{\text{probe}}\left(x,y;\delta_f\right)` of the
    coherent probe, which is modelled by
    Eq. :eq:`coherent_psi_probe_in_stem_probe_model_params__1`. Moreover,
    
    .. math ::
        \lim_{\Delta x,\Delta y\to0}
        \lim_{N_{x},N_{y}\to\infty}
        \psi_{\text{probe};n_{1},n_{2}}^{\text{periodic}}\left(\delta_f\right)=
        \psi_{\text{probe}}\left(x_{n_{2}},y_{n_{1}};\delta_f\right),
        :label: limit_of_psi_probe_n_1_n_2_periodic_in_stem_probe_discretized_periodic_rspace__1

    In other words, in the above sequence of limits,
    :math:`\psi_{\text{probe};n_{1},n_{2}}^{\text{periodic}}\left(\delta_f\right)`
    samples
    :math:`\psi_{\text{probe}}\left(x_{n_{2}},y_{n_{1}};\delta_f\right)`.

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
        ``pixel_size[0]`` and ``pixel_size[1]`` are :math:`\Delta x` and
        :math:`\Delta y` respectively, in units of Å. Both ``pixel_size[0]`` and
        ``pixel_size[1]`` must be positive.
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
        {"probe_model_params": \
         _check_and_convert_coherent_probe_model_params,
         "pixel_size": \
         _check_and_convert_pixel_size,
         "viewer_dims_in_pixels": \
         _check_and_convert_viewer_dims_in_pixels}
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
        real-space wavefunction.

        Parameters
        ----------
        deep_copy : `bool`, optional
            Let ``signal`` denote the attribute
            :attr:`embeam.stem.probe.discretized.periodic.rspace.Wavefunction.signal`.

            If ``deep_copy`` is set to ``True``, then a deep copy of ``signal``
            is returned.  Otherwise, a reference to ``signal`` is returned.

        Returns
        -------
        signal : :class:`hyperspy._signals.signal2d.ComplexSignal2D`
            The attribute
            :attr:`embeam.stem.probe.discretized.periodic.rspace.Wavefunction.signal`.

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
        
        metadata = {"General": {"title": "r-Space Probe Wavefunction"}, 
                    "Signal": dict()}

        signal = hyperspy.signals.ComplexSignal2D(data=self._calc_signal_data(),
                                                  metadata=metadata)

        module_alias = embeam.stem.probe.discretized
        module_alias._update_rspace_signal_axes(signal, self_core_attrs)

        return signal



    def _calc_signal_data(self):
        self_core_attrs = self.get_core_attrs(deep_copy=False)
        
        N_x, N_y = self_core_attrs["viewer_dims_in_pixels"]
        d_x, d_y = self_core_attrs["pixel_size"]
        
        d_k_x, d_k_y = (1.0/(N_x*d_x), 1.0/(N_y*d_y))

        temp_signal = self._discretized_kspace_wavefunction_signal()
        temp_signal_data = np.fft.ifftshift(temp_signal.data[::-1, :])
        temp_signal_data = np.fft.ifft2(temp_signal_data, norm="forward")
        signal_data = np.fft.fftshift(temp_signal_data)[::-1, :]*d_k_x*d_k_y
        
        return signal_data


    
    def _discretized_kspace_wavefunction_signal(self):
        self_core_attrs = self.get_core_attrs(deep_copy=False)
        
        N_x, N_y = self_core_attrs["viewer_dims_in_pixels"]
        d_x, d_y = self_core_attrs["pixel_size"]

        kwargs = \
            {"probe_model_params": self_core_attrs["probe_model_params"],
             "pixel_size": (1.0/(N_x*d_x), 1.0/(N_y*d_y)),
             "viewer_dims_in_pixels": (N_x, N_y)}
        discretized_kspace_wavefunction = \
            embeam.stem.probe.discretized.kspace.Wavefunction(**kwargs)

        discretized_kspace_wavefunction_signal = \
            discretized_kspace_wavefunction.get_signal(deep_copy=False)

        return discretized_kspace_wavefunction_signal



    @property
    def signal(self):
        r"""`hyperspy._signals.signal2d.Signal2D`: The hyperspy signal
        representation of the discretized real-space wavefunction.

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
    r"""The discretized periodic real-space fractional intensity of a probe.

    The discretized periodic real-space fractional intensity of a probe is
    defined as

    .. math ::
        p_{\text{probe};\mathbf{R};n_{1},n_{2}}^{\text{periodic}}
        \approx\frac{1}{\sqrt{\pi}}\sum_{l=1}^{N_{f}}
        w_{f;l}\left|\psi_{\text{probe};n_{1},n_{2}}^{\text{periodic}}
        \left(\delta_{f}=\sqrt{2}\sigma_{f}x_{f;l}\right)\right|^{2},
        :label: p_probe_R_n_1_n_2_periodic_in_stem_probe_discretized_periodic_rspace__1

    where :math:`\psi_{\text{probe};n_{1},n_{2}}^{\text{periodic}}
    \left(\delta_{f}=\sqrt{2}\sigma_{f}x_{f;l}\right)` is given by
    Eq. :eq:`psi_probe_n_1_n_2_periodic_in_stem_probe_discretized_periodic_rspace__1`;
    :math:`\delta_f` is the defocal offset; the :math:`w_{f;l}` are given by Eq
    :eq:`normalized_gauss_hermite_weights_in_stem_probe_model_params__1`;
    :math:`N_{f}` is the number of points used in the Gauss-Hermite quadrature
    scheme of
    Eq. :eq:`incoherent_r_space_p_probe_in_stem_probe_model_params__2`;
    :math:`\sigma_{f}` is given by
    Eq. :eq:`sigma_f_in_stem_probe_model_params__1`; and :math:`n_{1}` and
    :math:`n_{2}` are respectively the row and column indices of the discretized
    periodic real-space fractional intensity of the probe.

    Note that by imposing periodic boundary conditions to the discretized
    periodic real-space fractional intensity, we are introducing unphysical
    artifacts in our estimation and visualization of the corresponding
    real-space fractional intensity
    :math:`p_{\text{probe}}\left(\left.X=x\right|Y=y\right)` of the probe, which
    is modelled by
    Eq. :eq:`incoherent_r_space_p_probe_in_stem_probe_model_params__1`. 
    Moreover,
    
    .. math ::
        \lim_{\Delta x,\Delta y\to0}
        \lim_{N_{x},N_{y}\to\infty}
        \lim_{N_{f}\to\infty}
        p_{\text{probe};\mathbf{R};n_{1},n_{2}}^{\text{periodic}}
        =p_{\text{probe}}\left(\left.X=x_{n_{2}}\right|Y=y_{n_{1}}\right),
        :label: limit_of_p_probe_R_n_1_n_2_periodic_in_stem_probe_discretized_periodic_rspace__1
    
    where

    .. math ::
        x_{n}=\Delta x
        \left\{ -\left\lfloor N_{x}/2\right\rfloor +n\right\} ,
        :label: x_n_in_stem_probe_discretized_periodic_rspace__2

    with :math:`\Delta x` being the :math:`x`-dimension of each real-space
    pixel, and :math:`N_{x}` being the total number of columns;

    .. math ::
        y_{n}=\Delta y\left\{ \left\lfloor 
        \left(N_{y}-1\right)/2\right\rfloor -n\right\} ,
        :label: y_n_in_stem_probe_discretized_periodic_rspace__2

    with :math:`\Delta y` being the :math:`y`-dimension of each real-space
    pixel, and :math:`N_{y}` being the total number of rows. In other words, in
    the above sequence of limits,
    :math:`p_{\text{probe};\mathbf{R};n_{1},n_{2}}^{\text{periodic}}` samples
    :math:`p_{\text{probe}}\left(\left.X=x\right|Y=y\right)`.

    See the documentation for the class :class:`embeam.stem.probe.ModelParams`
    for further discussion on probe modelling.

    Parameters
    ----------
    probe_model_params : :class:`embeam.stem.probe.ModelParams` | `None`, optional
        The model parameters of the probe. If ``probe_model_params`` is set to
        ``None`` [i.e. the default value], then the parameter will be reassigned
        to the value ``embeam.stem.probe.ModelParams()``.
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

    Attributes
    ----------
    core_attrs : `dict`, read-only
        A `dict` representation of the core attributes: each `dict` key is a
        `str` representing the name of a core attribute, and the corresponding
        `dict` value is the object to which said core attribute is set. The core
        attributes are the same as the construction parameters, except that 
        their values might have been updated since construction.
    signal : :class:`hyperspy._signals.signal2d.Signal2D` | `None`, read-only
        If ``viewer_dims_in_pixels[0]*viewer_dims_in_pixels[1] > 0``, then
        ``signal`` is the ``hyperspy`` signal that stores the data and metadata
        of, and the visualization methods for the discretized periodic
        real-space fractional intensity of the probe. Otherwise, ``signal`` is
        set to ``None``.
    azimuthally_symmetric : `bool`, read-only
        If the specified probe model is azimuthally symmetric, then
        ``azimuthally_symmetric`` is set to ``True``. Otherwise, it is set to
        ``False``. See the documentation for the attribute
        :attr:`embeam.coherent.PhaseDeviation.azimuthally_symmetric` for a
        discussion on the mathematical conditions for azimuthal symmetry.
    coherent : `bool`, read-only
        If the specified probe model is coherent, then ``coherent`` is set to
        ``True``. Otherwise, it is set to ``False``.

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
        real-space fractional intensity.

        Parameters
        ----------
        deep_copy : `bool`, optional
            Let ``signal`` denote the attribute
            :attr:`embeam.stem.probe.discretized.symmetric.rspace.Intensity.signal`.

            If ``deep_copy`` is set to ``True``, then a deep copy of ``signal``
            is returned.  Otherwise, a reference to ``signal`` is returned.

        Returns
        -------
        signal : :class:`hyperspy._signals.signal2d.Signal2D`
            The attribute
            :attr:`embeam.stem.probe.discretized.symmetric.rspace.Intensity.signal`.

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
        wavelength = \
            self._get_wavelength()
        old_C_2_0_mag = \
            self._get_old_C_2_0_mag()
        sigma_f, gauss_hermite_points, gauss_hermite_weights = \
            self._get_sigma_f_and_gauss_hermite_points_and_weights()

        self_core_attrs = self.get_core_attrs(deep_copy=False)

        temp_probe_model_params = \
            copy.deepcopy(self_core_attrs["probe_model_params"])

        module_alias = embeam.stem.probe
        kwargs = {"probe_model_params": temp_probe_model_params}
        module_alias._disable_chromatic_aberrations(**kwargs)

        zip_obj = zip(gauss_hermite_points, gauss_hermite_weights)
        for l, (x_f_l, w_f_l) in enumerate(zip_obj):
            delta_f = np.sqrt(2)*sigma_f*x_f_l
            new_C_2_0_mag = old_C_2_0_mag + np.pi*delta_f/wavelength
                
            func_alias = module_alias._update_C_2_0_mag_in_probe_model_params
            kwargs = {"probe_model_params": temp_probe_model_params,
                      "C_2_0_mag": new_C_2_0_mag}
            func_alias(**kwargs)
                
            kwargs = self_core_attrs.copy()
            kwargs["probe_model_params"] = temp_probe_model_params
            kwargs["skip_validation_and_conversion"] = True
            discretized_rspace_wavefunction = Wavefunction(**kwargs)

            discretized_rspace_wavefunction_signal = \
                discretized_rspace_wavefunction.get_signal(deep_copy=False)
                
            kwargs = {"input_signal": discretized_rspace_wavefunction_signal,
                      "title": "r-Space Probe Fractional Intensity"}
            temp_signal = empix.abs_sq(**kwargs)
                
            if l == 0:
                signal = temp_signal
                signal.data *= w_f_l
            else:
                signal.data += w_f_l * temp_signal.data
                    
        signal.data /= np.sqrt(np.pi)

        return signal



    def _get_wavelength(self):
        self_core_attrs = self.get_core_attrs(deep_copy=False)

        probe_model_params = self_core_attrs["probe_model_params"]

        probe_model_params_core_attrs = \
            probe_model_params.get_core_attrs(deep_copy=False)
        
        gun_model_params = probe_model_params_core_attrs["gun_model_params"]

        gun_model_params_core_attrs = \
            gun_model_params.get_core_attrs(deep_copy=False)
        
        beam_energy = gun_model_params_core_attrs["mean_beam_energy"]
        
        wavelength = embeam.wavelength(beam_energy)

        return wavelength



    def _get_old_C_2_0_mag(self):
        self_core_attrs = self.get_core_attrs(deep_copy=False)

        probe_model_params = self_core_attrs["probe_model_params"]

        module_alias = embeam.stem.probe
        func_alias = module_alias._get_C_2_0_mag_from_probe_model_params        
        old_C_2_0_mag = func_alias(probe_model_params)

        return old_C_2_0_mag



    def _get_sigma_f_and_gauss_hermite_points_and_weights(self):
        self_core_attrs = self.get_core_attrs(deep_copy=False)

        probe_model_params = self_core_attrs["probe_model_params"]
        
        sigma_f = probe_model_params._sigma_f
        gauss_hermite_points = probe_model_params._gauss_hermite_points
        gauss_hermite_weights = probe_model_params._gauss_hermite_weights

        return sigma_f, gauss_hermite_points, gauss_hermite_weights



    @property
    def signal(self):
        r"""`hyperspy._signals.signal2d.Signal2D`: The hyperspy signal
        representation of the discretized real-space fractional intensity.

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
        r"""Construct the discretized periodic real-space fractional intensity
        corresponding to a given discretized periodic real-space wavefunction of
        some coherent probe.

        See the documentation for the class
        :class:`embeam.stem.probe.discretized.periodic.rspace.Wavefunction` for
        a discussion on discretized periodic real-space wavefunctions of
        coherent probes.

        Parameters
        ----------
        discretized_wavefunction : :class:`embeam.stem.probe.discretized.periodic.rspace.Wavefunction`
            The discretized periodic real-space wavefunction of the coherent
            probe of interest, from which to construct the discretized periodic
            real-space fractional intensity.

        Returns
        -------
        discretized_intensity : :class:`embeam.stem.probe.discretized.periodic.rspace.Intensity`
            The discretized periodic real-space fractional intensity
            corresponding to the given discretized periodic real-space
            wavefunction of the coherent probe of interest.

        """
        kwargs = {"obj": discretized_wavefunction,
                  "obj_name": "discretized_wavefunction",
                  "accepted_types": (Wavefunction,)}
        czekitout.check.if_instance_of_any_accepted_types(**kwargs)

        kwargs = discretized_wavefunction.core_attrs
        kwargs["skip_validation_and_conversion"] = True
        discretized_intensity = cls(**kwargs)

        discretized_wavefunction_signal = \
            discretized_wavefunction.get_signal(deep_copy=False)
        
        kwargs = {"input_signal": discretized_wavefunction_signal,
                  "title": "r-Space Probe Fractional Intensity"}
        discretized_intensity._signal = empix.abs_sq(**kwargs)

        return discretized_intensity



###########################
## Define error messages ##
###########################
