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

from ....clusters.cluster import ClusterTrait


class ClustersListTrait():
    """
    Simple list of Modifiers Clusters with, or without modifiers.

    Doesnt require modifiers to be on same object or even exist on
    any object.

    Has different methods for finding specific modifiers, such as
    finding next modifier of specific type starting from specific
    modifier, returning list of modifiers of specific type etc.

    Version 3, now can use clusters.

    Version 4, dropped support for MODCLUSTERS_LITE, as it has no use.
    Now ModifiersClustersList cant have modifiers in it.
    Every modifier should be a part of cluster.

    DefaultModifierCluster is generic cluster that represents
    single modifier with cluster attributes.

    Version 5, removed a lot of methods.

    Doesnt require modifiers to be on same object or even exist on
    any object.
    """

    # TODO: rework docstring
    # TODO: modifier priority
    # TODO: Add checks for passed function arguments
    # TODO: copying modifier settings

    # ============================================================
    #
    #               MODIFIERS LIST METHODS NAMING
    #
    # ============================================================
    # All methods that have 'actual_modifier' in their name
    # return actual Blender modifiers references, and assume that arguments
    # use Blender modifiers.
    #
    # All methods that have 'modifier' in their name return Cluster modifiers
    # unless used within SimpleModifiersList, which uses actual_modifiers
    # in this methods.
    # ModifiersCluster is a SimpleModifiersList.
    #
    # All methods that have 'cluster' in their name return Clusters, or even
    # nested clusters.
    #
    # All methods that have 'recursive' or 'full' or 'deep' in their name
    # recursively calls cluster methods of same functional as called method.
    # This also means that nested clusters will use same method.
    # NestedModifiersCluster use ModifiersClustersList.
    #
    # All methods that have 'loop' in their name iterate 'around' list, used
    # for creating tools that have some kind of UI. They work on single
    # layer, unless specified.
    #
    # Most methods that dont have anything of above in their name doesnt have
    # anything to do with modifiers and operate on lists in general.
    # ============================================================

    _MODIFIERS_LIST_V = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _check_if_cluster_removed(self):
        pass

    def _delete(self, action):
        action.subject._cluster_removed = True
        self._modifiers_list.remove(action.subject)

    # =====================================
    # THIS METHODS WORK ONLY WITH CLUSTERS.
    # =====================================
    # This method is for ExtendedModifiersList only
    def modifier_get_name(self, mod):
        """
        Returns modifier name
        Returns False, if no such modifier
        """
        return self.cluster_get_name(mod)

    # This method is for ExtendedModifiersList only
    def modifier_get_type(self, mod):
        """
        Returns modifier type
        Returns False, if no such modifier
        """
        return self.cluster_get_type(mod)

    # remove this?
    def cluster_get_name(self, mod):
        """
        Returns cluster name.
        """
        return mod.get_this_cluster_name()

    # remove this?
    def cluster_get_type(self, mod):
        """
        Returns cluster type.
        """
        return mod.get_this_cluster_type()

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
        self._check_if_cluster_removed()
        x = self.get_full_actual_modifiers_list()
        return x[i]

    def get_actual_modifier_by_name(self, m_name):
        """
        Returns modifier by name.
        Looks in nested clusters.
        Returns None if not found.
        """
        self._check_if_cluster_removed()
        for x in self.get_full_actual_modifiers_list():
            if x.name == m_name:
                return x
        raise ValueError

    def get_first_actual_modifier(self):
        """
        Returns first modifier of first cluster.
        """
        self._check_if_cluster_removed()
        x = self.get_full_actual_modifiers_list()
        return x[0]

    def get_last_actual_modifier(self):
        """
        Returns last modifier of last cluster.
        """
        self._check_if_cluster_removed()
        x = self.get_full_actual_modifiers_list()
        return x[-1]

    def get_actual_modifier_index(self, mod):
        """
        Returns actual modifier index
        """
        self._check_if_cluster_removed()
        x = self.get_full_actual_modifiers_list()
        return x.index(mod)

    # ==================
    # Info about this list
    # ==================
    def has_cluster(self, cluster):
        """
        Returns True if passed is in this cluster list.
        Returns False.
        """
        if cluster in self.get_list():
            return True
        return False

    def has_cluster_by_type(self, m_type):
        """
        Returns True if there is cluster of this type in this cluster list.
        Returns False.
        """
        for x in self.get_list():
            if x.get_this_cluster_type() == m_type:
                return True
        return False

    def has_cluster_by_name(self, m_name):
        """
        Returns True if there is cluster with this name in this cluster list.
        Returns False.
        """
        for x in self.get_list():
            if x.get_this_cluster_name() == m_name:
                return True
        return False

    def has_cluster_by_tag(self, tag):
        """
        Returns True if there is cluster with this tag in this cluster list.
        Returns False.
        """
        for x in self.get_list():
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
        """
        Returns True, if found actual_modifier in list.
        Returns False if not found.
        """
        if mod in self.get_full_actual_modifiers_list():
            return True
        return False

    def has_actual_modifier_by_type(self, m_type):
        """
        Returns True if found any actual_modifier of m_type.
        Returns False if not found.
        """

        for x in self.get_full_actual_modifiers_list():
            if x.type == m_type:
                return True
        return False

    def has_actual_modifier_by_name(self, m_name):
        """
        Returns True if found any actual_modifier with m_name.
        Returns False if not found.
        """
        for x in self.get_full_actual_modifiers_list():
            if x.name == m_name:
                return True
        return False

    # ---------------------------
    # Same methods for clusters
    # ---------------------------
    def recursive_has_cluster(self, mod):
        """
        Returns True, if found cluster in list.
        Returns False if not found.
        """
        if mod in self.get_full_list():
            return True
        return False

    def recursive_has_cluster_by_type(self, m_type):
        """
        Returns True if found any cluster of m_type.
        Returns False if not found.
        """

        for x in self.get_full_list():
            if x.get_this_cluster_type() == m_type:
                return True
        return False

    def recursive_has_cluster_by_name(self, m_name):
        """
        Returns True if found any cluster with m_name.
        Returns False if not found.
        """
        for x in self.get_full_list():
            if x.get_this_cluster_name() == m_name:
                return True
        return False

    # ========================
    # LIST GETTERS
    # ========================
    def get_full_list(self):
        """
        Returns full list of clusters, including nested ones.
        Also returns cluster that have other clusters in them.
        """
        self._check_if_cluster_removed()
        result = []
        for x in self.get_list():
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
        self._check_if_cluster_removed()
        result = []
        for x in self.get_list():
            if x.has_clusters():
                for y in x.get_deep_list():
                    result.append(y)
            else:
                result.append(x)
        return result

    def get_clusters_clusters_list(self):
        """
        Returns list of all of this layer clusters that contain other
        clusters in it, including nested ones.
        Returns empty list if no such clusters found.
        """
        self._check_if_cluster_removed()

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
        self._check_if_cluster_removed()

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
        """
        Returns full list of clusters by type, including nested ones.
        """
        self._check_if_cluster_removed()
        result = []
        for x in self.get_full_list():
            if m_type == x.get_this_cluster_type():
                result.append(x)
        return result

    def get_full_list_by_name(self, m_name):
        """
        Returns full list of clusters by name, including nested ones.
        """
        self._check_if_cluster_removed()
        result = []
        for x in self.get_full_list():
            if m_name in x.get_this_cluster_name():
                result.append(x)
        return result

    def get_full_list_by_tags(self, m_tags):
        """
        Returns full list of clusters by tags, including nested ones.
        """
        self._check_if_cluster_removed()
        result = []
        for x in self.get_full_list():
            if m_tags in x.get_this_cluster_tags():
                result.append(x)
        return result

    # ==============================
    # Methods based on get_clusters_clusters_list
    # ==============================
    # TODO: rename this
    def get_cluster_cluster_belongs_to(self, cluster):
        """
        Returns cluster cluster or modifier belongs to.
        Also returns this ModifiersClustersList.
        Looks in all clusters.
        """
        self._check_if_cluster_removed()
        if cluster is self:
            raise TypeError(
                    'First layer of ExtendedModifiersList is not a cluster.')

        if cluster in self._modifiers_list:
            return self

        g = self.get_full_list()
        for x in g:
            if cluster in x.get_list():
                return x

        raise ValueError(f'Cluster {cluster} is not in this list {self}.')

    def get_trace_to(self, cluster):
        """
        Returns trace to cluster, starting from this layer.
        Example:
        [TripleBevel, DoubleBevel, DefaultBevel]
        """
        result = []
        f = True
        c = cluster
        while f:
            layer = self.get_cluster_cluster_belongs_to(c)
            result.append(layer)
            if layer is self:
                f = False
            c = layer
        result.reverse()
        return result

    def get_depth(self, cluster):
        """
        Returns cluster depth, starting from 1 for this layer's clusters.
        """
        return len(self.get_trace_to(cluster))

    # ==============================
    # Methods based on get_deep_list
    # ==============================
    def get_deep_list_by_type(self, m_type):
        """
        Returns deep list of clusters by type, including nested ones.
        """
        self._check_if_cluster_removed()
        result = []
        for x in self.get_deep_list():
            if m_type == x.get_this_cluster_type():
                result.append(x)
        return result

    def get_deep_list_by_name(self, m_name):
        """
        Returns deep list of clusters by name, including nested ones.
        """
        self._check_if_cluster_removed()
        result = []
        for x in self.get_deep_list():
            if m_name in x.get_this_cluster_name():
                result.append(x)
        return result

    def get_deep_list_by_tags(self, m_tags):
        """
        Returns deep list of clusters by tags, including nested ones.
        """
        self._check_if_cluster_removed()
        result = []
        for x in self.get_deep_list():
            if m_tags in x.get_this_cluster_tags():
                result.append(x)
        return result

    # ==============================
    # Methods based on get_full_actual_modifiers_list
    # ==============================
    def get_full_actual_modifiers_list_by_type(self, m_type):
        """
        Returns full list of actual modifiers by type, including nested ones.
        """
        self._check_if_cluster_removed()
        result = []
        for x in self.get_full_actual_modifiers_list():
            if x.type == m_type:
                result.append(x)
        return result

    def get_full_actual_modifiers_list_by_name(self, m_name):
        """
        Returns full list of actual modifiers by name, including nested ones.
        """
        self._check_if_cluster_removed()
        result = []
        for x in self.get_full_actual_modifiers_list():
            if m_name in x.name:
                result.append(x)
        return result

    # ==================
    # First and last actual cluster's modifier methods.
    # Used when moving clusters.
    # ==================
    def recursive_get_first_actual_modifier(self, cluster):
        """
        Returns first actual modifier of a cluster.
        """
        self._check_if_cluster_removed()
        x = self.get_first().has_clusters()
        if x.has_clusters():
            y = x.get_first()
            return x.recursive_get_first_actual_modifier(y)
        else:
            return x.get_first()

    def recursive_get_last_actual_modifier(self, cluster):
        """
        Returns last actual modifier of a cluster.
        """
        self._check_if_cluster_removed()
        x = self.get_last().has_clusters()
        if x.has_clusters():
            y = x.get_last()
            return x.recursive_get_last_actual_modifier(y)
        else:
            return x.get_last()

    # ===============================
    # Renaming objects
    # ===============================
    def rename_cluster(self, cluster, new_cluster_name):
        """
        Renames cluster.
        Changes name if duplicates are found.

        Returns True or False.
        """
        self._check_if_cluster_removed()
        if not isinstance(cluster, ClusterTrait):
            raise TypeError

        if not isinstance(new_cluster_name, str):
            raise TypeError

        # TODO: not tested
        elif self.recursive_has_cluster(cluster):
            if isinstance(new_cluster_name, str):
                cluster.set_this_cluster_custom_name(new_cluster_name)
                self._cluster_number_format(cluster, self.get_full_list())
                return True
        else:
            raise ValueError

    # =======================
    # Clusters methods
    # =======================
    def deconstruct_cluster(self, cluster):
        """
        Deconstructs cluster into its components.

        If cluster has cluster, it will be replaced with them.
        If cluster has actual modifiers, it will be replaced with
        simpler clusters.
        """
        self._check_if_cluster_removed()
        if not isinstance(cluster, ClusterTrait):
            raise TypeError

        elif self.recursive_has_cluster(cluster):
            layer = self.get_cluster_cluster_belongs_to(cluster)
            clusters_index = layer.get_index(cluster)
            removing_active = False

            if layer.active_modifier_get() == cluster:
                removing_active = True

            # TODO: cluster being deconstructed
            if not cluster.cluster_being_deconstructed(self):
                return False
            y = cluster.get_list()

            if cluster.has_clusters():
                for x in reversed(y):
                    layer._modifiers_list.insert(clusters_index, x)
                # TODO: use remove_cluster for this?
                layer._modifiers_list.remove(cluster)
            else:
                parser = self._clusters_parser
                parse_result = parser._parse_modifiers_for_simple_clusters(y)
                layer._modifiers_list.remove(cluster)
                for x in reversed(parse_result):
                    layer._modifiers_list.insert(clusters_index, x)

            if removing_active:
                layer.active_modifier_set_by_index(clusters_index)
            return True
        else:
            raise ValueError

    def recursive_has_object(self, obj):
        return obj in self.get_full_list()\
                and obj in self.get_full_actual_modifiers_list()

    def check_obj_ref(self, s):
        if not self.recursive_has_object(s):
            o = None
            for x in self.get_full_list():
                if x.name == s.name:
                    if x.__class__ == s.__class__:
                        o = x
            for x in self.get_full_actual_modifiers_list():
                if x.name == s.name:
                    if x.__class__ == s.__class__:
                        o = x
            if o != s:
                raise ValueError(
                    f'This object {o} reference is broken {s}')
