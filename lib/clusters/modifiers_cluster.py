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

from .cluster_trait import ClusterTrait
from ..lists.modifiers_list import ModifiersList
from ..clusters_list_object_state import ListObjectState
import copy


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
            if cluster not in self.get_full_list()\
                    and cluster is not self:
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
        if not self.parser_variables['createable']:
            return None

        modifiers = []
        for x, y in zip(self.parser_variables['by_name'],
                        self.parser_variables['by_type']):
            if x != 'ANY' or y == 'ANY':
                return None
            modifiers.append(x, y)
        return modifiers


class ModifiersClusterState(ListObjectState):
    """Object representing stored cluster state."""
    _object_type = ModifiersCluster
