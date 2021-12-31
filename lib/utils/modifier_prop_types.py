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

import bpy

# This props not intended to be edited.
NOT_EDITABLE_PROPS = {'rna_type', 'debug'}

# This props should not be editable.
CHECK_PROP_IS_FALSE = {'is_hidden', 'is_readonly', 'is_runtime'}

# This is types of props that can be edited in modal operator
EDITABLE_TYPES = {'BOOL', 'INT', 'FLOAT', 'STRING', 'ENUM'}


def get_all_editable_props(modifier):
    """
    Returns all props that can be edited in modal operator.
    """
    if not isinstance(modifier, bpy.types.Modifier):
        raise TypeError
    result = []
    props = modifier.rna_type.properties
    for x in props:
        e = True
        if x in NOT_EDITABLE_PROPS:
            continue
        if props[x].type not in EDITABLE_TYPES:
            continue
        for y in CHECK_PROP_IS_FALSE:
            if getattr(props[x], y) is True:
                e = False
                continue
        if e:
            result.append(x)
    return result
