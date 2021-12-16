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
from lib.dummy_modifiers import DummyBlenderModifier, DummyBlenderObj


class DummyModifiersTests(unittest.TestCase):
    def setUp(self):
        self.o = DummyBlenderObj()

    def teatDown(self):
        del(self.o)

    def test_modifier_add(self):
        x = self.o.modifier_add('Bevel', 'BEVEL')
        self.assertEqual(self.o.modifiers[0], x)

    def test_modifier_remove(self):
        x = self.o.modifier_add('Bevel', 'BEVEL')
        self.o.modifier_remove(x.name)
        self.assertEqual(len(self.o.modifiers), 0)
