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

from ..object_state import ModifierState, ListObjectState


try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    _WITH_BPY = False


class ModifierStateClassTests(unittest.TestCase):
    def setUp(self):
        self.obj = ModifierState(
                name='modifier preset',
                data={'angle_limit': 123}, tags=['STORED'])

    def tearDown(self):
        del self.obj

    def test_object_data_item(self):
        self.assertEqual(self.obj['angle_limit'], 123)

    def test_object_name(self):
        self.assertEqual(self.obj.name, 'modifier preset')

    def test_object_tags(self):
        self.assertEqual(self.obj.tags, ['STORED'])


class ModifierStateClassSerializationTests(ModifierStateClassTests):
    def setUp(self):
        super().setUp()
        self.s = self.obj.serialize()
        self.obj = ModifierState.deserialize(self.s)

    def tearDown(self):
        super().tearDown()
        del self.s


class ListObjectStateClassTests(unittest.TestCase):
    def setUp(self):
        self.obj = None
