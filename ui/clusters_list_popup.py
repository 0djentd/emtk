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

import logging
import string
import re

import bpy

from bpy.props import BoolProperty, IntProperty, FloatProperty, StringProperty
from bpy.types import Operator

from ..lib.modifiers_operator import ModifiersOperator

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BMTOOLS_OT_clusters_list_popup(ModifiersOperator, Operator):
    bl_idname = "bmtools.clusters_list_popup"
    bl_label = "View and edit active object's clusters."

    def __init__(self):
        type(self).create_objects_modifiers_lists(type(self))
        print('Operator initialized')

    def __del__(self):
        self.m_list.save_clusters_state()
        del(self.m_list)
        print('Operator removed')

    @classmethod
    def poll(cls, context):
        print('Operator polled')
        if context.area.type != 'VIEW_3D':
            return False
        elif context.mode != 'OBJECT':
            return False
        elif len(context.selected_objects) != 1:
            return False
        elif context.object.type != 'MESH':
            return False
        else:
            return True

    def execute(self, context):
        raise TypeError
        print('Operator method')
        return {'FINISHED'}

    def modal(self, context, event):
        raise TypeError
        print('Operator modal')
        return {'INTERFACE', 'PASS_THROUGH'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        # self.__draw_clusters_list(box, self.m_list)
        for x in self.m_list.get_list():
            cluster_box = box.box()
            cluster_box.label(text=x.name)
            self.__draw_cluster(cluster_box, x)
            # op = cluster_box.operator('bmtools.bmtool_invoke_operator_func')
            # op.func = str(f'bpy.types.BMTOOLS_OT_clusters_list_popup.m_list.remove("{x.name}")')
        layout.label(text='EMTK')

    def __draw_clusters_list(self, layout, clusters_list):
        for x in clusters_list.get_list():
            self.__draw_cluster(layout, x)

    def __draw_modifiers_list(self, layout, modifiers_list):
        for x in modifiers_list.get_list():
            self.__draw_modifier(layout, x)

    def __draw_cluster(self, layout, cluster):
        line_2 = str(not cluster.collapsed)
        line = f'self.m_list.find_cluster_by_name(\'{cluster.name}\').collapsed = {line_2}'
        op = self.panel_operator(layout, line, text=cluster.name)
        if not cluster.collapsed:
            for x, y in zip(cluster._cluster_definition,
                            cluster._cluster_definition.values()):
                layout.label(text=f'{x}: {y}')
            for x in cluster.get_list():
                self.__draw_cluster(layout, x)
            if cluster.has_clusters():
                self.__draw_clusters_list(layout, cluster)
            else:
                self.__draw_modifiers_list(layout, cluster)

    def __draw_modifier(self, layout, modifier):
        layout.label(text=f'Modifier {modifier.name}')

    @classmethod
    def get_class_line(cls):
        if bpy.types.Panel not in cls.mro()\
                and bpy.types.Operator not in cls.mro():
            raise TypeError
        return f'bpy.types.{cls.__name__}'

    @classmethod
    def panel_operator(cls, layout, line, line_2=None, text=None):
        if type(line) is not str:
            raise TypeError
        if type(line_2) is not str and line_2 is not None:
            raise TypeError
        if text is not None:
            op = layout.operator('bmtools.bmtool_invoke_operator_func',
                                 text=text)
        else:
            op = layout.operator('bmtools.bmtool_invoke_operator_func')
        op.func = re.sub('self', cls.get_class_line(), line, count=1)
        if line_2 is not None:
            op.returned_variable = re.sub(
                'self', cls.get_class_line(), line_2, count=1)
        print(op.func)
        return op

    def invoke(self, context, event):
        print('Operator invoked')
        context.window_manager.invoke_popup(self)
        return {'RUNNING_MODAL'}
