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
import json

import bpy

from ..clusters.modifiers_cluster import ModifiersCluster
from ..clusters.clusters_layer import ClustersLayer
from ..clusters.cluster_trait import ClusterTrait


logger = logging.getLogger(__package__)


def deserialize_cluster_type(serialized_cluster_type, *args, **kwargs):
    """
    Takes string with info about cluster type as argument.

    Returns cluster type instance.
    """
    x = json.loads(serialized_cluster_type)

    if not isinstance(x, dict):
        t = type(serialized_cluster_type)
        raise TypeError(f'Serialized cluster type should be dict, not {t}')

    if x['cluster_class'] == 'ModifiersCluster':
        result = ModifiersCluster(
                                  cluster_name=x['cluster_name'],
                                  cluster_type=x['cluster_type'],
                                  modifiers_by_type=x['modifiers_by_types'],
                                  modifiers_by_name=x['modifiers_by_names'],
                                  cluster_tags=x['cluster_tags'],
                                  cluster_priority=x['cluster_priority'],
                                  cluster_is_sane=x['cluster_is_sane'],
                                  cluster_createable=x['cluster_createable'],
                                  dont_define_cluster=False,
                                  *args, **kwargs
                                  )

    elif x['cluster_class'] == 'ClustersLayer':
        result = ClustersLayer(
                               cluster_name=x['cluster_name'],
                               cluster_type=x['cluster_type'],
                               modifiers_by_type=x['modifiers_by_types'],
                               modifiers_by_name=x['modifiers_by_names'],
                               cluster_tags=x['cluster_tags'],
                               cluster_priority=x['cluster_priority'],
                               cluster_is_sane=x['cluster_is_sane'],
                               cluster_createable=x['cluster_createable'],
                               dont_define_cluster=False,
                               *args, **kwargs
                               )
    else:
        raise TypeError(f'Cant deserialize {x["cluster_class"]}')
    return result


def serialize_cluster_type(cluster_type):
    """
    Returns string with info about cluster_type that
    is enough to create new cluster_type instance
    through deserialize_cluster_type.
    """
    if not isinstance(cluster_type, ClusterTrait):
        raise TypeError
    return cluster_type.serialize_this_cluster_type()

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
