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

try:
    import bpy
    _WITH_BPY = True
except ModuleNotFoundError:
    from ..dummy_modifiers import DummyBlenderModifier
    _WITH_BPY = False

from ..clusters.cluster_trait import ClusterTrait
from ..clusters.default_modifier_cluster import DefaultModifierCluster
from ..utils import libemtk_VERSION

CLUSTERS_PARSER_VERSION = (0, 1, 0)

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
# logger.setLevel(logging.DEBUG)


class ClustersParser():
    """Base class for objects that should be able to parse clusters."""

    def __init__(self, *args,
                 skip_parser=None,
                 cluster_types=None,
                 only_default_cluster=None,
                 no_default_cluster=None,
                 parser_sanity_checks=None,
                 replace_on_update=None,
                 simple_clusters=None,
                 max_iterations=None,
                 **kwargs
                 ):

        super().__init__()

        # Skip parser and sanity checks, only use default cluster.
        if skip_parser:
            self.__SKIP_PARSE = True
        else:
            self.__SKIP_PARSE = False

        # Only use default cluster, but dont skip parser.
        if only_default_cluster:
            self.__DEFAULT_CLUSTERS = True
        else:
            self.__DEFAULT_CLUSTERS = False

        # Check clusters for errors.
        if parser_sanity_checks is None:
            self.__CLUSTERS_SANITY_CHECKS = True
        elif parser_sanity_checks:
            self.__CLUSTERS_SANITY_CHECKS = True
        else:
            self.__CLUSTERS_SANITY_CHECKS = False

        # Replace available cluster types when updaing existing one.
        if replace_on_update is None:
            self.__REPLACE_ON_UPDATE = True
        elif replace_on_update:
            self.__REPLACE_ON_UPDATE = True
        else:
            self.__REPLACE_ON_UPDATE = False

        # Replace available cluster types when updaing existing one.
        if simple_clusters is None:
            self.__SIMPLE_CLUSTERS = False
        elif simple_clusters:
            self.__SIMPLE_CLUSTERS = True
        else:
            self.__SIMPLE_CLUSTERS = False

        # Max amount of iterations for _parse_modifiers_recursively
        # Can also be interpreted as max amount of layers.
        if max_iterations is None:
            self.__RECURSIVE_PARSER_MAX_ITERATIONS = 100
        elif isinstance(max_iterations, int):
            self.__RECURSIVE_PARSER_MAX_ITERATIONS = max_iterations
        else:
            raise TypeError

        # Additional info.
        self._additional_info_log = []

        # Available cluster types
        self.available_cluster_types = []

        # Last new cluster type index.
        self._last_cluster_type_index = 1

        # Dont use default cluster.
        if not no_default_cluster:
            default_modififer_cluster = DefaultModifierCluster()
            self.update_cluster_types(default_modififer_cluster)

        # Available cluster types.
        if isinstance(cluster_types, list):
            for x in cluster_types:
                self.update_cluster_types(x)

    """
    parse_result is a list of lists with string, cluster and modifiers.
    Example:
    [['CREATE', <TRIPLE_BEVEL>, [<BEVEL>, <BEVEL>, <BEVEL>],
     ['CREATE', <TRIPLE_BEVEL>, [<BEVEL>, <BEVEL>, <BEVEL>],
     ['SKIP', <DOUBLE_BEVEL>, None]]
    """

    def _get_modifiers_clusters_types(self):
        result = []
        for x in self.available_cluster_types:
            if not x.has_clusters():
                result.append(x)
        return result

    def _get_clusters_layers_types(self):
        result = []
        for x in self.available_cluster_types:
            if x.has_clusters():
                result.append(x)
        return result

    def parse_recursively(self, modifiers_to_parse,
                          additional_types=None,
                          no_available_types=False,
                          no_available_layer_types=False,
                          clusters_names=None,
                          layers_to_create=None):
        """
        Parses clusters or actual modifiers recursively.

        If specified additional_types clusters list, uses them in parsing.
        If no_available_types is true, dont use available to object
        cluster types. Should only be used with additional_types.
        clusters_names is list of already existing names in clusters list.
        It should always be specified when partially reparsing list.

        Returns clusters ready to be put into ClustersList.
        Returns False if cant parse for some reason, for example if
        there are some modifiers that cant be used in any cluster.
        """
        if not isinstance(modifiers_to_parse, list):
            raise TypeError
        if clusters_names is None:
            clusters_names = []
        if type(clusters_names) is not list:
            raise TypeError

        if _WITH_BPY:
            modifier_type = bpy.types.Modifier
        elif not _WITH_BPY:
            modifier_type = DummyBlenderModifier

        for x in modifiers_to_parse:
            if not isinstance(x, modifier_type):
                if x.has_clusters():
                    has_clusters = True
                    has_layers = True
                else:
                    has_clusters = True
            else:
                has_modifiers = True

        if not has_modifiers\
                and not has_clusters\
                and not has_layers:
            raise TypeError

        # Check if passed list have modifiers
        if has_modifiers:
            modifiers_to_parse_2 = []
            for x in modifiers_to_parse:
                if not isinstance(x, modifier_type):
                    modifiers_to_parse_2.extend(
                        x.all_modifiers())
                modifiers_to_parse_2.append(x)

            # Parse modifiers once.
            if self.__SIMPLE_CLUSTERS:
                parse_result = self._parse_modifiers_for_simple_clusters(
                    modifiers_to_parse_2)
                if parse_result is False:
                    return False
            else:
                logger.debug("Trying to parse modifiers")
                parse_result = self._parse_modifiers(modifiers_to_parse_2,
                                                     additional_types,
                                                     no_available_types,
                                                     clusters_names)
                if parse_result is False:
                    logger.error("Error while parsing modifiers")
                    return False

            clusters_names += _get_clusters_names(parse_result)

        # If passed clusters, just continue with them.
        else:
            parse_result = modifiers_to_parse

        # Parse clusters a lot.
        result = self._parse_clusters_recursively(parse_result,
                                                  additional_types,
                                                  no_available_layer_types,
                                                  clusters_names,
                                                  layers_to_create)
        return result

    def parse_clusters_state(self, modifiers,
                             clusters_state,
                             clusters_names=None):
        """
        Reconstructs clusters and parses ones that
        was unable to reconstruct.
        """
        if clusters_names is None:
            clusters_names = []

        logger.debug("RESTORING CLUSTERS STATE")

        # Get cluster types from saved clusters_state.
        cluster_types = self._unwrap_saved_clusters_state(clusters_state)

        # Check that it was restored correctly
        if cluster_types is False or cluster_types is None:
            logger.error("Something is wrong with restoring cluster types")
            return False
        elif len(cluster_types) == 0:
            logger.info("Found no cluster types.")
            return False
        else:
            logger.debug(f"Found {len(cluster_types)} cluster types.")

        # Parse recursively with restored cluster types.
        parse_result = self.parse_recursively(
            modifiers, additional_types=cluster_types,
            no_available_types=False,
            no_available_layer_types=True,
            clusters_names=clusters_names)

        # Clean some.instance_data in created clusters.
        _clean_restored_clusters(parse_result)

        logger.debug(f"result is {parse_result}")
        logger.debug("FINISHED RESTORING CLUSTERS STATE")
        return parse_result

    # TODO: remove this
    # Wrappers
    def _parse_modifiers(self, modifiers_to_parse,
                         additional_types=None,
                         no_available_types=False,
                         clusters_names=None):
        """
        Parses modfiers_to_parse against this object's
        _available_cluster_types once.
        Object should already have
        available clusters list.

        Returns parse result list consisting of clusters.
        Returns False if not found any or cant parse
        passed modifiers list.
        Returns None, if doesnt work correctly.
        """
        if clusters_names is None:
            clusters_names = []

        logger.debug("-------------------------")
        logger.debug("Trying to parse_modifiers")
        logger.debug("-------------------------")

        cluster_types = []
        if not no_available_types:
            logger.debug("Using available cluster types.")
            cluster_types += self._get_modifiers_clusters_types()
        if additional_types is not None:
            logger.debug("Using additional cluster types.")
            compatible_additional = []
            for x in additional_types:
                if not x.has_clusters():
                    compatible_additional.append(x)
                    logger.debug(f"Using {x}")
            cluster_types += compatible_additional

        if len(modifiers_to_parse) == 0:
            logger.debug("No modifiers to parse.")
            return []

        if _WITH_BPY:
            modifier_type = bpy.types.Modifier
        elif not _WITH_BPY:
            modifier_type = DummyBlenderModifier

        if not isinstance(modifiers_to_parse[0], modifier_type):
            logger.debug("This is not an actual modifier.")
            return []

        # Skip parser and return result with default modifier clusters
        if self.__SKIP_PARSE:
            logger.debug(
                "Dont using any complex clusters.")
            result = []
            for mod in modifiers_to_parse:
                cluster = DefaultModifierCluster()
                x = []
                x.append(mod)
                if not cluster.set_this_cluster_modifiers(x):
                    return False
                result.append(cluster)
            return result

        parse_result = self._clusters_parser(modifiers_to_parse,
                                             cluster_types
                                             )

        unwrapped_result = self._unwrap_parse_result(
            parse_result, ['SKIP', 'CREATE'])

        clusters = self._initialize_clusters(unwrapped_result, clusters_names)

        return clusters

    def _parse_clusters(self, clusters_to_parse,
                        additional_types=None,
                        no_available_types=False,
                        clusters_names=None):
        """
        Parses clusters against this obect available nested cluster types.
        Object should already have
        available nested clusters types list.

        Returns parse result list consisting of clusters.
        Returns False if not found any or cant parse
        passed modifiers list.
        Returns None, if doesnt work correctly.
        """
        if clusters_names is None:
            clusters_names = []

        logger.debug("-------------------------")
        logger.debug("Trying to parse_clusters.")
        logger.debug("-------------------------")

        cluster_types = []
        if not no_available_types:
            logger.debug("Using available layer types.")
            cluster_types += self._get_clusters_layers_types()
        if additional_types is not None:
            logger.debug("Using additional layer types.")
            compatible_additional = []
            for x in additional_types:
                if x.has_clusters():
                    logger.debug(f"Using {x}")
                    compatible_additional.append(x)
            cluster_types += compatible_additional

        parse_result = self._clusters_parser(clusters_to_parse,
                                             cluster_types,
                                             )
        unwrapped_result = self._unwrap_parse_result(
            parse_result, ['SKIP', 'CREATE'])
        clusters = self._initialize_clusters(unwrapped_result, clusters_names)
        return clusters

    def _parse_clusters_recursively(self,
                                    modifiers_to_parse,
                                    additional_types=None,
                                    no_available_types=False,
                                    clusters_names=None,
                                    layers_to_create=None):
        """
        Parses clusters until there is no more
        possible cluster layers to create, unless
        number of layers_to_create specified.

        Returns parse_result as list of clusters.
        Returns False if something doesnt work.
        """
        if clusters_names is None:
            clusters_names = []

        logger.debug("-------------------------")
        logger.debug("Trying to parse_clusters_recursively.")
        logger.debug(f'additional_types {additional_types}')
        logger.debug(f'no_available_types {no_available_types}')
        logger.debug(f'clusters_names {clusters_names}')
        logger.debug(f'layers_to_create {layers_to_create}')
        if additional_types is not None:
            logger.debug("Using additional types:")
            for x in additional_types:
                logger.debug(f"{x}")

        if len(modifiers_to_parse) == 0:
            x = []
            return x

        parse_result = modifiers_to_parse

        parsing_iteration = 0
        parsing = True

        # If not specified how many layers to parse, use default number.
        if layers_to_create is None:
            max_iterations\
                = self.__RECURSIVE_PARSER_MAX_ITERATIONS
        else:
            max_iterations = layers_to_create

        # Parse clusters a lot.
        while parsing:
            old_parse_result = copy.copy(parse_result)
            parse_result = self._parse_clusters(parse_result,
                                                additional_types,
                                                no_available_types,
                                                clusters_names)
            # Compare previous iteration with this one,
            # and stop parsing if no changes.
            if old_parse_result == parse_result:
                parsing = False
            elif parsing_iteration >= (max_iterations-1):
                parsing = False
            else:
                parsing_iteration += 1
        return parse_result

    def _parse_modifiers_for_simple_clusters(self, modifiers_to_parse,
                                             additional_types=None,
                                             no_available_types=False):
        """
        Parses modfiers_to_parse against this object's
        simple _available_cluster_types.
        Object should already have
        available clusters list.

        Returns parse result list consisting of clusters.
        Returns False if not found any or cant parse
        passed modifiers list.
        Returns None, if doesnt work correctly.
        """
        e = copy.copy(modifiers_to_parse)
        cluster_types = []
        if not no_available_types:
            cluster_types += self._get_modifiers_clusters_types()
        if additional_types is not None:
            compatible_additional = []
            for x in additional_types:
                if x.has_clusters():
                    compatible_additional.append(x)
            cluster_types += compatible_additional

        simple_clusters = []
        for x in cluster_types:
            if x.get_this_cluster_possible_length() == 1:
                # TODO: probably no need to do that
                y = copy.deepcopy(x)
                simple_clusters.append(y)

        parse_result = self._clusters_parser(e,
                                             simple_clusters
                                             )
        unwrapped_result = self._unwrap_parse_result(parse_result, ['CREATE'])
        clusters = self._initialize_clusters(unwrapped_result)
        return clusters

    # Cluster types

    def update_cluster_types(self, cluster_type_to_add):
        """Adds cluster type to available cluster types"""
        if not isinstance(cluster_type_to_add, ClusterTrait):
            raise TypeError

        cluster_type = copy.deepcopy(cluster_type_to_add)
        logger.info("Trying to update cluster types list")
        logger.info(cluster_type)

        # Check for duplicates.
        for x in copy.copy(self.available_cluster_types):
            if x.get_this_cluster_default_name()\
                    == cluster_type.get_this_cluster_default_name():
                if self.__REPLACE_ON_UPDATE:
                    self.available_cluster_types.remove(x)
                else:
                    raise ValueError

        # If sanity checks are enabled
        if self.__CLUSTERS_SANITY_CHECKS:
            # Check cluster for any usual errors
            if cluster_type.check_this_cluster_sanity():
                self.available_cluster_types.append(cluster_type)
                cluster_type.modcluster_index\
                    = self._get_new_cluster_type_index()
                result = True

            # If modcluster cant be used
            else:
                raise ValueError
        else:
            cluster_type.modcluster_index\
                = self._get_new_cluster_type_index()
            self.available_cluster_types.append(cluster_type)
            result = True

        logger.info("Modifiers cluster availability is {}", result)
        logger.info("Finished updating cluster types list")
        logger.info(" ")
        return result

    def get_cluster_type_by_name(self, cluster_type_name):
        """
        Returns one of available to this object cluster
        types by name.
        """
        logger.debug(
            f"Trying to find cluster type by name {cluster_type_name}")
        for x in self.available_cluster_types:
            if x.name == cluster_type_name:
                return x
        raise ValueError(
            f"Cant find cluster with name {cluster_type_name}\
                        in {self.available_layer_types}")

    def get_cluster_type_by_type(self, cluster_type):
        """
        Returns one of available to this object cluster
        types by type.
        """
        logger.debug(
            f"Trying to find cluster type by type {cluster_type}")
        for x in self.available_cluster_types:
            if x.type == cluster_type:
                return x
        raise ValueError(
            f"Cant find cluster with type {cluster_type}\
                        in {self.available_layer_types}")

    def _unwrap_saved_clusters_state(self, clusters_state):
        """
        Returns clusters instances that are specified
        for reconstructing clusters.
        """
        result = []
        logger.debug("-------------------------")
        logger.debug("Unwrapping clusters state")

        for x in clusters_state:
            logger.debug("Trying to create cluster type ")
            logger.debug(f"{x}")
            cluster_info = x[0]
            cluster_name = cluster_info[1]

            if not isinstance(cluster_name, str):
                raise ValueError

            # Get cluster with default name that was saved.
            default_cluster_type = self.get_cluster_type_by_name(cluster_name)
            logger.debug(f"found {default_cluster_type}")

            # Get a copy of cluster type to modifiy it for later
            # use in parser.
            cluster_type = copy.deepcopy(default_cluster_type)

            # Clear custom modifiers names, if any.
            cluster_type.instance_data['by_name'] = []

            # Add custom modifier names to make sure correct modifier
            # will be used in parse.
            for mod in x[1]:
                modifier_names = []
                modifier_names.append(mod[3])
                cluster_type.instance_data['by_name'].append(
                    modifier_names)

            # Check if length is correct
            if len(cluster_type.instance_data['by_name']) \
                    != cluster_type.get_this_cluster_possible_length():
                logger.debug(
                    "Specified names list length is wrong.")
                raise ValueError

            cluster_names = cluster_type.instance_data['by_name']
            logger.debug(f"Modifiers names {cluster_names}")

            # Set custom cluster name.
            cluster_type.set_this_cluster_custom_name(cluster_info[3])

            # Add 'RESTORED' tag.
            logger.debug(f"Adding tag to {cluster_type}")
            cluster_type.add_tag_to_this_cluster('RESTORED')

            # Set index for new cluster type.
            cluster_type.modcluster_index = self._get_new_cluster_type_index()

            # Add cluster type to result.
            result.append(cluster_type)
        return result

    # Parser
    # =============================
    #
    #       CLUSTERS PARSER
    #
    # =============================

    def _clusters_parser(self, mods,
                         available_to_parser_cluster_types, *,
                         max_iterations=2000,
                         parser_sanity_checks=True
                         ):
        """
        Parses modifiers_to_parse for available_to_parser_cluster_types.

        It doesnt require modifiers to be actual modifiers.
        Difference between actual modifiers and clusters in parsing
        can be defined in cluster's check_availability method, or
        any additional method that it uses.
        Adds modifiers that was unable to parse to parse result.

        Returns parse_result consisting of lists with action
        that parser decided that should be done to cluster,
        cluster type instance and actual modifiers to add to it.

        Action can be either 'SKIP' or 'CREATE'.

        Example of parse_result:
        [['SKIP', TripleBevel, None],
        ['CREATE', DefaulModifiersCluster, [bevel, bevel]]]

        Returns empty list if doesnt work correctly.
        """

        if not isinstance(mods, list):
            logger.error("modifiers_to_parse is not a list.")
            raise TypeError

        if len(mods) == 0:
            logger.info("modifiers_to_parse is 0 modifiers long.")
            return []

        modifiers_to_parse = copy.copy(mods)
        if len(available_to_parser_cluster_types) == 0:
            logger.info("No cluster types available to parser, skipping all.")
            result = []
            for modifier in modifiers_to_parse:
                result.append(['SKIP', modifier, None])
            return result

        # Only use default modifier cluster in parsing
        if self.__DEFAULT_CLUSTERS:
            available_to_parser_cluster_types = []
            cluster = DefaultModifierCluster()
            available_to_parser_cluster_types.append(cluster)

        # Info
        if logger.isEnabledFor(logging.DEBUG):
            for x in modifiers_to_parse:
                logger.debug(f"{x}")

            logger.debug("===================================")
            logger.debug("       CLUSTERS PARSER LOG")
            logger.debug("===================================")
            logger.debug(f"libemtk_VERSION: {libemtk_VERSION}")
            logger.debug(f"CLUSTERS_PARSER_VERSION: {CLUSTERS_PARSER_VERSION}")
            logger.debug("Modifiers to parse:")
            logger.debug(modifiers_to_parse)
            logger.debug(" ")
            logger.debug("Available cluster types:")
            for x in available_to_parser_cluster_types:
                logger.debug("-------")
                logger.debug(
                    f"{x.default_data['type']}")
                logger.debug(
                    f"{x.get_this_cluster_tags()}")
                logger.debug(
                    f"{x}, {len(x.default_data['by_name'])} mods")
                logger.debug(
                    f"{x.default_data['by_type']}")
                logger.debug(
                    f"{x.default_data['by_name']}")
                logger.debug(
                    f"priority is {x.default_data['priority']}")
                logger.debug(" ")

        # Variables
        # if _WITH_BPY:
        #     modifier_type = bpy.types.Modifier
        # elif not _WITH_BPY:
        #     modifier_type = DummyBlenderModifier

        # # TODO: this doesnt works as expected
        # # idk why
        # # Actual modifiers before parsing
        # old_actual_modifiers = []

        # # Sanity checks
        # if parser_sanity_checks:
        #     # Get actual modifiers before parsing for sanity check
        #     for x in modifiers_to_parse:
        #         if isinstance(x, modifier_type):
        #             old_actual_modifiers.append(x)
        #         else:
        #             y = copy.copy(x.all_modifiers())
        #             old_actual_modifiers.extend(y)

        # Returned parse result
        parse_result = []

        # Previous iteration result
        # One of SUCCESS, POSSIBLE, FOUND or False
        iteration_result = None

        # Sequence of modifiers that currently being
        # parsed inside iteration loop
        parsed_modifiers = []

        # Types of clusters that wanted to continue to parse
        # this sequence
        possible_cluster_types = []

        # Types of clusters that can be created for this sequence
        # of modifiers, starting from first
        possible_clusters_confirmed = []

        # List of clusters to remove from possible_cluster_types
        clusters_to_remove = []

        # Should always be true at loop beginning
        need_another_modifier = True

        # Iteration counter
        parse_iteration = 0

        # False, if no modifiers left to parse
        parsing_modifiers = True

        # Iterate over modifiers or clusters
        while parsing_modifiers:
            logger.debug(f"Parse iteration {parse_iteration}")

            # Parser sanity checks
            if parser_sanity_checks:
                if len(possible_clusters_confirmed) > len(
                        available_to_parser_cluster_types):
                    raise ValueError("Too many possible clusters")
                elif len(possible_cluster_types) > len(
                        available_to_parser_cluster_types):
                    raise ValueError("Too many possible clusters")
                elif need_another_modifier is False:
                    raise ValueError(
                        "Parser doesnt need another modifier? Why?")
                elif parse_iteration\
                        >= max_iterations:
                    raise ValueError("Parsing failed, too many iterations")

            # Add modifier to sequence
            modifier = modifiers_to_parse.pop(0)
            logger.debug(f"Adding modifier to sequence {modifier}")
            parsed_modifiers.append(modifier)
            need_another_modifier = False

            # True if parser added cluster from parsed_modifiers
            # to parse_result without successfully parsing it
            # while parsing clusters
            skipped_modifier = False

            # Info
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug("Currently parsed modifiers:")
                logger.debug(parsed_modifiers)
                logger.debug("All modifiers to parse:")
                logger.debug(modifiers_to_parse)
                logger.debug("Current potentially possible cluster types:")
                logger.debug(possible_cluster_types)
                logger.debug("Current confirmed possible cluster types:")
                logger.debug(possible_clusters_confirmed)
                logger.debug(
                    f"Previous iteration result was '{iteration_result}'")

            # Decide what clusters types to use in checking
            if iteration_result == 'SUCCESS' or parse_iteration == 0:
                clusters_to_parse_against = available_to_parser_cluster_types
            elif iteration_result == 'POSSIBLE':
                clusters_to_parse_against = possible_cluster_types

            # =================
            # Checking clusters
            # =================
            # Check cluster types for compatibility with this sequence
            # of modifiers.
            for y in clusters_to_parse_against:
                possible_seq_len = len(modifiers_to_parse)\
                    + len(parsed_modifiers)

                cluster_len = len(y.default_data['by_type'])

                # Check if cluster is too long.
                if possible_seq_len < cluster_len:
                    result = False
                    logger.debug("Cant use {y.name}, not enough modifiers.")
                else:
                    result = y.check_availability(parsed_modifiers)
                    logger.debug(f"Checking {y.name}, {result}")

                # Cluster need more modifiers than provided.
                if result == 'CONTINUE':
                    logger.debug(f"Parsing, {y} need another modifier")

                    if y not in possible_cluster_types:
                        # TODO: this is slow
                        new_cluster = copy.deepcopy(y)
                        possible_cluster_types.append(new_cluster)
                        logger.debug(f"Adding {y} to possible types")
                    else:
                        logger.debug(f"{y} is already in possible types")

                    need_another_modifier = True

                # Cluster can be used with this sequence.
                elif result == 'FOUND':
                    logger.debug(f"Cluster {y} can be used")

                    # Get a copy of cluster type and add it to possible
                    # cluster types.
                    new_cluster = copy.deepcopy(y)
                    possible_clusters_confirmed.append(new_cluster)

                    # If there even a cluster
                    # to delete from possible_cluster_types
                    # Basically if modcluster is complex, this is true
                    if iteration_result == 'POSSIBLE':
                        clusters_to_remove.append(y)

                # Cluster cant be used.
                else:
                    logger.debug("This cluster type cant be used")

                    if iteration_result == 'POSSIBLE':
                        clusters_to_remove.append(y)

            # Removing not compatible with this modifiers sequence
            # clusters from possible types.
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(
                    f"possible_cluster_types: {possible_cluster_types}")
                logger.debug(f"Deleting {clusters_to_remove}")
            for x in clusters_to_remove:
                possible_cluster_types.remove(x)
            clusters_to_remove.clear()

            # Cluster creation
            # If allowed to skip cluster or modifier if no cluster can be
            # created at all, and add it to result.
            # Then request another modifier.
            if len(possible_cluster_types) == 0\
                    and len(possible_clusters_confirmed) == 0:
                for x in parsed_modifiers:
                    parsed_cluster_wrap = ['SKIP',
                                           x, None]
                    parse_result.append(parsed_cluster_wrap)
                parsed_modifiers.clear()
                need_another_modifier = True
                skipped_modifier = True
                iteration_result = 'SUCCESS'

            # If parser doesnt need another loop to decide what cluster to add
            elif need_another_modifier is False:
                logger.debug(" ")
                logger.debug(
                    "Trying to create new cluster")
                logger.debug("Parsed modifiers:")
                logger.debug(parsed_modifiers)

                # Priority select
                cluster_to_add = self._cluster_priority_select(
                    possible_clusters_confirmed)
                logger.debug(
                    f"Decided to create {cluster_to_add}")

                # Select modifiers to add to clusters:
                modifiers_count =\
                    cluster_to_add.get_this_cluster_possible_length()
                logger.debug(
                    f"It needs {modifiers_count} modifiers")
                logger.debug(
                    f"parsed_modifiers are {len(parsed_modifiers)}")

                modifiers_to_add_to_cluster = []

                # Add modifiers to cluster
                for i in range(modifiers_count):
                    mod = parsed_modifiers.pop(0)
                    logger.debug(f"Deleted {mod} from modifiers_to_parse")
                    modifiers_to_add_to_cluster.append(mod)
                    logger.debug("Added it to modifiers_to_add_to_cluster")

                # Add not parsed modifiers back to modifiers_to_parse
                if len(parsed_modifiers) > 0:
                    logger.debug(f"{len(parsed_modifiers)} not parsed")
                    for x in reversed(parsed_modifiers):
                        logger.debug(f"Adding {x} back to modifiers_to_parse")
                        modifiers_to_parse.insert(0, x)
                    parsed_modifiers.clear()
                    logger.debug("Cleared parsed modifiers list")

                # TODO: this is slow
                # new_cluster = copy.deepcopy(cluster_to_add)
                new_cluster = cluster_to_add

                # Clear possible clusters list
                possible_clusters_confirmed.clear()

                # Add cluster to return list
                # parse_result.append(new_cluster)
                parsed_cluster_wrap = ['CREATE',
                                       new_cluster,
                                       modifiers_to_add_to_cluster]
                parse_result.append(parsed_cluster_wrap)

                logger.debug("Added new cluster to result.")
                logger.debug(" ")

                need_another_modifier = True
                iteration_result = 'SUCCESS'

            # Parser needs another modifier
            elif need_another_modifier is True:
                logger.debug("Parser needs another modifier")
                iteration_result = 'POSSIBLE'
            else:
                raise ValueError("Something is wrong with cluster creation")

            # Info
            if iteration_result == 'SUCCESS':
                logger.debug("Iteration successfull")
                if skipped_modifier:
                    logger.debug("Skipped cluster")
                else:
                    logger.debug("Added new cluster")
            elif iteration_result == 'POSSIBLE':
                logger.debug("Iteration failed, possible cluster types found")
            else:
                raise ValueError("Something is wrong with iteration result")
            logger.debug("")

            # Decide if should continue parsing
            if len(modifiers_to_parse) == 0:
                need_another_modifier = False
                parsing_modifiers = False
            else:
                need_another_modifier = True
            parse_iteration += 1

        # Parse result sanity check
        if parser_sanity_checks:
            if type(parse_result) is not list:
                raise ValueError("Expected parse_result to be a list.")
            else:
                for x in parse_result:
                    if not isinstance(x[1], ClusterTrait):
                        raise ValueError(
                            "Expeced parse_result to have clusters in it.")
                if len(parse_result) == 0:
                    raise ValueError(
                        "Expected parse_result with at least one element.")

            # new_actual_modifiers = []

            # # Get actual modifiers after parsing for sanity check
            # for x in parse_result:
            #     if x[0] == 'SKIP':
            #         y2 = x[1].all_modifiers()
            #         y = copy.copy(y2)
            #         new_actual_modifiers.extend(y)
            #     else:
            #         if not x[1].has_clusters():
            #             y = copy.copy(x[2])
            #             new_actual_modifiers.append(y)

            # old_modifiers_len = len(old_actual_modifiers)
            # new_modifiers_len = len(new_actual_modifiers)

            # # Modifiers count is wrong.
            # if old_modifiers_len != new_modifiers_len:
            #     logger.error(
            #             "Actual modifiers count after parsing is wrong.")
            #     logger.error(old_modifiers_len)
            #     logger.error(new_modifiers_len)
            #     e = []
            #     for a_mod in old_actual_modifiers:
            #         if a_mod not in new_actual_modifiers:
            #             e.append(a_mod)
            #     logger.error(f'Missing modifiers: {e}')

            #     # TODO: this throws an error
            #     # but i kinda feel like its because
            #     # of sanity check itself
            #     # raise ValueError(
            #     #         "Actual modifiers count after parsing is wrong.")

        # Info
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("-------------")
            logger.debug("Parse result:")
            logger.debug(parse_result)
            logger.debug("===================================")
            logger.debug("         Finished parsing")
            logger.debug("===================================")
            logger.debug(" ")

        return parse_result

    def _cluster_priority_select(self, clusters):
        """
        Takes list of clusters as an argument.
        Returns cluster that have higher priority when
        deciding what cluster to create.
        """
        logger.debug("Selecting cluster.")

        # Highest priority.
        priority = clusters[0].get_this_cluster_priority()

        # Longest.
        length = clusters[0].get_this_cluster_possible_length()

        # Restored cluster length.
        length_2 = None

        result = clusters[0]

        found_restored_cluster = False

        # Get first restored cluster
        for x in clusters:
            if 'RESTORED' in x.get_this_cluster_tags():
                logger.debug("Selected RESTORED cluster.")
                length_2 = x.get_this_cluster_possible_length()
                result = x
                found_restored_cluster = True
                break

        # If no restored clusters, use priority.
        if not found_restored_cluster:
            for x in clusters:
                # If cluster has higher priority.
                if x.get_this_cluster_priority() > priority:

                    # And longer or same length.
                    if x.get_this_cluster_possible_length() >= length:
                        priority = x.get_this_cluster_priority()
                        length = x.get_this_cluster_possible_length()
                        result = x

                # Or it is just longer.
                elif x.get_this_cluster_possible_length() > length:
                    priority = x.get_this_cluster_priority()
                    length = x.get_this_cluster_possible_length()
                    result = x

        # If restored clusters, only use length
        else:
            for x in clusters:
                logger.debug(
                    f"Checking {x}, its tags is")
                logger.debug(
                    f"{x.get_this_cluster_tags()}")
                if 'RESTORED' in x.get_this_cluster_tags():
                    if x.get_this_cluster_possible_length() > length_2:
                        length_2 = x.get_this_cluster_possible_length()
                        result = x

        logger.debug(f"Selected {result} cluster.")
        logger.debug(f"{result.get_this_cluster_tags()}")
        return result

    # Parse result processing

    def _unwrap_parse_result(self, parse_result, tags):
        """
        Returns parse result filtered by parser decision.
        Returns False, if any errors in parse result.
        """
        unwrap = []
        if type(parse_result) is not list:
            return False
        for x in parse_result:
            # Check if element is a list.
            if type(x) is not list:
                return False
            # Check if it has parser decision already
            if type(x[0]) is not str:
                return False
            if x[0] in tags:
                unwrap.append(x)
        return unwrap

    def _initialize_clusters(self, parse_result, clusters_names=None):
        """
        Set clusters modifiers. Parse result should be in form of
        list of lists with cluster type object and modifiers.

        Returns ready to be put into modifiers list clusters.
        Returns False, if error while setting modifiers.
        """
        if clusters_names is None:
            clusters_names = []

        logger.debug("---------------------")
        logger.debug("Initializing clusters.")

        # Clusters list that will be returned.
        clusters = []

        if type(parse_result) is not list:
            raise TypeError
        # Check if no clusters were parsed.
        if len(parse_result) == 0:
            return clusters

        new_clusters_names = copy.copy(clusters_names)
        for x in parse_result:
            logger.debug(f"Initializing {x}")

            # Check if element is a list.
            if type(x) is not list:
                raise TypeError

            # If parser skipped this cluster, just skip it as well.
            if x[0] == 'SKIP':
                logger.debug("Skipped cluster")
                clusters.append(x[1])

            # If parsed successfully.
            elif x[0] == 'CREATE':
                logger.debug("Creating cluster")

                # Initialize cluster
                cluster = self._initialize_cluster(
                    x, new_clusters_names)
                if cluster is False:
                    return False

                new_clusters_names.append(cluster[1].get_this_cluster_name())

                # Add to result
                clusters.append(x[1])

        logger.debug("Created clusters: ")
        for x in clusters:
            logger.debug(f"{x}")

        return clusters

    def _initialize_cluster(
            self, parse_result_element, clusters_names=None):
        logger.debug("Initializing cluster")
        x = parse_result_element

        if clusters_names is None:
            clusters_names = []

        if not x[1].set_this_cluster_modifiers(x[2]):
            raise ValueError
        x[1]._object = self._object
        x[1]._mod = x[1][0]
        cluster_number_format(x[1], clusters_names)
        x[1]._controller = self._controller
        x[1]._clusters_parser = self
        return x

    # TODO: remove this

    def _get_new_cluster_type_index(self):
        """Returns unique for this parser cluster type index."""
        self._last_cluster_type_index += 1
        return self._last_cluster_type_index - 1


