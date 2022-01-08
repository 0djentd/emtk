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


import bpy

from bpy.props import BoolProperty, IntProperty, FloatProperty, StringProperty
from bpy.types import Panel, Operator

from ..lib.utils.modifier_prop_types import get_all_editable_props


class BlenderUIWrapper():
    """Base class for EMTK panels and menus.
    Provides additional methods based on 'poll' and 'draw' methods.
    """
    __tag_panel_init = True
    __tag_panel_invoke = True
    __panel_was_drawn = False

    __previous_active_object_id = None
    __previous_selected_objects_id = None
    __active_object_changed = True
    __selected_objects_changed = True

    __debug = True

    # Public properties.
    @classmethod
    @property
    def active_object_changed(cls)
        return cls.__active_object_changed

    @classmethod
    @property
    def selected_objects_changed(cls)
        return cls.__selected_objects_changed

    # Public methods that should not be overloaded. {{{
    @classmethod
    def poll(cls, context):
        # INIT
        if cls.__tag_panel_init:
            cls.panel_init(cls, context)
            cls.__tag_panel_init = False
        else:
            # POLL
            allow_draw = cls.panel_poll(cls, context)

        # REMOVE
        if not allow_draw:
            cls.__tag_panel_invoke = True
            cls.__panel_was_drawn = False
            if cls.__panel_was_drawn:
                cls.panel_remove(context)
        return allow_draw

    def draw(self, context):
        # get state
        active_object = id(context.object)
        selected_objects = []
        for x in context.selected_objects:
            selected_objects.append(id(x))

        # public variables
        if active_object != self.__previous_active_object:
            self.active_object_changed = True
        if selected_objects != self.__previous_selected_objects:
            self.selected_objects_changed = True

        # store state
        self.__previous_active_object = active_object
        self.__previous_selected_objects = selected_objects

        # INVOKE
        if self.__tag_panel_invoke:
            self.panel_invoke(context)
            self.__tag_panel_invoke = False
        self.__panel_was_drawn = True

        # DRAW
        self.panel_draw(context)
    # }}}

    # Public methods {{{
    @classmethod
    def panel_init(cls, context):
        """This method called once per Blender launch or addon
        reload on first object poll.

        It should have classmethod decorator.
        It should return None.
        """
        if cls.__debug:
            print('Panel was initiated')
        return

    @classmethod
    def panel_poll(cls, context):
        """This method called every time object is polled.

        It should have classmethod decorator.
        It should return True or False.
        """
        if cls.__debug:
            print('Panel was polled')
        return

    def panel_invoke(self, context):
        """This method called every time object is drawn after failed poll.
        Also called on first draw after Blender launch or addon reload.

        It should return None.
        """
        if self.__debug:
            print('Panel was invoked')
        return

    def panel_draw(self, context):
        """This method called every time object drawn.

        It should return None.
        """
        if self.__debug:
            print('Panel was drawn')
        return

    @classmethod
    def panel_remove(cls, context):
        """This method called every time object poll failed
        after successfull draw.

        It should have classmethod decorator.
        It should return None.
        """
        if cls.__debug:
            print('Panel was removed')
        return
    # }}}


class VIEW3D_PT_bmtool_panel(BlenderUIWrapper, Panel):
    bl_idname = "VIEW3D_PT_bmtool_panel"
    bl_label = "Edit clusters"
    bl_category = "BMTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"

    # Example:
    # {'Bevel': True, 'Array': False}
    modifiers_expanded = {}

    # Panel methods {{{
    @classmethod
    def panel_poll(cls, context):
        if context.object is None:
            allow_draw = False
        elif len(context.selected_objects) < 1:
            allow_draw = False
        else:
            allow_draw = True
        return allow_draw

    def panel_draw(self, context):
        if self.active_object_changed:
            self.modifiers_expanded = {}

        layout = self.layout
        layout.label(text="BMTools modifiers panel")
        for x in context.object.modifiers:
            self.__draw_modifier_props(x)
    # }}}

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


# Workaround to change panel class variables from button.
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
