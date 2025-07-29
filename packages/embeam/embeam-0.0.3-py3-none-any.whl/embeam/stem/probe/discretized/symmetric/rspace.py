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
r"""Contains class representing discretized real-space wavefunctions and
fractional intensities of probes that are azimuthally symmetric.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For performing deep copies.
import copy



# For general array handling.
import numpy as np

# For interpolations.
import scipy

# For validating and converting objects.
import czekitout.convert

# For defining classes that support enforced validation, updatability,
# pre-serialization, and de-serialization.
import fancytypes

# For creating hyperspy signals.
import hyperspy.signals

# For calculating the modulus squared of hyperspy signals.
import empix



# For validating, pre-serializing, and de-pre-serializing instances of
# :class:`embeam.stem.probe.ModelParams`.
import embeam.stem.probe

# For calculating the electron beam wavelength; validating, pre-serializing,
# de-pre-serializing, and generating objects used to construct instances of
# :class:`embeam.stem.probe.discretized.symmetric.rspace.Wavefunction` and
# :class:`embeam.stem.probe.discretized.symmetric.rspace.Intensity`; and
# temporarily disabling chromatic aberrations.
import embeam.stem.probe.discretized

# For constructing instances of
# :class:`embeam.stem.probe.symmetric.rspace.Wavefunction` and
# :class:`embeam.stem.probe.symmetric.rspace.Intensity`.
import embeam.stem.probe.symmetric.rspace



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
    r"""The discretized real-space wavefunction of an azimuthally symmetric and 
    coherent probe.

    The discretized real-space wavefunction of an azimuthally symmetric and
    coherent probe is defined as

    .. math ::
        \psi_{\text{probe};n_{1},n_{2}}^{\text{symmetric}}
        \left(\delta_{f}\right)=
        \psi_{\text{probe}}^{\text{symmetric}}\left(x_{n_{2}},y_{n_{1}};
        \delta_{f}\right),
        :label: psi_probe_n_1_n_2_symmetric_in_stem_probe_discretized_symmetric_rspace__1

    where
    :math:`\psi_{\text{probe}}^{\text{symmetric}}\left(x_{n_{2}},y_{n_{1}};
    \delta_{f}\right)` is given by
    Eq. :eq:`coherent_psi_probe_in_stem_probe_symmetric_rspace__1`;
    :math:`\delta_f` is the defocal offset; :math:`n_{1}` and :math:`n_{2}` are
    the row and column indices of the discretized object respectively;

    .. math ::
        x_{n}=\Delta x\left\{ -\left\lfloor N_{x}/2\right\rfloor +n\right\} ,
        :label: x_n_in_stem_probe_discretized_symmetric_rspace__1

    with :math:`\Delta x` being the :math:`x`-dimension of each pixel, and
    :math:`N_{x}` being the total number of columns; and

    .. math ::
        y_{n}=\Delta y
        \left\{ \left\lfloor \left(N_{y}-1\right)/2\right\rfloor -n\right\} ,
        :label: y_n_in_stem_probe_discretized_symmetric_rspace__1

    with :math:`\Delta y` being the :math:`y`-dimension of each pixel, and
    :math:`N_{y}` being the total number of rows.

    Note that
    :math:`\psi_{\text{probe};n_{1},n_{2}}^{\text{symmetric}}\left(\delta_{f}
    \right)` samples the real-space wavefunction of the azimuthally symmetric
    and coherent probe,
    i.e. :math:`\psi_{\text{probe}}^{\text{symmetric}}\left(x,y;
    \delta_{f}\right)`.

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
         _check_and_convert_symmetric_coherent_probe_model_params,
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
            :attr:`embeam.stem.probe.discretized.symmetric.rspace.Wavefunction.signal`.

            If ``deep_copy`` is set to ``True``, then a deep copy of ``signal``
            is returned.  Otherwise, a reference to ``signal`` is returned.

        Returns
        -------
        signal : :class:`hyperspy._signals.signal2d.ComplexSignal2D`
            The attribute
            :attr:`embeam.stem.probe.discretized.symmetric.rspace.Wavefunction.signal`.

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
        probe_model_params = self_core_attrs["probe_model_params"]

        kwargs = \
            {"probe_model_params": probe_model_params,
             "skip_validation_and_conversion": True}
        rspace_wavefunction = \
            embeam.stem.probe.symmetric.rspace.Wavefunction(**kwargs)

        kwargs = {"discretized_obj_core_attrs": self_core_attrs}
        r_samples = embeam.stem.probe.discretized._r_samples(**kwargs)

        kwargs = {"x": r_samples, "y": np.zeros_like(r_samples)}
        psi_samples = rspace_wavefunction._eval(**kwargs)
        
        psi_mag_interp = scipy.interpolate.interp1d(r_samples, 
                                                    np.abs(psi_samples), 
                                                    "cubic")
        psi_angle_interp = scipy.interpolate.interp1d(r_samples, 
                                                      np.angle(psi_samples), 
                                                      "cubic")

        kwargs = {"discretized_obj_core_attrs": self_core_attrs}
        r_grid = embeam.stem.probe.discretized._r_grid(**kwargs)
        
        signal_data = (psi_mag_interp(r_grid) 
                       * np.exp(1j * psi_angle_interp(r_grid)))
        
        return signal_data


    
    @property
    def signal(self):
        r"""`hyperspy._signals.signal2d.Signal2D`: The hyperspy signal
        representation of the discretized real-space wavefunction.

        Note that ``signal`` should be considered **read-only**.

        """
        result = self.get_signal(deep_copy=True)
        
        return result



