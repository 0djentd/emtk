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

from ..utils import get_attr_or_iter_from_str_nested
from ..utils import set_attr_or_iter_from_str_nested
from ..utils import get_last_attr_name_in_sequence
from ..utils import get_attr_obj_str


class Modifier():
    def __init__(self):
        self.dictionary = {'name': 'Bevel'}
        self.nested_dictionary = {'modifier':
                                  {'name': 'Bevel',
                                   'type': 'BEVEL'}}
        self.array = [234, 234234, 23412345]
        self.integer = 123
        self.string = 'BEVEL'


class Cluster():
    def mod(self, val):
        if val != 321:
            raise ValueError
        return self.modifier

    def __init__(self):
        self.modifier = Modifier()


class WorkaroundScriptTests(unittest.TestCase):
    check = True
    fast = False

    def setUp(self):
        self.cluster = Cluster()

    def tearDown(self):
        del(self.cluster)

    def test_integer(self):
        attr_str = 'modifier.integer'
        attr = self.cluster.modifier.integer
        attr_2 = get_attr_or_iter_from_str_nested(
            self.cluster, attr_str, check=self.check, fast=self.fast)
        self.assertEqual(attr, attr_2)

    def test_string(self):
        attr_str = 'modifier.string'
        attr = self.cluster.modifier.string
        attr_2 = get_attr_or_iter_from_str_nested(
            self.cluster, attr_str, check=self.check, fast=self.fast)
        self.assertEqual(attr, attr_2)

    def test_dictionary(self):
        attr_str = 'modifier.dictionary'
        attr = self.cluster.modifier.dictionary
        attr_2 = get_attr_or_iter_from_str_nested(
            self.cluster, attr_str, check=self.check, fast=self.fast)
        self.assertEqual(attr, attr_2)

    def test_dictionary_element_1(self):
        attr_str = "modifier.dictionary['name']"
        attr = self.cluster.modifier.dictionary['name']
        attr_2 = get_attr_or_iter_from_str_nested(
            self.cluster, attr_str, check=self.check, fast=self.fast)
        self.assertEqual(attr, attr_2)

    def test_dictionary_element_2(self):
        attr_str = 'modifier.dictionary["name"]'
        attr = self.cluster.modifier.dictionary["name"]
        attr_2 = get_attr_or_iter_from_str_nested(
            self.cluster, attr_str, check=self.check, fast=self.fast)
        self.assertEqual(attr, attr_2)

    def test_dictionary_element_3(self):
        attr_str = 'modifier.dictionary[\'name\']'
        attr = self.cluster.modifier.dictionary['name']
        attr_2 = get_attr_or_iter_from_str_nested(
            self.cluster, attr_str, check=self.check, fast=self.fast)
        self.assertEqual(attr, attr_2)

    def test_list_element_1(self):
        attr_str = 'modifier.array[1]'
        attr = self.cluster.modifier.array[1]
        attr_2 = get_attr_or_iter_from_str_nested(
            self.cluster, attr_str, check=self.check, fast=self.fast)
        self.assertEqual(attr, attr_2)

    def test_nested_dictionary_element_1(self):
        attr_str = "modifier.nested_dictionary['modifier']['name']"
        attr = self.cluster.modifier.nested_dictionary['modifier']['name']
        attr_2 = get_attr_or_iter_from_str_nested(
            self.cluster, attr_str, check=self.check, fast=self.fast)
        self.assertEqual(attr, attr_2)

    # SET ATTR
    def test_set_integer(self):
        attr_str = 'modifier.integer'
        attr = self.cluster.modifier.integer
        new_value = 123
        set_attr_or_iter_from_str_nested(self.cluster, attr_str, new_value,
                                         check=self.check, fast=self.fast)
        self.assertEqual(attr, new_value)

    def test_set_string(self):
        attr_str = 'modifier.string'
        new_value = 'asdffdsafdsfsd'
        set_attr_or_iter_from_str_nested(self.cluster, attr_str, new_value,
                                         check=self.check, fast=self.fast)
        self.assertEqual(self.cluster.modifier.string, new_value)

    # def test_dictionary(self):
    #     attr_str = 'modifier.dictionary'
    #     attr = self.cluster.modifier.dictionary
    #     attr_2 = get_attr_or_iter_from_str_nested(
    #             self.cluster, attr_str, check=self.check, fast=self.fast)
    #     self.assertEqual(attr, attr_2)

    # def test_dictionary_element_1(self):
    #     attr_str = "modifier.dictionary['name']"
    #     attr = self.cluster.modifier.dictionary['name']
    #     attr_2 = get_attr_or_iter_from_str_nested(
    #             self.cluster, attr_str, check=self.check, fast=self.fast)
    #     self.assertEqual(attr, attr_2)

    # def test_dictionary_element_2(self):
    #     attr_str = 'modifier.dictionary["name"]'
    #     attr = self.cluster.modifier.dictionary["name"]
    #     attr_2 = get_attr_or_iter_from_str_nested(
    #             self.cluster, attr_str, check=self.check, fast=self.fast)
    #     self.assertEqual(attr, attr_2)

    # def test_dictionary_element_3(self):
    #     attr_str = 'modifier.dictionary[\'name\']'
    #     attr = self.cluster.modifier.dictionary['name']
    #     attr_2 = get_attr_or_iter_from_str_nested(
    #             self.cluster, attr_str, check=self.check, fast=self.fast)
    #     self.assertEqual(attr, attr_2)

    # def test_list_element_1(self):
    #     attr_str = 'modifier.array[1]'
    #     attr = self.cluster.modifier.array[1]
    #     attr_2 = get_attr_or_iter_from_str_nested(
    #             self.cluster, attr_str, check=self.check, fast=self.fast)
    #     self.assertEqual(attr, attr_2)

    # def test_nested_dictionary_element_1(self):
    #     attr_str = "modifier.nested_dictionary['modifier']['name']"
    #     attr = self.cluster.modifier.nested_dictionary['modifier']['name']
    #     attr_2 = get_attr_or_iter_from_str_nested(
    #             self.cluster, attr_str, check=self.check, fast=self.fast)
    #     self.assertEqual(attr, attr_2)


