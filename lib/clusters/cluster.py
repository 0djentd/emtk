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

from .cluster_trait import ClusterTrait
from ..lists.modifiers_list import ModifiersList


class Cluster(ClusterTrait, ModifiersList):
    """
    Simple cluster type.

    What is Cluster?
    It is a representation of any number of modifiers or clusters, that can
    have its own custom modifier type (when used with ModifiersList), methods,
    and attributes.
    Method check_availability decides if modifiers can be considered as
    a modifier cluster.
    Instance of ModifiersCluster can be indexed, moved, selected as active
    modifier, sorted and saved in ClustersList.

    Examples:
    Modifier cluster, consisting of wireframe modifier and bevel with custom
    name. If one of conditions (type, name or position in stack) is false,
    check_availability will return false. Else, this two modifiers can be
    set as modifiers in ModifiersCluster instance.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
