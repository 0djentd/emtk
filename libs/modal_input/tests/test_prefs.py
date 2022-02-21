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
import copy
import time

from ..shortcuts import ModalShortcut
from ..shortcuts import ModalShortcutsGroup
from ..shortcuts import ModalShortcutsCache
from ..shortcuts import generate_new_shortcut
from ..shortcuts import _get_next_letter_in_shortcut_name
from ..shortcuts import method_cache


class UtilsTests(unittest.TestCase):

    def test_generate_new_shortcut(self):
        props_names = ['angle_limit',
                       'array',
                       'segments']
        result = []
        for x in props_names:
            result.append(generate_new_shortcut(x, result))

        result = result[1]
        result_expected = ModalShortcut('array', 'A', True, False, False)
        f = True
        for x in {'event_type', 'shift', 'ctrl', 'alt', 'shortcut_id'}:
            if getattr(result, x) != getattr(result_expected, x):
                f = False
        self.assertTrue(f)

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


example_1_args = ['angle', 'A', True, False, False]
example_2_args = ['width', 'W', False, True, False]


class ShortcutsTests(unittest.TestCase):

    def setUp(self):
        self.shortcut = ModalShortcut(*example_1_args)

    def tearDown(self):
        del self.shortcut

    def test_new_shortcut(self):
        shortcut = self.shortcut
        result = True
        if shortcut.shortcut_id != 'angle':
            result = False
        if shortcut.event_type != 'A':
            result = False
        if shortcut.shift is not True:
            result = False
        if shortcut.ctrl is True:
            result = False
        if shortcut.alt is True:
            result = False
        self.assertEqual(result, True)

    def test_new_shortcut_fail(self):
        args = ['angle', 'A', True, False, False]
        values = [123, 123.456, {}, []]
        for i, x in enumerate(args):
            with self.subTest():
                for y in values:
                    new_args = copy.copy(args)
                    new_args[i] = y
                    with self.assertRaises(TypeError):
                        ModalShortcut(*new_args)

    def test_cache_clear(self):
        self.assertEqual(self.shortcut.cache_clear(), None)


class Event():
    type = 'A'
    shift = True
    ctrl = False
    alt = False


class ShortcutsGroupTest(unittest.TestCase):
    def setUp(self):
        self.shortcuts = [ModalShortcut(*example_1_args),
                          ModalShortcut(*example_2_args)]
        self.group = ModalShortcutsGroup('BEVEL', self.shortcuts)

    def tearDown(self):
        del self.shortcuts
        del self.group

    def test_new_shortcuts_group_length(self):
        self.assertEqual(len(self.group), 2)

    def test_new_shortcuts_group_value(self):
        self.assertEqual(self.group.value, 'BEVEL')

    def test_new_shortcuts_group_refresh_is_false(self):
        self.assertEqual(self.group.tag_refresh, False)

    def test_new_shortcuts_group_shortcuts_equals(self):
        for i, x in enumerate(self.shortcuts):
            with self.subTest():
                self.assertEqual(x, self.group[x.shortcut_id])

    def test_find_by_shortcut_id(self):
        self.assertEqual(self.group.find_by_shortcut_id('angle'),
                         self.shortcuts[0])

    def test_find_by_mapping(self):
        self.assertEqual(self.group.find_by_mapping('A', True, False, False),
                         self.shortcuts[0])

    def test_find_by_event(self):
        e = Event()
        self.assertEqual(self.group.find_by_event(e),
                         self.group['angle'])

    def test_cache_clear(self):
        self.assertEqual(self.group.cache_clear(), None)


class ShortcutsCacheTests(unittest.TestCase):

    def setUp(self):
        self.cache = ModalShortcutsCache()
        self.groups = [ModalShortcutsGroup('BEVEL'),
                       ModalShortcutsGroup('ARRAY')]

    def tearDown(self):
        del self.cache
        del self.groups

    def test_new_shortcuts_cache(self):
        self.assertEqual(len(self.cache.shortcuts_groups), 0)

    def test_new_shortcuts_cache_groups(self):
        for x in self.groups:
            self.cache.update(x)
        self.assertEqual(self.cache.shortcuts_groups, self.groups)


class MethodsCacheTests(unittest.TestCase):

    @method_cache
    def method_example(self, val):
        pow(val, val)

    def test_iter_err(self):
        with self.assertRaises(ValueError):
            for x in range(10):
                for x in range(150):
                    self.method_example(x)
