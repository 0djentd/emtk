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

import re
# import logging
# import math
# import string

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)


def set_attr_or_iter_from_str_nested(
        obj, attr_str, val, check=True, fast=False):
    m = re.search('\..*', attr_str)
    obj_str = attr_str[0:m.start()]
    obj = get_attr_or_iter_from_str_nested(obj, obj_str, check, fast)
    attr = attr_str[m.start()+1:]
    setattr(obj, attr, val)
    return


def get_attr_or_iter_from_str_nested(obj, attr_str, check=True, fast=False):
    """Wrapper for getattr and iterattr, can be used with nested objects.

    Example:
    >>> class Cluster():
    >>>     x = {'y': {'z': True}}

    >>> c = Cluster()
    >>> get_attr_or_iter_from_str_nested(c, "x['y']")
    <<< {'z': True}
    """

    # logger.debug(obj, attr_str, check)
    if type(attr_str) is not str:
        raise TypeError
    if len(attr_str) == 0:
        raise ValueError
    if obj is None:
        raise TypeError

    for x in ',/\\=+;:':
        if x in attr_str:
            raise ValueError

    if fast:
        obj = eval('obj.' + attr_str)
        return obj

    var_str_elements = attr_str.split('.')
    # logger.debug(var_str_elements)

    for i, x in enumerate(var_str_elements):

        z_1 = len(re.findall('\[', x))
        z_2 = len(re.findall(']', x))

        # Sequence
        if z_1 == z_2 and z_1 > 1:
            obj = _workaround_iterable_sequence(obj, x)

        elif z_1 == z_2 and z_1 == 1:
            d_1 = len(re.findall('"', x))
            d_2 = len(re.findall("'", x))

            # List
            if d_1 == d_2 and d_1 == 0:
                m = re.search('\[[-]*[0-9]*]', x)
                index = int(x[m.start() + 1:m.end() - 1])
                list_attr = x[0:m.start()]
                list_obj = getattr(obj, list_attr)
                obj = list_obj[index]

            # Dict
            elif d_1 == 2:
                if d_2 != 0:
                    raise ValueError

                m = re.search('\[".*"]', x)
                index = x[m.start() + 2:m.end() - 2]
                list_attr = x[0:m.start()]
                list_obj = getattr(obj, list_attr)
                obj = list_obj[index]

            elif d_2 == 2:
                if d_1 != 0:
                    raise ValueError

                m = re.search("\['.*']", x)
                index = x[m.start() + 2:m.end() - 2]
                list_attr = x[0:m.start()]
                list_obj = getattr(obj, list_attr)
                obj = list_obj[index]

            else:
                raise ValueError

        # Attr
        elif z_1 == 0 and z_2 == 0:
            obj = getattr(obj, x)
        else:
            raise ValueError

        if i == len(var_str_elements) - 1:
            break
    # logger.debug(obj)
    return obj


def _workaround_iterable_sequence(obj, attr_str, check=True):
    """
    attr_str_example: x['dfsdf']['dsfgdgf'][1]['dfsdf']
    attr_str cant be like this:
    x[y['sdf]]
    x[y[0]]
    x[y + z]
    """

    # Example: ['x[', "'item'", "-1]"]
    s = attr_str.split('][')
    e = s[0]
    m = re.search('.*\[', e)
    attr_str_elements = [e[0:m.end() - 1], e[m.end():]]
    attr_str_elements.extend(s[1:])

    # Check {{{
    if check:
        last = None
        for i, x in enumerate(attr_str_elements):
            z_1 = len(re.findall('"', x))
            z_2 = len(re.findall("'", x))
            if z_1 > 2:
                raise ValueError
            if z_2 > 2:
                raise ValueError
            if z_1 != 0:
                if z_2 != 0:
                    raise ValueError

            if '\[' in x:
                if z_1 != 0:
                    raise ValueError
                if z_2 != 0:
                    raise ValueError

                if i == len(attr_str_elements) - 1:
                    raise ValueError
                if last == '\[':
                    raise ValueError
                last = '\['

            elif ']' in x:
                if i < len(attr_str_elements) - 1:
                    if z_1 != 0:
                        raise ValueError
                    if z_2 != 0:
                        raise ValueError

                if i == 0:
                    raise ValueError
                if last == ']':
                    raise ValueError
                last = ']'
    # }}}

    # Example: ['x', "'item'", "-1"]
    attr_str_elements[0] = re.sub('\[', '', attr_str_elements[0])
    attr_str_elements[-1] = re.sub(']', '', attr_str_elements[-1])

    for i, x in enumerate(attr_str_elements):
        if i == 0:
            obj = getattr(obj, attr_str_elements[0])
            continue

        # Dict
        if '"' in x or "'" in x:
            item = re.sub("'", '', x)
            item = re.sub('"', '', item)
            obj = obj[item]

        # List
        else:
            index = int(x)
            obj = obj[index]
    return obj
