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

from bpy.types import Menu


class VIEW3D_MT_PIE_emtk_pie_1(Menu):
    bl_label = "EMTK"
    bl_idname = "EMTK_MT_PIE_emtk_pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("object.emtkm", text="EMTKM", icon="CUBE")
        pie.operator("object.emtke2", text="Add modifier", icon="MOD_BEVEL")
        pie.operator("emtk.clusters_list_popup",
                     text="Clusters list", icon="CUBE")
