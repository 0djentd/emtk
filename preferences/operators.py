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

from ..lib.utils.modifier_prop_types import get_all_editable_props
from ..lib.utils.modifier_prop_types import get_props_filtered_by_types
from ..lib.utils.modifier_prop_types import MODIFIER_TYPES

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

    # bmtool_operator_shortcut_name
    # bmtool_operator_shortcut_group
    # bmtool_operator_shortcut_letter
    # bmtool_operator_shortcut_shift
    # bmtool_operator_shortcut_ctrl
    # bmtool_operator_shortcut_alt
    # bmtool_operator_shortcut_sens

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


class BMTOOL_OT_reparse_default_modifiers_props_kbs(  # {{{
        bpy.types.Operator):
    bl_idname = "object.reparse_default_modifiers_props_kbs"
    bl_label = "BMTool add all modifiers props to kbs"

    replace_kbs: BoolProperty(False)

    @classmethod
    def poll(self, context):
        if context.area.type != 'VIEW_3D':
            return False
        elif context.mode != 'OBJECT':
            return False
        elif len(context.selected_objects) != 1:
            return False
        elif context.object.type != 'MESH':
            return False
        return True

    def execute(self, context):
        modifiers = []
        for x in MODIFIER_TYPES:
            mod = bpy.context.object.modifiers.new(x.lower(), x)
            if mod is not None:
                mod.show_viewport = False
                modifiers.append(mod)

        prefs = bpy.context.preferences.addons['bmtools'].preferences

        s = {}
        for x in modifiers:
            props = get_all_editable_props(x, no_ignore=True)

            if self.replace_kbs:
                d = {x.type: {}}
            else:
                d = prefs.get_modal_operators_shortcuts_group(x.type)
                d = {x.type: d}

            for y in props:
                shortcut = generate_new_shortcut(y, d)
                d[x.type].update(shortcut)

            s.update(d)

        if self.replace_kbs:
            prefs.bmtool_modal_operators_serialized_shortcuts\
                    = serialize_kbs(s)
        else:
            i = 0
            for x, y in zip(s.keys(), s.values()):
                for z, e in zip(y.keys(), y.values()):
                    shortcut = {z: e}
                    prefs.add_modal_operators_shortcut(x, shortcut)
                    i += 1
            prefs.save_modal_operators_shortcuts_cache()
        return {'FINISHED'}
# }}}
