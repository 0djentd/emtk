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
from ..lists.traits.clusters.object_clusters_list\
        import ObjectClustersListTrait
from ..lists.traits.clusters.active_cluster import ActiveClusterTrait
from .cluster import ClusterTrait

from ..clusters_actions import ClustersAction, ClusterRequest

try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    from ..dummy_modifiers import DummyBlenderModifier, DummyBlenderObj
    _WITH_BPY = False


class ClustersLayer(
                    ClusterTrait,
                    ActiveClusterTrait,
                    ObjectClustersListTrait,
                    SortableClustersListTrait,
                    ClustersListTrait,
                    ModifiersList
                    ):

    """
    Base class for modifiers clusters that contain other clusters
    in them.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def has_clusters(self):
        """
        Returns True, if cluster consists of clusters.
        """
        return True
