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
from .lib.clusters.modifiers_cluster import ModifiersCluster
from .lib.clusters.clusters_layer import ClustersLayer

logger = logging.getLogger(__name__)
# logger.setLevel(logging.ERROR)
logger.setLevel(logging.DEBUG)


class ObjectState(collections.UserDict):
    def _get_data(self, obj):
        raise NotImplementedError

    _object_type = None
    _object_type_name = None

    def __init__(self, obj, name=None,  # {{{
                 tags=None, obj_subtype=None):
        self._name = ''
        self._type = ''
        self._tags = []
        if isinstance(obj, self._object_type):
            if obj_subtype is not None:
                raise TypeError('Modifier type should not be specified.')
            self.type = obj.type
            if name is None:
                self.name = obj.name + ' stored state'
            if tags is not None:
                self.tags = tags
            self.data = self._get_data(obj)

        elif isinstance(obj, str):
            logger.debug(f'Deserializing {self}')
            state = json.loads(obj)
            self.data = state['data']

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

        # elif isinstance(obj, dict):
        #     if name is None or obj_subtype is None:
        #         raise TypeError
        #     for x, y in obj.items():
        #         if type(x) is not str:
        #             raise TypeError
        #         if type(y) not in {bool, int, float, str}:
        #             raise TypeError
        #     self.data = obj
        #     self.name = name
        #     self.type = obj_subtype
        #     if tags is not None:
        #         self.tags = tags
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
        """Type that this stored state can be used with."""
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
        state = {'data': dict(self.data),
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
