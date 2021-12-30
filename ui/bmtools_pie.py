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

from bpy.types import Menu


# Modifiers pie menu
class VIEW_3D_MT_PIE_bmtools_pie_1(Menu):
    bl_label = "BMTools"
    bl_idname = "BMTOOLS_MT_PIE_bmtpie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("object.bmtoolm_2", text="BMToolM lite", icon="CUBE")
        pie.operator("object.bmtoolm", text="BMToolM", icon="CUBE")
        pie.operator("object.bmtoole2", text="BMToolE2", icon="CUBE")
