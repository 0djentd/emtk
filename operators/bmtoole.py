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
from bpy.types import Operator

from ..lib.modifiers_operator import ModifiersOperator


class BMTOOL_OT_bmtoole(ModifiersOperator, Operator):
    bl_idname = "object.bmtoole"
    bl_label = "BMToolE"
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
        self.create_objects_modifiers_lists(context)
        bpy.ops.object.shade_smooth()
        context.object.data.use_auto_smooth = True
        t = ['BEVEL', 'BOOLEAN', 'BEVEL', 'WEIGHTED_NORMAL']
        for x in t:
            self.m_list.create_modifier(x, x)
        self.report({'INFO'}, "Created a lot of modifiers")
        t.clear()
        return {'FINISHED'}
