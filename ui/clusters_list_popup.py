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
import cProfile

import bpy

from bpy.props import BoolProperty, IntProperty, FloatProperty, StringProperty
from bpy.types import Operator

from ..lib.modifiers_operator import ModifiersOperator
from ..lib.utils.modifier_prop_types import get_all_editable_props

from .ui_class_variables_editor import UIClassVariablesEditor

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

USE_PROFILER = False


class BMTOOLS_OT_clusters_list_popup(
        UIClassVariablesEditor, ModifiersOperator, Operator):
    bl_idname = "bmtools.clusters_list_popup"
    bl_label = "View and edit active object's clusters."

    def __init__(self):
        cls = type(self)
        cls.iteration = 0
        if USE_PROFILER:
            cProfile.runctx('cls.create_objects_modifiers_lists(cls)',
                            globals(), locals())
        else:
            cls.create_objects_modifiers_lists(cls)
        print('Operator initialized')

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
        print('Operator method')
        cls = type(self)
        cls.m_list.save_clusters_state()
        return {'FINISHED'}

    def cancel(self, context):
        cls = type(self)
        cls.m_list.save_clusters_state()
        print('Operator cancelled')

    def draw(self, context):
        cls = type(self)
        cls.iteration += 1
        layout = self.layout
        layout.label(text='EMTK')
        box = layout.box()

        if USE_PROFILER and cls.iteration in {1, 10, 100}:
            c = 'self._BMTOOLS_OT_clusters_list_popup__draw_clusters_list(box, cls.m_list)'
            print('Profiler stats for clusters list popup ')
            print(c)
            cProfile.runctx(c, globals(), locals())
        else:
            self._BMTOOLS_OT_clusters_list_popup__draw_clusters_list(
                    box, self.m_list)

    def __draw_clusters_list(self, layout, clusters_list):
        for x in clusters_list.get_list():
            cluster_box = layout.box()
            self.__draw_cluster(cluster_box, x)

    def __draw_modifiers_list(self, layout, modifiers_list):
        for x in modifiers_list.get_list():
            self.__draw_modifier(layout, x)

    def __draw_cluster(self, layout, cluster):  # {{{

        row = layout.row()

        # Cluster name {{{
        val = not cluster.variables['collapsed']
        line = f'self.m_list.find_cluster_by_name(\'{cluster.name}\').\
                variables[\'collapsed\'] = {val}'
        line = re.sub('self', self.get_class_line(), line)
        if not cluster.variables['collapsed']:
            icon = 'DOWNARROW_HLT'
        else:
            icon = 'RIGHTARROW'
        op = row.operator('bmtools.bmtool_invoke_operator_func',
                          text=cluster.name, icon=icon)
        op.func = line
        # }}}

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

        # Apply
        line = f'self.m_list.get_cluster_or_layer(self.m_list.find_cluster_by_name("{cluster.name}")).\
                apply("{cluster.name}")'
        line = re.sub('self', self.get_class_line(), line)
        col = row.column()
        op = col.operator('bmtools.bmtool_invoke_operator_func',
                          text='', icon='CHECKMARK')
        op.func = line

        # Visibility {{{
        v = {
             'show_viewport': None,
             'show_editmode': None,
             'show_on_cage': None,
             'show_render': None,
             }

        for i, x in enumerate(v):
            m = [0, 0, 0, 0]
            m[i] = 1
            line_2 = str(m)
            line = f'self.m_list.find_cluster_by_name("{cluster.name}").\
                    toggle_this_cluster_visibility({line_2})'
            line = re.sub('self', self.get_class_line(), line)
            val = cluster.get_this_cluster_visibility()[i]

            if val == 'ON':
                icon = 'CUBE'
            elif val == 'HALF':
                icon = 'CUBE'
            elif val == 'OFF':
                icon = 'X'
            else:
                raise ValueError

            col = row.column()
            op = col.operator('bmtools.bmtool_invoke_operator_func',
                              text='', icon=icon)
            op.func = line

        # }}}

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

        if not cluster.variables['collapsed']:
            row = layout.row()

            # Cluster definition {{{
            col = row.column()
            val = not cluster.variables['show_definition_expanded']
            line = f'self.m_list.find_cluster_by_name(\'{cluster.name}\').\
                    variables[\'show_definition_expanded\'] = {val}'
            line = re.sub('self', self.get_class_line(), line)
            if cluster.variables['show_definition_expanded']:
                icon = 'DOWNARROW_HLT'
            else:
                icon = 'RIGHTARROW'
            op = col.operator('bmtools.bmtool_invoke_operator_func',
                              text='Definition', icon=icon)
            op.func = line
            # }}}

            # Cluster props {{{
            col = row.column()
            val = not cluster.variables['show_props_expanded']
            line = f'self.m_list.find_cluster_by_name(\'{cluster.name}\').\
                    variables[\'show_props_expanded\'] = {val}'
            line = re.sub('self', self.get_class_line(), line)
            if cluster.variables['show_props_expanded']:
                icon = 'DOWNARROW_HLT'
            else:
                icon = 'RIGHTARROW'
            op = col.operator('bmtools.bmtool_invoke_operator_func',
                              text='Properties', icon=icon)
            op.func = line
            # }}}

            if cluster.variables['show_props_expanded']\
                    or cluster.variables['show_definition_expanded']:

                box = layout.box()

                if cluster.variables['show_definition_expanded']:
                    box_2 = box.box()
                    for x, y in zip(cluster.parser_variables,
                                    cluster.parser_variables.values()):
                        line = f'self.m_list.find_cluster_by_name(\'{cluster.name}\').parser_variables[\'{x}\']'
                        self.draw_var_editor(box_2, line, fast=True)

                if cluster.variables['show_props_expanded']:
                    box_2 = box.box()
                    for x, y in zip(cluster.variables,
                                    cluster.variables.values()):
                        line = f'self.m_list.find_cluster_by_name(\'{cluster.name}\').variables[\'{x}\']'
                        self.draw_var_editor(box_2, line, fast=True)

            if cluster.has_clusters():
                self.__draw_clusters_list(layout, cluster)
            else:
                self.__draw_modifiers_list(layout, cluster)
        # }}}

    def __draw_modifier(self, layout, modifier):  # {{{
        if modifier.show_expanded:
            icon = 'DOWNARROW_HLT'
        else:
            icon = 'RIGHTARROW'

        row = layout.row()

        # Modifier collapsed {{{
        val = not modifier.show_expanded
        col = row.column()
        line = f'self.m_list.find_modifier_by_name(\'{modifier.name}\').\
                show_expanded = {val}'
        line = re.sub('self', self.get_class_line(), line)
        if modifier.show_expanded:
            icon = 'DOWNARROW_HLT'
        else:
            icon = 'RIGHTARROW'
        op = col.operator('bmtools.bmtool_invoke_operator_func',
                          text=modifier.name + ' modifier', icon=icon)
        op.func = line
        # }}}

        # Actions {{{
        # Move down
        line = f'self.m_list.get_cluster_or_layer(self.m_list.find_modifier_by_name("{modifier.name}")).\
                move_down("{modifier.name}")'
        line = re.sub('self', self.get_class_line(), line)
        col = row.column()
        op = col.operator('bmtools.bmtool_invoke_operator_func',
                          text='', icon='TRIA_DOWN')
        op.func = line

        # Move up
        line = f'self.m_list.get_cluster_or_layer(self.m_list.find_modifier_by_name("{modifier.name}")).\
                move_up("{modifier.name}")'
        line = re.sub('self', self.get_class_line(), line)
        col = row.column()
        op = col.operator('bmtools.bmtool_invoke_operator_func',
                          text='', icon='TRIA_UP')
        op.func = line

        # Remove
        line = f'self.m_list.get_cluster_or_layer(self.m_list.find_modifier_by_name("{modifier.name}")).\
                remove("{modifier.name}")'
        line = re.sub('self', self.get_class_line(), line)
        col = row.column()
        op = col.operator('bmtools.bmtool_invoke_operator_func',
                          text='', icon='X')
        op.func = line

        # Apply
        line = f'self.m_list.get_cluster_or_layer(self.m_list.find_modifier_by_name("{modifier.name}")).\
                apply("{modifier.name}")'
        line = re.sub('self', self.get_class_line(), line)
        col = row.column()
        op = col.operator('bmtools.bmtool_invoke_operator_func',
                          text='', icon='CHECKMARK')
        op.func = line

        # Visibility {{{
        # v = {
        #      'show_viewport': None,
        #      'show_editmode': None,
        #      'show_on_cage': None,
        #      'show_render': None,
        #      }

        # for i, x in enumerate(v):
        #     m = [0, 0, 0, 0]
        #     m[i] = 1
        #     line_2 = str(m)
        #     line = f'self.m_list.find_cluster_by_name("{cluster.name}").\
        #             toggle_this_cluster_visibility({line_2})'
        #     line = re.sub('self', self.get_class_line(), line)
        #     val = cluster.get_this_cluster_visibility()[i]

        #     if val == 'ON':
        #         icon = 'CUBE'
        #     elif val == 'HALF':
        #         icon = 'CUBE'
        #     elif val == 'OFF':
        #         icon = 'X'
        #     else:
        #         raise ValueError

        #     col = row.column()
        #     op = col.operator('bmtools.bmtool_invoke_operator_func',
        #                       text='', icon=icon)
        #     op.func = line

        # }}}

        # Duplicate
        # line = f'self.m_list.get_cluster_or_layer(self.m_list.find_cluster_by_name("{cluster.name}")).\
        #         duplicate("{cluster.name}")'
        # line = re.sub('self', self.get_class_line(), line)
        # col = row.column()
        # op = col.operator('bmtools.bmtool_invoke_operator_func',
        #                   text='', icon='DUPLICATE')
        # op.func = line
        # }}}

        if modifier.show_expanded:
            box = layout.box()
            p = get_all_editable_props(modifier, no_ignore=True)
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
        for x in context.object.modifiers:
            x.show_expanded = False
        prefs = context.preferences.addons['bmtools'].preferences
        context.window_manager.invoke_popup(
                self, width=prefs.clusters_list_popup_width)
        return {'RUNNING_MODAL'}
