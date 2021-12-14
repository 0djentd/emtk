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
from bpy.types import Operator
from bpy.props import (
    IntProperty,
    FloatProperty
)

from ...classes.bmtool_operator import BMToolMod
from ...ui.bmtool_ui import BMToolUi


# ------------------------
# BMTool operator template
# ------------------------
class BMTBevel_2(BMToolUi, BMToolMod, Operator):
    # Used in ui
    bl_idname = "object.bmt_bevel_2"
    bl_label = "Add/change bevel_2"
    bl_description = "Add or edit bevel modifiers on selected object 2"

    # Modifier name used for modifier name in ui
    m_name = 'Bevel'
    # Used when adding new modifier
    m_type = 'BEVEL'

    # Operator properties
    width: FloatProperty()
    segments: IntProperty()

    # ------------------------------
    # Modifier-specific modal method
    # ------------------------------
    def bmtool_modal_2(self, context, event):
        if event.type == 'MOUSEMOVE':
            # Vector length for changing modifier settings
            delta_d = self.vec_len(context,
                                   self.first_x, event.mouse_x,
                                   self.first_y, event.mouse_y
                                   )

            self.report({'INFO'}, f"{event.mouse_x}, {event.mouse_y}")

            # Modal editing
            if self.bmtool_mode == "width":
                self.width = pow(delta_d, 2) * 0.000008
                self.mod.width = self.width
            elif self.bmtool_mode == "segments":
                self.segments = pow(delta_d, 2) * 0.00005
                self.mod.segments = self.segments

        # Modal editing modes switcher
        elif (event.type == 'W') & (event.value == 'PRESS'):
            self.bmtool_mode = "width"
        elif (event.type == 'S') & (event.value == 'PRESS'):
            self.bmtool_mode = "segments"

        # Modifier-specific actions
        elif (event.type == 'H') & (event.value == 'PRESS'):
            self.bmtool_modifier_remove(context, event)
        elif (event.type == 'C') & (event.value == 'PRESS'):
            self.mod.use_clamp_overlap = not self.mod.use_clamp_overlap

    # ------------------------------
    # Default settings
    # ------------------------------
    def bmtool_modifier_defaults(self, context):
        self.mod.width = 0.01
        self.mod.segments = 3
        self.mod.profile = 0.5
        self.mod.use_clamp_overlap = 1

        bpy.ops.object.shade_smooth()
        context.object.data.use_auto_smooth = True

    # ------------------------------
    # Info about current modifier
    # ------------------------------
    def bmtool_modifier_stats(self, context):
        modifprop_info = f"(S)egments {self.segments} "
        modifprop_info_2 = f"(W)idth {round(self.width, 3)} "
        modifprop_info_3 = " "
        return modifprop_info + modifprop_info_2 + modifprop_info_3
