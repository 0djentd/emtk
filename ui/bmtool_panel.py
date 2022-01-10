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


"""
Panels instancing cache workarounds.

So, basically, panels are being instantiated every 'draw' iteration.
This explains why __init__ being called on draw.
This is different from modal operators, that are instanced once.
However, 'draw' method is creating new instance every iteration there
too, as well as in usual operators.

If there is need to store data between iterations, class variables
should be used.

Some features like 'init', 'invoke' and 'remove' method can be
implemented through class variables.

Panels can have multiple 'instances' in user interface though, not
necessary with same context.

I assume this is possible to have cache for multiple 'instances'
in class variables by identyfing panels somehow.
"""
# TODO: No idea why this doesnt work properly with inheritance.
# class BlenderUIWrapper():  # {{{
#     """Base class for EMTK panels and menus.
#     Provides additional methods based on 'poll' and 'draw' methods.
#     """
#     __tag_panel_init = True
#     __tag_panel_invoke = True
#     __panel_was_drawn = False
# 
#     __previous_active_object_id = None
#     __previous_selected_objects_id = None
#     __active_object_changed = True
#     __selected_objects_changed = True
# 
#     __debug = True
# 
#     # Public properties.  # {{{
#     @classmethod
#     @property
#     def active_object_changed(cls):
#         return cls.__active_object_changed
# 
#     @classmethod
#     @property
#     def selected_objects_changed(cls):
#         return cls.__selected_objects_changed
#     # }}}
# 
#     # Public methods that should not be overloaded. {{{
#     @classmethod
#     def poll(cls, context):
#         # INIT
#         if cls.__tag_panel_init:
#             cls.panel_init(context)
#             if cls.__debug:
#                 print('Panel was initiated')
#             cls.__tag_panel_init = False
# 
#         # POLL
#         allow_draw = cls.panel_poll(context)
#         if cls.__debug:
#             print('Panel was polled')
# 
#         # REMOVE
#         if not allow_draw:
#             cls.__tag_panel_invoke = True
#             if cls.__panel_was_drawn:
#                 cls.panel_remove(context)
#                 if cls.__debug:
#                     print('Panel was removed')
#             cls.__panel_was_drawn = False
#         if cls.__debug:
#             print(allow_draw)
#         return allow_draw
# 
#     def draw(self, context):
#         # get state
#         active_object = id(context.object)
#         selected_objects = []
#         for x in context.selected_objects:
#             selected_objects.append(id(x))
# 
#         # public variables
#         if active_object != self.__previous_active_object_id:
#             self.active_object_changed = True
#         if selected_objects != self.__previous_selected_objects_id:
#             self.selected_objects_changed = True
# 
#         # store state
#         self.__previous_active_object_id = active_object
#         self.__previous_selected_objects_id = selected_objects
# 
#         # INVOKE
#         a = self.__tag_panel_invoke
#         if a:
#             self.panel_invoke(context)
#             if self.__debug:
#                 print('Panel was invoked')
#             self.__tag_panel_invoke = False
#         self.__panel_was_drawn = True
# 
#         # DRAW
#         self.panel_draw(context)
#         if self.__debug:
#             print('Panel was drawn')
#     # }}}
# 
#     # Public methods {{{
#     @classmethod
#     def panel_init(cls, context):
#         """This method called once per Blender launch or addon
#         reload on first object poll.
# 
#         It should have classmethod decorator.
#         It should return None.
#         """
#         return
# 
#     @classmethod
#     def panel_poll(cls, context):
#         """This method called every time object is polled.
# 
#         It should have classmethod decorator.
#         It should return True or False.
#         """
#         raise RuntimeError('No panel-specific method.')
# 
#     def panel_invoke(self, context):
#         """This method called every time object is drawn after failed poll.
#         Also called on first draw after Blender launch or addon reload.
# 
#         It should return None.
#         """
#         return
# 
#     def panel_draw(self, context):
#         """This method called every time object drawn.
# 
#         It should return None.
#         """
#         return
# 
#     @classmethod
#     def panel_remove(cls, context):
#         """This method called every time object poll failed
#         after successfull draw.
# 
#         It should have classmethod decorator.
#         It should return None.
#         """
#         return
#     # }}}
# # }}}


