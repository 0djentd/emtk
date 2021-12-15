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

from .clusters_list import ClustersList
from .traits.object_clusters_list import ObjectClustersListTrait

# Modifiers List utils
# Modifiers List
# Modifiers Clusters parser
# Modifiers Clusters List
# ----------------------
# Object Modifiers Clusters List
# ----------------------


class ObjectModifiersClustersList(
                                  ObjectClustersListTrait,
                                  ClustersList
                                  ):
    """
    ModfifiersClustersList of an object.

    Any ModifiersClustersList that can somehow use Blender modifiers
    stack using it.

    Have methods for adding, removing, moving and sorting modifiers
    within Blender modifiers stack.

    create_modifiers_list parses and populates modifiers list.
    """

    # Reference to object.
    # _object

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
