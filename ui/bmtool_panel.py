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

from bpy.props import BoolProperty, IntProperty, FloatProperty, StringProperty
from bpy.types import Panel, Operator

from ..lib.utils.modifier_prop_types import get_all_editable_props


class VIEW_3D_PT_bmtool_panel(Panel):
    bl_idname = "VIEW_3D_PT_bmtool_panel"
    bl_label = "Edit clusters"
    bl_category = "BMTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"

    __previous_state = False

    def __init__(self):
        self.__previous_state = False

    @classmethod
    def poll(cls, context):
        result = None
        if context.object is None:
            result = False
        elif len(context.selected_objects) < 1:
            result = False
        else:
            result = True
        if not result:
            cls.__previous_state = result
        return result

    def draw(self, context):
        if not self.__previous_state:
            # bpy.ops.bmtools.close_all_modifiers()
            # self.close_modifiers(context)
            self.__previous_state = True
            print(self)
            print(self.__previous_state)

        layout = self.layout
        layout.label(text="BMTools clusters panel")
        for x in context.object.modifiers:
            self.__draw_modifier_props(x)

    def close_modifiers(self, context):
        for x in context.object.modifiers:
            x.show_expanded = False

    def __draw_modifier_props(self, modifier):
        layout = self.layout.box()
        row = layout.row()
        col = row.column()
        col.prop(modifier, 'name')
        col = row.column()
        col.prop(modifier, 'show_expanded')
        p = get_all_editable_props(modifier)
        if modifier.show_expanded:
            for y in p:
                layout.prop(modifier, f'{y}')
