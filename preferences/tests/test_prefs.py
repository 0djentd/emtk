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

from ..shortcuts import generate_new_shortcut
from ..shortcuts import _get_next_letter_in_shortcut_name


class UtilsTests(unittest.TestCase):

    def test_generate_new_shortcut(self):
        props_names = [
                       'angle_limit',
                       'array',
                       'segments']
        result = {}
        for x in props_names:
            result.update(generate_new_shortcut(x, result))

        result_expected = {'angle_limit': {'letter': 'A',
                                           'shift': False,
                                           'ctrl': False,
                                           'alt': False},

                           'array': {'letter': 'A',
                                     'shift': True,
                                     'ctrl': False,
                                     'alt': False},

                           'segments': {'letter': 'S',
                                        'shift': False,
                                        'ctrl': False,
                                        'alt': False}}

        self.assertEqual(result, result_expected)

    def test_get_next_letter_in_name(self):
        shortcut_name = 'angle_limit'
        index = None

        index, letter = _get_next_letter_in_shortcut_name(shortcut_name, index)

        result = (index, letter)
        result_expected = (0, 'A')

        self.assertEqual(result, result_expected)

    def test_get_next_letter_in_name_2(self):
        shortcut_name = 'angle_limit'
        index = 0

        index, letter = _get_next_letter_in_shortcut_name(shortcut_name, index)

        result = (index, letter)
        result_expected = (1, 'N')

        self.assertEqual(result, result_expected)

    def test_get_next_letter_in_name_3(self):
        shortcut_name = 'angle_limit'
        index = 10

        with self.assertRaises(ValueError):
            index, letter = _get_next_letter_in_shortcut_name(
                    shortcut_name, index)
