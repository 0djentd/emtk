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

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# TODO: remove this module


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
        raise TypeError(var_type)
    return prop_name


def get_prop_group_name(cls):
    line = None
    name = cls.__name__
    if re.match('.*_OT_', name):
        line = re.sub('.*_OT_', 'cls_var_editor_operator_', name)
    elif re.match('.*_PT_', name):
        line = re.sub('.*_PT_', 'cls_var_editor_panel_', name)
    return line


def set_attr_or_iter_from_str_nested(
        obj, attr_str, val, check=True, fast=False):
    if obj is None:
        raise TypeError

    if check:
        _check_attr_str(attr_str)

    line = 'obj.' + attr_str + ' = val'
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug('Executing line: ' + line)
    # exec(line, globals(), locals())
    exec(line, {}, {'obj': obj, 'val': val})


def get_attr_or_iter_from_str_nested(obj, attr_str, check=True, fast=False):

    if check:
        _check_attr_str(attr_str)

    line = 'obj.' + attr_str

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug('Evaluating line: ' + line)

    # result = eval(line, globals(), locals())
    result = eval(line, {}, {'obj': obj})

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(f'Got {result}')
    return result


def _check_attr_str(attr_str: str):
    if re.match('obj\.', attr_str):
        raise ValueError
    if re.search('\*', attr_str):
        raise ValueError
    if re.search('/', attr_str):
        raise ValueError
    if re.search('\. ', attr_str):
        raise ValueError
    if re.search('=', attr_str):
        raise ValueError
    if re.search('  ', attr_str):
        raise ValueError
    if re.search('\+', attr_str):
        raise ValueError


def get_last_attr_name_in_sequence(sequence):
    """Get last attr name in sequence.

    Example:
    >>> get_last_attr_name_in_sequence('cluster.name')
    <<< 'name'
    >>> get_last_attr_name_in_sequence('cluster.modifiers[3]')
    <<< 'modifiers[3]'
    """
    if type(sequence) is not str:
        raise TypeError

    m = re.search('[^.]*\\Z', sequence)
    return m.string[m.start(): m.end()]


def get_attr_obj_str(sequence):
    """Get attribute's object from attr str.

    Returns list attr_str if attr is element of list.

    Example:
    >>> get_last_attr_name_in_sequence('m_list.cluster.name')
    <<< 'm_list.cluster'
    >>> get_last_attr_name_in_sequence('m_list.cluster.name[1]')
    <<< 'm_list.cluster.name'
    >>> get_attr_obj_str('cluster.modifiers[3]')
    <<< 'cluster.modifiers'
    >>> get_attr_obj_str('cluster')
    <<< None
    """
    if type(sequence) is not str:
        raise TypeError
    if '.' not in sequence and '[' not in sequence:
        return None

    # Example: 'cluster.modifiers[1]' -> 'modifiers[1]'
    m = re.search('[^.]*\\Z', sequence)
    f = False
    for x in '[]':
        if x in m.string[m.start():m.end()]:
            f = True
            break

    # Example: 'cluster.modifiers[1]' -> 'cluster.modifiers'
    if f:
        m = re.search('[.*\\Z', sequence)
        result = sequence[:m.start()-1]
    # Example: 'cluster.name' -> 'cluster'
    else:
        result = m.string[:m.start()-1]
    return result
