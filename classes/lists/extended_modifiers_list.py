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

from .object_modifiers_clusters_list import ObjectModifiersClustersList
from .first_layer_clusters_list import FirstLayerClustersList
from .modifiers_list_active_modifier import ModifiersListActiveModifier
from ..clusters_parser import ClustersParser


# Modifiers List utils
# Modifiers List
# Modifiers Clusters parser
# Modifiers Clusters List
# Object Modifiers Clusters List
# ----------------------
# Extended Modifiers List
# ----------------------

class ExtendedModifiersList(ModifiersListActiveModifier,
                            FirstLayerClustersList,
                            ObjectModifiersClustersList):
    """
    List of object modifiers with 'active modifier' that can be useful
    in modal operators.

    Can have only one active modifier at the time.
    Cant have no active modifier, if any modifier exists.
    Active modifier can be set with index, name, or reference.

    Can work with modifiers cluster lists as well.
    """

    def __init__(self):
        super().__init__()
        self._clusters_parser = ClustersParser()

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

    def create_modifiers_list(self, obj):
        """
        Creates and parses modifiers list for obj and
        selects first modifier as active.

        This method exists for both object and extended modifiers lists.

        Returns True, if found any modifiers.
        Returns False, if no modifiers found.
        """
        return self._create_extended_modifiers_list(obj)

    # TODO: this methods dont work with nested clusters
    def _create_extended_modifiers_list(self, obj):
        """
        Creates and parses modifiers list for obj and
        selects first modifier as active.

        Wrapper for ObjectModifiersClustersList's resfresh method.

        Returns True, if found any modifiers.
        Returns False, if no modifiers found.
        """

        # Update modifiers list
        modified = self._create_modifiers_list(obj)

        # Select first modifier, if found any modifiers
        if isinstance(self._modifiers_list, list):
            if len(self._modifiers_list) > 0:
                self._mod = self._modifiers_list[0]
        else:
            self._additional_info_log.append("This is not a list")

        return modified