class WorkaroundScriptTests_fast(WorkaroundScriptTests):
    fast = True


class WorkaroundScriptTests_no_check(WorkaroundScriptTests):
    check = False


class WorkaroundScriptTests_fast_no_check(WorkaroundScriptTests_fast):
    check = False


class SequenceParserFunctionsTests(unittest.TestCase):
    def test_get_last_attr_name_in_sequence(self):
        result_1 = get_last_attr_name_in_sequence('cluster.name')
        result_2 = 'name'
        self.assertEqual(result_1, result_2)

    def test_get_last_attr_name_in_sequence_2(self):
        result_1 = get_last_attr_name_in_sequence('modifiers[1].type')
        result_2 = 'type'
        self.assertEqual(result_1, result_2)

    def test_get_last_attr_name_in_sequence_3(self):
        result_1 = get_last_attr_name_in_sequence(
            'cluster.modifiers[\'Bevel\'].type')
        result_2 = 'type'
        self.assertEqual(result_1, result_2)

    def test_get_attr_obj_str(self):
        result_1 = get_attr_obj_str('cluster.name')
        result_2 = 'cluster'
        self.assertEqual(result_1, result_2)

    def test_get_attr_obj_str_2(self):
        result_1 = get_attr_obj_str('modifiers[1].type')
        result_2 = 'modifiers[1]'
        self.assertEqual(result_1, result_2)

    def test_get_attr_obj_str_3(self):
        result_1 = get_attr_obj_str(
            'cluster.modifiers[\'Bevel\'].type')
        result_2 = 'cluster.modifiers[\'Bevel\']'
        self.assertEqual(result_1, result_2)
