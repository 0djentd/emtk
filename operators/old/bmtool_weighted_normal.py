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
from ...classes.bmtool_operator import BMToolMod
from ...ui.bmtool_ui import BMToolUi


# Weighted Normal modifier operator
class BMTWeightedNormal(BMToolUi, BMToolMod, Operator):
    bl_idname = "object.bmt_weightednormal"
    bl_label = "Add/change weighted normal"
    bl_description = "Add or edit weighted normal modifiers on selected object"

    # Modifier name used for modifier name
    _DEFAULT_M_NAME = 'Weighted Normal'
    # Used when adding new modifier
    _DEFAULT_M_TYPE = 'WEIGHTED_NORMAL'

    # Modifier name used for modifier name
    m_name = 'Weighted Normal'
    # Used when adding new modifier
    m_type = 'WEIGHTED_NORMAL'

    # ------------------------------
    # Modifier-specific modal method
    # ------------------------------
    def bmtool_weightednormal_modal(self, context, event):
        mod = self.m_list.active_modifier_get()
        if event.type == 'MOUSEMOVE':

            # Modal
            if self.bmtool_mode == "weight":
                mod.weight = self.delta_d(context, event) * 0.00005
            elif self.bmtool_mode == "thresh":
                mod.thresh = self.delta_d(context, event) * 0.00005

        # Modal editing modes switcher
        elif (event.type == 'W') & (event.value == 'PRESS'):
            self.bmtool_mode = "weight"
        elif (event.type == 'T') & (event.value == 'PRESS'):
            self.bmtool_mode = "thresh"

        # Modifier actions
        elif (event.type == 'S') & (event.value == 'PRESS'):
            mod.keep_sharp = not mod.keep_sharp
        elif (event.type == 'F') & (event.value == 'PRESS'):
            mod.use_face_influence = not mod.use_face_influence

    # ------------------------------
    # Default settings
    # ------------------------------
    def bmtool_weightednormal_modifier_defaults(self, context):
        bpy.ops.object.shade_smooth()
        self.keep_sharp = False
        self.use_face_influence = False
        context.object.data.use_auto_smooth = True

    # ------------------------------
    # Info about current modifier
    # ------------------------------
    def bmtool_weightednormal_modifier_stats(self, context):
        mod = self.m_list.active_modifier_get()
        ui_t = []
        ui_t.append(f"MBTool {self.m_name}")
        ui_t.append(f"Mode = {self.bmtool_mode}")
        ui_t.append(" ")
        ui_t.append(f"---{self.m_type}---")
        ui_t.append(f"(T)hreshold {round(mod.thresh, 3)}")
        ui_t.append(f"(W)eight {round(mod.weight, 3)}")
        ui_t.append(f"Keep (s)harp {mod.keep_sharp}")
        ui_t.append(f"Use (f)ace influence {mod.use_face_influence}")
        return ui_t

    # =============================
    # methods that are used when class used in bmtoolm
    # =============================

    # ------------------------------
    # Modifier-specific modal method
    # ------------------------------
    def bmtool_modal_2(self, context, event):
        return self.bmtool_weightednormal_modal(context, event)

    # ------------------------------
    # Default settings
    # ------------------------------
    def bmtool_modifier_defaults(self, context):
        return self.bmtool_weightednormal_modifier_defaults(context)

    # ------------------------------
    # Info about current modifier
    # ------------------------------
    def bmtool_ui_modifier_stats(self, context):
        return self.bmtool_weightednormal_modifier_stats(context)
