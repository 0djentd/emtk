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
import re
import math
import copy

import bpy
from bpy.props import (BoolProperty, IntProperty,
                       FloatProperty, StringProperty)
from bpy.types import PropertyGroup

from .utils import (get_var_editor_prop_name,
                    get_prop_group_name,
                    get_last_attr_name_in_sequence,
                    get_attr_obj_str,
                    set_attr_or_iter_from_str_nested,
                    get_attr_or_iter_from_str_nested)

logger = logging.getLogger(__name__)
# logger.setLevel(logging.ERROR)
logger.setLevel(logging.DEBUG)


class UIClassVariablesEditorCache(PropertyGroup):  # {{{
    """This prop group used to edit variables in ui."""

    # New attribute value
    var_editor_bool: BoolProperty(default=False)
    var_editor_int: IntProperty(default=0)
    var_editor_float: FloatProperty(default=0.0)
    var_editor_str: StringProperty(default='')

    # Attribute name
    # Example: m_list[0].default_data['by_type'][0]
    # 'cls' should be skipped, as
    # var_editor_class is used insead.
    var_editor_currently_edited: StringProperty('')

    # Class name with 'bpy.types.' prefix
    # Example: bpy.types.BMTOOLS_OT_clusters_list_popup
    var_editor_class: StringProperty('')
# }}}


