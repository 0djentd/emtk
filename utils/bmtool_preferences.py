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

# import re
import json
import string

import bpy

from bpy.props import BoolProperty, IntProperty, FloatProperty, StringProperty
from bpy.types import AddonPreferences


class BMToolPreferences(AddonPreferences):  # {{{
    bl_idname = "bmtools"

    __need_modal_operators_shortcuts_cache_refresh = True
    __selected_shortcut = None
    __modal_operator_shortcuts_cache = None
    __strict_checks = True
    __last_bmtools_str_search = None


    # Settings {{{
    save_clusters: BoolProperty(
            name="Save clusters on operator finish",
            default=True
            )

    save_clusters_backup: BoolProperty(
            name="Save clusters backup on operator finish",
            default=True
            )

    backup_mesh_on_modifier_apply_remove: BoolProperty(
            name="Backup mesh on modifier apply or remove.",
            default=True
            )

    backup_collection_name: StringProperty(
            name="Name of collection that will be used for mesh backup.",
            default='BMToolM mesh backup'
            )

    custom_cluster_types: BoolProperty(
            name="Use custom cluster types.",
            default=True
            )

    always_add_custom_cluster_types: BoolProperty(
            name="Always add custom cluster types.",
            default=True
            )

    cluster_types: StringProperty(
            name="ClusterTypes",
            default="[]"
            )
    # }}}

    # KBS {{{
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

    # Currently edited shortcut props {{{
    """
    This props used to create fields in ui.
    """
    # Shortcut and group that is being edited
    bmtool_editing_modal_shortcut_name: StringProperty("")
    bmtool_editing_modal_shortcut_group: StringProperty("")

    bmtool_shortcut_letter: StringProperty(
            name="Shortcut mapping",
            maxlen=1,
            default="",
            )

    bmtool_shortcut_shift: BoolProperty(
            name="Shortcut require shift to be pressed",
            default=False
            )

    bmtool_shortcut_ctrl: BoolProperty(
            name="Shortcut require ctrl to be pressed",
            default=False
            )

    bmtool_shortcut_alt: BoolProperty(
            name="Shortcut require alt to be pressed",
            default=False
            )

    bmtool_shortcut_sens: FloatProperty(
            name="Sens",
            min=0.0,
            default=0.0
            )
    # }}}

    # This is search field
    bmtool_prop_search_str: StringProperty(
            name="Search through bmtool modal props",
            default=''
            )
    # }}}

    def draw(self, context):
        layout = self.layout
        layout.label(text="BMTool settings")
        layout.prop(self, "save_clusters")
        if self.save_clusters_backup:
            layout.prop(self, "save_clusters_backup")
        layout.prop(self, "backup_mesh_on_modifier_apply_remove")
        if self.backup_mesh_on_modifier_apply_remove:
            layout.prop(self, "backup_collection_name")
        layout.prop(self, "custom_cluster_types")
        if self.custom_cluster_types:
            layout.prop(self, "always_add_custom_cluster_types")
            layout.prop(self, "cluster_types")
        layout.prop(self, "bmtool_modal_operators_serialized_shortcuts")

        self.__draw_shortcuts_search()

    # Draw shortcut {{{
    def __draw_shortcuts_groups_dict(
            self, shortcut_groups_dict: dict):
        if not isinstance(shortcut_groups_dict, dict):
            raise TypeError

        for x, y in zip(
                shortcut_groups_dict.keys(),
                shortcut_groups_dict.values()):
            self.__draw_shortcuts_group(x, y)
        return

    def __draw_shortcuts_group(
            self, shortcuts_group_name: str, shortcut_group: dict):
        if not isinstance(shortcuts_group_name, str):
            raise TypeError
        if not isinstance(shortcut_group, dict):
            raise TypeError

        self.layout.label(text=shortcuts_group_name)
        for x, y in zip(shortcut_group.keys(), shortcut_group.values()):
            self.__draw_shortcut(shortcuts_group_name, x, y)
        return

    def __draw_shortcut(self,
                        shortcuts_group_name: str,
                        shortcut_name: str,
                        shortcut: dict):

        if not isinstance(shortcut_name, str):
            raise TypeError
        if not isinstance(shortcut, dict):
            raise TypeError

        if not check_shortcut_formatting(shortcut):
            self.layout.label(text='Shortcut is broken.')
            return
        # Example:
        # 'bevel: angle_limit: [letter=A, shift=True, sens=0.0005]'
        t = f"{shortcut_name}: ["
        # Shortcut's elements.
        i = 0
        for z, v in zip(shortcut.keys(), shortcut.values()):
            t = t + f"{z}={v}"
            if i < (len(shortcut) - 1):
                t = t + ', '
            i += 1
        t = t + "]"

        b = self.layout.operator("bmtools.start_editing_modal_shortcut",
                                 text=t)

        b.bmtool_operator_shortcut_name = shortcut_name
        b.bmtool_operator_shortcut_group = shortcuts_group_name

        if self.bmtool_editing_modal_shortcut_name == shortcut_name\
                and self.bmtool_editing_modal_shortcut_group\
                == shortcuts_group_name:
            self.__draw_shortcut_editor(shortcut_name, shortcuts_group_name)
        return

    def __draw_shortcut_editor(self, shortcut_name, shortcuts_group_name):
        layout = self.layout

        layout.prop(self, "bmtool_shortcut_letter")
        layout.prop(self, "bmtool_shortcut_shift")
        layout.prop(self, "bmtool_shortcut_ctrl")
        layout.prop(self, "bmtool_shortcut_alt")
        layout.prop(self, "bmtool_shortcut_sens")

        a = layout.operator("bmtools.add_or_update_modal_shortcut")

        a.bmtool_operator_shortcut_name\
            = self.bmtool_editing_modal_shortcut_name
        a.bmtool_operator_shortcut_group\
            = self.bmtool_editing_modal_shortcut_group

        a.bmtool_operator_shortcut_letter = self.bmtool_shortcut_letter
        a.bmtool_operator_shortcut_shift = self.bmtool_shortcut_shift
        a.bmtool_operator_shortcut_ctrl = self.bmtool_shortcut_ctrl
        a.bmtool_operator_shortcut_alt = self.bmtool_shortcut_alt
        a.bmtool_operator_shortcut_sens = self.bmtool_shortcut_sens
    # }}}

    def __draw_shortcuts_search(self):
        layout = self.layout
        layout.prop(self, "bmtool_prop_search_str")

        # keyboard shortcuts viewer {{{
        if len(self.bmtool_prop_search_str) > 1:

            self.__refresh_modal_opertors_shortcuts_cache()

            # Get filtered version of shortcuts.
            if self.__last_bmtools_str_search != self.bmtool_prop_search_str:
                props_groups_filtered = search_modal_operators_shortcuts(
                        self.__modal_operator_shortcuts_cache,
                        self.bmtool_prop_search_str)
                self.__props_groups_filtered_cache = props_groups_filtered
            else:
                props_groups_filtered = self.__props_groups_filtered_cache

            # Draw
            self.__draw_shortcuts_groups_dict(props_groups_filtered)

        else:
            layout.label(
                    text="Type shortcut name above to see modal shortcuts.")
            layout.label(text="Example: bevel angle")
        # }}}

    # Modal operators shortcuts cache {{{
    def __refresh_modal_opertors_shortcuts_cache(self):
        if not self.__need_modal_operators_shortcuts_cache_refresh:
            return
        self.__modal_operator_shortcuts_cache = deserialize_kbs(
                    self.bmtool_modal_operators_serialized_shortcuts)
        self.__need_modal_operators_shortcuts_cache_refresh = False

    def refresh_modal_opertors_shortcuts_cache(self):
        self.__refresh_modal_opertors_shortcuts_cache()

    def get_modal_operators_shortcuts_group(self, group_name: str) -> dict:
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
            if self.__strict_checks:
                raise ValueError
            else:
                return {}

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
        """Add new modal operators shortcut."""

        self.check_shortcut_formatting(shortcut)
        self.add_modal_operators_shortcuts_group(group_name)
        self.__modal_operator_shortcuts_cache[group_name].update(shortcut)

    def save_modal_operators_shortcuts_cache(self):
        """Saves modal operators shortcuts cache to prop."""

        s = serialize_kbs(self.__modal_operator_shortcuts_cache)
        self.bmtool_modal_operators_serialized_shortcuts = s
    # }}}
