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
import dataclasses

try:
    _WITH_BPY = True
except ModuleNotFoundError:
    _WITH_BPY = False

from ..utils.modifier_prop_types import get_all_editable_props


logger = logging.getLogger(__package__)
logger.setLevel(logging.DEBUG)

_CONFIG_CLASSES: dict = {}


class ReparseConfig(collections.UserDict):
    """Configuration to use when reparsing stored ClusterState.

    Attributes:
        data: dict  Dictionary with object properties as keys and
                    subclasses of PropertyReparserConfig as items.
    """
    def __init__(self, obj=None) -> None:
        if type(obj) is str:
            self.data = _deserialize_config(obj, _CONFIG_CLASSES)
        elif obj is None:
            self.data = {}
        else:
            self.data = {}
            for x in get_all_editable_props(obj):
                self.data.update({x: getattr(obj, x)})

    def serialize(self):
        result = {}
        for x, y in self.data.items():
            result.update({x: {'class': y.__name__,
                               'data': y.serialize()}
                           })
        return json.dumps(result)


class ListReparseConfig(ReparseConfig):
    def __init__(self, obj):
        self.items_data = []
        for x in obj.data:
            try:
                if obj.has_clusters():
                    logger.debug('ClustersLayer.')
                self.items_data.append(ListReparseConfig(x))
            except AttributeError:
                self.items_data.append(ReparseConfig(x))
        return


def _deserialize_config(obj, classes):
    data = json.loads(obj)
    result = {}
    for x, y in data.items():
        config_subclass = classes[y['class']]
        result.update({x: config_subclass.deserialize(y['data'])})
    return result


@dataclasses.dataclass
class _ReparseConfigElement():
    status: bool

    @staticmethod
    def deserialize(obj):
        if type(obj) is str:
            data = json.loads(obj)
        elif type(obj) is dict:
            data = obj
        return Basic(data)

    def serialize(self):
        data = {}
        for x, y in self.__dataclass_fields__.items():
            data.update({x: getattr(self, x)})
        return json.dumps(data)


@dataclasses.dataclass
class Basic(_ReparseConfigElement):
    """Simple reparse config.

    Attributes:
        status: bool    If False, property will not be used.
    """
    status: bool


@dataclasses.dataclass
class Delta(_ReparseConfigElement):
    """Reparse config for int and float properties.

    Attributes:
        status: bool            If False, property will not be used.
        delta: int or float     Range in which property can be changed without
                                considering modifier as different.
    """
    delta: float


_CONFIG_CLASSES.update({'Delta': Delta})
_CONFIG_CLASSES.update({'Basic': Basic})
