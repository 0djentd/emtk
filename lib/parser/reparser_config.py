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

"""
ParserConfig is created on object parse in ModifiersCluster.
It is used to decide which modifiers to consider the
ones used before serialization.
"""

import logging
import collections
import json
from .utils.modifier_prop_types import get_all_editable_props

try:
    import bpy
    Modifier = bpy.types.Modifier
    _WITH_BPY = True
except ModuleNotFoundError:
    from ..dummy_modifiers import DummyBlenderModifier
    Modifier = DummyBlenderModifier
    _WITH_BPY = False


logger = logging.getLogger(__package__)
logger.setLevel(logging.DEBUG)

_CONFIG_CLASSES = {}


class ReparserConfig(collections.UserDict):
    """Configuration to use when reparsing stored ClusterState.

    Attributes:
        data: dict  Dictionary with object properties as keys and
                    subclasses of PropertyReparserConfig as items.
    """
    def __init__(self, obj=None):
        if type(obj) is str:
            self.data = _deserialize_config(obj, self._CONFIG_CLASSES)
        elif type(obj) is Modifier:
            self.data = {}
            for x in get_all_editable_props(obj):
                self.data.update({x: getattr(obj, x)})
        else:
            self.data = {}

    def serialize(self):
        result = {}
        for x, y in self.data.items():
            result.update({x: {'class': y.__name__,
                               'data': y.serialize()}
                           })
        return json.dumps(result)


def _deserialize_config(obj, classes):
    data = json.loads(obj)
    result = {}
    for x, y in data.items():
        config_subclass = classes[y['class']]
        result.update({x: config_subclass.deserialize(y['data'])})
    return result


class _ReparseConfigElement():
    def __init__(self, status=False):
        self.status = status

    @property
    def status(self):
        raise NotImplementedError

    @status.setter
    def status(self, val):
        raise NotImplementedError

    @staticmethod
    def derialize(obj):
        raise NotImplementedError

    def serialize(self):
        raise NotImplementedError


class Basic(_ReparseConfigElement):
    """Simple reparse config.

    Attributes:
        status: bool    If False, property will not be used.
    """

    @staticmethod
    def derialize(obj):
        data = json.loads(obj)
        return Basic(data['status'])

    def serialize(self):
        return json.dumps({'status': self.status})


class Delta(_ReparseConfigElement):
    """Reparse config for int and float properties.

    Attributes:
        status: bool            If False, property will not be used.
        delta: int or float     Range in which property can be changed without
                                considering modifier as different.
    """
    def __init__(self, *args, delta, **kwargs):
        super().__init__(*args, **kwargs)
        self.delta = delta

    @property
    def delta(self):
        return self._delta

    @delta.setter
    def delta(self, val):
        if type(val) in {int, float}:
            self._delta = val
        else:
            raise TypeError(f'Expected int or float, got {type(val)}')

    @staticmethod
    def derialize(obj):
        data = json.loads(obj)
        return Delta(data['status'], data['delta'])

    def serialize(self):
        return json.dumps({'status': self.status,
                           'delta': self.delta})


_CONFIG_CLASSES.update({'Delta': Delta})
_CONFIG_CLASSES.update({'Basic': Basic})
