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

    def get_first_actual_modifier(self):
        """Returns first modifier of first cluster."""
        x = self.get_full_actual_modifiers_list()
        return x[0]

    def get_last_actual_modifier(self):
        """Returns last modifier of last cluster."""
        x = self.get_full_actual_modifiers_list()
        return x[-1]

    def get_actual_modifier_index(self, mod):
        """Returns actual modifier index"""
        x = self.get_full_actual_modifiers_list()
        return x.index(mod)

    # ==================
    # Info about this list
    # ==================
    def has_cluster_by_tag(self, tag):
        """Returns True if there is cluster with this tag in this cluster list.
        """
        for x in self._data:
            if tag in x.get_this_cluster_tags():
                return True
        return False

    # ==================
    # Info about full list
    # ==================
    # -------------------------------------------------------------------------
    # This methods name doesnt specify that they operate on full list, because
    # ModifiersClusterList cant contain actual modifiers in _modifiers_list.
    # -------------------------------------------------------------------------
    def has_actual_modifier(self, mod):
        """Returns True, if found actual_modifier in list."""
        if mod in self.get_full_actual_modifiers_list():
            return True
        return False

    def has_actual_modifier_by_type(self, m_type):
        """Returns True if found any actual_modifier of m_type."""
        for x in self.get_full_actual_modifiers_list():
            if x.type == m_type:
                return True
        return False

    def has_actual_modifier_by_name(self, m_name):
        """Returns True if found any actual_modifier with m_name."""
        for x in self.get_full_actual_modifiers_list():
            if x.name == m_name:
                return True
        return False

    # ---------------------------
    # Same methods for clusters
    # ---------------------------
    def recursive_has_cluster(self, mod):
        """Returns True, if found cluster in list."""
        if mod in self.get_full_list():
            return True
        return False

    def recursive_has_cluster_by_type(self, m_type):
        """Returns True if found any cluster of m_type."""

        for x in self.get_full_list():
            if x.get_this_cluster_type() == m_type:
                return True
        return False

    def recursive_has_cluster_by_name(self, m_name):
        """Returns True if found any cluster with m_name."""
        for x in self.get_full_list():
            if x.get_this_cluster_name() == m_name:
                return True
        return False

    # ---------------------
    # Same method for both.
    # ---------------------
    def recursive_has_object(self, obj):
        """Retruns True if object is in this layer or its clusters"""
        return obj in self.get_full_list()\
            + obj in self.get_full_actual_modifiers_list()

    # ========================
    # LIST GETTERS
    # ========================
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
        return result

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
        return result

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
        return result

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
        return result

    def get_all_clusters_and_modifiers(self):
        """
        Returns list of all clusters and modifiers anywhere in this cluster.
        """
        result = self.get_full_actual_modifiers_list()
        result.extend(self.get_full_list())
        return result

    # ==============================
    # Methods based on get_full_list
    # ==============================
    def get_full_list_by_type(self, m_type):
        """Returns full list of clusters by type."""
        result = []
        for x in self.get_full_list():
            if m_type == x.get_this_cluster_type():
                result.append(x)
        return result

    def get_full_list_by_name(self, m_name):
        """Returns full list of clusters by name."""
        result = []
        for x in self.get_full_list():
            if m_name in x.get_this_cluster_name():
                result.append(x)
        return result

    def get_full_list_by_tags(self, m_tags):
        """Returns full list of clusters by tags."""
        result = []
        for x in self.get_full_list():
            if m_tags in x.get_this_cluster_tags():
                result.append(x)
        return result

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

        if obj is self:
            raise TypeError(
                    'First layer of ExtendedModifiersList is not a cluster.')

        if obj in self._data:
            return self

        g = self.get_full_list()
        for x in g:
            if obj in x:
                return x
        raise ValueError(f'Cluster {obj} is not in this list {self}.')

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

    def get_depth(self, cluster):
        """Returns cluster depth, starting from 1 for this layer's clusters."""
        return len(self.get_trace_to(cluster))

    # ==============================
    # Methods based on get_deep_list
    # ==============================
    def get_deep_list_by_type(self, m_type):
        """Returns deep list of clusters by type, including nested ones."""
        result = []
        for x in self.get_deep_list():
            if m_type == x.get_this_cluster_type():
                result.append(x)
        return result

    def get_deep_list_by_name(self, m_name):
        """Returns deep list of clusters by name, including nested ones."""
        result = []
        for x in self.get_deep_list():
            if m_name in x.get_this_cluster_name():
                result.append(x)
        return result

    def get_deep_list_by_tags(self, m_tags):
        """Returns deep list of clusters by tags, including nested ones."""
        result = []
        for x in self.get_deep_list():
            if m_tags in x.get_this_cluster_tags():
                result.append(x)
        return result

    # TODO: this methods not really useful
    # ==============================
    # Methods based on get_full_actual_modifiers_list
    # ==============================
    @check_if_removed
    def get_full_actual_modifiers_list_by_type(self, m_type):
        """Returns full list of actual modifiers by type, including nested ones.
        """
        result = []
        for x in self.get_full_actual_modifiers_list():
            if x.type == m_type:
                result.append(x)
        return result

    @check_if_removed
    def get_full_actual_modifiers_list_by_name(self, m_name):
        """Returns full list of actual modifiers by name, including nested ones.
        """
        result = []
        for x in self.get_full_actual_modifiers_list():
            if m_name in x.name:
                result.append(x)
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

    def items(self):
        return self.data

    def names(self):
        result = []
        for x in self.data:
            result.append(x.name)
        return result

    def types(self):
        result = []
        for x in self.data:
            result.append(x.type)
        return result


class full_clusters_list(clusters_list_generated_list):
    pass


class full_modifiers_list(clusters_list_generated_list):
    pass


class full_modifiers_clusters_list(clusters_list_generated_list):
    pass


class full_clusters_layers_list(clusters_list_generated_list):
    pass
