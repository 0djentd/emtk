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
from lib.clusters.modifiers_cluster import ModifiersCluster
from lib.clusters.clusters_layer import ClustersLayer


class ExtendedModifiersListTests():
    def setUp(self):
        self.o = DummyBlenderObj()
        mods = []
        mods.append(self.o.modifier_add('Bevel', 'BEVEL'))
        self.e = ExtendedModifiersList(self.o)

    def tearDown(self):
        del(self.o)
        del(self.e)

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
        result = False
        i = 0
        for x in self.e.get_full_list():
            i = 0
            for y in self.e.get_full_list():
                if y is x:
                    i += 1
                    if i != 1:
                        if not isinstance(result, list):
                            result = []
                        result.append(x)
        self.assertFalse(result)

    def test_duplicate_modifiers(self):
        result = False
        i = 0
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

    def test_clusters_active_modifier_exists(self):
        result = False
        for x in self.e.get_clusters_clusters_list():
            if x._mod is None:
                if not isinstance(result, list):
                    result = []
                result.append(x)
        self.assertFalse(result)


class ExtendedModifiersListNoModifiersTest(
        ExtendedModifiersListTests, unittest.TestCase):
    """
    No modifiers at all.
    """

    def setUp(self):
        self.o = DummyBlenderObj()
        self.e = ExtendedModifiersList(self.o)

    def test_active_modifier_is_in_the_list(self):
        self.assertFalse(self.e.has_cluster(self.e.active_modifier_get()))


