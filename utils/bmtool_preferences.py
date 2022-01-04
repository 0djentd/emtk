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

import re
import json

from bpy.props import BoolProperty, IntProperty, FloatProperty, StringProperty
from bpy.types import AddonPreferences


class BMToolPreferences(AddonPreferences):
    bl_idname = "bmtools"

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
    """
    bmtool_modal_operators_serialized_shortcuts: StringProperty(
            name='Modal operators serialized shortcuts.'
            default=""
            )

    # Currently edited shortcut props {{{
    """
    This props used to create fields in ui.
    """
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

    bmtool_shortcut_sens_int: IntProperty(
            name="Sens",
            hard_min=0,
            default=0
            )

    bmtool_shortcut_sens_float: FloatProperty(
            name="Sens",
            hard_min=0.0,
            default=0.0
            )
    # }}}

    # This is search field
    bmtool_prop_search_str: StringProperty(
            name="Search through bmtool modal props",
            default=""
            )
    # }}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__need_modal_operators_shortcuts_cache_refresh = True
        self.__modal_operator_shortcuts_cache = None
        self.__strict_checks = True

    def draw(self, context):
        layout = self.layout
        layout.label(text="BMTool options")
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

        if self.__selected_shortcut:
            layout.prop(self, "bmtool_shortcut_letter")
            layout.prop(self, "bmtool_shortcut_shift")
            layout.prop(self, "bmtool_shortcut_ctrl")
            layout.prop(self, "bmtool_shortcut_alt")
            layout.prop(self, "bmtool_shortcut_sens_int")
            layout.prop(self, "bmtool_shortcut_sent_float")
            layout.operator("bmtools.add_or_update_modal_shortcut")

        # keyboard shortcuts viewer {{{
        layout.prop(self, "bmtool_prop_search_str")

        s = []
        s.append(str(self.bmtool_prop_search_str))
        s.append(re.sub('_', ' ', s[0]))
        s.append(s[0].upper())
        s.append(s[0].lower())
        s.append(s[1].upper())
        s.append(s[1].lower())
        s.append(s[1].title())

        # element example: ['a', 'a_shift', 'a_ctl', 'a_alt']
        props_to_display = []

        # TODO: not implemented.
        if len(self.bmtool_prop_search_str) > 1:
            props_groups_filtered = search_modal_operators_shortcuts(
                    self.__modal_operator_shortcuts_cache, self.bmtool_prop_search_str)
            for x in props_groups_filtered:
                for y in props_groups_filtered[x]:
                    p = props_groups_filtered[x][y]
                    t = f"{x}: {y}: ["
                    for i, z in enumerate(p):
                        # z is name of element
                        # val is its value
                        val = p[z]
                        t = t + f"{z}={val}"
                        if i < (len(p) - 1):
                            t = t + ', '
                    t = t + "]"
                    layout.label(text=t)
        else:
            layout.label(
                    text="Type modifier property name above to view modal shortcuts.")
            layout.label(text="Example: bevel angle")
        # }}}

    # Modal operators shortcuts cache {{{
    def __refresh_modal_opertors_shortcuts_cache(self):
        if not self.__need_modal_operators_shortcuts_cache_refresh:
            return
        self.__modal_operator_shortcuts_cache\
                = deserialize_kbs(self.bmtool_modal_operators_serialized_shortcuts)

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

    def add_modal_operators_shortcut(self, group_name: str, shortcut: dict) -> bool:
        """Add new modal operators shortcut."""

        self.check_shortcut_element_formatting(shortcut)
        self.add_modal_operators_shortcuts_group(group_name)
        self.__modal_operator_shortcuts_cache[group_name].update(shortcut)

    def save_modal_operators_shortcuts_cache(self):
        """Saves modal operators shortcuts cache to prop."""

        s = serialize_kbs(self.__modal_operator_shortcuts_cache)
        self.bmtool_modal_operators_serialized_shortcuts = s
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
    for x in shortcuts:
        if not isinstance(shortcuts[x], dict):
            raise TypeError
        for y in shortcuts[x]:
            if not isinstance(shortcuts[x][y], str)\
                    and not isinstance(shortcuts[x][y], bool)\
                    and not isinstance(shortcuts[x][y], int)\
                    and not isinstance(shortcuts[x][y], float):
                raise TypeError

    kbs = json.dumps(shortcuts)

    if not isinstance(kbs, str):
        raise TypeError
    if deserialize_kbs(kbs) != shortcuts:
        raise ValueError
    return kbs
# }}}


def check_shortcuts_formatting(shortcuts: dict) -> bool:  # {{{
    if not isinstance(shortcuts, dict):
        raise TypeError
    for x in shortcuts:
        check_shortcuts_group_formatting(shortcuts[x])


def check_shortcuts_group_formatting(shortcuts_group: dict) -> bool:
    if not isinstance(shortcuts_group, dict):
        raise TypeError
    for y in shortcuts_group:
        check_shortcut_element_formatting(shortcuts_group[y])


def check_shortcut_formatting(shortcut):
    if not isinstance(shortcut, dict):
        raise TypeError
    g = {'letter', 'shift', 'ctrl', 'alt'}
    for x in g:
        if x not in shortcut:
            raise ValueError
    for y in shortcut:
        if not isinstance(shortcut[y], str)\
                and not isinstance(shortcut[y], bool)\
                and not isinstance(shortcut[y], int)\
                and not isinstance(shortcut[y], float):
            raise TypeError
# }}}


def filter_kbs_by_str(shortcuts: dict, s: str) -> dict:
    result = {}
    for x in shortcuts:
        if s in x:
            result.update({x: shortcuts[x]})
    return result
# }}}

# Operators {{{
class BMTOOLS_OT_start_editing_modal_shortcut(bpy.types.Operator):
    bl_idname = "bmtools.start_editing_modal_shortcut"
    bl_description = "Start editing modal shortcut"

    bmtool_operator_shortcut_group: StringProperty(
            name="Shortcut group",
            default="",
            )

    bmtool_operator_shortcut_name: StringProperty(
            name="Shortcut name",
            default="",
            )

    @classmethod
    def poll(self, context):
        if len(self.bmtool_operator_shortcut_name) == 0\
                or len(self.bmtool_operator_shortcut_group) == 0:
            return False
        return True

    def execute(self, context):
        prefs = context.preferences.addons['bmtools'].preferences

        prefs.bmtool_editing_modal_shortcut_name = self.bmtool_operator_shortcut_name
        prefs.bmtool_editing_modal_shortcut_group = self.bmtool_operator_shortcut_group

        self.bmtool_operator_shortcut_name = ""
        self.bmtool_operator_shortcut_group = ""
        return {'FINISHED'}

class BMTOOLS_OT_add_or_update_modal_shortcut(bpy.types.Operator):
    bl_idname = "bmtools.add_or_update_modal_shortcut"
    bl_description = "Add or update modal shortcut"
    bmtool_operator_shortcut_name: StringProperty(
            name="Shortcut name",
            default="",
            )

   
    bmtool_operator_shortcut_group: StringProperty(
            name="Shortcut group",
            default="",
            )

    # Dict  {{{
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
            hard_min=0.0,
            default=0.0
            )
    # }}}

    def execute(self, context):
        prefs = context.preferences.addons['bmtools'].preferences
        shortcut = {'name': self.bmtool_operator_shortcut_name,
                    'shift': self.bmtool_operator_shortcut_shift,
                    'ctrl': self.bmtool_operator_shortcut_ctrl,
                    'alt': self.bmtool_operator_shortcut_alt,
                    'sens': self.bmtool_operator_shortcut_sens,
                    }

        if not check_shortcut_elements(shortcut):
            return {'CANCELLED'}
        kbs = deserialize_kbs(prefs.bmtool_modal_operators_serialized_shortcuts)
        prefs.bmtool_editing_shortcut = True
        return {'FINISHED'}
# }}}
