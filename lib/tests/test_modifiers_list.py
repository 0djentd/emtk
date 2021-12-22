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

import unittest
from lib.lists.modifiers_list import ModifiersList
from lib.dummy_modifiers import DummyBlenderObj


class ModifiersListTests(unittest.TestCase):
    def setUp(self):
        self.o = DummyBlenderObj()
        mods = []
        mods.append(self.o.modifier_add('Bevel', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel', 'BEVEL'))

        self.m_list = ModifiersList(no_obj=True)
        self.m_list._modifiers_list = mods

    def teatDown(self):
        del(self.o)
        del(self.m_list)

    def test_get_last(self):
        self.assertEqual(self.m_list.get_last(), self.o.modifiers[-1])

    def test_get_first(self):
        self.assertEqual(self.m_list.get_first(), self.o.modifiers[0])

    def test_get_list_in_range_inclusive(self):
        mod1 = self.m_list.get_first()
        mod2 = self.m_list.get_last()
        self.assertEqual(self.m_list.get_list_in_range_inclusive(
            mod1, mod2), self.m_list._modifiers_list)

    def test_get_list_in_range_not_inclusive(self):
        mod1 = self.m_list.get_first()
        mod2 = self.m_list.get_last()
        self.assertEqual(self.m_list.get_list_in_range_not_inclusive(
            mod1, mod2), self.m_list._modifiers_list[1:2])
