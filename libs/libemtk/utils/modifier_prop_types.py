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

try:
    import bpy
    Modifier = bpy.types.Modifier
    _WITH_BPY = True
except ModuleNotFoundError:
    from ..dummy_modifiers import DummyBlenderModifier
    Modifier = DummyBlenderModifier
    _WITH_BPY = False

logger = logging.getLogger(__package__)
logger.setLevel(logging.DEBUG)


# Const
# Props that cant be edited or properly displayed
NOT_VAL_PROP = {
    'rna_type',
    'debug',
}

# This props not intended to be edited.
# TODO: there is more not editable props
NOT_EDITABLE_PROP = {
    'type',
}

# Props that can be edited in emtk_operator anyway.
IGNORE_PROPS = {
    'name',
    'show_viewport',
    'show_render',
    'show_in_editmode',
    'show_on_cage',
    'show_expanded',
    'is_active',
}

# If one of this modifier prop properties is True,
# prop should not be editable.
CHECK_PROP_IS_FALSE = {
    'is_hidden',
    'is_readonly',
    'is_runtime',
    'is_output'
}

# This is types of props that can be edited in modal operator
EDITABLE_TYPES = {
    'BOOLEAN',
    'INT',
    'FLOAT',
    'STRING',
    'ENUM',
    'COLLECTION'
}

# All supported modifier types.
MODIFIER_TYPES = [
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
    # "MESH_TO_VOLUME",
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
    # "VOLUME_DISPLACE",
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


def get_all_editable_props(modifier, no_ignore=False):
    """
    Returns list of names of all modifier props that
    can be edited in modal operator.
    """
    if not _WITH_BPY:
        return ['angle_limit', 'segments']

    result = []
    props = modifier.rna_type.properties
    props_names = modifier.rna_type.properties.keys()
    for x in props_names:
        e = True
        if x in NOT_VAL_PROP:
            continue
        if x in NOT_EDITABLE_PROP:
            continue
        if x in IGNORE_PROPS and not no_ignore:
            continue
        if props[x].type not in EDITABLE_TYPES:
            continue
        for y in CHECK_PROP_IS_FALSE:
            if getattr(props[x], y) is True:
                e = False
                continue
        if e:
            result.append(x)

    for x in result:
        if not isinstance(x, str):
            raise TypeError
    return result


def get_props_filtered_by_types(modifier) -> dict:
    """Returns dict with modifier props."""
    result = {}
    props = get_all_editable_props(modifier)
    mod_props = modifier.rna_type.properties
    for x in props:
        t = mod_props[x].type
        if t not in result:
            result.update({t: set()})
        result[t].add(x)

    if not isinstance(result, dict):
        raise TypeError
    for x in result:
        if not isinstance(result[x], set):
            raise TypeError
        for y in x:
            if not isinstance(y, str):
                raise TypeError
    logger.debug(result)
    return result


def filter_props_by_type(modifier, props,
                         props_type, props_subtype=None):
    """Returns new list of modifier props filtered by props_type"""
    if not isinstance(props_type, str):
        raise TypeError
    if not isinstance(props, list):
        raise TypeError
    for x in props:
        if not isinstance(x, str):
            raise TypeError

    result = []
    mod_props = modifier.rna_type.properties
    for x in props:
        if mod_props[x].type != props_type:
            continue
        if props_subtype is not None\
                and mod_props[x].subtype == props_subtype:
            continue
        result.append(x)
    return result


def filter_props_by_types_subtypes(
        obj, props_names, t=None, s=None):
    """Returns filtered list of props names"""
    if not isinstance(t, list) and t is not None:
        raise TypeError
    if not isinstance(s, list) and s is not None:
        raise TypeError
    if not isinstance(props_names, list):
        raise TypeError
    for x in props_names:
        if not isinstance(x, str):
            raise TypeError

    result = []
    for x in props_names:
        prop = obj.rna_type.properties[x]
        if t is not None:
            if prop.type not in t:
                continue
        if s is not None:
            if prop.subtype not in s:
                continue
        result.append(x)
    return result
