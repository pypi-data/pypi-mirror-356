# -*- coding: utf-8 -*-
# Copyright 2025 Matthew Fitzpatrick.
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
r"""Contains tests for the root of the package :mod:`embeam`.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For operations related to unit tests.
import pytest

# For general array handling.
import numpy as np



# For modelling beams and lenses in electron microscopy.
import embeam



##################################
## Define classes and functions ##
##################################



def generate_gun_model_params():
    kwargs = {"mean_beam_energy": 20,
              "intrinsic_energy_spread": 0.6e-3,
              "accel_voltage_spread": 0}
    gun_model_params = embeam.gun.ModelParams(**kwargs)

    return gun_model_params



def generate_wavelength():
    gun_model_params = generate_gun_model_params()

    kwargs = {"beam_energy": gun_model_params.core_attrs["mean_beam_energy"]}
    wavelength = embeam.wavelength(**kwargs)

    return wavelength



def generate_defocus_aberration():
    m = 2
    d_f = -5000
    wavelength = generate_wavelength()

    kwargs = {"m": m,
              "n": 0,
              "C_mag": (2*np.pi*d_f) / (m*wavelength),
              "C_ang": 0}
    defocus_aberration = embeam.coherent.Aberration(**kwargs)

    return defocus_aberration



def generate_spherical_aberration():
    m = 4
    C_s = 8e-3/1e-10
    wavelength = generate_wavelength()

    kwargs = {"m": m,
              "n": 0,
              "C_mag": (2*np.pi*C_s) / (m*wavelength),
              "C_ang": 0}
    spherical_aberration = embeam.coherent.Aberration(**kwargs)

    return spherical_aberration



def generate_astigmatism_aberration():
    kwargs = {"m": 3,
              "n": 3,
              "C_mag": 75000,
              "C_ang": 0.75}
    astigmatism_aberration = embeam.coherent.Aberration(**kwargs)

    return astigmatism_aberration



def generate_symmetric_and_coherent_aberrations():
    symmetric_and_coherent_aberrations = (generate_defocus_aberration(),
                                          generate_spherical_aberration())

    return symmetric_and_coherent_aberrations



def generate_asymmetric_and_coherent_aberrations():
    asymmetric_and_coherent_aberrations = \
        (generate_symmetric_and_coherent_aberrations()
         + (generate_astigmatism_aberration(),))

    return asymmetric_and_coherent_aberrations



def generate_symmetric_and_coherent_lens_model_params():
    symmetric_and_coherent_aberrations = \
        generate_symmetric_and_coherent_aberrations()

    kwargs = \
        {"coherent_aberrations": symmetric_and_coherent_aberrations,
         "chromatic_aberration_coef": 0,
         "mean_current": 50,
         "std_dev_current": 0}
    symmetric_and_coherent_lens_model_params = \
        embeam.lens.ModelParams(**kwargs)

    return symmetric_and_coherent_lens_model_params



def generate_asymmetric_and_coherent_lens_model_params():
    lens_model_params = generate_symmetric_and_coherent_lens_model_params()
    
    coherent_aberrations = generate_asymmetric_and_coherent_aberrations()

    new_core_attr_subset_candidate = {"coherent_aberrations": \
                                      coherent_aberrations}
    lens_model_params.update(new_core_attr_subset_candidate)

    asymmetric_and_coherent_lens_model_params = lens_model_params

    return asymmetric_and_coherent_lens_model_params



def generate_symmetric_and_incoherent_lens_model_params():
    lens_model_params = generate_symmetric_and_coherent_lens_model_params()
    
    new_core_attr_subset_candidate = {"chromatic_aberration_coef": 8}
    lens_model_params.update(new_core_attr_subset_candidate)

    symmetric_and_incoherent_lens_model_params = lens_model_params

    return symmetric_and_incoherent_lens_model_params



def generate_asymmetric_and_incoherent_lens_model_params():
    lens_model_params = generate_symmetric_and_incoherent_lens_model_params()
    
    coherent_aberrations = \
        generate_asymmetric_and_coherent_aberrations()

    new_core_attr_subset_candidate = {"coherent_aberrations": \
                                      coherent_aberrations}
    lens_model_params.update(new_core_attr_subset_candidate)

    asymmetric_and_incoherent_lens_model_params = lens_model_params

    return asymmetric_and_incoherent_lens_model_params



def generate_symmetric_and_coherent_probe_model_params():
    lens_model_params = generate_symmetric_and_coherent_lens_model_params()

    kwargs = \
        {"lens_model_params": lens_model_params,
         "convergence_semiangle": 4.84,
         "gun_model_params": generate_gun_model_params(),
         "defocal_offset_supersampling": 9}
    symmetric_and_coherent_probe_model_params = \
        embeam.stem.probe.ModelParams(**kwargs)

    return symmetric_and_coherent_probe_model_params



def generate_asymmetric_and_coherent_probe_model_params():
    probe_model_params = generate_symmetric_and_coherent_probe_model_params()

    lens_model_params = generate_asymmetric_and_coherent_lens_model_params()

    new_core_attr_subset_candidate = {"lens_model_params": \
                                      lens_model_params}
    probe_model_params.update(new_core_attr_subset_candidate)

    asymmetric_and_coherent_probe_model_params = probe_model_params

    return asymmetric_and_coherent_probe_model_params



def generate_symmetric_and_incoherent_probe_model_params():
    probe_model_params = generate_symmetric_and_coherent_probe_model_params()

    lens_model_params = generate_symmetric_and_incoherent_lens_model_params()

    new_core_attr_subset_candidate = {"lens_model_params": \
                                      lens_model_params}
    probe_model_params.update(new_core_attr_subset_candidate)

    symmetric_and_incoherent_probe_model_params = probe_model_params

    return symmetric_and_incoherent_probe_model_params



def generate_asymmetric_and_incoherent_probe_model_params():
    probe_model_params = generate_symmetric_and_coherent_probe_model_params()

    lens_model_params = generate_asymmetric_and_incoherent_lens_model_params()

    new_core_attr_subset_candidate = {"lens_model_params": \
                                      lens_model_params}
    probe_model_params.update(new_core_attr_subset_candidate)

    asymmetric_and_incoherent_probe_model_params = probe_model_params

    return asymmetric_and_incoherent_probe_model_params



def generate_symmetric_kspace_probe_wavefunction():
    probe_model_params = generate_symmetric_and_coherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params}
    symmetric_kspace_probe_wavefunction = \
        embeam.stem.probe.kspace.Wavefunction(**kwargs)

    return symmetric_kspace_probe_wavefunction



def generate_asymmetric_kspace_probe_wavefunction():
    probe_model_params = generate_asymmetric_and_coherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params}
    asymmetric_kspace_probe_wavefunction = \
        embeam.stem.probe.kspace.Wavefunction(**kwargs)

    return asymmetric_kspace_probe_wavefunction



def generate_symmetric_and_coherent_kspace_probe_intensity():
    probe_model_params = generate_symmetric_and_coherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params}
    symmetric_and_coherent_kspace_probe_intensity = \
        embeam.stem.probe.kspace.Intensity(**kwargs)

    return symmetric_and_coherent_kspace_probe_intensity



def generate_asymmetric_and_coherent_kspace_probe_intensity():
    probe_model_params = generate_asymmetric_and_coherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params}
    asymmetric_and_coherent_kspace_probe_intensity = \
        embeam.stem.probe.kspace.Intensity(**kwargs)

    return asymmetric_and_coherent_kspace_probe_intensity



def generate_symmetric_and_incoherent_kspace_probe_intensity():
    probe_model_params = generate_symmetric_and_incoherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params}
    symmetric_and_incoherent_kspace_probe_intensity = \
        embeam.stem.probe.kspace.Intensity(**kwargs)

    return symmetric_and_incoherent_kspace_probe_intensity



def generate_asymmetric_and_incoherent_kspace_probe_intensity():
    probe_model_params = generate_asymmetric_and_incoherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params}
    asymmetric_and_incoherent_kspace_probe_intensity = \
        embeam.stem.probe.kspace.Intensity(**kwargs)

    return asymmetric_and_incoherent_kspace_probe_intensity



def generate_symmetric_rspace_probe_wavefunction():
    probe_model_params = generate_symmetric_and_coherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params}
    symmetric_rspace_probe_wavefunction = \
        embeam.stem.probe.symmetric.rspace.Wavefunction(**kwargs)

    return symmetric_rspace_probe_wavefunction



def generate_symmetric_and_coherent_rspace_probe_intensity():
    probe_model_params = generate_symmetric_and_coherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params}
    symmetric_and_coherent_rspace_probe_intensity = \
        embeam.stem.probe.symmetric.rspace.Intensity(**kwargs)

    return symmetric_and_coherent_rspace_probe_intensity



def generate_symmetric_and_incoherent_rspace_probe_intensity():
    probe_model_params = generate_symmetric_and_incoherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params}
    symmetric_and_incoherent_rspace_probe_intensity = \
        embeam.stem.probe.symmetric.rspace.Intensity(**kwargs)

    return symmetric_and_incoherent_rspace_probe_intensity



def generate_kspace_pixel_size():
    L_x = 250
    L_y = 250

    d_k_x = 1 / L_x
    d_k_y = 1 / L_y

    kspace_pixel_size = (d_k_x, d_k_y)

    return kspace_pixel_size



def generate_viewer_dims_in_pixels():
    viewer_dims_in_pixels = (64, 64)

    return viewer_dims_in_pixels



def generate_rspace_pixel_size():
    kspace_pixel_size = generate_kspace_pixel_size()
    viewer_dims_in_pixels = generate_viewer_dims_in_pixels()

    L_x = 1/kspace_pixel_size[0]
    L_y = 1/kspace_pixel_size[1]

    d_x = L_x/viewer_dims_in_pixels[0]
    d_y = L_y/viewer_dims_in_pixels[1]

    rspace_pixel_size = (d_x, d_y)

    return rspace_pixel_size



def generate_symmetric_discretized_kspace_probe_wavefunction():
    probe_model_params = generate_symmetric_and_coherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params,
         "pixel_size": generate_kspace_pixel_size(),
         "viewer_dims_in_pixels": generate_viewer_dims_in_pixels()}
    symmetric_discretized_kspace_probe_wavefunction = \
        embeam.stem.probe.discretized.kspace.Wavefunction(**kwargs)

    return symmetric_discretized_kspace_probe_wavefunction



def generate_asymmetric_discretized_kspace_probe_wavefunction():
    probe_model_params = generate_asymmetric_and_coherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params,
         "pixel_size": generate_kspace_pixel_size(),
         "viewer_dims_in_pixels": generate_viewer_dims_in_pixels()}
    asymmetric_discretized_kspace_probe_wavefunction = \
        embeam.stem.probe.discretized.kspace.Wavefunction(**kwargs)

    return asymmetric_discretized_kspace_probe_wavefunction



def generate_symmetric_and_coherent_discretized_kspace_probe_intensity():
    probe_model_params = generate_symmetric_and_coherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params,
         "pixel_size": generate_kspace_pixel_size(),
         "viewer_dims_in_pixels": generate_viewer_dims_in_pixels()}
    symmetric_and_coherent_discretized_kspace_probe_intensity = \
        embeam.stem.probe.discretized.kspace.Intensity(**kwargs)

    return symmetric_and_coherent_discretized_kspace_probe_intensity



def generate_asymmetric_and_coherent_discretized_kspace_probe_intensity():
    probe_model_params = generate_asymmetric_and_coherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params,
         "pixel_size": generate_kspace_pixel_size(),
         "viewer_dims_in_pixels": generate_viewer_dims_in_pixels()}
    asymmetric_and_coherent_discretized_kspace_probe_intensity = \
        embeam.stem.probe.discretized.kspace.Intensity(**kwargs)

    return asymmetric_and_coherent_discretized_kspace_probe_intensity



def generate_symmetric_and_incoherent_discretized_kspace_probe_intensity():
    probe_model_params = generate_symmetric_and_incoherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params,
         "pixel_size": generate_kspace_pixel_size(),
         "viewer_dims_in_pixels": generate_viewer_dims_in_pixels()}
    symmetric_and_incoherent_discretized_kspace_probe_intensity = \
        embeam.stem.probe.discretized.kspace.Intensity(**kwargs)

    return symmetric_and_incoherent_discretized_kspace_probe_intensity



def generate_asymmetric_and_incoherent_discretized_kspace_probe_intensity():
    probe_model_params = generate_asymmetric_and_incoherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params,
         "pixel_size": generate_kspace_pixel_size(),
         "viewer_dims_in_pixels": generate_viewer_dims_in_pixels()}
    asymmetric_and_incoherent_discretized_kspace_probe_intensity = \
        embeam.stem.probe.discretized.kspace.Intensity(**kwargs)

    return asymmetric_and_incoherent_discretized_kspace_probe_intensity



def generate_symmetric_discretized_rspace_probe_wavefunction():
    probe_model_params = generate_symmetric_and_coherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params,
         "pixel_size": generate_rspace_pixel_size(),
         "viewer_dims_in_pixels": generate_viewer_dims_in_pixels()}
    symmetric_discretized_rspace_probe_wavefunction = \
        embeam.stem.probe.discretized.symmetric.rspace.Wavefunction(**kwargs)

    return symmetric_discretized_rspace_probe_wavefunction



def generate_symmetric_and_coherent_discretized_rspace_probe_intensity():
    probe_model_params = generate_symmetric_and_coherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params,
         "pixel_size": generate_rspace_pixel_size(),
         "viewer_dims_in_pixels": generate_viewer_dims_in_pixels()}
    symmetric_and_coherent_discretized_rspace_probe_intensity = \
        embeam.stem.probe.discretized.symmetric.rspace.Intensity(**kwargs)

    return symmetric_and_coherent_discretized_rspace_probe_intensity



def generate_symmetric_and_incoherent_discretized_rspace_probe_intensity():
    probe_model_params = generate_symmetric_and_incoherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params,
         "pixel_size": generate_rspace_pixel_size(),
         "viewer_dims_in_pixels": generate_viewer_dims_in_pixels()}
    symmetric_and_incoherent_discretized_rspace_probe_intensity = \
        embeam.stem.probe.discretized.symmetric.rspace.Intensity(**kwargs)

    return symmetric_and_incoherent_discretized_rspace_probe_intensity



def generate_symmetric_discretized_periodic_rspace_probe_wavefunction():
    probe_model_params = generate_symmetric_and_coherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params,
         "pixel_size": generate_rspace_pixel_size(),
         "viewer_dims_in_pixels": generate_viewer_dims_in_pixels()}
    symmetric_discretized_periodic_rspace_probe_wavefunction = \
        embeam.stem.probe.discretized.periodic.rspace.Wavefunction(**kwargs)

    return symmetric_discretized_periodic_rspace_probe_wavefunction



def generate_asymmetric_discretized_periodic_rspace_probe_wavefunction():
    probe_model_params = generate_asymmetric_and_coherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params,
         "pixel_size": generate_rspace_pixel_size(),
         "viewer_dims_in_pixels": generate_viewer_dims_in_pixels()}
    asymmetric_discretized_periodic_rspace_probe_wavefunction = \
        embeam.stem.probe.discretized.periodic.rspace.Wavefunction(**kwargs)

    return asymmetric_discretized_periodic_rspace_probe_wavefunction



def generate_discretized_periodic_rspace_probe_intensity_1():
    probe_model_params = generate_symmetric_and_coherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params,
         "pixel_size": generate_rspace_pixel_size(),
         "viewer_dims_in_pixels": generate_viewer_dims_in_pixels()}
    discretized_periodic_rspace_probe_intensity_1 = \
        embeam.stem.probe.discretized.periodic.rspace.Intensity(**kwargs)

    return discretized_periodic_rspace_probe_intensity_1



def generate_discretized_periodic_rspace_probe_intensity_2():
    probe_model_params = generate_asymmetric_and_coherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params,
         "pixel_size": generate_rspace_pixel_size(),
         "viewer_dims_in_pixels": generate_viewer_dims_in_pixels()}
    discretized_periodic_rspace_probe_intensity_2 = \
        embeam.stem.probe.discretized.periodic.rspace.Intensity(**kwargs)

    return discretized_periodic_rspace_probe_intensity_2



def generate_discretized_periodic_rspace_probe_intensity_3():
    probe_model_params = generate_symmetric_and_incoherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params,
         "pixel_size": generate_rspace_pixel_size(),
         "viewer_dims_in_pixels": generate_viewer_dims_in_pixels()}
    discretized_periodic_rspace_probe_intensity_3 = \
        embeam.stem.probe.discretized.periodic.rspace.Intensity(**kwargs)

    return discretized_periodic_rspace_probe_intensity_3



def generate_discretized_periodic_rspace_probe_intensity_4():
    probe_model_params = generate_asymmetric_and_incoherent_probe_model_params()

    kwargs = \
        {"probe_model_params": probe_model_params,
         "pixel_size": generate_rspace_pixel_size(),
         "viewer_dims_in_pixels": generate_viewer_dims_in_pixels()}
    discretized_periodic_rspace_probe_intensity_4 = \
        embeam.stem.probe.discretized.periodic.rspace.Intensity(**kwargs)

    return discretized_periodic_rspace_probe_intensity_4



def test_1_of_discretized_periodic_rspace_probe_intensities():
    intensities = \
        (generate_discretized_periodic_rspace_probe_intensity_1(),
         generate_discretized_periodic_rspace_probe_intensity_2(),
         generate_discretized_periodic_rspace_probe_intensity_3(),
         generate_discretized_periodic_rspace_probe_intensity_4())

    cls_alias = embeam.stem.probe.discretized.periodic.rspace.Intensity
    
    kwargs = {"serializable_rep": intensities[0].pre_serialize()}
    cls_alias.de_pre_serialize(**kwargs)

    new_core_attr_subset_candidate = {"pixel_size": (0.5, 0.75)}
    intensities[1].update(new_core_attr_subset_candidate)

    intensities[0].validation_and_conversion_funcs
    intensities[0].pre_serialization_funcs
    intensities[0].de_pre_serialization_funcs
        
    for intensity in intensities:
        intensity.signal
        intensity.signal

    kwargs = \
        {"discretized_wavefunction": \
         generate_symmetric_discretized_periodic_rspace_probe_wavefunction()}
    intensities += \
        (cls_alias.construct_from_discretized_wavefunction(**kwargs),)

    abs_diff = np.abs(intensities[0].signal.data-intensities[-1]._signal.data)
    assert (abs_diff.max() < 1e-10)

    assert (intensities[0].is_azimuthally_symmetric == True)
    assert (intensities[0].is_coherent == True)

    assert (intensities[1].is_azimuthally_symmetric == False)
    assert (intensities[1].is_coherent == True)

    assert (intensities[2].is_azimuthally_symmetric == True)
    assert (intensities[2].is_coherent == False)

    assert (intensities[3].is_azimuthally_symmetric == False)
    assert (intensities[3].is_coherent == False)

    assert (intensities[4].is_azimuthally_symmetric == True)
    assert (intensities[4].is_coherent == True)

    return None



def test_1_of_discretized_periodic_rspace_probe_wavefunctions():
    wavefunctions = \
        (generate_symmetric_discretized_periodic_rspace_probe_wavefunction(),
         generate_asymmetric_discretized_periodic_rspace_probe_wavefunction())

    cls_alias = embeam.stem.probe.discretized.periodic.rspace.Wavefunction
    
    kwargs = {"serializable_rep": wavefunctions[0].pre_serialize()}
    cls_alias.de_pre_serialize(**kwargs)

    new_core_attr_subset_candidate = {"pixel_size": (0.5, 0.75)}
    wavefunctions[1].update(new_core_attr_subset_candidate)

    wavefunctions[0].validation_and_conversion_funcs
    wavefunctions[0].pre_serialization_funcs
    wavefunctions[0].de_pre_serialization_funcs
        
    for wavefunction in wavefunctions:
        wavefunction.signal
        wavefunction.signal

    assert (wavefunctions[0].is_azimuthally_symmetric == True)

    assert (wavefunctions[1].is_azimuthally_symmetric == False)

    return None



def test_1_of_discretized_symmetric_rspace_probe_intensities():
    intensities = \
        (generate_symmetric_and_coherent_discretized_rspace_probe_intensity(),
         generate_symmetric_and_incoherent_discretized_rspace_probe_intensity())

    cls_alias = embeam.stem.probe.discretized.symmetric.rspace.Intensity
    
    kwargs = {"serializable_rep": intensities[0].pre_serialize()}
    cls_alias.de_pre_serialize(**kwargs)

    new_core_attr_subset_candidate = {"pixel_size": (0.5, 0.75)}
    intensities[1].update(new_core_attr_subset_candidate)

    intensities[0].validation_and_conversion_funcs
    intensities[0].pre_serialization_funcs
    intensities[0].de_pre_serialization_funcs
        
    for intensity in intensities:
        intensity.signal
        intensity.signal

    kwargs = \
        {"discretized_wavefunction": \
         generate_symmetric_discretized_rspace_probe_wavefunction()}
    intensities += \
        (cls_alias.construct_from_discretized_wavefunction(**kwargs),)

    abs_diff = np.abs(intensities[0].signal.data-intensities[-1]._signal.data)
    assert (abs_diff.max() < 1e-10)

    assert (intensities[0].is_coherent == True)

    assert (intensities[1].is_coherent == False)

    assert (intensities[2].is_coherent == True)

    return None



def test_1_of_discretized_symmetric_rspace_probe_wavefunctions():
    wavefunction = generate_symmetric_discretized_rspace_probe_wavefunction()

    cls_alias = embeam.stem.probe.discretized.symmetric.rspace.Wavefunction
    
    kwargs = {"serializable_rep": wavefunction.pre_serialize()}
    cls_alias.de_pre_serialize(**kwargs)

    new_core_attr_subset_candidate = {"pixel_size": (0.5, 0.75)}
    wavefunction.update(new_core_attr_subset_candidate)

    wavefunction.validation_and_conversion_funcs
    wavefunction.pre_serialization_funcs
    wavefunction.de_pre_serialization_funcs
        
    wavefunction.signal
    wavefunction.signal

    return None



def test_1_of_discretized_kspace_probe_intensities():
    format_arg_sets = (("", ""), ("a", ""), ("", "in"), ("a", "in"))
    unformatted_func_name = ("generate_{}symmetric_and_{}coherent"
                             "_discretized_kspace_probe_intensity")
    intensities = tuple()
    for format_arg_set in format_arg_sets:
        func_name = unformatted_func_name.format(*format_arg_set)
        intensities += (globals()[func_name](),)

    cls_alias = embeam.stem.probe.discretized.kspace.Intensity
    
    kwargs = {"serializable_rep": intensities[0].pre_serialize()}
    cls_alias.de_pre_serialize(**kwargs)

    new_core_attr_subset_candidate = {"pixel_size": (0.5, 0.75)}
    intensities[1].update(new_core_attr_subset_candidate)

    intensities[0].validation_and_conversion_funcs
    intensities[0].pre_serialization_funcs
    intensities[0].de_pre_serialization_funcs
        
    for intensity in intensities:
        intensity.signal
        intensity.signal

    kwargs = \
        {"discretized_wavefunction": \
         generate_symmetric_discretized_kspace_probe_wavefunction()}
    intensities += \
        (cls_alias.construct_from_discretized_wavefunction(**kwargs),)

    abs_diff = np.abs(intensities[0].signal.data-intensities[-1].signal.data)
    assert (abs_diff.max() < 1e-10)

    assert (intensities[0].is_azimuthally_symmetric == True)
    assert (intensities[0].is_coherent == True)

    assert (intensities[1].is_azimuthally_symmetric == False)
    assert (intensities[1].is_coherent == True)

    assert (intensities[2].is_azimuthally_symmetric == True)
    assert (intensities[2].is_coherent == False)

    assert (intensities[3].is_azimuthally_symmetric == False)
    assert (intensities[3].is_coherent == False)

    assert (intensities[4].is_azimuthally_symmetric == True)
    assert (intensities[4].is_coherent == True)

    return None



def test_1_of_discretized_kspace_probe_wavefunctions():
    wavefunctions = \
        (generate_symmetric_discretized_kspace_probe_wavefunction(),
         generate_asymmetric_discretized_kspace_probe_wavefunction())

    cls_alias = embeam.stem.probe.discretized.kspace.Wavefunction
    
    kwargs = {"serializable_rep": wavefunctions[0].pre_serialize()}
    cls_alias.de_pre_serialize(**kwargs)

    new_core_attr_subset_candidate = {"pixel_size": (0.5, 0.75)}
    wavefunctions[1].update(new_core_attr_subset_candidate)

    wavefunctions[0].validation_and_conversion_funcs
    wavefunctions[0].pre_serialization_funcs
    wavefunctions[0].de_pre_serialization_funcs
        
    for wavefunction in wavefunctions:
        wavefunction.signal
        wavefunction.signal

    assert (wavefunctions[0].is_azimuthally_symmetric == True)

    assert (wavefunctions[1].is_azimuthally_symmetric == False)

    return None



def test_1_of_symmetric_rspace_probe_intensities():
    intensities = \
        (generate_symmetric_and_coherent_rspace_probe_intensity(),
         generate_symmetric_and_incoherent_rspace_probe_intensity())

    cls_alias = embeam.stem.probe.symmetric.rspace.Intensity
    
    kwargs = {"serializable_rep": intensities[0].pre_serialize()}
    cls_alias.de_pre_serialize(**kwargs)

    new_core_attr_subset_candidate = {"probe_model_params": None}
    intensities[0].update(new_core_attr_subset_candidate)

    intensities[0].validation_and_conversion_funcs
    intensities[0].pre_serialization_funcs
    intensities[0].de_pre_serialization_funcs
        
    assert (intensities[0].is_coherent == True)

    assert (intensities[1].is_coherent == False)

    for skip_validation_and_conversion in (True, False):
        kwargs = \
            {"x": 0,
             "y": 0,
             "skip_validation_and_conversion": skip_validation_and_conversion}
        _ = \
            intensities[0].eval(**kwargs)

    kwargs = {"coherent_aberrations": (generate_spherical_aberration(),)}
    lens_model_params = embeam.lens.ModelParams(**kwargs)

    kwargs = {"lens_model_params": lens_model_params}
    probe_model_params = embeam.stem.probe.ModelParams(**kwargs)

    kwargs = {"probe_model_params": probe_model_params}
    cls_alias(**kwargs)

    return None



def test_1_of_symmetric_rspace_probe_wavefunctions():
    wavefunction = generate_symmetric_rspace_probe_wavefunction()

    cls_alias = embeam.stem.probe.symmetric.rspace.Wavefunction
    
    kwargs = {"serializable_rep": wavefunction.pre_serialize()}
    cls_alias.de_pre_serialize(**kwargs)

    new_core_attr_subset_candidate = {"probe_model_params": None}
    wavefunction.update(new_core_attr_subset_candidate)

    wavefunction.validation_and_conversion_funcs
    wavefunction.pre_serialization_funcs
    wavefunction.de_pre_serialization_funcs

    for skip_validation_and_conversion in (True, False):
        kwargs = \
            {"x": 0,
             "y": 0,
             "skip_validation_and_conversion": skip_validation_and_conversion}
        _ = \
            wavefunction.eval(**kwargs)

    probe_model_param_sets = \
        (generate_asymmetric_and_coherent_probe_model_params(),
         generate_symmetric_and_incoherent_probe_model_params())

    for probe_model_param_set in probe_model_param_sets:
        with pytest.raises(ValueError) as err_info:
            kwargs = {"probe_model_params": probe_model_param_set}
            cls_alias(**kwargs)

    return None



def test_1_of_kspace_probe_intensities():
    format_arg_sets = (("", ""), ("a", ""), ("", "in"), ("a", "in"))
    unformatted_func_name = ("generate_{}symmetric_and_{}coherent"
                             "_kspace_probe_intensity")
    intensities = tuple()
    for format_arg_set in format_arg_sets:
        func_name = unformatted_func_name.format(*format_arg_set)
        intensities += (globals()[func_name](),)

    cls_alias = embeam.stem.probe.kspace.Intensity
    
    kwargs = {"serializable_rep": intensities[0].pre_serialize()}
    cls_alias.de_pre_serialize(**kwargs)

    new_core_attr_subset_candidate = {"probe_model_params": None}
    intensities[0].update(new_core_attr_subset_candidate)

    intensities[0].validation_and_conversion_funcs
    intensities[0].pre_serialization_funcs
    intensities[0].de_pre_serialization_funcs

    assert (intensities[0].is_azimuthally_symmetric == True)
    assert (intensities[0].is_coherent == True)

    assert (intensities[1].is_azimuthally_symmetric == False)
    assert (intensities[1].is_coherent == True)

    assert (intensities[2].is_azimuthally_symmetric == True)
    assert (intensities[2].is_coherent == False)

    assert (intensities[3].is_azimuthally_symmetric == False)
    assert (intensities[3].is_coherent == False)

    for skip_validation_and_conversion in (True, False):
        kwargs = \
            {"k_x": 0,
             "k_y": 0,
             "skip_validation_and_conversion": skip_validation_and_conversion}
        _ = \
            intensities[0].eval(**kwargs)

    return None



def test_1_of_kspace_probe_wavefunctions():
    wavefunctions = (generate_symmetric_kspace_probe_wavefunction(),
                     generate_asymmetric_kspace_probe_wavefunction())

    cls_alias = embeam.stem.probe.kspace.Wavefunction
    
    kwargs = {"serializable_rep": wavefunctions[0].pre_serialize()}
    cls_alias.de_pre_serialize(**kwargs)

    new_core_attr_subset_candidate = {"probe_model_params": None}
    wavefunctions[0].update(new_core_attr_subset_candidate)

    wavefunctions[0].validation_and_conversion_funcs
    wavefunctions[0].pre_serialization_funcs
    wavefunctions[0].de_pre_serialization_funcs

    assert (wavefunctions[0].is_azimuthally_symmetric == True)

    assert (wavefunctions[1].is_azimuthally_symmetric == False)

    for skip_validation_and_conversion in (True, False):
        kwargs = \
            {"k_x": 0,
             "k_y": 0,
             "skip_validation_and_conversion": skip_validation_and_conversion}
        _ = \
            wavefunctions[0].eval(**kwargs)

    with pytest.raises(ValueError) as err_info:
        kwargs = {"probe_model_params": \
                  generate_symmetric_and_incoherent_probe_model_params()}
        cls_alias(**kwargs)

    return None



def test_1_of_probe_model_param_sets():
    probe_model_param_sets = \
        (generate_symmetric_and_coherent_probe_model_params(),
         generate_asymmetric_and_coherent_probe_model_params(),
         generate_symmetric_and_incoherent_probe_model_params(),
         generate_asymmetric_and_incoherent_probe_model_params())

    cls_alias = embeam.stem.probe.ModelParams
    
    kwargs = {"serializable_rep": probe_model_param_sets[0].pre_serialize()}
    cls_alias.de_pre_serialize(**kwargs)

    new_core_attr_subset_candidate = {"convergence_semiangle": 5}
    probe_model_param_sets[1].update(new_core_attr_subset_candidate)

    probe_model_param_sets[0].validation_and_conversion_funcs
    probe_model_param_sets[0].pre_serialization_funcs
    probe_model_param_sets[0].de_pre_serialization_funcs
        
    assert (probe_model_param_sets[0].is_azimuthally_symmetric == True)
    assert (probe_model_param_sets[0].is_coherent == True)

    assert (probe_model_param_sets[1].is_azimuthally_symmetric == False)
    assert (probe_model_param_sets[1].is_coherent == True)

    assert (probe_model_param_sets[2].is_azimuthally_symmetric == True)
    assert (probe_model_param_sets[2].is_coherent == False)

    assert (probe_model_param_sets[3].is_azimuthally_symmetric == False)
    assert (probe_model_param_sets[3].is_coherent == False)

    return None



def test_1_of_coherent_aberrations():
    coherent_aberrations = (generate_defocus_aberration(),
                            generate_spherical_aberration(),
                            generate_astigmatism_aberration())

    cls_alias = embeam.coherent.Aberration
    
    kwargs = {"serializable_rep": coherent_aberrations[0].pre_serialize()}
    cls_alias.de_pre_serialize(**kwargs)

    new_core_attr_subset_candidate = {"C_mag": 1}
    coherent_aberrations[0].update(new_core_attr_subset_candidate)

    coherent_aberrations[0].validation_and_conversion_funcs
    coherent_aberrations[0].pre_serialization_funcs
    coherent_aberrations[0].de_pre_serialization_funcs
        
    assert (coherent_aberrations[0].is_azimuthally_symmetric == True)

    assert (coherent_aberrations[1].is_azimuthally_symmetric == True)

    assert (coherent_aberrations[2].is_azimuthally_symmetric == False)

    return None



def test_1_of_phase_deviations():
    coherent_aberrations = (generate_defocus_aberration(),
                            generate_spherical_aberration(),
                            generate_astigmatism_aberration())

    kwargs = {"beam_energy": 30,
              "coherent_aberrations": coherent_aberrations,
              "defocal_offset": 0.5}
    cls_alias = embeam.coherent.PhaseDeviation
    phase_deviation = cls_alias(**kwargs)
    
    kwargs = {"serializable_rep": phase_deviation.pre_serialize()}
    cls_alias.de_pre_serialize(**kwargs)

    phase_deviation.validation_and_conversion_funcs
    phase_deviation.pre_serialization_funcs
    phase_deviation.de_pre_serialization_funcs

    assert (phase_deviation.is_azimuthally_symmetric == False)

    with pytest.raises(ValueError) as err_info:
        new_core_attr_subset_candidate = {"coherent_aberrations": \
                                          2*coherent_aberrations[:1]}
        phase_deviation.update(new_core_attr_subset_candidate)

    new_core_attr_subset_candidate = {"coherent_aberrations": \
                                      coherent_aberrations[:2]}
    phase_deviation.update(new_core_attr_subset_candidate)

    assert (phase_deviation.is_azimuthally_symmetric == True)

    for skip_validation_and_conversion in (True, False):
        kwargs = \
            {"k_x": 0,
             "k_y": 0,
             "skip_validation_and_conversion": skip_validation_and_conversion}
        _ = \
            phase_deviation.eval(**kwargs)

    with pytest.raises(ValueError) as err_info:
        kwargs = {"k_x": 0.0, "k_y": [1, 0]}
        phase_deviation.eval(**kwargs)

    with pytest.raises(TypeError) as err_info:
        kwargs = {"k_x":10.0j, "k_y": 0}
        phase_deviation.eval(**kwargs)

    return None



def test_1_of_rise_distance_resolution():
    intensities = \
        (generate_symmetric_and_coherent_discretized_rspace_probe_intensity(),
         generate_discretized_periodic_rspace_probe_intensity_1(),
         generate_symmetric_and_coherent_discretized_kspace_probe_intensity(),
         generate_discretized_periodic_rspace_probe_intensity_2())

    func_alias = embeam.stem.probe.resolution.rise_distance

    kwargs = {"discretized_rspace_intensity": intensities[0], "rise": 20}
    assert (type(func_alias(**kwargs)) is float)

    kwargs = {"discretized_rspace_intensity": intensities[1], "rise": (20, 40)}
    assert (type(func_alias(**kwargs)) is tuple)

    kwargs = {"discretized_rspace_intensity": intensities[3],
              "rise": 20.0,
              "skip_validation_and_conversion": True}
    func_alias(**kwargs)

    with pytest.raises(TypeError) as err_info:
        kwargs = {"discretized_rspace_intensity": intensities[2], "rise": 20}
        func_alias(**kwargs)

    with pytest.raises(TypeError) as err_info:
        kwargs = {"discretized_rspace_intensity": intensities[0], "rise": 200}
        func_alias(**kwargs)

    with pytest.raises(TypeError) as err_info:
        kwargs = {"discretized_rspace_intensity": intensities[0], "rise": -10}
        func_alias(**kwargs)

    with pytest.raises(TypeError) as err_info:
        kwargs = {"discretized_rspace_intensity": intensities[0],
                  "rise": (1, 200)}
        func_alias(**kwargs)

    with pytest.raises(TypeError) as err_info:
        kwargs = {"discretized_rspace_intensity": intensities[0],
                  "rise": (-1, 200)}
        func_alias(**kwargs)

    return None



def test_1_of_information_resolution():
    intensities = \
        (generate_symmetric_and_coherent_discretized_rspace_probe_intensity(),
         generate_discretized_periodic_rspace_probe_intensity_1())

    func_alias = embeam.stem.probe.resolution.information

    kwargs = {"discretized_rspace_intensity": intensities[1],
              "signal_to_noise_ratio": 20}
    assert (type(func_alias(**kwargs)) is float)

    kwargs = {"discretized_rspace_intensity": intensities[1],
              "signal_to_noise_ratio": (20, 40)}
    assert (type(func_alias(**kwargs)) is tuple)

    kwargs = {"discretized_rspace_intensity": intensities[0],
              "signal_to_noise_ratio": 20.0,
              "skip_validation_and_conversion": True}
    func_alias(**kwargs)

    with pytest.raises(TypeError) as err_info:
        kwargs = {"discretized_rspace_intensity": intensities[0],
                  "signal_to_noise_ratio": 20}
        func_alias(**kwargs)

    with pytest.raises(TypeError) as err_info:
        kwargs = {"discretized_rspace_intensity": intensities[1],
                  "signal_to_noise_ratio": -10}
        func_alias(**kwargs)

    with pytest.raises(TypeError) as err_info:
        kwargs = {"discretized_rspace_intensity": intensities[1],
                  "signal_to_noise_ratio": (-1, 200)}
        func_alias(**kwargs)

    return None



###########################
## Define error messages ##
###########################
