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

import copy
import json
import dataclasses
import logging

from .cluster_trait import ClusterTrait
from ..lists.modifiers_list import ModifiersList
from ..object_state import ObjectState, ModifierState
# from ..parser.reparser_config import Basic, Delta

try:
    import bpy
    Modifier = bpy.types.Modifier
    _WITH_BPY = True
except ModuleNotFoundError:
    from ..dummy_modifiers import DummyBlenderModifier
    Modifier = DummyBlenderModifier
    _WITH_BPY = False

logger = logging.getLogger(__name__)
# logger.setLevel(logging.ERROR)
logger.setLevel(logging.DEBUG)


class ModifiersCluster(
                       ClusterTrait,
                       ModifiersList
                       ):
    """
    Base class for modifiers cluster type
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # This method is different in ClustersListTrait.
    def _check_cluster_or_modifier(self, cluster):
        if type(cluster) is str:
            result = self.find_cluster_by_name(cluster)
            if result is None:
                result = self.find_modifier_by_name(cluster)
            if result is None:
                raise ValueError
            cluster = result
        elif cluster is None:
            cluster = self
        else:
            if cluster not in self:
                if cluster is not self:
                    raise ValueError
        return cluster

    @property
    def modifiers(self):
        return copy.copy(self._data)

    def get_modifiers_for_instantiation(self):
        """
        Returns list of names and types of modifiers
        that are required to create this cluster.
        Returns None, if cluster cant be created.
        """
        if not self.default_data['createable']:
            return None

        modifiers = []
        for x, y in zip(self.default_data['by_name'],
                        self.default_data['by_type']):
            if x != 'ANY' or y == 'ANY':
                return None
            modifiers.append(x, y)
        return modifiers

    def get_state(self):
        return ModifiersClusterState(self)


@dataclasses.dataclass
class ModifiersClusterState(ObjectState):  # {{{
    items_data: list

    def serialize(self):
        logger.debug(f'Serializing {self}')
        self._check_type(self)
        state = {}
        state.update = {
                        'data': self.data,
                        'items_data': self.items_data,
                        }
        return json.dumps(state)

    @classmethod
    def deserialize(cls, obj):
        state = json.loads(obj)
        data = {}
        data.update({'data': state['data'],
                     'items_data': state['items_data'],
                     })
        return cls(**data)

    @classmethod
    def get_data_from_obj(cls, obj):
        names = []
        for x in type(obj).mro():
            names.append(x.__name__)
        if 'ModifiersList' not in names:
            raise TypeError(f'Expected cluster, got {type(obj)}')

        data = {}
        data.update({'name': ''})
        data.update({'tags': []})
        data.update({'data': cls._get_data(obj)})
        items_data = []
        for x in obj._data:
            items_data.append(ModifierState(x))
        data.update({'items_data': items_data})
        return cls(**data)

    def compare(self, obj):
        if not isinstance(obj, ModifiersCluster):
            raise TypeError
        for x, y in zip(self.data, self.data.values()):
            if obj.instance_data[x] != y:
                return False
        if not self.compare_items(obj.items_data):
            return False
        return True

    def compare_items(self, items):
        if not isinstance(items, list):
            raise TypeError
        if len(self.items_data) != items:
            return False
        for i, x in enumerate(self.items_data):
            if not x.compare(items[i]):
                return False
        return True
# }}}