def _check_and_convert_symmetric_probe_model_params(params):
    module_alias = embeam.stem.probe
    func_alias = module_alias._check_and_convert_symmetric_probe_model_params
    probe_model_params = func_alias(params)

    return probe_model_params



class Intensity(fancytypes.PreSerializableAndUpdatable):
    r"""The discretized real-space fractional intensity of an azimuthally 
    symmetric probe.

    The discretized real-space fractional intensity of an azimuthally symmetric
    probe is defined as

    .. math ::
        p_{\text{probe};\mathbf{R};n_{1},n_{2}}^{\text{symmetric}}=
        p_{\text{probe}}^{\text{symmetric}}\left(\left.X=x_{n_{2}}\right|
        Y=y_{n_{1}}\right),
        :label: p_probe_R_n_1_n_2_symmetric_in_stem_probe_discretized_symmetric_rspace__1

    where
    :math:`p_{\text{probe}}^{\text{symmetric}}\left(\left.X=x_{n_{2}}\right|
    Y=y_{n_{1}}\right)` is given by
    Eq. :eq:`symmetric_r_space_p_probe_in_stem_probe_symmetric_rspace__1`;
    :math:`n_{1}` and :math:`n_{2}` are the row and column indices of the
    discretized object respectively;

    .. math ::
        x_{n}=\Delta x
        \left\{ -\left\lfloor N_{x}/2\right\rfloor +n\right\} ,
        :label: x_n_in_stem_probe_discretized_symmetric_rspace__2

    with :math:`\Delta x` being the :math:`x`-dimension of each real-space
    pixel, and :math:`N_{x}` being the total number of columns;

    .. math ::
        y_{n}=\Delta y\left\{ \left\lfloor 
        \left(N_{y}-1\right)/2\right\rfloor -n\right\} ,
        :label: y_n_in_stem_probe_discretized_symmetric_rspace__2

    with :math:`\Delta y` being the :math:`y`-dimension of each real-space
    pixel, and :math:`N_{y}` being the total number of rows. In other words,
    :math:`p_{\text{probe};\mathbf{R};n_{1},n_{2}}^{\text{symmetric}}` samples
    :math:`p_{\text{probe}}^{\text{symmetric}}\left(\left.X=x_{n_{2}}\right|
    Y=y_{n_{1}}\right)`.

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
        {"probe_model_params": \
         _check_and_convert_symmetric_probe_model_params,
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

        is_coherent = probe_model_params.is_coherent

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
        self_core_attrs = self.get_core_attrs(deep_copy=False)

        metadata = {"General": {"title": "r-Space Probe Fractional Intensity"}, 
                    "Signal": dict()}

        signal = hyperspy.signals.Signal2D(data=self._calc_signal_data(),
                                           metadata=metadata)

        module_alias = embeam.stem.probe.discretized
        module_alias._update_rspace_signal_axes(signal, self_core_attrs)

        return signal



    def _calc_signal_data(self):
        self_core_attrs = self.get_core_attrs(deep_copy=False)
        
        N_x, N_y = self_core_attrs["viewer_dims_in_pixels"]
        probe_model_params = self_core_attrs["probe_model_params"]

        if probe_model_params.is_coherent:
            kwargs = self_core_attrs
            kwargs["skip_validation_and_conversion"] = True
            discretized_rspace_wavefunction = Wavefunction(**kwargs)

            discretized_rspace_wavefunction_signal = \
                discretized_rspace_wavefunction.get_signal(deep_copy=False)
            
            kwargs = {"input_signal": discretized_rspace_wavefunction_signal,
                      "title": "r-Space Probe Fractional Intensity"}
            signal_data = empix.abs_sq(**kwargs).data
        else:
            kwargs = \
                {"probe_model_params": probe_model_params,
                 "skip_validation_and_conversion": True}
            rspace_intensity = \
                embeam.stem.probe.symmetric.rspace.Intensity(**kwargs)

            kwargs = {"discretized_obj_core_attrs": self_core_attrs}
            r_samples = embeam.stem.probe.discretized._r_samples(**kwargs)

            kwargs = {"x": r_samples, "y": np.zeros_like(r_samples)}
            p_samples = rspace_intensity._eval(**kwargs)
        
            p_interp = scipy.interpolate.interp1d(r_samples, p_samples, "cubic")

            kwargs = {"discretized_obj_core_attrs": self_core_attrs}
            r_grid = embeam.stem.probe.discretized._r_grid(**kwargs)
        
            signal_data = p_interp(r_grid)
        
        return signal_data



    @property
    def signal(self):
        r"""`hyperspy._signals.signal2d.Signal2D`: The hyperspy signal
        representation of the discretized real-space fractional intensity.

        Note that ``signal`` should be considered **read-only**.

        """
        result = self.get_signal(deep_copy=True)
        
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
        r"""Construct the discretized real-space fractional intensity 
        corresponding to a given discretized real-space wavefunction of some 
        azimuthally symmetric and coherent probe.

        See the documentation for the class
        :class:`embeam.stem.probe.discretized.symmetric.rspace.Wavefunction` for
        a discussion on discretized real-space wavefunctions of azimuthally
        symmetric and coherent probes.

        Parameters
        ----------
        discretized_wavefunction : :class:`embeam.stem.probe.discretized.symmetric.rspace.Wavefunction`
            The discretized real-space wavefunction of the azimuthally symmetric
            and coherent probe of interest, from which to construct the
            discretized real-space fractional intensity.

        Returns
        -------
        discretized_intensity : :class:`embeam.stem.probe.discretized.symmetric.rspace.Intensity`
            The discretized real-space fractional intensity corresponding to the
            given discretized real-space wavefunction of the azimuthally
            symmetric and coherent probe of interest.

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
