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

from bpy.props import BoolProperty, IntProperty, FloatProperty
from bpy.types import AddonPreferences


class BMToolPreferences(AddonPreferences):
    bl_idname = "bmtools"

    bmtool_additional_info: BoolProperty(
            name="Show additional info in modal operators",
            default=True
            )

    save_clusters: BoolProperty(
            name="Save clusters on operator finish",
            default=True
            )

    save_clusters_backup: BoolProperty(
            name="Save clusters backup on operator finish",
            default=True
            )

    def draw(self, context):
        layout = self.layout
        layout.label(text="BMTool options")
        layout.prop(self, "bmtool_additional_info")
        layout.prop(self, "save_clusters")
