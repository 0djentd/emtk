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
from bpy.types import PropertyGroup

from .utils import get_attr_or_iter_from_str_nested
from .utils import set_attr_or_iter_from_str_nested

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UIClassVariablesEditorCache(PropertyGroup):
    """This prop group used to edit variables in ui."""

    # New attribute value
    var_editor_bool: BoolProperty(False)
    var_editor_int: IntProperty(0)
    var_editor_float: FloatProperty(0.0)
    var_editor_str: StringProperty('')

    # Attribute name
    # Example: m_list.get_first().parser_variables['by_type'][0]
    # 'cls' should be skipped, as
    # var_editor_currently_edited_class is used insead.
    var_editor_currently_edited: StringProperty('')

    # Class name
    # Example: bpy.types.BMTOOLS_OT_clusters_list_popup
    var_editor_currently_edited_class: StringProperty('')


class UIClassVariablesEditor():
    """
    Mix-in class for operators and panels that
    should edit class variables.
    """

    # info {{{
    """
    How this thing should work:

    To edit class variable from ui, some property should be used.
    Type of property should be same as edited variable type.

    There is bool, int, float and str properties in blender.
    There is no list and dict properties that can be easily used
    to edit class variable.

    bool, int, float and str should have following buttons:
        edit variable

    list and dict should have following buttons:
        edit variable
        move variable up
        move variable down
        add new variable
        remove variable

    edit variable should be useable with other lists and dicts.

    Only one variable should be edited at the time.

    What internal states should editor have:
        1) no variable edited:
            dont draw editor.
            dont update variables.
            draw buttons "start editing"

        2) editing variable:
            draw property
            update variable in draw method.
            draw button "stop editing"
            draw buttons "start editing"
    """
    # }}}

    def draw_var_editor(self,  # {{{
                        layout,
                        attr_str,
                        *args,
                        draw_name=True,
                        name=None,
                        draw_value=None,
                        round_value=2,
                        icon=None,
                        fast=False,
                        check=False,
                        **kwargs
                        ):

        """Draw editor for variable."""

        if type(attr_str) is not str:
            raise TypeError
        for x in '+=-':
            if x in attr_str:
                raise ValueError
        """
        Property and button look like this:
        distance [123] (stop)
        """
        m = re.match('self\.', attr_str)
        if m is not None:
            attr_str = attr_str[5:]

        cls = type(self)
        attr = get_attr_or_iter_from_str_nested(
                cls, attr_str, fast=fast, check=check)

        prop_group_name = get_prop_group_name(cls)
        prop_group = getattr(bpy.context.scene, prop_group_name)
        attr_type = type(attr)
        if attr_type is list:
            return

        elif attr_type is dict:
            return
        else:
            prop_name = _get_var_editor_prop_name(attr_type)

        row = layout.row()
        col = row.column()

        # Active
        if prop_group.var_editor_currently_edited == attr_str:
            col.prop(prop_group, prop_name, text='')
            line = f'self.var_editor_stop("{attr_str}")'
            line = re.sub('self', self.get_class_line(), line)
            col = row.column()
            if icon is not None:
                op = col.operator('bmtools.bmtool_invoke_operator_func',
                                  text="Save", icon=icon)
            else:
                op = col.operator('bmtools.bmtool_invoke_operator_func',
                                  text="Save")
            op.func = line

        # Editable
        else:
            if draw_name:
                if name is not None:
                    var_name = name
                else:
                    var_name = re.sub('.*\.', '', attr_str)
                if draw_value:
                    var_name += ': '
            else:
                var_name = ''

            if draw_value:
                if type(attr) is float:
                    val = math.round(attr, round_value)
                else:
                    val = attr
                val = str(val)
            else:
                val = ''

            line = f'self.var_editor_start("{attr_str}")'
            line = re.sub('self', self.get_class_line(), line)

            if icon is not None:
                op = col.operator('bmtools.bmtool_invoke_operator_func',
                                  text=var_name + val, icon=icon)
            else:
                op = col.operator('bmtools.bmtool_invoke_operator_func',
                                  text=var_name + val)
            op.func = line
    # }}}

    @classmethod
    def var_editor_start(cls, variable):  # {{{
        if type(variable) is not str:
            raise TypeError

        prop_group_name = get_prop_group_name(cls)
        prop_group = getattr(bpy.context.scene, prop_group_name)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(' ')
            logger.debug(f'Variable editor inv. {cls}, {variable}')
            logger.debug(f'prop_group_name: {prop_group_name}')
            logger.debug(f'prop_group: {prop_group}')

            logger.debug(f'var_editor_currently_edited: {prop_group.var_editor_currently_edited}')
            logger.debug(f'var_editor_bool: {prop_group.var_editor_bool}')
            logger.debug(f'var_editor_int: {prop_group.var_editor_int}')
            logger.debug(f'var_editor_float: {prop_group.var_editor_float}')
            logger.debug(f'var_editor_str: {prop_group.var_editor_str}')

        prop_group.var_editor_currently_edited = variable
        if '(' in variable:
            attr = get_attr_or_iter_from_str_nested(cls, variable, fast=True)
        else:
            attr = get_attr_or_iter_from_str_nested(cls, variable)

        attr_type = type(attr)
        prop_name = _get_var_editor_prop_name(attr_type)
        setattr(prop_group, prop_name, attr)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'var_editor_currently_edited: {prop_group.var_editor_currently_edited}')
            logger.debug(f'var_editor_bool: {prop_group.var_editor_bool}')
            logger.debug(f'var_editor_int: {prop_group.var_editor_int}')
            logger.debug(f'var_editor_float: {prop_group.var_editor_float}')
            logger.debug(f'var_editor_str: {prop_group.var_editor_str}')
            logger.debug('Variable editor inv. finished')
            logger.debug(' ')
    # }}}

    @classmethod
    def var_editor_stop(cls, variable):  # {{{
        if type(variable) is not str:
            raise TypeError

        prop_group_name = get_prop_group_name(cls)
        prop_group = getattr(bpy.context.scene, prop_group_name)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(' ')
            logger.debug(f'Variable editor remove {cls}, {variable}')
            logger.debug(f'prop_group_name: {prop_group_name}')
            logger.debug(f'prop_group: {prop_group}')

            logger.debug(f'var_editor_currently_edited: {prop_group.var_editor_currently_edited}')
            logger.debug(f'var_editor_bool: {prop_group.var_editor_bool}')
            logger.debug(f'var_editor_int: {prop_group.var_editor_int}')
            logger.debug(f'var_editor_float: {prop_group.var_editor_float}')
            logger.debug(f'var_editor_str: {prop_group.var_editor_str}')

        if '(' in variable:
            attr = get_attr_or_iter_from_str_nested(
                    cls, prop_group.var_editor_currently_edited, fast=True)
        else:
            attr = get_attr_or_iter_from_str_nested(
                    cls, prop_group.var_editor_currently_edited)

        attr_type = type(attr)
        prop_name = _get_var_editor_prop_name(attr_type)
        attr_val = getattr(prop_group, prop_name)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'attr: {attr}')
            logger.debug(f'prop_name: {prop_name}')
            logger.debug(f'attr_val: {attr_val}')

        if '(' in variable:
            set_attr_or_iter_from_str_nested(
                    cls, prop_group.var_editor_currently_edited,
                    attr_val, fast=True)
        else:
            set_attr_or_iter_from_str_nested(
                    cls, prop_group.var_editor_currently_edited, attr_val)

        if logger.isEnabledFor(logging.DEBUG):
            if '(' in variable:
                attr = get_attr_or_iter_from_str_nested(
                        cls, prop_group.var_editor_currently_edited, fast=True)
            else:
                attr = get_attr_or_iter_from_str_nested(
                        cls, prop_group.var_editor_currently_edited)

            logger.debug(f'new attr: {attr}')

            logger.debug(f'var_editor_currently_edited: {prop_group.var_editor_currently_edited}')
            logger.debug(f'var_editor_bool: {prop_group.var_editor_bool}')
            logger.debug(f'var_editor_int: {prop_group.var_editor_int}')
            logger.debug(f'var_editor_float: {prop_group.var_editor_float}')
            logger.debug(f'var_editor_str: {prop_group.var_editor_str}')

            logger.debug('Variable editor remove finished')
            logger.debug(' ')

        prop_group.var_editor_currently_edited = ''
    # }}}


def _get_var_editor_prop_name(var_type):
    if var_type is bool:
        prop_name = "var_editor_bool"
    elif var_type is int:
        prop_name = "var_editor_int"
    elif var_type is float:
        prop_name = "var_editor_float"
    elif var_type is str:
        prop_name = "var_editor_str"
    else:
        raise TypeError
    return prop_name


def get_prop_group_name(cls):
    line = None
    name = cls.__name__
    if re.match('.*_OT_', name):
        line = re.sub('.*_OT_', 'cls_var_editor_operator_', name)
    elif re.match('.*_PT_', name):
        line = re.sub('.*_PT_', 'cls_var_editor_panel_', name)
    return line
