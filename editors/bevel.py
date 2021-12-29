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

from ..classes.bmtool_editor import ModifierEditor
import bpy
import math


# Bevel modifier editor
class BMToolEditorBevel(ModifierEditor):
    _MODIFIER_EDITOR_NAME = 'Bevel Editor'
    _DEFAULT_M_NAME = 'Bevel'
    _DEFAULT_M_TYPE = 'BEVEL'
    _MODIFIER_CREATEABLE = True

    bmtool_mode = "Select mode"

    """
    Type example:
    EDITOR_TYPE = ['BEVEL_CLUSTER', 'BEVEL', 'BEVELED_BOOLEAN']

    Modifiers mapping example:
    MODIFIER_MAPPING = {'BEVEL_CLUSTER': 'get_first()',
                        'BEVEL': None,  # this means obj itself is modifier
                        'BEVELED_BOOLEAN': 'get_next_by_type('BEVEL')}

    Attributes example:
    [{'attr': 'segments',
      'mods': [<MODIFIER_MAPPING>, <MODIFIER_MAPPING>]
      'type': 'uint',
      'sens': 0.00005},
     {'attr': 'angle',
      'mods': [<MODIFIER_MAPPING>]
      'type': 'uint',
      'sens': 0.0005}]
    """

    # TODO: Remove this
    def bevel_segment_count(self, m_list):
        y = 0
        for x in m_list.get_list():
            if x.type == 'BEVEL':
                y += x.get_by_index(0).segments
        return y

    def bmtool_editor_modal_2(
        """Editor-specific modal method"""
            self, context, event, m_list, selected_objects):
        mod = m_list.active_modifier_get().get_by_index(0)
        if event.type == 'MOUSEMOVE':

            # Modal editing
            if self.bmtool_mode == "width":
                mod.width = self.delta_d(context, event) * 0.000008
            elif self.bmtool_mode == "segments":
                mod.segments = self.delta_d(context, event) * 0.00005
            elif self.bmtool_mode == "profile":
                mod.profile = self.delta_d(context, event) * 0.00001
            elif self.bmtool_mode == "angle":
                mod.angle_limit = math.radians(
                        self.delta_d(context, event) * 0.0001)

        # Modal editing modes switcher
        elif (event.type == 'W') & (event.value == 'PRESS'):
            self.bmtool_mode = "width"
        elif (event.type == 'S') & (event.value == 'PRESS'):
            self.bmtool_mode = "segments"
        elif (event.type == 'D') & (event.value == 'PRESS'):
            self.bmtool_mode = "profile"
        elif (event.type == 'A') & (event.value == 'PRESS'):
            self.bmtool_mode = "angle"

        # Modifier-specific actions
        elif (event.type == 'H') & (event.value == 'PRESS'):
            mod.harden_normals = not mod.harden_normals
        elif (event.type == 'C') & (event.value == 'PRESS'):
            mod.use_clamp_overlap = not mod.use_clamp_overlap
        elif (event.type == 'G') & (event.value == 'PRESS'):
            self.bmtool_modifier_defaults(context)
        elif (event.type == 'F') & (event.value == 'PRESS'):
            bpy.ops.object.shade_smooth()
            bpy.context.object.data.use_auto_smooth = True

    # --------------------------------
    # Editor default modifier settings
    # --------------------------------
    def bmtool_editor_modifier_defaults(
            self, context, m_list, selected_objects):
        mod = m_list.active_modifier_get().get_by_index(0)
        mod.affect = 'EDGES'
        # 'VERTICES', 'EDGES'

        mod.miter_outer = 'MITER_ARC'
        # 'MITER_SHARP', 'MITER_PATCH', 'MITER_ARC'

        mod.miter_inner = 'MITER_SHARP'
        # 'MITER_SHARP', 'MITER_ARC'

        mod.limit_method = 'ANGLE'
        # 'NONE', 'ANGLE', 'WEIGHT', 'VGROUP'

        mod.width = 0.01
        mod.segments = 3
        mod.profile = 0.5
        mod.use_clamp_overlap = 1

        bpy.ops.object.shade_smooth()
        context.object.data.use_auto_smooth = True

    # ------------------------------
    # Editor info about current modifier
    # ------------------------------
    def bmtool_editor_modifier_stats(self, context, m_list, selected_objects):
        mod = m_list.active_modifier_get().get_by_index(0)
        ui_t = []
        ui_t.append("MBTool Bevel")
        ui_t.append(f"Total seg. count {self.bevel_segment_count(m_list)}")
        ui_t.append(f"Mode = {self.bmtool_mode}")
        ui_t.append(" ")
        ui_t.append(f"---{mod.type}---")
        ui_t.append(f"(S)egments {mod.segments}")
        ui_t.append(f"(W)idth {round(mod.width, 3)}")
        ui_t.append(f"(A)ngle {round(mod.angle_limit, 1)}")
        return ui_t
