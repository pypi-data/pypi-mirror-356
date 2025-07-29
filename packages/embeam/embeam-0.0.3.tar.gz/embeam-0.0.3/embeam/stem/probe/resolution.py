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
r"""Contains functions that calculate different measures of the spatial
resolution of probes.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For using special math functions and constants.
import numpy as np

# For interpolating 1D hyperspy signal data.
import scipy.interpolate

# For validating and converting objects.
import czekitout.check
import czekitout.convert

# For creating hyperspy signals.
import hyperspy.signals
import hyperspy.axes

# For calculating the intensities of probe wavefunctions, and averaging
# azimuthally and integrating annularly hyperspy signals.
import empix



# For validating instances of
# :class:`embeam.stem.probe.discretized.symmetric.Intensity` and
# :class:`embeam.stem.probe.discretized.periodic.Intensity`; generating
# real-space and k-space coordinates; and calculating ``alpha_max/lambda``,
# where ``alpha_max`` is the probe convergence semiangle, and ``lambda`` is the
# electron beam wavelength.
import embeam.stem.probe.discretized



##################################
## Define classes and functions ##
##################################

# List of public objects in objects.
__all__ = ["rise_distance",
           "information"]



def _check_and_convert_discretized_rspace_intensity(params):
    obj_name = "discretized_rspace_intensity"
    obj = params[obj_name]

    module_alias = embeam.stem.probe.discretized

    if "rise" in params:
        accepted_types = (module_alias.symmetric.rspace.Intensity,
                          module_alias.periodic.rspace.Intensity)
    else:
        accepted_types = (module_alias.periodic.rspace.Intensity,)

    kwargs = {"obj": obj,
              "obj_name": obj_name,
              "accepted_types": accepted_types}
    czekitout.check.if_instance_of_any_accepted_types(**kwargs)

    discretized_rspace_intensity = obj

    return discretized_rspace_intensity



def _check_and_convert_rise(params):
    obj_name = "rise"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}

    current_func_name = "_check_and_convert_rise"

    try:
        rise = czekitout.convert.to_positive_float(**kwargs)
        if rise >= 100:
            err_msg = globals()[current_func_name+"_err_msg_1"]
            raise ValueError(err_msg)
    except:
        try:
            rise = czekitout.convert.to_tuple_of_positive_floats(**kwargs)
            if np.any(np.array(rise) >= 100):
                err_msg = globals()[current_func_name+"_err_msg_1"]
                raise ValueError(err_msg)
        except:
            err_msg = globals()[current_func_name+"_err_msg_1"]
            raise TypeError(err_msg)

    return rise



def _check_and_convert_skip_validation_and_conversion(params):
    module_alias = embeam
    func_alias = module_alias._check_and_convert_skip_validation_and_conversion
    skip_validation_and_conversion = func_alias(params)

    return skip_validation_and_conversion



_module_alias = \
    embeam.gun
_default_rise = \
    60
_default_skip_validation_and_conversion = \
    _module_alias._default_skip_validation_and_conversion



def rise_distance(discretized_rspace_intensity,
                  rise=\
                  _default_rise,
                  skip_validation_and_conversion=\
                  _default_skip_validation_and_conversion):
    r"""Estimate the rise-distance measure of the spatial resolution of the 
    probe of interest for a given rise-distance ratio.

    We define the :math:`\eta` percent to :math:`\left(100-\eta\right)` percent
    rise-distance for a given non-negative bivariate function
    :math:`F\left(x,y\right)` to be

    .. math ::
        R_{\text{rise-distance}}\left(\eta\right)=S^{-1}\left(100-\eta\right)
        -S^{-1}\left(\eta\right),
        :label: rise_distance_in_stem_probe_resolution__1

    where

    .. math ::
        0<\eta<50,
        :label: eta_constraint_in_stem_probe_resolution__1

    :math:`S^{-1}\left(\eta\right)` is the inverse function to

    .. math ::
        S\left(u\right)=100\frac{\int_{-\infty}^{u}dx\,
        \int_{-\infty}^{\infty}dy\,
        \overline{F}\left(r_{xy}\right)}{\int_{-\infty}^{\infty}dx\,
        \int_{-\infty}^{\infty}dy\,\overline{F}\left(r_{xy}\right)},
        :label: integrated_intensity_for_rise_distance_in_stem_probe_resolution__1

    with

    .. math ::
        r_{xy}=\sqrt{x^{2}+y^{2}},
        :label: r_xy_in_stem_probe_resolution__1

    and :math:`\overline{F}\left(r_{xy}\right)` being the azimuthal average of
    :math:`F\left(x,y\right)`:

    .. math ::
        \overline{F}\left(r_{xy}\right)=\frac{1}{2\pi r_{xy}}
        \int_{0}^{2\pi}d\phi\,r_{xy}
        F\left(r_{xy}\cos\left(\phi\right),r_{xy}\sin\left(\phi\right)\right).
        :label: overline_F_in_stem_probe_resolution__1

    In our discussion, it is convenient to define the quantity

    .. math ::
        \Delta_{S}=100-2\eta
        :label: rise_in_stem_probe_resolution__1

    as the “rise”, and to let :math:`p_{\text{probe};\mathbf{R};n_{1},n_{2}}` be
    a discretized real-space probe fractional intensity that samples a
    continuous function
    :math:`\tilde{p}_{\text{probe}}\left(\left.X=x\right|Y=y\right)`:

    .. math ::
        p_{\text{probe};\mathbf{R};n_{1},n_{2}}=
        \tilde{p}_{\text{probe}}\left(\left.X=x_{n_{2}}\right|
        Y=y_{n_{1}}\right),
        :label: p_probe_R_n_1_n_2_in_stem_probe_resolution__1

    where

    .. math ::
        x_{n}=\Delta x\left\{ -\left\lfloor N_{x}/2\right\rfloor +n\right\} ,
        :label: x_n_in_stem_probe_resolution__1

    with :math:`\Delta x` being the :math:`x`-dimension of each pixel, and
    :math:`N_{x}` being the total number of columns of
    :math:`p_{\text{probe};\mathbf{R};n_{1},n_{2}}`; and

    .. math ::
        y_{n}=\Delta y\left\{ \left\lfloor \left(N_{y}-1\right)/2\right\rfloor 
        -n\right\} ,
        :label: y_n_in_stem_probe_resolution__1

    with :math:`\Delta y` being the :math:`y`-dimension of each pixel, and
    :math:`N_{y}` being the total number of rows of
    :math:`p_{\text{probe};\mathbf{R};n_{1},n_{2}}`; and

    .. math ::
        \lim_{\Delta x,\Delta y\to0}
        \lim_{N_{x},N_{y}\to\infty}
        \lim_{N_{f}\to\infty}
        p_{\text{probe};\mathbf{R};n_{1},n_{2}}=
        p_{\text{probe}}\left(\left.X=x_{n_{2}}\right|Y=y_{n_{1}}\right),
        :label: limit_of_p_probe_R_n_1_n_2_in_stem_probe_resolution__1

    with :math:`N_{f}` being the number of points used in the Gauss-Hermite
    quadrature scheme of
    Eq. :eq:`incoherent_r_space_p_probe_in_stem_probe_model_params__2`, and
    :math:`p_{\text{probe}}\left(\left.X=x\right|Y=y\right)` being the
    real-space fractional intensity of the probe for which we want to estimate
    :math:`R_{\text{rise-distance}}\left(\eta\right)`.

    For given :math:`p_{\text{probe};\mathbf{R};n_{1},n_{2}}` and
    :math:`\Delta_{S}` as input, the Python function
    :func:`embeam.stem.probe.resolution.rise_distance` estimates
    :math:`R_{\text{rise-distance}}\left(\eta\right)` for the function

    .. math ::
        F\left(x,y\right)=p_{\text{probe}}\left(\left.X=x\right|Y=y\right).
        :label: function_for_which_to_calculate_rise_distance_in_stem_probe_resolution__1

    The Python function estimates
    :math:`R_{\text{rise-distance}}\left(\eta\right)` by performing a series of
    interpolations and numerical integrations, where the integrands are sampled
    at the points

    .. math ::
        A=\left\{ \left.\left(x_{n_{2}},y_{n_{1}}\right)\right|
        n_{1}\in\left\{ 0,\ldots,N_{y}-1\right\}, 
        n_{2}\in\left\{ 0,\ldots,N_{x}-1\right\} \right\} ,
        :label: points_in_rspace_discretized_wavefunction_in_stem_probe_resolution__1

    [i.e. the sampling points of
    :math:`p_{\text{probe};\mathbf{R};n_{1},n_{2}}`]; and the interpolation
    knots include points in :math:`A`. In the sequence of limits introduced in
    Eq. :eq:`limit_of_p_probe_R_n_1_n_2_in_stem_probe_resolution__1` above,
    :func:`embeam.stem.probe.resolution.rise_distance` should give the exact
    :math:`R_{\text{rise-distance}}\left(\eta\right)` for
    :math:`p_{\text{probe}}\left(\left.X=x\right|Y=y\right)` within machine
    precision.

    See the documentation for the class :class:`embeam.stem.probe.ModelParams`
    for further discussion on probe modelling.

    Parameters
    ----------
    discretized_rspace_intensity : :class:`embeam.stem.probe.discretized.symmetric.rspace.Intensity` | :class:`embeam.stem.probe.discretized.periodic.rspace.Intensity`
        The discretized real-space probe fractional intensity
        :math:`p_{\text{probe};\mathbf{R};n_{1},n_{2}}` described above.
    rise : `float` | `array_like` (`float`, ndim=1), optional
        The value or set of values of the rise :math:`\Delta_{S}`
        [i.e. :eq:`rise_in_stem_probe_resolution__1`] for which to estimate the
        :math:`\eta` percent to :math:`\left(100-\eta\right)` percent
        rise-distance of the probe of interest. Note that the rise must be
        greater than 0, and less than 100.
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
    result : `float` | `array_like` (`float`, ndim=1)
        If the input argument ``rise`` is a floating-point number, then
        ``result`` is the estimate of the :math:`\eta` percent to
        :math:`\left(100-\eta\right)` percent rise-distance of the probe of
        interest for the rise of value ``rise``. Otherwise, if the input
        argument ``rise`` is an array of floating-point numbers, then ``result``
        is an array of floating-point numbers where ``result[i]`` is the
        estimate of the :math:`\eta` percent to :math:`\left(100-\eta\right)`
        percent rise-distance of the probe of interest for the rise of value
        ``rise[i]``, with ``i`` being an integer satisfying ``0<=i<len(rise)``.

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
    result = _rise_distance(**kwargs)

    return result