class ExtendedModifiersListDifferentModifiersTests(
        ExtendedModifiersListTests, unittest.TestCase):
    """
    No complex modifiers clusters.
    """

    def setUp(self):
        self.o = DummyBlenderObj()
        mods = []
        mods.append(self.o.modifier_add('Bevel6', 'BEVEL'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('TopBevel', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel2', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel6', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel6', 'BEVEL'))
        mods.append(self.o.modifier_add('MediumBevel', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel6', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel6', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel6', 'BEVEL'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('TopBevel', 'BEVEL'))
        mods.append(self.o.modifier_add('WeightedNormal', 'WEIGHTED_NORMAL'))
        self.e = ExtendedModifiersList(self.o)


class ExtendedModifiersListLoadClustersTests(
        ExtendedModifiersListTests, unittest.TestCase):
    """
    Saving and loading clusters.
    """

    def setUp(self):
        self.o = DummyBlenderObj()
        mods = []
        mods.append(self.o.modifier_add('Bevel6', 'BEVEL'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('TopBevel', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel2', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel6', 'BEVEL'))
        mods.append(self.o.modifier_add('WeightedNormal', 'WEIGHTED_NORMAL'))
        self.e = ExtendedModifiersList(self.o)
        self.e.save_modifiers_state()
        self.e.save_clusters_state()

        self.old_clusters_state = self.e.get_clusters_state()

        del(self.e)

        self.e = ExtendedModifiersList(self.o)

        self.old_clusters_state_2 = self.e.get_clusters_state()

        del(self.e)

        self.e = ExtendedModifiersList(self.o)

    def test_number_of_clusters(self):
        self.assertEqual(self.e.get_list_length(), 7)

    def test_check_clusters_state_eq(self):
        self.assertEqual(
                self.old_clusters_state, self.e.get_clusters_state())

    def test_check_clusters_state_eq_2(self):
        self.assertEqual(
                self.old_clusters_state_2, self.e.get_clusters_state())


class ExtendedModifiersListLayersTests(
        ExtendedModifiersListTests, unittest.TestCase):
    """
    Cluster layers and complex clusters.
    """

    def setUp(self):
        self.o = DummyBlenderObj()
        mods = []
        mods.append(self.o.modifier_add('Bevel6', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('Boolean3', 'BOOLEAN'))
        mods.append(self.o.modifier_add('Boolean3', 'BOOLEAN'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('TopBevel', 'BEVEL'))
        mods.append(self.o.modifier_add('WeightedNormal', 'WEIGHTED_NORMAL'))
        mods.append(self.o.modifier_add('Bevel2', 'BEVEL'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Boolean3', 'BOOLEAN'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel2', 'BEVEL'))
        mods.append(self.o.modifier_add('Boolean3', 'BOOLEAN'))
        mods.append(self.o.modifier_add('Bevel6', 'BEVEL'))
        mods.append(self.o.modifier_add('Boolean3', 'BOOLEAN'))
        mods.append(self.o.modifier_add('Boolean3', 'BOOLEAN'))
        mods.append(self.o.modifier_add('Bevel2', 'BEVEL'))
        mods.append(self.o.modifier_add('Boolean3', 'BOOLEAN'))
        mods.append(self.o.modifier_add('MediumBevel', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel6', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel6', 'BEVEL'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('TopBevel', 'BEVEL'))
        mods.append(self.o.modifier_add('WeightedNormal', 'WEIGHTED_NORMAL'))
        mods.append(self.o.modifier_add('TopBevel', 'BEVEL'))
        mods.append(self.o.modifier_add('WeightedNormal', 'WEIGHTED_NORMAL'))
        mods.append(self.o.modifier_add('Bevel6', 'BEVEL'))
        clusters = []

        cluster = ModifiersCluster(cluster_name='Beveled Boolean',
                                   cluster_type='BEVELED_BOOLEAN',
                                   modifiers_by_type=[
                                       ['BOOLEAN'], ['BEVEL']],
                                   modifiers_by_name=[['ANY'], ['ANY']],
                                   cluster_priority=0,
                                   cluster_createable=True,
                                   )
        clusters.append(cluster)

        cluster = ModifiersCluster(cluster_name='Triple Bevel',
                                   cluster_type='TRIPLE_BEVEL',
                                   modifiers_by_type=[
                                       ['BEVEL'], ['BEVEL'], ['BEVEL']],
                                   modifiers_by_name=[
                                       ['ANY'], ['ANY'], ['ANY']],
                                   cluster_priority=0,
                                   cluster_createable=True,
                                   )
        clusters.append(cluster)

        cluster = ClustersLayer(cluster_name='Double Triple Bevel Cluster',
                                cluster_type='BEVEL_CLUSTER',
                                modifiers_by_type=[
                                    ['TRIPLE_BEVEL'], ['TRIPLE_BEVEL']],
                                modifiers_by_name=[['ANY'], ['ANY']],
                                cluster_priority=0,
                                cluster_createable=True,
                                )
        clusters.append(cluster)

        self.e = ExtendedModifiersList(self.o, cluster_types=clusters)

    def test_first_cluster_is_double_bevel(self):
        self.assertEquals(self.e.get_first().type, 'BEVEL_CLUSTER')

    def test_first_cluster_has_two_triple_bevels(self):
        self.assertEquals(
                self.e.get_first().get_first().type, 'TRIPLE_BEVEL')

    def test_triple_bevel_has_bevel(self):
        self.assertEquals(
                self.e.get_first().get_first().get_first().type, 'BEVEL')

    def test_triple_bevel_has_three_modifiers(self):
        self.assertEquals(
                self.e.get_first().get_first().get_list_length(), 3)


class ExtendedModifiersListLayersMovingTests(
        ExtendedModifiersListTests, unittest.TestCase):
    """
    Cluster layers and complex clusters.
    """

    def setUp(self):
        self.o = DummyBlenderObj()
        mods = []
        mods.append(self.o.modifier_add('Bevel6', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('Boolean3', 'BOOLEAN'))
        mods.append(self.o.modifier_add('Boolean3', 'BOOLEAN'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('TopBevel', 'BEVEL'))
        mods.append(self.o.modifier_add('WeightedNormal', 'WEIGHTED_NORMAL'))
        mods.append(self.o.modifier_add('Bevel2', 'BEVEL'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Boolean3', 'BOOLEAN'))
        mods.append(self.o.modifier_add('Bevel5', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel2', 'BEVEL'))
        mods.append(self.o.modifier_add('Boolean3', 'BOOLEAN'))
        mods.append(self.o.modifier_add('Bevel6', 'BEVEL'))
        mods.append(self.o.modifier_add('Boolean3', 'BOOLEAN'))
        mods.append(self.o.modifier_add('Boolean3', 'BOOLEAN'))
        mods.append(self.o.modifier_add('Bevel2', 'BEVEL'))
        mods.append(self.o.modifier_add('Boolean3', 'BOOLEAN'))
        mods.append(self.o.modifier_add('MediumBevel', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel6', 'BEVEL'))
        mods.append(self.o.modifier_add('Bevel6', 'BEVEL'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('Array', 'ARRAY'))
        mods.append(self.o.modifier_add('TopBevel', 'BEVEL'))
        mods.append(self.o.modifier_add('WeightedNormal', 'WEIGHTED_NORMAL'))
        mods.append(self.o.modifier_add('TopBevel', 'BEVEL'))
        mods.append(self.o.modifier_add('WeightedNormal', 'WEIGHTED_NORMAL'))
        mods.append(self.o.modifier_add('Bevel6', 'BEVEL'))
        clusters = []

        cluster = ModifiersCluster(cluster_name='Beveled Boolean',
                                   cluster_type='BEVELED_BOOLEAN',
                                   modifiers_by_type=[
                                       ['BOOLEAN'], ['BEVEL']],
                                   modifiers_by_name=[['ANY'], ['ANY']],
                                   cluster_priority=0,
                                   cluster_createable=True,
                                   )
        clusters.append(cluster)

        cluster = ModifiersCluster(cluster_name='Triple Bevel',
                                   cluster_type='TRIPLE_BEVEL',
                                   modifiers_by_type=[
                                       ['BEVEL'], ['BEVEL'], ['BEVEL']],
                                   modifiers_by_name=[
                                       ['ANY'], ['ANY'], ['ANY']],
                                   cluster_priority=0,
                                   cluster_createable=True,
                                   )
        clusters.append(cluster)

        cluster = ClustersLayer(cluster_name='Double Triple Bevel Cluster',
                                cluster_type='BEVEL_CLUSTER',
                                modifiers_by_type=[
                                    ['TRIPLE_BEVEL'], ['TRIPLE_BEVEL']],
                                modifiers_by_name=[['ANY'], ['ANY']],
                                cluster_priority=0,
                                cluster_createable=True,
                                )
        clusters.append(cluster)

        self.e = ExtendedModifiersList(self.o, cluster_types=clusters)

        self.moved_cluster = self.e.get_by_index(1)
        self.moved_cluster_2 = self.e.get_by_index(2)
        self.e.move_down(self.moved_cluster)

    def test_moved_cluster_up(self):
        self.assertEqual(self.moved_cluster, self.e.get_by_index(2))

    def test_moved_cluster_down(self):
        self.assertEqual(self.moved_cluster_2, self.e.get_by_index(1))
