# ##### BEGIN GPL LICENSE BLOCK #####
#
# Copyright 2022, Sergey Shapochkin
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
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

    def get_modifiers_for_instantiation(self):
        """
        Returns list of names and types of modifiers
        that are required to create this cluster.
        Returns None, if cluster cant be created.
        """
        if not self._cluster_definition['createable']:
            return None

        modifiers = []
        for x, y in zip(self._cluster_definition['by_name'],
                        self._cluster_definition['by_type']):
            if x != 'ANY' or y == 'ANY':
                return None
            modifiers.append(x, y)
        return modifiers
