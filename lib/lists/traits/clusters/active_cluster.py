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


# TODO: this trait requires class to also inherit ObjectClustersListTrait
class ActiveClusterTrait():
    """
    Active cluster and selection for clusters list.

    Selection works on single layer of clusters.
    """

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

    # ===============
    # Active modifier
    # ===============
    # TODO: this methods should be renamed
    @property
    def active_modifier(self):
        return self.active_modifiers_get()

    @active_modifier.setter
    def active_modifier(self, mod):
        return self.active_modifier_set(mod)

    def active_modifier_get(self):
        """Returns active modifier"""
        return self._mod

    def active_modifier_get_type(self):
        """Returns active modifier type"""
        return self.modifier_get_type(self._mod)

    def active_modifier_get_name(self):
        """Returns active modifier type"""
        return self.modifier_get_name(self._mod)

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

    # ===========================
    # Multilayer active modifier
    # ===========================
    def active_cluster_get_deep(self):
        """
        Recursive method.

        Returns active cluster, or its own active cluster.

        Stops on collapsed cluster or cluster without
        clusters in it.
        """

        cluster = self.active_modifier_get()

        if cluster.has_clusters():
            if cluster.modcluster_collapsed is True:
                return cluster
            else:
                return cluster.active_cluster_get_deep()
        else:
            return cluster

    def get_active_cluster_layer(self):
        """
        Returns list active cluster belongs to.
        """

        return self.get_cluster_cluster_belongs_to(
                self.active_cluster_get_deep())

    # ===========================================
    # SELECTION
    # ===========================================
    def add_cluster_to_selection(self, cluster):
        """
        Adds cluster to selection on this layer.
        """
        if self.has_cluster(cluster):
            if self._selected_clusters is None:
                self._selected_clusters = []
                self._selected_clusters.append(cluster)
            elif cluster not in self._selected_clusters:
                self._selected_clusters.append(cluster)

    def start_selecting_clusters(self, cluster=False):
        """
        Sets cluster that selection should start from on this layer.
        """
        if cluster is False:
            cluster = self.active_modifier_get()
        if self.has_cluster(cluster):
            self._cluster_to_select_from = self.active_modifier_get()

    def clear_cluster_selection(self):
        """
        Clears modifier selection on this layer.
        """
        self._cluster_to_select_from = None
        self._selected_clusters = None

    def get_cluster_selection(self):
        """
        Returns list of clusters that were selected on this layer.
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

        # If no selection, return empty list.
        if result is None:
            result = []
        return result

    # ================================
    # Operations on selection
    # ================================
    def move_selected_clusters_up(self):
        clusters = self.get_cluster_selection()
        return self.move_clusters(clusters, direction='UP')

    def move_selected_clusters_down(self):
        clusters = self.get_cluster_selection()
        return self.move_clusters(clusters, direction='DOWN')

    def construct_cluster_from_selection(self):
        """
        Reparse selecion on this layer and try to create cluster from it.
        """

        # Get selection on this layer
        clusters = self.get_cluster_selection()
        if (clusters is None) or (clusters == []):
            return False

        # Info
        self._additional_info_log.append("Selected clusters is ")
        for x in clusters:
            self._additional_info_log.append(f"{x}")

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
            self._additional_info_log.append(
                    "reparsing modifiers.")
            modifiers = []
            for x in clusters:
                modifiers += x.get_full_actual_modifiers_list()
            result = self._clusters_parser.parse_recursively(
                    modifiers,
                    clusters_names=self.get_full_list_of_cluster_names())

        # If there is only cluster layers,
        # try to create another layer from them
        else:
            self._additional_info_log.append(
                    "reparsing clusters.")
            result = self._clusters_parser._parse_clusters_recursively(
                    clusters)

        # If result is bad, revert changes.
        if result is False or None:
            self._additional_info_log.append(
                    "reparsing clusters failed.")
            for x in reversed(clusters):
                self._modifiers_list.insert(clusters_index, x)
            return False

        # Info
        self._additional_info_log.append(
                "Selected clusters reparse result is ")
        for x in result:
            self._additional_info_log.append(f"{x}")

        # Insert clusters.
        for x in reversed(result):
            self._modifiers_list.insert(clusters_index, x)

        if removing_active:
            self.active_modifier_set_by_index(clusters_index)

        return True

    def create_modifier_after_active_modifier(self, m_name, m_type):
        """
        Creates modifier after active modifier.
        """
        i = self.get_index(self.active_modifier)
        mod = self.create_modifier(m_name, m_type)
        if mod is False:
            return False
        result = self.move_to_index(mod, i+1)
        if result is False:
            return False
        return True