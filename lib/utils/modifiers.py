# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import logging
import copy
import json

try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    from ..dummy_modifiers import DummyBlenderModifier
    _WITH_BPY = False

logger = logging.getLogger(__package__)
logger.setLevel(logging.INFO)


def get_modifier_state(modifier):
    """
    Returns dict with modifier's properties that can be
    serialized.
    """

    if _WITH_BPY:
        if not isinstance(modifier, bpy.types.Modifier):
            raise TypeError
    else:
        if not isinstance(modifier, DummyBlenderModifier):
            raise TypeError

    logger.info(f'Trying to get modifier state for {modifier}')
    result = {}
    for x in dir(modifier):

        # Skip what cant be stored.
        if '__' in x\
                or x == 'name':
            continue
        y = getattr(modifier, x)
        if not isinstance(y, str)\
                and not isinstance(y, int)\
                and not isinstance(y, float)\
                and not isinstance(y, bool):
            logger.debug(f'Skipping {type(y)}')
            continue

        # Add attribute name and value to result.
        result.update({x: y})

    # Add extra_info
    result.update({'extra_info': {}})
    logger.debug(f'Result is {result}')
    logger.debug('Finished getting modifier state.')
    return result


def restore_modifier_state(modifier, modifier_state):
    """
    Restores modifier state from dict.
    """
    logger.info(f'Restoring {modifier_state} for {modifier}')
    if _WITH_BPY:
        if not isinstance(modifier, bpy.types.Modifier):
            raise TypeError
    else:
        if not isinstance(modifier, DummyBlenderModifier):
            raise TypeError

    if not isinstance(modifier_state, dict):
        raise TypeError
    if modifier.type != modifier_state.type:
        raise ValueError('Wrong modifier type.')

    for x in modifier_state:
        if x == 'type'\
                or x == 'extra_info':
            logger.debug(f'Skipping {x}')
            continue
        setattr(modifier, modifier_state[x], x)
        logger.debug(f'Restored {modifier_state[x]}')

    logger.debug('Finished restoring modifier state.')
    return