def _rise_distance(discretized_rspace_intensity, rise):
    F_bar_2d_data = _F_bar_2d_data(discretized_rspace_intensity)

    kwargs = {"discretized_obj_core_attrs": \
              discretized_rspace_intensity.get_core_attrs(deep_copy=False)}
    x_vec = embeam.stem.probe.discretized._x_vec(**kwargs)
    y_vec = embeam.stem.probe.discretized._y_vec(**kwargs)
    
    d_x = x_vec[1] - x_vec[0]
    d_y = -(y_vec[1] - y_vec[0])

    trapezoid = np.trapezoid if hasattr(np, "trapezoid") else np.trapz
    
    integrate_F_bar_2d_wrt_y_data = d_y * trapezoid(F_bar_2d_data, axis=0)
    
    S = np.zeros([x_vec.size])
    for x_idx in range(x_vec.size):
        f2 = integrate_F_bar_2d_wrt_y_data[x_idx]
        if x_idx > 0:
            S[x_idx] += S[x_idx-1] + 0.5 * d_x * (f1+f2)  # Trapezoidal rule.
        f1 = f2
    S *= 100 / S[-1]

    UnivariateSpline = scipy.interpolate.UnivariateSpline

    if isinstance(rise, float):
        eta = (100 - rise) / 2
        S_inv_at_eta = UnivariateSpline(x=x_vec, y=S-eta, s=0).roots()[0]
        S_inv_at_100_minus_eta = UnivariateSpline(x=x_vec,
                                                  y=S-(100-eta),
                                                  s=0).roots()[0]
        result = (S_inv_at_100_minus_eta - S_inv_at_eta).item()
    else:
        result = tuple()
        for idx in range(len(rise)):
            eta = (100 - rise[idx]) / 2
            S_inv_at_eta = UnivariateSpline(x=x_vec, y=S-eta, s=0).roots()[0]
            S_inv_at_100_minus_eta = UnivariateSpline(x=x_vec,
                                                      y=S-(100-eta),
                                                      s=0).roots()[0]
            result += ((S_inv_at_100_minus_eta - S_inv_at_eta).item(),)

    return result



