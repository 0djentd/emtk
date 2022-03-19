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

import unittest
from libs.emtk.dummy_modifiers import DummyBlenderObj


class DummyModifiersTests(unittest.TestCase):
    def setUp(self):
        self.o = DummyBlenderObj()
        self.o.modifier_add('Bevel', 'BEVEL')
        self.o.modifier_add('bevel', 'BOOLEAN')
        self.o.modifier_add('b', 'BEVEL')
        self.o.modifier_add('Bevel2', 'ARRAY')
        self.o.modifier_add('Bevel1', 'BEVEL')
        self.o_len = len(self.o.modifiers)

    def teatDown(self):
        del(self.o)

    def test_modifier_add(self):
        x = self.o.modifier_add('Bevel', 'BEVEL')
        self.assertEqual(self.o.modifiers[self.o_len], x)

    def test_modifier_remove(self):
        x = self.o.modifier_add('Bevel', 'BEVEL')
        self.o.modifier_remove(x.name)
        self.assertEqual(len(self.o.modifiers), self.o_len)

    def test_duplicate_modifiers(self):
        result = True
        y = []
        for x in self.o.modifiers:
            if x.name not in y:
                y.append(x.name)
            else:
                result = False
        self.assertTrue(result)
