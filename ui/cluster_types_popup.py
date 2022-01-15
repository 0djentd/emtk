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

from bpy.types import Operator
from bpy.props import BoolProperty, IntProperty, FloatProperty, StringProperty

from ..lib.utils.modifier_prop_types import get_all_editable_props

from .ui_class_variables_editor import UIClassVariablesEditor

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

USE_PROFILER = False


class BMTOOLS_OT_clusters_types_popup(
        UIClassVariablesEditor, Operator):
    bl_idname = "bmtools.cluster_types_popup"
    bl_label = "View and edit cluster types"

    def __init__(self):
        cls = type(self)
        cls.iteration = 0
        cls.edited_cluster_type = None
        print('Operator initialized')

    @classmethod
    def poll(cls, context):
        if context.area.type != 'VIEW_3D':
            return False
        else:
            return True

    def execute(self, context):
        print('Operator method')
        cls = type(self)
        return {'FINISHED'}

    # TODO: reuse?
    def draw(self, context):
        cls = type(self)
        cls.iteration += 1
        layout = self.layout
        layout.label(text='EMTK')
        row = layout.row()
        col = row.column()
        self.__draw_switcher(col)
        col = row.column()
        self.__draw_cluster_types_list(col)
        col = row.column()
        self.__draw_cluster_type(col)

    def __draw_switcher(self, layout):
        return

    def __draw_cluster_types_list(self, layout):
        return

    def __draw_cluster_type(self, layout):
        return

    def invoke(self, context, event):
        print('Operator invoked')
        prefs = context.preferences.addons['bmtools'].preferences
        context.window_manager.invoke_popup(
                self, width=prefs.clusters_list_popup_width)
        return {'RUNNING_MODAL'}
