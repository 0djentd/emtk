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
import logging
# import math
# import string

logger = logging.getLogger(__name__)
# logger.setLevel(logging.ERROR)
logger.setLevel(logging.DEBUG)


# TODO: add checks for attr_str.
# TODO: remove this method.
def set_attr_or_iter_from_str_nested(
        obj, attr_str, val, check=True, fast=False):
    if obj is None:
        raise TypeError

    if check:
        if re.match('\*', attr_str):
            raise ValueError
        if re.match('/', attr_str):
            raise ValueError
        if re.match('\. ', attr_str):
            raise ValueError
        if re.match('=', attr_str):
            raise ValueError
        if re.match('  ', attr_str):
            raise ValueError
        if re.match('\+', attr_str):
            raise ValueError

    line = 'obj.' + attr_str + ' = val'
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug('Executing line: ' + line)
    # exec(line, globals(), locals())
    exec(line, {}, {'obj': obj, 'val': val})


# TODO: remove this method.
def get_attr_or_iter_from_str_nested(obj, attr_str, check=True, fast=False):

    if check:
        if re.match('\*', attr_str):
            raise ValueError
        if re.match('/', attr_str):
            raise ValueError
        if re.match('\. ', attr_str):
            raise ValueError
        if re.match('=', attr_str):
            raise ValueError
        if re.match('  ', attr_str):
            raise ValueError
        if re.match('\+', attr_str):
            raise ValueError

    line = 'obj.' + attr_str
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug('Evaluating line: ' + line)
    # result = eval(line, globals(), locals())
    result = eval(line, {}, {'obj': obj})
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(f'Got {result}')
    return result
