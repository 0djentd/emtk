# ##### BEGIN GPL LICENSE BLOCK #####
#
# Copyright 2022, Sergey Shapochkin
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import logging
import json
import collections
import dataclasses
import copy

try:
    import bpy
    Modifier = bpy.types.Modifier
    _WITH_BPY = True
except ModuleNotFoundError:
    from .dummy_modifiers import DummyBlenderModifier
    Modifier = DummyBlenderModifier
    _WITH_BPY = False

# TODO: move this functions to this module
from .utils.modifier_prop_types import MODIFIER_TYPES as ALL_MODIFIER_TYPES
from .utils.modifier_prop_types import get_all_editable_props

logger = logging.getLogger(__name__)
# logger.setLevel(logging.ERROR)
logger.setLevel(logging.DEBUG)

# Types to use in serialization/deserialization.
# This set can be edited in runtime.
types = {bool, int, float, str, list, dict, set, tuple}

# This list is populated at runtime because of type check
# in _serialize_object and _deserialize_object.
# This type check is used to allow nested objects of different type.
obj_state_classes = []

# TODO: this explaination of reparse is not too good.
"""
Design.

What features required to be implemented?

Modifier presets.

Clusters.
Clusters presets.
Different cluster subtypes support.

UI for presets.
UI for clusters.
UI for default cluster settings (a.k.a. cluster_type,
cluster_definition, parser_variables ...)

Full modal input support.
Full View3D support.

What this means?
Basically, all modifiers and clusters editing should be
possible in View3D, with minimum of menus, panels and as
fast as using built-in modal operators.
This should not limit customization of toolkit in any way
and can be ignored when some feature is too complex to customize
through single modal operator or popup.
Example:
    Cluster subtypes editing should not be implemented using
    modal operator, because it will not be possible to
    visualize changes made to cluster subtype using
    current clusters library implementation.

Support for storing cluster subtypes in preferences, scene and object.
"""
"""
How serialization/deserialization/reparse/parse works:

    When cluster is first created (for example when new modifier is added)
    it is being parsed. On this stage, it has no ObjectState instance.
    ObjectState is being created when clusters list is removed (for example when
    operator returns {'FINISHED'}). This is required to later reparse clusters.

    Reparsing clusters is a process of instantiating clusters with same
    modifiers and clusters in them. It requires at least some of
    list's objects variables to be stored in ObjectState associated with
    cluster.
    Reparsing clusters is required to associate stored cluster variables with
    actual modifiers.

    Example: ModifiersClusterState that has information about
    names of modifiers in it and some of their properties.

    ReparseConfig is an object that defines how stored variables should be
    compared with existing ones.
    
    Example: reparse_config.Delta can be used to allow successfully
    reparsing objects with their int/float variables slightly different.

    After finishing reparsing clusters, ObjectState objects are no longer used
    and would be created again on operator finish.
    When serialized ObjectState already exists at this stage, it is copied
    to backup property of object.

Pros and cons:
    Whole thing uses json instead of bpy.type.Property. Editing variables in UI
    can be done using ui_class_variables_editor module.
    Why whole thing uses json then?
    Because blender collections does not support more than one object type.
    Implementing everything through pointer properties and collections will
    be much harder and probably will require using a lot 
    of usual variables anyway.
    Example:
    ClustersLayer can have both ModifiersClusters and ClustersLayers in it.
"""
"""
Properties:
    This data is used in reparse/deserialization:
        class: str              Object class name (type(obj).__name__)
        data: dict              Object data (cluster name)
        This data only used in ListObjectState:
        objects_data: list      ObjectsState subclass instances.

    This data is used in UI only:
        name: str       Name of object state used in ui.
        tags: set       Object state's tags, used for sorting in ui.
"""
"""
After this rework, cluster_trait will have following attrs:
Properties:
    default_state: ObjectState      ObjectState that is defined on
                                    cluster creation.
    reparse_state: ObjectState      Previous ObjectState.

    # TODO: should this be named instance_data? no.
    instance_data: dict     Variables used anywhere else. Example: cluster
                            name, ui state, tags and sorting rules.
                            They are stored in ObjectState.

    # TODO: should this be in instance_data? yes.
    sorting_rules: list     Sorting rules applied to this cluster.

    # TODO: should this be in instance_data? yes.
    # TODO: should this be named data? no.
    data: list              Clusters instances.
"""
"""
TODO: rework.
Default cluster settings is basically presets.
Default cluster settings and presets are the same thing.

Initial cluster settings is what 'default cluster settings' should
be called instead.

Presets can be 'layered' on initial cluster settings.
Presets are used to modify objects.
Initial cluster settings are to parse cluster when it is created and
when modifiers were changed outside of clusters list.

Modal input.
"""


