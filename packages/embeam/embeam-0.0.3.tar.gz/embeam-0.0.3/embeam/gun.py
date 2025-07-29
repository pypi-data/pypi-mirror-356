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
"""For modelling electron guns.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For validating and converting objects.
import czekitout.check
import czekitout.convert

# For defining classes that support enforced validation, updatability,
# pre-serialization, and de-serialization.
import fancytypes



# For recycling default values of parameters.
import embeam



##################################
## Define classes and functions ##
##################################

# List of public objects in package.
__all__ = ["ModelParams"]



def _check_and_convert_mean_beam_energy(params):
    obj_name = "mean_beam_energy"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    mean_beam_energy = czekitout.convert.to_positive_float(**kwargs)

    return mean_beam_energy



def _pre_serialize_mean_beam_energy(mean_beam_energy):
    obj_to_pre_serialize = mean_beam_energy
    serializable_rep = obj_to_pre_serialize
    
    return serializable_rep



def _de_pre_serialize_mean_beam_energy(serializable_rep):
    mean_beam_energy = serializable_rep

    return mean_beam_energy



def _check_and_convert_intrinsic_energy_spread(params):
    obj_name = "intrinsic_energy_spread"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    intrinsic_energy_spread = czekitout.convert.to_nonnegative_float(**kwargs)

    return intrinsic_energy_spread



def _pre_serialize_intrinsic_energy_spread(intrinsic_energy_spread):
    obj_to_pre_serialize = intrinsic_energy_spread
    serializable_rep = obj_to_pre_serialize
    
    return serializable_rep



def _de_pre_serialize_intrinsic_energy_spread(serializable_rep):
    intrinsic_energy_spread = serializable_rep

    return intrinsic_energy_spread



def _check_and_convert_accel_voltage_spread(params):
    obj_name = "accel_voltage_spread"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    accel_voltage_spread = czekitout.convert.to_nonnegative_float(**kwargs)

    return accel_voltage_spread



def _pre_serialize_accel_voltage_spread(accel_voltage_spread):
    obj_to_pre_serialize = accel_voltage_spread
    serializable_rep = obj_to_pre_serialize
    
    return serializable_rep



def _de_pre_serialize_accel_voltage_spread(serializable_rep):
    accel_voltage_spread = serializable_rep

    return accel_voltage_spread



_module_alias = embeam
_default_mean_beam_energy = 80
_default_intrinsic_energy_spread = 0
_default_accel_voltage_spread = 0
_default_skip_validation_and_conversion = False



class ModelParams(fancytypes.PreSerializableAndUpdatable):
    r"""The model parameters of an electron gun.

    See the documentation for the class :class:`embeam.stem.probe.ModelParams`
    for a discussion on how electron gun model parameters are used to model
    probes.

    Parameters
    ----------
    mean_beam_energy : `float`, optional
        The mean electron beam energy :math:`E` in units of keV. Must be
        positive.
    intrinsic_energy_spread : `float`, optional
        The standard deviation of the electrons in the gun :math:`\sigma_E` in
        units of keV, when operating a voltage supply that does not fluctuate.
        In other words, ``intrinsic_energy_spread`` is the intrinsic energy
        spread of the gun. Must be non-negative.
    accel_voltage_spread : `float`, optional
        The standard deviation of the accelerating voltage :math:`\sigma_V` in
        units of kV. Must be non-negative.
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
    ctor_param_names = ("mean_beam_energy",
                        "intrinsic_energy_spread",
                        "accel_voltage_spread")
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
                 mean_beam_energy=\
                 _default_mean_beam_energy,
                 intrinsic_energy_spread=\
                 _default_intrinsic_energy_spread,
                 accel_voltage_spread=\
                 _default_accel_voltage_spread,
                 skip_validation_and_conversion=\
                 _default_skip_validation_and_conversion):
        ctor_params = {key: val
                       for key, val in locals().items()
                       if (key not in ("self", "__class__"))}
        kwargs = ctor_params
        kwargs["skip_cls_tests"] = True
        fancytypes.PreSerializableAndUpdatable.__init__(self, **kwargs)

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



def _check_and_convert_gun_model_params(params):
    obj_name = "gun_model_params"
    obj = params[obj_name]

    accepted_types = (ModelParams, type(None))
    
    if isinstance(obj, accepted_types[-1]):
        gun_model_params = accepted_types[0]()
    else:
        kwargs = {"obj": obj,
                  "obj_name": obj_name,
                  "accepted_types": accepted_types}
        czekitout.check.if_instance_of_any_accepted_types(**kwargs)

        kwargs = obj.get_core_attrs(deep_copy=False)
        gun_model_params = accepted_types[0](**kwargs)

    return gun_model_params



def _pre_serialize_gun_model_params(gun_model_params):
    obj_to_pre_serialize = gun_model_params
    serializable_rep = obj_to_pre_serialize.pre_serialize()
    
    return serializable_rep



def _de_pre_serialize_gun_model_params(serializable_rep):
    gun_model_params = ModelParams.de_pre_serialize(serializable_rep)
    
    return gun_model_params



_default_gun_model_params = None



###########################
## Define error messages ##
###########################
