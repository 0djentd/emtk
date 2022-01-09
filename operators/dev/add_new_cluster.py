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
from bpy.props import FloatProperty, StringProperty

from ...lib.modifiers_operator import ModifiersOperator


class BMTOOL_OT_add_new_cluster(ModifiersOperator, Operator):
    bl_idname = "bmtools.add_new_cluster"
    bl_label = "Add new cluster"

    cluster_type: StringProperty(name="Cluster Type", default='')
    cluster_number: FloatProperty(name="Number of clusters", default=1.0)

    """
    So, basically, when invoke_props_dialog is called and invoke returns
    'RUNNING_MODAL', it throws segfault, if popup is closed. 'PASS_THROUGH'
    in modal doesnt helps too.

    But practically modal can be replaced with draw,
    as it is invoked just as often anyways.

    Probably best idea is to use draw method, expecially considering
    that operators have init and del methods.
    Actually, operator properties dialog works much better
    clusters than panels.
    """

    def __init__(self):
        self.x = 0
        self.create_objects_modifiers_lists()
        print('Operator initialized')

    def __del__(self):
        print('Operator removed')

    @classmethod
    def poll(cls, context):
        print('Operator polled')
        if context.area.type != 'VIEW_3D':
            return False
        elif context.mode != 'OBJECT':
            return False
        elif len(context.selected_objects) == 0:
            return False
        elif context.object.type != 'MESH':
            return False
        else:
            return True

    def execute(self, context):
        print('Operator method')
        if self.cluster_number == 1:
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

    def modal(self, context, event):
        if self.x > 1000:
            raise ValueError
        self.x += 1
        print('Operator modal')
        return {'PASS_THROUGH'}

    def draw(self, context):
        print('Operator draw')
        if self.cluster_number > 2:
            self.cluster_type = "sdfgsdfgsdfg"
        layout = self.layout
        layout.prop(self, "cluster_type")
        layout.prop(self, "cluster_number")

    def cancell(self, context):
        print('Operator cancelled')

    def invoke(self, context, event):
        print('Operator invoked')
        context.window_manager.invoke_props_dialog(self)
        return {'RUNNING_MODAL'}