# functions used when serializing/deserializing object state.  {{{
# This is workaround for serializing tuples and sets
def _add_type_name_to_dict(obj):
    """Add info about element type to dictionary.

    This required for correct deserialization.
    Does not works with nested not-serializeable objects though.
    """
    if not isinstance(obj, dict):
        raise TypeError
    result = {}
    for x, y in obj.items():
        element_type_name = type(y).__name__
        result.update({x: {'data': y, 'type': element_type_name}})
    return result


def _remove_type_name_from_dict(obj, strict=True):
    if not isinstance(obj, dict):
        raise TypeError
    result = {}
    for x, y in obj.items():
        t = None
        for x in types:
            if y['type'] == x.__name__:
                t = x
                break
        if t is not None:
            result.update({x: t(y['data'])})
        else:
            line = f"""Unsupported type in stored object state "{y[type]}", expected
type in {types}""".replace('\n', ' ')
            if strict:
                raise TypeError(line)
            logger.error(line)
            result.update({x: y['data']})
    return result
# }}}


@dataclasses.dataclass(kw_only=True)
class ObjectState(collections.UserDict):  # {{{
    data: dict
    name: str
    subtype: str
    tags: list

    def _get_data(self, obj):
        raise NotImplementedError

    _object_type = None

    def serialize(self):
        logger.debug(f'Serializing {self}')
        self._check_type(self)
        state = {}
        for x, y in self.__dataclass_fields__.items():
            if x == 'items_data':
                items_data = _add_type_name_to_dict(self.items_data)
                for y in items_data['data'].items():
                    y = y.serialize()
                state.update({x: items_data})
            else:
                state.update({x: getattr(self, x)})
        return json.dumps(state)

    @classmethod
    def deserialize(cls, obj):
        state = json.loads(obj)
        data = {}
        for x in cls.__dataclass_fields__:
            if x == 'items_data':
                items_data = []
                for y in state[x]:
                    items_data.append(_get_object_state_subclass(y).deserialize(y))
                data.update({x: items_data})
            else:
                data.update({x: state[x]})
        return cls(**data)

    @classmethod
    def get_data_from_obj(cls, obj):
        raise NotImplementedError

    @staticmethod
    def _check_type(obj):
        for x, y in obj.__dataclass_fields__.items():
            if type(getattr(obj, x)) is not y['type']:
                raise TypeError
# }}}


@dataclasses.dataclass(kw_only=True)
class ListObjectState(ObjectState):  # {{{
    items_data: list

    @classmethod
    def get_data_from_obj(cls, obj):
        if 'ModifiersList' not in obj.mro():
            raise TypeError
        data = {}
        data.update({'name': ''})
        data.update({'subtype': obj.type})
        data.update({'tags': []})
        data.update({'data': cls._get_data(obj)})
        data.update({'items_data': cls._get_items_data(obj)})
        return cls(**data)

    @staticmethod
    def _get_data(obj):
        return obj.instance_data

    @staticmethod
    def _get_items_data(obj):
        data = []
        for x in obj:
            data.append(get_object_data(x))
        return data
# }}}


def _get_class_names(object_instance):
    names = []
    for x in object_instance.mro():
        names.append(x.__name__)
    return names


def _get_object_state_subclass(name):
    if name == 'ListObjectState':
        return ListObjectState
    elif name == 'ModifierState':
        return ModifierState

def deserialize_object_state(obj):



def get_object_data(obj):
    """Returns ListObjectState or ModifierState."""
    if 'ModifiersList' in _get_class_names(obj):
        return ListObjectState.get_data_from_obj(obj)
    elif isinstance(obj, Modifier):
        return ModifierState.get_data_from_obj(obj)
    else:
        raise TypeError


@dataclasses.dataclass(kw_only=True)
class ModifierState(ObjectState):
    """Object representing stored modifier state."""

    _object_type = Modifier

    @classmethod
    def get_data_from_obj(cls, obj):
        data = {}
        data.update({'name': ''})
        data.update({'subtype': obj.type})
        data.update({'tags': []})
        data.update({'data': cls._get_data(obj)})
        return cls(**data)

    @staticmethod
    def _get_data(obj):
        data = {}
        for x in get_all_editable_props(obj):
            val = getattr(obj, x)
            data.update({x: val})
        return data
