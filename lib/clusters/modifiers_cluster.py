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

import copy

from .cluster_trait import ClusterTrait

from ..lists.modifiers_list import ModifiersList
from ..lists.traits.modifiers.active_modifier \
        import ActiveModifierTrait


class ModifiersCluster(
                       ClusterTrait,
                       ActiveModifierTrait,
                       ModifiersList
                       ):
    """
    Base class for modifiers cluster type
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def modifiers(self):
        return copy.copy(self._modifiers_list)
