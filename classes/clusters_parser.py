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

import bpy

from .clusters import DefaultModifierCluster, ModifierCluster


class ClustersParser():
    """
    Base class for objects that should be able to parse clusters.
    """

    # Max amount of iterations for _parse_modifiers_recursively
    # Can also be interpreted as max amount of layers.
    __RECURSIVE_PARSER_MAX_ITERATIONS = 10

    # Skip parser and sanity checks, only use default cluster.
    __SKIP_PARSE = False

    # Only use default cluster, but dont skip parser.
    __DEFAULT_CLUSTERS = False

    # Use only simple clusters on first recursive
    # parse iteration. Basically, this makes it
    # so that every cluster that was using multiple
    # modifiers now using multiple simple clusters.
    __SIMPLE_CLUSTERS = False

    # Check clusters for errors.
    __CLUSTERS_SANITY_CHECKS = True

    # Replace available cluster types when updaing existing one.
    __REPLACE_ON_UPDATE = True

    # Additional info.
    _MODIFIERS_LIST_V = True

    def __init__(self):
        # Additional info.
        self._additional_info_log = []

        # Available to object cluster types.
        self._available_cluster_types = []

        # Available to object nested cluster types.
        self._available_layer_types = []

        # Last new cluster type index.
        self._last_cluster_type_index = 1

    # =============================
    # Parse_result is a list
    # of lists with string, cluster
    # and modifiers.
    # =============================
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
        Returns False if cant parse for some reason.
        """
        if clusters_names is None:
            clusters_names = []

        # Check if passed list have modifiers
        if isinstance(modifiers_to_parse[0], bpy.types.Modifier):

            # Parse modifiers once.
            if self._ClustersParser__SIMPLE_CLUSTERS:
                parse_result = self._parse_modifiers_for_simple_clusters(
                        modifiers_to_parse)
                if parse_result is False:
                    return False
            else:
                self._additional_info_log.append("Trying to parse modifiers")
                parse_result = self._parse_modifiers(modifiers_to_parse,
                                                     additional_types,
                                                     no_available_types,
                                                     clusters_names)
                if parse_result is False:
                    self._additional_info_log.append("=====================")
                    self._additional_info_log.append(
                            "Error while parsing modifiers")
                    self._additional_info_log.append("=====================")
                    return False

            clusters_names += self._get_clusters_names(parse_result)

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

        self._additional_info_log.append("========================")
        self._additional_info_log.append("RESTORING CLUSTERS STATE")
        self._additional_info_log.append("========================")

        # Get cluster types from saved clusters_state.
        cluster_types = self._unwrap_saved_clusters_state(clusters_state)

        # Check that it was restored correctly
        if cluster_types is False or cluster_types is None:
            self._additional_info_log.append(
                    "Something is wrong with restoring cluster types")
            return False
        elif len(cluster_types) == 0:
            self._additional_info_log.append(
                    "Found no cluster types.")
            return False
        else:
            self._additional_info_log.append(
                    f"Found {len(cluster_types)} cluster types.")

        # Parse recursively with restored cluster types.
        parse_result = self.parse_recursively(
                modifiers, additional_types=cluster_types,
                no_available_types=False,
                no_available_layer_types=True,
                clusters_names=clusters_names)

        # Clean some variables in created clusters.
        self._clean_restored_clusters(parse_result)

        self._additional_info_log.append("result is ")
        for x in parse_result:
            self._additional_info_log.append(f"{x}")

        self._additional_info_log.append("========================")
        self._additional_info_log.append("FINISHED RESTORING CLUSTERS STATE")
        self._additional_info_log.append("========================")
        return parse_result

    def update_cluster_types_list(self, cluster_type_to_add):
        """
        Adds cluster type to _available_cluster_types or
        _available_layer_types, depending on ModifierCluster
        subclass.

        Returns True if added
        Returns False if cant be added
        """

        cluster_type = copy.deepcopy(cluster_type_to_add)
        # cluster_type = cluster_type_to_add

        ui_t = []
        ui_t.append("-----------------------------------")
        ui_t.append("Trying to update cluster types list")

        y = None

        # Check for duplicates.
        for x in self._available_cluster_types:
            if x.get_this_cluster_default_name()\
                    == cluster_type.get_this_cluster_default_name():
                if self._ClustersParser__REPLACE_ON_UPDATE:
                    y = x
                else:
                    return False

        # Delete duplicate
        if y is not None:
            self._available_cluster_types.remove(y)

        y = None

        # Check for duplicates in layers.
        for x in self._available_layer_types:
            if x.get_this_cluster_default_name()\
                    == cluster_type.get_this_cluster_default_name():
                if self._ClustersParser__REPLACE_ON_UPDATE:
                    y = x
                else:
                    return False

        # Delete duplicate in layers.
        if y is not None:
            self._available_layer_types.remove(y)

        # If sanity checks are enabled
        if self._ClustersParser__CLUSTERS_SANITY_CHECKS:
            # Check cluster for any usual errors
            if cluster_type.check_this_cluster_sanity():
                if cluster_type.has_clusters():
                    self._available_layer_types.append(cluster_type)
                else:
                    self._available_cluster_types.append(cluster_type)

                cluster_type.modcluster_index\
                    = self._get_new_cluster_type_index()
                result = True

            # If modcluster cant be used
            else:
                result = False
        else:
            cluster_type.modcluster_index\
                    = self._get_new_cluster_type_index()
            if cluster_type.has_clusters():
                self._available_layer_types.append(cluster_type)
            else:
                self._available_cluster_types.append(cluster_type)
            result = True

        ui_t.append(f"Modifiers cluster availability is {result}")
        ui_t.append("Finished updating cluster types list")
        ui_t.append("-----------------------------------")
        ui_t.append(" ")
        for line in ui_t:
            self._additional_info_log.append(line)
        return result

    def _get_new_cluster_type_index(self):
        self._last_cluster_type_index += 1
        return self._last_cluster_type_index - 1

    # ==============================
    # cluster types
    # ===============================
    def _get_cluster_type_by_name(self, cluster_type_name):
        """
        Returns one of available to this object cluster
        types by name.
        Return False, if not found any.
        """
        self._additional_info_log.append(
                f"Trying to find cluster type by name {cluster_type_name}")
        for x in self._available_cluster_types:
            if x.get_this_cluster_default_name() == cluster_type_name:
                self._additional_info_log.append(
                        f"Found {x}")
                return x
        for x in self._available_layer_types:
            if x.get_this_cluster_default_name() == cluster_type_name:
                self._additional_info_log.append(
                        f"Found {x}")
                return x
        self._additional_info_log.append(
                "Dont found any")
        return False

    def _get_cluster_type_by_type(self, cluster_type):
        """
        Returns one of available to this object cluster
        types by type.
        Return False, if not found any.
        """
        self._additional_info_log.append(
                f"Trying to find cluster type by type {cluster_type}")
        for x in self._available_cluster_types:
            if x.get_this_cluster_type == cluster_type:
                self._additional_info_log.append(
                        f"Found {x}")
                return x
        for x in self._available_layer_types:
            if x.get_this_cluster_type == cluster_type:
                self._additional_info_log.append(
                        f"Found {x}")
                return x
        self._additional_info_log.append(
                "Dont found any")
        return False

    # ==============================
    # Wrappers
    # ===============================
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

        self._additional_info_log.append("-------------------------")
        self._additional_info_log.append("Trying to parse_modifiers")
        self._additional_info_log.append("-------------------------")

        cluster_types = []
        if not no_available_types:
            self._additional_info_log.append("Using available cluster types.")
            cluster_types += self._available_cluster_types
        if additional_types is not None:
            self._additional_info_log.append("Using additional cluster types.")
            compatible_additional = []
            for x in additional_types:
                if not x.has_clusters():
                    compatible_additional.append(x)
                    self._additional_info_log.append(f"Using {x}")
            cluster_types += compatible_additional

        if len(modifiers_to_parse) == 0:
            self._additional_info_log.append("No modifiers to parse.")
            return []

        if not isinstance(modifiers_to_parse[0], bpy.types.Modifier):
            self._additional_info_log.append("This is not an actual modifier.")
            return []

        # Skip parser and return result with default modifier clusters
        if self._ClustersParser__SKIP_PARSE:
            self._additional_info_log.append(
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

        self._additional_info_log.append("-------------------------")
        self._additional_info_log.append("Trying to parse_clusters.")
        self._additional_info_log.append("-------------------------")

        cluster_types = []
        if not no_available_types:
            self._additional_info_log.append("Using available layer types.")
            cluster_types += self._available_layer_types
        if additional_types is not None:
            self._additional_info_log.append("Using additional layer types.")
            compatible_additional = []
            for x in additional_types:
                if x.has_clusters():
                    self._additional_info_log.append(f"Using {x}")
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

        self._additional_info_log.append("-------------------------")
        self._additional_info_log.append(
                "Trying to parse_clusters_recursively.")
        if additional_types is not None:
            for x in additional_types:
                self._additional_info_log.append("Using additional types:")
                self._additional_info_log.append(f"{x}")

        if len(modifiers_to_parse) == 0:
            x = []
            return x

        parse_result = modifiers_to_parse

        parsing_iteration = 0
        parsing = True

        # If not specified how many layers to parse, use default number.
        if layers_to_create is None:
            max_iterations\
                    = self._ClustersParser__RECURSIVE_PARSER_MAX_ITERATIONS
        else:
            max_iterations = layers_to_create

        new_clusters_names = []

        # Parse clusters a lot.
        while parsing:
            # Get a copy of old parse result.
            old_parse_result = copy.copy(parse_result)

            # Parse again.
            parse_result = self._parse_clusters(parse_result,
                                                additional_types,
                                                no_available_types,
                                                clusters_names)

            # If parser doesnt work.
            if parse_result is False or None:
                self._additional_info_log.append("=====================")
                self._additional_info_log.append(
                        "Error while parsing clusters")
                self._additional_info_log.append("=====================")
                return False

            new_clusters_names += self._get_clusters_names(parse_result)

            # Old clusters.
            old_cluster_types = []
            for x in old_parse_result:
                old_cluster_types.append(x.get_this_cluster_type())

            # New clusters.
            new_cluster_types = []
            for x in parse_result:
                new_cluster_types.append(x.get_this_cluster_type())

            # Compare previous iteration with this one,
            # and stop parsing if no changes.
            # TODO: remove this
            if old_parse_result == parse_result:
                parsing = False
            elif old_cluster_types == new_cluster_types:
                parsing = False
            elif parsing_iteration >= (max_iterations-1):
                parsing = False
            else:
                parsing_iteration += 1

        return parse_result

    # ===================
    # Loading clusters state
    # ====================
    # TODO: move to util
    def _unwrap_saved_clusters_state(self, clusters_state):
        """
        Returns clusters instances that are specified
        for reconstructing clusters.
        """
        result = []
        self._additional_info_log.append("-------------------------")
        self._additional_info_log.append("Unwrapping clusters state")

        for x in clusters_state:
            self._additional_info_log.append("Trying to create cluster type ")
            self._additional_info_log.append(f"{x}")
            cluster_info = x[0]
            cluster_name = cluster_info[1]

            # Get cluster with default name that was saved.
            default_cluster_type = self._get_cluster_type_by_name(cluster_name)
            self._additional_info_log.append(f"found {default_cluster_type}")

            # Get a copy of cluster type to modifiy it for later
            # use in parser.
            cluster_type = copy.deepcopy(default_cluster_type)

            # Clear custom modifiers names, if any.
            cluster_type._modcluster_specified_modifier_names = []

            # Add custom modifier names to make sure correct modifier
            # will be used in parse.
            for mod in x[1]:
                modifier_names = []
                modifier_names.append(mod[3])
                cluster_type._modcluster_specified_modifier_names.append(
                        modifier_names)

            # Check if length is correct
            if len(cluster_type._modcluster_specified_modifier_names) \
                    != cluster_type.get_this_cluster_possible_length():
                self._additional_info_log.append(
                        "Specified names list length is wrong.")
                return False

            cluster_names = cluster_type._modcluster_specified_modifier_names
            self._additional_info_log.append(
                    f"Modifiers names {cluster_names}")

            # Set custom cluster name.
            cluster_type.set_this_cluster_custom_name(cluster_info[3])

            # Add 'RESTORED' tag.
            self._additional_info_log.append(
                    f"Adding tag to {cluster_type}")
            cluster_type.add_tag_to_this_cluster('RESTORED')

            # Set index for new cluster type.
            cluster_type.modcluster_index = self._get_new_cluster_type_index()

            # Add cluster type to result.
            result.append(cluster_type)

        return result

    def _clean_restored_clusters(self, clusters):
        """
        Remove restored clusters attributes that are
        only required during parse.
        """
        for x in clusters:
            x.remove_tag_from_this_cluster('RESTORED')
            x._modcluster_specified_modifier_names = []

    # =============================
    #
    #       CLUSTERS PARSER
    #
    # =============================
    def _clusters_parser(self, mods,
                         available_to_parser_cluster_types, *,
                         max_iterations=200,
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
            self._additional_info_log.append(
                    "modifiers_to_parse is not a list.")
            x = []
            return x

        if len(mods) == 0:
            self._additional_info_log.append(
                    "modifiers_to_parse is 0 modifiers long.")
            x = []
            return x

        modifiers_to_parse = copy.copy(mods)

        if len(available_to_parser_cluster_types) == 0:
            self._additional_info_log.append(
                    "No cluster types available to parser, skipping all.")
            result = []
            for modifier in modifiers_to_parse:
                e = []
                e.append('SKIP')
                e.append(modifier)
                e.append(None)
                result.append(e)
            return result

        # Only use default modifier cluster in parsing
        if self._ClustersParser__DEFAULT_CLUSTERS:
            available_to_parser_cluster_types = []
            cluster = DefaultModifierCluster()
            available_to_parser_cluster_types.append(cluster)

        # Returned parse result
        parse_result = []

        # Previous iteration result
        # One of SUCCESS, POSSIBLE, FOUND or False
        iteration_result = None

        # Info
        self._additional_info_log.append("===================================")
        self._additional_info_log.append("       CLUSTERS PARSER LOG")
        self._additional_info_log.append("===================================")
        self._additional_info_log.append("Modifiers to parse:")
        if isinstance(modifiers_to_parse[0], bpy.types.Modifier):
            for x in modifiers_to_parse:
                self._additional_info_log.append(f"{x}")
        elif isinstance(modifiers_to_parse[0], ModifierCluster):
            for x in modifiers_to_parse:
                self._additional_info_log.append(
                        f"{x._modcluster_specified_modifier_names}")
                self._additional_info_log.append(
                        f"{x.get_this_cluster_tags()}")
                self._additional_info_log.append(f"{x}")
        self._additional_info_log.append(" ")
        self._additional_info_log.append("Available cluster types:")
        for x in available_to_parser_cluster_types:
            self._additional_info_log.append("-------")
            self._additional_info_log.append(
                    f"{x.get_this_cluster_tags()}")
            self._additional_info_log.append(
                    f"{x}, {len(x._MODCLUSTER_MODIFIERS_BY_TYPE)} mods")
            self._additional_info_log.append(
                    f"{x._MODCLUSTER_MODIFIERS_BY_TYPE}")
            self._additional_info_log.append(
                    f"{x._MODCLUSTER_MODIFIERS_BY_POSSIBLE_NAMES}")
            self._additional_info_log.append(
                    f"{x._modcluster_specified_modifier_names}")
            self._additional_info_log.append(
                    f"modcluster priority is {x._MODCLUSTER_PRIORITY}")
            self._additional_info_log.append(" ")

        # Actual modifiers before parsing
        old_actual_modifiers = []

        # Sanity checks
        if parser_sanity_checks:
            if len(modifiers_to_parse) < 1:
                self._additional_info_log.append("No modifiers to parse")
                x = []
                return x

            # Get actual modifiers before parsing for sanity check
            for x in modifiers_to_parse:
                if isinstance(x, bpy.types.Modifier):
                    old_actual_modifiers.append(x)
                else:
                    y = copy.copy(x.get_full_actual_modifiers_list())
                    old_actual_modifiers += y

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

        # Iterate over modifiers of object
        while parsing_modifiers:
            self._additional_info_log.append(
                    f"Parse iteration {parse_iteration}")

            # Parser sanity checks
            if parser_sanity_checks:
                if len(possible_clusters_confirmed) > len(
                        available_to_parser_cluster_types):
                    self._additional_info_log.append(
                            "Parser doesnt work, too many possible clusters")
                    return
                elif len(possible_cluster_types) > len(
                        available_to_parser_cluster_types):
                    self._additional_info_log.append(
                            "Parser doesnt work, too many possible clusters")
                    return
                elif need_another_modifier is False:
                    self._additional_info_log.append(
                            "Parser doesnt need another modifier? Why?")
                    return
                elif parse_iteration\
                        >= max_iterations:
                    self._additional_info_log.append(
                            "Parsing failed, too many iterations")
                    return

            # Add modifier to sequence
            modifier = modifiers_to_parse.pop(0)
            self._additional_info_log.append(
                    f"Adding modifier to sequence {modifier}")
            parsed_modifiers.append(modifier)
            need_another_modifier = False

            # True if parser added cluster from parsed_modifiers
            # to parse_result without successfully parsing it
            # while parsing clusters
            skipped_modifier = False

            # Info
            self._additional_info_log.append("Currently parsed modifiers:")
            for x in parsed_modifiers:
                self._additional_info_log.append(f"{x}")
            self._additional_info_log.append("All modifiers to parse:")
            for x in modifiers_to_parse:
                self._additional_info_log.append(f"{x}")
            self._additional_info_log.append(
                    "Current potentially possible cluster types:")
            for x in possible_cluster_types:
                self._additional_info_log.append(f"{x}")
            self._additional_info_log.append(
                    "Current confirmed possible cluster types:")
            for x in possible_clusters_confirmed:
                self._additional_info_log.append(f"{x}")

            # Decide what clusters types to use in checking
            if iteration_result == 'SUCCESS' or parse_iteration == 0:
                self._additional_info_log.append(
                        "Previous iteration was successfull")
                clusters_to_parse_against = available_to_parser_cluster_types
            elif iteration_result == 'POSSIBLE':
                self._additional_info_log.append("Previous iteration failed")
                clusters_to_parse_against = possible_cluster_types

            # =================
            # Checking clusters
            # =================
            # Check cluster types for compatibility with this sequence
            # of modifiers.
            for y in clusters_to_parse_against:
                possible_seq_len = len(modifiers_to_parse)\
                        + len(parsed_modifiers)

                cluster_len = y.get_this_cluster_possible_length()

                # Check if cluster is too long.
                if possible_seq_len < cluster_len:
                    result = False

                    self._additional_info_log.append(
                            f"Checking {y.get_this_cluster_name()}, {result}")
                    self._additional_info_log.append(
                            "Cant use it, not enough modifiers.")
                else:
                    result = y.check_availability(parsed_modifiers)

                    self._additional_info_log.append(
                            f"Checking {y.get_this_cluster_name()}, {result}")

                # Cluster need more modifiers than provided.
                if result == 'CONTINUE':
                    self._additional_info_log.append(
                            f"Continuing parsing, {y} need another modifier")

                    # Dont append possible_cluster_types
                    # if cluster is already there.
                    k = False
                    for x in possible_cluster_types:
                        if y.modcluster_index == x.modcluster_index:
                            self._additional_info_log.append(
                                    f"{y} is already in possible types")
                            k = True
                    if k is False:
                        new_cluster = copy.deepcopy(y)
                        possible_cluster_types.append(new_cluster)
                        self._additional_info_log.append(
                                f"Adding {y} to possible types")

                    need_another_modifier = True

                # Cluster can be used with this sequence.
                elif result == 'FOUND':
                    self._additional_info_log.append(
                            f"Cluster {y} can be used")

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
                    self._additional_info_log.append(
                            "This cluster type cant be used")

                    if iteration_result == 'POSSIBLE':
                        clusters_to_remove.append(y)

            # Removing not compatible with this modifiers sequence
            # clusters from possible types.
            for x in clusters_to_remove:
                self._additional_info_log.append(
                        "Current possible_cluster_types")
                for y in possible_cluster_types:
                    self._additional_info_log.append(f"{x}")
                self._additional_info_log.append(
                        f"Deleting {x} from possible_cluster_types")

                # Remove cluster from possible cluster types.
                possible_cluster_types.remove(x)

                self._additional_info_log.append(
                        "Current possible_cluster_types")
                for y in possible_cluster_types:
                    self._additional_info_log.append(f"{x}")
            clusters_to_remove.clear()

            # ====================
            # Cluster creation
            # ====================
            # If allowed to skip cluster or modifier if no cluster can be
            # created at all, and add it to result.
            # Then request another modifier.
            # TODO: allow_skip_modiifers variable doesnt do anything
            if (len(possible_cluster_types) == 0)\
                    & (len(possible_clusters_confirmed) == 0):
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
                self._additional_info_log.append(" ")
                self._additional_info_log.append(
                        "Trying to create new cluster")
                self._additional_info_log.append("Parsed modifiers:")
                for x in parsed_modifiers:
                    self._additional_info_log.append(f"{x}")

                # Priority select
                cluster_to_add = self._cluster_priority_select(
                        possible_clusters_confirmed)
                self._additional_info_log.append(
                        f"Decided to create {cluster_to_add}")

                # Select modifiers to add to clusters:
                modifiers_count =\
                    cluster_to_add.get_this_cluster_possible_length()
                self._additional_info_log.append(
                        f"It needs {modifiers_count} modifiers")
                self._additional_info_log.append(
                        f"parsed_modifiers are {len(parsed_modifiers)}")

                modifiers_to_add_to_cluster = []

                # Add modifiers to cluster
                i = 0
                while i < modifiers_count:
                    mod = parsed_modifiers.pop(0)
                    self._additional_info_log.append(
                            f"Deleted {mod} from modifiers_to_parse")
                    modifiers_to_add_to_cluster.append(mod)
                    self._additional_info_log.append(
                            "Added it to modifiers_to_add_to_cluster")
                    i += 1

                # TODO: Is this even possible?
                # Add not parsed modifiers back to modifiers_to_parse
                not_parsed_modifiers_count = len(parsed_modifiers)
                if not_parsed_modifiers_count > 0:
                    self._additional_info_log.append(
                            f"{not_parsed_modifiers_count} not parsed")
                    for x in reversed(parsed_modifiers):
                        self._additional_info_log.append(
                                f"Adding {x} back to modifiers_to_parse")
                        modifiers_to_parse.insert(0, x)
                    parsed_modifiers.clear()
                    self._additional_info_log.append(
                            "Cleared parsed modifiers list")

                new_cluster = copy.deepcopy(cluster_to_add)

                # Clear possible clusters list
                possible_clusters_confirmed.clear()

                # Add cluster to return list
                # parse_result.append(new_cluster)
                parsed_cluster_wrap = ['CREATE',
                                       new_cluster,
                                       modifiers_to_add_to_cluster]
                parse_result.append(parsed_cluster_wrap)

                self._additional_info_log.append(
                        "Added new cluster to result.")
                self._additional_info_log.append(
                        f"It is {len(modifiers_to_add_to_cluster)} modifiers")
                self._additional_info_log.append(" ")
                need_another_modifier = True
                iteration_result = 'SUCCESS'

            # Parser needs another modifier
            elif need_another_modifier is True:
                self._additional_info_log.append(
                        "Parser needs another modifier")
                iteration_result = 'POSSIBLE'
            else:
                self._additional_info_log.append("Parser doesnt work")
                self._additional_info_log.append(
                        "Something is wrong with cluster creation")

            # Info
            if iteration_result == 'SUCCESS':
                if skipped_modifier:
                    self._additional_info_log.append(
                            "Iteration successfull, skipped cluster")
                else:
                    self._additional_info_log.append(
                            "Iteration successfull, added new cluster")
            elif iteration_result == 'POSSIBLE':
                self._additional_info_log.append(
                        "Iteration failed, possible cluster types found")
            else:
                self._additional_info_log.append(
                        "Parser doesnt work")
                self._additional_info_log.append(
                        "Something is wrong with iteration result")
                self._additional_info_log.append(
                        "Are there enough cluster types?")
            self._additional_info_log.append(" ")

            # Decide if should continue parsing
            if len(modifiers_to_parse) == 0:
                # Stop parsing
                need_another_modifier = False
                parsing_modifiers = False
            else:
                need_another_modifier = True

            # Start next iteration
            parse_iteration += 1

        # Parse result sanity check
        if parser_sanity_checks:
            if not isinstance(parse_result, list):
                self._additional_info_log.append(
                        "Parse result is not a list, why?")
                self._additional_info_log.append(" ")
                x = []
                return x
            else:
                for x in parse_result:
                    if not isinstance(x[1], ModifierCluster):
                        self._additional_info_log.append(
                                "Parse result is not a cluster list, why?")
                        self._additional_info_log.append(" ")
                        x = []
                        return x

            new_actual_modifiers = []

            # Get actual modifiers after parsing for sanity check
            for x in parse_result:
                if x[0] == 'SKIP':
                    y2 = x[1].get_full_actual_modifiers_list()
                    y = copy.copy(y2)
                    new_actual_modifiers += y
                else:
                    y = copy.copy(x[2])
                    new_actual_modifiers += y

            old_modifiers_len = len(old_actual_modifiers)
            new_modifiers_len = len(new_actual_modifiers)

            if old_modifiers_len != new_modifiers_len:
                self._additional_info_log.append(
                        "Actual modifiers count after parsing is wrong.")
                self._additional_info_log.append(
                        f"old {old_modifiers_len}, new {new_modifiers_len} ")
                self._additional_info_log.append(" ")

        # Info
        self._additional_info_log.append("-------------")
        self._additional_info_log.append("Parse result:")
        for x in parse_result:
            self._additional_info_log.append(f"{x}")
        self._additional_info_log.append("===================================")
        self._additional_info_log.append("         Finished parsing")
        self._additional_info_log.append("===================================")
        self._additional_info_log.append(" ")

        if len(parse_result) == 0:
            return False

        return parse_result

    def _cluster_priority_select(self, clusters):
        """
        Takes list of clusters as an argument.
        Returns cluster that have higher priority when
        deciding what cluster to create.
        """
        self._additional_info_log.append("Selecting cluster.")

        # Highest priority.
        y = clusters[0].get_this_cluster_priority()

        # Longest.
        k = clusters[0].get_this_cluster_possible_length()

        # Restored cluster length.
        m = None

        result = clusters[0]

        found_restored_cluster = False

        # Get first restored cluster
        for x in clusters:
            if 'RESTORED' in x.get_this_cluster_tags():
                self._additional_info_log.append("Selected RESTORED cluster.")
                m = x.get_this_cluster_possible_length()
                result = x
                found_restored_cluster = True
                break

        # If no restored clusters, use priority.
        if not found_restored_cluster:
            for x in clusters:
                # If cluster has higher priority.
                if x.get_this_cluster_priority() > y:

                    # And longer or same length.
                    if x.get_this_cluster_possible_length() >= k:
                        y = x.get_this_cluster_priority()
                        k = x.get_this_cluster_possible_length()
                        result = x

                # Or it is just longer.
                elif x.get_this_cluster_possible_length() > k:
                    y = x.get_this_cluster_priority()
                    k = x.get_this_cluster_possible_length()
                    result = x

        # If restored clusters, only use length
        else:
            for x in clusters:
                self._additional_info_log.append(
                        f"Checking {x}, its tags is")
                self._additional_info_log.append(
                        f"{x.get_this_cluster_tags()}")
                if 'RESTORED' in x.get_this_cluster_tags():
                    if x.get_this_cluster_possible_length() > m:
                        m = x.get_this_cluster_possible_length()
                        result = x

        self._additional_info_log.append(f"Selected {result} cluster.")
        self._additional_info_log.append(f"{result.get_this_cluster_tags()}")
        return result

    # ====================
    # Parse result processing
    # ====================
    def _unwrap_parse_result(self, parse_result, tags):
        """
        Returns parse result filtered by parser decision.
        Returns False, if any errors in parse result.
        """

        unwrap = []

        # Check if parse result is a list.
        if not isinstance(parse_result, list):
            return False

        for x in parse_result:

            # Check if element is a list.
            if not isinstance(x, list):
                return False

            # Check if it has parser decision already
            if not isinstance(x[0], str):
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

        self._additional_info_log.append("---------------------")
        self._additional_info_log.append("Initializing clusters.")

        # Clusters list that will be returned.
        clusters = []

        # Check if parse result is a list.
        if not isinstance(parse_result, list):
            return False

        # Check if no clusters were parsed.
        if len(parse_result) == 0:
            return clusters

        new_clusters_names = copy.copy(clusters_names)

        for x in parse_result:
            self._additional_info_log.append(f"Initializing {x}")

            # Check if element is a list.
            if not isinstance(x, list):
                return False

            # If parser skipped this cluster, just skip it as well.
            if x[0] == 'SKIP':
                self._additional_info_log.append("Skipped cluster")

                # Add to result
                clusters.append(x[1])

            # If parsed successfully.
            elif x[0] == 'CREATE':
                self._additional_info_log.append("Creating cluster")

                # Initialize cluster
                cluster = self._initialize_cluster(
                        x, new_clusters_names)

                if cluster is False:
                    return False

                new_clusters_names.append(cluster[1].get_this_cluster_name())

                # Add to result
                clusters.append(x[1])

        self._additional_info_log.append("Created clusters: ")
        for x in clusters:
            self._additional_info_log.append(f"{x}")

        return clusters

    def _initialize_cluster(
            self, parse_result_element, clusters_names=None):

        if clusters_names is None:
            clusters_names = []

        x = parse_result_element

        self._additional_info_log.append("Initializing cluster")

        # Set its modifiers.
        if not x[1].set_this_cluster_modifiers(x[2]):
            return False

        x[1]._object = self._object

        # Layer-specific.
        if x[1].has_clusters():
            if x[1].get_list_length() > 0:
                x[1]._mod = x[1].get_first()

        # Set cluster name.
        x[1] = self._cluster_number_format(
                x[1], clusters_names)
        return x

    def _cluster_number_format(
            self, cluster, clusters_names=None):
        """
        Changes cluster's custom name, if cluster with same default
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

    # TODO: move to util
    def _get_clusters_names(self, clusters):
        """
        Returns list of custom names from list of clusters.
        """
        result = []
        for x in clusters:
            result.append(x.get_this_cluster_name())

        return result

    # ====================================
    # TODO: this methods should be removed.
    # maybe not idk.
    # ====================================
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
        cluster_types = []
        if not no_available_types:
            cluster_types += self._available_cluster_types
        if additional_types is not None:
            compatible_additional = []
            for x in additional_types:
                if x.has_clusters():
                    compatible_additional.append(x)
            cluster_types += compatible_additional

        simple_clusters = []
        e = copy.copy(modifiers_to_parse)
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
