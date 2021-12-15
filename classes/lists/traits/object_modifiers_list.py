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


class ObjectModifiersListTrait():
    """
    List of object modifiers.

    List that can somehow use Blender modifiers stack, but dont
    use clusters, should use it.

    Have methods for adding, removing, moving and sorting modifiers
    within Blender modifiers stack.
    """
    def __init__(self):
        super().__init__()

    # ===================================
    # Changing modifiers_list of an object
    # ===================================
    def move_up(self, mod):
        """
        Moves modifier up.
        Returns False if modifier already last in list.
        Returns False if cant move it.
        """
        return self._move_actual_modifier(mod, 'UP')

    def move_down(self, mod):
        """
        Moves modifier down
        Returns False if modifier already first in list
        """
        return self._move_actual_modifier(mod, 'DOWN')

    def _move_actual_modifier(self, mod, direction):
        """
        Moves actual_modifier in blender modifiers
        stack. Direction should be either UP or DOWN.
        """

        ui_t = []

        # Index of modifier in this list.
        x = self.get_index(mod)

        # Dont move, if modifier is last or first.
        if direction == 'UP':
            if x == 0:
                return False
        elif direction == 'DOWN':
            if x == self.get_list_length() - 1:
                return False

        # Info
        for line in self._modifiers_list_info():
            ui_t.append(f"{line}")
        ui_t.append("Moving modifiers.")

        if direction == 'UP':
            if self._ModifiersList__DUMMY_MODIFIERS:
                self._dummy_modifiers.modifier_move_up(
                        modifier=mod.name)
            else:
                bpy.ops.object.modifier_move_up(
                        modifier=mod.name)
        if direction == 'DOWN':
            if self._ModifiersList__DUMMY_MODIFIERS:
                self._dummy_modifiers.modifier_move_down(
                        modifier=mod.name)
            else:
                bpy.ops.object.modifier_move_down(
                        modifier=mod.name)

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
