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
    bmtool_modal_operator_shortcuts: StringProperty(
            name='BMTool modal operators shortcuts.'
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
            # all props
            for x in self.props_names:
                # props names from bmtool_prop_search_str
                for z in s:
                    if z in x:

                        # mapping element
                        names = [
                                 x,
                                 f'{x}_shift',
                                 f'{x}_alt',
                                 f'{x}_ctl'
                                 ]

                        # check duplicates in props
                        dont_add = False
                        for p in props_to_display:
                            if p == names:
                                dont_add = True

                        if not dont_add:
                            props_to_display.append(names)

            print(len(props_to_display))
            for x in props_to_display:
                kbs_name = re.sub('_', ' ', x[0])
                kbs_name = kbs_name.title()
                layout.label(text=kbs_name)
                for y in x:
                    layout.prop(self, y)

        else:
            layout.label(
                    text="Type modifier property name above to view modal shortcuts.")
            layout.label(text="Example: bevel angle")
        # }}}


def deserialize_kbs(kbs: str) -> dict:  # {{{
    """Deserialize string with shortcuts."""
    if not isinstance(kbs, str):
        raise TypeError

    shortcuts = json.loads(kbs)

    if not isinstance(shortcuts, dict):
        raise TypeError
    for x in shortcuts:
        if not isinstance(shortcuts[x], dict):
            raise TypeError
        for y in shortcuts[x]:
            if not isinstance(shortcuts[x][y], str)\
                    and not isinstance(shortcuts[x][y], bool)\
                    and not isinstance(shortcuts[x][y], int)\
                    and not isinstance(shortcuts[x][y], float):
                raise TypeError
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


def filter_kbs_by_str(shortcuts: dict, s: str) -> dict:
    result = {}
    for x in shortcuts:
        if s in x:
            result.update({x: shortcuts[x]})
    return result

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
        kbs = deserialize_kbs(prefs.bmtool_modal_operator_shortcuts)
        prefs.bmtool_editing_shortcut = True
        return {'FINISHED'}
