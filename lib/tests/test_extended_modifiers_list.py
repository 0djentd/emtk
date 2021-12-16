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
from lib.clusters.cluster import ClusterTrait


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

    def test_first_cluster_name(self):
        c = self.e.get_deep_list()[0]
        self.assertEqual(c.name, c.get_first().name)

    def test_last_cluster_name(self):
        c = self.e.get_deep_list()[-1]
        self.assertEqual(c.name, c.get_last().name)

    def test_first_cluster_type(self):
        c = self.e.get_deep_list()[0]
        self.assertEqual(c.type, c.get_first().type)

    def test_last_cluster_type(self):
        c = self.e.get_deep_list()[-1]
        self.assertEqual(c.type, c.get_last().type)

    def test_all_clusters_initialized(self):
        result = True
        for x in self.e.get_full_list():
            if not x._modcluster_initialized:
                if not isinstance(result, list):
                    result = []
                result.append(x)
        self.assertTrue(result)

    def test_all_clusters_have_modifiers(self):
        result = True
        for x in self.e.get_full_list():
            if len(x._modifiers_list) == 0:
                if not isinstance(result, list):
                    result = []
                result.append(x)
        self.assertTrue(result)

    def test_duplicate_cluster_names(self):
        result = True
        names = []
        for x in self.e.get_full_list():
            if x.name not in names:
                names.append(x.name)
            else:
                if not isinstance(result, list):
                    result = []
                result.append(x)
        self.assertTrue(result)

    def test_duplicate_clusters(self):
        result = True
        for x in self.e.get_full_list():
            i = 0
            for y in self.e.get_full_list():
                if y is x:
                    i += 1
        if i != 1:
            result = False
        self.assertTrue(result)

    def test_duplicate_modifiers(self):
        result = False
        for x in self.e.get_full_actual_modifiers_list():
            i = 0
            for y in self.e.get_full_actual_modifiers_list():
                if y is x:
                    i += 1
                    if i != 1:
                        if not isinstance(result, list):
                            result = []
                        result.append(x)
        self.assertFalse(result)

    def test_all_clusters_is_clusters(self):
        result = True
        for x in self.e.get_full_list():
            if not isinstance(x, ClusterTrait):
                if not isinstance(result, list):
                    result = []
                result.append(x)
        self.assertTrue(result)

    def test_all_clusters_have_object(self):
        result = True
        for x in self.e.get_full_list():
            if x._object is None:
                if not isinstance(result, list):
                    result = []
                result.append(x)
        self.assertTrue(result)

    def test_all_clusters_have_active_modifier(self):
        result = False
        for x in self.e.get_clusters_clusters_list():
            if x._mod is None:
                if not isinstance(result, list):
                    result = []
                result.append(x)
        self.assertFalse(result)

    def test_all_clusters_are_sane(self):
        result = False
        for x in self.e.get_full_list():
            if not x.check_this_cluster_sanity():
                if not isinstance(result, list):
                    result = []
                result.append(x)
        self.assertFalse(result)

    def test_actual_modifiers_count(self):
        self.assertEqual(len(self.e.get_full_actual_modifiers_list()),
                         len(self.o.modifiers))

    def test_actual_modifiers_types(self):
        result = False
        for x, y in zip(self.e.get_full_actual_modifiers_list(),
                        self.o.modifiers):
            if x.type != y.type:
                if not isinstance(result, list):
                    result = []
                result.append(x)
        self.assertFalse(result)

    def test_actual_modifiers_names(self):
        result = False
        for x, y in zip(self.e.get_full_actual_modifiers_list(),
                        self.o.modifiers):
            if x.name != y.name:
                if not isinstance(result, list):
                    result = []
                result.append(x)
        self.assertFalse(result)

    def test_active_modifier_is_in_the_list(self):
        self.assertTrue(self.e.has_cluster(self.e.active_modifier_get()))

    def test_clusters_active_modifier_is_in_the_list(self):
        result = False
        for x in self.e.get_clusters_clusters_list():
            if not self.e.has_cluster(self.e.active_modifier_get()):
                if not isinstance(result, list):
                    result = []
                result.append(x)
        self.assertFalse(result)
