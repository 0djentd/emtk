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
from lib.clusters.modifiers_cluster import ModifiersCluster
from lib.clusters.clusters_layer import ClustersLayer
from lib.utils.clusters import serialize_cluster_type, deserialize_cluster_type


class ClustersSerializationTests():
    def tearDown(self):
        del(self.cluster)
        del(self.serialized_cluster)

    def test_serialize_deserialize(self):
        cluster_2 = deserialize_cluster_type(self.serialized_cluster)
        serialized_cluster_2 = serialize_cluster_type(cluster_2)
        self.assertEqual(self.serialized_cluster, serialized_cluster_2)

    def test_serialize_deserialize_progressive(self):
        cluster_3 = deserialize_cluster_type(self.serialized_cluster)
        serialized_cluster_3 = serialize_cluster_type(cluster_3)

        cluster_2 = deserialize_cluster_type(serialized_cluster_3)
        serialized_cluster_2 = serialize_cluster_type(cluster_2)

        self.assertEqual(self.serialized_cluster, serialized_cluster_2)


class ClustersSerializationClusterTests(
        ClustersSerializationTests, unittest.TestCase):
    def setUp(self):
        self.cluster = ModifiersCluster(cluster_name='Beveled Boolean',
                                        cluster_type='BEVELED_BOOLEAN',
                                        modifiers_by_type=[
                                            ['BOOLEAN'], ['BEVEL']],
                                        modifiers_by_name=[['ANY'], ['ANY']],
                                        cluster_priority=0,
                                        cluster_createable=True,
                                        )

        self.serialized_cluster = serialize_cluster_type(self.cluster)


class ClustersSerializationLayerTests(
        ClustersSerializationTests, unittest.TestCase):

    def setUp(self):
        self.cluster = ClustersLayer(cluster_name='Double Bevel Layer',
                                     cluster_type='BEVEL_CLUSTER',
                                     modifiers_by_type=[
                                         ['TRIPLE_BEVEL'], ['TRIPLE_BEVEL']],
                                     modifiers_by_name=[['ANY'], ['ANY']],
                                     cluster_priority=0,
                                     cluster_createable=True,
                                     )
        self.serialized_cluster = serialize_cluster_type(self.cluster)
