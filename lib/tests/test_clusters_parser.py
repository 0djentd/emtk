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


class ClustersSerializationClusterTests(
        unittest.TestCase):

    def setUp(self):
        self.cluster = ModifiersCluster(cluster_name='Beveled Boolean',
                                        cluster_type='BEVELED_BOOLEAN',
                                        modifiers_by_type=[
                                            ['BOOLEAN'], ['BEVEL']],
                                        modifiers_by_name=[['ANY'], ['ANY']],
                                        cluster_priority=0,
                                        cluster_createable=True,
                                        )

        self.serialized_cluster = self.cluster.get_this_cluster_definition()

    def tearDown(self):
        del(self.cluster)
        del(self.serialized_cluster)

    def test_get_cluster_definition(self):
        x = self.cluster.get_this_cluster_definition()
        self.assertEqual(x, self.serialized_cluster)