class UIClassVariablesEditor():   # {{{
    """
    Mix-in class for operators and panels that
    should be able to edit class variables from
    Blender UI ('draw(self, context)' method) using this module.
    """

    # info {{{
    """
    How this thing works:

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

    # this method can be recursive.
    @classmethod
    def draw_var_editor(cls,  # {{{
                        layout,
                        attr_str,
                        *args,
                        check=True,
                        **kwargs
                        ):
        """Draw editor for variable."""

        if type(attr_str) is not str:
            raise TypeError
        for x in '+=-':
            if x in attr_str:
                raise ValueError

        attr_str = re.sub('"', '\"', attr_str)
        attr_str = re.sub("'", "\'", attr_str)

        m = re.match('self\.', attr_str)
        if m is not None:
            attr_str = attr_str[5:]

        m = re.match('cls\.', attr_str)
        if m is not None:
            attr_str = attr_str[4:]

        attr = get_attr_or_iter_from_str_nested(
            cls, attr_str, check=check)
        if attr is None:
            logger.debug(f'Ignoring variable "{attr_str}", type is None.')
            return

        attr_type = type(attr)

        # recursive 'draw_var_editor'
        if attr_type is list:
            cls.__draw_list(
                layout,
                attr_str,
                attr=attr,
                check=check,
                *args,
                **kwargs
            )

        elif attr_type is dict:
            cls.__draw_dict(
                layout,
                attr_str,
                attr=attr,
                check=check,
                *args,
                **kwargs
            )
        # draw property
        else:
            cls.__draw_variable(
                layout,
                attr_str,
                attr=attr,
                check=check,
                *args,
                **kwargs
            )
    # }}}

    @classmethod
    def __draw_list(cls,  # {{{
                    layout,
                    attr_str,
                    *args,
                    attr=None,
                    draw_name=True,
                    name=None,
                    draw_value=None,
                    round_value=2,
                    icon=None,
                    check=False,
                    editable=True,
                    **kwargs
                    ):

        if attr is None:
            raise TypeError

        prop_group_name = get_prop_group_name(cls)
        prop_group = getattr(bpy.context.scene, prop_group_name)

        logger.debug('Drawing list')
        box = layout.box()

        attr_name = get_last_attr_name_in_sequence(attr_str)

        # Editable
        if attr_str not in prop_group.var_editor_currently_edited:
            line = f'cls.var_editor_start("{attr_str}")'
            line = re.sub('cls', cls.get_class_line(), line)
            if icon is not None:
                op = box.operator('bmtools.bmtool_invoke_operator_func',
                                  text=attr_name, icon=icon)
            else:
                op = box.operator('bmtools.bmtool_invoke_operator_func',
                                  text=attr_name)
            op.func = line
            return

        # Expanded (active)
        else:
            line = f'cls.var_editor_stop("{attr_str}")'
            line = re.sub('cls', cls.get_class_line(), line)

            if icon is not None:
                op = box.operator('bmtools.bmtool_invoke_operator_func',
                                  text=attr_name, icon=icon)
            else:
                op = box.operator('bmtools.bmtool_invoke_operator_func',
                                  text=attr_name)
            op.func = line

            for i, e in enumerate(attr):
                row = box.row()
                col = row.column()

                element_str = attr_str + f'[{i}]'
                logger.debug(f'Drawing element {element_str}')

                # Variable
                cls.draw_var_editor(col, element_str)

                if not editable:
                    continue

                # Remove element
                col = row.column()
                line = f'cls.{attr_str}.pop({i})'
                line = re.sub('cls', cls.get_class_line(), line)
                op = col.operator('bmtools.bmtool_invoke_operator_func',
                                  text="", icon='X')
                op.func = line

                line_2 = 'cls._UIClassVariablesEditor__move_list_element'

                # Move element
                col = row.column()
                line = line_2 + f'("{attr_str}", index={i}, direction=\'UP\')'
                line = re.sub('cls', cls.get_class_line(), line)
                op = col.operator('bmtools.bmtool_invoke_operator_func',
                                  text="", icon='TRIA_UP')
                op.func = line

                # Move element
                col = row.column()
                line = line_2 \
                    + f'("{attr_str}", index={i}, direction=\'DOWN\')'
                line = re.sub('cls', cls.get_class_line(), line)
                op = col.operator('bmtools.bmtool_invoke_operator_func',
                                  text="", icon='TRIA_DOWN')
                op.func = line

                line_2 = 'cls._UIClassVariablesEditor__duplicate_list_element'

                # Duplicate element
                col = row.column()
                line = line_2 \
                    + f'("{attr_str}", index={i})'
                line = re.sub('cls', cls.get_class_line(), line)
                op = col.operator('bmtools.bmtool_invoke_operator_func',
                                  text="", icon='TRIA_DOWN')
                op.func = line
            return
    # }}}

    @classmethod
    def __draw_dict(cls,  # {{{
                    layout,
                    attr_str,
                    attr,
                    *args,
                    draw_name=True,
                    name=None,
                    draw_value=None,
                    round_value=2,
                    icon=None,
                    check=False,
                    editable=True,
                    **kwargs
                    ):

        logger.debug('Drawing dict')

        if attr is None:
            raise TypeError

        prop_group_name = get_prop_group_name(cls)
        prop_group = getattr(bpy.context.scene, prop_group_name)

        logger.debug('Drawing list')
        box = layout.box()

        attr_name = get_last_attr_name_in_sequence(attr_str)

        # Editable
        if attr_str not in prop_group.var_editor_currently_edited:
            line = f'cls.var_editor_start("{attr_str}")'
            line = re.sub('cls', cls.get_class_line(), line)
            if icon is not None:
                op = box.operator('bmtools.bmtool_invoke_operator_func',
                                  text=attr_name, icon=icon)
            else:
                op = box.operator('bmtools.bmtool_invoke_operator_func',
                                  text=attr_name)
            op.func = line
            return

        # Expanded (active)
        else:
            line = f'cls.var_editor_stop("{attr_str}")'
            line = re.sub('cls', cls.get_class_line(), line)

            if icon is not None:
                op = box.operator('bmtools.bmtool_invoke_operator_func',
                                  text=attr_name, icon=icon)
            else:
                op = box.operator('bmtools.bmtool_invoke_operator_func',
                                  text=attr_name)
            op.func = line

            for x, y in zip(attr, attr.values()):
                row = box.row()
                col = row.column()

                element_str = attr_str + f'[\'{x}\']'
                logger.debug(f'Drawing element {element_str}')

                # Variable
                cls.draw_var_editor(col, element_str)

                if not editable:
                    continue

                # Remove element
                col = row.column()
                line = f'cls.{attr_str}.pop(\'{x}\')'
                line = re.sub('cls', cls.get_class_line(), line)
                op = col.operator('bmtools.bmtool_invoke_operator_func',
                                  text="", icon='X')
                op.func = line
        return
    # }}}

    @classmethod
    def __draw_variable(cls,  # {{{
                        layout,
                        attr_str,
                        *args,
                        attr=None,
                        draw_name=True,
                        name=None,
                        draw_value=None,
                        round_value=2,
                        icon=None,
                        check=False,
                        editable=True,
                        **kwargs
                        ):

        if attr is None:
            raise TypeError

        prop_group_name = get_prop_group_name(cls)
        prop_group = getattr(bpy.context.scene, prop_group_name)
        prop_name = get_var_editor_prop_name(type(attr))

        row = layout.row()
        col = row.column()

        # Active
        if editable and prop_group.var_editor_currently_edited == attr_str:
            col.prop(prop_group, prop_name, text='')
            line = f'cls.var_editor_stop("{attr_str}")'
            line = re.sub('cls', cls.get_class_line(), line)
            col = row.column()
            if icon is not None:
                op = col.operator('bmtools.bmtool_invoke_operator_func',
                                  text="Save", icon=icon)
            else:
                op = col.operator('bmtools.bmtool_invoke_operator_func',
                                  text="Save")
            op.func = line
            return

        # Editable
        else:
            if draw_name:
                if name is not None:
                    var_name = name
                else:
                    m = re.search('[^.]*\\Z', attr_str)
                    var_name = m.string[m.start(): m.end()]
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

            if not editable:
                col.label(text=var_name + val)
                return

            line = f'cls.var_editor_start("{attr_str}")'
            line = re.sub('cls', cls.get_class_line(), line)

            if icon is not None:
                op = col.operator('bmtools.bmtool_invoke_operator_func',
                                  text=var_name + val, icon=icon)
            else:
                op = col.operator('bmtools.bmtool_invoke_operator_func',
                                  text=var_name + val)
            op.func = line
            return
    # }}}

    @classmethod
    def var_editor_start(cls, variable):  # {{{
        """Start editing class variable in UI.

        variable str should only use " or '.

        Example:
        var_editor_start(bpy.types.BMTOOLS_OT_clusters_list_popup,
                         'm_list.get_cluster().name')
        """
        if type(variable) is not str:
            raise TypeError

        prop_group_name = get_prop_group_name(cls)
        prop_group = getattr(bpy.context.scene, prop_group_name)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(' ')
            logger.debug(f'Variable editor inv. {cls}, {variable}')
            logger.debug(f'prop_group_name: {prop_group_name}')
            logger.debug(f'prop_group: {prop_group}')

            logger.debug(f'var_editor_currently_edited: \
                    {prop_group.var_editor_currently_edited}')

        prop_group.var_editor_currently_edited = variable
        attr = get_attr_or_iter_from_str_nested(cls, variable)

        attr_type = type(attr)

        if attr_type not in {list, dict}:
            prop_name = get_var_editor_prop_name(attr_type)
            setattr(prop_group, prop_name, attr)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'var_editor_currently_edited: \
                    {prop_group.var_editor_currently_edited}')
            logger.debug('Variable editor inv. finished')
            logger.debug(' ')
    # }}}

    @classmethod
    def var_editor_stop(cls, variable):  # {{{
        """Stop editing class variable in UI and set edited class variable.

        variable str should only use " or '.

        Example:
        var_editor_stop(bpy.types.BMTOOLS_OT_clusters_list_popup,
                         'm_list.get_cluster().name')
        """
        if type(variable) is not str:
            raise TypeError

        prop_group_name = get_prop_group_name(cls)
        prop_group = getattr(bpy.context.scene, prop_group_name)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(' ')
            logger.debug(f'Variable editor remove {cls}, {variable}')
            logger.debug(f'prop_group_name: {prop_group_name}')
            logger.debug(f'prop_group: {prop_group}')

            logger.debug(f'var_editor_currently_edited: \
                    {prop_group.var_editor_currently_edited}')

        attr = get_attr_or_iter_from_str_nested(
            cls, prop_group.var_editor_currently_edited)

        attr_type = type(attr)

        if attr_type not in {list, dict}:
            prop_name = get_var_editor_prop_name(attr_type)
            attr_val = getattr(prop_group, prop_name)

            # Set attribute value
            set_attr_or_iter_from_str_nested(
                cls, prop_group.var_editor_currently_edited, attr_val)

        if logger.isEnabledFor(logging.DEBUG):
            attr = get_attr_or_iter_from_str_nested(
                cls, prop_group.var_editor_currently_edited)

            logger.debug(f'new attr: {attr}')

            logger.debug(f'var_editor_currently_edited: \
                    {prop_group.var_editor_currently_edited}')
            logger.debug('Variable editor remove finished')
            logger.debug(' ')

        prop_group.var_editor_currently_edited = ''
    # }}}

    @classmethod
    def __move_list_element(  # {{{
            cls, list_attr_str: str, index: int, direction: str):
        if type(list_attr_str) is not str:
            raise TypeError
        if type(index) is not int:
            raise TypeError

        attr = get_attr_or_iter_from_str_nested(cls, list_attr_str)
        logger.info(f'Moving {attr} element {index} {direction}')

        if direction == 'UP':
            if index != len(attr) - 1:
                e = attr.pop(index)
                attr.insert(index + 1, e)
            else:
                return
        elif direction == 'DOWN':
            if index != 0:
                e = attr.pop(index)
                attr.insert(index - 1, e)
            else:
                return
        else:
            raise ValueError
    # }}}

    @classmethod
    def __duplicate_list_element(  # {{{
            cls, list_attr_str: str, index: int):
        if type(list_attr_str) is not str:
            raise TypeError
        if type(index) is not int:
            raise TypeError

        attr = get_attr_or_iter_from_str_nested(cls, list_attr_str)
        element = attr[index]
        duplicate = copy.deepcopy(element)
        attr.insert(index + 1, duplicate)

        logger.info(f'Duplicating {attr} element {index}')
        logger.debug(f'{element}, {duplicate}')

    # }}}
# }}}
