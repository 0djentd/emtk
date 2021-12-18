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

try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    from ....dummy_modifiers import DummyBlenderModifier, DummyBlenderObj
    _WITH_BPY = False

from ....parser import ClustersParser
from ....clusters_controller import ClustersController
from ....clusters_actions import ClustersAction, ClusterRequest


class FirstLayerClustersListTrait():
    """
    This is class with methods used for 'first layer' of
    clusters. Basically, any layers in it should consist of
    clusters or modifiers of the same object.
    """

    # ExtendedModifiersList version.
    # Used to check if saved clusters state can
    # be used 'as is', or need some kind of
    # editing.
    _EXTENDED_MODIFIERS_LIST_VERSION = (0, 1, 0)

    # List of versions that uncompatible with current
    # version.
    _EXTENDED_MODIFIERS_LIST_NO_COMPAT = [(0, 2, 0), (0, 0, 5)]

    def __init__(self, *args, no_parse=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = ClustersController(self, *args, **kwargs)
        self._controller._object = self._object
        self._clusters_parser = ClustersParser(*args, **kwargs)
        self._clusters_parser._object = self._object
        self._clusters_parser._controller = self._controller
        if not no_parse:
            self._create_modifiers_list()

    def __str__(self):
        result = 'Extended Modifiers List, clusters: '
        for x in self.get_full_list():
            result = result + x.name + ' '
        return result

    def create_modifiers_list(self, obj=None):
        """
        Creates modifiers list for object.
        Parses modifiers, if needed.
        Returns True, if found any modifiers
        and False if not
        """
        return self._create_modifiers_list(obj)

    def _create_modifiers_list(self, obj=None):
        ui_t = []

        ui_t.append("======================")
        ui_t.append("Creating modifiers list")
        ui_t.append("======================")

        if obj is None and self._object is not None:
            obj = self._object

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
            if _WITH_BPY:
                clusters_state = self._object['PreviousClusters']
            elif not _WITH_BPY:
                clusters_state = self._object.props['PreviousClusters']

            already_parsed = True
        except KeyError:
            already_parsed = False

        # Parse modifiers.
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
                self._mod = self._modifiers_list[0]
                modified = True

        # Restore clusters state.
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
                self._mod = self._modifiers_list[0]
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

    def ask(self, question):
        """
        Returns actions required to allow action, if it is not
        allowed.
        Can return empty list.
        """
        if question.subject in self._modifiers_list:
            return []
        if question.subject is self:
            raise ValueError
        return []

    def remove(self, cluster):
        """
        Removes cluster from this list.
        """
        if cluster not in self._modifiers_list:
            raise ValueError

        y = ClustersAction('REMOVE', cluster)
        x = ClusterRequest(self, y)
        self._controller.do(x)

    def perform_action(self, action):
        if action.subject not in self._modifiers_list:
            raise ValueError(f"{action.subject}")

        x = action.verb

        if x == 'REMOVE':
            self._delete(action)
        elif x == 'MOVE':
            self._move(action)
        elif x == 'DECONSTRUCT':
            self._deconstruct(action)
        else:
            raise ValueError

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

        if _WITH_BPY:
            x = self._object.modifiers.new(m_name, m_type)
        elif not _WITH_BPY:
            x = self._object.modifier_add(m_name, m_type)

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
            if _WITH_BPY:
                modifiers.append(
                        self._object.modifiers.new(x[0], x[1]))
            if not _WITH_BPY:
                modifiers.append(
                        self._object.modifier_add(x[0], x[1]))
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
        if not isinstance(layer, FirstLayerClustersListTrait):
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
        # TODO: this probably dont works.
        if _WITH_BPY:
            if isinstance(modifier_or_cluster, bpy.types.Modifier):
                mod = modifier_or_cluster
        elif not _WITH_BPY:
            if isinstance(modifier_or_cluster, DummyBlenderModifier):
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
    def get_metainfo(self):
        """
        Returns list with some info about version of ExtendedModifiersList.
        """
        result = []
        result.append("ExtendedModifiersList")
        result.append(self._EXTENDED_MODIFIERS_LIST_VERSION)
        return result

    def get_clusters_state(self):
        """
        Returns list with info about current clusters state.
        """
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
                t = 'CLUSTER'
            else:
                modifiers = x.get_list()
                for mod in modifiers:
                    h = []
                    h.append(x.get_index(mod))
                    h.append(mod.get_this_cluster_default_name())
                    h.append(mod.get_this_cluster_type())
                    h.append(mod.get_this_cluster_name())
                    m.append(h)
                t = 'LAYER'
            cluster = [e, m, t]
            result.append(cluster)
        return result

    def save_clusters_state(self, prop_name=None):
        """
        Saves current object actual clusters info
        to object's property with prop_name.
        """
        if prop_name is None:
            name = 'PreviousClusters'
        elif isinstance(prop_name, str):
            if len(prop_name) > 0:
                name = prop_name
            else:
                raise ValueError
        else:
            raise TypeError

        t_1 = time.time()
        y = self.get_clusters_state()
        x = json.dumps(y)

        if _WITH_BPY:
            self._object[name] = x
        elif not _WITH_BPY:
            self._object.props[name] = x

        t_2 = time.time()
        t_3 = t_2 - t_1
        self._additional_info_log.append(f"Saved clusters, {t_3}")

    def load_clusters_state(self, prop_name=None):
        """
        Returns previous object clusters info
        from object property with prop_name.
        If no saved clusters, returns False.
        """
        t_1 = time.time()

        if prop_name is None:
            name = 'PreviousClusters'
        elif isinstance(prop_name, str):
            if len(prop_name) > 0:
                name = prop_name
            else:
                raise ValueError
        else:
            raise TypeError

        try:
            if _WITH_BPY:
                previous_clusters = self._object[name]
            elif not _WITH_BPY:
                previous_clusters = self._object.props[name]
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

    def save_modifiers_state(self, prop_name=None):
        """
        Saves current object actual modifiers info
        to object property with prop_name.
        """
        if prop_name is None:
            name = 'PreviousModifiers'
        elif isinstance(prop_name, str):
            if len(prop_name) > 0:
                name = prop_name
            else:
                raise ValueError
        else:
            raise TypeError

        y = self.get_modifiers_state()
        x = json.dumps(y)

        if _WITH_BPY:
            self._object[name] = x
        elif not _WITH_BPY:
            self._object.props[name] = x

    def load_modifiers_state(self, prop_name=None):
        """
        Returns previous object actual modifiers info
        from object property with prop_name.

        If no saved modifiers, returns False.
        """
        if prop_name is None:
            name = 'PreviousModifiers'
        elif isinstance(prop_name, str):
            if len(prop_name) > 0:
                name = prop_name
            else:
                raise ValueError
        else:
            raise TypeError

        try:
            if _WITH_BPY:
                previous_modifiers = self._object[name]
            elif not _WITH_BPY:
                previous_modifiers = self._object.props[name]
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

        # if length is different, dont
        # compare list elements.
        if len(x) != len(y):
            return True

        if x == y:
            return False
        return True
