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

import copy
import bpy

from ..modifiers_list import ModifiersList

# Modifiers List utils
# Modifiers List
# Modifiers Clusters parser
# Modifiers Clusters List
# ----------------------
# Object Modifiers Clusters List
# ----------------------


class ObjectClustersListTrait():
    """
    This is class that can be used to add methods
    for editing object's modifiers to ClustersList.
    """

    __NO_OBJ = False

    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.__NO_OBJ:
            if obj is None:
                raise ValueError

        self._object = obj

    # ===================================
    # Changing modifiers_list of an object
    # ===================================
    def move_up(self, mod):
        """
        Moves cluster up.

        This method can be used from any
        ObjectModifiersClustersList, including
        nested modifiers clusters.

        Returns False if modifier already last in list.
        """
        return self.move_cluster(mod, 'UP')

    def move_down(self, mod):
        """
        Moves cluster down

        This method can be used from any
        ObjectModifiersClustersList, including
        nested modifiers clusters.

        Returns False if modifier already first in list
        """
        return self.move_cluster(mod, 'DOWN')

    def move_cluster(self, mod, direction):
        """
        Moves cluster in blender modifiers
        stack. Direction should be either UP or DOWN.
        """

        if not isinstance(mod, ModifiersList):
            raise TypeError

        ui_t = []

        # Index of cluster in this list.
        x = self.get_index(mod)

        # Dont move, if cluster is last or first.
        if direction == 'UP':
            if x == 0:
                return False
        elif direction == 'DOWN':
            if x == self.get_list_length() - 1:
                return False
        else:
            raise ValueError

        # Info
        for line in self._modifiers_list_info():
            ui_t.append(f"{line}")
        ui_t.append("Moving modifiers.")

        # Get actual modifiers.
        modifiers_to_be_moved = copy.copy(
                mod.get_full_actual_modifiers_list())

        # Get cluster that cluster will be moved through.
        if direction == 'UP':
            mod_to_be_moved_through = self.get_by_index(x-1)
        elif direction == 'DOWN':
            mod_to_be_moved_through = self.get_by_index(x+1)

        # Ask cluster if it can be moved
        if not mod.cluster_being_moved(
                self._modifiers_list, direction):
            return False

        # Ask cluster that will be moved through if it can be moved
        if not mod_to_be_moved_through.cluster_being_moved(
                self._modifiers_list, direction):
            return False

        # How many times actual modifiers need to be moved.
        modifier_move_count = len(
                mod_to_be_moved_through.get_full_actual_modifiers_list())

        # Reverse modifier sequence
        if direction == 'DOWN':
            modifiers_to_be_moved.reverse()

        # Move modifiers.
        for z in range(modifier_move_count):
            ui_t.append(
                    "Moving actual modifiers inside of clusters lists.")
            for actual_modifier in modifiers_to_be_moved:
                ui_t.append(f"Moving {actual_modifier}")
                if direction == 'UP':
                    if self._ModifiersList__DUMMY_MODIFIERS:
                        self._dummy_modifiers.modifier_move_up(
                                modifier=actual_modifier.name)
                    else:
                        bpy.ops.object.modifier_move_up(
                                modifier=actual_modifier.name)
                elif direction == 'DOWN':
                    if self._ModifiersList__DUMMY_MODIFIERS:
                        self._dummy_modifiers.modifier_move_down(
                                modifier=actual_modifier.name)
                    else:
                        bpy.ops.object.modifier_move_down(
                                modifier=actual_modifier.name)

        # Move modifier in list.
        moved_mod = self._modifiers_list.pop(x)
        if direction == 'UP':
            self._modifiers_list.insert(x - 1, moved_mod)
        if direction == 'DOWN':
            self._modifiers_list.insert(x + 1, moved_mod)

        # Info.
        ui_t.append("Finished moving modifiers.")
        for line in self._modifiers_list_info():
            ui_t.append(f"{line}")
        for line in ui_t:
            self._additional_info_log.append(line)

        return True

    def move_clusters(self, clusters, direction):
        """
        Moves list of clusters.

        Returns True or False.
        """
        if not isinstance(clusters, list):
            raise TypeError

        # Dont move, if modifier is last or first.
        if direction == 'UP':
            x = self.get_index(clusters[0])
            if x == 0:
                return False
        elif direction == 'DOWN':
            x = self.get_index(clusters[-1])
            if x == self.get_list_length() - 1:
                return False
        else:
            raise ValueError

        clusters_to_move = copy.copy(clusters)

        if direction == 'DOWN':
            clusters_to_move = clusters_to_move.reverse()

        for cluster in clusters_to_move:
            if direction == 'UP':
                if not self.move_up(cluster):
                    return False
            elif direction == 'DOWN':
                if not self.move_down(cluster):
                    return False
        return True

    def move_to_index(self, mod, i):
        """
        Moves cluster to index.

        Returns True if moved modifier.
        Returns False if any errors.
        """
        # TODO: not tested
        if i < self.get_list_length():
            m_i = self.get_index(mod)
            d_i = i - m_i
            x = 0
            if d_i > 0:
                while x <= d_i:
                    self.move_up(mod)
                    x += 1
                return True
            elif d_i < 0:
                while x >= d_i:
                    self.move_up(mod)
                    x -= 1
                return True
