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

try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    from ..dummy_modifiers import DummyBlenderModifier
    _WITH_BPY = False

logger = logging.getLogger(__package__)
logger.setLevel(logging.INFO)

_MODIFIER_TYPES = [
                   "DATA_TRANSFER",
                   "MESH_CACHE",
                   "MESH_SEQUENCE_CACHE",
                   "NORMAL_EDIT",
                   "WEIGHTED_NORMAL",
                   "UV_PROJECT",
                   "UV_WARP",
                   "VERTEX_WEIGHT_EDIT",
                   "VERTEX_WEIGHT_MIX",
                   "VERTEX_WEIGHT_PROXIMITY",
                   "ARRAY",
                   "BEVEL",
                   "BOOLEAN",
                   "BUILD",
                   "DECIMATE",
                   "EDGE_SPLIT",
                   "NODES",
                   "MASK",
                   "MIRROR",
                   "MESH_TO_VOLUME",
                   "MULTIRES",
                   "REMESH",
                   "SCREW",
                   "SKIN",
                   "SOLIDIFY",
                   "SUBSURF",
                   "TRIANGULATE",
                   "VOLUME_TO_MESH",
                   "WELD",
                   "WIREFRAME",
                   "ARMATURE",
                   "CAST",
                   "CURVE",
                   "DISPLACE",
                   "HOOK",
                   "LAPLACIANDEFORM",
                   "LATTICE",
                   "MESH_DEFORM",
                   "SHRINKWRAP",
                   "SIMPLE_DEFORM",
                   "SMOOTH",
                   "CORRECTIVE_SMOOTH",
                   "LAPLACIANSMOOTH",
                   "SURFACE_DEFORM",
                   "WARP",
                   "WAVE",
                   "VOLUME_DISPLACE",
                   "CLOTH",
                   "COLLISION",
                   "DYNAMIC_PAINT",
                   "EXPLODE",
                   "FLUID",
                   "OCEAN",
                   "PARTICLE_INSTANCE",
                   "PARTICLE_SYSTEM",
                   "SOFT_BODY",
                   "SURFACE"
                   ]


def get_modifier_state(modifier):
    """Returns dict with modifier's properties that can be
    serialized.

    'extra_info' not used when restoring modifier props.
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
    """Restores modifier state from dict."""
    logger.info(f'Restoring {modifier_state} for {modifier}')

    if _WITH_BPY:
        modifier_type = bpy.types.Modifier
    else:
        modifier_type = DummyBlenderModifier

    if not isinstance(modifier, modifier_type):
        raise TypeError
    if not isinstance(modifier_state, dict):
        raise TypeError
    if modifier.type != modifier_state['type']:
        raise ValueError('Wrong modifier type.')

    _IGNORE_MODIFIER_ATTR = ['type', 'extra_info']

    for x in modifier_state:
        if x in _IGNORE_MODIFIER_ATTR\
                or 'is_' in x:
            logger.debug(f'Skipping {x}')
            continue
        setattr(modifier, x, modifier_state[x])
        logger.debug(f'Restored {modifier_state[x]}')
    logger.debug('Finished restoring modifier state.')
