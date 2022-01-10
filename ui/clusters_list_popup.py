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
import math

import bpy

from bpy.props import BoolProperty, IntProperty, FloatProperty, StringProperty
from bpy.types import Operator

from ..lib.modifiers_operator import ModifiersOperator
from ..lib.utils.modifier_prop_types import get_all_editable_props

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
        layout.label(text='EMTK')
        box = layout.box()
        # self.__draw_clusters_list(box, self.m_list)
        for x in self.m_list.get_list():
            cluster_box = box.box()
            self.__draw_cluster(cluster_box, x)

    def __draw_clusters_list(self, layout, clusters_list):
        for x in clusters_list.get_list():
            self.__draw_cluster(layout, x)

    def __draw_modifiers_list(self, layout, modifiers_list):
        for x in modifiers_list.get_list():
            self.__draw_modifier(layout, x)

    def __draw_cluster(self, layout, cluster):

        row = layout.row()

        # Cluster collapsed
        val = not cluster.collapsed
        line = f'self.m_list.find_cluster_by_name(\'{cluster.name}\').\
                collapsed = {val}'
        line = re.sub('self', self.get_class_line(), line)
        if not cluster.collapsed:
            icon = 'DOWNARROW_HLT'
        else:
            icon = 'RIGHTARROW'
        op = row.operator('bmtools.bmtool_invoke_operator_func',
                          text=cluster.name, icon=icon)
        op.func = line

        # Actions {{{
        # Move down
        line = f'self.m_list.get_cluster_or_layer(self.m_list.find_cluster_by_name("{cluster.name}")).\
                move_down("{cluster.name}")'
        line = re.sub('self', self.get_class_line(), line)
        col = row.column()
        op = col.operator('bmtools.bmtool_invoke_operator_func',
                          text='', icon='TRIA_DOWN')
        op.func = line

        # Move up
        line = f'self.m_list.get_cluster_or_layer(self.m_list.find_cluster_by_name("{cluster.name}")).\
                move_up("{cluster.name}")'
        line = re.sub('self', self.get_class_line(), line)
        col = row.column()
        op = col.operator('bmtools.bmtool_invoke_operator_func',
                          text='', icon='TRIA_UP')
        op.func = line

        # Remove
        line = f'self.m_list.get_cluster_or_layer(self.m_list.find_cluster_by_name("{cluster.name}")).\
                remove("{cluster.name}")'
        line = re.sub('self', self.get_class_line(), line)
        col = row.column()
        op = col.operator('bmtools.bmtool_invoke_operator_func',
                          text='', icon='X')
        op.func = line

        # Duplicate
        line = f'self.m_list.get_cluster_or_layer(self.m_list.find_cluster_by_name("{cluster.name}")).\
                duplicate("{cluster.name}")'
        line = re.sub('self', self.get_class_line(), line)
        col = row.column()
        op = col.operator('bmtools.bmtool_invoke_operator_func',
                          text='', icon='DUPLICATE')
        op.func = line

        # Deconstruct
        line = f'self.m_list.get_cluster_or_layer(self.m_list.find_cluster_by_name("{cluster.name}")).\
                deconstruct("{cluster.name}")'
        line = re.sub('self', self.get_class_line(), line)
        col = row.column()
        op = col.operator('bmtools.bmtool_invoke_operator_func',
                          text='', icon='MOD_DECIM')
        op.func = line
        # }}}

        if not cluster.collapsed:
            box = layout.box()

            # Cluster definition collapsed {{{
            val = not cluster.show_definition_expanded
            line = f'self.m_list.find_cluster_by_name(\'{cluster.name}\').\
                    show_definition_expanded = {val}'
            line = re.sub('self', self.get_class_line(), line)
            if cluster.show_definition_expanded:
                icon = 'DOWNARROW_HLT'
            else:
                icon = 'RIGHTARROW'
            op = box.operator('bmtools.bmtool_invoke_operator_func',
                              text='Definition', icon=icon)
            op.func = line

            if cluster.show_definition_expanded:
                box_2 = box.box()
                for x, y in zip(cluster._cluster_definition,
                                cluster._cluster_definition.values()):
                    box_2.label(text=f"{x}: {y}")
            # }}}

            # Cluster props collapsed {{{
            val = not cluster.show_props_expanded
            line = f'self.m_list.find_cluster_by_name(\'{cluster.name}\').\
                    show_props_expanded = {val}'
            line = re.sub('self', self.get_class_line(), line)
            if cluster.show_props_expanded:
                icon = 'DOWNARROW_HLT'
            else:
                icon = 'RIGHTARROW'
            op = box.operator('bmtools.bmtool_invoke_operator_func',
                              text='Properties', icon=icon)
            op.func = line
            if cluster.show_props_expanded:
                box_2 = box.box()
                for x, y in zip(cluster._cluster_props,
                                cluster._cluster_props.values()):
                    box_2.label(text=f"{x}: {y}")
            # }}}

            if cluster.has_clusters():
                self.__draw_clusters_list(layout, cluster)
            else:
                self.__draw_modifiers_list(layout, cluster)

    def __draw_modifier(self, layout, modifier):
        if modifier.show_expanded:
            icon = 'DOWNARROW_HLT'
        else:
            icon = 'RIGHTARROW'

        # Modifier collapsed {{{
        val = not modifier.show_expanded
        line = f'self.m_list.find_modifier_by_name(\'{modifier.name}\').\
                show_expanded = {val}'
        line = re.sub('self', self.get_class_line(), line)
        if modifier.show_expanded:
            icon = 'DOWNARROW_HLT'
        else:
            icon = 'RIGHTARROW'
        op = layout.operator('bmtools.bmtool_invoke_operator_func',
                             text=modifier.name + ' modifier', icon=icon)
        op.func = line

        if modifier.show_expanded:
            box = layout.box()
            p = get_all_editable_props(modifier)
            for i, y in enumerate(p):
                if math.remainder(i, 2) == 0:
                    row = box.row()
                col = row.column()
                col.prop(modifier, y)
        # }}}

    @classmethod
    def get_class_line(cls):
        if bpy.types.Panel not in cls.mro()\
                and bpy.types.Operator not in cls.mro():
            raise TypeError
        return f'bpy.types.{cls.__name__}'

    def invoke(self, context, event):
        print('Operator invoked')
        context.window_manager.invoke_popup(self, width=350)
        return {'RUNNING_MODAL'}
