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
import json
import time

import bpy

from .clusters_list import ClustersList
from ..clusters_parser import ClustersParser
from ..sortable_clusters_list import SortableClustersList


class FirstLayerClustersList(ClustersList, SortableClustersList):
    """
    This is class with methods used for 'first layer' of
    clusters. Basically, any layers in it should consist of
    clusters or modifiers of the same object.
    """

    def __init__(self):
        super().__init__()
        self._clusters_parser = ClustersParser()

    def __init_subclass__(cls):
        cls._clusters_parser = ClustersParser()

    def create_modifiers_list(self, obj):
        """
        Creates modifiers list for object.
        Parses modifiers, if needed.
        Returns True, if found any modifiers
        and False if not
        """
        return self._create_modifiers_list(obj)

    def _create_modifiers_list(self, obj):
        ui_t = []

        ui_t.append("======================")
        ui_t.append("Creating modifiers list")
        ui_t.append("======================")

        # Modifiers list.
        # self._modifiers_list = []

        self._object = obj

        # Are modifiers sorted already?
        self._modifiers_sorted = False

        # some methods reqire it.
        self._modifiers_list_obj_list = True

        # Was create_modifiers_list able to find any modifiers?
        modified = False

        # Was clusters parsed before?
        already_parsed = False

        # Set parser's object
        self._clusters_parser._object = self._object

        parse_result = []

        # Get actual object modifiers
        modifiers_to_parse = []
        for modifier in self._object.modifiers:
            ui_t.append(f"Adding {modifier} to modifiers to parse")
            modifiers_to_parse.append(modifier)

        try:
            clusters_state = self._object['PreviousClusters']
            already_parsed = True
        except KeyError:
            already_parsed = False

        # Parse modifiers
        if already_parsed is False:
            ui_t.append("Modifiers not parsed.")
            if len(modifiers_to_parse) > 0:
                parse_result\
                        = self._clusters_parser.parse_recursively(
                            modifiers_to_parse)
                if parse_result is False:
                    self._additional_info_log.append(
                            "Error while parsing. Cant create modifiers list.")
                    for line in self._clusters_parser._additional_info_log:
                        self._additional_info_log.append(line)
                    for line in ui_t:
                        self._additional_info_log.append(line)
                    self._modifiers_list = []
                    return False
                ui_t.append("Setting parse result as a modifiers list.")
                self._modifiers_list = parse_result
                modified = True
        elif already_parsed:
            ui_t.append("")
            if len(modifiers_to_parse) > 0:
                clusters_state = self.load_clusters_state()
                self._additional_info_log.append("Modifiers already parsed.")
                self._additional_info_log += clusters_state
                parse_result = self._clusters_parser.parse_clusters_state(
                        modifiers_to_parse, clusters_state,
                        clusters_names=self.get_full_list_of_cluster_names())
                if parse_result is False:
                    self._additional_info_log.append(
                            "Error while parsing. Cant create modifiers list.")
                    for line in self._clusters_parser._additional_info_log:
                        self._additional_info_log.append(line)
                    for line in ui_t:
                        self._additional_info_log.append(line)
                    self._modifiers_list = []
                    return False
                self._additional_info_log.append("Parse result ")
                for line in parse_result:
                    self._additional_info_log.append(f"{line}")
                self._modifiers_list = parse_result
                modified = True

        if self._MODIFIERS_LIST_V:
            ui_t.append("===================================")
            ui_t.append("Finished creating modifiers list")
            ui_t.append("===================================")
            for line in self._clusters_parser._additional_info_log:
                self._additional_info_log.append(line)
            for line in self._modifiers_list_info():
                ui_t.append(f"{line}")
            for line in ui_t:
                self._additional_info_log.append(line)
        if modified:
            return True
        else:
            return False

    # TODO: this method should be removed
    def update_cluster_types_list(self, cluster):
        return self._clusters_parser.update_cluster_types_list(cluster)

    # TODO: this thing barely works.
    # actually kinda works idk
    # TODO: test with multi-layer
    # I dont sure why it works even.
    # This method should be only used from ModifiersClustersList.
    # Even though it exists in modifier clusters as well.
    # Btw, if this returns false, modal operator should be
    # finished.
    def remove_cluster(self, cluster):
        """
        Removes cluster from this list or nested lists.
        Cant remove last modifier.

        Returns False, if any errors.
        Returns True, if deleted cluster.
        """

        # Layer cluster belongs to
        layer = self.get_cluster_cluster_belongs_to(cluster)
        self._additional_info_log.append(f"Removing {cluster} from {layer}")

        # Can cluster be removed from its layer
        cluster_can_be_removed = False

        # Should layer be removed as well?
        remove_layer = False

        # Was cluster active before removing
        removing_active_cluster = False

        # Was cluster last in list
        removing_active_cluster_last = False

        # Check if there is such cluster to begin with
        if self.recursive_has_cluster(cluster):
            # Check if it can be deleted without deleting layer
            if isinstance(layer, FirstLayerClustersList):
                cluster_can_be_removed = True
            elif layer._MODCLUSTER_DYNAMIC:
                cluster_can_be_removed = True

            self._additional_info_log.append(
                    f"Cluster can be removed? {cluster_can_be_removed}")

            if cluster_can_be_removed:

                # Check if it is active
                if layer.active_modifier_get() is cluster:
                    removing_active_cluster = True
                    if layer.get_last() == layer.active_modifier_get():
                        removing_active_cluster_last = True

                # Ask cluster if it can be removed
                if not cluster.cluster_being_removed(self):
                    return False

                if cluster.has_clusters():
                    # Get list of clusters with modifiers
                    for x in cluster.get_deep_list():
                        # Get actual modifiers to be removed
                        # TODO: what is dat?
                        mods = x.get_full_actual_modifiers_list()
                        for mod in mods:
                            # TODO: why this thorws error?
                            self._object.modifiers.remove(mod)
                            self._additional_info_log.append(
                                    f"removing actual modifier {mod}")
                else:
                    # Get actual modifiers to be removed
                    # TODO: what is dat?
                    # TODO: this method returns copy of _modifiers_list
                    # TODO: need another method for actual list reference
                    # but get_actual_full_actual_modifiers_list is kinda
                    # too complicated ya know?
                    mods = cluster.get_full_actual_modifiers_list()
                    for mod in mods:
                        # TODO: why this thorws error?
                        self._object.modifiers.remove(mod)
                        self._additional_info_log.append(
                                f"removing actual modifier {mod}")

                # If there any clusters left on layer
                if layer.get_list_length() > 0:
                    # Select next cluster, if removing active
                    if removing_active_cluster:
                        if removing_active_cluster_last:
                            layer.active_modifier_set(
                                    layer.find_previous_any_loop(cluster))
                        else:
                            layer.active_modifier_set(
                                    layer.find_next_any_loop(cluster))

                # If no clusters, it should be removed
                else:
                    remove_layer = True

                # Remove cluster
                layer.get_actual_list().remove(cluster)

            # If not dynamic, it should be removed
            else:
                remove_layer = True

            self._additional_info_log.append(
                    f"Should layer be removed as well? {remove_layer}")

            # Remove layer
            if remove_layer:
                if not layer._modifiers_list_obj_list:
                    x = self.get_cluster_cluster_belongs_to(layer)
                    self._additional_info_log.append(
                            f"removing layer from {x}")
                    if not self.remove_cluster(layer):
                        return False
                else:
                    self._additional_info_log.append(
                            f"cant remove layer {layer}")
                    return False

            return True
        return False

    def apply_cluster(self, cluster):
        """
        Applies cluster in this list.

        Returns False, if any errors.
        This should return FINISHED in operator.
        Returns True, if applied cluster.
        """
        # Check if there is such cluster to begin with
        if self.recursive_has_cluster(cluster):

            # Ask cluster if it can be applied
            if not cluster.cluster_being_applied(self):
                return False

            if cluster.has_clusters():
                # Get list of clusters with modifiers
                for z in cluster.get_deep_list():

                    # Get reference to modifiers list
                    x = z.get_full_actual_modifiers_list()

                    # Get shallow copy to iterate over original modifiers list
                    # and remove references
                    x2 = copy.copy(x)

                    # Remove modifiers
                    for y in x:
                        e = y.name
                        bpy.ops.object.modifier_apply(modifier=e)

                    # Remove reference to modifiers
                    for z in x2:
                        x.remove(z)
            else:
                # Get reference to modifiers list
                x = cluster.get_full_actual_modifiers_list()

                # Get shallow copy to iterate over original modifiers list
                # and remove references
                x2 = copy.copy(x)

                # Remove modifiers
                for y in x:
                    e = y.name
                    bpy.ops.object.modifier_apply(modifier=e)

                # Remove reference to modifiers
                for z in x2:
                    x.remove(z)

            # Remove cluster.
            # Check if applying modifier will make any nested clusers
            # have no clusters in them.
            # TODO: this should ask clusters if they can be removed.
            layer = self.get_cluster_cluster_belongs_to(cluster)
            layer_to_remove = self._check_which_layer_should_be_removed(layer)

            # if some layer should be removed too.
            if layer_to_remove is not False:
                result = self.remove_cluster(layer_to_remove)
                # TODO: check first, then apply modifiers?
                if result is False:
                    return False

            # if only cluster should be removed.
            else:
                result = self.remove_cluster(cluster)
                if result is False:
                    return False

            return True
        return False

    def create_modifier(self, m_name, m_type, layer=None, cluster_index=None):
        """
        Creates modifier, adds parsed cluster
        to the end of list.

        Returns reference to created modifier.
        Returns None, if used from wrong list.
        """

        # Layer to create cluster on
        if layer is None:
            layer = self

        # New cluster index on layer
        if cluster_index is None:
            cluster_index = layer.get_list_length() - 1

        if self._MODIFIERS_LIST_V:
            ui_t = []
            ui_t.append("===================================")
            ui_t.append("Add modifier to modifiers list")
            ui_t.append("===================================")
            for line in self._modifiers_list_info():
                ui_t.append(f"{line}")
            for line in ui_t:
                self._additional_info_log.append(line)

        x = self._object.modifiers.new(m_name, m_type)

        z = []
        z.append(x)
        result = self._clusters_parser._parse_modifiers(z)

        ui_t.append(f"Created modifier {x}")
        ui_t.append(f"parse result is {result}")
        self._modifiers_list += result

        if self._MODIFIERS_LIST_V:
            ui_t = []
            ui_t.append("===================================")
            ui_t.append("Finished add modifier to modifiers list")
            ui_t.append("===================================")
            for line in self._modifiers_list_info():
                ui_t.append(f"{line}")
            for line in ui_t:
                self._additional_info_log.append(line)
        return x

    def create_cluster(self, cluster_type):
        """
        Creates cluster by type with modifiers and
        adds it to the end of the list.

        Returns True, if successfully created cluster.
        """
        modifiers = []
        for x in cluster_type.get_modifiers_sequence():
            modifiers.append(
                    self._object.modifiers.new(x[0], x[1]))
        cluster = copy.deepcopy(cluster_type)
        clusters_names = self.get_full_list_of_cluster_names()
        self._clusters_parser._initialize_cluster(
                cluster, modifiers, clusters_names)
        self._modifiers_list.append(cluster)
        return True

    # ===============
    # Operations on selection
    # ===============
    def apply_clusters_selection(self):
        """
        Applies selected clusters on active layer, if any.
        """

        layer = self.get_layer()

        clusters = copy.copy(layer.get_cluster_selection())

        for x in clusters:
            if not self.apply_cluster(x):
                self._additional_info_log.append(
                        "Applying selected clusters failed.")
                return False
        return True

    def remove_clusters_selection(self):
        """
        Removes selected clusters on active layer, if any.
        """

        layer = self.get_layer()

        clusters = copy.copy(layer.get_cluster_selection())

        for x in clusters:
            if not self.remove_cluster(x):
                self._additional_info_log.append(
                        "Removing selected clusters failed.")
                return False
        return True

    # ===============
    # Utility
    # ===============
    def get_full_list_of_cluster_names(self):
        """
        Returns full list of custom cluster names.
        """
        result = []
        for x in self.get_full_list():
            result.append(x.get_this_cluster_name())
        return result

    def _check_if_actual_modifiers_list_is_correct(self):
        """
        Checks if actual modifiers in clusters ordered correctly,
        according to Blender modifiers stack.
        """

        x = self.get_full_actual_modifiers_list()
        y = self._object.modifiers

        if len(x) != len(y):
            return False

        for z, e in zip(x, y):
            if z.name != e.name:
                return False
            if z.type != e.type:
                return False
        return True

    def _check_which_layer_should_be_removed(self, layer):
        """
        Checks if there is no clusters on layers.

        Returns lowest level clusters layer that should be removed.
        Returns False, if no layer should be removed.
        """
        if not isinstance(layer, FirstLayerClustersList):
            if layer.get_list_length() == 0:
                layer_2 = self.get_cluster_cluster_belongs_to(layer)
                result = self.recursive_check_which_layer_should_be_removed(
                        layer_2)
                if result is False:
                    return layer
                else:
                    return result
        return False

    def get_actual_modifier_index(self, modifier_or_cluster, get_last=False):
        """
        Returns actual modifier index or index of first cluster's
        actual modifier.
        If get_last is True, looks for last actual modifier.
        """
        if isinstance(modifier_or_cluster, bpy.types.Modifier):
            mod = modifier_or_cluster
        else:
            if get_last is False:
                mod = self.recursive_get_first_actual_modifier(
                        modifier_or_cluster)
            else:
                mod = self.recursive_get_last_actual_modifier(
                        modifier_or_cluster)

        x = self.get_full_actual_modifiers_list()
        return x.index(mod)

    def has_clusters(self):
        """
        This method exists to stop recursive methods.
        """
        return True

    # =================
    # Storing modifiers state
    # ================
    def get_clusters_state(self):
        result = []

        # Example of cluster
        # [[0, Triple_Bevel, BEVEL_CLUSTER, triple_bevel.005],
        # [[0, TripleBevel, DOUBLE_BEVEL], [1, TripleBevel.001, DOUBLE_BEVEL]],
        # 'CLUSTER']
        #
        # Example of layer
        # [[1, DoubleBevel, DOUBLE_BEVEL,],
        # [[4, Bevel, BEVEL], [5, Bevel.001, BEVEL]],
        # 'LAYER']

        # Get actual modifiers.
        actual_modifiers = []
        for x in self._object.modifiers:
            actual_modifiers.append(x)

        # Get list of all clusters.
        clusters = self.get_full_list()
        for i, x in enumerate(clusters):
            e = []
            e.append(i)
            e.append(x.get_this_cluster_default_name())
            e.append(x.get_this_cluster_type())
            e.append(x.get_this_cluster_name())
            m = []
            if not x.has_clusters():
                modifiers = x.get_full_actual_modifiers_list()
                for mod in modifiers:
                    h = []
                    h.append(actual_modifiers.index(mod))
                    h.append(mod.name)
                    h.append(mod.type)
                    h.append(mod.name)
                    m.append(h)
                t = 'LAYER'
            else:
                modifiers = x.get_list()
                for mod in modifiers:
                    h = []
                    h.append(x.get_index(mod))
                    h.append(mod.get_this_cluster_default_name())
                    h.append(mod.get_this_cluster_type())
                    h.append(mod.get_this_cluster_name())
                    m.append(h)
                t = 'CLUSTER'
            cluster = [e, m, t]
            result.append(cluster)
        return result

    def save_clusters_state(self):
        """
        Saves current object actual clusters info
        to object props.
        """
        t_1 = time.time()
        y = self.get_clusters_state()
        x = json.dumps(y)
        self._object['PreviousClusters'] = x
        t_2 = time.time()
        t_3 = t_2 - t_1
        self._additional_info_log.append(f"Saved clusters, {t_3}")

    def load_clusters_state(self):
        """
        Returns previous object actual clusters info
        from object props.
        If no saved clusters, returns False
        """
        t_1 = time.time()
        try:
            previous_clusters = self._object['PreviousClusters']
        except KeyError:
            previous_clusters = False

        if previous_clusters is not False:
            x = json.loads(previous_clusters)
            t_2 = time.time()
            t_3 = t_2 - t_1
            self._additional_info_log.append(f"Loaded clusters, {t_3}")
            for line in x:
                self._additional_info_log.append(f"{line}")
            return x
        else:
            return False

    # ==========================
    # saving modifiers state for fast check.
    # ==========================
    def get_modifiers_state(self):
        """
        Returns current object actual modifiers info.
        """
        modifiers = self._object.modifiers
        y = []
        for i, mod in enumerate(modifiers):
            y.append([i, mod.name, mod.type])
        return y

    def save_modifiers_state(self):
        """
        Saves current object actual modifiers info
        to object props.
        """
        y = self.get_modifiers_state()
        x = json.dumps(y)
        self._object['PreviousModifiers'] = x

    def load_modifiers_state(self):
        """
        Returns previous object actual modifiers info
        from object props.
        If no saved modifiers, returns False
        """
        try:
            previous_modifiers = self._object['PreviousModifiers']
        except KeyError:
            previous_modifiers = False
        return previous_modifiers

    def check_modifiers_state_change(self):
        """
        Compares previous modifiers stack state with
        existing one.
        Returns True, if modifiers list changed since last
        save_modifiers_state usage.
        """
        x = self.load_modifiers_state()

        # There is no saved modifiers list state
        if x is False:
            return False

        y = self.get_modifiers_state()

        # if length is different, dont even
        # compare list elements.
        if len(x) != len(y):
            return True

        if x == y:
            return False
        return True
