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

import collections
import copy
import logging

from ....clusters.cluster_trait import ClusterTrait
from ....controller.answers import ActionDefaultDeconstuct
from ....controller.actions import (
                                    ClustersAction,
                                    ClustersCommand,
                                    )
from ...utils import check_if_removed, check_obj_ref

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ClustersListTrait():
    """
    Class that should be inherited by any ModifiersList subclass that uses
    clusters.
    """

    def find_cluster_by_name(self, name: str):
        for x in self.get_full_list():
            if x.name == name:
                return x

    def find_modifier_by_name(self, name: str):
        for x in self.get_full_actual_modifiers_list():
            if x.name == name:
                return x

    def __init__(self, *args, no_default_actions=False, **kwargs):
        super().__init__(
                         no_default_actions=no_default_actions,
                         *args, **kwargs)
        if not no_default_actions:
            default_actions = [ActionDefaultDeconstuct]
            for x in default_actions:
                self.add_action_answer(x(self))

    def _check_if_cluster_removed(self):
        return

    def has_clusters(self):
        return True

    def _check_cluster_or_modifier(self, cluster):
        if type(cluster) is str:
            result = self.find_cluster_by_name(cluster)
            if result is None:
                result = self.find_modifier_by_name(cluster)
            if result is None:
                raise ValueError
            cluster = result
        elif cluster is None:
            return None
        else:
            if cluster not in self.get_full_list()\
                    and cluster is not self:
                raise ValueError
        return cluster

    # ====================
    # Actions
    # ====================
    @check_if_removed
    def deconstruct(self, clusters):
        """Deconstructs clusters on this layer."""
        if type(clusters) is not list:
            clusters = [clusters]
        result = []
        for x in clusters:
            result.append(self._check_cluster_or_modifier(x))
        clusters = result
        logger.info(f'Deconstructing {clusters} on layer {self}')

        for cluster in clusters:
            # TODO: use ClusterRequest instead.
            x = ClustersAction('DECONSTRUCT', cluster)
            x = ClustersCommand(x,
                                affect_clusters=False,
                                affect_modifiers=False,
                                dry_clusters=False,
                                dry_modifiers=False,
                                )

            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f'Created {x}')
            self._controller.do(x)

    @check_if_removed
    def create(self, cluster_type_instance):
        """Creates cluster or layer on this layer."""
        logger.info(f'Creating {cluster_type_instance} on layer {self}')
        raise ValueError

    # =============
    # Actual modifier getters
    # Always return actual modifiers
    # =============
    def get_actual_modifier_by_index(self, i):
        """
        Returns modifier by index.
        Looks in nested clusters.
        Always return actual modifiers.
        """
        x = self.get_full_actual_modifiers_list()
        return x[i]

    def get_actual_modifier_by_name(self, m_name):
        """
        Returns modifier by name.
        Looks in nested clusters.
        Returns None if not found.
        """
        for x in self.get_full_actual_modifiers_list():
            if x.name == m_name:
                return x
        raise ValueError(f'No modifier with name "{m_name}"')

    # ========================
    # LIST GETTERS
    # ========================
    # def all_elements(self):
    # def full_list(self):
    def get_all_clusters_and_modifiers(self):
        """
        Returns list of all clusters and modifiers anywhere in this cluster.
        """
        result = self.get_full_actual_modifiers_list()
        result.extend(self.get_full_list())
        return full_list(result)

    # def all_clusters(self):
    # def full_clusters_list(self):
    def get_full_list(self):
        """
        Returns full list of clusters, including nested ones.
        Also returns cluster that have other clusters in them.
        """
        result = []
        for x in self._data:
            result.append(x)
            if x.has_clusters():
                for y in x.get_full_list():
                    result.append(y)
        return full_list(result)

    # def all_modifiers_clusters(self):
    # def full_modifiers_clusters_list(self):
    def get_deep_list(self):
        """
        Returns list of this layer clusters including nested ones.
        Only return clusters that contain no other clusters.
        """
        result = []
        for x in self._data:
            if x.has_clusters():
                for y in x.get_deep_list():
                    result.append(y)
            else:
                result.append(x)
        return full_modifiers_clusters_list(result)

    # def all_layers(self):
    # def full_clusters_layers_list(self):
    def get_full_layers_list(self):
        """
        Returns list of all of this layer clusters that contain other
        clusters in it, including nested ones.
        Returns empty list if no such clusters found.
        """
        result = []
        for x in self.get_full_list():
            if x.has_clusters():
                result.append(x)
        return full_clusters_layers_list(result)

    # def all_modifiers(self):
    # def full_modifiers_list(self):
    def get_full_actual_modifiers_list(self):
        """
        Returns full list of this layer actual modifiers,
        including nested ones.
        Returns empty list if no actual modifiers found.
        """
        result = []
        for x in self.get_deep_list():
            for y in x.get_full_actual_modifiers_list():
                result.append(y)
        return full_modifiers_list(result)

    # ==============================
    # Methods based on get_cluster_or_layer
    # ==============================
    # TODO: this doesnt work at all.
    # @check_obj_ref
    @check_if_removed
    def get_cluster_or_layer(self, obj):
        """
        Returns cluster or layer that cluster or modifier belongs to.
        Also returns this ModifiersClustersList.
        Looks in all clusters.
        """
        if type(obj) is str:
            raise TypeError

        # if obj is self:
        #     raise TypeError(
        #             'First layer of ExtendedModifiersList is not a cluster.')

        if obj in self._data:
            return self

        g = self.get_full_list()
        for x in g:
            if obj in x:
                return x
        raise ValueError(f'Cluster {obj} is not in {self}.')

    @check_if_removed
    def get_trace_to(self, cluster):
        """Returns trace to cluster, starting from this layer."""
        result = []
        f = True
        c = cluster
        while f:
            layer = self.get_cluster_or_layer(c)
            result.append(layer)
            if layer is self:
                f = False
            c = layer
        result.reverse()
        return result

    # ==================
    # First and last actual cluster's modifier methods.
    # Used when moving clusters.
    # ==================
    @check_if_removed
    def recursive_get_first_actual_modifier(self, cluster):
        """Returns first actual modifier of a cluster."""
        x = self[0].has_clusters()
        if x.has_clusters():
            y = x[0]
            return x.recursive_get_first_actual_modifier(y)
        else:
            return x[0]

    @check_if_removed
    def recursive_get_last_actual_modifier(self, cluster):
        """Returns last actual modifier of a cluster."""
        x = self[-1].has_clusters()
        if x.has_clusters():
            y = x[-1]
            return x.recursive_get_last_actual_modifier(y)
        else:
            return x[-1]

    # ===============================
    # Renaming objects
    # ===============================
    # TODO: remove this
    @check_if_removed
    def rename_cluster(self, cluster, new_cluster_name):
        """
        Renames cluster.
        Changes name if duplicates are found.

        Returns True or False.
        """
        if not isinstance(cluster, ClusterTrait):
            raise TypeError

        if not isinstance(new_cluster_name, str):
            raise TypeError

        elif self.recursive_has_cluster(cluster):
            if isinstance(new_cluster_name, str):
                cluster.set_this_cluster_custom_name(new_cluster_name)
                self._cluster_number_format(cluster, self.get_full_list())
                return True
        else:
            raise ValueError


class clusters_list_generated_list(collections.UserList):

    def __init__(self, obj, *args, **kwargs):
        self.data = list(obj)

    def items(self):
        return self.data

    def names(self):
        result = {}
        for x in self.data:
            result.update({x.name: x})
        return result

    def types(self):
        result = {}
        for x in self.data:
            result.update({x.type: x})
        return result

    def tags(self):
        result = {}
        for x in self.data:
            result.update({set(x.get_this_cluster_tags()): x})
        return result


class full_modifiers_list(clusters_list_generated_list):
    """List of all modifiers."""
    pass


class full_modifiers_clusters_list(clusters_list_generated_list):
    """List of all modifiers clusters."""
    pass


class full_clusters_layers_list(clusters_list_generated_list):
    """List of all clusters layers."""
    pass


class full_clusters_list(clusters_list_generated_list):
    """List of all clusters."""
    pass


class full_list(clusters_list_generated_list):
    """List of all modifiers and clusters."""
    pass
