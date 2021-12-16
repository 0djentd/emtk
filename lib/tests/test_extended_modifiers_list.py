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
from lib.lists.extended_modifiers_list import ExtendedModifiersList
from lib.dummy_modifiers import DummyBlenderObj


class ExtendedModifiersListTests(unittest.TestCase):
    def setUp(self):
        self.o = DummyBlenderObj()
        mods = []
        mods.append(self.o.modifier_add('Bevel', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel', 'BEVEL'))

        self.e = ExtendedModifiersList(self.o)
        self.e.create_modifiers_list(self.o)

    def tearDown(self):
        del(self.o)
        del(self.e)

    def test_create_modifiers_list(self):
        c = self.e.get_first()
        result = (self.e.get_list_length() == 3)\
            and (c.get_list_length() == 1)\
            and (c.has_clusters() is False)
        self.assertTrue(result)

    def test_create_modifiers_list_first_name(self):
        c = self.e.get_first()
        self.assertEqual(c.name, c.get_first().name)

    def test_create_modifiers_list_last_name(self):
        c = self.e.get_last()
        self.assertEqual(c.name, c.get_last().name)
