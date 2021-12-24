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

# import copy
import json
from .modifiers_cluster import ModifiersCluster
from .clusters_layer import ClustersLayer
from .cluster_trait import ClusterTrait


def deserialize_cluster_type(serialized_cluster_type, *args, **kwargs):
    """
    Takes string with info about cluster type as argument.

    Returns cluster type instance.
    """
    x = json.loads(serialized_cluster_type)

    if not isinstance(x, dict):
        t = type(serialized_cluster_type)
        raise TypeError(f'Serialized cluster type should be dict, not {t}')

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
        raise TypeError
    return cluster_type.serialize_this_cluster_type()


def get_types_from_object_props(self, obj, addon_name, prop_name):
    """
    Returns cluster types from object prop.
    """
    return


def get_types_from_scene_prop(self, obj, addon_name, prop_name):
    """
    Returns cluster types from scene prop.
    """
    return


def get_types_from_addon_prefs(self, obj, addon_name, prop_name):
    """
    Returns cluster types from addon prefs.
    """
    return
