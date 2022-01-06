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


class VIEW3D_PT_bmtool_panel(Panel):
    bl_idname = "VIEW3D_PT_bmtool_panel"
    bl_label = "Edit clusters"
    bl_category = "BMTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"

    # Example:
    # {'Bevel': True, 'Array': False}
    modifiers_expanded = {}
    previous_objects = []
    tag_panel_invoke = False
    # tag_objects_changed = False

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
            cls.tag_panel_invoke = True
        return result

    def draw(self, context):
        if self.tag_panel_invoke:
            self.panel_invoke(context)
            self.tag_panel_invoke = False
        if self.tag_objects_changed:
            self.panel_objects_changed(context)
            # self.tag_objects_changed = False
        self.panel_draw(context)
        self.

    def panel_draw(self, context):
        layout = self.layout
        layout.label(text="BMTools modifiers panel")
        for x in context.object.modifiers:
            self.__draw_modifier_props(x)

    def panel_invoke(self, context):
        return

    def panel_objects_changed(self, context):
        return

    def check_if_objects_changed(self, context):
        """Returns True, if objects changed after previous iteration."""
        result = None
        if self.previous_objects != context.selected_objects:
            result = True
        if self.previous_active != context.object:
            result = True
        return result
            
            
        

    def __draw_modifier_props(self, modifier):
        if modifier.name not in self.modifiers_expanded:
            self.modifiers_expanded.update({modifier.name: True})

        layout = self.layout.box()
        row = layout.row()
        col = row.column()
        col.prop(modifier, 'name')
        col = row.column()

        # Expand
        x = col.operator('bmtools.update_panel_dict_attr', text='Expand')
        x.obj = self.bl_idname
        x.attr_name = 'modifiers_expanded'
        x.element_name = modifier.name
        x.action = 'ADD'
        x.element_val_type = 'BOOL'
        x.element_val_bool = not self.modifiers_expanded[modifier.name]

        # Props
        if self.modifiers_expanded[modifier.name]:
            p = get_all_editable_props(modifier)
            for y in p:
                layout.prop(modifier, f'{y}')

    # def set_dict_val(self, operator, val):
    #     if type(val) is bool:
    #         operator.element_val_type = 'BOOL'
    #         operator.element_val_bool = val
    #     if type(val) is int:
    #         operator.element_val_type = 'INT'
    #         operator.element_val_int = val
    #     if type(val) is float:
    #         operator.element_val_type = 'FLOAT'
    #         operator.element_val_float = val
    #     if type(val) is str:
    #         operator.element_val_type = 'STR'
    #         operator.element_val_str = val
    #     else:
    #         raise TypeError


class BMTOOLS_OT_update_panel_dict(Operator):
    bl_idname = "bmtools.update_panel_dict_attr"
    bl_label = "Change bmtools panel dict value."

    # Object to set attr for
    obj: StringProperty("")

    # Attribute name (expecting dict)
    attr_name: StringProperty("")

    # Action in {'ADD', 'REPLACE', 'REMOVE'}
    action: StringProperty("")

    # Dict key
    element_name: StringProperty("")

    # Dict value type str in {'BOOL', 'INT', 'FLOAT', 'STR'}
    element_val_type: StringProperty("")

    # Dict value (only one prop used)
    element_val_bool: BoolProperty(False)
    element_val_int: IntProperty(0)
    element_val_float: FloatProperty(0.0)
    element_val_str: StringProperty("")

    def execute(self, context):
        if len(self.obj) == 0:
            raise ValueError
        if len(self.attr_name) == 0:
            raise ValueError
        if '.' in self.obj:
            raise ValueError
        if '.' in self.attr_name:
            raise ValueError

        x = getattr(bpy.types, self.obj)
        attr = getattr(x, self.attr_name)

        if not isinstance(attr, dict):
            raise TypeError

        if self.element_val_type == 'BOOL':
            val = self.element_val_bool
        elif self.element_val_type == 'INT':
            val = self.element_val_int
        elif self.element_val_type == 'FLOAT':
            val = self.element_val_float
        elif self.element_val_type == 'STR':
            val = self.element_val_str
        else:
            raise ValueError

        if self.action == 'ADD':
            attr.update({self.element_name: val})
        elif self.action == 'REPLACE':
            if self.modifier_name in attr:
                attr.update({self.element_name: val})
        elif self.action == 'REMOVE':
            attr.pop('self.element_name')
        else:
            raise ValueError

        return {'FINISHED'}