def _F_bar_2d_data(discretized_rspace_intensity):
    discretized_obj_core_attrs = \
        discretized_rspace_intensity.get_core_attrs(deep_copy=False)
    probe_model_params = \
        discretized_obj_core_attrs["probe_model_params"]

    if probe_model_params.is_azimuthally_symmetric:
        discretized_rspace_intensity_signal = \
            discretized_rspace_intensity.get_signal(deep_copy=False)
        F_bar_2d_data = \
            discretized_rspace_intensity_signal.data
    else:
        interpolated_F_bar_1d = \
            _interpolated_F_bar_1d(discretized_rspace_intensity)

        kwargs = {"discretized_obj_core_attrs": discretized_obj_core_attrs}
        x_vec = embeam.stem.probe.discretized._x_vec(**kwargs)
        y_vec = embeam.stem.probe.discretized._y_vec(**kwargs)
        
        F_bar_2d_data = np.zeros([y_vec.size, x_vec.size])

        for x_idx, x_coord in enumerate(x_vec):
            for y_idx, y_coord in enumerate(y_vec):
                r_xy = np.sqrt(x_coord**2 + y_coord**2)
                F_bar_2d_data[y_idx, x_idx] = interpolated_F_bar_1d(r_xy)

    return F_bar_2d_data



