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

import json

from ..dummy_modifiers import DummyBlenderModifier


class ClusterTrait():
    """
    This ModifiersList trait should be in every
    cluster used in ClustersList.
    """

    def __init__(self, *args,
                 cluster_name=None,
                 cluster_type=None,
                 modifiers_by_type=None,

                 # Arguments that can be skipped
                 modifiers_by_name=None,
                 cluster_tags=None,
                 cluster_priority=None,
                 cluster_is_sane=None,
                 cluster_createable=None,
                 dont_define_cluster=None,
                 **kwargs
                 ):

        super().__init__(no_obj=True, *args, **kwargs)

        # ===============================================================
        # This is variables that should be defined in ModifiersCluster type.
        # ===============================================================

        # Name that should be returned by default to ModifiersList
        self._MODCLUSTER_NAME = None

        # Type that should be returned to ModifiersList
        self._MODCLUSTER_TYPE = None

        # Priority interpreted by parser
        self._MODCLUSTER_PRIORITY = None

        # If true, does not allows to clear cluster.
        self._MODCLUSTER_NO_CLEAR = False

        # ModifiersCluster tags
        self._MODCLUSTER_DEFAULT_TAGS = []

        # List of lists of possible modifier types that this
        # ModifiersCluster should consists of
        # Takes modifier order into consideration
        # If not at index 0, can be 'ANY'
        self._MODCLUSTER_MODIFIERS_BY_TYPE = [[]]

        # List of lists of possible names for every modifier
        # in _MODCLUSTER_MODIFIERS_BY_TYPE
        # Takes modifier order into consideration
        # Can be 'ANY'
        self._MODCLUSTER_MODIFIERS_BY_POSSIBLE_NAMES = [[]]

        # Can cluster's modifiers list be changed after initialization?
        # why tho
        self._MODCLUSTER_DYNAMIC = False

        # TODO: why
        # Variable for nested clusters.
        # Use modifier clusters instead of usual modifier references.
        self._MODIFIER_CLUSTERS = False

        # Force skip cluster sanity check.
        # Should be False.
        self._MODCLUSTER_IS_SANE = False

        # Can this cluster be created?
        # In other words, can its _MODIFIERS_BY_TYPE be used
        # to create new modifiers on object.
        self._MODCLUSTER_CREATEABLE = False

        # Additional info log.
        self._MODCLUSTER_V = False

        if not dont_define_cluster:

            # Set cluster type name.
            if isinstance(cluster_name, str):
                if len(cluster_name) == 0:
                    raise ValueError
                self._MODCLUSTER_NAME = cluster_name
            else:
                raise TypeError

            # Set cluster type that will be returned to ClustersList.
            if isinstance(cluster_type, str):
                if len(cluster_type) == 0:
                    raise ValueError
                self._MODCLUSTER_TYPE = cluster_type
            else:
                raise TypeError

            # Set cluster type default tags.
            if isinstance(cluster_tags, list):
                for x in cluster_tags:
                    if not isinstance(x, str):
                        raise TypeError
                self._MODCLUSTER_DEFAULT_TAGS = cluster_tags
            elif cluster_tags is None:
                self._MODCLUSTER_DEFAULT_TAGS = []
            else:
                raise TypeError

            # Set cluster type modifiers by type.
            if isinstance(modifiers_by_type, list):
                for x in modifiers_by_type:
                    if not isinstance(x, str):
                        if isinstance(x, list):
                            for y in x:
                                if not isinstance(y, str):
                                    raise TypeError
                        else:
                            raise TypeError
                self._MODCLUSTER_MODIFIERS_BY_TYPE = modifiers_by_type
            else:
                raise TypeError

            # Set cluster type modifiers by names.
            if isinstance(modifiers_by_name, list):
                for x in modifiers_by_name:
                    if not isinstance(x, str):
                        if isinstance(x, list):
                            for y in x:
                                if not isinstance(y, str):
                                    raise TypeError
                        else:
                            raise TypeError
                self._MODCLUSTER_MODIFIERS_BY_POSSIBLE_NAMES\
                    = modifiers_by_name
            elif modifiers_by_name is None:
                self._MODCLUSTER_MODIFIERS_BY_POSSIBLE_NAMES = []
                for x in self._MODCLUSTER_MODIFIERS_BY_TYPE:
                    self._MODCLUSTER_MODIFIERS_BY_POSSIBLE_NAMES.append('ANY')
            else:
                raise TypeError

            # Set cluster priority for parser.
            if isinstance(cluster_priority, int):
                self._MODCLUSTER_PRIORITY = cluster_priority
            elif cluster_priority is None:
                self._MODCLUSTER_PRIORITY = 0
            else:
                raise TypeError

            # Allow cluster to skip sanity check.
            if cluster_is_sane is True:
                self._MODCLUSTER_IS_SANE = True
            else:
                self._MODCLUSTER_IS_SANE = False

            # Allow to create cluster with its modifers
            if cluster_createable is True:
                self._MODCLUSTER_CREATEABLE = True
            else:
                self._MODCLUSTER_CREATEABLE = False

        # -------------------------------------------
        # Modifiers names that can be sometimes used
        # instead of default ones.
        self._modcluster_specified_modifier_names = []

        # Custom name that can be changed in runtime.
        self._modcluster_custom_name = None

        # Custom tags that can be changed in runtime.
        self._modcluster_custom_tags = []

        # Initialized.
        self._modcluster_initialized = False

        # Modifiers list.
        self._modifiers_list = []

        # Sorting rules.
        self._sorting_rules = []

        # Should this cluster content be shown collapsed in ui?
        # Also stops recursive active_modifier_get_deep()
        self.modcluster_collapsed = True

        # Check cluster sanity.
        if not dont_define_cluster\
                and not self._MODCLUSTER_IS_SANE\
                and not self.check_this_cluster_sanity():
            raise ValueError

    def __str__(self):
        result = f"{self.get_this_cluster_default_name()} cluster, "
        result = result + f"{len(self._modifiers_list)} "
        if self.has_clusters():
            result = result + "clusters, "
        else:
            result = result + "modifiers, "
        result = result + f"index {self.modcluster_index}, "
        result = result + f"tags {self.get_this_cluster_tags()}, "
        return result

    # Collapsed
    @property
    def collapsed(self):
        return self.modcluster_collapsed

    @collapsed.setter
    def collapsed(self, collapsed_val):
        if collapsed_val:
            self.modcluster_collapsed = True
        elif not collapsed_val:
            self.modcluster_collapsed = False

    @collapsed.deleter
    def collapsed(self, collapsed_val):
        del(self.modcluster_collapsed)

    # Cluster name
    @property
    def name(self):
        return self.get_this_cluster_name()

    @name.setter
    def name(self, cluster_name):
        return self.set_this_cluster_custom_name(cluster_name)

    # Cluster type
    @property
    def type(self):
        return self.get_this_cluster_type()

    # ============================
    # Methods reserved for objects
    # ============================
    def modcluster_extra_availability_check(self, modifiers):
        """
        Additional method reserved for custom types.
        Checks if modifiers can be considered as
        ModifiersCluster of this type.

        Returns CONTINUE if can potentially be available,
        but missing some modifiers that can be found later.
        Returns FOUND if modifiers can be considered
        ModifiersCluster of this type.
        Returns False, if not usable.
        Returns None, if no decision.
        """
        return

    def check_this_cluster_sanity_custom(self):
        """
        Method reserved for object-specific sanity checks.

        Should return True or False.
        """
        return True

    # ============================
    # ModifiersClustersList actions
    # ============================
    # TODO: rework this
    # TODO: does this actually require full clusters list?
    def cluster_being_moved(self, modifiers_clusters_list, direction):
        """
        Method reserved for object-specific actions on cluster move in
        ModifiersClustersList.

        Passed arguments are list this cluster belongs to and direction
        as one of UP or DOWN.

        Returns True if cluster can be successfully moved.
        Returns False if cluster shouldnt be moved.
        """
        return True

    def cluster_being_deconstructed(self, clusters_list):
        """
        Method reserved for object-specific actions on cluster
        deconstruction in ModifiersClustersList.

        Passed arguments are list this cluster belongs to.

        Returns True if cluster can be successfully moved.
        Returns False if cluster shouldnt be moved.
        """
        return True

    def cluster_being_removed(self, modifiers_clusters_list):
        """
        Method reserved for object-specific actions on cluster remove in
        ModifiersClustersList.

        Passed arguments are list this cluster belongs to.

        Returns True if cluster can be successfully removed.
        Returns False if cluster shouldnt be removed.
        """
        return True

    def cluster_being_applied(self, modifiers_clusters_list):
        """
        Method reserved for object-specific actions on cluster apply in
        ModifiersClustersList.

        Passed arguments are list this cluster belongs to.

        Returns True if cluster can be successfully applied.
        Returns False if cluster shouldnt be applied.
        """
        return True

    # ===========================
    # ModifiersCluster methods
    # ===========================
    def is_complex(self):
        """
        Checks if this cluster cant be considered as usual modifier.

        Returns True if modifier cluster consists of more than
        one blender modifier.
        Also returns True if has no modifiers at all.
        """

        if self.get_list_length() != 1:
            return True
        return False

    def has_clusters(self):
        """
        Checks if this cluster have clusters in it.
        Returns False if this cluster consists of modifiers or something
        else.
        """
        return False

    def get_this_cluster_type(self):
        """
        Returns this ModifiersCluster's type
        """
        return self._MODCLUSTER_TYPE

    def get_this_cluster_name(self):
        """
        Returns this ModifiersCluster's custom name, or default name.
        """
        if self._modcluster_custom_name is not None:
            return self._modcluster_custom_name
        else:
            return self._MODCLUSTER_NAME

    def get_this_cluster_custom_name(self):
        """
        Returns this ModifiersCluster's custom name.
        """
        return self._modcluster_custom_name

    def get_this_cluster_default_name(self):
        """
        Returns this ModifiersCluster's default name.
        """
        return self._MODCLUSTER_NAME

    def set_this_cluster_custom_name(self, cluster_name):
        """
        Sets cluster custom cluster name.
        Returns True or False, if cluster is not editable.
        """
        if isinstance(cluster_name, str):
            self._modcluster_custom_name = cluster_name
        else:
            raise TypeError

    # ===========================
    # Cluster tags
    # ===========================
    def get_this_cluster_tags(self):
        """
        Returns this ModifiersCluster's custom tags, or default tags.
        """
        return self._MODCLUSTER_DEFAULT_TAGS + self._modcluster_custom_tags

    def add_tag_to_this_cluster(self, custom_tag):
        """
        Set this ModifiersCluster's custom tags.
        Takes string as an argument.
        Returns True if successfully added tag.
        """
        if isinstance(custom_tag, str):
            if custom_tag not in self._modcluster_custom_tags:
                self._modcluster_custom_tags.append(custom_tag)
                return True
            else:
                return False
        else:
            raise TypeError

    # TODO: this is not correct implementation
    def remove_tag_from_this_cluster(self, custom_tag):
        """
        Remove this ModifiersCluster's custom tags.
        Takes string as an argument.
        Returns True if successfully removed tag.
        Returns False if no such tag or cant remove.
        """
        y = []
        result = False
        for x in self._modcluster_custom_tags:
            if x == custom_tag:
                y.append(x)
                result = True

        for x in y:
            self._modcluster_custom_tags.remove(x)

        return result

    # ===========================
    # Initializing cluster
    # ===========================
    def set_this_cluster_modifiers(self, modifiers):
        """
        Replaces list of modifiers with modifiers
        Returns True or False, if cluster is not editable
        """

        if not isinstance(modifiers, list):
            raise TypeError
        if len(modifiers) == 0:
            raise ValueError
        for x in modifiers:
            if not isinstance(x, DummyBlenderModifier)\
                    and not isinstance(x, ClusterTrait):
                raise TypeError

        # If havent set modifiers already
        if self._modcluster_initialized is False:
            self._modifiers_list = modifiers
            self._modcluster_initialized = True
            self._mod = self._modifiers_list[0]
            return True

        # If allowed to reset modifiers
        elif self._MODCLUSTER_DYNAMIC:
            self._modifiers_list = modifiers
            self._mod = self._modifiers_list[0]
            return True

        else:
            return False

    # ===========================
    # Clusters sorting
    # ===========================
    def add_sorting_rule(self, sorting_rule):
        """
        Add new sorting rule for this cluster or
        replace existing one.

        Returns True or False, if cluster not sortable.
        """

        if 'NO_SORT' in self.get_this_cluster_tags():
            return False

        self.remove_sorting_rule(sorting_rule.name)

        self._sorting_rules.append(sorting_rule)
        return True

    def remove_sorting_rule(self, sorting_rule_name):
        """
        Removes sorting rule by name.

        Returns True or False, if no such sorting
        rule.
        """

        removed_sorting_rule = False
        r = []
        for x in self._sorting_rules:
            if x.name == sorting_rule_name:
                r += x
        for x in r:
            self._sorting_rules.remove(x)
            removed_sorting_rule = True
        return removed_sorting_rule

    def get_sorting_rules(self):
        """
        Returns sorting rules for this cluster.
        Returns empty list, if cluster disabled
        sorting.
        """
        if 'NO_SORT' in self.get_this_cluster_tags():
            return []
        else:
            return self._sorting_rules

    # ==========
    # Parsing
    # ==========
    def get_this_cluster_possible_length(self):
        """
        Returns maximum possible modifiers sequence length for this cluster.
        """
        return len(self._MODCLUSTER_MODIFIERS_BY_TYPE)

    def get_this_cluster_priority(self):
        """
        Returns priority for this cluster in parsing.
        """
        return self._MODCLUSTER_PRIORITY

    def check_availability(self, modifiers):
        """
        Checks if sequence of modifiers or clusters can be
        considered ModifiersCluster of this type.

        Returns CONTINUE if can potentially be available,
        but missing some modifiers that can be found later.
        Returns FOUND if modifiers or clusters can be considered
        ModifiersCluster of this type.
        Returns False, if not usable.
        """

        for mod in modifiers:
            if isinstance(mod, DummyBlenderModifier):
                pass
            elif isinstance(mod, ClusterTrait):
                pass
            elif isinstance(mod, DummyBlenderModifier):
                pass
            else:
                raise TypeError(f'{mod} is not a modifier or cluster.')

        # How many modifiers are correct?
        x = 0

        # How many modifiers should be correct?
        x2 = len(self._MODCLUSTER_MODIFIERS_BY_TYPE)

        # Iteration number
        y = 0

        # Iterate over provided modifiers sequence
        for mod in modifiers:

            modifiers_by_type = self._MODCLUSTER_MODIFIERS_BY_TYPE

            # Check modifiers by types
            if (modifiers_by_type[y] != ['ANY'])\
                    and (modifiers_by_type[y] != 'ANY'):

                # Check modifier type
                if isinstance(mod, ClusterTrait):
                    if mod.type not in modifiers_by_type[y]:
                        return 'WRONG CLUSTER TYPE'
                else:
                    if mod.type not in modifiers_by_type[y]:
                        return 'WRONG ACTUAL MODIFIER TYPE'

            # Use specific names list, if there is one
            if len(self._modcluster_specified_modifier_names) != 0:
                modifiers_by_names\
                        = self._modcluster_specified_modifier_names
            else:
                modifiers_by_names\
                        = self._MODCLUSTER_MODIFIERS_BY_POSSIBLE_NAMES

            # Check name
            if (modifiers_by_names[y] != ['ANY'])\
                    and (modifiers_by_names[y] != 'ANY'):

                # Check modifiers names
                if isinstance(mod, ClusterTrait):
                    if isinstance(modifiers_by_names[y], list):
                        if mod.name\
                                not in modifiers_by_names[y]:
                            return 'WRONG CLUSTER NAME'
                    else:
                        if mod.name\
                                != modifiers_by_names[y]:
                            return 'WRONG CLUSTER NAME'
                else:
                    if isinstance(modifiers_by_names[y], list):
                        if mod.name not in modifiers_by_names[y]:
                            return 'WRONG ACTUAL MODIFIER NAME'
                    else:
                        if mod.name != modifiers_by_names[y]:
                            return 'WRONG ACTUAL MODIFIER NAME'

            x += 1
            if x == x2:
                return 'FOUND'
            elif (x < x2) & (x == len(modifiers)):
                return 'CONTINUE'
            y += 1

        # Additional checks reserved for custom types
        additional_checks = self.modcluster_extra_availability_check(
                modifiers)

        if additional_checks is not None:
            return additional_checks

        return None

    def check_this_cluster_sanity(self):
        """
        Checks if this cluster type would work properly.

        Reccomended to check every time enabling new
        cluster type or changing existing one.

        Basically should always return False, because
        modifiers clusters are kinda unusable and
        overengeneered.

        Returns True if not found any errors.
        Returns False if something is wrong.
        """

        # Additional checks
        if not self.check_this_cluster_sanity_custom():
            return False

        # If specified that cluster is sane
        if self._MODCLUSTER_IS_SANE:
            return True

        l_1 = self._MODCLUSTER_MODIFIERS_BY_TYPE
        len_1 = len(l_1)

        l_2 = self._MODCLUSTER_MODIFIERS_BY_POSSIBLE_NAMES
        len_2 = len(l_2)

        if len(self._modcluster_specified_modifier_names) > 0:
            if len_2 != len(self._modcluster_specified_modifier_names):
                raise ValueError(
                        'Length of specified modifiers names is wrong.')
        if len_1 != len_2:
            raise ValueError(
                    f'Length of types ({l_1}) and names ({l_2}) is different.')
        if len_1 == 0:
            raise ValueError(
                    'Length of modifiers types cant be 0.')
        if self._MODCLUSTER_MODIFIERS_BY_TYPE[0] == ['ANY']:
            raise ValueError(
                    'First modifier cant be any, specify modifier type.')
        for mod_types in self._MODCLUSTER_MODIFIERS_BY_TYPE:
            if isinstance(mod_types, list):
                if len(mod_types) == 0:
                    raise ValueError('Modifier types length is 0.')
        for mod_names in self._MODCLUSTER_MODIFIERS_BY_POSSIBLE_NAMES:
            if isinstance(mod_names, list):
                if len(mod_names) == 0:
                    raise ValueError('Modifier names length is 0.')
        return True

    # ===================
    # Cluster visibility
    # ===================
    def get_this_cluster_visibility(self):
        """
        Returns list with info about this cluster visability
        """
        y1 = []
        y2 = []
        y3 = []
        y4 = []

        mods = self.get_full_actual_modifiers_list()
        for mod in mods:
            y1.append(mod.show_render)
            y2.append(mod.show_viewport)
            y3.append(mod.show_in_editmode)
            y4.append(mod.show_on_cage)

        y = [y1, y2, y3, y4]

        result = []

        for x in y:
            if True in x:
                if False in x:
                    result.append('HALF')
                else:
                    result.append('ON')
            else:
                result.append('OFF')
        return result

    def set_this_cluster_visibility(self,
                                    vis_settings=None
                                    ):
        """
        Sets this cluster visibility.
        Takes list as an argument.
        """
        if vis_settings is None:
            vis_settings = [None, None, None, None]

        y1, y2, y3, y4 = vis_settings

        # y1 = vis_settings[0]
        # y2 = vis_settings[1]
        # y3 = vis_settings[2]
        # y4 = vis_settings[3]

        mods = self.get_full_actual_modifiers_list()

        if y1 is not None:
            for mod in mods:
                mod.show_render = y1

        if y2 is not None:
            for mod in mods:
                mod.show_viewport = y2

        if y3 is not None:
            for mod in mods:
                mod.show_in_editmode = y3

        if y4 is not None:
            for mod in mods:
                mod.show_on_cage = y4

    def toggle_this_cluster_visibility(self, vis_settings=None):
        """
        Toggles this cluster visibility.
        If not all actual modifiers have some kind
        of visibility, turns it off completely.

        Takes list as an argument.
        """
        if vis_settings is None:
            vis_settings = [False, False, False, False]

        if True not in vis_settings:
            return

        old_cluster_vis = self.get_this_cluster_visibility()
        new_cluster_vis = []

        i = 0

        for x in old_cluster_vis:
            if vis_settings[i] is True:
                if x == 'HALF':
                    new_cluster_vis.append(False)
                elif x == 'ON':
                    new_cluster_vis.append(False)
                elif x == 'OFF':
                    new_cluster_vis.append(True)
            else:
                new_cluster_vis.append(None)

            i += 1

        self.set_this_cluster_visibility(new_cluster_vis)

    # =======================================
    # Utility
    # =======================================
    def serialize_this_cluster_type(self):
        x = {}

        if self.has_clusters():
            c = 'ClustersLayer'
        else:
            c = 'ModifiersCluster'

        x.update({'cluster_class': f'{c}'})
        x.update({'cluster_name': self._MODCLUSTER_NAME})
        x.update({'cluster_type': self._MODCLUSTER_TYPE})
        x.update({'modifiers_by_types':
                 self._MODCLUSTER_MODIFIERS_BY_TYPE})
        x.update({'modifiers_by_names':
                 self._MODCLUSTER_MODIFIERS_BY_POSSIBLE_NAMES})
        x.update({'cluster_tags': self._MODCLUSTER_DEFAULT_TAGS})
        x.update({'cluster_priority': self._MODCLUSTER_PRIORITY})
        x.update({'cluster_is_sane': self._MODCLUSTER_IS_SANE})
        x.update({'cluster_createable': self._MODCLUSTER_CREATEABLE})
        result = json.dumps(x)
        return result

    # TODO: can be removed
    def clear_this_cluster(self):
        """
        Resets all unnecessary for cluster type
        attributes in already initialized cluster.

        Returns True or False, if cant reset this
        type of clusters.
        """

        if self._MODCLUSTER_NO_CLEAR:
            return False

        self._mod = None
        self._modifiers_list = []
        self._object = None
        self._modcluster_specified_modifier_names = []
        self._modcluster_custom_name = None
        self._modcluster_custom_tags = []
        self.modcluster_index = None
        self.collapsed = True
        self._modcluster_initialized = False
        return True
