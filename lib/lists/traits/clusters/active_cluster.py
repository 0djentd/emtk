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

import copy
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# TODO: this trait requires class to also inherit ObjectClustersListTrait
class ActiveClusterTrait():
    """Active cluster and selection for clusters list."""

    # Active_modifier doesnt neccessary means that this is an actual modifier.
    # It mostly used for clusters, as every modifier is a cluster anyways.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Cluster that selection started from
        self._cluster_to_select_from = None

        # Additional cluster selection
        self._selected_clusters = None

        # Active modifier
        self._mod = None

    # Shortcuts {{{
    def get_cluster(self):
        """
        Returns active cluster on deepest non-collapsed layer.

        This method should only be used if creating some kind of user
        interface that uses ExtendedModifiersList.
        """
        cluster = self.active_modifier_get()
        if cluster.has_clusters():
            if cluster.modcluster_collapsed is True:
                return cluster
            else:
                return cluster.active_cluster_get_deep()
        else:
            return cluster

    def get_layer(self):
        """
        Returns ModifiersClustersList, which active
        cluster belongs to on deepest non-collapsed layer.

        This method should only be used if creating some kind of user
        interface that uses ExtendedModifiersList.
        """
        return self.get_cluster_or_layer(
                self.active_cluster_get_deep())
    # }}}

    # Active modifier {{{
    # TODO: rename all this methods to active.
    @property
    def active_modifier(self):
        """Returns active modifier or None, if no modifiers."""
        if len(self._modifiers_list) > 0:
            return self.active_modifier_get()
        else:
            return None

    @active_modifier.setter
    def active_modifier(self, mod):
        if isinstance(mod, int):
            return self.active_modifier_set_by_index(mod)
        else:
            return self.active_modifier_set(mod)

    def active_modifier_get(self):
        """Returns active modifier"""
        return self._mod

    def active_modifier_set_by_index(self, i):
        """Set active modifier by index"""
        self._mod = self._modifiers_list[i]

    def active_modifier_set(self, modifier):
        """
        Set active modifier by reference

        Returns True if successfully found modifier.
        Returns False if modifier is not in list.
        """
        if modifier in self.get_list():
            self._mod = modifier
            return True
        return False
    # }}}

    # SELECTION {{{
    def add_to_selection(self, cluster):
        """Adds cluster to selection on this layer."""
        if self.has_cluster(cluster):
            if self._selected_clusters is None:
                self._selected_clusters = []
                self._selected_clusters.append(cluster)
            elif cluster not in self._selected_clusters:
                self._selected_clusters.append(cluster)
        else:
            raise ValueError

    def start_selecting(self, cluster=None):
        """
        Sets cluster that selection should start from on this layer.
        """
        if cluster is None:
            cluster = self.active_modifier_get()
        elif self.has_cluster(cluster):
            self._cluster_to_select_from = self.active_modifier_get()
        else:
            raise ValueError

    def stop_selecting(self):
        """Clear all selected clusters."""
        self._cluster_to_select_from = None
        self._selected_clusters = None

    def get_selection(self, add_active=True):
        """
        Returns list of clusters that were selected on this layer.
        If add_active, will append active cluster to result, even
        if no clusters were selected.
        """

        # Get usual selection.
        if self._cluster_to_select_from is not None:
            result = self.get_list_in_range_inclusive(
                    self._cluster_to_select_from, self._mod)
        else:
            result = None

        # Get per-cluster selection.
        if self._selected_clusters is not None:
            if result is not None:
                result += self._selected_clusters
            else:
                result = self._selected_clusters

        # Add active cluster
        if add_active:
            if self.active_modifier not in result:
                result.append(self.active_modifier)
        else:
            if result is None:
                result = []
        return result
    # }}}

    # Operations on selection {{{
    def remove_selection(self):
        """
        Removes selected clusters on this layer.
        """
        clusters = copy.copy(self.get_cluster_selection())
        for x in clusters:
            self.remove(x)

    def apply_selection(self):
        """
        Applies selected clusters on this layer.
        """
        clusters = copy.copy(self.get_cluster_selection())
        for x in clusters:
            self.apply(x)

    def deconstruct_selection(self):
        """
        Deconstructs selected clusters on this layer.
        """
        clusters = copy.copy(self.get_cluster_selection())
        for x in clusters:
            self.deconstruct(x)

    def move_up_selection(self):
        """
        Moves up selected clusters on this layer.
        """
        self._move_selection('UP')

    def move_down_selection(self):
        """
        Moves down selected clusters on this layer.
        """
        self._move_selection('DOWN')

    def _move_selection(self, direction):
        """
        Deconstructs selected clusters on this layer.
        """
        clusters = copy.copy(self.get_cluster_selection())
        if direction == 'DOWN':
            clusters.reverse()
        for x in clusters:
            self.deconstruct(x)

    def construct_cluster_from_selection(self):
        """
        Reparse selecion on this layer and try to create cluster from it.
        """

        # Get selection on this layer
        clusters = self.get_cluster_selection()
        if (clusters is None) or (clusters == []):
            return False

        logger.info("Constructiong clusters from selection.")

        # Info
        logger.debug(f"Selected clusters is {clusters}")

        # Check if removing active cluster
        removing_active = False
        if self.active_modifier_get() in clusters:
            removing_active = True
            clusters_index = self.get_index(clusters[0])

        clusters_index = self.get_index(clusters[0])

        # Check if there is clusters or only clusterlayers
        parse_modifiers = False
        # TODO: this should be in parser
        for x in clusters:
            if x.has_clusters() is False:
                parse_modifiers = True
                break

        # Remove clusters.
        # This should be done before reparsing, because
        # parser should check for available names.
        # TODO: parser should be able to exclude parsed clusters
        # from name check list.
        for x in clusters:
            self._modifiers_list.remove(x)

        # If there is, reparse modifiers
        if parse_modifiers:
            logger.info("Reparsing modifiers.")
            modifiers = []
            for x in clusters:
                modifiers += x.get_full_actual_modifiers_list()
            result = self._clusters_parser.parse_recursively(
                    modifiers,
                    clusters_names=self.get_full_list_of_cluster_names())

        # If there is only cluster layers,
        # try to create another layer from them
        else:
            logger.info("Reparsing clusters.")
            result = self._clusters_parser._parse_clusters_recursively(
                    clusters)

        # If result is bad, revert changes.
        if result is False or None:
            logger.error("Reparsing clusters failed.")
            logger.debug(f"Reverting changes to {clusters}")
            for x in reversed(clusters):
                self._modifiers_list.insert(clusters_index, x)
            return False

        # Info
        logger.debug("Finished reparsing.")
        logger.debug(f"Selected clusters reparse result is {result}")

        # Insert clusters.
        for x in reversed(result):
            self._modifiers_list.insert(clusters_index, x)

        if removing_active:
            self.active_modifier_set_by_index(clusters_index)

        return True

    # }}}
