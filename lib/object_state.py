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



# functions used when serializing/deserializing object state.  {{{
# This is workaround for serializing tuples and sets
def _add_type_name_to_dict(obj):
    """Add info about element type to dictionary.

    This required for correct deserialization.
    Does not works with nested not-serializeable objects though.

    Example:
    >>> _add_type_name_to_dict({'angle_limit': 30})
    <<< {'angle_limit': {'data': 30, 'type': 'int'}}
    """
    if isinstance(obj, dict):
        result = {}
        for x, y in obj.items():
            element_type_name = type(y).__name__
            result.update({x: {'data': y, 'type': element_type_name}})
    # TODO: remove this
    elif type(obj) is list:
        result = []
        for x, y in obj.items():
            element_type_name = type(y).__name__
            result.append({'data': y, 'type': element_type_name})
    return result


def _remove_type_name_from_dict(obj, strict=True):
    """
    Example:
    >>> _remove_type_name_from_dict(
    ...         {'angle_limit': {'data': 30, 'type': 'int'}})
    <<< {'angle_limit': 30}
    """
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
    else:
        raise ValueError


# }}}

def get_object_data(obj):
    """Returns ListObjectState or ModifierState for object."""
    if 'ModifiersList' in _get_class_names(obj):
        return ListObjectState.get_data_from_obj(obj)
    elif isinstance(obj, Modifier):
        return ModifierState.get_data_from_obj(obj)
    else:
        raise TypeError


@dataclasses.dataclass(kw_only=True)
class _ObjectState(collections.UserDict):  # {{{
    """
    This classes should not be instantiated using constructor.
    Use one of classmethods insead.
    """

    data: dict
    name: str
    tags: list

    def serialize(self):
        """Serialize object to str."""
        raise NotImplementedError

    @classmethod
    def deserialize(cls, obj):
        """Deserialize str to object."""
        raise NotImplementedError

    @classmethod
    def get_data_from_obj(cls, obj):
        """Create ObjectState from object."""
        raise NotImplementedError

    @staticmethod
    def _check_type(obj):
        """Check if types of dataclass variables are correct."""
        for x, y in obj.__dataclass_fields__.items():
            if type(getattr(obj, x)) != y.type:
                raise TypeError
# }}}


@dataclasses.dataclass(kw_only=True)
class ClustersListState():  # {{{
    data: list

    def serialize(self):
        """Serialize object to str."""
        state = {}
        data = _add_type_name_to_dict(self.data)
        for y in data.items():
            y = y.serialize()
        state.update({'data': data})
        return json.dumps(state)

    @classmethod
    def deserialize(cls, obj):
        """Deserialize str to object."""
        state = json.loads(obj)
        return cls(**state)

    @classmethod
    def get_data_from_obj(cls, obj):
        if 'ModifiersList' not in obj.mro():
            raise TypeError(f'Expected cluster, got {type(obj)}')
        data = {}
        data.update({'data': cls._get_items_data(obj)})
        return cls(**data)

    @staticmethod
    def _get_items_data(obj):
        result = []
        for x in obj:
            result.append(_get_object_state_subclass(x).get_data_from_obj(x))
        return result
# }}}


@dataclasses.dataclass(kw_only=True)
class ListObjectState(_ObjectState):  # {{{
    items_data: list

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
            elif x == 'data':
                state.update({x: _add_type_name_to_dict(self.data)})
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
                for y in state[x].items():
                    items_data.append(
                            _get_object_state_subclass(
                                y['type']).deserialize(y))
                data.update({x: items_data})
            elif x == 'data':
                data.update({x: _remove_type_name_from_dict(state[x])})
            else:
                data.update({x: state[x]})
        return cls(**data)

    @classmethod
    def get_data_from_obj(cls, obj):
        if 'ModifiersList' not in obj.mro():
            raise TypeError(f'Expected cluster, got {type(obj)}')
        data = {}
        data.update({'name': ''})
        data.update({'tags': []})
        data.update({'data': cls._get_data(obj)})
        data.update({'items_data': cls._get_items_data(obj)})
        return cls(**data)

    @staticmethod
    def _get_items_data(obj):
        result = []
        for x in obj:
            result.append(_get_object_state_subclass(x).get_data_from_obj(x))
        return result
# }}}


@dataclasses.dataclass(kw_only=True)
class ModifierState(_ObjectState):  # {{{
    """Object representing stored modifier state."""

    _object_type = Modifier

    def serialize(self):
        logger.debug(f'Serializing {self}')
        self._check_type(self)
        state = {}
        for x, y in self.__dataclass_fields__.items():
            state.update({x: getattr(self, x)})
        return json.dumps(state)

    @classmethod
    def deserialize(cls, obj):
        state = json.loads(obj)
        data = {}
        for x in cls.__dataclass_fields__:
            data.update({x: state[x]})
        return cls(**data)

    @classmethod
    def get_data_from_obj(cls, obj):
        if type(obj) is not cls._object_type:
            raise TypeError(f'Expected {cls._object_type}, got {type(obj)}')
        data = {'name': '',
                'tags': [],
                'data': cls._get_data(obj)}
        return cls(**data)

    @staticmethod
    def _get_data(obj):
        data = {}
        for x in get_all_editable_props(obj):
            val = getattr(obj, x)
            data.update({x: val})
        return data
# }}}