def _interpolated_F_bar_1d(discretized_rspace_intensity):
    discretized_rspace_intensity_signal = \
        discretized_rspace_intensity.get_signal(deep_copy=False)
    optional_params = \
        empix.OptionalAzimuthalAveragingParams(center=(0, 0))

    kwargs = \
        {"input_signal": discretized_rspace_intensity_signal,
         "optional_params": optional_params}
    azimuthally_averaged_discretized_rspace_intensity_signal = \
        empix.azimuthally_average(**kwargs)
    
    F_bar_1d = azimuthally_averaged_discretized_rspace_intensity_signal

    offset = F_bar_1d.axes_manager[0].offset
    scale = F_bar_1d.axes_manager[0].scale
    size = F_bar_1d.axes_manager[0].size
        
    interpolated_F_bar_1d = \
        scipy.interpolate.interp1d(x=offset+scale*np.arange(size),
                                   y=F_bar_1d.data,
                                   kind="cubic",
                                   bounds_error=False,
                                   fill_value=0,
                                   assume_sorted=True)

    return interpolated_F_bar_1d



def _check_and_convert_signal_to_noise_ratio(params):
    obj_name = "signal_to_noise_ratio"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}

    current_func_name = "_check_and_convert_signal_to_noise_ratio"
    
    try:
        signal_to_noise_ratio = czekitout.convert.to_positive_float(**kwargs)
    except:
        try:
            func_alias = czekitout.convert.to_tuple_of_positive_floats
            signal_to_noise_ratio = func_alias(**kwargs)
        except:
            err_msg = globals()[current_func_name+"_err_msg_1"]
            raise TypeError(err_msg)

    return signal_to_noise_ratio



_default_signal_to_noise_ratio = 50