# UTILS
def _get_clusters_names(clusters):
    """Returns list of custom names from list of clusters."""
    result = []
    for x in clusters:
        result.append(x.get_this_cluster_name())
    return result


def cluster_number_format(
        cluster, clusters_names=None):
    """Changes cluster's custom name, if cluster with same default
    of custom name exists in clusters list.

    Returns cluster with changed name.
    """

    if clusters_names is None:
        clusters_names = []

    # DefaultModifierCluster cant have duplicated name already
    if isinstance(cluster, DefaultModifierCluster):
        return cluster

    # If it already have custom name for whatever reason
    if cluster.get_this_cluster_name()\
            == cluster.get_this_cluster_custom_name():
        return cluster

    # Number of clusters with this name
    y = 0

    # String to add to cluster name
    e = cluster.get_this_cluster_name()

    # Find existing clusters with similar name
    for x in clusters_names:
        if e in x:
            y += 1

    # Formats name to "cluster_name.cluster_number"
    e += "."
    if y <= 100:
        e += "0"
    if y <= 10:
        e += "0"
    e += f"{y}"
    cluster.set_this_cluster_custom_name(e)
    return cluster


def _clean_restored_clusters(clusters):
    """Remove restored clusters attributes that are
    only required during parse."""
    for x in clusters:
        x.remove_tag_from_this_cluster('RESTORED')
        x.instance_data['by_name'] = []
    return clusters
