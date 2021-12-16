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

from ....dummy_modifiers import DummyBlenderModifier, DummyBlenderObj


class DummyModifiersClustersListTrait():
    """
    Methods for creating dummy modifiers list.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dummy_blender_object = DummyBlenderObj()
        self._dummy_modifiers_list = []
        self._real_modifiers_list = self._modifiers_list

    def duplicate_modifiers_list_to_dummy(self, *, replace=False):
        dummy_clusters_list = copy.deepcopy(self._modifiers_list)
        dummy_mods = []

        y = []
        for x in dummy_clusters_list:
            if x.has_clusters:
                y += x.get_deep_list()
            else:
                y.append(x)

        for x in y:
            x._real_blender_object = x._object
            x._dummy_blender_object = self._dummy_blender_object

            mods = copy.copy(x.get_list())
            x._real_modifiers_list = x._modifiers_list
            x._dummy_modifiers_list = []

            for mod in mods:
                dummy_mod = DummyBlenderModifier(mod.name, mod.type)
                dummy_mods.append(dummy_mod)
                x._dummy_modifiers_list.append(dummy_mod)

        self._dummy_object.set_modifiers(dummy_mods)

        self._real_modifiers_list = copy.copy(self._modifiers_list)
        self._dummy_modifiers_list = dummy_clusters_list

    def switch_to_real_modifiers_list(self):
        self._modifiers_list = self._real_modifiers_list
        self._object = self._real_blender_object
        for x in self.get_full_list():
            x._modifiers_list = x._real_modifiers_list
            x._object = x._real_blender_object

    def switch_to_dummy_modifiers_list(self):
        self._modifiers_list = self._dummy_modifiers_list
        self._object = self._dummy_blender_object
        for x in self.get_full_list():
            x._modifiers_list = x._dummy_modifiers_list
            self._object = self._dummy_blender_object
