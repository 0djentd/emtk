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

from .modifiers_cluster import ModifierCluster
from ..lists.object_modifiers_clusters_list import ObjectModifiersClustersList
from ..lists.modifiers_list_active_modifier import ModifiersListActiveModifier

# Modifiers List utils
# Modifiers List -> Modifiers Clusters
# Modifiers Cluster List + Modifiers Cluster
# ModifiersListActiveModifier
# ----------------
# NestedModifiers Cluster
# ----------------


class ClustersLayer(ModifiersListActiveModifier,
                    ObjectModifiersClustersList,
                    ModifierCluster):
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
