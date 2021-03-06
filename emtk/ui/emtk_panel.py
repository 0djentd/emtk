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

from bpy.types import Panel
from libemtk.utils.modifier_prop_types import get_all_editable_props

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
# class BlenderUIWrapper():
#     """Base class for libemtk panels and menus.
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
#     # Public properties.
#     @classmethod
#     @property
#     def active_object_changed(cls):
#         return cls.__active_object_changed
#
#     @classmethod
#     @property
#     def selected_objects_changed(cls):
#         return cls.__selected_objects_changed
#
#
#     # Public methods that should not be overloaded.
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
#
#
#     # Public methods
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
#
#


class VIEW3D_PT_emtk_panel(Panel):
    bl_idname = "VIEW3D_PT_emtk_panel"
    bl_label = "Edit clusters"
    bl_category = "EMTK"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"

    instances = []

    # TODO: move to base class.
    # WRAPPER
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

    # Properties.
    @classmethod
    @property
    def active_object_changed(cls):
        return cls.__active_object_changed

    @classmethod
    @property
    def selected_objects_changed(cls):
        return cls.__selected_objects_changed

    # tag panel invoke
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

    # panel was drawn

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

    # Public methods that should not be overloaded.

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

    # Public methods

    @classmethod
    def panel_init(cls, context):
        """This method called once per Blender launch or addon
        reload on first object poll.

        It should have classmethod decorator.
        It should return None.
        """
        return

    # Example:
    # {'Bevel': True, 'Array': False}
    modifiers_expanded = {}

    # Panel methods
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
        layout.label(text="EMTK modifiers panel")
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

    def __draw_modifier_props(self, modifier):
        layout = self.layout.box()

        # Props
        if modifier.show_expanded:
            p = get_all_editable_props(modifier)
            for y in p:
                layout.prop(modifier, f'{y}')
