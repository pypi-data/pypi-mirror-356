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
"""For modelling lenses.

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



# For modelling coherent lens aberrations and phase deviations.
import embeam.coherent



##################################
## Define classes and functions ##
##################################

# List of public objects in package.
__all__ = ["ModelParams"]



def _check_and_convert_coherent_aberrations(params):
    module_alias = embeam.coherent
    func_alias = module_alias._check_and_convert_coherent_aberrations
    coherent_aberrations = func_alias(params)

    return coherent_aberrations



def _pre_serialize_coherent_aberrations(coherent_aberrations):
    obj_to_pre_serialize = coherent_aberrations
    module_alias = embeam.coherent
    func_alias = module_alias._pre_serialize_coherent_aberrations
    serializable_rep = func_alias(obj_to_pre_serialize)

    return serializable_rep



def _de_pre_serialize_coherent_aberrations(serializable_rep):
    module_alias = embeam.coherent
    func_alias = module_alias._de_pre_serialize_coherent_aberrations
    coherent_aberrations = func_alias(serializable_rep)

    return coherent_aberrations



def _check_and_convert_chromatic_aberration_coef(params):
    obj_name = "chromatic_aberration_coef"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    chromatic_aberration_coef = czekitout.convert.to_nonnegative_float(**kwargs)

    return chromatic_aberration_coef



def _pre_serialize_chromatic_aberration_coef(chromatic_aberration_coef):
    obj_to_pre_serialize = chromatic_aberration_coef
    serializable_rep = obj_to_pre_serialize
    
    return serializable_rep



def _de_pre_serialize_chromatic_aberration_coef(serializable_rep):
    chromatic_aberration_coef = serializable_rep

    return chromatic_aberration_coef



def _check_and_convert_mean_current(params):
    obj_name = "mean_current"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    mean_current = czekitout.convert.to_positive_float(**kwargs)

    return mean_current



def _pre_serialize_mean_current(mean_current):
    obj_to_pre_serialize = mean_current
    serializable_rep = obj_to_pre_serialize
    
    return serializable_rep



def _de_pre_serialize_mean_current(serializable_rep):
    mean_current = serializable_rep

    return mean_current



def _check_and_convert_std_dev_current(params):
    obj_name = "std_dev_current"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    std_dev_current = czekitout.convert.to_nonnegative_float(**kwargs)

    return std_dev_current



def _pre_serialize_std_dev_current(std_dev_current):
    obj_to_pre_serialize = std_dev_current
    serializable_rep = obj_to_pre_serialize
    
    return serializable_rep



def _de_pre_serialize_std_dev_current(serializable_rep):
    std_dev_current = serializable_rep

    return std_dev_current



_module_alias = \
    embeam.coherent
_default_coherent_aberrations = \
    _module_alias._default_coherent_aberrations
_default_chromatic_aberration_coef = \
    0
_default_mean_current = \
    50
_default_std_dev_current = \
    0
_default_skip_validation_and_conversion = \
    _module_alias._default_skip_validation_and_conversion



class ModelParams(fancytypes.PreSerializableAndUpdatable):
    r"""The model parameters of a lens.

    See the documentation for the class :class:`embeam.stem.probe.ModelParams`
    for a discussion on how lens model parameters are used to model probes.

    Parameters
    ----------
    coherent_aberrations : `array_like` (:class:`embeam.coherent.Aberration`, ndim=1), optional
        The set of coherent lens aberrations. No coherent lens aberration should
        be specified more than once.
    chromatic_aberration_coef : `float`, optional
        The chromatic aberration coefficient :math:`C_c` in units of mm. Must be
        non-negative.
    mean_current : `float`, optional
        The mean lens current :math:`I` in units of pA. Must be positive.
    std_dev_current : `float`, optional
        The standard deviation of the lens current :math:`\sigma_I` in units of 
        pA. Must be non-negative.
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
    ctor_param_names = ("coherent_aberrations",
                        "chromatic_aberration_coef",
                        "mean_current",
                        "std_dev_current")
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
                 coherent_aberrations=\
                 _default_coherent_aberrations,
                 chromatic_aberration_coef=\
                 _default_chromatic_aberration_coef,
                 mean_current=\
                 _default_mean_current,
                 std_dev_current=\
                 _default_std_dev_current,
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

        coherent_aberrations = self_core_attrs["coherent_aberrations"]

        kwargs = {"coherent_aberrations": coherent_aberrations}
        phase_deviation = embeam.coherent.PhaseDeviation(**kwargs)

        is_azimuthally_symmetric = phase_deviation.is_azimuthally_symmetric
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
        r"""`bool`: A boolean variable indicating whether the phase deviation
        due to the coherent lens aberrations is azimuthally symmetric.

        See the summary documentation of the classes
        :class:`embeam.coherent.PhaseDeviation` and
        :class:`embeam.coherent.Aberration` for additional context.

        The phase deviation due to a set of coherent lens aberrations is
        azimuthally symmetric if :math:`\sum_{m=0}^{\infty}\sum_{n=0}^{\infty} n
        \left(C_{m,n}^{\text{mag}} C_{m,n}^{\text{ang}}\right)^2=0`.

        If ``is_azimuthally_symmetric`` is set to ``True``, then the phase
        deviation is azimuthally symmetric. Otherwise, the phase deviation is
        not azimuthally symmetric.

        Note that ``is_azimuthally_symmetric`` should be considered
        **read-only**.

        """
        result = self._is_azimuthally_symmetric
        
        return result



def _check_and_convert_lens_model_params(params):
    obj_name = "lens_model_params"
    obj = params[obj_name]

    accepted_types = (ModelParams, type(None))
    
    if isinstance(obj, accepted_types[-1]):
        lens_model_params = accepted_types[0]()
    else:
        kwargs = {"obj": obj,
                  "obj_name": obj_name,
                  "accepted_types": accepted_types}
        czekitout.check.if_instance_of_any_accepted_types(**kwargs)

        kwargs = obj.get_core_attrs(deep_copy=False)
        lens_model_params = accepted_types[0](**kwargs)

    return lens_model_params



def _pre_serialize_lens_model_params(lens_model_params):
    obj_to_pre_serialize = lens_model_params
    serializable_rep = obj_to_pre_serialize.pre_serialize()
    
    return serializable_rep



def _de_pre_serialize_lens_model_params(serializable_rep):
    lens_model_params = ModelParams.de_pre_serialize(serializable_rep)
    
    return lens_model_params



_default_lens_model_params = None



###########################
## Define error messages ##
###########################
