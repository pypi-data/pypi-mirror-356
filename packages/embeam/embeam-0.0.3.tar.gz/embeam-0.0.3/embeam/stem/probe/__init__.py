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
"""For modelling and visualizing probes.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For generating Gauss-Hermite quadrature points and weights, and special math
# functions.
import numpy as np

# For validating and converting objects.
import czekitout.check
import czekitout.convert

# For defining classes that support enforced validation, updatability,
# pre-serialization, and de-serialization.
import fancytypes



# Import child modules and packages of current package.
import embeam.stem.probe.kspace
import embeam.stem.probe.symmetric
import embeam.stem.probe.discretized
import embeam.stem.probe.resolution

# For validating, pre-serializing, and de-pre-serializing instances of the class
# :class:`embeam.lens.ModelParams`.
import embeam.lens

# For validating, pre-serializing, and de-pre-serializing instances of the class
# :class:`embeam.gun.ModelParams`.
import embeam.gun

# For constructing instances of the class :class:`embeam.coherent.Aberration`.
import embeam.coherent



##################################
## Define classes and functions ##
##################################

# List of public objects in package.
__all__ = ["ModelParams"]



def _check_and_convert_lens_model_params(params):
    module_alias = embeam.lens
    func_alias = module_alias._check_and_convert_lens_model_params
    lens_model_params = func_alias(params)

    return lens_model_params



def _pre_serialize_lens_model_params(lens_model_params):
    obj_to_pre_serialize = lens_model_params
    module_alias = embeam.lens
    func_alias = module_alias._pre_serialize_lens_model_params
    serializable_rep = func_alias(obj_to_pre_serialize)

    return serializable_rep



def _de_pre_serialize_lens_model_params(serializable_rep):
    module_alias = embeam.lens
    func_alias = module_alias._de_pre_serialize_lens_model_params
    lens_model_params = func_alias(serializable_rep)

    return lens_model_params



def _check_and_convert_gun_model_params(params):
    module_alias = embeam.gun
    func_alias = module_alias._check_and_convert_gun_model_params
    gun_model_params = func_alias(params)

    return gun_model_params



def _pre_serialize_gun_model_params(gun_model_params):
    obj_to_pre_serialize = gun_model_params
    module_alias = embeam.gun
    func_alias = module_alias._pre_serialize_gun_model_params
    serializable_rep = func_alias(obj_to_pre_serialize)

    return serializable_rep



def _de_pre_serialize_gun_model_params(serializable_rep):
    module_alias = embeam.gun
    func_alias = module_alias._de_pre_serialize_gun_model_params
    gun_model_params = func_alias(serializable_rep)

    return gun_model_params



def _check_and_convert_convergence_semiangle(params):
    obj_name = "convergence_semiangle"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    convergence_semiangle = czekitout.convert.to_positive_float(**kwargs)

    return convergence_semiangle



def _pre_serialize_convergence_semiangle(convergence_semiangle):
    obj_to_pre_serialize = convergence_semiangle
    serializable_rep = obj_to_pre_serialize
    
    return serializable_rep



def _de_pre_serialize_convergence_semiangle(serializable_rep):
    convergence_semiangle = serializable_rep

    return convergence_semiangle



def _check_and_convert_defocal_offset_supersampling(params):
    obj_name = "defocal_offset_supersampling"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    defocal_offset_supersampling = czekitout.convert.to_positive_int(**kwargs)

    return defocal_offset_supersampling



def _pre_serialize_defocal_offset_supersampling(defocal_offset_supersampling):
    obj_to_pre_serialize = defocal_offset_supersampling
    serializable_rep = obj_to_pre_serialize
    
    return serializable_rep



def _de_pre_serialize_defocal_offset_supersampling(serializable_rep):
    defocal_offset_supersampling = serializable_rep

    return defocal_offset_supersampling



_module_alias_1 = \
    embeam.lens
_module_alias_2 = \
    embeam.gun
_default_lens_model_params = \
    _module_alias_1._default_lens_model_params
_default_gun_model_params = \
    _module_alias_2._default_gun_model_params
_default_convergence_semiangle = \
    15
_default_defocal_offset_supersampling = \
    9
_default_skip_validation_and_conversion = \
    _module_alias_1._default_skip_validation_and_conversion



class ModelParams(fancytypes.PreSerializableAndUpdatable):
    r"""The model parameters of a probe.

    Note that ``embeam`` currently does not support the modelling of finite
    source effects that lead to spatially incoherent probes.

    As discussed in greater detail in e.g. Ref. [Kirkland1]_, the
    :math:`k`-space wavefunction of a coherent probe is well-described by the
    following model:

    .. math ::
        \Phi_{\text{probe}}\left(k_{x},k_{y};\delta_{f}\right)=
        \frac{1}{\sqrt{\pi k_{xy,\max}^{2}}}
        \Theta\left(k_{xy,\max}-k_{xy}\right)
        e^{-i\chi\left(k_{x},k_{y};\delta_{f}\right)},
        :label: coherent_Phi_probe_in_stem_probe_model_params__1

    where :math:`k_{x}` and :math:`k_{y}` are the Fourier coordinates; 

    .. math ::
        k_{xy}=\sqrt{k_{x}^{2}+k_{y}^{2}},
        :label: k_xy_in_stem_probe_model_params__1

    .. math ::
        k_{xy,\max}=\frac{\alpha_{\max}}{\lambda},
        :label: k_xy_max_in_stem_probe_model_params__1

    with :math:`\alpha_{\max}` being the convergence semiangle, and
    :math:`\lambda` being the electron beam wavelength [given by
    Eq. :eq:`electron_beam_wavelength__1`]; :math:`\delta_f` is the defocal
    offset; :math:`\Theta\left(u\right)` is the Heaviside step function; and
    :math:`\chi\left(k_{x},k_{y};\delta_f\right)` is given by
    Eq. :eq:`chi_in_coherent_aberration__1`. The corresponding real-space
    wavefunction of the coherent probe can be expressed as

    .. math ::
        \psi_{\text{probe}}\left(x,y;\delta_{f}\right)=
        \int_{-\infty}^{\infty}dk_{x}\,\int_{-\infty}^{\infty}dk_{y}\,
        \Phi_{\text{probe}}\left(k_{x},k_{y};\delta_{f}\right)
        e^{2\pi ik_{x}x+2\pi ik_{y}y},
        :label: coherent_psi_probe_in_stem_probe_model_params__1

    where :math:`x` and :math:`y` are the real-space coordinates. The
    :math:`k`-space fractional intensity of the coherent probe is simply:

    .. math ::
        p_{\text{probe}}\left(\left.K_{x}=k_{x}\right|K_{y}=k_{y};
        \delta_{f}\right)&=\left|\Phi_{\text{probe}}\left(k_{x},k_{y};
        \delta_{f}\right)\right|^{2}\\&=\frac{1}{\pi k_{xy,\max}^{2}}
        \Theta\left(k_{xy,\max}-k_{xy}\right)\\
        &=p_{\text{probe}}\left(\left.K_{x}=k_{x}\right|K_{y}=k_{y};
        \delta_{f}=0\right),
        :label: coherent_k_space_p_probe_in_stem_probe_model_params__1

    and the corresponding real-space fractional intensity of the coherent probe
    is:

    .. math ::
        p_{\text{probe}}\left(\left.X=x\right|Y=y;\delta_{f}\right)=
        \left|\psi_{\text{probe}}\left(x,y;\delta_{f}\right)\right|^{2}.
        :label: coherent_r_space_p_probe_in_stem_probe_model_params__1

    In scenarios where the probe forming lens is subject to chromatic
    aberrations, and there are small fluctuations in the electron beam energy
    over time, there will be correspondingly small fluctuations in the defocus
    of the electron beam over time. In such cases, the :math:`k`-space
    fractional intensity of the incoherent probe is well-described by the
    following model:

    .. math ::
        p_{\text{probe}}\left(\left.K_{x}=k_{x}\right|K_{y}=k_{y}\right)
        &=\int_{-\infty}^{\infty}d\delta_{f}\,
        p_{\sigma_{f}}\left(\delta_{f}\right)
        p_{\text{probe}}\left(\left.K_{x}=k_{x}\right|K_{y}=k_{y};
        \delta_{f}\right)\\
        &=p_{\text{probe}}\left(\left.K_{x}=k_{x}\right|K_{y}=k_{y};
        \delta_{f}=0\right)\int_{-\infty}^{\infty}d\delta_{f}\,
        p_{\sigma_{f}}\left(\delta_{f}\right)\\
        &=p_{\text{probe}}\left(\left.K_{x}=k_{x}\right|K_{y}=k_{y};
        \delta_{f}=0\right),
        :label: incoherent_k_space_p_probe_in_stem_probe_model_params__1

    where :math:`p_{\sigma_{f}}\left(\delta_{f}\right)` is the distribution of
    :math:`\delta_{f}`:

    .. math ::
        p_{\sigma_{f}}\left(\delta_{f}\right)=\frac{1}{\sigma_{f}\sqrt{2\pi}}
        \exp\left(-\frac{1}{2}\frac{\delta_{f}^{2}}{\sigma_{f}^{2}}\right),
        :label: p_sigma_f_in_stem_probe_model_params__1

    with :math:`\sigma_{f}` being the defocal spread:

    .. math ::
        \sigma_{f}=C_{c}\sqrt{\left(\frac{\sigma_{E}/e}{V}\right)^{2}
        +\left(2\frac{\sigma_{I}}{I}\right)^{2}
        +\left(\frac{\sigma_{V}}{V}\right)^{2}},
        :label: sigma_f_in_stem_probe_model_params__1

    :math:`C_c` being the chromatic aberration coefficient, :math:`I` being the
    mean current of the probe forming lens, :math:`\sigma_I` being the standard
    deviation of the current of the probe forming lens, :math:`V` being the mean
    accelerating voltage, :math:`e` being the elementary charge,
    :math:`\sigma_V` being the standard deviation of the accelerating voltage,
    and :math:`\sigma_E` being the standard deviation of the electrons in the
    gun when operating a voltage supply that does not fluctuate
    [i.e. :math:`\sigma_E` is the intrinsic energy spread of the gun]. The
    corresponding real-space fractional intensity of the incoherent probe is:

    .. math ::
        p_{\text{probe}}\left(\left.X=x\right|Y=y\right)=
        \int_{-\infty}^{\infty}d\delta_{f}\,
        p_{\sigma_{f}}\left(\delta_{f}\right)
        p_{\text{probe}}\left(\left.X=x\right|Y=y;\delta_{f}\right).
        :label: incoherent_r_space_p_probe_in_stem_probe_model_params__1

    In ``embeam``, the integral in
    Eq. :eq:`incoherent_r_space_p_probe_in_stem_probe_model_params__1` is
    numerically evaluated using Gauss-Hermite quadrature:

    .. math ::
        p_{\text{probe}}\left(\left.X=x\right|Y=y\right)\approx
        \frac{1}{\sqrt{\pi}}\sum_{l=1}^{N_{f}}w_{f;l}
        p_{\text{probe}}\left(\left.X=x\right|Y=y;
        \delta_{f}=\sqrt{2}\sigma_{f}x_{f;l}\right),
        :label: incoherent_r_space_p_probe_in_stem_probe_model_params__2

    where :math:`x_{f;l}` is the :math:`l^{\text{th}}` root of the Physicists'
    version of the :math:`N_{f}^{\text{th}}` Hermite polynomial
    :math:`H_{N_{f}}\left(x\right)`; and :math:`w_{f;l}` is the
    :math:`l^{\text{th}}` quadrature weight:

    .. math ::
        w_{f;l}=\sqrt{\pi}
        \frac{\tilde{w}_{f;l}}{\sum_{l=1}^{N_{f}}\tilde{w}_{f;l}},
        :label: normalized_gauss_hermite_weights_in_stem_probe_model_params__1

    with

    .. math ::
        \tilde{w}_{f;l}=\frac{2^{N_{f}-1}N_{f}!\sqrt{\pi}}{N_{f}^{2}
        \left\{ H_{N_{f}-1}\left(x_{l}\right)\right\} ^{2}}.
        :label: unnormalized_gauss_hermite_weights_in_stem_probe_model_params__1

    Note that the right-hand-side (RHS) of
    Eq. :eq:`incoherent_r_space_p_probe_in_stem_probe_model_params__2` equals
    the RHS Eq. :eq:`incoherent_r_space_p_probe_in_stem_probe_model_params__1`
    in the limit that :math:`N_{f}\to\infty`.

    Parameters
    ----------
    lens_model_params : :class:`embeam.lens.ModelParams` | `None`, optional
        The model parameters of the probe forming lens. If ``lens_model_params``
        is set to ``None`` [i.e. the default value], then no chromatic or
        coherent lens aberrations are assumed to be present.
    gun_model_params : :class:`embeam.gun.ModelParams` | `None`, optional
        The electron gun model parameters. If ``gun_model_params`` is set to
        ``None`` [i.e. the default value], then the parameter will be reassigned
        to the value ``embeam.gun.ModelParams()``.
    convergence_semiangle : `float`, optional
        The convergence semiangle in mrads. Must be positive.
    defocal_offset_supersampling : `int`, optional
        The number of points :math:`N_f` to use in the Gauss-Hermite quadrature
        scheme of
        Eq. :eq:`normalized_gauss_hermite_weights_in_stem_probe_model_params__1`.
        Must be positive.
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
    ctor_param_names = ("lens_model_params",
                        "gun_model_params",
                        "convergence_semiangle",
                        "defocal_offset_supersampling")
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
                 lens_model_params=\
                 _default_lens_model_params,
                 gun_model_params=\
                 _default_gun_model_params,
                 convergence_semiangle=\
                 _default_convergence_semiangle,
                 defocal_offset_supersampling=\
                 _default_defocal_offset_supersampling,
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
        self._update_sigma_f()
        self._is_coherent = (self._sigma_f == 0.0).item()
        self._update_gauss_hermite_points_and_weights()
        self._update_is_azimuthally_symmetric()

        return None



    def _update_gauss_hermite_points_and_weights(self):
        if self._is_coherent:
            self._gauss_hermite_points = np.array([0])
            self._gauss_hermite_weights = np.sqrt([np.pi])
        else:
            self_core_attrs = \
                self.get_core_attrs(deep_copy=False)
            defocal_offset_supersampling = \
                self_core_attrs["defocal_offset_supersampling"]
            self._gauss_hermite_points, self._gauss_hermite_weights = \
                np.polynomial.hermite.hermgauss(defocal_offset_supersampling)

        return None



    def _update_sigma_f(self):
        self_core_attrs = self.get_core_attrs(deep_copy=False)

        lens_model_params = self_core_attrs["lens_model_params"]
        gun_model_params = self_core_attrs["gun_model_params"]

        lens_model_params_core_attrs = \
            lens_model_params.get_core_attrs(deep_copy=False)
        gun_model_params_core_attrs = \
            gun_model_params.get_core_attrs(deep_copy=False)

        C_c = (lens_model_params_core_attrs["chromatic_aberration_coef"]
               * (1e-3/1e-10))
        I = lens_model_params_core_attrs["mean_current"]
        sigma_I = lens_model_params_core_attrs["std_dev_current"]

        E = gun_model_params_core_attrs["mean_beam_energy"]
        sigma_E = gun_model_params_core_attrs["intrinsic_energy_spread"]
        sigma_V = gun_model_params_core_attrs["accel_voltage_spread"]

        self._sigma_f = C_c * np.sqrt((sigma_E/E)**2
                                      + (2*sigma_I/I)**2
                                      + (sigma_V/E)**2)

        return None


    def _update_is_azimuthally_symmetric(self):
        self_core_attrs = self.get_core_attrs(deep_copy=False)

        lens_model_params = self_core_attrs["lens_model_params"]

        is_azimuthally_symmetric = lens_model_params.is_azimuthally_symmetric
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



    @property
    def is_azimuthally_symmetric(self):
        r"""`bool`: A boolean variable indicating whether the probe model is 
        azimuthally symmetric.

        See the summary documentation of the classes
        :class:`embeam.coherent.PhaseDeviation` and
        :class:`embeam.coherent.Aberration` for additional context.

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



def _check_and_convert_probe_model_params(params):
    obj_name = "probe_model_params"
    obj = params[obj_name]

    accepted_types = (ModelParams, type(None))
    
    if isinstance(obj, accepted_types[-1]):
        probe_model_params = accepted_types[0]()
    else:
        kwargs = {"obj": obj,
                  "obj_name": obj_name,
                  "accepted_types": accepted_types}
        czekitout.check.if_instance_of_any_accepted_types(**kwargs)

        kwargs = obj.get_core_attrs(deep_copy=False)
        probe_model_params = accepted_types[0](**kwargs)

    return probe_model_params



def _pre_serialize_probe_model_params(probe_model_params):
    obj_to_pre_serialize = probe_model_params
    serializable_rep = obj_to_pre_serialize.pre_serialize()
    
    return serializable_rep



def _de_pre_serialize_probe_model_params(serializable_rep):
    probe_model_params = ModelParams.de_pre_serialize(serializable_rep)
    
    return probe_model_params



_default_probe_model_params = None



def _check_and_convert_symmetric_probe_model_params(params):
    probe_model_params = _check_and_convert_probe_model_params(params)

    current_func_name = "_check_and_convert_symmetric_probe_model_params"

    if not probe_model_params.is_azimuthally_symmetric:
        err_msg = globals()[current_func_name+"_err_msg_1"]
        raise ValueError(err_msg)

    return probe_model_params



def _check_and_convert_coherent_probe_model_params(params):
    probe_model_params = _check_and_convert_probe_model_params(params)

    current_func_name = "_check_and_convert_coherent_probe_model_params"

    if not probe_model_params.is_coherent:
        err_msg = globals()[current_func_name+"_err_msg_1"]
        raise ValueError(err_msg)

    return probe_model_params



def _check_and_convert_symmetric_coherent_probe_model_params(params):
    current_func_name = ("_check_and_convert"
                         "_symmetric_coherent_probe_model_params")
    
    try:
        func_alias = _check_and_convert_symmetric_probe_model_params
        probe_model_params = func_alias(params)
    except:
        err_msg = globals()[current_func_name+"_err_msg_1"]
        raise ValueError(err_msg)

    if not probe_model_params.is_coherent:
        err_msg = globals()[current_func_name+"_err_msg_1"]
        raise ValueError(err_msg)

    return probe_model_params



def _disable_chromatic_aberrations(probe_model_params):
    probe_model_params_core_attrs = \
        probe_model_params.get_core_attrs(deep_copy=False)
    lens_model_params = \
        probe_model_params_core_attrs["lens_model_params"]

    kwargs = {"new_core_attr_subset_candidate": \
              {"chromatic_aberration_coef": 0}}
    lens_model_params.update(**kwargs)

    kwargs = {"new_core_attr_subset_candidate": \
              {"lens_model_params": lens_model_params}}
    probe_model_params.update(**kwargs)

    return None


def _get_C_2_0_mag_from_probe_model_params(probe_model_params):
    probe_model_params_core_attrs = \
        probe_model_params.get_core_attrs(deep_copy=False)
    lens_model_params = \
        probe_model_params_core_attrs["lens_model_params"]

    lens_model_params_core_attrs = \
        lens_model_params.get_core_attrs(deep_copy=False)
    coherent_aberrations = \
        lens_model_params_core_attrs["coherent_aberrations"]

    C_2_0_mag = 0
    
    for coherent_aberration in coherent_aberrations:
        coherent_aberration_core_attrs = \
            coherent_aberration.get_core_attrs(deep_copy=False)
        
        mn_pair = (coherent_aberration_core_attrs["m"],
                   coherent_aberration_core_attrs["n"])
        if mn_pair == (2, 0):
            C_2_0_mag = coherent_aberration_core_attrs["C_mag"]
            break

    return C_2_0_mag



def _update_C_2_0_mag_in_probe_model_params(probe_model_params, C_2_0_mag):
    probe_model_params_core_attrs = \
        probe_model_params.get_core_attrs(deep_copy=False)
    lens_model_params = \
        probe_model_params_core_attrs["lens_model_params"]

    lens_model_params_core_attrs = \
        lens_model_params.get_core_attrs(deep_copy=False)
    coherent_aberrations = \
        lens_model_params_core_attrs["coherent_aberrations"]

    defocus_aberration_not_found = True
    
    for coherent_aberration in coherent_aberrations:
        coherent_aberration_core_attrs = \
            coherent_aberration.get_core_attrs(deep_copy=False)

        mn_pair = (coherent_aberration_core_attrs["m"],
                   coherent_aberration_core_attrs["n"])
        if mn_pair == (2, 0):
            defocus_aberration_not_found = False
            kwargs = {"new_core_attr_subset_candidate": \
                      {"C_mag": C_2_0_mag}}
            coherent_aberration.update(**kwargs)
            break

    if defocus_aberration_not_found:
        kwargs = {"m": 2,
                  "n": 0,
                  "C_mag": C_2_0_mag,
                  "C_ang": 0,
                  "skip_validation_and_conversion": True}
        coherent_aberration = embeam.coherent.Aberration(**kwargs)
        coherent_aberrations += (coherent_aberration,)

    kwargs = {"new_core_attr_subset_candidate": \
              {"coherent_aberrations": coherent_aberrations}}
    lens_model_params.update(**kwargs)

    kwargs = {"new_core_attr_subset_candidate": \
              {"lens_model_params": lens_model_params}}
    probe_model_params.update({"lens_model_params": lens_model_params})

    return None



###########################
## Define error messages ##
###########################

_check_and_convert_symmetric_probe_model_params_err_msg_1 = \
    ("The object ``probe_model_params`` must specify an azimuthally symmetric "
     "probe model.")

_check_and_convert_coherent_probe_model_params_err_msg_1 = \
    ("The object ``probe_model_params`` must specify a coherent probe model.")

_check_and_convert_symmetric_coherent_probe_model_params_err_msg_1 = \
    ("The object ``probe_model_params`` must specify an azimuthally symmetric "
     "and coherent probe model.")
