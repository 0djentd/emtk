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

from .clusters_layer import ClustersLayer


class ClustersGroup(
                    ClustersLayer
                    ):
    """
    This is ClusterLayer-based cluster type that supports dynamic changing of
    clusters list.

    It is intended to be used as cluster group, or, in other
    words, folder, to simplify manipulating multiple clusters.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, cluster_dynamic=True, **kwargs)

    def add_cluster_to_this_group(self, cluster, direction='DOWN'):
        """
        Adds cluster to cluster group.

        If direction is down, adds it to the end of the list.
        If direction is up, adds it to the beginning of the list.

        Returns True or False, if add cluster.
        """
        if not self.recursive_has_cluster(cluster):
            if self._modcluster_initialized\
                    and self._cluster_definition['dynamic'] is True:
                if direction == 'DOWN':
                    self._modifiers_list.append(cluster)
                elif direction == 'UP':
                    self._modifiers_list.insert(0, cluster)
                else:
                    return False
                return True
        return False

    def remove_cluster_from_this_group(self, cluster):
        """
        Removes cluster from this cluster group.

        Returns cluster.
        Returns False, if there is no such cluster.
        """
        if not self.recursive_has_cluster(cluster):
            if self._modcluster_initialized:
                x = self._modifiers_list.pop(cluster)
                return x
        return False
