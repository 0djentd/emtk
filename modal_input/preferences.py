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

import math
# import re

from bpy.props import (
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       )
from .shortcuts import (
                        serialize_kbs,
                        deserialize_kbs,
                        check_shortcuts_formatting,
                        check_shortcuts_group_formatting,
                        check_shortcut_formatting,
                        check_shortcut_element_formatting,
                        filter_shortcuts_group_by_str,
                        search_modal_operators_shortcuts,
                        generate_new_shortcut,
                        )


class ModalShortcutsPreferences():
    """
    Mix-in class for AddonPreferences.

    It provides methods for displaying editing modal operator shortcuts.
    """

    __need_modal_operators_shortcuts_cache_refresh = True
    __modal_operator_shortcuts_cache = None
    __last_bmtools_str_search = None

    # Serialized shortcuts. {{{
    """
    Serialized keyboard shortcuts to be used in adaptive modifiers
    editor.

    Examples:
    kbs = {
           # Group
           'bevel': {
                     # Prop
                     'angle_limit': {'letter': 'A',
                                     'shift': True,
                                     'ctrl': False,
                                     'alt': False,
                                     'sens': 0.005
                                     }
                     }
           }
    {{{
    """
    bmtool_modal_operators_serialized_shortcuts: StringProperty(
            name='Modal operators serialized shortcuts.',
            default='{"BEVEL": {"angle_limit": {"letter": "A", "shift": false, "ctrl": false, "alt": false, "sens": 0.0005}}}'
            )
    # }}}

    # Currently edited shortcut props {{{
    # Shortcut and group that is being edited
    bmtool_editing_modal_shortcut_name: StringProperty("")
    bmtool_editing_modal_shortcut_group: StringProperty("")

    # Its properties
    edited_shortcut_letter: StringProperty(name="Letter", maxlen=1, default="")
    edited_shortcut_shift: BoolProperty(name="Shift", default=False)
    edited_shortcut_ctrl: BoolProperty(name="Ctrl", default=False)
    edited_shortcut_alt: BoolProperty(name="Alt", default=False)
    edited_shortcut_sens: FloatProperty(name="Sens", default=1)

    # This is search field
    shortcuts_groups_search_str: StringProperty(
            name="Search through bmtool modal props groups",
            default=''
            )

    shortcuts_search_str: StringProperty(
            name="Search through bmtool modal props",
            default=''
            )
    # }}}

    # Search {{{
    def __draw_shortcuts_search(self, context):
        layout = self.layout
        layout.prop(self, "shortcuts_groups_search_str")
        layout.prop(self, "shortcuts_search_str")

        if len(self.shortcuts_search_str) != 'NO_SHORTCUTS':

            self.__refresh_modal_opertors_shortcuts_cache()

            # Get filtered version of shortcuts.
            if self.__last_bmtools_str_search != self.shortcuts_search_str:
                props_groups_filtered = search_modal_operators_shortcuts(
                        self.__modal_operator_shortcuts_cache,
                        self.shortcuts_search_str)
                self.__props_groups_filtered_cache = props_groups_filtered
            else:
                self.__last_bmtools_str_search = self.shortcuts_search_str
                props_groups_filtered = self.__props_groups_filtered_cache

            # Filter by group
            if self.shortcuts_groups_search_str != "":
                props_groups_to_display = {}
                for x in props_groups_filtered:
                    if self.shortcuts_groups_search_str.upper() in x:
                        props_groups_to_display.update(
                                {x: props_groups_filtered[x]})
            else:
                props_groups_to_display = props_groups_filtered

            # Draw
            self.__draw_shortcuts_groups_dict(layout, props_groups_to_display)

        else:
            layout.label(
                    text="Type shortcut name above to see modal shortcuts.")
            layout.label(text="Example: bevel angle")
    # }}}

    # Draw shortcut {{{
    def __draw_shortcuts_groups_dict(
            self, layout, shortcut_groups_dict: dict):
        if not isinstance(shortcut_groups_dict, dict):
            raise TypeError

        layout = layout.box()
        layout.label(text="Shortcuts")
        for x, y in zip(
                shortcut_groups_dict.keys(),
                shortcut_groups_dict.values()):
            box = layout.box()
            self.__draw_shortcuts_group(box, x, y)
        return

    def __draw_shortcuts_group(
            self, layout, shortcuts_group_name: str, shortcut_group: dict):
        if not isinstance(shortcuts_group_name, str):
            raise TypeError
        if not isinstance(shortcut_group, dict):
            raise TypeError

        layout.label(text=shortcuts_group_name)
        i = 0
        row = None
        for x, y in zip(shortcut_group.keys(), shortcut_group.values()):
            if math.remainder(i, 5) == 0:
                row = layout.row()
            col = row.column()
            self.__draw_shortcut(col, shortcuts_group_name, x, y)
            i += 1
            if i == len(shortcut_group.values()):
                for x in range(int(math.remainder(i, 5))):
                    col = row.column()
                    col.label(text="")
        return

    def __draw_shortcut(self,
                        layout,
                        shortcuts_group_name: str,
                        shortcut_name: str,
                        shortcut: dict):

        if not isinstance(shortcut_name, str):
            raise TypeError
        if not isinstance(shortcut, dict):
            raise TypeError

        if not check_shortcut_formatting(shortcut):
            layout.label(text='Shortcut is broken.')
            return
        # Example:
        # 'bevel: angle_limit: [letter=A, shift=True, sens=0.0005]'
        t = f"{shortcut_name}: ["
        # Shortcut's elements.
        i = 0
        for z, v in zip(shortcut.keys(), shortcut.values()):
            if type(v) == float:
                t = t + f"{z}={round(v, 2)}"
            else:
                t = t + f"{z}={v}"

            if i < (len(shortcut) - 1):
                t = t + ', '
            i += 1
        t = t + "]"

        b = layout.operator("bmtools.start_editing_modal_shortcut",
                            text=t)

        b.shortcut_name = shortcut_name
        b.shortcut_group = shortcuts_group_name

        if self.bmtool_editing_modal_shortcut_name == shortcut_name\
                and self.bmtool_editing_modal_shortcut_group\
                == shortcuts_group_name:
            self.__draw_shortcut_editor(
                    layout, shortcut_name, shortcuts_group_name)
        return

    def __draw_shortcut_editor(
            self, layout, shortcut_name, shortcuts_group_name):
        row = layout.row()
        col = row.column()
        col.prop(self, "edited_shortcut_letter")
        col = row.column()
        col.prop(self, "edited_shortcut_shift")
        col = row.column()
        col.prop(self, "edited_shortcut_ctrl")
        col = row.column()
        col.prop(self, "edited_shortcut_alt")
        col = row.column()
        col.prop(self, "edited_shortcut_sens")

        a = layout.operator("bmtools.add_or_update_modal_shortcut")

        a.shortcut_name\
            = self.bmtool_editing_modal_shortcut_name
        a.shortcut_group\
            = self.bmtool_editing_modal_shortcut_group

        a.shortcut_letter = self.edited_shortcut_letter
        a.shortcut_shift = self.edited_shortcut_shift
        a.shortcut_ctrl = self.edited_shortcut_ctrl
        a.shortcut_alt = self.edited_shortcut_alt
        a.shortcut_sens = self.edited_shortcut_sens
    # }}}

    # Cache {{{
    def get_modal_operators_shortcuts_group(
            self, group_name: str, strict_checks=False) -> dict:
        """This method should be used to get shortcuts in operator."""
        if not isinstance(group_name, str):
            raise TypeError

        self.__refresh_modal_opertors_shortcuts_cache()
        if group_name in self.__modal_operator_shortcuts_cache:
            g = self.__modal_operator_shortcuts_cache[group_name]
            check_shortcuts_group_formatting(g)
            return g
        else:
            print(f'No modal operators shortcuts group named {group_name}')
            if strict_checks:
                raise ValueError
            else:
                return {}

    def refresh_modal_opertors_shortcuts_cache(self):
        self.__refresh_modal_opertors_shortcuts_cache()

    def __refresh_modal_opertors_shortcuts_cache(self):
        """Load serialized shortcuts from json str."""
        if not self.__need_modal_operators_shortcuts_cache_refresh:
            return
        self.__modal_operator_shortcuts_cache = deserialize_kbs(
                    self.bmtool_modal_operators_serialized_shortcuts)
        self.__need_modal_operators_shortcuts_cache_refresh = False

    def add_modal_operators_shortcuts_group(self, group_name: str) -> bool:
        """Add new modal operators shortcuts group."""
        if not isinstance(group_name, str):
            raise TypeError

        self.__refresh_modal_opertors_shortcuts_cache()
        if group_name not in self.__modal_operator_shortcuts_cache:
            g = {group_name: {}}
            self.__modal_operator_shortcuts_cache.update(g)
            return True
        return False

    def add_modal_operators_shortcut(
            self, group_name: str, shortcut: dict) -> bool:
        """Add new modal operators shortcut.

        This method only edits cache, not serialized str.
        save_modal_operators_shortcuts_cache should be used after editing.

        Expecting dict with dicts as its values.
        Example:
        {"angle_limit": {"letter": "A",
                         "shift": false,
                         "ctrl": false,
                         "alt": false,
                         "sens": 0.0005}}
        """

        print(f'Adding {shortcut}')
        if not isinstance(group_name, str):
            raise TypeError
        if not isinstance(shortcut, dict):
            raise TypeError
        for x in shortcut:
            if not isinstance(shortcut[x], dict):
                raise TypeError
            if len(shortcut[x]) < 4:
                raise ValueError(shortcut)
        if len(shortcut) > 1:
            raise ValueError

        for x, y in zip(shortcut.keys(), shortcut.values()):
            check_shortcut_formatting(shortcut[x])

        self.add_modal_operators_shortcuts_group(group_name)
        self.__modal_operator_shortcuts_cache[group_name].update(shortcut)

    def save_modal_operators_shortcuts_cache(self):
        """Saves modal operators shortcuts cache to prop."""

        s = serialize_kbs(self.__modal_operator_shortcuts_cache)
        self.bmtool_modal_operators_serialized_shortcuts = s
    # }}}