class VIEW3D_PT_bmtool_panel(Panel):
    bl_idname = "VIEW3D_PT_bmtool_panel"
    bl_label = "Edit clusters"
    bl_category = "BMTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"

    instances = []

    # TODO: move to base class.
    # WRAPPER  {{{
    __tag_panel_init = True
    __tag_panel_invoke_value = True
    __panel_was_drawn_value = False

    __previous_active_object_id = None
    __previous_selected_objects_id = None
    __active_object_changed = True
    __selected_objects_changed = True

    __debug = True

    def get_instance_variables(self):
        """
        Returns 'instance' variables from class variables.
        This is workaround for panel instancing.
        """
        return type(self).instances[0]

    # Properties.  # {{{
    @classmethod
    @property
    def active_object_changed(cls):
        return cls.__active_object_changed

    @classmethod
    @property
    def selected_objects_changed(cls):
        return cls.__selected_objects_changed

    # tag panel invoke  {{{
    @property
    def __tag_panel_invoke(self):
        self._get_tag_panel_invoke()

    @__tag_panel_invoke.setter
    def __tag_panel_invoke(self, val):
        self._set_tag_panel_invoke(val)

    @classmethod
    def _get_tag_panel_invoke(cls):
        return cls.__tag_panel_invoke_value

    @classmethod
    def _set_tag_panel_invoke(cls, val):
        cls.__tag_panel_invoke_value = val
    # }}}

    # panel was drawn  {{{
    @property
    def __panel_was_drawn(self):
        self._get_panel_was_drawn()

    @__panel_was_drawn.setter
    def __panel_was_drawn(self, val):
        self._set_panel_was_drawn(val)

    @classmethod
    def _get_panel_was_drawn(cls):
        return cls.__panel_was_drawn_value

    @classmethod
    def _set_panel_was_drawn(cls, val):
        cls.__panel_was_drawn_value = val
    # }}}
    # }}}

    # Public methods that should not be overloaded. {{{
    @classmethod
    def poll(cls, context):
        if cls.__debug:
            print(cls, type(cls))
            print(cls.instances)
            for x in cls.instances:
                print(id(x))
            print(id(cls))

        # TODO: move to draw
        # INIT
        if cls.__tag_panel_init:
            cls.panel_init(context)
            if cls.__debug:
                print('Panel was initiated')
            cls.__tag_panel_init = False

        # POLL
        allow_draw = cls.panel_poll(context)
        if cls.__debug:
            print('Panel was polled')

        # TODO: move to draw
        # REMOVE
        if not allow_draw:
            cls.__tag_panel_invoke = True
            if cls.__panel_was_drawn:
                cls.panel_remove(context)
                if cls.__debug:
                    print('Panel was removed')
            cls.__panel_was_drawn = False
        if cls.__debug:
            print(allow_draw)
        return allow_draw

    def draw(self, context):
        cls = type(self)
        if self.__debug:
            print(self, cls, type(cls))
            print(cls.instances)
            print(self.instances)
            for x in self.instances:
                print(id(x))
            print(id(self))

        if self not in cls.instances:
            cls.instances.append(self)

        # get state
        active_object = id(context.object)
        selected_objects = []
        for x in context.selected_objects:
            selected_objects.append(id(x))

        # public variables
        if active_object != cls.__previous_active_object_id:
            self.active_object_changed = True
        if selected_objects != cls.__previous_selected_objects_id:
            self.selected_objects_changed = True

        # store state
        cls.__previous_active_object_id = active_object
        cls.__previous_selected_objects_id = selected_objects

        # INVOKE
        a = cls.__tag_panel_invoke
        if a:
            self.panel_invoke(context)
            if self.__debug:
                print('Panel was invoked')
            cls.__tag_panel_invoke = False
        cls.__panel_was_drawn = True

        # DRAW
        self.panel_draw(context)
        if cls.__debug:
            print('Panel was drawn')
    # }}}

    # Public methods {{{
    @classmethod
    def panel_init(cls, context):
        """This method called once per Blender launch or addon
        reload on first object poll.

        It should have classmethod decorator.
        It should return None.
        """
        return

    # }}}
    # }}}

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

    def panel_invoke(self, context):
        cls = type(self)
        self = type(self)
        self.modifiers_expanded = {}
        for x in context.object.modifiers:
            cls.modifiers_expanded.update({x.name: x.show_expanded})

    @classmethod
    def panel_remove(cls, context):
        cls.modifiers_expanded = {}
    # }}}

    def __draw_modifier_props(self, modifier):
        cls = type(self)
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
        if cls.modifiers_expanded[modifier.name]:
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


class BMTOOLS_OT_bmtool_invoke_operator_func(Operator):
    """Workaround to change panel class variables from button."""
    bl_idname = "bmtools.bmtool_invoke_operator_func"
    bl_label = "Invoke one of bmtools operator functions."
    
    # Line to eval
    func: StringProperty("")

    # Variable to write result to
    returned_variable: StringProperty("")

    def execute(self, context):
        line = self.func
        line_2 = self.returned_variable
        if not isinstance(line, str):
            raise TypeError
        if not isinstance(line_2, str):
            raise TypeError
        if type(line) is not str:
            raise TypeError
        if type(line_2) is not str:
            raise TypeError

        if line[0:9] != 'bpy.types.'\
                and line[0:7] != 'bpy.ops.':
            raise ValueError

        for x in line[:]:
            if x not in string.ascii_letters\
                    and not in '()[],._ ':
                raise ValueError

        if len(line_2) > 4:
            if line_2[0:9] != 'bpy.types.'\
                    and line_2[0:7] != 'bpy.ops.':
                raise ValueError

            for x in line_2[:]:
                if x not in string.ascii_letters\
                        and not in list("[]'._"):
                    raise ValueError

        line = self.func
        result = eval(line)
        if len(line_2) > 4:
            line_2 = line_2 + ' = result'
            eval(line_2)
        print(f"'{line}'")
        print(f"'{result}'")
        print(f"'{line_2}'")
        return {'FINISHED'}

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
