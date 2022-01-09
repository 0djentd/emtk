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

from bpy.types import Operator
from ..classes.modal_clusters_operator import ModalClustersOperator
from ..ui.bmtool_ui import BMToolUi


# Tool for viewing and general editing of
# all modifiers of an object
class BMTOOL_OT_bmtoolm_2(BMToolUi, ModalClustersOperator, Operator):
    bl_idname = "object.bmtoolm_2"
    bl_label = "View objects modifiers"
    bl_description = "View modifiers on selected object"

    def bmtool_ui_modifier_stats(self, context):
        ui_t = []
        ui_t.append(" BMToolM lite ")
        return ui_t
