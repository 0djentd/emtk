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

try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    # from ....dummy_modifiers import DummyBlenderModifier
    _WITH_BPY = False

from ..clusters.modifiers_cluster import ModifiersCluster
from ..clusters.clusters_layer import ClustersLayer
from ..clusters.cluster_trait import ClusterTrait


logger = logging.getLogger(__package__)
logger.setLevel(logging.DEBUG)


def deserialize_cluster_type(cluster_type, *args, **kwargs):
    """
    Takes string with info about cluster type or dict as argument.

    Returns cluster type instance.
    """
    if not isinstance(cluster_type, str):
        raise TypeError(f'Expected str, not {type(cluster_type)}')
    return deserialize_cluster_type_definition(
            json.loads(cluster_type))


def deserialize_cluster_type_definition(cluster_type_definition,
                                        *args, **kwargs):
    if not isinstance(cluster_type_definition, dict):
        raise TypeError(f'Expected dict, not {type(cluster_type_definition)}')

    x = cluster_type_definition

    if x['cluster_trait_subclass'] == 'ModifiersCluster':
        result = ModifiersCluster(
                                  cluster_name=x['name'],
                                  cluster_type=x['type'],
                                  modifiers_by_type=x['by_type'],
                                  modifiers_by_name=x['by_name'],
                                  cluster_tags=x['tags'],
                                  cluster_priority=x['priority'],
                                  cluster_is_sane=x['sane'],
                                  cluster_createable=x['createable'],
                                  dont_define_cluster=False,
                                  *args, **kwargs
                                  )

    elif x['cluster_trait_subclass'] == 'ClustersLayer':
        result = ClustersLayer(
                               cluster_name=x['name'],
                               cluster_type=x['type'],
                               modifiers_by_type=x['by_type'],
                               modifiers_by_name=x['by_name'],
                               cluster_tags=x['tags'],
                               cluster_priority=x['priority'],
                               cluster_is_sane=x['sane'],
                               cluster_createable=x['createable'],
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
        raise TypeError(f'Expected ClusterTrait, not {type(cluster_type)}')
    return cluster_type.serialize_this_cluster_type()


# ==========================
# Cluster types from settings
# ==========================
def get_cluster_types_from_settings(addon_name, group=None):
    """
    Returns list of cluster types from addon settings.
    """

    logger.info(f'Trying to get cluster types from settings for {addon_name}')

    c = _get_cluster_types_definitions_from_settings(addon_name)
    c = _filter_by_attr(c, 'group', group)
    result = []
    for x in c:
        y = deserialize_cluster_type_definition(x)
        logger.info(f'Deserialized {x} as {y}')
        result.append(y)
    return result


def save_cluster_type_to_settings(
                                  cluster_type,
                                  addon_name,
                                  group=None,
                                  ):
    """
    Saves cluster type to addon setting.
    """

    cluster_definition = cluster_type.serialize_this_cluster_type()
    cluster_definition = json.loads(cluster_definition)
    _save_cluster_type_definition_to_settings(
            cluster_definition, addon_name, group)


def _save_cluster_type_definition_to_settings(cluster, addon_name, group):
    """
    Saves cluster type definition to addon settings.
    """
    logger.info(f'Saving {cluster} to {addon_name} settings, group {group}')

    # Get clusters that are already in settings.
    c = _get_cluster_types_definitions_from_settings(addon_name)
    logger.debug(f'Found types: {c}')
    c = _filter_by_attr(c, 'group', group)
    cluster['group'] = group
    c = _replace_cluster_type(c, cluster)
    logger.debug(f'Types after adding cluster type: {c}')

    # Save to settings
    serialized_cluster_types = json.dumps(c)
    bpy.context.preferences.addons[
            addon_name].preferences.cluster_types = serialized_cluster_types


def _get_cluster_types_definitions_from_settings(addon_name):
    """
    Returns list of cluster type definitions from addon settings.
    """
    if not isinstance(addon_name, str):
        raise TypeError

    logger.debug(f'Trying to get clusters definitions for {addon_name}')

    if _WITH_BPY:
        c = bpy.context.preferences.addons[
                addon_name].preferences.cluster_types
        if c == '':
            c = []
            logger.error('No cluster types found in settings')
        else:
            c = json.loads(c)
            logger.debug(f'Found {c} in addon settings')
    else:
        raise TypeError
    if not isinstance(c, list):
        raise TypeError
    return c


# ===================
# Object cluster types
# ===================
# def get_cluster_types_from_object(obj, addon_name, prop=None, group=None,
#                                   *args, dont_add_prop=True):
#     """
#     Returns list of deserialized but not unwrapped
#     cluster types from addon settings.
#     """
#     if not isinstance(addon_name, str):
#         raise TypeError
#     if not isinstance(prop, str) and not isinstance(prop, int):
#         raise TypeError
#     if not isinstance(group, str) and not isinstance(group, int):
#         raise TypeError
# 
#     cluster_types = []
#     result = []
# 
#     for x in c:
#         cluster_types.append(deserialize_cluster_type(x))
#     for x in cluster_types:
#         if x['group'] == group:
#             result.append(x)
#     return result
# 
# 
# def get_cluster_types_from_object(obj, addon_name, prop=None, group=None,
#                                   *args, dont_add_prop=True):
#     if prop is None:
#         prop = 'cluster_types'
#     prop_name = f'{addon_name}{prop}'
#     try:
#         c = getattr(obj, prop_name)
#     except KeyError:
#         if not dont_add_prop:
#             setattr(obj, prop_name, json.dumps([]))
#         return []
# 
# def save_cluster_type_to_object(
#                                 obj,
#                                 deserialized_cluster_type_to_add,
#                                 addon_name,
#                                 group=None,
#                                 ):
#     """
#     Saves cluster type to object props.
#     """
#     if _WITH_BPY:
#         if not isinstance(obj, bpy.types.Object):
#             raise TypeError
#     else:
#         raise TypeError
#     if not isinstance(deserialized_cluster_type_to_add, str):
#         raise TypeError
#     if len(deserialized_cluster_type_to_add) == 0:
#         raise ValueError
#     if not isinstance(addon_name, str):
#         raise TypeError
#     if not isinstance(group, str) and not isinstance(group, None):
#         raise TypeError
# 
#     deserialized_cluster_types = get_cluster_types_from_object(
#             obj, addon_name, group, dont_add_prop=False)
# 
#     duplicates = []
# 
#     for x in deserialized_cluster_types:
#         if deserialized_cluster_type_to_add.cluster_name == x.cluster_name:
#             duplicates.append(x)
# 
#     for x in duplicates:
#         deserialized_cluster_types.remove(x)
# 
#     deserialized_cluster_types.append(
#             deserialized_cluster_type_to_add)
# 
#     serialized_cluster_types = json.dumps(
#             deserialized_cluster_types)
# 
#     setattr(obj, addon_name, serialized_cluster_types)
#     return


# TODO: remove type checks
# Utils
def _replace_cluster_type(cluster_types, cluster_type):
    if not isinstance(cluster_types, list):
        raise TypeError(f'Expected list, got {type(cluster_types)}')
    for x in cluster_types:
        if not isinstance(x, dict):
            raise TypeError(f'Expected dict, got {type(x)}')
    if not isinstance(cluster_type, dict):
        raise TypeError(f'Expected list, got {type(cluster_types)}')

    clusters = cluster_types[:]
    cluster = cluster_type
    remove = []
    for x in clusters:
        if x['name'] == cluster['name']\
                or x['type'] == cluster['type']:
            remove.append(x)
    if len(remove) > 1:
        raise ValueError
    else:
        for x in remove:
            clusters.remove(x)
        clusters.append(cluster)
    return clusters


def _filter_by_attr(cluster_types, attr_name, value):
    if not isinstance(cluster_types, list):
        raise TypeError(f'Expected list, got {type(cluster_types)}')
    for x in cluster_types:
        if not isinstance(x, dict):
            raise TypeError(f'Expected dict, got {type(x)}')
    if not isinstance(attr_name, str):
        raise TypeError(f'Expected str, got {type(attr_name)}')

    result = []
    for x in cluster_types:
        if x[attr_name] == value:
            result.append(x)
    return result
