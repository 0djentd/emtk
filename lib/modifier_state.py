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
import copy

try:
    import bpy
    _WITH_BPY = True
    Modifier = bpy.types.Modifier
except ModuleNotFoundError:
    _WITH_BPY = False
    from .dummy_modifiers import DummyBlenderModifier
    Modifier = DummyBlenderModifier

# TODO: move this functions to this module
from .utils.modifier_prop_types import MODIFIER_TYPES as ALL_MODIFIER_TYPES
from .utils.modifier_prop_types import get_all_editable_props

# Objects
from .lib.clusters.modifiers_cluster import ModifiersCluster
from .lib.clusters.clusters_layer import ClustersLayer
from .lib.lists.extended_modifiers_list import ExtendedModifiersList

logger = logging.getLogger(__name__)
# logger.setLevel(logging.ERROR)
logger.setLevel(logging.DEBUG)

# Types to use in serialization/deserialization.
# This set can be edited in runtime.
types = {bool, int, float, str, list, dict, set, tuple}


# This two functions only used when serializing/deserializing object state.
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


class ObjectState(collections.UserDict):
    def _get_data(self, obj):
        raise NotImplementedError

    _object_type = None
    _object_type_name = None

    """
    Properties:
    type: str       Object subtype (example: bpy.types.Modifier.type)
    data: dict      Data required to deserialize object.
    name: str       Name of object state used in ui.
    tags: set       Object state's tags, used for sorting in ui.
    """

    def __init__(self, obj, name=None,  # {{{
                 tags=None, obj_subtype=None, types=None):
        self._name = ''
        self._type = ''
        self._tags = []
        logger.info('Creating ObjectState.')
        if isinstance(obj, self._object_type):
            logger.debug(f'Trying to get {obj} attributes.')
            if obj_subtype is not None:
                raise TypeError('Modifier type should not be specified.')
            self.type = obj.type
            if name is None:
                self.name = obj.name + ' stored state'
            if tags is not None:
                self.tags = tags
            self.data = self._get_data(obj)

        elif isinstance(obj, str):
            logger.debug('Deserializing str.')
            state = json.loads(obj)
            self.data = _remove_type_name_from_dict(state['data'])
            if name is None:
                self.name = name
            else:
                self.name = state['name']

            if obj_subtype is None:
                self.type = state['type']
            else:
                self.type = obj_subtype

            if tags is None:
                self.tags = state['tags']
            else:
                self.tags = tags
        else:
            raise TypeError
    # }}}

    def compare(self, obj):
        if type(obj) is type(self):
            logger.debug(f'Comparing {self} and {obj}')
            if self.data != obj.data\
                    or self.type != obj.type\
                    or self.tags != obj.tags\
                    or self.name != obj.name:
                return False
            logger.debug('Objects eq.')
            return True
        else:
            raise TypeError

    # Properties {{{
    @property
    def type(self):
        f"""{self._object_type_name} type that this
stored state can be used with.""".replace('\n', ' ')
        return self._type

    @type.setter
    def type(self, obj_subtype):
        if not isinstance(obj_subtype, str):
            raise TypeError
        if obj_subtype not in ALL_MODIFIER_TYPES:
            raise ValueError
        self._type = obj_subtype

    @property
    def name(self):
        """Name of stored state used in UI."""
        return self._name

    @name.setter
    def name(self, modifier_state_name):
        if not isinstance(modifier_state_name, str):
            raise TypeError
        self._name = modifier_state_name

    @property
    def tags(self):
        for x in self._tags:
            if type(x) is not str:
                raise TypeError
        return self._tags

    @tags.setter
    def tags(self, obj):
        if type(obj) is not list:
            raise TypeError
        self._tags = obj
    # }}}

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"""{self._object_type_name} state: {self.name}, {self.type},
{self.tags}, {len(self.data)} elements.""".replace('\n', ' ')

    def serialize(self):
        logger.debug(f'Serializing {self}')
        state = {'data': dict(_add_type_name_to_dict(self.data)),
                 'name': str(self.name),
                 'tags': list(self.tags),
                 'type': str(self.type)}
        return json.dumps(state)


class ModifierState(ObjectState):
    """Object representing stored modifier state."""

    _object_type = Modifier
    _object_type_name = 'Modifier'

    def _get_data(self, obj):
        data = {}
        for x in get_all_editable_props(obj):
            val = getattr(obj, x)
            data.update({x: val})
        return data


class ModifiersClusterState(ObjectState):
    """Object representing stored cluster state."""

    _object_type = ModifiersCluster
    _object_type_name = 'ModifiersCluster'

    def _get_data(self, obj):
        result = copy.copy(obj.variables)
        elements = []
        for x, y in obj.items():
            elements.append(y.name)
        # TODO: this doesnt work
        result.update({'by_name': elements})

        elements = []
        for x, y in obj.items():
            elements.append(ModifierState(y).serialize())
        # TODO: this doesnt work
        result.update({'modifiers_state': elements})
        return result


class ClustersLayerState(ObjectState):
    """Object representing stored cluster state."""

    _object_type = ClustersLayer
    _object_type_name = 'ClustersLayer'

    def _get_data(self, obj):
        result = copy.copy(obj.variables)

        elements = []
        for x, y in obj.items():
            elements.append(y.name)
        # TODO: this doesnt work
        result.update({'by_name': elements})
        return result


class ClustersListState(ObjectState):
    """Object representing stored clusters list state."""

    _object_type = ExtendedModifiersList
    _object_type_name = 'ExtendedModifiersList'

    def _get_data(self, obj):
        result = {}
        elements = []
        for x, y in obj.items():
            elements.append(y.name)
        # TODO: this doesnt work
        result.update({'by_name': elements})
        return result
