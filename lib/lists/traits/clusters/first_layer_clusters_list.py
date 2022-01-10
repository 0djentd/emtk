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
import json
import logging

try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    from ....dummy_modifiers import DummyBlenderModifier
    _WITH_BPY = False

from ....parser import ClustersParser
from ....controller.clusters_controller import ClustersController
from ....controller.answers import ActionDefaultRemove
from ....utils.modifiers import get_modifier_state, restore_modifier_state

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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

    def find_cluster_by_name(self, name: str):
        for x in self.get_full_list():
            if x.name == name:
                return x

    def find_modifier_by_name(self, name: str):
        for x in self.get_full_actual_modifiers_list():
            if x.name == name:
                return x

    def __init__(self, *args,
                 no_default_actions=None,
                 no_parse=None, **kwargs):

        super().__init__(*args, **kwargs)
        self._controller = ClustersController(self, *args, **kwargs)

        self._controller._object = self._object
        self._clusters_parser = ClustersParser(*args, **kwargs)
        self._clusters_parser._object = self._object
        self._clusters_parser._controller = self._controller

        if not no_default_actions:
            self.add_action_answer(
                    ActionDefaultRemove(self, only_interpret=True))
        if not no_parse:
            self.create_modifiers_list()

    # Parsing {{{
    def create_modifiers_list(self, obj=None):
        """
        Creates modifiers list for object.
        Parses modifiers, if needed.
        Returns True, if found any modifiers
        and False if not
        """
        logger.info("Creating modifiers list.")
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
            logger.debug(f"Adding {modifier} to modifiers to parse")
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
            logger.info("Modifiers not parsed.")
            if len(modifiers_to_parse) > 0:
                parse_result\
                        = self._clusters_parser.parse_recursively(
                            modifiers_to_parse)
                if parse_result is False:
                    logger.error(
                            "Error while parsing. Cant create modifiers list.")
                    raise ValueError
                logger.info("Setting parse result as a modifiers list.")
                self._modifiers_list = parse_result
                self._mod = self._modifiers_list[0]
                modified = True

        # Restore clusters state.
        elif already_parsed:
            if len(modifiers_to_parse) > 0:
                clusters_state = self.load_clusters_state()
                logger.info("Modifiers already parsed.")
                logger.info(clusters_state)
                parse_result = self._clusters_parser.parse_clusters_state(
                        modifiers_to_parse, clusters_state,
                        clusters_names=self.get_full_list_of_cluster_names())
                if parse_result is False:
                    logger.error(
                            "Error while parsing. Cant create modifiers list.")
                    raise ValueError
                logger.info("Parse result ")
                logger.info(parse_result)
                self._modifiers_list = parse_result
                self._mod = self._modifiers_list[0]
                modified = True

        logger.info("Finished creating modifiers list")

        if modified:
            return True
        else:
            return False

    def update_cluster_types(self, cluster):
        """Add new cluster type"""
        return self._clusters_parser.update_cluster_types(cluster)

    def remove_cluster_type(self, cluster):
        """Remove cluster type"""
        return self._clusters_parser.remove_cluster_type(cluster)
    # }}}

    # Actions {{{
    def ask(self, question):
        """
        Returns actions required to allow action, if it is not
        allowed.
        Can return empty list.
        """
        # For first layer, this not needed
        if question.subject is self:
            raise ValueError

    # TODO: Remove this method
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

        logger.info("Adding modifier to modifiers list.")

        if _WITH_BPY:
            x = self._object.modifiers.new(m_name, m_type)
        elif not _WITH_BPY:
            x = self._object.modifier_add(m_name, m_type)

        z = []
        z.append(x)
        result = self._clusters_parser._parse_modifiers(z)

        logger.info(f"Created modifier {x}")
        logger.debug(f"parse result is {result}")
        self._modifiers_list += result

        logger.info("Finished adding modifier to modifiers list.")
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

    def duplicate(self, cluster):
        """
        Duplicates cluster modifiers and reparses them.
        This will add parsed cluster to first layer.
        """
        modifiers = []
        for x in cluster.get_full_actual_modifiers_list():
            modifier_props = get_modifier_state(x)
            if _WITH_BPY:
                modifiers.append(
                        self._object.modifiers.new(x.name, x.type))
            if not _WITH_BPY:
                modifiers.append(
                        self._object.modifier_add(x.name, x.type))
            restore_modifier_state(modifiers[-1], modifier_props)
        result = self._clusters_parser.parse_recursively(modifiers)
        self._modifiers_list.extend(result)
    # }}}

    # Storing clusters state {{{
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

        y = self.get_clusters_state()
        x = json.dumps(y)

        if _WITH_BPY:
            self._object[name] = x
        elif not _WITH_BPY:
            self._object.props[name] = x

        logger.info("Saved clusters")
        logger.debug(f"{x}")

    def load_clusters_state(self, prop_name=None):
        """
        Returns previous object clusters info
        from object property with prop_name.
        If no saved clusters, returns False.
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

        try:
            if _WITH_BPY:
                previous_clusters = self._object[name]
            elif not _WITH_BPY:
                previous_clusters = self._object.props[name]
        except KeyError:
            previous_clusters = False

        if previous_clusters is not False:
            x = json.loads(previous_clusters)
            logger.info("Loaded clusters")
            logger.debug(f"{x}")
            return x
        else:
            return False
    # }}}

    # saving modifiers state for fast check. {{{
    def get_modifiers_state(self):
        """Returns current object actual modifiers info."""
        result = []
        for x in self._object.modifiers:
            result.append(get_modifier_state(x))
        return result

    def save_modifiers_state(self, prop_name=None):
        """Saves current object actual modifiers info
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
        Returns saved actual modifiers info
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
    # }}}

    # Utility {{{
    def get_full_list_of_cluster_names(self):
        """Returns full list of custom cluster names."""
        result = []
        for x in self.get_full_list():
            result.append(x.get_this_cluster_name())
        return result

    def _check_if_actual_modifiers_list_is_correct(self):
        """
        Checks if actual modifiers in clusters ordered
        as in actual Blender modifiers stack.

        Returns True or throws an error.
        """

        x = self.get_full_actual_modifiers_list()
        y = self._object.modifiers

        if len(x) != len(y):
            raise ValueError

        for z, e in zip(x, y):
            if z.name != e.name:
                raise ValueError
            if z.type != e.type:
                raise ValueError
        return True

    def __str__(self):
        result = 'Extended Modifiers List, clusters: '
        y = 0
        for x in self.get_full_list():
            if y < 6:
                y += 1
                result = result + x.name + ' '
            else:
                length = len(self.get_full_list())
                result = result + f'... total clusters number is {length}'
                break
        return result

    def __repr__(self):
        return self.__str__()
    # }}}
