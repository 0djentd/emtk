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

import json
import dataclasses
import logging

from ..lists.modifiers_list import ModifiersList
from ..lists.traits.clusters.clusters_list import ClustersListTrait
from ..lists.traits.clusters.sortable_clusters_list\
    import SortableClustersListTrait
from ..lists.traits.clusters.active_cluster import ActiveClusterTrait
from .cluster_trait import ClusterTrait
from ..object_state import ObjectState
from .modifiers_cluster import ModifiersCluster, ModifiersClusterState

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


class ClustersLayer(
    ActiveClusterTrait,
    SortableClustersListTrait,
    ClustersListTrait,
    ClusterTrait,
    ModifiersList
):

    """
    Base class for modifiers clusters that contain other clusters
    in them.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_clusters_for_instantiation(self):
        """
        Returns list of names and types of clusters or
        layers that are required to create this layer.
        Returns None, if cluster cant be created.
        """
        if not self.default_data['createable']:
            return None

        clusters = []
        for x, y in zip(self.default_data['by_name'],
                        self.default_data['by_type']):
            if x != 'ANY' or y == 'ANY':
                return None
            clusters.append(x, y)
        return clusters

    def get_state(self):
        return ClustersLayerState(self)


@dataclasses.dataclass
class ClustersLayerState(ObjectState):  
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
        if 'ClustersLayer' not in names:
            raise TypeError(f'Expected cluster, got {type(obj)}')

        data = {}
        data.update({'name': ''})
        data.update({'tags': []})
        data.update({'data': obj.instance_data})
        items_data = []
        for x in obj._data:
            if isinstance(x, ClustersLayer):
                items_data.append(ClustersLayerState(x))
            elif isinstance(x, ModifiersCluster):
                items_data.append(ModifiersClusterState(x))
        data.update({'items_data': items_data})
        return cls(**data)

    def compare(self, obj):
        if not isinstance(obj, ClustersLayer):
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

