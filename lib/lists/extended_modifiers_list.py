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

from .modifiers_list import ModifiersList
from .traits.clusters.clusters_list import ClustersListTrait
from .traits.clusters.sortable_clusters_list import SortableClustersListTrait
from .traits.clusters.active_cluster import ActiveClusterTrait
from .traits.clusters.first_layer_clusters_list \
        import FirstLayerClustersListTrait
from ..clusters_list_object_state import ListObjectState


class ExtendedModifiersList(
                            FirstLayerClustersListTrait,
                            ActiveClusterTrait,
                            SortableClustersListTrait,
                            ClustersListTrait,
                            ModifiersList
                            ):
    """
    Clusters list with methods for editing, adding, removing,
    sorting and parsing clusters or modifiers on multiple clusters layers of
    the same Blender object.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ClustersListState(ListObjectState):
    """Object representing stored clusters list state."""
    _object_type = ExtendedModifiersList

    def _get_data(self, obj):
        return {}