# }}}


# Functions {{{
def deserialize_kbs(kbs: str) -> dict:  # {{{
    """Deserialize string with shortcuts."""
    if not isinstance(kbs, str):
        raise TypeError
    shortcuts = json.loads(kbs)
    check_shortcuts_formatting(shortcuts)
    return shortcuts
# }}}


def serialize_kbs(shortcuts: dict) -> str:  # {{{
    """Serialize dict with shortcuts."""
    check_shortcuts_formatting(shortcuts)

    kbs = json.dumps(shortcuts)

    if not isinstance(kbs, str):
        raise TypeError
    if deserialize_kbs(kbs) != shortcuts:
        raise ValueError
    return kbs
# }}}


def check_shortcuts_formatting(shortcuts: dict) -> bool:  # {{{
    if not isinstance(shortcuts, dict):
        raise TypeError(f'Expected dict, got {type(shortcuts)}')
    for x in shortcuts:
        check_shortcuts_group_formatting(shortcuts[x])


def check_shortcuts_group_formatting(shortcuts_group: dict) -> bool:
    if not isinstance(shortcuts_group, dict):
        raise TypeError(f'Expected dict, got {type(shortcuts_group)}')
    for y in shortcuts_group.values():
        check_shortcut_formatting(y)


def check_shortcut_formatting(shortcut):
    if not isinstance(shortcut, dict):
        raise TypeError(f'Expected dict, got {type(shortcut)}')
    g = {'letter', 'shift', 'ctrl', 'alt'}
    for x in g:
        if x not in shortcut.keys():
            raise ValueError
    for x, y in zip(shortcut.keys(), shortcut.values()):
        check_shortcut_element_formatting(x, y)
    return True


