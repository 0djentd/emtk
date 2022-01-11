#!/bin/python

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


import cProfile

from lib.lists.extended_modifiers_list import ExtendedModifiersList
from lib.dummy_modifiers import DummyBlenderObj
from lib.clusters.cluster_trait import ClusterTrait
from lib.clusters.modifiers_cluster import ModifiersCluster
from lib.clusters.clusters_layer import ClustersLayer

obj = DummyBlenderObj()
mods = []

for x in range(5):
    mods.append(obj.modifier_add('Bevel6', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('TopBevel', 'BEVEL'))
    mods.append(obj.modifier_add('WeightedNormal', 'WEIGHTED_NORMAL'))
    mods.append(obj.modifier_add('Bevel2', 'BEVEL'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel2', 'BEVEL'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('Bevel6', 'BEVEL'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('Bevel2', 'BEVEL'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('MediumBevel', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel6', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel6', 'BEVEL'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('TopBevel', 'BEVEL'))
    mods.append(obj.modifier_add('WeightedNormal', 'WEIGHTED_NORMAL'))
    mods.append(obj.modifier_add('TopBevel', 'BEVEL'))
    mods.append(obj.modifier_add('WeightedNormal', 'WEIGHTED_NORMAL'))
    mods.append(obj.modifier_add('Bevel6', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('TopBevel', 'BEVEL'))
    mods.append(obj.modifier_add('WeightedNormal', 'WEIGHTED_NORMAL'))
    mods.append(obj.modifier_add('Bevel2', 'BEVEL'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel2', 'BEVEL'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('Bevel6', 'BEVEL'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('Bevel2', 'BEVEL'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('MediumBevel', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel6', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel6', 'BEVEL'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('TopBevel', 'BEVEL'))
    mods.append(obj.modifier_add('WeightedNormal', 'WEIGHTED_NORMAL'))
    mods.append(obj.modifier_add('TopBevel', 'BEVEL'))
    mods.append(obj.modifier_add('WeightedNormal', 'WEIGHTED_NORMAL'))
    mods.append(obj.modifier_add('Bevel6', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('TopBevel', 'BEVEL'))
    mods.append(obj.modifier_add('WeightedNormal', 'WEIGHTED_NORMAL'))
    mods.append(obj.modifier_add('Bevel2', 'BEVEL'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('Bevel5', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel2', 'BEVEL'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('Bevel6', 'BEVEL'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('Bevel2', 'BEVEL'))
    mods.append(obj.modifier_add('Boolean3', 'BOOLEAN'))
    mods.append(obj.modifier_add('MediumBevel', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel6', 'BEVEL'))
    mods.append(obj.modifier_add('Bevel6', 'BEVEL'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('Array', 'ARRAY'))
    mods.append(obj.modifier_add('TopBevel', 'BEVEL'))
    mods.append(obj.modifier_add('WeightedNormal', 'WEIGHTED_NORMAL'))
    mods.append(obj.modifier_add('TopBevel', 'BEVEL'))
    mods.append(obj.modifier_add('WeightedNormal', 'WEIGHTED_NORMAL'))
    mods.append(obj.modifier_add('Bevel6', 'BEVEL'))

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

cluster = ModifiersCluster(cluster_name='Triple Bevel 2',
                           cluster_type='TRIPLE_BEVEL_2',
                           modifiers_by_type=[
                               ['ARRAY'], ['BEVEL'], ['BEVEL']],
                           modifiers_by_name=[
                               ['ANY'], ['Bevel4'], ['ANY']],
                           cluster_priority=3,
                           cluster_createable=False,
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

cluster = ClustersLayer(cluster_name='Double 2 Triple Bevel Cluster',
                        cluster_type='BEVEL_CLUSTER_2',
                        modifiers_by_type=[
                            ['DOUBLE_BEVEL'], ['TRIPLE_BEVEL']],
                        modifiers_by_name=[['Double Triple Bevel Cluster'],
                                           ['ANY']],
                        cluster_priority=1,
                        cluster_createable=True,
                        )
clusters.append(cluster)

e = ExtendedModifiersList(obj, cluster_types=clusters)

cProfile.run('e = ExtendedModifiersList(obj, cluster_types=clusters)')