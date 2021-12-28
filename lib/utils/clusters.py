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
import copy

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


# TODO: Save cluster definitions serialized list of serialized dicts.
# This will allow to skip dict if it raises any errors.
# TODO: remove type checks for release

# ========
# WRAPPERS
# ========


# SETTINGS
# def get_cluster_types_from_settings(addon_name, group=None):
#     """Returns list of cluster types from addon settings."""
#     c = get_cluster_types_definitions_from_settings(addon_name)
#     if group is not None:
#         c = _filter_by_attr(c, 'group', group)
#     return instantiate_cluster_types_from_definitions(c)
#
#
# def save_cluster_type_to_settings(
#         cluster_type, addon_name, group=None):
#     """Save cluster type to addon setting."""
#     d = cluster_type.get_this_cluster_definition()
#     save_cluster_type_definition_to_settings(
#             d, addon_name, group)
#
#
# def remove_cluster_type_from_settings(
#         cluster_type, addon_name, group=None):
#     """Removes cluster type from settings."""
#     t = cluster_type.get_this_cluster_definition()
#     remove_cluster_type_definition_from_settings(t, addon_name, group)
#
#
# # OBJECT
# def get_cluster_types_from_obj(
#         obj, addon_name, group=None, dont_add_prop=False):
#     """Returns list of cluster types definitions from obj.
#     Obj can be object, scene, or view layer."""
#     t = get_cluster_types_definitions_from_obj(
#             obj, addon_name, dont_add_prop)
#     if group is not None:
#         t = _filter_by_attr(t, 'group', group)
#     return instantiate_cluster_types_from_definitions(t)
#
#
# def save_cluster_type_to_obj(
#         obj, cluster_type, addon_name, group=None, dont_add_prop=False):
#     """Saves cluster type to obj prop"""
#     d = cluster_type.get_this_cluster_definition()
#     save_cluster_type_definition_to_obj(
#             obj, d, addon_name, group, dont_add_prop=False)
#
#
# def remove_cluster_type_from_obj(
#         obj, cluster_type, addon_name, group=None):
#     """Removes cluster type from settings."""
#     t = cluster_type.get_this_cluster_definition()
#     remove_cluster_type_definition_from_obj(obj, t, addon_name, group)


# ==========================
# Cluster types from settings
# ==========================
def get_cluster_types_definitions_from_settings(addon_name, group=None):
    if not isinstance(addon_name, str):
        raise TypeError

    c = bpy.context.preferences.addons[
            addon_name].preferences.cluster_types
    c = json.loads(c)

    # Check list
    if not isinstance(c, list):
        raise TypeError
    for x in c:
        if not isinstance(x, dict):
            raise TypeError

    if group is not None:
        c = _filter_by_attr(c, 'group', group)
    return c


def save_cluster_type_definition_to_settings(
        cluster, addon_name, group=None):
    if not isinstance(cluster, dict):
        raise TypeError
    if not isinstance(addon_name, str):
        raise TypeError
    if not isinstance(group, str) and group is not None:
        raise TypeError

    # load
    c = get_cluster_types_definitions_from_settings(addon_name, group)

    # and add group to definition.
    if group is not None:
        cluster['group'] = group
    else:
        cluster['group'] = 'ANY'

    # add new def
    c = _add_replace_cluster_type(c, cluster)

    # write
    c = json.dumps(c)
    bpy.context.preferences.addons[
            addon_name].preferences.cluster_types = c


def remove_cluster_type_definition_from_settings(
        cluster, addon_name, group=None):
    if not isinstance(cluster, dict):
        raise TypeError
    if not isinstance(addon_name, str):
        raise TypeError
    if not isinstance(group, str) and group is not None:
        raise TypeError

    t = get_cluster_types_definitions_from_settings(addon_name, group)
    t = _remove_cluster_type(t, cluster)
    bpy.context.preferences.addons[addon_name].preferences.cluster_types = t


# ===================
# Object cluster types
# ===================
def get_cluster_types_definitions_from_obj(
        obj, addon_name, dont_add_prop=False):
    if obj is None:
        raise TypeError
    if not isinstance(addon_name, str):
        raise TypeError
    try:
        t = obj[addon_name]
    except KeyError:
        if not dont_add_prop:
            obj[addon_name] = '[]'
            t = obj[addon_name]
        else:
            raise KeyError
    return t


# def save_cluster_type_definition_to_obj(
#         obj, addon_name, dont_add_prop=False):
#     return


# =======
# Utils
# =======
def _add_replace_cluster_type(definitions, cluster_type):
    """
    Adds cluster type definition to list of definitions.
    Replaces existing one with same name and type.
    """
    if not isinstance(definitions, list):
        raise TypeError(f'Expected list, got {type(definitions)}')
    for x in definitions:
        if not isinstance(x, dict):
            raise TypeError(f'Expected dict, got {type(x)}')
    if not isinstance(cluster_type, dict):
        raise TypeError(f'Expected list, got {type(definitions)}')

    c = copy.copy(definitions)
    cluster = cluster_type
    remove = []
    for x in c:
        if x['name'] == cluster['name']\
                and x['type'] == cluster['type']\
                and x['cluster_trait_subclass']\
                == cluster['cluster_trait_subclass']:
            remove.append(x)
    for x in remove:
        c.remove(x)

    c.append(cluster)
    return c


def _remove_cluster_type(definitions, cluster_type):
    if not isinstance(definitions, list):
        raise TypeError(f'Expected list, got {type(definitions)}')
    for x in definitions:
        if not isinstance(x, dict):
            raise TypeError(f'Expected dict, got {type(x)}')
    if not isinstance(cluster_type, dict):
        raise TypeError(f'Expected dict, got {type(cluster_type)}')
    remove = []
    for x in definitions:
        if x == cluster_type:
            remove.append(x)
    for x in remove:
        definitions.remove(x)
    return definitions


def _filter_by_attr(definitions, attr_name, value):
    if not isinstance(definitions, list):
        raise TypeError(f'Expected list, got {type(definitions)}')
    for x in definitions:
        if not isinstance(x, dict):
            raise TypeError(f'Expected dict, got {type(x)}')
    if not isinstance(attr_name, str):
        raise TypeError(f'Expected str, got {type(attr_name)}')

    result = []
    for x in definitions:
        if x[attr_name] == value:
            result.append(x)
    return result


def instantiate_cluster_types_from_definitions(cluster_types_definitions):
    if not isinstance(cluster_types_definitions, list):
        raise TypeError
    result = []
    for x in cluster_types_definitions:
        if not isinstance(x, dict):
            raise TypeError
        result.append(deserialize_cluster_type_definition(x))
    return result


# =========================
# instantiated cluster type
# =========================
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
