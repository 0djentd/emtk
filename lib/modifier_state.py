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

try:
    import bpy
    _WITH_BPY = True
    Modifier = bpy.types.Modifier
except ModuleNotFoundError:
    _WITH_BPY = False
    from .dummy_modifiers import DummyBlenderModifier
    Modifier = DummyBlenderModifier

from .utils.modifier_prop_types import MODIFIER_TYPES as ALL_MODIFIER_TYPES
from .utils.modifier_prop_types import get_all_editable_props

logger = logging.getLogger(__name__)
# logger.setLevel(logging.ERROR)
logger.setLevel(logging.DEBUG)


class ModifierState(collections.UserDict):
    """Object representing stored modifier state."""

    def __init__(self, obj, name=None,  # {{{
                 tags=None, modifier_type=None):
        self._name = ''
        self._type = ''
        self._tags = []
        if isinstance(obj, Modifier):
            if modifier_type is not None:
                raise TypeError('Modifier type should not be specified.')
            if name is None:
                self.name = obj.name + ' stored state'
            self.type = obj.type
            if tags is not None:
                self.tags = tags
            data = {}
            for x in get_all_editable_props(obj):
                val = getattr(obj, x)
                data.update({x: val})
            self.data = data
        elif isinstance(obj, str):
            logger.debug(f'Deserializing {self}')
            state = json.deserialize(obj)
            self.data = state['data']
            self.name = state['name']
            self.type = state['type']
            self.tags = state['tags']
        elif isinstance(obj, dict):
            if name is None or modifier_type is None:
                raise TypeError
            for x, y in obj.items():
                if type(x) is not str:
                    raise TypeError
                if type(y) not in {bool, int, float, str}:
                    raise TypeError
            self.data = obj
            self.name = name
            self.type = modifier_type
            if tags is not None:
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
        """Modifier type that this data can be used for."""
        return self._type

    @type.setter
    def type(self, modifier_type):
        if not isinstance(modifier_type, str):
            raise TypeError
        if modifier_type not in ALL_MODIFIER_TYPES:
            raise ValueError
        self._type = modifier_type

    @property
    def name(self):
        """Name of modifier state used in UI."""
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
        return f"""Modifier state: {self.name}, {self.type}, 
{self.tags}, {len(self.data)} elements.""".replace('\n', ' ')

    def serialize(self):
        logger.debug(f'Serializing {self}')
        state = {'data': dict(self.data),
                 'name': str(self.name),
                 'tags': list(self.tags),
                 'type': str(self.type)}
        return json.dumps(state)
