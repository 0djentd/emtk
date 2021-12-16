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

from .modifiers_list import ModifiersList
from .traits.clusters_list import ClustersListTrait
from .traits.sortable_clusters_list import SortableClustersListTrait
from .traits.object_clusters_list import ObjectClustersListTrait
from .traits.active_cluster import ActiveClusterTrait
from .traits.first_layer_clusters_list import FirstLayerClustersListTrait


class ExtendedModifiersList(
                            FirstLayerClustersListTrait,
                            ActiveClusterTrait,
                            ObjectClustersListTrait,
                            SortableClustersListTrait,
                            ClustersListTrait,
                            ModifiersList
                            ):
    """
    First layer of clusters list with methods for editing, adding, removing,
    sorting and parsing clusters or modifiers on multiple clusters layers of
    same Blender object.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
