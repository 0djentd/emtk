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

from bpy.props import (
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       StringProperty
                       )

from ..lib.utils.modifier_prop_types import get_all_editable_props
# from ..lib.utils.modifier_prop_types import get_props_filtered_by_types
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
    shortcut_name: StringProperty(
            name="Shortcut to be edited",
            default=""
            )

    shortcut_group: StringProperty(
            name="Group to be edited",
            default=""
            )
    # }}}

    def execute(self, context):
        prefs = context.preferences.addons['bmtools'].preferences

        # Deselect
        if prefs.bmtool_editing_modal_shortcut_name\
                == self.shortcut_name\
                and prefs.bmtool_editing_modal_shortcut_group\
                == self.shortcut_group:
            prefs.bmtool_editing_modal_shortcut_name = ""
            prefs.bmtool_editing_modal_shortcut_group = ""

        # Select
        else:
            prefs.bmtool_editing_modal_shortcut_name\
                = self.shortcut_name
            prefs.bmtool_editing_modal_shortcut_group\
                = self.shortcut_group

            group = prefs.get_modal_operators_shortcuts_group(
                    self.shortcut_group)
            shortcut = group[self.shortcut_name]

            if 'sens' in shortcut:
                prefs.edited_shortcut_sens = shortcut['sens']
            prefs.edited_shortcut_letter = shortcut['letter']
            prefs.edited_shortcut_shift = shortcut['shift']
            prefs.edited_shortcut_ctrl = shortcut['ctrl']
            prefs.edited_shortcut_alt = shortcut['alt']

        return {'FINISHED'}
# }}}


class BMTOOLS_OT_add_or_update_modal_shortcut(bpy.types.Operator):  # {{{
    bl_label = "Add or change bmtool modal operator kbs."
    bl_idname = "bmtools.add_or_update_modal_shortcut"
    bl_description = "Add or update modal shortcut"

    # shortcut_name
    # shortcut_group
    # shortcut_letter
    # shortcut_shift
    # shortcut_ctrl
    # shortcut_alt
    # shortcut_sens

    # Shortcut name and group {{{
    shortcut_name: StringProperty(
            name="Shortcut to be edited",
            default=""
            )

    shortcut_group: StringProperty(
            name="Group to be edited",
            default=""
            )
    # }}}

    # Shortcut attrs {{{
    shortcut_letter: StringProperty(
            name="Shortcut mapping",
            maxlen=1,
            default="",
            )

    shortcut_shift: BoolProperty(
            name="Shortcut require shift to be pressed",
            default=False
            )

    shortcut_ctrl: BoolProperty(
            name="Shortcut require ctrl to be pressed",
            default=False
            )

    shortcut_alt: BoolProperty(
            name="Shortcut require alt to be pressed",
            default=False
            )

    shortcut_sens: FloatProperty(
            name="Sens",
            default=0.0
            )
    # }}}

    def execute(self, context):
        prefs = context.preferences.addons['bmtools'].preferences
        shortcut = {'letter': self.shortcut_letter,
                    'shift': self.shortcut_shift,
                    'ctrl': self.shortcut_ctrl,
                    'alt': self.shortcut_alt,
                    'sens': self.shortcut_sens,
                    }

        if not check_shortcut_formatting(shortcut):
            return {'CANCELLED'}
        kbs = deserialize_kbs(
                prefs.bmtool_modal_operators_serialized_shortcuts)

        if self.shortcut_group not in kbs:
            kbs.update({self.shortcut_group: {}})

        kbs[self.shortcut_group].update(
                {self.shortcut_name: shortcut})

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

    replace_kbs: BoolProperty(
            name='Replace existing.',
            default=True
            )

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

        replace = self.replace_kbs

        s = {}
        for x in modifiers:
            props = get_all_editable_props(x, no_ignore=True)

            if replace:
                d = {}
            else:
                d = prefs.get_modal_operators_shortcuts_group(x.type)

            for y in props:
                for z in d:
                    if not isinstance(d[z], dict):
                        raise TypeError
                    for h in d[z]:
                        if not isinstance(d[z][h], str)\
                                and not isinstance(d[z][h], bool):
                            raise TypeError(d[z])

                shortcut = generate_new_shortcut(y, d)
                d.update(shortcut)
                if len(d) < 1:
                    raise ValueError

            s_e = {x.type: d}
            s.update(s_e)

        if replace:
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
