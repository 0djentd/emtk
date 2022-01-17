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

from bpy.types import Operator

from ..lib.modifiers_operator import ModifiersOperator
from ..lib.utils.modifiers import get_modifier_state


class BMTOOL_OT_bmtoole2(ModifiersOperator, Operator):
    bl_idname = "object.bmtoole2"
    bl_label = "BMToolE2"
    bl_description = "Add modifiers on selected objects"

    @classmethod
    def poll(self, context):
        if context.area.type != 'VIEW_3D':
            return False
        elif context.mode != 'OBJECT' and self._BMTOOL_EDITMODE is False:
            return False
        elif len(context.selected_objects) > 1 and self._BMTOOL_SINGLE_OBJECT:
            return False
        elif len(context.selected_objects) == 0:
            return False
        elif context.object.type != 'MESH':
            return False
        return True

    def execute(self, context):

        modifiers = []
        for x in context.object.modifiers:
            modifiers.append(x)

        mods = []
        if (len(modifiers)) == 0:
            for x in range(1):
                mod = context.object.modifiers.new('Bevel', 'BEVEL')
                mod.segments = 1
                mods.append(mod)

        self.create_objects_modifiers_lists(context)

        self.m_list[0].set_this_cluster_visibility(
                (True, False, True, False))
        print(get_modifier_state(self.m_list._object.modifiers['Bevel']))
        del(self.selected_objects)
        del(self.m_list)
        return {'FINISHED'}
