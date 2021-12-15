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


def deserialize_cluster_type(serialized_cluster_type, **kwargs):
    """
    Takes string with info about cluster type as argument.

    Returns cluster type instance.
    """
    x = json.loads(serialized_cluster_type)
    if x[0] == 'ModifiersCluster':
        result = ModifiersCluster(
                                  cluster_name=x[1],
                                  cluster_type=x[2],
                                  modifiers_by_type=x[3],
                                  modifiers_by_name=x[4],
                                  cluster_tags=x[5],
                                  cluster_priority=x[6],
                                  cluster_is_sane=x[7],
                                  cluster_createable=x[8],
                                  dont_define_cluster=False,
                                  **kwargs
                                  )
    else:
        raise TypeError
    return result


def serialize_cluster_type(cluster_type):
    """
    Returns string with info about cluster_type that
    is enough to create new cluster_type instance
    through deserialize_cluster_type.
    """
    if not isinstance(cluster_type, ModifiersCluster):
        raise TypeError
    return cluster_type.serialize_this_cluster_type()
