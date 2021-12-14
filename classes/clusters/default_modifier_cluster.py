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

import bpy

from ..modifiers_cluster import ModifierCluster


class DefaultModifierCluster(ModifierCluster):
    """
    Cluster type for default modifiers without custom behaviour, tags, or name.
    Consist of one modifier.
    """

    _MODCLUSTER_NAME = "Default Modifier"

    _MODCLUSTER_TYPE = "DEFAULT_MODIFIER_CLUSTER"

    _MODCLUSTER_IS_SANE = True

    _MODCLUSTER_MODIFIERS_BY_TYPE = [['ANY']]

    _MODCLUSTER_MODIFIERS_BY_POSSIBLE_NAMES = [['ANY']]

    _MODCLUSTER_CREATEABLE = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_this_cluster_name(self):
        if len(self._modifiers_list) != 1:
            return self._MODCLUSTER_NAME
        return self._modifiers_list[0].name

    def get_this_cluster_type(self):
        if len(self._modifiers_list) != 1:
            return self._MODCLUSTER_TYPE
        return self._modifiers_list[0].type

    # Check if passed argument are actually Blender modifier
    def modcluster_extra_availability_check(self, mod):
        if isinstance(mod[0], ModifierCluster):
            return False
        else:
            return 'FOUND'

    # ===========================
    # Initializing cluster
    # ===========================
    def set_this_cluster_modifiers(self, modifiers):
        """
        Replaces list of modifiers with modifiers.
        For this type of clusters, it checks that there is only one modifier.
        Returns True or False, if cluster is not editable
        """

        # If not a list
        if not isinstance(modifiers, list):
            return False

        # If there is not exactly one modifier
        if len(modifiers) != 1:
            return False

        # If it is not an actual modifier
        if not isinstance(modifiers[0], bpy.types.Modifier):
            return False

        # If havent set modifiers already
        if self._modcluster_initialized is False:
            self._modifiers_list = modifiers
            self._modcluster_initialized = True
            return True

        # If allowed to reset modifiers
        elif self._MODCLUSTER_DYNAMIC:
            self._modifiers_list = modifiers
            return True

        else:
            return False
