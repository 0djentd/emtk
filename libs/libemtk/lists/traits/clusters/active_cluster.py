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

import copy
import logging

from ...utils import check_if_removed, check_obj_ref

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# TODO: remove this mixin?


class ActiveClusterTrait():
    """Active cluster and selection for clusters list."""

    # Active_modifier doesnt neccessary means that this is an actual modifier.
    # It mostly used for clusters, as every modifier is a cluster anyways.

    def get_cluster(self):
        """
        Returns active cluster on deepest non-collapsed layer.

        This method should only be used if creating some kind of user
        interface that uses ExtendedModifiersList.
        """
        cluster = self.active
        if cluster.has_clusters():
            if cluster.instance_data['collapsed'] is True:
                return cluster
            else:
                return cluster.get_cluster()
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
            self.get_cluster())

    # Operations on selection
    def remove_selection(self):
        """
        Removes selected clusters on this layer.
        """
        clusters = copy.copy(self.get_selection())
        self.selection.clear()
        for x in clusters:
            self.remove(x)

    def apply_selection(self):
        """
        Applies selected clusters on this layer.
        """
        clusters = copy.copy(self.get_selection())
        self.selection.clear()
        for x in clusters:
            self.apply(x)

    def deconstruct_selection(self):
        """
        Deconstructs selected clusters on this layer.
        """
        clusters = copy.copy(self.get_selection())
        self.selection.clear()
        for x in clusters:
            self.deconstruct(x)

    def move_selection(self, direction):
        """
        Deconstructs selected clusters on this layer.
        """
        clusters = copy.copy(self.get_selection())
        if direction == 'DOWN':
            clusters.reverse()
        for x in clusters:
            self.deconstruct(x)

    def construct_cluster_from_selection(self):
        """
        Reparse selecion on this layer and try to create cluster from it.
        """

        # Get selection on this layer
        clusters = self.get_selection()
        self.selection.clear()
        if (clusters is None) or (clusters == []):
            return False

        logger.info("Constructiong clusters from selection.")

        # Info
        logger.debug(f"Selected clusters is {clusters}")

        # Check if removing active cluster
        removing_active = False
        if self.active in clusters:
            removing_active = True
            clusters_index = self.index(clusters[0])

        clusters_index = self.index(clusters[0])

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
            self._data.remove(x)

        # If there is, reparse modifiers
        if parse_modifiers:
            logger.info("Reparsing modifiers.")
            modifiers = []
            for x in clusters:
                modifiers += x.all_modifiers()
            result = self._clusters_parser.parse_recursively(
                modifiers,
                clusters_names=self.all_clusters().names())

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
                self._data.insert(clusters_index, x)
            return False

        # Info
        logger.debug("Finished reparsing.")
        logger.debug(f"Selected clusters reparse result is {result}")

        # Insert clusters.
        for x in reversed(result):
            self._data.insert(clusters_index, x)

        if removing_active:
            self.active = clusters_index

        return True
