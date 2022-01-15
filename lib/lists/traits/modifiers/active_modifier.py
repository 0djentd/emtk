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

from ...utils import check_if_removed, check_obj_ref


class ActiveModifierTrait():
    """
    Active modifier for ModifiersList.
    """

    # Active_modifier doesnt neccessary means that this is an actual modifier.
    # It mostly used for clusters, as every modifier is a cluster anyways.
    # TODO: add modifiers selection

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Active modifier
        self._mod = None

    @property
    @check_if_removed
    def active(self):
        if self._mod is None:
            if len(self._modifiers_list) != 0:
                return self._modifiers_list[0]
        return self._mod

    @active.setter
    @check_if_removed
    def active(self, mod):
        if type(mod) is int:
            self._mod = self._modifiers_list[mod]
        else:
            if mod not in self._modifiers_list:
                raise ValueError
            self._mod = mod
