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
r"""Contains classes representing discretized wavefunctions and fractional
intensities of probes.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For general array handling.
import numpy as np

# For converting objects.
import czekitout.convert

# For creating hyperspy signals.
import hyperspy.axes



# Import child modules and packages of current package.
import embeam.stem.probe.discretized.kspace
import embeam.stem.probe.discretized.symmetric
import embeam.stem.probe.discretized.periodic



##################################
## Define classes and functions ##
##################################

# List of public objects in objects.
__all__ = []



def _check_and_convert_pixel_size(params):
    obj_name = "pixel_size"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    pixel_size = czekitout.convert.to_pair_of_positive_floats(**kwargs)

    return pixel_size



def _pre_serialize_pixel_size(pixel_size):
    obj_to_pre_serialize = pixel_size
    serializable_rep = obj_to_pre_serialize
    
    return serializable_rep



def _de_pre_serialize_pixel_size(serializable_rep):
    pixel_size = serializable_rep

    return pixel_size



def _check_and_convert_viewer_dims_in_pixels(params):
    obj_name = \
        "viewer_dims_in_pixels"
    kwargs = \
        {"obj": params[obj_name], "obj_name": obj_name}
    viewer_dims_in_pixels = \
        czekitout.convert.to_pair_of_positive_ints(**kwargs)

    return viewer_dims_in_pixels



def _pre_serialize_viewer_dims_in_pixels(viewer_dims_in_pixels):
    obj_to_pre_serialize = viewer_dims_in_pixels
    serializable_rep = obj_to_pre_serialize
    
    return serializable_rep



def _de_pre_serialize_viewer_dims_in_pixels(serializable_rep):
    viewer_dims_in_pixels = serializable_rep

    return viewer_dims_in_pixels



def _k_x_vec(discretized_obj_core_attrs):
    d_k_x = discretized_obj_core_attrs["pixel_size"][0]
    N_x = discretized_obj_core_attrs["viewer_dims_in_pixels"][0]
    k_x_vec = d_k_x * np.arange(-(N_x//2), N_x-(N_x//2))

    return k_x_vec



def _k_y_vec(discretized_obj_core_attrs):
    d_k_y = discretized_obj_core_attrs["pixel_size"][1]
    N_y = discretized_obj_core_attrs["viewer_dims_in_pixels"][1]
    k_y_vec = d_k_y * np.arange((N_y-1)//2, (N_y-1)//2-N_y, -1)

    return k_y_vec



def _update_kspace_signal_axes(signal, discretized_obj_core_attrs):
    d_k_x, d_k_y = discretized_obj_core_attrs["pixel_size"]
    N_x, N_y = discretized_obj_core_attrs["viewer_dims_in_pixels"]

    axes_labels = (r"$k_x$", r"$k_y$")
    sizes = (N_x, N_y)
    scales = (d_k_x, -d_k_y)
    offsets = (_k_x_vec(discretized_obj_core_attrs)[0],
               _k_y_vec(discretized_obj_core_attrs)[0])
    units = ("1/Å", "1/Å")

    if abs(scales[0]+scales[1]) < 1e-10:
        scales = (scales[0], -scales[0])
        
    for axis_idx in range(len(units)):
        axis = hyperspy.axes.UniformDataAxis(size=sizes[axis_idx],
                                             scale=scales[axis_idx],
                                             offset=offsets[axis_idx])
        signal.axes_manager[axis_idx].update_from(axis)
        signal.axes_manager[axis_idx].name = axes_labels[axis_idx]
        signal.axes_manager[axis_idx].units = units[axis_idx]
            
    return None



def _x_vec(discretized_obj_core_attrs):
    d_x = discretized_obj_core_attrs["pixel_size"][0]
    N_x = discretized_obj_core_attrs["viewer_dims_in_pixels"][0]
    x_vec = d_x * np.arange(-(N_x//2), N_x-(N_x//2))
        
    return x_vec
        
        
        
def _y_vec(discretized_obj_core_attrs):
    d_y = discretized_obj_core_attrs["pixel_size"][1]
    N_y = discretized_obj_core_attrs["viewer_dims_in_pixels"][1]
    y_vec = d_y * np.arange((N_y-1)//2, (N_y-1)//2-N_y, -1)
        
    return y_vec



def _r_samples(discretized_obj_core_attrs):
    dr = min(discretized_obj_core_attrs["pixel_size"]) / 2
        
    max_abs_x = np.amax(np.abs(_x_vec(discretized_obj_core_attrs)))
    max_abs_y = np.amax(np.abs(_y_vec(discretized_obj_core_attrs)))
    r_max = np.linalg.norm([max_abs_x, max_abs_y])
        
    r_samples = np.arange(0, r_max+dr, dr)
        
    return r_samples



def _r_grid(discretized_obj_core_attrs):
    x_vec = _x_vec(discretized_obj_core_attrs)
    y_vec = _y_vec(discretized_obj_core_attrs)
    pair_of_1d_coord_arrays = (x_vec, y_vec)

    x_grid, y_grid = np.meshgrid(*pair_of_1d_coord_arrays, indexing="xy")
    r_grid = np.sqrt(x_grid*x_grid + y_grid*y_grid)

    return r_grid



def _update_rspace_signal_axes(signal, discretized_obj_core_attrs):
    d_x, d_y = discretized_obj_core_attrs["pixel_size"]
    N_x, N_y = discretized_obj_core_attrs["viewer_dims_in_pixels"]

    axes_labels = (r"$x$", r"$y$")
    sizes = (N_x, N_y)
    scales = (d_x, -d_y)
    offsets = (_x_vec(discretized_obj_core_attrs)[0],
               _y_vec(discretized_obj_core_attrs)[0])
    units = ("Å", "Å")

    if abs(scales[0]+scales[1]) < 1e-10:
        scales = (scales[0], -scales[0])
        
    for axis_idx in range(len(units)):
        axis = hyperspy.axes.UniformDataAxis(size=sizes[axis_idx],
                                             scale=scales[axis_idx],
                                             offset=offsets[axis_idx])
        signal.axes_manager[axis_idx].update_from(axis)
        signal.axes_manager[axis_idx].name = axes_labels[axis_idx]
        signal.axes_manager[axis_idx].units = units[axis_idx]
            
    return None



###########################
## Define error messages ##
###########################