def check_shortcut_element_formatting(element_name, element):
    if element_name == 'letter':
        if not isinstance(element, str):
            raise TypeError
        if len(element) != 1:
            raise ValueError
        if element not in string.ascii_uppercase:
            if element in string.ascii_lowercase:
                element = element.upper()
            else:
                raise ValueError
    elif element_name in {'shift', 'alt', 'ctrl'}:
        if not isinstance(element, bool):
            raise TypeError
    elif element_name == 'sens':
        if not isinstance(element, float):
            raise TypeError

    if not isinstance(element, str)\
            and not isinstance(element, bool)\
            and not isinstance(element, int)\
            and not isinstance(element, float):
        raise TypeError

# }}}


def filter_shortcuts_group_by_str(  # {{{
        shortcuts: dict, s: str) -> dict:
    """Filters shortcuts in a shortcuts group by name.

    Returns new shortcuts group.
    """
    result = {}
    for x, z in zip(
            shortcuts.keys(),
            shortcuts.values()):
        if s in x:
            result.update({x: z})
    return result


def search_modal_operators_shortcuts(
        shortcuts: dict, shortcut_name: str) -> dict:
    """Filters shortcuts groups dict by shortcut name.

    Returns new shortcuts groups dict.
    """
    if not isinstance(shortcut_name, str):
        raise TypeError

    result = {}
    for x, y in zip(shortcuts.keys(), shortcuts.values()):
        f = filter_shortcuts_group_by_str(y, shortcut_name)
        if len(f) > 0:
            result.update({x: f})
    check_shortcuts_formatting(result)
    return result

