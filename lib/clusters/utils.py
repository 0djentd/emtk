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
