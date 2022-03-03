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

# TODO: Not implemented


class VIEW3D_MT_PIE_cluster_types(Menu):
    bl_label = "Cluster types editing"
    bl_idname = "BMTOOLS_MT_PIE_cluster_types"

    def draw(self, context):
        layout = self.layout()
        pie = layout.menu_pie()

        op = pie.operator("emtk.edit_cluster_types",
                          text="Edit cluster types")
        op.obj = 'SETTINGS'

        op = pie.operator("emtk.edit_cluster_types",
                          text="Edit scene cluster types")
        op.obj = 'SCENE'

        op = pie.operator("emtk.edit_cluster_types",
                          text="Edit object cluster types")
        op.obj = 'OBJECT'