def information(discretized_rspace_intensity,
                signal_to_noise_ratio=\
                _default_signal_to_noise_ratio,
                skip_validation_and_conversion=\
                _default_skip_validation_and_conversion):
    r"""Estimate the information resolution of the probe of interest for a given
    signal-to-noise ratio.

    In Ref. [Ishitani1]_, the authors define the information resolution
    :math:`R_{\text{inf}}` of a probe as

    .. math ::
        R_{\text{inf}}=\frac{2}{\sqrt{\pi\rho_{s}}},
        :label: R_inf_in_stem_probe_resolution__1

    where :math:`\rho_{s}` is the information-passing capacity density:

    .. math ::
        \rho_{s}=\frac{1}{2}\int_{0}^{2k_{xy,\max}}dk_{xy}
        \int_{0}^{2\pi}dk_{\phi}\,k_{xy}
        G\left(k_{xy}\cos\left(k_{\phi}\right),
        k_{xy}\sin\left(k_{\phi}\right)\right),
        :label: rho_s_in_stem_probe_resolution__1

    with :math:`k_{xy,\max}` being given by
    Eq. :eq:`k_xy_max_in_stem_probe_model_params__1`,

    .. math ::
        G\left(k_{x},k_{y}\right)=\log_{2}\left[1+\left|\tau\left(k_{x},
        k_{y}\right)\right|^{2}\left\{ S/N\right\} \right],
        :label: G_function_in_stem_probe_resolution__1

    :math:`S/N` being the signal-to-noise ratio, :math:`\tau\left(k_x,
    k_y\right)` being the optical transfer function of the optical system:

    .. math ::
        \tau\left(k_{x},k_{y}\right)=\int_{-\infty}^{\infty}dx\,
        \int_{-\infty}^{\infty}dy\,
        p_{\text{probe}}\left(\left.X=x\right|Y=y\right)
        e^{-2\pi ik_{x}x-2\pi ik_{y}y},
        :label: optical_transfer_function_in_stem_probe_resolution__1

    and :math:`p_{\text{probe}}\left(\left.X=x\right|Y=y\right)` being the
    real-space fractional intensity of the probe.

    In our discussion, it is convenient to let
    :math:`p_{\text{probe};\mathbf{R};n_{1},n_{2}}` be a discretized real-space
    probe fractional intensity that samples a continuous function
    :math:`\tilde{p}_{\text{probe}}\left(\left.X=x\right|Y=y\right)`:

    .. math ::
        p_{\text{probe};\mathbf{R};n_{1},n_{2}}=
        \tilde{p}_{\text{probe}}\left(\left.X=x_{n_{2}}\right|
        Y=y_{n_{1}}\right),
        :label: p_probe_R_n_1_n_2_in_stem_probe_resolution__2

    where

    .. math ::
        x_{n}=\Delta x\left\{ -\left\lfloor N_{x}/2\right\rfloor +n\right\} ,
        :label: x_n_in_stem_probe_resolution__2

    with :math:`\Delta x` being the :math:`x`-dimension of each pixel, and
    :math:`N_{x}` being the total number of columns of
    :math:`p_{\text{probe};\mathbf{R};n_{1},n_{2}}`; and

    .. math ::
        y_{n}=\Delta y\left\{ \left\lfloor \left(N_{y}-1\right)/2\right\rfloor 
        -n\right\} ,
        :label: y_n_in_stem_probe_resolution__2

    with :math:`\Delta y` being the :math:`y`-dimension of each pixel, and
    :math:`N_{y}` being the total number of rows of
    :math:`p_{\text{probe};\mathbf{R};n_{1},n_{2}}`; and

    .. math ::
        \lim_{\Delta x,\Delta y\to0}
        \lim_{N_{x},N_{y}\to\infty}
        \lim_{N_{f}\to\infty}
        p_{\text{probe};\mathbf{R};n_{1},n_{2}}=
        p_{\text{probe}}\left(\left.X=x_{n_{2}}\right|Y=y_{n_{1}}\right),
        :label: limit_of_p_probe_R_n_1_n_2_in_stem_probe_resolution__2

    with :math:`N_{f}` being the number of points used in the Gauss-Hermite
    quadrature scheme of
    Eq. :eq:`incoherent_r_space_p_probe_in_stem_probe_model_params__2`, and
    :math:`p_{\text{probe}}\left(\left.X=x\right|Y=y\right)` being the
    real-space fractional intensity of the probe for which we want to estimate
    :math:`R_{\text{inf}}`.

    For given :math:`p_{\text{probe};\mathbf{R};n_{1},n_{2}}` and :math:`S/N` as
    input, the Python function :func:`embeam.stem.probe.resolution.information`
    estimates :math:`R_{\text{inf}}` for the probe of interest. The Python
    function estimates :math:`R_{\text{inf}}` by performing a series of
    interpolations and numerical integrations, where the integrands are sampled
    at the points

    .. math ::
        A=\left\{ \left.\left(x_{n_{2}},y_{n_{1}}\right)\right|
        n_{1}\in\left\{ 0,\ldots,N_{y}-1\right\}, 
        n_{2}\in\left\{ 0,\ldots,N_{x}-1\right\} \right\} ,
        :label: points_in_rspace_discretized_wavefunction_in_stem_probe_resolution__2

    [i.e. the sampling points of
    :math:`p_{\text{probe};\mathbf{R};n_{1},n_{2}}`]; and the interpolation
    knots include points in :math:`A`. In the sequence of limits introduced in
    Eq. :eq:`limit_of_p_probe_R_n_1_n_2_in_stem_probe_resolution__2` above,
    :func:`embeam.stem.probe.resolution.information` should give the exact
    :math:`R_{\text{inf}}` for the probe of interest within machine precision.
    
    See the documentation for the class :class:`embeam.stem.probe.ModelParams`
    for further discussion on probe modelling.

    Parameters
    ----------
    discretized_rspace_intensity : :class:`embeam.stem.probe.discretized.periodic.rspace.Intensity`
        The discretized real-space probe fractional intensity
        :math:`p_{\text{probe};\mathbf{R};n_{1},n_{2}}` described above.
        Because the calculation the information resolution
        :math:`R_{\text{inf}}` is prohibitively expensive in terms of
        computational time for discretized non-periodic real-space probe
        fractional intensities, :math:`p_{\text{probe};\mathbf{R};n_{1},n_{2}}` 
        must be periodic.
    signal_to_noise_ratio : `float` | `array_like` (`float`, ndim=1), optional
        The value or set of values of the signal-to-noise ratio :math:`S/N` for
        which to estimate the information resolution :math:`R_{\text{inf}}` of
        the probe of interest. Note that the signal-to-noise ratio must be
        greater than 0.
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
    result : `float` | `array_like` (`float`, ndim=1)
        If the input argument ``signal_to_noise_ratio`` is a floating-point
        number, then ``result`` is the estimate of the information resolution
        :math:`R_{\text{inf}}` of the probe of interest for the signal-to-noise
        ratio of value ``signal_to_noise_ratio``. Otherwise, if the input
        argument ``signal_to_noise_ratio`` is an array of floating-point
        numbers, then ``result`` is an array of floating-point numbers where
        ``result[i]`` is the estimate of the :math:`R_{\text{inf}}` of the probe
        of interest for the signal-to-noise ratio of value
        ``signal_to_noise_ratio[i]``, with ``i`` being an integer satisfying
        ``0<=i<len(signal_to_noise_ratio)``.

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
    result = _information(**kwargs)

    return result



def _information(discretized_rspace_intensity, signal_to_noise_ratio):
    k_xy_max = _k_xy_max(discretized_rspace_intensity)
    tau = _optical_transfer_function(discretized_rspace_intensity)

    if isinstance(signal_to_noise_ratio, float):
        kwargs = {"tau": tau,
                  "signal_to_noise_ratio": signal_to_noise_ratio,
                  "k_xy_max": k_xy_max}
        result = _R_inf(**kwargs).item()
    else:
        result = tuple()
        for idx in range(len(signal_to_noise_ratio)):
            kwargs = {"tau": tau,
                      "signal_to_noise_ratio": signal_to_noise_ratio[idx],
                      "k_xy_max": k_xy_max}
            result += (_R_inf(**kwargs).item(),)

    return result



def _k_xy_max(discretized_rspace_intensity):
    discretized_obj_core_attrs = \
        discretized_rspace_intensity.get_core_attrs(deep_copy=False)
    
    kwargs = \
        {"discretized_obj_core_attrs": discretized_obj_core_attrs}
    soft_aperture = \
        embeam.stem.probe.discretized.kspace._SoftAperture(**kwargs)
    k_xy_max = \
        soft_aperture._k_xy_max

    return k_xy_max



def _optical_transfer_function(discretized_rspace_intensity):
    F_bar_2d = discretized_rspace_intensity.get_signal(deep_copy=False)
    
    discretized_obj_core_attrs = \
        discretized_rspace_intensity.get_core_attrs(deep_copy=False)
    
    N_x, N_y = discretized_obj_core_attrs["viewer_dims_in_pixels"]
    d_x, d_y = discretized_obj_core_attrs["pixel_size"]
    d_k_x, d_k_y = (1.0/(N_x*d_x), 1.0/(N_y*d_y))
    k_x_vec = d_k_x * np.arange(-(N_x//2), N_x-(N_x//2))
    k_y_vec = d_k_y * np.arange((N_y-1)//2, (N_y-1)//2-N_y, -1)
    
    temp_signal_data = \
        np.fft.ifftshift(F_bar_2d.data[::-1, :])
    optical_transfer_function_data = \
        np.fft.fftshift(np.fft.rfft2(temp_signal_data))[::-1, :]
    optical_transfer_function_data /= \
        optical_transfer_function_data[(N_y-1)//2, (N_x//2)]
    optical_transfer_function = \
        hyperspy.signals.ComplexSignal2D(data=optical_transfer_function_data)

    axes_labels = (r"$k_x$", r"$k_y$")
    sizes = (N_x, N_y)
    scales = (d_k_x, -d_k_y)
    offsets = (k_x_vec[0], k_y_vec[0])
    units = ("1/Å", "1/Å")

    scales = ((scales[0], -scales[0])
              if abs(scales[0]+scales[1]) < 1e-10
              else scales)

    for axis_idx in range(len(units)):
        name = axes_labels[axis_idx]
        axis = hyperspy.axes.UniformDataAxis(size=sizes[axis_idx],
                                             scale=scales[axis_idx],
                                             offset=offsets[axis_idx],
                                             units=units[axis_idx])
        optical_transfer_function.axes_manager[axis_idx].update_from(axis)
        optical_transfer_function.axes_manager[axis_idx].name = name
            
    return optical_transfer_function



def _R_inf(tau, signal_to_noise_ratio, k_xy_max):
    temp_signal = empix.abs_sq(tau)
    temp_signal.data = np.log2(1 + temp_signal.data * signal_to_noise_ratio)

    kwargs = {"center": (0, 0),
              "radial_range": (0, 2*k_xy_max),
              "title": None}
    optional_params = empix.OptionalAnnularIntegrationParams(**kwargs)

    kwargs = {"input_signal": temp_signal, "optional_params": optional_params}
    rho_s = empix.annularly_integrate(**kwargs).data[0] / 2
    
    R_inf = 2/np.sqrt(np.pi*rho_s)

    return R_inf



###########################
## Define error messages ##
###########################

_check_and_convert_rise_err_msg_1 = \
    ("The object ``rise`` must be either a positive real number less than 100, "
     "or a 1D array of positive real numbers less than 100.")

_check_and_convert_signal_to_noise_ratio_err_msg_1 = \
    ("The object ``signal_to_noise_ratio`` must be either a positive real "
     "number, or a 1D array of positive real numbers.")
