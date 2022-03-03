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

from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    StringProperty,
    EnumProperty,
)

from .shortcuts import ModalShortcutsCache, ModalShortcut


class ModalShortcutsPreferences():
    """Mix-in class for bpy.types.AddonPreferences.

    It provides methods for displaying and editing modal operator shortcuts.
    """

    __need_modal_operators_shortcuts_cache_refresh = True
    __modal_operator_shortcuts_cache = None
    _modal_shortcuts = None

    emtk_modal_operators_serialized_shortcuts: StringProperty(
        name='Modal operators serialized shortcuts.',
        default='')

    @property
    def modal_shortcuts(self):
        self._check_cache_refresh()
        return self._modal_shortcuts

    @modal_shortcuts.setter
    def modal_shortcuts(self, val):
        if isinstance(val, ModalShortcutsCache):
            self._modal_shortcuts = val
        else:
            raise TypeError

    # Currently edited shortcut properties
    # Shortcut and group that is being edited
    emtk_editing_modal_shortcut_value: StringProperty("")
    emtk_editing_modal_shortcut_group: StringProperty("")

    # Its properties
    edited_shortcut_event_type: StringProperty(
        name="Letter", maxlen=1, default="")
    edited_shortcut_shift: BoolProperty(name="Shift", default=False)
    edited_shortcut_ctrl: BoolProperty(name="Ctrl", default=False)
    edited_shortcut_alt: BoolProperty(name="Alt", default=False)

    # This is search field
    shortcuts_groups_search_str: StringProperty(
        name="Search through emtk modal props groups",
        default=''
    )

    shortcuts_search_str: StringProperty(
        name="Search through emtk modal props",
        default=''
    )

    # Search

    def draw_shortcuts_search(self, context):
        return self.__draw_shortcuts_search(context)

    def __draw_shortcuts_search(self, context):
        layout = self.layout
        layout.prop(self, "shortcuts_groups_search_str")
        layout.prop(self, "shortcuts_search_str")

        self._check_cache_refresh()

        result = self.modal_shortcuts.search_by_shortcut_id(
            self.shortcuts_groups_search_str, self.shortcuts_search_str)

        if not result:
            layout.label(
                text="Type shortcut name above to see modal shortcuts.")
            layout.label(text="Example: bevel angle")
            return

        for x in result:
            self.layout.label(text=x.value)
            box = layout.box()
            for i, y in enumerate(x.search_by_shortcut_id(
                    self.shortcuts_search_str)):
                if i % 3 == 0:
                    row = box.row()
                col = row.column()
                if x.value == self.emtk_editing_modal_shortcut_group\
                        and y.shortcut_id\
                        == self.emtk_editing_modal_shortcut_value:
                    self.__draw_shortcut_editor(
                        col, x.value, y.shortcut_id, y)
                else:
                    self.__draw_shortcut(col, x.value, y.shortcut_id, y)

    # Draw shortcut

    def __draw_shortcut(self,
                        layout,
                        shortcuts_group_name: str,
                        shortcut_name: str,
                        shortcut):

        if type(shortcuts_group_name) is not str:
            raise TypeError
        if type(shortcut_name) is not str:
            raise TypeError
        if not isinstance(shortcut, ModalShortcut):
            raise TypeError

        b = layout.operator("emtk.start_editing_modal_shortcut",
                            text=f'{shortcut}')
        b.shortcut_name = shortcut_name
        b.shortcut_group = shortcuts_group_name

    def __draw_shortcut_editor(self,
                               layout,
                               shortcuts_group_name: str,
                               shortcut_name: str,
                               shortcut):

        row = layout.row()
        col = row.column()
        col.prop(self, "edited_shortcut_event_type")
        col = row.column()
        col.prop(self, "edited_shortcut_shift")
        col = row.column()
        col.prop(self, "edited_shortcut_ctrl")
        col = row.column()
        col.prop(self, "edited_shortcut_alt")

        a = layout.operator("emtk.add_or_update_modal_shortcut")
        a.shortcut_name = shortcut_name
        a.shortcut_group = shortcuts_group_name
        a.shortcut_event_type = self.edited_shortcut_event_type
        a.shortcut_shift = self.edited_shortcut_shift
        a.shortcut_ctrl = self.edited_shortcut_ctrl
        a.shortcut_alt = self.edited_shortcut_alt

    def save_cache(self):
        self.emtk_modal_operators_serialized_shortcuts\
            = self.modal_shortcuts.serialize()

    def refresh_cache(self):
        self._modal_shortcuts = ModalShortcutsCache(
            self.emtk_modal_operators_serialized_shortcuts)

    def _check_cache_refresh(self):
        if self._modal_shortcuts is None:
            self.refresh_cache()
