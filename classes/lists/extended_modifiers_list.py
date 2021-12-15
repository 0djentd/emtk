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

from .traits.first_layer_clusters_list import FirstLayerClustersListTrait
from .clusters_list import ClustersList


class ExtendedModifiersList(
                            FirstLayerClustersListTrait,
                            ClustersList
                            ):
    """
    List of object modifiers with 'active modifier' that can be useful
    in modal operators.

    Can have only one active modifier at the time.
    Cant have no active modifier, if any modifier exists.
    Active modifier can be set with index, name, or reference.

    Can work with modifiers cluster lists as well.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
