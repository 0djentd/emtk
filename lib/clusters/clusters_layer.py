# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

from ..lists.modifiers_list import ModifiersList
from ..lists.traits.clusters.clusters_list import ClustersListTrait
from ..lists.traits.clusters.sortable_clusters_list\
        import SortableClustersListTrait
from ..lists.traits.clusters.active_cluster import ActiveClusterTrait
from .cluster_trait import ClusterTrait


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
        if not self._cluster_definition['createable']:
            return None

        clusters = []
        for x, y in zip(self._cluster_definition['by_name'],
                        self._cluster_definition['by_type']):
            if x == 'ANY' or y == 'ANY':
                return None
            clusters.append(x, y)
        return clusters
