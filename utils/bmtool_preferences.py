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

from bpy.props import BoolProperty, IntProperty, FloatProperty, StringProperty
from bpy.types import AddonPreferences


class BMToolPreferences(AddonPreferences):
    bl_idname = "bmtools"

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

    def draw(self, context):
        layout = self.layout
        layout.label(text="BMTool options")
        layout.prop(self, "save_clusters")
        layout.prop(self, "save_clusters_backup")
        layout.prop(self, "backup_mesh_on_modifier_apply_remove")
        if self.backup_mesh_on_modifier_apply_remove:
            layout.prop(self, "backup_collection_name")