# }}}
# }}}


class BMTOOLS_OT_start_editing_modal_shortcut(bpy.types.Operator):  # {{{
    bl_idname = "bmtools.start_editing_modal_shortcut"
    bl_label = "Start editing bmtool modal operator kbs."
    bl_description = "Start editing modal shortcut"

    # Shortcut name and group {{{
    bmtool_operator_shortcut_name: StringProperty(
            name="Shortcut to be edited",
            default=""
            )

    bmtool_operator_shortcut_group: StringProperty(
            name="Group to be edited",
            default=""
            )
    # }}}

    def execute(self, context):
        prefs = context.preferences.addons['bmtools'].preferences

        # Deselect
        if prefs.bmtool_editing_modal_shortcut_name\
                == self.bmtool_operator_shortcut_name\
                and prefs.bmtool_editing_modal_shortcut_group\
                == self.bmtool_operator_shortcut_group:
            prefs.bmtool_editing_modal_shortcut_name = ""
            prefs.bmtool_editing_modal_shortcut_group = ""

        # Select
        else:
            prefs.bmtool_editing_modal_shortcut_name\
                = self.bmtool_operator_shortcut_name
            prefs.bmtool_editing_modal_shortcut_group\
                = self.bmtool_operator_shortcut_group

        return {'FINISHED'}
# }}}


class BMTOOLS_OT_add_or_update_modal_shortcut(bpy.types.Operator):  # {{{
    bl_label = "Add or change bmtool modal operator kbs."
    bl_idname = "bmtools.add_or_update_modal_shortcut"
    bl_description = "Add or update modal shortcut"

    # Shortcut name and group {{{
    bmtool_operator_shortcut_name: StringProperty(
            name="Shortcut to be edited",
            default=""
            )

    bmtool_operator_shortcut_group: StringProperty(
            name="Group to be edited",
            default=""
            )
    # }}}

    # Shortcut attrs {{{
    bmtool_operator_shortcut_letter: StringProperty(
            name="Shortcut mapping",
            maxlen=1,
            default="",
            )

    bmtool_operator_shortcut_shift: BoolProperty(
            name="Shortcut require shift to be pressed",
            default=False
            )

    bmtool_operator_shortcut_ctrl: BoolProperty(
            name="Shortcut require ctrl to be pressed",
            default=False
            )

    bmtool_operator_shortcut_alt: BoolProperty(
            name="Shortcut require alt to be pressed",
            default=False
            )

    bmtool_operator_shortcut_sens: FloatProperty(
            name="Sens",
            default=0.0
            )
    # }}}

    def execute(self, context):
        prefs = context.preferences.addons['bmtools'].preferences
        shortcut = {'letter': self.bmtool_operator_shortcut_letter,
                    'shift': self.bmtool_operator_shortcut_shift,
                    'ctrl': self.bmtool_operator_shortcut_ctrl,
                    'alt': self.bmtool_operator_shortcut_alt,
                    'sens': self.bmtool_operator_shortcut_sens,
                    }

        if not check_shortcut_formatting(shortcut):
            return {'CANCELLED'}
        kbs = deserialize_kbs(
                prefs.bmtool_modal_operators_serialized_shortcuts)

        if self.bmtool_operator_shortcut_group not in kbs:
            kbs.update({self.bmtool_operator_shortcut_group: {}})

        kbs[self.bmtool_operator_shortcut_group].update(
                {self.bmtool_operator_shortcut_name: shortcut})

        prefs.bmtool_modal_operators_serialized_shortcuts = serialize_kbs(kbs)
        prefs.refresh_modal_opertors_shortcuts_cache()

        prefs.bmtool_editing_modal_shortcut_name = ""
        prefs.bmtool_editing_modal_shortcut_group = ""
        return {'FINISHED'}
# }}}
