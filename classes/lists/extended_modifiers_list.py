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

from .first_layer_clusters_list import FirstLayerClustersList

# Traits
from .traits.object_clusters_list import ObjectClustersListTrait
from .traits.active_cluster import ActiveClusterTrait


class ExtendedModifiersList(
                            ActiveClusterTrait,
                            FirstLayerClustersList,
                            ObjectClustersListTrait
                            ):
    """
    List of object modifiers with 'active modifier' that can be useful
    in modal operators.

    Can have only one active modifier at the time.
    Cant have no active modifier, if any modifier exists.
    Active modifier can be set with index, name, or reference.

    Can work with modifiers cluster lists as well.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_cluster(self):
        """
        Returns active cluster on deepest non-collapsed layer.

        This method should only be used if creating some kind of user
        interface that uses ExtendedModifiersList.
        """
        return self.active_cluster_get_deep()

    def get_layer(self):
        """
        Returns ModifiersClustersList, which active
        cluster belongs to on deepest non-collapsed layer.

        This method should only be used if creating some kind of user
        interface that uses ExtendedModifiersList.
        """
        return self.get_active_cluster_layer()
