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
# import copy
import json

import bpy

from ..clusters.utils import deserialize_cluster_type

logger = logging.getLogger(__package__)


def get_cluster_types_from_settings(addon_name, group):
    """
    Returns list of deserialized but not unwrapped
    cluster types from addon settings.
    """
    if not isinstance(addon_name, str):
        raise TypeError
    if not isinstance(group, str) and not isinstance(group, int):
        raise TypeError

    cluster_types = []
    result = []
    c = bpy.context.preferences.addons[addon_name].preferences.cluster_types
    for x in c:
        cluster_types.append(deserialize_cluster_type(x))
    for x in cluster_types:
        if x['group'] == group:
            result.append(x)
    return result


def get_cluster_types_from_object(obj, addon_name, group,
                                  *args, dont_add_prop=True):
    """
    Returns list of deserialized but not unwrapped
    cluster types from addon settings.
    """
    if not isinstance(addon_name, str):
        raise TypeError
    if not isinstance(group, str) and not isinstance(group, int):
        raise TypeError

    cluster_types = []
    result = []
    prop_name = f'{addon_name}{group}'

    try:
        c = getattr(obj, prop_name)
    except KeyError:
        if not dont_add_prop:
            setattr(obj, prop_name, json.dumps([]))
        return []

    for x in c:
        cluster_types.append(deserialize_cluster_type(x))
    for x in cluster_types:
        if x['group'] == group:
            result.append(x)
    return result


def save_cluster_type_to_object(
                                obj,
                                addon_name,
                                group,
                                deserialized_cluster_type_to_add,
                                ):
    """
    Saves cluster type to object props.
    """
    if not isinstance(obj, bpy.types.Object):
        raise TypeError
    if not isinstance(deserialized_cluster_type_to_add, str):
        raise TypeError
    if len(deserialized_cluster_type_to_add) == 0:
        raise ValueError

    deserialized_cluster_types = get_cluster_types_from_object(
            obj, addon_name, group, dont_add_prop=False)

    duplicates = []

    for x in deserialized_cluster_types:
        if deserialized_cluster_type_to_add.cluster_name == x.cluster_name:
            duplicates.append(x)

    for x in duplicates:
        deserialized_cluster_types.remove(x)

    deserialized_cluster_types.append(
            deserialized_cluster_type_to_add)

    serialized_cluster_types = json.dumps(
            deserialized_cluster_types)

    setattr(obj, f'{addon_name}{group}', serialized_cluster_types)
    return
